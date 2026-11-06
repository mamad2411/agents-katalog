#!/usr/bin/env python3
"""Build a logo from a spec file — real geometry, real type, real booleans.

The point of this script is that nobody hand-writes an SVG path. You describe the
mark in JSON (rectangles, circles, polygons, letters set in an installed face) and
the script outlines, combines and exports it. Every boolean is done by Skia's
path engine, so cut-outs are exact and printable, not a stack of fake shapes.

    logo.py build spec.json -o out/
    logo.py build spec.json -o out/ --trim --mono "#ffffff"

Spec
----
{
  "name": "genzys",
  "size": [1000, 1000],
  "palette": {"ink": "#0a1420", "gold": "#fdcc3f"},
  "shapes": [
    {"id": "plate", "rect": [0, 0, 1000, 850], "fill": "gold"},
    {"id": "g", "glyph": {"text": "G", "font": "DIN Alternate",
                          "style": "Bold", "height": 480},
     "center": [500, 425], "fill": "ink"}
  ],
  "ops": [
    {"op": "subtract", "a": "plate", "b": "g", "out": "plate_cut"}
  ],
  "draw": ["plate_cut", "lane"]
}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pathops
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fonts import glyph_path, resolve  # noqa: E402


# --------------------------------------------------------------------------- #
# geometry
# --------------------------------------------------------------------------- #
def _rect(x, y, w, h, r=0.0) -> pathops.Path:
    path = pathops.Path()
    if not r:
        path.moveTo(x, y)
        path.lineTo(x + w, y)
        path.lineTo(x + w, y + h)
        path.lineTo(x, y + h)
        path.close()
        return path

    r = min(r, w / 2, h / 2)
    k = r * 0.5523
    path.moveTo(x + r, y)
    path.lineTo(x + w - r, y)
    path.cubicTo(x + w - r + k, y, x + w, y + r - k, x + w, y + r)
    path.lineTo(x + w, y + h - r)
    path.cubicTo(x + w, y + h - r + k, x + w - r + k, y + h, x + w - r, y + h)
    path.lineTo(x + r, y + h)
    path.cubicTo(x + r - k, y + h, x, y + h - r + k, x, y + h - r)
    path.lineTo(x, y + r)
    path.cubicTo(x, y + r - k, x + r - k, y, x + r, y)
    path.close()
    return path


def _circle(cx, cy, r) -> pathops.Path:
    path = pathops.Path()
    k = r * 0.5523
    path.moveTo(cx, cy - r)
    path.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    path.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    path.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    path.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    path.close()
    return path


def _polygon(points) -> pathops.Path:
    path = pathops.Path()
    path.moveTo(*points[0])
    for point in points[1:]:
        path.lineTo(*point)
    path.close()
    return path


def _glyph(spec: dict, center=None, at=None) -> pathops.Path:
    """Outline text from an installed face and place it where asked.

    pathops.Path.transform() is a no-op in this build, so the offset is baked into
    the drawing matrix instead of being applied afterwards.
    """
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.ttLib import TTFont

    text = spec["text"]
    family = spec["font"]
    style = spec.get("style", "Regular")
    height = float(spec.get("height", 100))
    tracking = float(spec.get("tracking", 0))

    face_path, face_index = resolve(family, style)
    font = TTFont(face_path, fontNumber=face_index, lazy=True)
    upem = font["head"].unitsPerEm
    cap = getattr(font["OS/2"], "sCapHeight", 0) if "OS/2" in font else 0
    scale = (height / cap) if cap else (height / upem)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()

    placed = []
    x_cursor = 0.0
    for char in text:
        name = cmap.get(ord(char))
        if not name:
            continue
        placed.append((name, x_cursor))
        x_cursor += glyph_set[name].width + tracking / 1000 * upem

    if not placed:
        raise SystemExit(f"no glyphs for {text!r} in {family} {style}")

    # Measure first, so the placement can be exact.
    probe = BoundsPen(glyph_set)
    for name, x in placed:
        glyph_set[name].draw(TransformPen(probe, (scale, 0, 0, -scale, x * scale, 0)))
    x0, y0, x1, y1 = probe.bounds or (0, 0, 0, 0)

    if center:
        dx, dy = center[0] - (x0 + x1) / 2, center[1] - (y0 + y1) / 2
    elif at:
        dx, dy = at[0] - x0, at[1] - y0
    else:
        dx, dy = -x0, -y1

    path = pathops.Path()
    pen = pathops.PathPen(path)
    for name, x in placed:
        glyph_set[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x * scale + dx, dy)))
    font.close()
    return path


def _shape(spec: dict) -> pathops.Path:
    if "rect" in spec:
        x, y, w, h = spec["rect"]
        return _rect(x, y, w, h, float(spec.get("radius", 0)))
    if "circle" in spec:
        return _circle(*spec["circle"])
    if "polygon" in spec:
        return _polygon(spec["polygon"])
    if "glyph" in spec:
        return _glyph(spec["glyph"], spec.get("center"), spec.get("at"))
    raise SystemExit(f"shape has no geometry: {spec}")


def _bounds(paths: list[pathops.Path]):
    boxes = [p.bounds for p in paths if p.bounds]
    if not boxes:
        return (0, 0, 0, 0)
    return (
        min(b[0] for b in boxes),
        min(b[1] for b in boxes),
        max(b[2] for b in boxes),
        max(b[3] for b in boxes),
    )


# --------------------------------------------------------------------------- #
# build
# --------------------------------------------------------------------------- #
OPS = {
    "union": pathops.PathOp.UNION,
    "subtract": pathops.PathOp.DIFFERENCE,
    "intersect": pathops.PathOp.INTERSECTION,
    "exclude": pathops.PathOp.XOR,
}


def _inside(inner, outer) -> bool:
    """Bounds dalam bounds? Cukup untuk memutuskan 'inlay' vs 'potongan lepas'."""
    ix0, iy0, ix1, iy1 = _bounds([inner])
    ox0, oy0, ox1, oy1 = _bounds([outer])
    eps = 1.0
    return ix0 >= ox0 - eps and iy0 >= oy0 - eps and ix1 <= ox1 + eps and iy1 <= oy1 + eps


def _flatten(spec: dict, drawn) -> "pathops.Path":
    """Satu path untuk versi satu warna.

    Menjumlahkan semua bentuk begitu saja menghasilkan blok pejal: huruf yang
    tadinya kontras dengan pelat berubah jadi warna yang sama, lalu hilang.
    Jadi lapisan di atas yang warnanya beda DAN berada di dalam siluet dianggap
    inlay — di versi satu warna dia harus jadi lubang, bukan tinta.

    Urutan `draw` = bawah ke atas. Bisa dipaksa lewat `mono: {union:[...], cut:[...]}`.
    """
    cfg = spec.get("mono") or {}
    by_id = dict(drawn)

    if cfg.get("union") or cfg.get("cut"):
        acc = None
        for name in cfg.get("union") or []:
            acc = by_id[name]["path"] if acc is None else pathops.op(acc, by_id[name]["path"], pathops.PathOp.UNION)
        for name in cfg.get("cut") or []:
            acc = pathops.op(acc, by_id[name]["path"], pathops.PathOp.DIFFERENCE) if acc is not None else None
        if acc is None:
            raise SystemExit("mono.union / mono.cut tidak menyebut bentuk yang ada")
        return acc

    acc = drawn[0][1]["path"]
    base_fill = drawn[0][1]["fill"]
    for _, item in drawn[1:]:
        p = item["path"]
        if item["fill"] == base_fill:
            acc = pathops.op(acc, p, pathops.PathOp.UNION)
        elif _inside(p, acc):
            acc = pathops.op(acc, p, pathops.PathOp.DIFFERENCE)
        else:
            acc = pathops.op(acc, p, pathops.PathOp.UNION)
    return acc


def build(spec: dict, out_dir: Path, trim=False, mono=None) -> dict:
    palette = spec.get("palette", {})
    width, height = spec.get("size", [1000, 1000])

    shapes: dict[str, dict] = {}
    for shape in spec["shapes"]:
        shapes[shape["id"]] = {"path": _shape(shape), "fill": shape.get("fill", "ink")}

    ops = spec.get("ops", [])
    for i, op in enumerate(ops):
        a, b = shapes[op["a"]]["path"], shapes[op["b"]]["path"]
        # pathops.op() returns a new Path: op(one, two, operator, fix_winding=...)
        # There is no out-parameter — passing one lands in fix_winding.
        result = pathops.op(a, b, OPS[op["op"]])
        shapes[op["out"]] = {"path": result, "fill": shapes[op["a"]]["fill"]}
        # Jangan buang input yang masih dipakai op berikutnya.
        used_later = {op2[k] for op2 in ops[i + 1:] for k in ("a", "b")}
        if op.get("consume", True):
            for name in (op["a"], op["b"]):
                if name not in used_later:
                    shapes.pop(name, None)

    order = spec.get("draw") or list(shapes)
    drawn = [(name, shapes[name]) for name in order if name in shapes]
    if not drawn:
        raise SystemExit("nothing to draw")

    x0, y0, x1, y1 = _bounds([item["path"] for _, item in drawn])
    if trim:
        view = (x0, y0, x1 - x0, y1 - y0)
    else:
        view = (0, 0, width, height)

    def render(fill_override=None, background=None, single=None) -> str:
        body = []
        if background:
            body.append(f'<rect width="{view[2]:.3f}" height="{view[3]:.3f}" fill="{background}"/>')
        items = [("mono", {"path": single})] if single is not None else drawn
        for _, item in items:
            paint = fill_override or palette.get(item["fill"], item["fill"])
            pen = SVGPathPen(None, ntos=lambda v: f"{v:.2f}")
            item["path"].draw(pen)
            body.append(f'<path d="{pen.getCommands()}" fill="{paint}"/>')
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{view[2]:.3f}" '
            f'height="{view[3]:.3f}" viewBox="{view[0]:.3f} {view[1]:.3f} '
            f'{view[2]:.3f} {view[3]:.3f}">\n  '
            + "\n  ".join(body)
            + "\n</svg>\n"
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    name = spec.get("name", "mark")

    files = {}
    files["mark"] = out_dir / f"{name}.svg"
    files["mark"].write_text(render())

    if mono:
        files["mono"] = out_dir / f"{name}-mono.svg"
        files["mono"].write_text(render(fill_override=mono, single=_flatten(spec, drawn)))
    else:
        print("catatan: tanpa --mono versi satu warna belum ada — logo belum selesai "
              "(aturan 5)", file=sys.stderr)

    colours = {palette.get(item["fill"], item["fill"]) for _, item in drawn}
    report = {
        "name": name,
        "viewBox": [round(v, 2) for v in view],
        "ink": [round(v, 2) for v in (x0, y0, x1 - x0, y1 - y0)],
        "colours": sorted(colours),
        "parts": [name for name, _ in drawn],
        "files": {key: str(value) for key, value in files.items()},
    }
    (out_dir / f"{name}.json").write_text(json.dumps(report, indent=2))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    cmd = sub.add_parser("build")
    cmd.add_argument("spec")
    cmd.add_argument("-o", "--out", default=".")
    cmd.add_argument("--trim", action="store_true", help="crop the viewBox to the ink")
    cmd.add_argument("--mono", metavar="COLOUR", help="also export a one-colour version")

    args = parser.parse_args()
    if args.command == "build":
        spec = json.loads(Path(args.spec).read_text())
        report = build(spec, Path(args.out), trim=args.trim, mono=args.mono)
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
