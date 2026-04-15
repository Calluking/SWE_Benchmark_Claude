#!/usr/bin/env bash
# Run one SWE-bench Lite instance with the installed Claude Code CLI.
#
# This script logs:
# - the exact prompt and metadata used for the run
# - raw Claude stream-json output
# - Claude debug logs
# - captured stderr/stdout from the launcher
# - token usage extracted from the stream log
#
# Usage:
#   ./scripts/run_swe_lite_one_claude.sh
#   SWE_LITE_INDEX=1 ./scripts/run_swe_lite_one_claude.sh
#   SWE_LITE_SPLIT=test SWE_LITE_INDEX=0 ./scripts/run_swe_lite_one_claude.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SWE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${SWE_ROOT}/.." && pwd)"
DATASET_ROOT="${DATASET_ROOT:-${SWE_ROOT}/data/SWE-bench_Lite}"
WORK_ROOT="${WORK_ROOT:-${SWE_ROOT}/runs}"
SPLIT="${SWE_LITE_SPLIT:-dev}"
INDEX="${SWE_LITE_INDEX:-1}"
EMPTY_MCP="${EMPTY_MCP:-${SCRIPT_DIR}/empty_mcp.json}"
OUTPUT_FORMAT="${SWE_LITE_OUTPUT_FORMAT:-stream-json}"
ENABLE_DEBUG="${SWE_LITE_ENABLE_DEBUG:-1}"
SAVE_STREAM="${SWE_LITE_SAVE_STREAM:-1}"
METRICS_TSV="${SWE_LITE_METRICS_TSV:-${SWE_ROOT}/runs/run_metrics.tsv}"
HEARTBEAT_SEC="${SWE_LITE_HEARTBEAT_SEC:-0}"
HB_PID=""

_ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
log() { echo "[$(_ts)] $*" >&2; }

_heartbeat_stop() {
  if [[ -n "${HB_PID:-}" ]] && kill -0 "${HB_PID}" 2>/dev/null; then
    kill "${HB_PID}" 2>/dev/null || true
    wait "${HB_PID}" 2>/dev/null || true
  fi
  HB_PID=""
}

cd "${SWE_ROOT}"

if ! command -v claude >/dev/null 2>&1; then
  echo "claude not on PATH." >&2
  exit 1
fi
log "preparing SWE-bench Lite instance split=${SPLIT} index=${INDEX}"
IFS=$'\t' read -r INSTANCE_ID WORK_DIR < <(
  python3 "${SCRIPT_DIR}/prepare_swe_lite_one.py" \
    --no-mcp \
    --dataset-root "${DATASET_ROOT}" \
    --split "${SPLIT}" \
    --index "${INDEX}" \
    --work-root "${WORK_ROOT}"
)

INSTANCE_JSON="${WORK_DIR}/instance.json"
REPO_SLUG="$(python3 -c "import json; print(json.load(open('${INSTANCE_JSON}'))['repo'])")"
BASE_COMMIT="$(python3 -c "import json; print(json.load(open('${INSTANCE_JSON}'))['base_commit'])")"
REPO_DIR="${WORK_DIR}/repo"
REMOTE="https://github.com/${REPO_SLUG}.git"

RUN_LOG_DIR="${WORK_DIR}/logs"
mkdir -p "${RUN_LOG_DIR}"
PROMPT_FILE="${RUN_LOG_DIR}/prompt.txt"
STDOUT_LOG="${RUN_LOG_DIR}/claude_stream.jsonl"
STDERR_LOG="${RUN_LOG_DIR}/claude_stderr.log"
DEBUG_LOG="${RUN_LOG_DIR}/claude_debug.log"
COMMAND_LOG="${RUN_LOG_DIR}/command.sh"
META_JSON="${RUN_LOG_DIR}/run_meta.json"

cat >"${PROMPT_FILE}" <<'EOF'
Read TASK.md in the current directory and complete the SWE-bench Lite task.
Use only built-in Claude Code tools. Work in the repo/ subdirectory.
Keep a careful log in your final response of what you changed and how tests went.
EOF

cat >"${COMMAND_LOG}" <<EOF
#!/usr/bin/env bash
claude -p --dangerously-skip-permissions --strict-mcp-config \
  --add-dir "${WORK_DIR}" \
  --output-format stream-json \
  --include-partial-messages \
  --include-hook-events \
  --verbose \
  ${ENABLE_DEBUG:+--debug-file "${DEBUG_LOG}"} \
  --no-session-persistence \
  --name "${INSTANCE_ID}" \
  "$(cat "${PROMPT_FILE}")"
EOF

cat >"${META_JSON}" <<EOF
{
  "instance_id": "${INSTANCE_ID}",
  "split": "${SPLIT}",
  "index": ${INDEX},
  "work_dir": "${WORK_DIR}",
  "repo": "${REPO_SLUG}",
  "base_commit": "${BASE_COMMIT}",
  "dataset_root": "${DATASET_ROOT}",
  "stdout_log": "${STDOUT_LOG}",
  "stderr_log": "${STDERR_LOG}",
  "debug_log": "${DEBUG_LOG}"
}
EOF

log "instance_id=${INSTANCE_ID}"
log "work_dir=${WORK_DIR}"
log "repo=${REPO_SLUG} @ ${BASE_COMMIT}"
log "logs=${RUN_LOG_DIR}"

if [[ ! -d "${REPO_DIR}/.git" ]]; then
  log "cloning repo into ${REPO_DIR}"
  mkdir -p "$(dirname "${REPO_DIR}")"
  GIT_TERMINAL_PROMPT=0 git clone --progress "${REMOTE}" "${REPO_DIR}"
else
  log "repo already present"
fi

log "checking out ${BASE_COMMIT}"
if git -C "${REPO_DIR}" cat-file -e "${BASE_COMMIT}^{commit}" 2>/dev/null; then
  log "commit already local"
else
  git -C "${REPO_DIR}" fetch --progress origin "${BASE_COMMIT}" 2>&1 || git -C "${REPO_DIR}" fetch --progress origin
fi
git -C "${REPO_DIR}" checkout --quiet "${BASE_COMMIT}"

export NO_PROXY="127.0.0.1,localhost,::1,${NO_PROXY:-}"

CLAUDE_ARGS=(
  -p
  --dangerously-skip-permissions
  --strict-mcp-config
  --add-dir "${WORK_DIR}"
  --output-format "${OUTPUT_FORMAT}"
  --include-partial-messages
  --include-hook-events
  --no-session-persistence
  --name "${INSTANCE_ID}"
)
if [[ "${OUTPUT_FORMAT}" == "stream-json" ]]; then
  CLAUDE_ARGS+=(--verbose)
fi
if [[ "${ENABLE_DEBUG}" == "1" ]]; then
  CLAUDE_ARGS+=(--debug-file "${DEBUG_LOG}")
fi

if [[ "${HEARTBEAT_SEC}" != "0" ]]; then
  (
    while true; do
      sleep "${HEARTBEAT_SEC}"
      log "claude still running ..."
    done
  ) &
  HB_PID=$!
  trap '_heartbeat_stop' EXIT
fi

cd "${WORK_DIR}"
log "launching claude"
set +e
if [[ "${SAVE_STREAM}" == "1" ]]; then
  claude "${CLAUDE_ARGS[@]}" "$(cat "${PROMPT_FILE}")" \
    2> >(tee "${STDERR_LOG}" >&2) \
    | tee "${STDOUT_LOG}"
  CLAUDE_EC=${PIPESTATUS[0]}
else
  claude "${CLAUDE_ARGS[@]}" "$(cat "${PROMPT_FILE}")" \
    2> >(tee "${STDERR_LOG}" >&2)
  CLAUDE_EC=$?
fi
set -e

_heartbeat_stop
trap - EXIT

log "claude exited with code ${CLAUDE_EC}"

if [[ "${SAVE_STREAM}" == "1" ]]; then
  log "extracting token usage to ${METRICS_TSV}"
  python3 "${SCRIPT_DIR}/extract_stream_usage.py" \
    --stream-log "${STDOUT_LOG}" \
    --append-tsv "${METRICS_TSV}" \
    --set instance_id="${INSTANCE_ID}" \
    --set split="${SPLIT}" \
    --set lite_index="${INDEX}" \
    --set repo="${REPO_SLUG}" \
    --set base_commit="${BASE_COMMIT}" \
    --set exit_code="${CLAUDE_EC}" \
    --set output_format="${OUTPUT_FORMAT}"
fi

log "done"
exit "${CLAUDE_EC}"
