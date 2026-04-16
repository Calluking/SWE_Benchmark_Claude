# 10 个任务的平均变化对比

这份说明对比了 `og-memory_result.md` 中的 10 个任务，与 `runs_clean/` 里对应的 clean 运行结果。

## 对比范围

我对下面 10 个任务做了逐项比较，然后再取平均：

- `marshmallow-code__marshmallow-1343`
- `marshmallow-code__marshmallow-1359`
- `pvlib__pvlib-python-1072`
- `pvlib__pvlib-python-1606`
- `pvlib__pvlib-python-1707`
- `pvlib__pvlib-python-1854`
- `sqlfluff__sqlfluff-1517`
- `sqlfluff__sqlfluff-1733`
- `sqlfluff__sqlfluff-1763`
- `sqlfluff__sqlfluff-2419`

## 平均工具调用数

| 指标 | clean 平均值 | og-memory 平均值 | 平均变化 | 百分比变化 |
| --- | ---: | ---: | ---: | ---: |
| `Read` | 14.9 | 14.0 | -0.9 | -6.0% |
| `Bash` | 48.9 | 44.4 | -4.5 | -9.2% |
| `API time (s)` | 316.4 | 328.0 | +11.6 | +3.7% |

## 平均 token 和费用变化

这里的 clean 数据来自最终运行结果的原始日志，`og-memory` 数据来自 `og-memory_result.md` 的 token 表格。

| 指标 | clean 平均值 | og-memory 平均值 | 平均变化 | 百分比变化 |
| --- | ---: | ---: | ---: | ---: |
| `Input tokens` | 598.0 | 561.2 | -36.8 | -6.1% |
| `Output tokens` | 24,085.2 | 21,143.8 | -2,941.4 | -12.2% |
| `Cache read tokens` | 4,923,249.8 | 4,410,297.5 | -512,952.3 | -10.4% |
| `Cache creation tokens` | 65,315.2 | 70,528.3 | +5,213.1 | +8.0% |
| `Cost (USD)` | $0.6950 | $0.6355 | -$0.0595 | -8.6% |

## 如何理解

- 负数表示 `og-memory` 平均用得更少。
- 在这 10 个任务里，`Bash` 调用数下降最明显。
- `Read` 也略有下降，但幅度不大。
- `API time` 在这组样本里略有上升。
- token 方面，`og-memory` 仍然更省：`Output tokens`、`Cache read tokens` 和总费用都下降了。
- 唯一上升的是 `Cache creation tokens`，但增幅不大。

## 按任务的明细

| 任务 | clean `Read` | og-memory `Read` | clean `Bash` | og-memory `Bash` |
| --- | ---: | ---: | ---: | ---: |
| `marshmallow-code__marshmallow-1343` | 12 | 9 | 34 | 20 |
| `marshmallow-code__marshmallow-1359` | 13 | 8 | 29 | 54 |
| `pvlib__pvlib-python-1072` | 13 | 10 | 46 | 30 |
| `pvlib__pvlib-python-1606` | 11 | 11 | 27 | 31 |
| `pvlib__pvlib-python-1707` | 13 | 12 | 27 | 24 |
| `pvlib__pvlib-python-1854` | 16 | 15 | 30 | 42 |
| `sqlfluff__sqlfluff-1517` | 24 | 24 | 75 | 79 |
| `sqlfluff__sqlfluff-1733` | 19 | 17 | 106 | 95 |
| `sqlfluff__sqlfluff-1763` | 17 | 16 | 48 | 52 |
| `sqlfluff__sqlfluff-2419` | 11 | 18 | 67 | 17 |

## 结论

这 10 个任务里，`og-memory` 的表现可以概括为：

- 工具调用更少，尤其是 `Bash`
- 输出 token 更少
- cache read token 更少
- 总费用更低
- 但 API time 略高

所以如果只保留一个最稳妥的结论，可以写成：

> `og-memory` 在这组任务里整体更省 token 和费用，同时减少了 shell 操作；但它并没有明显缩短 API time。
