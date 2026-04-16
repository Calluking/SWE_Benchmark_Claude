# og-memory 与 clean 运行结果对比

这份说明对比以下两个 CSV：

- [og_memory_run_results.csv](/home/luzh22/jiuwenclaw/SWE_clean/SWE_Benchmark_Claude/og_memory_run_results.csv)
- [clean_run results.csv](/home/luzh22/jiuwenclaw/SWE_clean/SWE_Benchmark_Claude/clean_run%20results.csv)

## 哪些数据可以直接比较

`og-memory` 的 CSV 里有 22 个 `dev` 任务。
clean 的 CSV 里一共有 45 个任务：

- 34 个 `dev` 任务
- 11 个 `test` 任务

所以严格来说，真正能一一对应比较的是这 22 个双方都出现的 `dev` 任务。

## 覆盖情况

| 指标 | clean | og-memory |
| --- | ---: | ---: |
| 总行数 | 45 | 22 |
| `dev` 行数 | 34 | 22 |
| `test` 行数 | 11 | 0 |
| 失败行数 | 0 | 1 |

`og-memory` 里唯一失败的任务是：

- `pydicom__pydicom-1413`

## 计算方法

这次我改成了“按任务先算百分比变化，再取平均”的方式：

1. 对每个共享任务，先算：
   `(og-memory - clean) / clean * 100`
2. 再把这 22 个任务的百分比变化求平均

这和“先求总体平均，再算百分比”是不一样的。

## 共享任务的平均百分比变化

| 指标 | 任务级平均百分比变化 |
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

## 说明

- `og-memory` 的 `api_ms` 仍然更高，按任务平均后是 `+32.2%`。
- `total_ms` 更高，主要是因为那次失败任务在触发 rate limit 之前跑了很久。
- `Bash` 调用数平均略低，但变化不大。
- `Output tokens` 稍微更少一些，但差距也不大。
- 像 `tool_Write`、`tool_Glob`、`tool_TodoWrite` 这种很稀疏的列没有放进百分比表，因为有些共享任务的 clean 基线是 `0`，这种情况下按任务算百分比会变成未定义。

## 结论

对于这 22 个共享的 `dev` 任务，`og-memory` 没有体现出明显的效率提升。
更明显的现象是：

- `api_ms` 更高
- `total_ms` 更高
- `Bash` 略少一点
- `Output tokens` 略少一点

如果要比较更宽的全集，clean CSV 还包含 `test` 任务，所以不能直接和 `og-memory` 做严格的一一对比，除非先筛到同一批 `dev` 任务。
