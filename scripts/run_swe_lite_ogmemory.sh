#!/usr/bin/env bash
# Run one SWE-bench Lite instance with Claude Code CLI + oG-Memory MCP.
#
# Same as run_swe_lite_one_claude.sh but loads the og-memory MCP server
# so that oG-Memory hooks (inject_memory / extract_memory) fire and the
# og-memory MCP tools are available in the session.
#
# Prerequisites:
#   - ./setup_ogmemory.sh must have been run (creates .venv and .mcp.json)
#   - AGFS server must be running:  agfs-server  (see oG-Memory/ENV.md)
#   - ANTHROPIC_API_KEY must be set
#
# Usage:
#   ./scripts/run_swe_lite_ogmemory.sh
#   SWE_LITE_INDEX=1 ./scripts/run_swe_lite_ogmemory.sh
#   SWE_LITE_SPLIT=test SWE_LITE_INDEX=0 ./scripts/run_swe_lite_ogmemory.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SWE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${SWE_ROOT}/.." && pwd)"
DATASET_ROOT="${DATASET_ROOT:-${REPO_ROOT}/SWE-bench/data/SWE-bench_Lite}"
WORK_ROOT="${WORK_ROOT:-${SWE_ROOT}/runs}"
SPLIT="${SWE_LITE_SPLIT:-test}"
INDEX="${SWE_LITE_INDEX:-1}"
MCP_CONFIG="${SWE_ROOT}/.mcp.json"
MODEL="${SWE_LITE_MODEL:-claude-haiku-4-5-20251001}"
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

# -- Pre-flight checks --------------------------------------------------------
if ! command -v claude >/dev/null 2>&1; then
  echo "claude not on PATH. Run: npm i -g @anthropic-ai/claude-code" >&2
  exit 1
fi

if [[ ! -f "${MCP_CONFIG}" ]]; then
  echo "ERROR: .mcp.json not found at ${MCP_CONFIG}" >&2
  echo "Run ./setup_ogmemory.sh first to generate it." >&2
  exit 1
fi

VENV_PYTHON="$(python3 -c "import json; cfg=json.load(open('${MCP_CONFIG}')); print(cfg['mcpServers']['og-memory']['command'])")"
if [[ ! -x "${VENV_PYTHON}" ]]; then
  echo "ERROR: python in .mcp.json not found: ${VENV_PYTHON}" >&2
  echo "Re-run ./setup_ogmemory.sh to regenerate .mcp.json for this machine." >&2
  exit 1
fi

log "og-memory MCP config : ${MCP_CONFIG}"
log "og-memory python     : ${VENV_PYTHON}"
log "model                : ${MODEL}"

# -- MCP health check: verify the og-memory server can start and respond ------
log "checking og-memory MCP server health..."
MCP_HEALTH_CHECK=$(
  printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"health-check","version":"1.0"}}}\n' \
  | "${VENV_PYTHON}" -m claudecode_plugin.mcp_server 2>/dev/null \
  | head -1 \
  || true
)
if python3 -c "import json,sys; d=json.loads(sys.argv[1]); exit(0 if 'result' in d else 1)" "${MCP_HEALTH_CHECK}" 2>/dev/null; then
  MCP_VERSION="$(python3 -c "import json,sys; d=json.loads(sys.argv[1]); print(d['result']['serverInfo']['version'])" "${MCP_HEALTH_CHECK}" 2>/dev/null || echo "unknown")"
  log "og-memory MCP health : OK (server=og-memory v${MCP_VERSION})"
else
  echo "ERROR: og-memory MCP server did not respond correctly." >&2
  echo "  Check that AGFS is running: agfs-server (see oG-Memory/ENV.md)" >&2
  echo "  Debug: printf '{...initialize...}' | ${VENV_PYTHON} -m claudecode_plugin.mcp_server" >&2
  exit 1
fi

# -- Prepare instance ---------------------------------------------------------
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

cat >"${PROMPT_FILE}" <<EOF
Read ${WORK_DIR}/TASK.md and complete the SWE-bench Lite task.
Use only built-in Claude Code tools. Work in the ${WORK_DIR}/repo/ subdirectory.
Keep a careful log in your final response of what you changed and how tests went.
EOF

cat >"${COMMAND_LOG}" <<EOF
#!/usr/bin/env bash
claude -p --dangerously-skip-permissions --strict-mcp-config \
  --mcp-config "${MCP_CONFIG}" \
  --model "${MODEL}" \
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
  "mcp_config": "${MCP_CONFIG}",
  "model": "${MODEL}",
  "og_memory": true,
  "stdout_log": "${STDOUT_LOG}",
  "stderr_log": "${STDERR_LOG}",
  "debug_log": "${DEBUG_LOG}"
}
EOF

log "instance_id=${INSTANCE_ID}"
log "work_dir=${WORK_DIR}"
log "repo=${REPO_SLUG} @ ${BASE_COMMIT}"
log "logs=${RUN_LOG_DIR}"

# -- Clone / checkout repo ----------------------------------------------------
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

# -- Build Claude args --------------------------------------------------------
CLAUDE_ARGS=(
  -p
  --dangerously-skip-permissions
  --strict-mcp-config
  --mcp-config "${MCP_CONFIG}"
  --model "${MODEL}"
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

# -- Launch Claude -------------------------------------------------------------
# NOTE: CWD stays at SWE_ROOT so Claude finds .claude/settings.json (hooks)
# and .mcp.json (og-memory) in the current directory. TASK.md and repo/ are
# referenced by absolute path in the prompt and via --add-dir.
log "launching claude with og-memory MCP (cwd=${SWE_ROOT})"
STARTED_AT="$(_ts)"
STARTED_EPOCH="$(date +%s)"
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
FINISHED_EPOCH="$(date +%s)"
WALL_TIME_SEC="$(( FINISHED_EPOCH - STARTED_EPOCH ))"

_heartbeat_stop
trap - EXIT

log "claude exited with code ${CLAUDE_EC} (wall_time=${WALL_TIME_SEC}s)"

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
    --set output_format="${OUTPUT_FORMAT}" \
    --set model="${MODEL}" \
    --set og_memory="true" \
    --set started_at="${STARTED_AT}" \
    --set wall_time_sec="${WALL_TIME_SEC}"
fi

log "done"
exit "${CLAUDE_EC}"
