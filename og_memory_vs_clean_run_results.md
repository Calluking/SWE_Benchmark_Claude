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

## Money totals by split

These are totals for each whole CSV split, not overlap-only.

| Split | clean | og-memory |
| --- | ---: | ---: |
| `dev` | `$16.1724` | `$12.2008` |
| `test` | `$7.4682` | `$0.0000` |
| `all` | `$23.6407` | `$12.2008` |

## Overlap-only money total

This is the sum across the 22 shared `dev` tasks only.

| Metric | clean | og-memory |
| --- | ---: | ---: |
| Shared 22-task total | `$11.7608` | `$12.2008` |

The one failed `og-memory` task is:

- `pydicom__pydicom-1413`

## Shared-task totals

The table below uses the 22 tasks shared by both CSVs.
These are totals over the 22 shared tasks, not averages.

For each metric, I compute:

1. sum the clean values across the 22 shared tasks
2. sum the `og-memory` values across the same 22 tasks
3. compute `(og-memory total - clean total) / clean total * 100`

So this table shows the net percentage change across the whole shared set.

| Metric | Explanation | Clean exact | og-memory exact | Overall % change |
| --- | --- | ---: | ---: | ---: |
| `api_ms` | API time in milliseconds | 5,525,247 | 6,792,339 | +22.9% |
| `total_ms` | Total runtime in milliseconds | 6,473,940 | 20,286,577 | +213.4% |
| `input_tokens` | Input tokens | 10,948 | 11,118 | +1.6% |
| `output_tokens` | Output tokens | 411,284 | 403,414 | -1.9% |
| `total_cost_usd` | Total cost in USD | $11.7609 | $12.2008 | +3.7% |
| `token_only_cost_usd` | Token-only estimated cost from input/output tokens only | $2.0674 | $2.0282 | -1.9% |
| `num_turns` | Number of Claude turns | 1,363 | 1,385 | +1.6% |
| `tool_calls_total` | Total tool calls | 1,341 | 1,363 | +1.6% |
| `tool_Bash` | Bash tool calls | 924 | 901 | -2.5% |
| `tool_Read` | Read tool calls | 266 | 269 | +1.1% |
| `tool_Edit` | Edit tool calls | 132 | 144 | +9.1% |

## Notes

- `og-memory` is still slower overall for `api_ms`, by `+22.9%`.
- `total_ms` is much higher because the one failed `og-memory` run spent a long time before the rate limit hit.
- `Bash` usage is slightly lower overall.
- Output tokens are slightly lower overall.
- On token pricing alone, `og-memory` is slightly cheaper for the shared 22 tasks, as shown by `token_only_cost_usd`.
- The recorded total cost is still higher because cache/context charges are also part of the bill.
- Sparse tool columns like `tool_Write`, `tool_Glob`, and `tool_TodoWrite` are omitted because the shared set contains zero baselines for some of those metrics, which makes extra percentage reporting less useful.

## Short conclusion

For these 22 shared `dev` tasks, `og-memory` shows a mixed result:

- higher API time
- much higher total runtime
- slightly lower `Bash` usage
- slightly lower output tokens
- higher recorded total cost
- lower token-only cost

If you want to compare the files at a broader level, the clean CSV also includes `test` runs, so that comparison is not apples-to-apples unless you filter to `dev` only.
