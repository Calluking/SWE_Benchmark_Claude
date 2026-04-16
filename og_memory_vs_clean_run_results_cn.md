# og-memory 与 clean 运行结果对比

## SWE-Lite

SWE-Lite 是 SWE-bench 的精简版基准，用来评估模型在真实代码仓库中的修复能力。
它把任务拆成两个 split：

- `dev`：用于本地试验和调试
- `test`：用于正式评估

在这份对比里，对比项目为 31 个任务。下面保留任务 ID、仓库和任务描述：

| 任务 ID | 仓库 | 任务描述 |
| --- | --- | --- |
| `marshmallow-code__marshmallow-1343` | `marshmallow-code/marshmallow` | 修复 `marshmallow` 里 `version 2.20.0` 的 `NoneType` 下标访问错误 |
| `marshmallow-code__marshmallow-1359` | `marshmallow-code/marshmallow` | 修复 `DateTime` 字段不能作为 `List` / `Tuple` 内部字段的问题 |
| `pvlib__pvlib-python-1072` | `pvlib/pvlib-python` | 修复带时区输入时 `temperature.fuentes` 在 `pandas>=1.0.0` 下报错 |
| `pvlib__pvlib-python-1154` | `pvlib/pvlib-python` | 修复 `pvlib.irradiance.reindl()` 在 `GHI = 0` 时产生 `NaN` |
| `pvlib__pvlib-python-1606` | `pvlib/pvlib-python` | 修复上下界相等时黄金分割搜索失败的问题 |
| `pvlib__pvlib-python-1707` | `pvlib/pvlib-python` | 修复 `iam.physical` 在 `n = 1` 且 `aoi > 90°` 时返回 `nan` |
| `pvlib__pvlib-python-1854` | `pvlib/pvlib-python` | 修复单个 `Array` 的 `PVSystem` 报错 |
| `pydicom__pydicom-1139` | `pydicom/pydicom` | 让 `PersonName3` 可迭代 |
| `pydicom__pydicom-1256` | `pydicom/pydicom` | 修复 `from_json` 对 SQ 数据元素中的 `BulkDataURI` 转换不正确的问题 |
| `pydicom__pydicom-1694` | `pydicom/pydicom` | 修复 `suppress_invalid_tags=True` 时 `Dataset.to_json_dict` 仍会抛异常的问题 |
| `pydicom__pydicom-901` | `pydicom/pydicom` | 修复 `pydicom` 不应定义 handler / formatter / log level 的问题 |
| `pylint-dev__astroid-1196` | `pylint-dev/astroid` | 修复 `getitem` 没有推断出实际解包后的值 |
| `pylint-dev__astroid-1268` | `pylint-dev/astroid` | 修复 `AsStringVisitor` 缺少 `visit_unknown` 属性 |
| `pylint-dev__astroid-1333` | `pylint-dev/astroid` | 修复 `astroid 2.9.1` 在缺少 `__init__.py` 时让 `pylint` 解析失败的问题 |
| `pylint-dev__astroid-1866` | `pylint-dev/astroid` | 修复 `TypeError: unsupported format string passed to NoneType.__format__` |
| `pylint-dev__astroid-1978` | `pylint-dev/astroid` | 修复 `numpy` 的弃用警告 |
| `pyvista__pyvista-4315` | `pyvista/pyvista` | 修复 `Rectilinear grid` 不允许把序列作为输入的问题 |
| `sqlfluff__sqlfluff-1517` | `sqlfluff/sqlfluff` | 修复双分号时出现 `Dropped elements in sequence matching` |
| `sqlfluff__sqlfluff-1625` | `sqlfluff/sqlfluff` | 修复在没有 `join` 的情况下 `TSQL - L031` 错误触发别名警告 |
| `sqlfluff__sqlfluff-1733` | `sqlfluff/sqlfluff` | 修复 `WITH` 语句中首个字段换行后多出一个空格 |
| `sqlfluff__sqlfluff-1763` | `sqlfluff/sqlfluff` | 修复 `dbt postgres fix` 触发 `UnicodeEncodeError` 并清空 `.sql` 文件的问题 |
| `sqlfluff__sqlfluff-2419` | `sqlfluff/sqlfluff` | 实现 `L060` 更具体的错误信息 |
| `astropy__astropy-12907` | `astropy/astropy` | 修复 `separability_matrix` 对嵌套 `CompoundModels` 的计算不正确 |
| `astropy__astropy-14182` | `astropy/astropy` | 实现 `RestructuredText` 输出支持 header rows |
| `astropy__astropy-14365` | `astropy/astropy` | 修复 `ascii.qdp` 表格格式默认把 QDP 命令当作大写的问题 |
| `astropy__astropy-14995` | `astropy/astropy` | 修复 `NDDataRef` 在一个操作数没有 mask 时的 mask 传播失败 |
| `astropy__astropy-6938` | `astropy/astropy` | 修复 `io.fits` 里与 `D` 指数相关的潜在 bug |
| `astropy__astropy-7746` | `astropy/astropy` | 修复给 `WCS` 转换传空列表 / 空数组时出问题 |
| `django__django-10914` | `django/django` | 实现默认 `FILE_UPLOAD_PERMISSION = 0o644` |
| `django__django-10924` | `django/django` | 实现 `FilePathField.path` 支持 callable |
| `django__django-11001` | `django/django` | 修复多行 `RawSQL` 创建的 `order_by` 子句被错误移除 |


## 模型说明与定价

运行使用的是 **Claude Haiku 4.5**。它主打低延迟和较低成本，适合交互式场景和代码子代理。

| 项目 | 内容 |
| --- | --- |
| 模型 | Claude Haiku 4.5 |
| 简要说明 | 低延迟、成本更友好，适合实时交互和 coding sub-agents |
| 输入价格 | `$1 / 100万 tokens` |
| 输出价格 | `$5 / 100万 tokens` |


## 金额总和

这里是 31 个任务的总和。

| 指标 | clean | og-memory |
| --- | ---: | ---: |
| 共享 31 任务总和 | `$17.1651` | `$16.6131` |


## 计算方法


1. 把 31 个共享任务里 clean 的数值先求和
2. 把同一批任务里 `og-memory` 的数值先求和
3. 再计算：
   `(og-memory 总和 - clean 总和) / clean 总和 * 100`

这表示的是整组任务的净百分比变化。

## 整体变化

这里展示的是 31 个重叠任务的总和值。

| 指标 | 说明 | claude code | claude code + og-memory | 变化 | 整体百分比变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `api_ms` | API 时间（毫秒） | 8,351,032 | 9,100,931 | +749,899 | +9.0% |
| `total_ms` | 总运行时间（毫秒） | 9,774,530 | 30,509,894 | +20,735,364 | +212.1% |
| `input_tokens` | 输入 tokens | 16,246 | 15,216 | -1,030 | -6.3% |
| `output_tokens` | 输出 tokens | 607,446 | 562,001 | -45,445 | -7.5% |
| `cache_cost_usd` | 缓存费用（美元） | $14.1116 | $13.5855 | -$0.5261 | -3.7% |
| `total_cost_usd` | 总费用（美元） | $17.1651 | $16.6131 | -$0.5519 | -3.2% |
| `num_turns` | Claude 轮次 | 2,023 | 1,894 | -129 | -6.4% |
| `tool_calls_total` | 工具调用总数 | 1,992 | 1,863 | -129 | -6.5% |
| `tool_Bash` | 执行任务次数 | 1,348 | 1,229 | -119 | -8.8% |
| `tool_Read` | 读取次数 | 392 | 370 | -22 | -5.6% |
| `tool_Edit` | 修改次数 | 207 | 191 | -16 | -7.7% |

## 说明

- 这 31 个任务都来自 Python 相关仓库，涵盖 `astropy`、`django`、`marshmallow`、`pvlib`、`pydicom`、`pylint-dev/astroid`、`pyvista` 和 `sqlfluff`。
- 任务表只展示了任务 ID、仓库和一句话任务描述，方便快速看出每个问题在修什么。
- `og-memory` 的 `api_ms` 仍然更高，整体是 `+9.0%`。
- `total_ms` 更高，主要是因为那次失败任务在触发 rate limit 之前跑了很久。
- `Bash` 调用数整体更少。
- `Output tokens` 整体也更少。
- `total_cost_usd` 更低，说明在这批重叠任务里，`og-memory` 的最终账单更低。
- 像 `tool_Write`、`tool_Glob`、`tool_TodoWrite` 这种很稀疏的列没有放进表里，因为共享任务里有些基线为 `0`，继续展开这些列的百分比意义不大。

## 结论

对于这 31 个共享任务，`og-memory` 呈现出一种“更省钱、但不更快”的结果：

- `api_ms` 更高
- `total_ms` 高很多
- `Bash` 更少
- `Output tokens` 更少
- `总费用` 更低

如果你只看这 31 个重叠任务，`og-memory` 在“最终账单更低”这一点上是成立的；但它在 `api_ms` 和 `total_ms` 上仍然不是更快的方案。
