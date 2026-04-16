#!/usr/bin/env bash
# Run a range of SWE-bench Lite instances in parallel, split across workers.
#
# Example:
#   SWE_LITE_START=12 SWE_LITE_END=21 SWE_LITE_WORKERS=2 SWE_LITE_WORKER_ID=1 \
#     ./scripts/run_swe_lite_range_parallel.sh
#
# This assigns indices by modulo:
#   worker 1 gets: start, start + workers, start + 2*workers, ...
#   worker 2 gets: start + 1, start + 1 + workers, ...

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

START="${SWE_LITE_START:-0}"
END="${SWE_LITE_END:-0}"
WORKERS="${SWE_LITE_WORKERS:-1}"
WORKER_ID="${SWE_LITE_WORKER_ID:-1}"
SPLIT="${SWE_LITE_SPLIT:-dev}"
DATASET_ROOT="${DATASET_ROOT:-}"
WORK_ROOT="${WORK_ROOT:-}"
MAX_PARALLEL="${SWE_LITE_MAX_PARALLEL:-1}"

if [[ "${WORKER_ID}" -lt 1 || "${WORKER_ID}" -gt "${WORKERS}" ]]; then
  echo "SWE_LITE_WORKER_ID must be between 1 and SWE_LITE_WORKERS" >&2
  exit 1
fi

if [[ "${START}" -gt "${END}" ]]; then
  echo "SWE_LITE_START must be <= SWE_LITE_END" >&2
  exit 1
fi

indices=()
for ((i=START; i<=END; i++)); do
  if (((i - START) % WORKERS + 1 == WORKER_ID)); then
    indices+=("${i}")
  fi
done

if [[ "${#indices[@]}" -eq 0 ]]; then
  echo "No indices assigned to worker ${WORKER_ID}/${WORKERS} for range ${START}-${END}" >&2
  exit 0
fi

run_one() {
  local idx="$1"
  echo "[worker ${WORKER_ID}/${WORKERS}] starting index ${idx}" >&2
  local env_args=(
    SWE_LITE_SPLIT="${SPLIT}"
    SWE_LITE_INDEX="${idx}"
  )
  if [[ -n "${DATASET_ROOT}" ]]; then
    env_args+=(DATASET_ROOT="${DATASET_ROOT}")
  fi
  if [[ -n "${WORK_ROOT}" ]]; then
    env_args+=(WORK_ROOT="${WORK_ROOT}")
  fi
  env "${env_args[@]}" "${SCRIPT_DIR}/run_swe_lite_one_claude.sh"
  echo "[worker ${WORKER_ID}/${WORKERS}] finished index ${idx}" >&2
}

running=0
for idx in "${indices[@]}"; do
  run_one "${idx}" &
  running=$((running + 1))
  if [[ "${running}" -ge "${MAX_PARALLEL}" ]]; then
    wait -n
    running=$((running - 1))
  fi
done

wait
