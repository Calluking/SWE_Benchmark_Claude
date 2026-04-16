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

1. sum the clean values across the 22 shared tasks
2. sum the `og-memory` values across the same 22 tasks
3. compute `(og-memory total - clean total) / clean total * 100`

So this table shows the net percentage change across the whole shared set.

| Metric | Overall % change |
| --- | ---: |
| `api_ms` | +22.9% |
| `total_ms` | +213.4% |
| `input_tokens` | +1.6% |
| `output_tokens` | -1.9% |
| `total_cost_usd` | +3.7% |
| `num_turns` | +1.6% |
| `tool_calls_total` | +1.6% |
| `tool_Bash` | -2.5% |
| `tool_Read` | +1.1% |
| `tool_Edit` | +9.1% |

## Notes

- `og-memory` is still slower overall for `api_ms`, by `+22.9%`.
- `total_ms` is much higher because the one failed `og-memory` run spent a long time before the rate limit hit.
- Tool usage is mostly similar, with `Bash` slightly lower overall.
- Output tokens are slightly lower overall.
- Sparse tool columns like `tool_Write`, `tool_Glob`, and `tool_TodoWrite` are omitted because the shared set contains zero baselines for some of those metrics, which makes extra percentage reporting less useful.

## Short conclusion

For these 22 shared `dev` tasks, `og-memory` shows a mixed result:

- higher API time
- much higher total runtime
- slightly lower `Bash` usage
- slightly lower output tokens
- lower total cost overall

If you want to compare the files at a broader level, the clean CSV also includes `test` runs, so that comparison is not apples-to-apples unless you filter to `dev` only.
