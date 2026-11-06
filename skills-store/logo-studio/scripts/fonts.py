#!/usr/bin/env python3
"""Resolve a font family + style to a file on disk, and pull glyph outlines out of it.

macOS keeps fonts in four places. We scan them once, cache the (family, style) ->
path map, and re-scan when a family is missing. No network, no font server.

    fonts.py list                 # every family, with its styles
    fonts.py path "DIN Alternate" Bold
    fonts.py glyph "DIN Alternate" Bold G 480
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont, TTCollection

FONT_DIRS = [
    Path.home() / "Library/Fonts",
    Path("/Library/Fonts"),
    Path("/System/Library/Fonts"),
    Path("/System/Library/Fonts/Supplemental"),
]
CACHE = Path(__file__).resolve().parent.parent / ".cache" / "fonts.json"

STYLE_ALIASES = {
    "regular": ["regular", "book", "roman", "normal"],
    "bold": ["bold", "semibold", "demi", "heavy"],
    "light": ["light", "thin", "extralight", "ultralight"],
    "italic": ["italic", "oblique"],
}


def _faces_in(path: Path):
    """Yield (family, style, path) for every face in a font file."""
    try:
        if path.suffix.lower() in {".ttc", ".otc"}:
            fonts = TTCollection(str(path), lazy=True).fonts
        else:
            fonts = [TTFont(str(path), lazy=True, fontNumber=0)]
    except Exception:
        return

    for index, font in enumerate(fonts):
        try:
            names = font["name"]
            family = names.getDebugName(16) or names.getDebugName(1)
            style = names.getDebugName(17) or names.getDebugName(2) or "Regular"
            if family:
                # A .ttc holds several faces; remember which one this is.
                yield family, style, str(path), index
        except Exception:
            continue
        finally:
            try:
                font.close()
            except Exception:
                pass


def scan(force: bool = False) -> dict:
    if CACHE.exists() and not force:
        try:
            return json.loads(CACHE.read_text())
        except Exception:
            pass

    index: dict[str, dict[str, str]] = {}
    for folder in FONT_DIRS:
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*")):
            if path.suffix.lower() not in {".ttf", ".otf", ".ttc", ".otc"}:
                continue
            for family, style, file_path, face in _faces_in(path):
                index.setdefault(family, {}).setdefault(style, [file_path, face])

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(index, indent=0, sort_keys=True))
    return index


def resolve(family: str, style: str = "Regular", refresh: bool = True):
    """Return (file path, face index) for a family + style."""
    if Path(family).is_file():
        return family, 0

    index = scan()
    styles = index.get(family)
    if not styles and refresh:
        styles = scan(force=True).get(family)
    if not styles:
        raise SystemExit(f"font family not installed: {family}")

    def as_pair(value):
        return (value, 0) if isinstance(value, str) else tuple(value)

    if style in styles:
        return as_pair(styles[style])

    wanted = style.lower()
    for alias in STYLE_ALIASES.get(wanted, []):
        for name, value in styles.items():
            if name.lower() == alias:
                return as_pair(value)
    for name, value in styles.items():
        if wanted in name.lower():
            return as_pair(value)
    return as_pair(next(iter(styles.values())))


def glyph_path(family: str, style: str, text: str, size: float,
               tracking: float = 0.0, cap_align: bool = True):
    """Outline `text` from a real face. Returns (svg path data, (x, y, w, h)).

    size is the cap height in document units when cap_align is set — the optical
    height a mark needs, not the em box. tracking is extra space in 1/1000 em.
    The path is translated so its ink starts at (0, 0).
    """
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.transformPen import TransformPen

    path, face = resolve(family, style)
    font = TTFont(path, fontNumber=face, lazy=True)
    upem = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()

    cap = getattr(font["OS/2"], "sCapHeight", 0) if "OS/2" in font else 0
    scale = (size / cap) if (cap_align and cap) else (size / upem)

    glyphs = []
    x_cursor = 0.0
    for char in text:
        name = cmap.get(ord(char))
        if not name:
            continue
        glyphs.append((name, x_cursor * scale))
        x_cursor += glyph_set[name].width + tracking / 1000 * upem

    if not glyphs:
        raise SystemExit(f"no glyphs for {text!r} in {family} {style}")

    def draw(pen, dx=0.0, dy=0.0):
        for name, x in glyphs:
            glyph_set[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x + dx, dy)))

    # Pass 1: exact ink bounds (H/V commands make regex measuring unreliable).
    bounds = BoundsPen(glyph_set)
    draw(bounds)
    x0, y0, x1, y1 = bounds.bounds or (0, 0, 0, 0)

    # Pass 2: the same shapes, shifted so the ink sits at the origin.
    out = SVGPathPen(glyph_set, ntos=lambda v: f"{v:.3f}")
    draw(out, -x0, -y1)
    font.close()

    return out.getCommands(), (0.0, 0.0, x1 - x0, y1 - y0)


def _ink_bounds(d: str) -> tuple[float, float, float, float]:
    """Bounding box of an absolute-coordinate path (M/L/C/Q/Z only)."""
    import re

    numbers = re.findall(r"-?\d+(?:\.\d+)?", d)
    xs = [float(v) for i, v in enumerate(numbers) if i % 2 == 0]
    ys = [float(v) for i, v in enumerate(numbers) if i % 2 == 1]
    if not xs or not ys:
        return 0.0, 0.0, 0.0, 0.0
    return min(xs), min(ys), max(xs), max(ys)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    command = argv[1]

    if command == "list":
        index = scan()
        needle = argv[2].lower() if len(argv) > 2 else ""
        for family in sorted(index):
            if needle and needle not in family.lower():
                continue
            print(f"{family}: {', '.join(sorted(index[family]))}")
        return 0

    if command == "path":
        path, face = resolve(argv[2], argv[3] if len(argv) > 3 else "Regular")
        print(f"{path}#{face}" if face else path)
        return 0

    if command == "glyph":
        d, box = glyph_path(argv[2], argv[3], argv[4], float(argv[5]))
        print(json.dumps({"d": d, "bounds": box}))
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
