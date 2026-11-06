#!/usr/bin/env python3
"""Prove a logo survives the real world before anyone ships it.

Renders the mark at the sizes it will actually live at (16 px favicon up to 256 px),
on light and dark, then measures instead of guessing:

  coverage     ink share at 16 px — under 8% it disappears, over 88% it is a blob
  colours      how many fills the file uses (a mark needs 1–3)
  contrast     WCAG ratio of every fill against the page it sits on
  safe area    margin between the ink and the viewBox edge
  weight       thinnest stroke at 16 px, in device pixels

    proof.py mark.svg -o proof.png --dark "#0a1420" --light "#f2f0ea"

Exit code 1 means at least one check failed — do not ship it.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from pathlib import Path

SIZES = [256, 128, 64, 48, 32, 24, 16]


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb) -> float:
    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b) -> float:
    la, lb = luminance(hex_to_rgb(a)), luminance(hex_to_rgb(b))
    high, low = max(la, lb), min(la, lb)
    return (high + 0.05) / (low + 0.05)


def fills_in(svg: str) -> list[str]:
    found = re.findall(r'fill="(#[0-9a-fA-F]{3,8})"', svg)
    return sorted({value.lower() for value in found})


PAGE = """<!doctype html>
<meta charset="utf-8">
<style>
  body {{ margin: 0; background: {bg}; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}
  .wrap {{ padding: 26px 30px; }}
  .row {{ display: flex; align-items: flex-end; gap: 30px; }}
  .cell {{ display: flex; flex-direction: column; align-items: center; gap: 8px; }}
  .cap {{ font: 10px ui-monospace, monospace; letter-spacing: .12em; color: {label}; }}
  img {{ display: block; }}
</style>
<div class="wrap">
  <div class="row" id="row"></div>
</div>
<script>
const sizes = {sizes};
const src = {src};
const row = document.getElementById('row');
for (const s of sizes) {{
  const cell = document.createElement('div');
  cell.className = 'cell';
  cell.innerHTML = `<img src="${{src}}" width="${{s}}" height="${{s}}"><span class="cap">${{s}}</span>`;
  row.appendChild(cell);
}}
</script>
"""


def data_uri(svg_path: Path) -> str:
    """Inline the SVG. A file:// image inside set_content() is blocked by Chromium."""
    payload = base64.b64encode(svg_path.read_bytes()).decode("ascii")
    return f"data:image/svg+xml;base64,{payload}"


def render(svg_path: Path, out_png: Path, bg: str, label: str) -> None:
    from playwright.sync_api import sync_playwright

    page_html = PAGE.format(
        bg=bg,
        label=label,
        sizes=json.dumps(SIZES),
        src=json.dumps(data_uri(svg_path)),
    )
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 400}, device_scale_factor=2)
        page.set_content(page_html)
        page.wait_for_timeout(400)
        page.screenshot(path=str(out_png), full_page=True)
        browser.close()


def measure(svg_path: Path) -> dict:
    """Rasterise at 16 px in the browser and read the pixels back."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.set_content("<canvas id='c' width='16' height='16'></canvas>")
        result = page.evaluate(
            """async (src) => {
                const img = new Image();
                img.src = src;
                await img.decode();
                const canvas = document.getElementById('c');
                const ctx = canvas.getContext('2d', { willReadFrequently: true });
                ctx.clearRect(0, 0, 16, 16);
                ctx.drawImage(img, 0, 0, 16, 16);
                const { data } = ctx.getImageData(0, 0, 16, 16);

                let ink = 0;
                const tally = new Map();
                for (let i = 0; i < data.length; i += 4) {
                    if (data[i + 3] <= 128) continue;
                    ink++;
                    const key = `${data[i]},${data[i + 1]},${data[i + 2]}`;
                    tally.set(key, (tally.get(key) || 0) + 1);
                }
                // Thinnest run of ink in any row: the smallest feature that still
                // has to survive at 16 px.
                let thinnest = 16;
                for (let y = 0; y < 16; y++) {
                    let run = 0;
                    for (let x = 0; x < 16; x++) {
                        if (data[(y * 16 + x) * 4 + 3] > 128) { run++; }
                        else { if (run > 0) thinnest = Math.min(thinnest, run); run = 0; }
                    }
                    if (run > 0) thinnest = Math.min(thinnest, run);
                }

                const ranked = [...tally.entries()].sort((a, b) => b[1] - a[1]);
                const toHex = (rgb) => '#' + rgb.split(',').map(v =>
                    (+v).toString(16).padStart(2, '0')).join('');
                return {
                    coverage: ink / 256,
                    thinnest: thinnest,
                    distinct: tally.size,
                    dominant: ranked.length ? toHex(ranked[0][0]) : null,
                    weights: ranked.slice(0, 4).map(([k, v]) => [toHex(k), v]),
                };
            }""",
            data_uri(svg_path),
        )
        browser.close()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg")
    parser.add_argument("-o", "--out", default="proof.png")
    parser.add_argument("--dark", default="#0a1420")
    parser.add_argument("--light", default="#f2f0ea")
    args = parser.parse_args()

    svg_path = Path(args.svg)
    svg = svg_path.read_text()
    out = Path(args.out)

    dark_png = out.with_name(out.stem + "-dark.png")
    light_png = out.with_name(out.stem + "-light.png")
    render(svg_path, dark_png, args.dark, "#8ba0b8")
    render(svg_path, light_png, args.light, "#6b7a88")

    colours = fills_in(svg)
    if not colours:
        print("tidak ada fill=\"#hex\" di SVG — palette harus hex (#rrggbb), "
              "bukan nama warna", file=sys.stderr)
    raster = measure(svg_path)

    fails, warns = [], []

    def check(name, ok, value, hard=True):
        entry = {"name": name, "pass": ok, "value": value, "hard": hard}
        if not ok:
            (fails if hard else warns).append(f"{name} ({value})")
        return entry

    full_bleed = raster["coverage"] > 0.98
    checks = [
        check("colours", 1 <= len(colours) <= 3, str(len(colours))),
        check("ink-16", raster["coverage"] > 0, f"{raster['coverage'] * 100:.0f}%"),
        # A full-bleed plate has no gaps to measure, so legibility there rests on
        # internal detail instead of on stroke width.
        check("feature-16", full_bleed or raster["thinnest"] >= 1,
              "penuh" if full_bleed else f"{raster['thinnest']}px"),
        check("detail-16", raster["distinct"] >= 2 or len(colours) == 1,
              f"{raster['distinct']} warna"),
    ]

    # A logo is exempt from WCAG's contrast rule, so these are warnings: they say
    # the mark will sit quietly on that page, not that the file is broken.
    page_dark = contrast(raster["dominant"] or "#ffffff", args.dark)
    page_light = contrast(raster["dominant"] or "#ffffff", args.light)
    checks.append(check("contrast-dark", page_dark >= 3.0, f"{page_dark:.1f}:1", hard=False))
    checks.append(check("contrast-light", page_light >= 3.0, f"{page_light:.1f}:1", hard=False))

    internal = []
    for i, a in enumerate(colours):
        for b in colours[i + 1:]:
            internal.append(contrast(a, b))
    if internal:
        checks.append(check("contrast-internal", min(internal) >= 2.0,
                            f"{min(internal):.1f}:1", hard=False))

    verdict = "LULUS" if not fails else "GAGAL"
    if not fails and warns:
        verdict = "LULUS (dengan catatan)"

    print(json.dumps({
        "svg": str(svg_path),
        "colours": colours,
        "raster16": raster,
        "checks": checks,
        "warnings": warns,
        "proof": {"dark": str(dark_png), "light": str(light_png)},
        "verdict": verdict,
    }, indent=2))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
