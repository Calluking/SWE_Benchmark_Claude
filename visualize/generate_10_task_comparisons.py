#!/usr/bin/env python3
"""Generate 10 per-task SVG bar charts comparing clean vs og-memory runs.

This script compares:
- tool call counts from the clean run logs under `runs_clean/`
- tool call counts and API times from `og-memory_result.md`

It emits one SVG chart per task into the requested output directory, plus a
small `index.md` file that lists the generated images.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Iterable


TASK_ORDER = [
    "marshmallow-code__marshmallow-1343",
    "marshmallow-code__marshmallow-1359",
    "pvlib__pvlib-python-1072",
    "pvlib__pvlib-python-1606",
    "pvlib__pvlib-python-1707",
    "pvlib__pvlib-python-1854",
    "sqlfluff__sqlfluff-1517",
    "sqlfluff__sqlfluff-1733",
    "sqlfluff__sqlfluff-1763",
    "sqlfluff__sqlfluff-2419",
]

TABLE_RE = re.compile(r"^(?P<run>[A-Za-z0-9_.\-__]+)\t(?P<api>[0-9.]+)s\t(?P<calls>\d+)$")
DETAIL_HEADER_RE = re.compile(r"^(?P<run>[A-Za-z0-9_.\-__]+) \((?P<api>[0-9.]+)s\)$")
COUNT_RE = re.compile(r"(?P<tool>[A-Za-z][A-Za-z0-9_]*)\s*:\s*(?P<count>\d+)")


@dataclass
class RunData:
    api_seconds: float
    total_calls: int
    counts: dict[str, int]


def _parse_og_memory_markdown(md_path: Path) -> dict[str, RunData]:
    lines = md_path.read_text(encoding="utf-8", errors="replace").splitlines()
    runs: dict[str, RunData] = {}

    in_table = False
    in_detail = False
    current_run: str | None = None
    for raw in lines:
        line = raw.strip()
        if line == "Tool Usage & API Time per Run":
            in_table = True
            continue
        if line == "Tool Breakdown Detail":
            in_table = False
            in_detail = True
            continue
        if line == "Key Observations":
            break

        if in_table:
            if not line or line.startswith("Run\t"):
                continue
            m = TABLE_RE.match(line)
            if m:
                runs[m.group("run")] = RunData(
                    api_seconds=float(m.group("api")),
                    total_calls=int(m.group("calls")),
                    counts={},
                )
            continue

        if in_detail:
            if not line:
                continue
            header = DETAIL_HEADER_RE.match(line)
            if header:
                current_run = header.group("run")
                runs.setdefault(
                    current_run,
                    RunData(api_seconds=float(header.group("api")), total_calls=0, counts={}),
                ).api_seconds = float(header.group("api"))
                continue
            if current_run and ":" in line:
                counts = {m.group("tool"): int(m.group("count")) for m in COUNT_RE.finditer(line)}
                if counts:
                    runs[current_run].counts.update(counts)

    return runs


def _parse_clean_counts(stream_log: Path) -> tuple[dict[str, int], float]:
    counts: Counter[str] = Counter()
    api_ms = 0.0
    for line in stream_log.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "stream_event" and obj.get("event", {}).get("type") == "content_block_start":
            cb = obj["event"].get("content_block", {})
            if cb.get("type") == "tool_use":
                counts[cb.get("name", "Unknown")] += 1
        elif obj.get("type") == "result":
            api_ms = float(obj.get("duration_api_ms") or 0)
    return dict(counts), api_ms / 1000.0


def _tool_order(counts_a: dict[str, int], counts_b: dict[str, int]) -> list[str]:
    preferred = ["Read", "Bash", "Edit", "Write", "TaskOutput", "Grep", "TodoWrite", "Monitor"]
    seen = set(counts_a) | set(counts_b)
    ordered = [t for t in preferred if t in seen]
    rest = sorted(seen - set(ordered))
    return ordered + rest


def _svg_bar_chart(
    task: str,
    clean: RunData,
    og: RunData,
    clean_api_s: float,
    out_path: Path,
) -> None:
    tools = _tool_order(clean.counts, og.counts)
    max_value = max(max(clean.counts.get(t, 0), og.counts.get(t, 0)) for t in tools) or 1
    width = 1200
    height = 780
    margin = 90
    chart_top = 130
    chart_bottom = 610
    chart_height = chart_bottom - chart_top
    colors = {"clean": "#2f6fed", "og-memory": "#f08a24"}
    n = len(tools)
    if n <= 5:
        bar_width, pair_gap, group_gap = 56, 18, 34
    elif n <= 8:
        bar_width, pair_gap, group_gap = 46, 14, 22
    else:
        bar_width, pair_gap, group_gap = 36, 12, 14

    total_width = n * (2 * bar_width + pair_gap + group_gap)
    start_x = max(margin + 18, (width - total_width) / 2)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="600" y="44" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700">{escape(task)} tool count comparison</text>',
        '<text x="600" y="74" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#555">',
        escape(
            f"clean API {clean_api_s:.1f}s, calls {sum(clean.counts.values())} | "
            f"og-memory API {og.api_seconds:.1f}s, calls {og.total_calls}"
        ),
        '</text>',
        f'<line x1="{margin}" y1="{chart_bottom}" x2="{width - margin}" y2="{chart_bottom}" stroke="#333" stroke-width="2"/>',
        f'<line x1="{margin}" y1="{chart_top}" x2="{margin}" y2="{chart_bottom}" stroke="#333" stroke-width="2"/>',
    ]

    tick_count = 5
    for i in range(tick_count + 1):
        frac = i / tick_count
        y = chart_bottom - int(frac * chart_height)
        value = int(round(frac * max_value))
        parts.extend(
            [
                f'<line x1="{margin - 6}" y1="{y}" x2="{width - margin}" y2="{y}" stroke="#ececec" stroke-width="1"/>',
                f'<text x="{margin - 12}" y="{y + 4}" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#666">{value}</text>',
            ]
        )

    for idx, tool in enumerate(tools):
        x = start_x + idx * (2 * bar_width + pair_gap + group_gap)
        clean_v = clean.counts.get(tool, 0)
        og_v = og.counts.get(tool, 0)
        clean_h = int((clean_v / max_value) * chart_height) if max_value else 0
        og_h = int((og_v / max_value) * chart_height) if max_value else 0
        clean_y = chart_bottom - clean_h
        og_y = chart_bottom - og_h
        clean_x = x
        og_x = x + bar_width + pair_gap

        parts.extend(
            [
                f'<rect x="{clean_x}" y="{clean_y}" width="{bar_width}" height="{clean_h}" fill="{colors["clean"]}" rx="4"/>',
                f'<rect x="{og_x}" y="{og_y}" width="{bar_width}" height="{og_h}" fill="{colors["og-memory"]}" rx="4"/>',
                f'<text x="{clean_x + bar_width/2}" y="{max(clean_y - 8, 124)}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#111">{clean_v}</text>',
                f'<text x="{og_x + bar_width/2}" y="{max(og_y - 8, 124)}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#111">{og_v}</text>',
                f'<text x="{x + bar_width + pair_gap/2}" y="{chart_bottom + 24}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="700" fill="#222">{tool}</text>',
            ]
        )

    legend_x = 860
    legend_y = 104
    for i, (name, color) in enumerate(colors.items()):
        y = legend_y + i * 28
        parts.extend(
            [
                f'<rect x="{legend_x}" y="{y - 12}" width="18" height="18" fill="{color}" rx="3"/>',
                f'<text x="{legend_x + 26}" y="{y + 2}" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#222">{name}</text>',
            ]
        )

    parts.append("</svg>")
    out_path.write_text("\n".join(parts), encoding="utf-8")


def _generate_index(out_dir: Path, tasks: Iterable[str]) -> None:
    lines = [
        "# 10 Task Comparison Charts",
        "",
        "Generated from `og-memory_result.md` and `runs_clean/`.",
        "",
    ]
    for task in tasks:
        fname = f"{task}.svg"
        lines.append(f"- [{task}]({fname})")
        lines.append(f"  - ![]({fname})")
    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--og-summary",
        type=Path,
        default=Path("og-memory_result.md"),
        help="Path to og-memory_result.md",
    )
    parser.add_argument(
        "--clean-root",
        type=Path,
        default=Path("runs_clean"),
        help="Path to the clean runs directory",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("visualize/ten_task_charts"),
        help="Where to write the 10 SVG charts",
    )
    args = parser.parse_args()

    og_runs = _parse_og_memory_markdown(args.og_summary)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for task in TASK_ORDER:
        clean_stream = args.clean_root / task / "logs" / "claude_stream.jsonl"
        if not clean_stream.exists():
            raise SystemExit(f"missing clean run log: {clean_stream}")
        clean_counts, clean_api_s = _parse_clean_counts(clean_stream)
        og = og_runs.get(task)
        if og is None:
            raise SystemExit(f"missing og-memory summary for {task}")
        out_path = args.output_dir / f"{task}.svg"
        _svg_bar_chart(task, RunData(clean_api_s, sum(clean_counts.values()), clean_counts), og, clean_api_s, out_path)

    _generate_index(args.output_dir, TASK_ORDER)
    print(f"Wrote {len(TASK_ORDER)} charts to {args.output_dir}")


if __name__ == "__main__":
    main()
