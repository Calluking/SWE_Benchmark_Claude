#!/usr/bin/env python3
"""Rebuild clean run result CSVs from run folders and stream logs.

This script reads the run directories directly and reconstructs the same
metrics columns as the historical `clean_run results.csv` file.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from datasets import load_from_disk


CSV_COLUMNS = [
    "folder",
    "instance_id",
    "repo",
    "split",
    "lite_index",
    "model",
    "failed",
    "api_ms",
    "total_ms",
    "input_tokens",
    "output_tokens",
    "total_cost_usd",
    "num_turns",
    "tool_calls_total",
    "tool_Bash",
    "tool_Edit",
    "tool_Glob",
    "tool_Grep",
    "tool_Read",
    "tool_TodoWrite",
    "tool_Write",
    "tool_bash",
]

TOOL_COLUMNS = {
    "Bash": "tool_Bash",
    "Edit": "tool_Edit",
    "Glob": "tool_Glob",
    "Grep": "tool_Grep",
    "Read": "tool_Read",
    "TodoWrite": "tool_TodoWrite",
    "Write": "tool_Write",
    "bash": "tool_bash",
}


def load_dataset_index(root: Path) -> dict[str, dict[str, int]]:
    ds = load_from_disk(str(root))
    index: dict[str, dict[str, int]] = {}
    for split in ds.keys():
        index[split] = {row["instance_id"]: i for i, row in enumerate(ds[split])}
    return index


def parse_stream_log(path: Path) -> tuple[dict[str, int], dict[str, Any]]:
    counts = {col: 0 for col in TOOL_COLUMNS.values()}
    final_result: dict[str, Any] = {}
    if not path.exists():
        return counts, final_result

    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            if obj.get("type") == "stream_event" and obj.get("event", {}).get("type") == "content_block_start":
                content_block = obj["event"].get("content_block", {})
                if content_block.get("type") == "tool_use":
                    name = content_block.get("name")
                    if name in TOOL_COLUMNS:
                        counts[TOOL_COLUMNS[name]] += 1
            elif obj.get("type") == "result":
                final_result = obj

    return counts, final_result


def first_model_name(result: dict[str, Any]) -> str:
    model_usage = result.get("modelUsage")
    if isinstance(model_usage, dict) and model_usage:
        return next(iter(model_usage.keys()))
    return ""


def build_rows(folder: Path, split: str, dataset_index: dict[str, dict[str, int]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for inst_dir in sorted(p for p in folder.iterdir() if p.is_dir()):
        instance_json = inst_dir / "instance.json"
        stream_log = inst_dir / "logs" / "claude_stream.jsonl"
        if not instance_json.exists():
            continue
        inst = json.loads(instance_json.read_text(encoding="utf-8"))
        counts, result = parse_stream_log(stream_log)
        tool_total = sum(counts.values())
        split_index = dataset_index.get(split, {}).get(inst["instance_id"], "")
        rows.append(
            {
                "folder": folder.name,
                "instance_id": inst["instance_id"],
                "repo": inst.get("repo", ""),
                "split": split,
                "lite_index": split_index,
                "model": first_model_name(result) or "",
                "failed": int(bool(result.get("is_error", False))),
                "api_ms": int(result.get("duration_api_ms", 0) or 0),
                "total_ms": int(result.get("duration_ms", 0) or 0),
                "input_tokens": int((result.get("usage") or {}).get("input_tokens", 0) or 0),
                "output_tokens": int((result.get("usage") or {}).get("output_tokens", 0) or 0),
                "total_cost_usd": result.get("total_cost_usd", 0) or 0,
                "num_turns": int(result.get("num_turns", 0) or 0),
                "tool_calls_total": tool_total,
                **counts,
            }
        )

    rows.sort(key=lambda r: (r["lite_index"] if isinstance(r["lite_index"], int) else 10**9, r["instance_id"]))
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in CSV_COLUMNS})


def resolve_dataset_root(root: Path) -> Path:
    candidates = [
        root / "data" / "SWE-bench_Lite",
        root.parent / "SWE-bench" / "data" / "SWE-bench_Lite",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Could not find SWE-bench_Lite dataset. Tried: {candidates}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dev-folder", type=Path, default=Path("runs_clean_dev"))
    parser.add_argument("--test-folder", type=Path, default=Path("runs_clean_test"))
    parser.add_argument("--dev-output", type=Path, default=Path("clean_run_dev_result.csv"))
    parser.add_argument("--test-output", type=Path, default=Path("clean_run_test_result.csv"))
    args = parser.parse_args()

    root = args.root.resolve()
    dataset_root = resolve_dataset_root(root)
    dataset_index = load_dataset_index(dataset_root)

    dev_rows = build_rows(root / args.dev_folder, "dev", dataset_index)
    test_rows = build_rows(root / args.test_folder, "test", dataset_index)

    write_csv(root / args.dev_output, dev_rows)
    write_csv(root / args.test_output, test_rows)

    print(f"Wrote {len(dev_rows)} dev rows to {root / args.dev_output}")
    print(f"Wrote {len(test_rows)} test rows to {root / args.test_output}")


if __name__ == "__main__":
    main()
