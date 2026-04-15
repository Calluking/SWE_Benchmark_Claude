#!/usr/bin/env python3
"""Render a simple SVG pie chart for API time comparison."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from html import escape


API_MS = {
    "clean": 210_642,
    "og-memory": 185_554,
}


def _polar_to_xy(cx: float, cy: float, r: float, angle_deg: float) -> tuple[float, float]:
    rad = math.radians(angle_deg)
    return cx + r * math.cos(rad), cy + r * math.sin(rad)


def _arc_path(cx: float, cy: float, r: float, start_deg: float, end_deg: float) -> str:
    start_x, start_y = _polar_to_xy(cx, cy, r, start_deg)
    end_x, end_y = _polar_to_xy(cx, cy, r, end_deg)
    large_arc = 1 if end_deg - start_deg > 180 else 0
    return (
        f"M {cx:.2f} {cy:.2f} "
        f"L {start_x:.2f} {start_y:.2f} "
        f"A {r:.2f} {r:.2f} 0 {large_arc} 1 {end_x:.2f} {end_y:.2f} "
        f"Z"
    )


def _make_svg() -> str:
    total = sum(API_MS.values()) or 1
    values = list(API_MS.items())
    colors = {"clean": "#2f6fed", "og-memory": "#f08a24"}

    width = 980
    height = 520
    cx = 260
    cy = 260
    r = 160

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="490" y="42" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700">sqlfluff__sqlfluff-2419 API time comparison</text>',
        '<text x="490" y="74" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#555">',
        escape(f"clean: {API_MS['clean']:,} ms | og-memory: {API_MS['og-memory']:,} ms"),
        '</text>',
    ]

    start_angle = -90.0
    label_rows = []
    for name, value in values:
        sweep = (value / total) * 360.0
        end_angle = start_angle + sweep
        path = _arc_path(cx, cy, r, start_angle, end_angle)
        parts.append(f'<path d="{path}" fill="{colors[name]}"/>')

        mid_angle = start_angle + sweep / 2.0
        label_rows.append((name, value, value / total * 100, mid_angle))
        start_angle = end_angle

    label_x = 560
    label_y = 300
    row_gap = 36
    for i, (name, value, pct, mid_angle) in enumerate(label_rows):
        sx, sy = _polar_to_xy(cx, cy, r, mid_angle)
        row_y = label_y + i * row_gap
        parts.extend(
            [
                f'<line x1="{sx:.2f}" y1="{sy:.2f}" x2="{label_x - 18}" y2="{row_y - 5}" stroke="#666" stroke-width="1.5"/>',
                f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="3.5" fill="#666"/>',
                f'<text x="{label_x}" y="{row_y}" text-anchor="start" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#111">{name}: {value:,} ms ({pct:.1f}%)</text>',
            ]
        )

    parts.extend(
        [
            f'<rect x="560" y="175" width="18" height="18" fill="{colors["clean"]}" rx="3"/>',
            '<text x="586" y="189" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#222">clean</text>',
            f'<rect x="560" y="203" width="18" height="18" fill="{colors["og-memory"]}" rx="3"/>',
            '<text x="586" y="217" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#222">og-memory</text>',
            '<text x="560" y="280" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="#444">This pie chart shows only API time, not wall-clock time.</text>',
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
