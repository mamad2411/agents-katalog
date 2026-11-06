#!/usr/bin/env python3
"""design-read.py — "lensa" referensi UI/UX: baca halaman nyata (Framer, Dribbble,
Figma Community, situs produk apa pun) lalu keluarkan angka + screenshot yang bisa
dipakai AI, bukan kesan "katanya bagus".

Pakai:
  design-read.py <url>            # analisa halaman -> ~/.agents/refs/<slug>/
  design-read.py <file.png>       # baca screenshot lokal (warna dominan + dimensi)
  design-read.py <url> --no-shot  # tanpa screenshot (lebih cepat)
  design-read.py <url> --json     # cetak tokens.json ke stdout

Output ~/.agents/refs/<slug>/:
  desktop.png  desktop-hero.png  mobile.png
  tokens.json   angka mentah (palet, type scale, spacing, radius, section, CTA, a11y)
  notes.md      ringkasan siap dibaca AI

Exit: 0 sukses · 1 argumen salah · 2 gagal buka halaman · 3 Playwright tidak ada.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HOME = os.path.expanduser("~")
REFS = os.path.join(HOME, ".agents", "refs")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

EXTRACT_JS = r"""
() => {
  const count = (o, k) => { if (k) o[k] = (o[k] || 0) + 1; };
  const rgb = (s) => {
    const m = (s || '').match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(',').map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const hex = (c) => (c ? '#' + [c.r, c.g, c.b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('') : 'transparent');
  const lum = (c) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  };
  const contrast = (a, b) => {
    const [l1, l2] = [lum(a), lum(b)].sort((x, y) => y - x);
    return (l1 + 0.05) / (l2 + 0.05);
  };

  const fonts = {}, sizes = {}, weights = {}, textColors = {}, bgColors = {},
        lineHeights = {}, radii = {}, shadows = {}, gaps = {}, pads = {}, containers = {},
        durations = {}, easings = {};
  const sections = [], ctas = [], images = [], headings = [], smallTargets = [], lowContrast = [];
  const bodyBg = rgb(getComputedStyle(document.body).backgroundColor) || { r: 255, g: 255, b: 255, a: 1 };

  const visible = (el, r) => {
    const cs = getComputedStyle(el);
    return r.width > 6 && r.height > 6 && cs.display !== 'none' &&
           cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0.05;
  };

  const all = [...document.querySelectorAll('body *')];
  let counted = 0;
  for (const el of all) {
    const r = el.getBoundingClientRect();
    if (!visible(el, r)) continue;
    counted++;
    const cs = getComputedStyle(el);

    const gapVal = cs.columnGap !== 'normal' ? cs.columnGap : cs.gap;
    if (gapVal && gapVal !== 'normal' && gapVal !== '0px') count(gaps, gapVal);
    if (cs.transitionDuration && cs.transitionDuration !== '0s') count(durations, cs.transitionDuration);
    if (cs.animationDuration && cs.animationDuration !== '0s') count(durations, cs.animationDuration);
    if (cs.transitionTimingFunction && cs.transitionTimingFunction !== 'ease') count(easings, cs.transitionTimingFunction);
    count(radii, cs.borderRadius);
    if (cs.boxShadow && cs.boxShadow !== 'none') count(shadows, cs.boxShadow);
    const pt = Math.round(parseFloat(cs.paddingTop)), pl = Math.round(parseFloat(cs.paddingLeft));
    if (pt > 3) count(pads, pt + 'px');
    if (pl > 3) count(pads, pl + 'px');
    if (cs.maxWidth && cs.maxWidth !== 'none') count(containers, cs.maxWidth);

    const bg = rgb(cs.backgroundColor);
    if (bg && bg.a > 0.5) count(bgColors, hex(bg));

    const isLeafText = (el.children.length === 0) && (el.textContent || '').trim();
    if (isLeafText) {
      const fg = rgb(cs.color);
      const size = Math.round(parseFloat(cs.fontSize));
      count(fonts, cs.fontFamily.split(',')[0].replace(/["']/g, ''));
      count(sizes, size + 'px');
      count(weights, cs.fontWeight);
      count(lineHeights, cs.lineHeight);
      if (fg) {
        count(textColors, hex(fg));
        if (fg.a > 0.5 && bg && bg.a > 0.5) {
          const ratio = contrast(fg, bg);
          if (ratio < 4.5 && parseFloat(cs.fontSize) < 24 && lowContrast.length < 6) {
            lowContrast.push({ text: (el.textContent || '').trim().slice(0, 40), ratio: Math.round(ratio * 10) / 10 });
          }
        }
      }
    }

    const tag = el.tagName.toLowerCase();
    if (/^h[1-6]$/.test(tag) && (el.textContent || '').trim()) {
      headings.push({ level: Number(tag[1]), text: el.textContent.trim().slice(0, 60) });
    }
    if ((tag === 'button' || tag === 'a') && r.height < 24 && (el.textContent || '').trim()) {
      smallTargets.push({ text: el.textContent.trim().slice(0, 30), h: Math.round(r.height) });
    }
    if (tag === 'button' || (tag === 'a' && bg && bg.a > 0.5)) {
      const label = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
      const fgHex = rgb(cs.color) ? hex(rgb(cs.color)) : null;
      const buttonSized = r.height >= 24 && r.height <= 96 && r.width <= 480;
      const sameAsBody = bg && Math.abs(bg.r - bodyBg.r) < 8 && Math.abs(bg.g - bodyBg.g) < 8 && Math.abs(bg.b - bodyBg.b) < 8;
      if (label && buttonSized && !sameAsBody && fgHex !== '#0000ee') {
        ctas.push({
          label, tag,
          bg: hex(bg),
          fg: fgHex,
          radius: cs.borderRadius, h: Math.round(r.height), w: Math.round(r.width),
          weight: cs.fontWeight, size: Math.round(parseFloat(cs.fontSize)),
          y: Math.round(r.top + scrollY),
        });
      }
    }
  }

  for (const el of [...document.querySelectorAll('img')]) {
    const r = el.getBoundingClientRect();
    if (r.width < 24 || r.height < 24) continue;
    images.push({
      w: Math.round(r.width), h: Math.round(r.height),
      ratio: Math.round((r.width / Math.max(r.height, 1)) * 100) / 100,
      alt: (el.getAttribute('alt') || '').slice(0, 60), missingAlt: !el.getAttribute('alt'),
      loading: el.getAttribute('loading') || 'eager',
      y: Math.round(r.top + scrollY),
    });
  }

  // Section = blok anak langsung <main> (atau body bila tak ada main), urut vertikal.
  // Bila pembungkusnya cuma 1 blok besar, turun satu level supaya section tetap terlihat.
  let root = document.querySelector('main') || document.body;
  const kidsOf = (el) => [...el.children].filter(c => c.getBoundingClientRect().height >= 80);
  for (let depth = 0; depth < 3; depth++) {
    const kids = kidsOf(root);
    if (kids.length >= 3) break;
    const next = [...root.children].sort((a, b) => b.children.length - a.children.length)[0];
    if (!next || next.children.length === 0) break;
    root = next;
  }
  // Deteksi grid: kumpulan anak berukuran hampir sama (kartu) -> kolom, baris, lebar kartu.
  const gridInfo = (scope) => {
    let best = null;
    const cands = [scope, ...scope.querySelectorAll('div,ul,section,ol')].slice(0, 600);
    for (const c of cands) {
      const kids = [...c.children].filter(k => k.getBoundingClientRect().height > 40);
      if (kids.length < 4) continue;
      const rects = kids.map(k => k.getBoundingClientRect());
      const ws = rects.map(r => Math.round(r.width)).sort((a, b) => a - b);
      const median = ws[Math.floor(ws.length / 2)];
      if (median < 80) continue;  // 1-2px = spacer/garis, bukan kartu
      const same = ws.filter(w => Math.abs(w - median) <= 4).length;
      if (same < 4) continue;
      const rows = {};
      for (const r of rects) { const t = Math.round(r.top); rows[t] = (rows[t] || 0) + 1; }
      const cols = Math.max(...Object.values(rows));
      const info = { cols, rows: Object.keys(rows).length, cardW: median, count: same };
      if (!best || info.count > best.count) best = info;
    }
    return best;
  };

  for (const el of [...root.children]) {
    const r = el.getBoundingClientRect();
    if (r.height < 80) continue;
    const cs = getComputedStyle(el);
    const txt = (el.innerText || '').trim().replace(/\s+/g, ' ');
    const bg = rgb(cs.backgroundColor);
    sections.push({
      tag: el.tagName.toLowerCase(),
      y: Math.round(r.top + scrollY), h: Math.round(r.height),
      bg: bg && bg.a > 0.5 ? hex(bg) : 'transparent',
      display: cs.display,
      hasImage: !!el.querySelector('img, video, canvas, svg'),
      hasForm: !!el.querySelector('input, textarea, select'),
      headings: [...el.querySelectorAll('h1,h2,h3')].slice(0, 2).map(h => h.textContent.trim().slice(0, 50)),
      text: txt.slice(0, 120),
      grid: gridInfo(el),
    });
  }

  const top = (o, n) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n);

  return {
    meta: {
      title: document.title,
      description: (document.querySelector('meta[name=description]') || {}).content || '',
      lang: document.documentElement.lang || '',
      height: document.body.scrollHeight,
      width: innerWidth,
      counted,
      bodyBg: hex(bodyBg),
    },
    fonts: top(fonts, 5), sizes: top(sizes, 14), weights: top(weights, 5),
    textColors: top(textColors, 8), bgColors: top(bgColors, 8),
    lineHeights: top(lineHeights, 5), radii: top(radii, 6), shadows: top(shadows, 4),
    gaps: top(gaps, 8), pads: top(pads, 8), containers: top(containers, 5),
    durations: top(durations, 5), easings: top(easings, 4),
    sections: sections.slice(0, 14), ctas: ctas.slice(0, 12), images: images.slice(0, 20),
    headings, smallTargets: smallTargets.slice(0, 6), lowContrast,
    reducedMotionCss: (() => {
      for (const sheet of document.styleSheets) {
        try {
          for (const rule of sheet.cssRules) {
            if ((rule.conditionText || '').includes('prefers-reduced-motion')) return true;
          }
        } catch (e) { /* stylesheet lintas-origin */ }
      }
      return false;
    })(),
  };
}
"""


VIEWPORTS = [(360, 780), (768, 1024), (1024, 768), (1440, 900)]
AXE_CDN = "https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js"


PERF_JS = r"""
async () => await new Promise((resolve) => {
  let lcp = 0, cls = 0;
  try {
    new PerformanceObserver((l) => { for (const e of l.getEntries()) lcp = e.startTime; })
      .observe({ type: 'largest-contentful-paint', buffered: true });
  } catch (e) {}
  try {
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) if (!e.hadRecentInput) cls += e.value;
    }).observe({ type: 'layout-shift', buffered: true });
  } catch (e) {}
  setTimeout(() => {
    const nav = performance.getEntriesByType('navigation')[0] || {};
    const fcp = (performance.getEntriesByType('paint').find((p) => p.name === 'first-contentful-paint') || {}).startTime || 0;
    resolve({
      ttfb: Math.round(nav.responseStart || 0),
      fcp: Math.round(fcp),
      lcp: Math.round(lcp),
      cls: Math.round(cls * 1000) / 1000,
    });
  }, 900);
})
"""


def probe_viewports(page):
    """Cek layout di 4 lebar: apakah ada scroll horizontal / elemen keluar layar."""
    out = []
    for w, h in VIEWPORTS:
        try:
            page.set_viewport_size({"width": w, "height": h})
            page.wait_for_timeout(500)
            r = page.evaluate(
                """() => {
                  const de = document.documentElement;
                  const over = de.scrollWidth - de.clientWidth;
                  const bad = [];
                  for (const el of document.querySelectorAll('body *')) {
                    const b = el.getBoundingClientRect();
                    if (b.width > 0 && b.right > innerWidth + 2) {
                      bad.push({ tag: el.tagName.toLowerCase(), right: Math.round(b.right) });
                    }
                  }
                  bad.sort((a, b) => b.right - a.right);
                  return { w: innerWidth, overflowPx: Math.max(0, over), beyond: bad.length, worst: bad.slice(0, 3) };
                }"""
            )
            out.append(r)
        except Exception:
            continue
    return out


def run_axe(page):
    """Audit a11y standar industri (axe-core WCAG 2.1 A/AA). Gagal muat = jujur, bukan lolos.
    Sumber di-inject lewat evaluate (bukan <script src>) supaya CSP situs tidak memblokir."""
    cache = os.path.join(HOME, ".agents", "vendor", "axe.min.js")
    try:
        if os.path.exists(cache) and os.path.getsize(cache) > 100_000:
            src = open(cache, encoding="utf-8").read()
        else:
            os.makedirs(os.path.dirname(cache), exist_ok=True)
            src = urllib.request.urlopen(AXE_CDN, timeout=25).read().decode()
            open(cache, "w", encoding="utf-8").write(src)
    except Exception as exc:
        return {"available": False, "reason": f"gagal unduh axe-core: {str(exc)[:60]}"}

    try:
        page.evaluate(src)
        v = page.evaluate(
            """async () => {
              const r = await axe.run(document, {
                runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] },
              });
              return r.violations.map(v => ({
                id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length,
                sample: ((v.nodes[0] && v.nodes[0].html) || '').slice(0, 90),
              }));
            }"""
        )
        return {"available": True, "violations": v}
    except Exception as exc:
        return {"available": False, "reason": str(exc)[:100]}


def slugify(url: str) -> str:
    host = urllib.parse.urlparse(url).netloc.replace("www.", "") or "ref"
    path = urllib.parse.urlparse(url).path.strip("/").replace("/", "-")[:40]
    slug = re.sub(r"[^a-z0-9.-]+", "-", f"{host}-{path}".lower()).strip("-")
    return slug or "ref"


def fmt_list(pairs, suffix=""):
    return ", ".join(f"{k}{suffix} ×{v}" for k, v in pairs)


def type_scale(sizes):
    """Skala tipe + rasio antar-step dari ukuran yang benar-benar dipakai.
    Ukuran yang muncul 1-2 kali biasanya artefak (badge, label kecil), bukan skala."""
    import statistics

    items = [(int(s.replace("px", "")), c) for s, c in sizes]
    all_px = sorted({s for s, _ in items})
    dom = sorted({s for s, c in items if c >= 3}) or all_px
    # Rasio tipe dihitung dari ukuran display/body (>=16px); ukuran <16 = UI micro,
    # kalau dicampur hasilnya 1.0x semua dan menyesatkan.
    display = [s for s in dom if s >= 16] or dom
    ratios = [b / a for a, b in zip(display, display[1:]) if a > 0]
    ratio = round(statistics.median(ratios), 2) if ratios else None
    return all_px, dom, ratio


def write_notes(d, url, out, shots):
    m = d["meta"]
    px, dom, ratio = type_scale(d["sizes"])
    lines = [
        f"# Referensi: {m['title'][:80] or url}",
        f"<{url}>  ·  dibaca {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Ringkasan",
        f"- Viewport dianalisa: {m['width']}px · tinggi halaman {m['height']}px · {m['counted']} elemen terlihat",
        f"- Bahasa: {m['lang'] or '?'} · background body `{m['bodyBg']}`",
        f"- Section terdeteksi: {len(d['sections'])} · CTA: {len(d['ctas'])} · gambar: {len(d['images'])}",
        "",
        "## Tipografi",
        f"- Font: {fmt_list(d['fonts'])}",
        f"- Ukuran dominan: {', '.join(f'{s}px' for s in dom)}" if dom else "- Ukuran: -",
        f"- Semua ukuran: {', '.join(f'{s}px' for s in px)}" if px else "",
        f"- Rasio antar-step: ~{ratio}x" if ratio else "- Rasio: tidak konsisten (acak)",
        f"- Weight: {fmt_list(d['weights'])} · line-height: {fmt_list(d['lineHeights'])}",
        "",
        "## Warna",
        f"- Teks: {fmt_list(d['textColors'])}",
        f"- Permukaan (bg): {fmt_list(d['bgColors'])}",
        f"- Kontras gagal (<4.5:1): {len(d['lowContrast'])}" + (
            " → " + "; ".join(f"\"{c['text']}\" {c['ratio']}:1" for c in d['lowContrast']) if d['lowContrast'] else ""),
        "",
        "## Ritme & bentuk",
        f"- Gap: {fmt_list(d['gaps'])}",
        f"- Padding: {fmt_list(d['pads'])}",
        f"- Radius: {fmt_list(d['radii'])}",
        f"- Shadow: {len(d['shadows'])} varian" if d['shadows'] else "- Shadow: tidak dipakai (border/flat)",
        f"- Container max-width: {fmt_list(d['containers'])}",
        "",
        "## Layout (urut vertikal)",
        "| y | tinggi | bg | isi | grid | heading |",
        "|---|---|---|---|---|---|",
    ]
    for s in d["sections"]:
        kind = []
        if s["hasImage"]:
            kind.append("media")
        if s["hasForm"]:
            kind.append("form")
        if not kind:
            kind.append("teks")
        g = s.get("grid")
        if not g:
            grid_txt = "-"
        elif g["rows"] == 1 and g["cols"] > 6:
            grid_txt = f"baris horizontal {g['cols']} item · {g['cardW']}px"
        else:
            grid_txt = f"{g['cols']} kol × {g['rows']} baris · kartu {g['cardW']}px"
        lines.append(
            f"| {s['y']} | {s['h']} | `{s['bg']}` | {', '.join(kind)} | {grid_txt} | {' / '.join(s['headings'])[:50] or '-'} |"
        )
    lines += ["", "## CTA"]
    for c in d["ctas"][:6]:
        lines.append(
            f"- \"{c['label']}\" · bg `{c['bg']}` · teks `{c['fg']}` · radius {c['radius']} · {c['h']}×{c['w']} · {c['size']}px/{c['weight']}"
        )
    if not d["ctas"]:
        lines.append("- tidak ada tombol dengan latar solid")
    lines += ["", "## Gambar"]
    ratios = sorted({f"{i['ratio']}:1" for i in d["images"]})
    lines.append(f"- {len(d['images'])} gambar · rasio dominan: {', '.join(ratios[:6]) or '-'}")
    if any(i["missingAlt"] for i in d["images"]):
        lines.append(f"- {sum(1 for i in d['images'] if i['missingAlt'])} gambar tanpa alt (cacat a11y — jangan ditiru)")
    lines += ["", "## Aksesibilitas"]
    h = d["headings"]
    order = ", ".join("h" + str(x["level"]) for x in h[:8]) or "-"
    lines.append(f"- Heading: {len(h)} · urutan: {order}")
    if d["smallTargets"]:
        lines.append(f"- Target <24px: {len(d['smallTargets'])} (contoh: \"{d['smallTargets'][0]['text']}\")")

    lines += ["", "## Responsive (diukur di 4 lebar)"]
    for v in d.get("viewports", []):
        flag = "OK" if v["overflowPx"] <= 2 else f"SCROLL HORIZONTAL {v['overflowPx']}px"
        lines.append(f"- {v['w']}px: {flag} · {v['beyond']} elemen keluar layar")

    axe = d.get("axe") or {}
    lines += ["", "## Audit otomatis (axe-core, WCAG 2.1 A/AA)"]
    if axe.get("available"):
        vs = axe.get("violations", [])
        lines.append(f"- {len(vs)} jenis pelanggaran · {sum(v['nodes'] for v in vs)} node")
        for v in vs[:6]:
            lines.append(f"  - [{v['impact']}] {v['id']} ×{v['nodes']} — {v['help'][:70]}")
    else:
        lines.append(f"- tidak bisa dijalankan: {axe.get('reason', '?')}")

    if d.get("durations"):
        lines += ["", "## Motion (terukur)"]
        lines.append(f"- Durasi: {fmt_list(d['durations'])}")
        lines.append(f"- Easing: {fmt_list(d['easings'])}")

    p = d.get("perf")
    if p:
        lines += ["", "## Performa (lab, bukan field)"]
        lines.append(f"- TTFB {p['ttfb']}ms · FCP {p['fcp']}ms · LCP {p['lcp']}ms · CLS {p['cls']}")
        lines.append("- Ambang: LCP ≤2500ms, CLS ≤0.1. Angka lab bisa lebih baik dari pengguna nyata.")

    lines += [
        "",
        "## Prinsip yang bisa dipakai",
        f"- Skala tipe {ratio}x → bangun token dari skala ini, jangan pilih ukuran per komponen."
        if ratio else "- Skala tipe tidak konsisten — justru contoh cara yang salah.",
        f"- Palet: 1 warna aksi dominan + netral; permukaan dominan `{m['bodyBg']}`.",
        "- Ambil grid, density, ritme spacing, dan hierarki. JANGAN copy teks, logo, atau aset.",
        "",
        "## Bukti visual",
    ]
    for name, path in shots.items():
        lines.append(f"- `{path}` ({name})")
    lines.append("")
    open(os.path.join(out, "notes.md"), "w", encoding="utf-8").write("\n".join(lines))


def read_url(url, out, shots_enabled):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright tidak terpasang: python3 -m pip install playwright && playwright install chromium", file=sys.stderr)
        return 3

    shots = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-blink-features=AutomationControlled"])
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900}, device_scale_factor=1,
            user_agent=UA, locale="en-US",
        )
        page = ctx.new_page()
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=45_000)
        except Exception as exc:
            print(f"gagal membuka {url}: {exc}", file=sys.stderr)
            browser.close()
            return 2
        status = resp.status if resp else 0
        page.wait_for_timeout(2500)
        # buang overlay cookie yang menutupi layout
        for sel in ("text=Accept all", "text=Accept", "text=Setuju", "[aria-label*='close' i]"):
            try:
                el = page.locator(sel).first
                if el.is_visible(timeout=400):
                    el.click(timeout=800)
            except Exception:
                pass

        title = page.title()
        data = page.evaluate(EXTRACT_JS)
        try:
            data["perf"] = page.evaluate(PERF_JS)
        except Exception:
            data["perf"] = None
        data["meta"]["status"] = status
        data["meta"]["url"] = url

        if shots_enabled:
            try:
                page.screenshot(path=os.path.join(out, "desktop-hero.png"), animations="disabled")
                page.screenshot(path=os.path.join(out, "desktop.png"), full_page=True, animations="disabled")
                shots["desktop-hero"] = os.path.join(out, "desktop-hero.png")
                shots["desktop"] = os.path.join(out, "desktop.png")
            except Exception as exc:
                print(f"screenshot desktop gagal: {exc}", file=sys.stderr)

            try:
                mctx = browser.new_context(
                    viewport={"width": 390, "height": 844}, device_scale_factor=2,
                    user_agent=UA, locale="en-US", is_mobile=True, has_touch=True,
                )
                mp = mctx.new_page()
                mp.goto(url, wait_until="domcontentloaded", timeout=45_000)
                mp.wait_for_timeout(1800)
                mp.screenshot(path=os.path.join(out, "mobile.png"), full_page=True, animations="disabled")
                shots["mobile"] = os.path.join(out, "mobile.png")
                mctx.close()
            except Exception as exc:
                print(f"screenshot mobile gagal: {exc}", file=sys.stderr)

        # Responsive + a11y diukur setelah screenshot supaya tidak mengubah bidikan.
        data["viewports"] = probe_viewports(page)
        data["axe"] = run_axe(page)
        browser.close()

    data["meta"]["blocked"] = bool(re.search(r"just a moment|attention required|captcha|access denied", title, re.I))
    return data, shots


def read_image(path, out):
    from PIL import Image

    im = Image.open(path).convert("RGB")
    small = im.resize((160, max(1, int(160 * im.height / im.width))))
    quant = small.quantize(colors=8)
    palette = quant.getpalette()[:24]
    counts = sorted(quant.getcolors(), reverse=True)
    colors = [
        {"hex": "#%02x%02x%02x" % tuple(palette[i * 3:i * 3 + 3]), "pixels": n}
        for n, i in counts
    ]
    data = {"meta": {"title": os.path.basename(path), "width": im.width, "height": im.height}, "colors": colors}
    json.dump(data, open(os.path.join(out, "tokens.json"), "w"), indent=2)
    lines = [
        f"# Gambar referensi: {os.path.basename(path)}",
        f"- Dimensi: {im.width}×{im.height} (rasio {round(im.width / im.height, 2)}:1)",
        f"- Warna dominan: {', '.join(c['hex'] for c in colors[:6])}",
        "",
        "Langkah berikut: buka file gambarnya dengan tool Read (multimodal) untuk membaca layout,",
        "hierarki, dan density-nya. Angka di atas hanya pembantu palet.",
        "",
    ]
    open(os.path.join(out, "notes.md"), "w", encoding="utf-8").write("\n".join(lines))
    return data


def tailwind_block(data, url):
    """Terjemahkan hasil ukur jadi @theme Tailwind v4 — titik awal, bukan final."""
    bg = [c for c, _ in (data.get("bgColors") or [])][:3]
    fg = [c for c, _ in (data.get("textColors") or [])][:3]
    font = (data.get("fonts") or [["Inter"]])[0][0]
    _, dom, _r = type_scale(data.get("sizes", []))
    radii = [c for c, _ in (data.get("radii") or []) if c.endswith("px") and c != "0px"][:3]
    gaps = [c for c, _ in (data.get("gaps") or []) if c.endswith("px")][:4]
    lines = [f"/* token awal dari {url} — rapikan nama & buang yang tidak dipakai */", "@theme {"]
    for i, c in enumerate(bg, 1):
        lines.append(f"  --color-bg-{i}: {c}; /* permukaan atau aksen dominan — pisahkan manual */")
    for i, c in enumerate(fg, 1):
        lines.append(f"  --color-text-{i}: {c};")
    lines.append(f"  --font-sans: '{font}', sans-serif;")
    for i, s in enumerate(dom, 1):
        lines.append(f"  --text-{i}: {s}px;")
    for i, r in enumerate(radii, 1):
        lines.append(f"  --radius-{i}: {r};")
    for i, g in enumerate(gaps, 1):
        lines.append(f"  --spacing-{i}: {g};")
    lines.append("}")
    return "\n".join(lines)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        sys.exit("pakai: design-read.py <url|gambar> [--no-shot] [--json]")
    target = args[0]
    is_url = target.startswith(("http://", "https://"))
    if not is_url and not os.path.exists(os.path.expanduser(target)):
        sys.exit(f"bukan URL dan file tidak ada: {target}")

    slug = slugify(target) if is_url else re.sub(r"[^a-z0-9]+", "-", os.path.basename(target).lower())[:40]
    out = os.path.join(REFS, slug)
    os.makedirs(out, exist_ok=True)

    if is_url:
        result = read_url(target, out, "--no-shot" not in flags)
        if isinstance(result, int):
            return result
        data, shots = result
    else:
        data = read_image(os.path.expanduser(target), out)
        shots = {}

    json.dump(data, open(os.path.join(out, "tokens.json"), "w"), indent=2, ensure_ascii=False)
    if is_url:
        write_notes(data, target, out, shots)

    if "--json" in flags:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    if "--tailwind" in flags:
        if is_url:
            print(tailwind_block(data, target))
        else:
            print("mode gambar tidak punya token CSS — pakai URL untuk --tailwind")
        return 0

    m = data["meta"]
    if not is_url:
        print(f"img  {m['title']} · {m['width']}×{m['height']}")
        print(f"warna {', '.join(c['hex'] for c in data['colors'][:6])}")
        print(f"keluar {out.replace(HOME, '~')}/notes.md — buka gambarnya dengan Read untuk baca layout")
        return 0
    px, dom, ratio = type_scale(data.get("sizes", []))
    print(f"ref  {m.get('title', '')[:60] or target}")
    if m.get("blocked"):
        print("WARN halaman menampilkan captcha/blokir — screenshot bisa tidak mewakili")
    print(f"     {m.get('counted', 0)} elemen · {m.get('height', '?')}px · bg {m.get('bodyBg', '-')}")
    if dom:
        joined = ", ".join(str(s) for s in dom)
        print(f"tipe {joined}px · rasio ~{ratio}x" if ratio else f"tipe {joined}px · rasio tidak konsisten")
    if data.get("textColors"):
        print(f"teks {', '.join(c[0] for c in data['textColors'][:4])}")
    if data.get("bgColors"):
        print(f"bg   {', '.join(c[0] for c in data['bgColors'][:4])}")
    if data.get("radii"):
        print(f"radius {', '.join(c[0] for c in data['radii'][:3])}")
    if data.get("sections"):
        grids = [s["grid"] for s in data["sections"] if s.get("grid")]
        print(f"section {len(data['sections'])} · CTA {len(data.get('ctas', []))} · img {len(data.get('images', []))}")
        if grids:
            g = max(grids, key=lambda x: x["count"])
            print(f"grid {g['cols']} kolom × {g['rows']} baris · kartu {g['cardW']}px")
    vps = data.get("viewports") or []
    bad = [v for v in vps if v["overflowPx"] > 2]
    if vps:
        print(f"responsive {len(vps)} lebar · " + ("OK semua" if not bad else
              f"SCROLL di {', '.join(str(v['w']) for v in bad)}px (maks {max(v['overflowPx'] for v in bad)}px)"))
    axe = data.get("axe") or {}
    if axe.get("available"):
        vs = axe["violations"]
        print(f"axe {len(vs)} jenis · {sum(v['nodes'] for v in vs)} node" +
              (f" · teratas {vs[0]['id']}" if vs else ""))
    else:
        print(f"axe tidak jalan: {axe.get('reason', '?')}")
    perf = data.get("perf")
    if perf:
        print(f"perf LCP {perf['lcp']}ms · CLS {perf['cls']} · FCP {perf['fcp']}ms")
    print(f"keluar {out.replace(HOME, '~')}/notes.md")
    for name, path in shots.items():
        print(f"  {name:13s} {path.replace(HOME, '~')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
