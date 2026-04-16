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

## 金额汇总

这里先给出整个 CSV 的分组总和，不是只看重叠任务。

| Split | clean | og-memory |
| --- | ---: | ---: |
| `dev` | `$16.1724` | `$12.2008` |
| `test` | `$7.4682` | `$0.0000` |
| `all` | `$23.6407` | `$12.2008` |

## 重叠任务的金额总和

这里是 22 个共享 `dev` 任务的总和。

| 指标 | clean | og-memory |
| --- | ---: | ---: |
| 共享 22 任务总和 | `$11.7608` | `$12.2008` |

`og-memory` 里唯一失败的任务是：

- `pydicom__pydicom-1413`

## 计算方法

这次我改成了“先求总和，再算整体百分比变化”的方式：

1. 把 22 个共享任务里 clean 的数值先求和
2. 把同一批任务里 `og-memory` 的数值先求和
3. 再计算：
   `(og-memory 总和 - clean 总和) / clean 总和 * 100`

这表示的是整组任务的净百分比变化。

## 共享任务的整体变化

这里展示的是 22 个重叠任务的总和，不是平均值。

| 指标 | 说明 | clean 精确值 | og-memory 精确值 | 整体百分比变化 |
| --- | --- | ---: | ---: | ---: |
| `api_ms` | API 时间（毫秒） | 5,525,247 | 6,792,339 | +22.9% |
| `total_ms` | 总运行时间（毫秒） | 6,473,940 | 20,286,577 | +213.4% |
| `input_tokens` | 输入 tokens | 10,948 | 11,118 | +1.6% |
| `output_tokens` | 输出 tokens | 411,284 | 403,414 | -1.9% |
| `total_cost_usd` | 总费用（美元） | $11.7609 | $12.2008 | +3.7% |
| `token_only_cost_usd` | 仅按输入 / 输出 tokens 估算的费用 | $2.0674 | $2.0282 | -1.9% |
| `num_turns` | Claude 轮次 | 1,363 | 1,385 | +1.6% |
| `tool_calls_total` | 工具调用总数 | 1,341 | 1,363 | +1.6% |
| `tool_Bash` | 执行任务次数 | 924 | 901 | -2.5% |
| `tool_Read` | 读取次数 | 266 | 269 | +1.1% |
| `tool_Edit` | 修改次数 | 132 | 144 | +9.1% |

## 说明

- `og-memory` 的 `api_ms` 仍然更高，整体是 `+22.9%`。
- `total_ms` 更高，主要是因为那次失败任务在触发 rate limit 之前跑了很久。
- `Bash` 调用数整体略少一点。
- `Output tokens` 整体也略少一点。
- 只看 token 单价的话，`og-memory` 在这 22 个任务上其实略便宜，见 `token_only_cost_usd`。
- 但真实记录的总费用更高，是因为 cache / context 费用也算在账里。
- 像 `tool_Write`、`tool_Glob`、`tool_TodoWrite` 这种很稀疏的列没有放进表里，因为共享任务里有些基线为 `0`，继续展开这些列的百分比意义不大。

## 结论

对于这 22 个共享的 `dev` 任务，`og-memory` 呈现出一种混合结果：

- `api_ms` 更高
- `total_ms` 高很多
- `Bash` 略少一点
- `Output tokens` 略少一点
- `记录里的总费用` 更高
- `仅 token 估算费用` 更低

如果要比较更宽的全集，clean CSV 还包含 `test` 任务，所以不能直接和 `og-memory` 做严格的一一对比，除非先筛到同一批 `dev` 任务。
