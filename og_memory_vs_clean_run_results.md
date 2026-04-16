# og-memory vs clean run results

This note compares:

- [og_memory_run_results.csv](/home/luzh22/jiuwenclaw/SWE_clean/SWE_Benchmark_Claude/og_memory_run_results.csv)
- [clean_run results.csv](/home/luzh22/jiuwenclaw/SWE_clean/SWE_Benchmark_Claude/clean_run%20results.csv)

## What is comparable

The `og-memory` CSV now contains 32 rows:

- 22 `dev` runs
- 9 `test` runs

The clean CSV contains 45 runs total:

- 34 `dev` runs
- 11 `test` runs

So the fair apples-to-apples comparison is the 31 shared tasks that appear in both files after excluding the failed `og-memory` run.

Below is the task list for those 31 Python tasks, including the repository and a one-line task description:

| Task ID | Repository | Task description |
| --- | --- | --- |
| `marshmallow-code__marshmallow-1343` | `marshmallow-code/marshmallow` | Fix the NoneType indexing error in marshmallow version 2.20.0 |
| `marshmallow-code__marshmallow-1359` | `marshmallow-code/marshmallow` | Fix DateTime fields so they can be used inside List and Tuple fields |
| `pvlib__pvlib-python-1072` | `pvlib/pvlib-python` | Fix temperature.fuentes crashing with tz-aware inputs on pandas>=1.0.0 |
| `pvlib__pvlib-python-1154` | `pvlib/pvlib-python` | Fix pvlib.irradiance.reindl() producing NaN when GHI = 0 |
| `pvlib__pvlib-python-1606` | `pvlib/pvlib-python` | Fix golden-section search when the upper and lower bounds are equal |
| `pvlib__pvlib-python-1707` | `pvlib/pvlib-python` | Fix iam.physical returning nan when n = 1 and aoi > 90 degrees |
| `pvlib__pvlib-python-1854` | `pvlib/pvlib-python` | Fix PVSystem error when only a single Array is present |
| `pydicom__pydicom-1139` | `pydicom/pydicom` | Make PersonName3 iterable |
| `pydicom__pydicom-1256` | `pydicom/pydicom` | Fix from_json conversion of BulkDataURI inside SQ data elements |
| `pydicom__pydicom-1694` | `pydicom/pydicom` | Fix Dataset.to_json_dict exceptions when suppress_invalid_tags=True |
| `pydicom__pydicom-901` | `pydicom/pydicom` | Fix pydicom defining handler, formatter, and log level settings |
| `pylint-dev__astroid-1196` | `pylint-dev/astroid` | Fix getitem so it infers the actual unpacked value |
| `pylint-dev__astroid-1268` | `pylint-dev/astroid` | Fix the AsStringVisitor missing visit_unknown attribute |
| `pylint-dev__astroid-1333` | `pylint-dev/astroid` | Fix pylint parsing failure when astroid 2.9.1 is missing __init__.py |
| `pylint-dev__astroid-1866` | `pylint-dev/astroid` | Fix TypeError from unsupported format string passed to NoneType.__format__ |
| `pylint-dev__astroid-1978` | `pylint-dev/astroid` | Fix the NumPy deprecation warning |
| `pyvista__pyvista-4315` | `pyvista/pyvista` | Fix Rectilinear grid so it does not reject sequence inputs |
| `sqlfluff__sqlfluff-1517` | `sqlfluff/sqlfluff` | Fix "Dropped elements in sequence matching" when there is a doubled semicolon |
| `sqlfluff__sqlfluff-1625` | `sqlfluff/sqlfluff` | Fix TSQL L031 incorrectly firing when no join is present |
| `sqlfluff__sqlfluff-1733` | `sqlfluff/sqlfluff` | Fix the extra space that appears when the first field moves to a new line in a WITH statement |
| `sqlfluff__sqlfluff-1763` | `sqlfluff/sqlfluff` | Fix dbt postgres fix errors that raise UnicodeEncodeError and wipe the .sql file |
| `sqlfluff__sqlfluff-2419` | `sqlfluff/sqlfluff` | Make the L060 rule emit a more specific error message |
| `astropy__astropy-12907` | `astropy/astropy` | Fix separability_matrix for nested CompoundModels |
| `astropy__astropy-14182` | `astropy/astropy` | Add header row support to RestructuredText output |
| `astropy__astropy-14365` | `astropy/astropy` | Fix ascii.qdp so it does not assume QDP commands are uppercase |
| `astropy__astropy-14995` | `astropy/astropy` | Fix NDDataRef mask propagation when one operand has no mask |
| `astropy__astropy-6938` | `astropy/astropy` | Fix a potential FITS bug related to D exponents |
| `astropy__astropy-7746` | `astropy/astropy` | Fix WCS transforms when empty lists or arrays are passed |
| `django__django-10914` | `django/django` | Set the default FILE_UPLOAD_PERMISSION to 0o644 |
| `django__django-10924` | `django/django` | Allow FilePathField.path to accept a callable |
| `django__django-11001` | `django/django` | Fix order_by clauses created from multiline RawSQL being removed incorrectly |

## Coverage

| Metric | clean | og-memory |
| --- | ---: | ---: |
| Total rows | 45 | 32 |
| `dev` rows | 34 | 23 |
| `test` rows | 11 | 9 |
| Failed rows | 0 | 1 |

## Money totals by split

These are totals for each whole CSV split, not overlap-only.

| Split | clean | og-memory |
| --- | ---: | ---: |
| `dev` | `$16.1724` | `$12.6254` |
| `test` | `$7.4682` | `$4.5784` |
| `all` | `$23.6407` | `$17.2038` |

## Overlap-only money total

This is the sum across the 31 shared tasks only.

| Metric | clean | og-memory |
| --- | ---: | ---: |
| Shared 31-task total | `$17.1651` | `$16.6131` |

The one failed `og-memory` task is:

- `pydicom__pydicom-1413`

## Shared-task totals

The table below uses the 31 tasks shared by both CSVs after excluding the failed `og-memory` run.
These are totals over the shared tasks, not averages.

For each metric, I compute:

1. sum the clean values across the 31 shared tasks
2. sum the `og-memory` values across the same 31 tasks
3. compute `(og-memory total - clean total) / clean total * 100`

So this table shows the net percentage change across the whole shared set.

| Metric | Explanation | Clean exact | og-memory exact | Overall % change |
| --- | --- | ---: | ---: | ---: |
| `api_ms` | API time in milliseconds | 8,351,032 | 9,100,931 | +9.0% |
| `total_ms` | Total runtime in milliseconds | 9,774,530 | 30,509,894 | +212.1% |
| `input_tokens` | Input tokens | 16,246 | 15,216 | -6.3% |
| `output_tokens` | Output tokens | 607,446 | 562,001 | -7.5% |
| `total_cost_usd` | Total cost in USD | $17.1651 | $16.6131 | -3.2% |
| `cache_cost_usd` | Cache-related cost in USD, computed as total cost minus input/output token cost | $14.1116 | $13.5855 | -3.7% |
| `num_turns` | Number of Claude turns | 2,023 | 1,894 | -6.4% |
| `tool_calls_total` | Total tool calls | 1,992 | 1,863 | -6.5% |
| `tool_Bash` | Bash tool calls | 1,348 | 1,229 | -8.8% |
| `tool_Read` | Read tool calls | 392 | 370 | -5.6% |
| `tool_Edit` | Edit tool calls | 207 | 191 | -7.7% |

## Notes

- These 31 tasks are all Python tasks from the repositories listed above.
- The table focuses on the task ID, repository, and a one-line description so you can quickly tell what each benchmark instance is about.
- `og-memory` is still slower overall for `api_ms`, by `+9.0%`.
- `total_ms` is much higher because the one failed `og-memory` run spent a long time before the rate limit hit.
- `Bash` usage is lower overall.
- Output tokens are lower overall.
- `total_cost_usd` is lower, which means the final bill is lower on this shared set.
- `cache_cost_usd` is derived from the total cost after subtracting the input/output token cost.
- Sparse tool columns like `tool_Write`, `tool_Glob`, and `tool_TodoWrite` are omitted because the shared set contains zero baselines for some of those metrics, which makes extra percentage reporting less useful.

## Short conclusion

For these 31 shared tasks, `og-memory` shows a "cheaper, but not faster" result:

- higher API time
- much higher total runtime
- lower `Bash` usage
- lower output tokens
- lower total cost
- lower cache-related cost

If you only look at the 31 overlapping tasks, `og-memory` wins on final cost, but it is still not the faster option on `api_ms` or `total_ms`.
