The launcher expects the SWE-bench Lite dataset at:

```bash
./data/SWE-bench_Lite
```

## Download Dataset

If you do not already have the dataset locally, download it from Hugging Face
and save it in the local `data/` directory:

```bash
mkdir -p ./data
python3 - <<'PY'
from datasets import load_dataset

ds = load_dataset("SWE-bench/SWE-bench_Lite")
ds.save_to_disk("./data/SWE-bench_Lite")
PY
```

If your dataset lives somewhere else, point the script at it explicitly:

```bash
export DATASET_ROOT=/path/to/SWE-bench_Lite
```

If you are cloning this repo onto a new machine, make sure the dataset is present
before running the script. The repo itself does not include the benchmark data.

Run the SWE-Lite trial with Claude Code:

```bash
SWE_LITE_INDEX=1 ./scripts/run_swe_lite_one_claude.sh
```

## Run In Parallel

If you want to split a range of SWE-Lite indices across multiple workers, use
the parallel wrapper script:

By default, the parallel wrapper uses the `test` split. Set
`SWE_LITE_SPLIT=dev` explicitly if you want the smaller dev set.

```bash
SWE_LITE_START=12 SWE_LITE_END=21 SWE_LITE_WORKERS=2 SWE_LITE_WORKER_ID=1 \
  ./scripts/run_swe_lite_range_parallel.sh
```

For the second worker, change `SWE_LITE_WORKER_ID`:

```bash
SWE_LITE_START=12 SWE_LITE_END=21 SWE_LITE_WORKERS=2 SWE_LITE_WORKER_ID=2 \
  ./scripts/run_swe_lite_range_parallel.sh
```

How it splits the work:

- worker 1 gets `12, 14, 16, 18, 20`
- worker 2 gets `13, 15, 17, 19, 21`

If you want each worker to run more than one task at a time, set
`SWE_LITE_MAX_PARALLEL`:

```bash
SWE_LITE_START=12 SWE_LITE_END=21 SWE_LITE_WORKERS=2 SWE_LITE_WORKER_ID=1 \
SWE_LITE_MAX_PARALLEL=2 ./scripts/run_swe_lite_range_parallel.sh
```
