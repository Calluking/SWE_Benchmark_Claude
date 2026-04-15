#!/usr/bin/env python3
"""Extract token totals from a Claude Code `stream-json` log."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _walk(obj: Any, acc: dict[str, int]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            lk = str(k).lower()
            if lk in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"):
                if isinstance(v, (int, float)):
                    acc["input_tokens"] = max(acc["input_tokens"], int(v))
            elif lk == "output_tokens":
                if isinstance(v, (int, float)):
                    acc["output_tokens"] = max(acc["output_tokens"], int(v))
            else:
                _walk(v, acc)
    elif isinstance(obj, list):
        for item in obj:
            _walk(item, acc)


def extract_usage(path: Path) -> dict[str, int]:
    acc = {"input_tokens": 0, "output_tokens": 0}
    if not path.exists():
        return acc
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            _walk(json.loads(line), acc)
        except json.JSONDecodeError:
            continue
    return acc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stream-log", type=Path, required=True)
    parser.add_argument("--append-tsv", type=Path, required=True)
    parser.add_argument("--set", action="append", default=[], metavar="KEY=VAL")
    args = parser.parse_args()

    meta: dict[str, str] = {}
    for item in args.set:
        if "=" not in item:
            raise SystemExit(f"--set needs KEY=VAL, got {item!r}")
        key, value = item.split("=", 1)
        meta[key.strip()] = value.strip()

    usage = extract_usage(args.stream_log)
    row = {
        "ts_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stream_log": str(args.stream_log.resolve()),
        "input_tokens": str(usage["input_tokens"]),
        "output_tokens": str(usage["output_tokens"]),
        **meta,
    }

    args.append_tsv.parent.mkdir(parents=True, exist_ok=True)
    write_header = not args.append_tsv.exists() or args.append_tsv.stat().st_size == 0
    extra_keys = sorted(k for k in row if k not in ("ts_utc", "stream_log", "input_tokens", "output_tokens"))
    fieldnames = ["ts_utc", "stream_log", "input_tokens", "output_tokens"] + extra_keys
    with args.append_tsv.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fieldnames})

    print(json.dumps({"input_tokens": usage["input_tokens"], "output_tokens": usage["output_tokens"]}, indent=2))


if __name__ == "__main__":
    main()
