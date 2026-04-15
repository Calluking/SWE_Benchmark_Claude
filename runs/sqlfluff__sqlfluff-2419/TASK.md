# SWE-bench Lite single-instance run (no MCP)

## instance_id
`sqlfluff__sqlfluff-2419`

## repo / base_commit
- **repo:** `sqlfluff/sqlfluff`
- **base_commit:** `f1dba0e1dd764ae72d67c3d5e1471cf14d3db030`

Local checkout (if the run script cloned it): subdirectory `repo/` under this instance folder.

## FAIL_TO_PASS (must become green after your fix)
```json
"[\"test/rules/std_L060_test.py::test__rules__std_L060_raised\"]"
```

## PASS_TO_PASS (must stay green)
```json
"[]"
```

## problem_statement
Rule L060 could give a specific error message
At the moment rule L060 flags something like this:

```
L:  21 | P:   9 | L060 | Use 'COALESCE' instead of 'IFNULL' or 'NVL'.
```

Since we likely know the wrong word, it might be nice to actually flag that instead of both `IFNULL` and `NVL` - like most of the other rules do.

That is it should flag this:

```
L:  21 | P:   9 | L060 | Use 'COALESCE' instead of 'IFNULL'.
```
 Or this:

```
L:  21 | P:   9 | L060 | Use 'COALESCE' instead of 'NVL'.
```

As appropriate.

What do you think @jpy-git ?



---
## Instructions for the agent

1. Use only built-in Claude Code tools (`Read`, `Edit`, `Bash`, etc.). Do not call external MCP tools.
2. Work in the checked-out repo under `repo/`. Implement the fix and run the failing tests.
3. In your final reply, summarize how tests went and what you changed.
