#!/usr/bin/env python3
"""Export one SWE-bench Lite row to a run directory with TASK.md."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from datasets import load_from_disk


def _json_safe(obj):
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)


def _task_md(rec: dict, use_mcp: bool) -> str:
    if use_mcp:
        intro = """# SWE-bench Lite single-instance run

## instance_id
`{instance_id}`

## repo / base_commit
- **repo:** `{repo}`
- **base_commit:** `{base_commit}`

Local checkout (if the run script cloned it): subdirectory `repo/` under this instance folder.

## FAIL_TO_PASS (must become green after your fix)
```json
{fail_to_pass}
```

## PASS_TO_PASS (must stay green)
```json
{pass_to_pass}
```

## problem_statement
{problem_statement}

---
## Instructions for the agent

1. Use only built-in Claude Code tools (`Read`, `Edit`, `Bash`, etc.). Do not call external MCP tools.
2. Work in the checked-out repo under `repo/`. Implement the fix and run the failing tests.
3. In your final reply, summarize how tests went and what you changed.
"""
    else:
        intro = """# SWE-bench Lite single-instance run (no MCP)

## instance_id
`{instance_id}`

## repo / base_commit
- **repo:** `{repo}`
- **base_commit:** `{base_commit}`

Local checkout (if the run script cloned it): subdirectory `repo/` under this instance folder.

## FAIL_TO_PASS (must become green after your fix)
```json
{fail_to_pass}
```

## PASS_TO_PASS (must stay green)
```json
{pass_to_pass}
```

## problem_statement
{problem_statement}

---
## Instructions for the agent

1. Use only built-in Claude Code tools (`Read`, `Edit`, `Bash`, etc.). Do not call external MCP tools.
2. Work in the checked-out repo under `repo/`. Implement the fix and run the failing tests.
3. In your final reply, summarize how tests went and what you changed.
"""
    return intro.format(
        instance_id=rec["instance_id"],
        repo=rec["repo"],
        base_commit=rec["base_commit"],
        fail_to_pass=json.dumps(rec.get("FAIL_TO_PASS") or [], ensure_ascii=False, indent=2),
        pass_to_pass=json.dumps(rec.get("PASS_TO_PASS") or [], ensure_ascii=False, indent=2),
        problem_statement=rec.get("problem_statement") or "",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", type=Path, required=True)
    parser.add_argument("--split", default="dev", choices=("dev", "test"))
    parser.add_argument("--index", type=int, default=1)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--no-mcp", action="store_true")
    args = parser.parse_args()

    ds = load_from_disk(str(args.dataset_root))
    split = ds[args.split]
    if args.index < 0 or args.index >= len(split):
        raise SystemExit(f"index {args.index} out of range for split {args.split} (len={len(split)})")

    rec = _json_safe(dict(split[args.index]))
    work = args.work_root / rec["instance_id"]
    work.mkdir(parents=True, exist_ok=True)

    (work / "instance.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
    (work / "TASK.md").write_text(_task_md(rec, use_mcp=not args.no_mcp), encoding="utf-8")

    print(f'{rec["instance_id"]}\t{work.resolve()}')


if __name__ == "__main__":
    main()
