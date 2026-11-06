#!/usr/bin/env python3
"""design-visual.py — visual regression: bukti bahwa UI tidak berubah tanpa sengaja.

Pakai:
  dvisual <url>                 # run pertama = simpan baseline; berikutnya = bandingkan
  dvisual <url> --update        # jadikan hasil sekarang baseline baru (setelah perubahan disengaja)
  dvisual <url> --threshold 0.5 # toleransi % piksel berubah (default 0.3)
  dvisual <url> --json

Output ~/.agents/refs/<slug>/visual/:
  desktop.png mobile.png     baseline
  last-desktop.png ...       hasil run terakhir
  diff-desktop.png ...       peta perubahan (merah = beda)

Exit: 0 identik/di bawah ambang · 1 ada perubahan melebihi ambang · 2 gagal ambil · 3 Playwright hilang.
"""
import json
import os
import sys
import time
import urllib.parse

HOME = os.path.expanduser("~")
REFS = os.path.join(HOME, ".agents", "refs")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
MAX_H = 6000  # batasi tinggi full-page supaya diff tetap cepat & stabil


def slugify(url):
    u = urllib.parse.urlparse(url)
    host = u.netloc.replace("www.", "") or "ref"
    path = u.path.strip("/").replace("/", "-")[:40]
    return (host + ("-" + path if path else "")).lower().replace("/", "-")


def shoot(page, path, full=True):
    page.screenshot(path=path, full_page=full, animations="disabled")
    return path


def capture(url, out):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright tidak terpasang.", file=sys.stderr)
        return 3

    os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 900},
                                  device_scale_factor=1, user_agent=UA, locale="id-ID")
        page = ctx.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45_000)
        except Exception as exc:
            print(f"gagal membuka {url}: {exc}", file=sys.stderr)
            browser.close()
            return 2
        page.wait_for_timeout(2200)
        # matikan animasi berulang supaya diff tidak berisik
        page.add_style_tag(content="*,*::before,*::after{animation-play-state:paused!important;"
                                   "transition:none!important;caret-color:transparent!important}")
        page.wait_for_timeout(400)
        shoot(page, os.path.join(out, "last-desktop.png"))
        page.wait_for_timeout(700)
        shoot(page, os.path.join(out, "noise-desktop.png"))
        ctx.close()

        mctx = browser.new_context(viewport={"width": 390, "height": 844},
                                   device_scale_factor=2, user_agent=UA, locale="id-ID",
                                   is_mobile=True, has_touch=True)
        mp = mctx.new_page()
        try:
            mp.goto(url, wait_until="domcontentloaded", timeout=45_000)
            mp.wait_for_timeout(1800)
            mp.add_style_tag(content="*,*::before,*::after{animation-play-state:paused!important;"
                                     "transition:none!important}")
            mp.wait_for_timeout(300)
            shoot(mp, os.path.join(out, "last-mobile.png"))
            mp.wait_for_timeout(700)
            shoot(mp, os.path.join(out, "noise-mobile.png"))
        finally:
            mctx.close()
        browser.close()
    return 0


def compare(base_path, last_path, diff_path):
    """Kembalikan (persen_berubah, bbox, tinggi_base, tinggi_last) atau None kalau gagal."""
    from PIL import Image, ImageChops

    base = Image.open(base_path).convert("RGB")
    last = Image.open(last_path).convert("RGB")
    h = min(base.height, last.height, MAX_H)
    w = min(base.width, last.width)
    b = base.crop((0, 0, w, h))
    l = last.crop((0, 0, w, h))

    diff = ImageChops.difference(b, l).convert("L").point(lambda v: 255 if v > 14 else 0)
    changed = sum(1 for v in diff.getdata() if v)
    pct = changed / float(w * h) * 100
    bbox = diff.getbbox()

    if bbox:
        overlay = last.copy().convert("RGB")
        red = Image.new("RGB", overlay.size, (220, 38, 38))
        mask = diff.crop((0, 0, overlay.width, overlay.height)).convert("L")
        overlay.paste(red, (0, 0), mask.point(lambda v: 90 if v else 0))
        overlay.crop((0, 0, w, h)).save(diff_path)
    return round(pct, 3), bbox, base.height, last.height


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = sys.argv[1:]
    if not args:
        sys.exit("pakai: design-visual.py <url> [--update] [--threshold 0.3] [--json]")
    url = args[0]
    threshold = 0.3
    if "--threshold" in flags:
        threshold = float(flags[flags.index("--threshold") + 1])

    out = os.path.join(REFS, slugify(url), "visual")
    code = capture(url, out)
    if code:
        return code

    report = {"url": url, "threshold": threshold, "viewports": {}}
    has_change = False
    for name in ("desktop", "mobile"):
        base = os.path.join(out, f"{name}.png")
        last = os.path.join(out, f"last-{name}.png")
        if "--update" in flags or not os.path.exists(base):
            _copy(last, base)
            report["viewports"][name] = {"status": "baseline"}
            continue
        try:
            pct, bbox, hb, hl = compare(base, last, os.path.join(out, f"diff-{name}.png"))
        except Exception as exc:
            report["viewports"][name] = {"status": "error", "detail": str(exc)[:80]}
            continue

        # Noise floor: beda antara dua bidikan berurutan tanpa perubahan kode
        # (lazy image, karusel). Dikurangkan supaya tidak jadi alarm palsu.
        noise_pct = 0.0
        noise_path = os.path.join(out, f"noise-{name}.png")
        if os.path.exists(noise_path):
            try:
                noise_pct, _, _, _ = compare(last, noise_path, os.path.join(out, f"noise-diff-{name}.png"))
            except Exception:
                noise_pct = 0.0
        effective = round(max(0.0, pct - noise_pct), 3)
        status = "changed" if effective > threshold else "same"
        has_change = has_change or status == "changed"
        report["viewports"][name] = {
            "status": status, "changedPercent": pct, "noisePercent": noise_pct,
            "effectivePercent": effective, "bbox": bbox,
            "heightBase": hb, "heightLast": hl,
            "diff": os.path.join(out, f"diff-{name}.png") if bbox else None,
        }

    json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=2)

    if "--json" in flags:
        print(json.dumps(report, indent=2))
    else:
        print(f"visual {url}")
        for name, r in report["viewports"].items():
            if r["status"] == "baseline":
                print(f"  {name:7s} baseline disimpan")
            elif r["status"] == "error":
                print(f"  {name:7s} gagal: {r['detail']}")
            else:
                mark = "BERUBAH" if r["status"] == "changed" else "sama"
                extra = ""
                if r["status"] == "changed":
                    extra = f" · bbox {r['bbox']} · diff {os.path.basename(r['diff'])}"
                dh = r["heightLast"] - r["heightBase"]
                noise = f" · noise {r['noisePercent']}%" if r.get("noisePercent") else ""
                print(f"  {name:7s} {mark:7s} {r['effectivePercent']}% piksel{extra}"
                      + (f" · tinggi {dh:+d}px" if dh else "") + noise)
        print(f"ambang {threshold}% · hasil {'BERUBAH' if has_change else 'STABIL'}")
        print(f"data  {out.replace(HOME, '~')}/report.json")
    return 1 if has_change else 0


def _copy(src, dst):
    import shutil
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    sys.exit(main())
