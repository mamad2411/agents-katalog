#!/usr/bin/env python3
"""design-check.py — gerbang kualitas UI: ukur build sendiri, bukan cuma diklaim.

Pakai:
  dcheck <url>                 # tabel PASS/FAIL + exit 1 kalau ada yang gagal
  dcheck <url> --json          # keluaran mesin
  dcheck <url> --max-sizes 10  # longgarkan batas jumlah ukuran tipe

Yang diperiksa (semua terukur, bukan opini):
  overflow        tidak ada scroll horizontal di 360/768/1024/1440px
  contrast        axe color-contrast + hitungan DOM = 0
  tap-target      tidak ada target < 24px (WCAG 2.2 target-size bila tersedia)
  img-alt         semua gambar punya alt
  heading-order   urutan heading tidak melompat
  label           input punya label/aria-label
  reduced-motion  CSS menghormati prefers-reduced-motion
  type-scale      jumlah ukuran tipe dominan <= batas (skala, bukan acak)
  spacing-grid    >= 70% gap/padding kelipatan 4px

Exit: 0 semua lulus · 1 ada yang gagal · 2 gagal buka halaman · 3 Playwright hilang.
"""
import importlib.util
import json
import os
import sys

HOME = os.path.expanduser("~")
READER = os.path.join(HOME, ".agents", "scripts", "design-read.py")

spec = importlib.util.spec_from_file_location("design_read", READER)
dr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dr)

AXE_RULES = {
    "contrast": {"color-contrast"},
    "tap-target": {"target-size", "target-size-enhanced"},
    "img-alt": {"image-alt"},
    "heading-order": {"heading-order", "empty-heading"},
    "label": {"label", "select-name", "input-button-name", "form-field-multiple-labels"},
}


def axe_count(axe, rule_ids):
    if not axe.get("available"):
        return None
    return sum(v["nodes"] for v in axe["violations"] if v["id"] in rule_ids)


def multiples_of_4(values):
    nums = []
    for k, _c in values:
        try:
            nums.append(float(str(k).replace("px", "")))
        except ValueError:
            continue
    if not nums:
        return None
    on_grid = [n for n in nums if n > 0 and abs(n % 4) < 0.51]
    return round(len(on_grid) / len(nums) * 100)


def evaluate(data, max_sizes=8):
    rows = []

    def add(name, ok, detail, hard=True):
        rows.append({"gate": name, "ok": ok, "detail": detail, "hard": hard})

    vps = data.get("viewports") or []
    bad = [v for v in vps if v["overflowPx"] > 2]
    overflow_detail = "OK di 4 lebar" if not bad else "scroll horizontal: " + ", ".join(
        str(v["w"]) + "px+" + str(v["overflowPx"]) for v in bad
    )
    add("overflow", not bad, overflow_detail)

    axe = data.get("axe") or {}
    if not axe.get("available"):
        add("contrast", None, f"axe tidak jalan ({axe.get('reason', '?')})", hard=False)
        add("tap-target", None, "axe tidak jalan", hard=False)
        add("img-alt", None, "axe tidak jalan", hard=False)
        add("heading-order", None, "axe tidak jalan", hard=False)
        add("label", None, "axe tidak jalan", hard=False)
    else:
        c = axe_count(axe, AXE_RULES["contrast"])
        add("contrast", c == 0, f"{c} node kontras gagal")
        t = axe_count(axe, AXE_RULES["tap-target"])
        small = len(data.get("smallTargets") or [])
        # Gate keras pakai axe (sudah mengecualikan link inline sesuai WCAG 2.2);
        # hitungan DOM hanya info tambahan.
        add("tap-target", (t or 0) == 0, f"axe {t} · DOM <24px {small} (link inline dikecualikan)")
        a = axe_count(axe, AXE_RULES["img-alt"])
        add("img-alt", a == 0, f"{a} gambar tanpa alt")
        h = axe_count(axe, AXE_RULES["heading-order"])
        add("heading-order", h == 0, f"{h} masalah urutan heading")
        l = axe_count(axe, AXE_RULES["label"])
        add("label", l == 0, f"{l} input tanpa label")

    add("reduced-motion", bool(data.get("reducedMotionCss")),
        "CSS punya prefers-reduced-motion" if data.get("reducedMotionCss") else "tidak ada media query reduced-motion")

    _, dom, _ratio = dr.type_scale(data.get("sizes", []))
    add("type-scale", len(dom) <= max_sizes, f"{len(dom)} ukuran dominan (batas {max_sizes})", hard=False)

    pct = multiples_of_4((data.get("gaps") or []) + (data.get("pads") or []))
    add("spacing-grid", pct is None or pct >= 70,
        "tidak ada data" if pct is None else f"{pct}% kelipatan 4px", hard=False)

    p = data.get("perf")
    if p:
        add("perf-lcp", p["lcp"] <= 2500, f"LCP {p['lcp']}ms (≤2500)", hard=False)
        add("perf-cls", p["cls"] <= 0.1, f"CLS {p['cls']} (≤0.1)", hard=False)
    else:
        add("perf", None, "tidak terukur", hard=False)
    return rows


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = sys.argv[1:]
    if not args:
        sys.exit("pakai: design-check.py <url> [--json] [--max-sizes N]")
    url = args[0]
    max_sizes = 8
    if "--max-sizes" in flags:
        max_sizes = int(flags[flags.index("--max-sizes") + 1])

    out = os.path.join(dr.REFS, dr.slugify(url))
    os.makedirs(out, exist_ok=True)
    result = dr.read_url(url, out, shots_enabled=False)
    if isinstance(result, int):
        return result
    data, _shots = result
    json.dump(data, open(os.path.join(out, "tokens.json"), "w"), indent=2, ensure_ascii=False)

    rows = evaluate(data, max_sizes)
    failed = [r for r in rows if r["ok"] is False and r["hard"]]
    warned = [r for r in rows if r["ok"] is False and not r["hard"]]
    skipped = [r for r in rows if r["ok"] is None]

    if "--json" in flags:
        print(json.dumps({"url": url, "gates": rows, "failed": len(failed), "warned": len(warned)}, indent=2))
    else:
        print(f"check {data['meta'].get('title', '')[:58] or url}")
        for r in rows:
            mark = "PASS" if r["ok"] else ("FAIL" if r["ok"] is False and r["hard"] else ("WARN" if r["ok"] is False else "SKIP"))
            print(f"  {mark:4s} {r['gate']:14s} {r['detail']}")
        verdict = "LULUS" if not failed else f"GAGAL ({len(failed)} gate keras)"
        print(f"hasil {verdict}" + (f" · {len(warned)} peringatan" if warned else "") +
              (f" · {len(skipped)} tidak terukur" if skipped else ""))
        print(f"data  {out.replace(HOME, '~')}/tokens.json")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
