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
