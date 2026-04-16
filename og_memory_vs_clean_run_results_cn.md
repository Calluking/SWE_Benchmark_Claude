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

这次我改成了“先求总和，再算整体百分比变化”的方式：

1. 把 22 个共享任务里 clean 的数值先求和
2. 把同一批任务里 `og-memory` 的数值先求和
3. 再计算：
   `(og-memory 总和 - clean 总和) / clean 总和 * 100`

这表示的是整组任务的净百分比变化。

## 共享任务的整体百分比变化

| 指标 | 整体百分比变化 |
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

## 说明

- `og-memory` 的 `api_ms` 仍然更高，整体是 `+22.9%`。
- `total_ms` 更高，主要是因为那次失败任务在触发 rate limit 之前跑了很久。
- `Bash` 调用数整体略少一点，但变化不大。
- `Output tokens` 整体也略少一点。
- 像 `tool_Write`、`tool_Glob`、`tool_TodoWrite` 这种很稀疏的列没有放进百分比表，因为共享任务里有些基线为 `0`，继续展开这些列的百分比意义不大。

## 结论

对于这 22 个共享的 `dev` 任务，`og-memory` 呈现出一种混合结果：

- `api_ms` 更高
- `total_ms` 高很多
- `Bash` 略少一点
- `Output tokens` 略少一点
- `总费用` 更低

如果要比较更宽的全集，clean CSV 还包含 `test` 任务，所以不能直接和 `og-memory` 做严格的一一对比，除非先筛到同一批 `dev` 任务。
