# og-memory vs clean run results

This note compares:

- [og_memory_run_results.csv](/home/luzh22/jiuwenclaw/SWE_clean/SWE_Benchmark_Claude/og_memory_run_results.csv)
- [clean_run results.csv](/home/luzh22/jiuwenclaw/SWE_clean/SWE_Benchmark_Claude/clean_run%20results.csv)

## What is comparable

The `og-memory` CSV contains 22 `dev` runs.
The clean CSV contains 45 runs total:

- 34 `dev` runs
- 11 `test` runs

So the fair apples-to-apples comparison is the 22 shared `dev` tasks that appear in both files.

## Coverage

| Metric | clean | og-memory |
| --- | ---: | ---: |
| Total rows | 45 | 22 |
| `dev` rows | 34 | 22 |
| `test` rows | 11 | 0 |
| Failed rows | 0 | 1 |

The one failed `og-memory` task is:

- `pydicom__pydicom-1413`

## Shared-task averages

The table below uses the 22 tasks shared by both CSVs.

For each metric, I now compute:

1. the percentage difference for each task: `(og-memory - clean) / clean * 100`
2. the average of those 22 per-task percentages

So this is an average of task-level percentage changes, not the percentage change
of the overall averages.

| Metric | Avg task-wise % change |
| --- | ---: |
| `api_ms` | +32.2% |
| `total_ms` | +230.1% |
| `input_tokens` | +4.0% |
| `output_tokens` | +1.9% |
| `total_cost_usd` | +11.8% |
| `num_turns` | +4.1% |
| `tool_calls_total` | +4.0% |
| `tool_Bash` | +2.7% |
| `tool_Read` | +6.0% |
| `tool_Edit` | +19.8% |

## Notes

- `og-memory` is still slower on average for `api_ms`, and the task-wise mean is `+32.2%`.
- `total_ms` is much higher because the one failed `og-memory` run spent a long time before the rate limit hit.
- Tool usage is mostly similar, with `Bash` only slightly lower on average.
- Output tokens are a bit lower, but the difference is small.
- Sparse tool columns like `tool_Write`, `tool_Glob`, and `tool_TodoWrite` are omitted from the percentage table because some shared tasks have a clean baseline of zero, which makes a per-task percentage undefined.

## Short conclusion

For these 22 shared `dev` tasks, the `og-memory` CSV does not show a clear efficiency win.
The most noticeable differences are:

- higher API time
- higher total runtime
- slightly higher `Bash` usage
- slightly higher output tokens

If you want to compare the files at a broader level, the clean CSV also includes `test` runs, so that comparison is not apples-to-apples unless you filter to `dev` only.
