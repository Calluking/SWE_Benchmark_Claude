# 10-task average tool count change

This note summarizes the 10 tasks from `og-memory_result.md` against the matching
`runs_clean/` logs.

## What I measured

I counted how many times `Read` and `Bash` were used in each run, then averaged
the counts across these 10 tasks:

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

## Average counts

| Metric | Clean average | og-memory average | Average change | % change |
| --- | ---: | ---: | ---: | ---: |
| `Read` | 14.9 | 14.0 | -0.9 | -6.0% |
| `Bash` | 48.9 | 44.4 | -4.5 | -9.2% |
| `API time (s)` | 316.4 | 328.0 | +11.6 | +3.7% |

## Average token and cost change

For the richer token/cost fields, I used the final result payload from the clean
run logs and the token table from `og-memory_result.md`.

| Metric | Clean average | og-memory average | Average change | % change |
| --- | ---: | ---: | ---: | ---: |
| `Input tokens` | 598.0 | 561.2 | -36.8 | -6.1% |
| `Output tokens` | 24,085.2 | 21,143.8 | -2,941.4 | -12.2% |
| `Cache read tokens` | 4,923,249.8 | 4,410,297.5 | -512,952.3 | -10.4% |
| `Cache creation tokens` | 65,315.2 | 70,528.3 | +5,213.1 | +8.0% |
| `Cost (USD)` | $0.6950 | $0.6355 | -$0.0595 | -8.6% |

## How to read this

- A negative change means `og-memory` used fewer tool calls on average.
- In this 10-task sample, the biggest drop is in `Bash`.
- `Read` also goes down a little, but the change is much smaller.
- API time moves the other way here: `og-memory` is slightly higher on average,
  by about `11.6` seconds.

## Per-task detail

| Task | Clean `Read` | og-memory `Read` | Clean `Bash` | og-memory `Bash` |
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

## Takeaway

Across these 10 tasks, the `og-memory` runs used:

- about `0.9` fewer `Read` calls on average
- about `4.5` fewer `Bash` calls on average
- about `11.6` more seconds of API time on average
- about `512,952` fewer cache-read tokens on average
- about `2,941` fewer output tokens on average
- about `$0.0595` less cost on average

So the clearest signal is not a dramatic change in reading, but a moderate
reduction in shell execution, while API time is a little higher in the
`og-memory` sample set. On the token side, `og-memory` is still cheaper overall:
it lowers output tokens, cache-read tokens, and total cost, even though cache
creation tokens tick up a bit.
