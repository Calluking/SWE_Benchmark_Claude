#!/usr/bin/env python3
"""Render a simple SVG chart comparing tool counts for two runs."""

from __future__ import annotations

import argparse
from pathlib import Path
from html import escape


COUNTS = {
    "og-memory": {
        "Read": 18,
        "Bash": 17,
        "Edit": 1,
        "Write": 1,
        "TaskOutput": 4,
    },
    "clean": {
        "Read": 11,
        "Bash": 67,
        "Edit": 1,
        "Write": 1,
    },
}


def _bar_height(value: int, max_value: int, plot_height: int) -> int:
    if max_value <= 0:
        return 0
    return int((value / max_value) * plot_height)


def _make_svg() -> str:
    tools = ["Read", "Bash", "Edit", "Write", "TaskOutput"]
    max_value = max(
        max(run.get(tool, 0) for tool in tools)
        for run in COUNTS.values()
    ) or 1

    width = 1200
    height = 760
    margin = 90
    chart_top = 130
    chart_bottom = 600
    chart_height = chart_bottom - chart_top
    bar_width = 48
    pair_gap = 16
    group_gap = 22
    colors = {"clean": "#2f6fed", "og-memory": "#f08a24"}

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="600" y="46" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700">sqlfluff__sqlfluff-2419 tool count comparison</text>',
        '<text x="600" y="76" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#555">',
        escape("og-memory: Read 18, Bash 17, Edit 1, Write 1, TaskOutput 4 | clean: Read 11, Bash 67, Edit 1, Write 1"),
        '</text>',
        f'<line x1="{margin}" y1="{chart_bottom}" x2="{width - margin}" y2="{chart_bottom}" stroke="#333" stroke-width="2"/>',
        f'<line x1="{margin}" y1="{chart_top}" x2="{margin}" y2="{chart_bottom}" stroke="#333" stroke-width="2"/>',
    ]

    tick_count = 5
    for i in range(tick_count + 1):
        frac = i / tick_count
        y = chart_bottom - int(frac * chart_height)
        value = int(frac * max_value)
        parts.extend(
            [
                f'<line x1="{margin - 6}" y1="{y}" x2="{width - margin}" y2="{y}" stroke="#e9e9e9" stroke-width="1"/>',
                f'<text x="{margin - 12}" y="{y + 4}" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#666">{value}</text>',
            ]
        )

    group_x = margin + 35
    for idx, tool in enumerate(tools):
        x = group_x + idx * (2 * bar_width + pair_gap + group_gap)
        og_v = COUNTS["og-memory"].get(tool, 0)
        clean_v = COUNTS["clean"].get(tool, 0)
        og_h = _bar_height(og_v, max_value, chart_height)
        clean_h = _bar_height(clean_v, max_value, chart_height)
        og_y = chart_bottom - og_h
        clean_y = chart_bottom - clean_h
        clean_x = x
        og_x = x + bar_width + pair_gap

        parts.extend(
            [
                f'<rect x="{clean_x}" y="{clean_y}" width="{bar_width}" height="{clean_h}" fill="{colors["clean"]}" rx="4"/>',
                f'<rect x="{og_x}" y="{og_y}" width="{bar_width}" height="{og_h}" fill="{colors["og-memory"]}" rx="4"/>',
                f'<text x="{clean_x + bar_width/2}" y="{clean_y - 8}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#111">{clean_v}</text>',
                f'<text x="{og_x + bar_width/2}" y="{og_y - 8}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#111">{og_v}</text>',
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
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Where to save the SVG chart.")
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(_make_svg(), encoding="utf-8")


if __name__ == "__main__":
    main()
