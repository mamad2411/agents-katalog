#!/usr/bin/env python3
"""framer_ref.py — ambil referensi UI/UX dari site Framer (dan site apa pun).

Pemakaian:
  framer-ref.sh <url>                 # analisa 1 site -> refs/<slug>/
  framer-ref.sh --gallery [kategori]  # daftar site Framer bagus (portfolio/saas/...)
  framer-ref.sh <url> --no-shot       # tanpa screenshot (cepat, token saja)

Output ke ~/.agents/refs/<slug>/:
  page.html      HTML mentah
  tokens.json    palet, tipografi, radius, shadow, gradient, spacing
  notes.md       ringkasan siap baca AI (layout, hierarki, CTA, palet)
  desktop.png    screenshot full-page 1440px
  desktop-hero.png  viewport atas saja (paling penting buat AI)
  mobile.png     screenshot full-page 390px

Exit: 0 sukses, 1 argumen salah, 2 gagal ambil halaman.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HOME = os.path.expanduser("~")
REFS = os.path.join(HOME, ".agents", "refs")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
GALLERY = "https://www.framer.com/community/gallery/"
MAX_PAGE_HTML = 60_000_000

EXTRACT_JS = r"""
() => {
  const freq = (o, k) => { if (!k) return; o[k] = (o[k] || 0) + 1 };
  const fonts = {}, colors = {}, sizes = {}, weights = {}, radii = {},
        shadows = {}, gradients = {}, lineHeights = {}, letters = {};
  const els = [...document.querySelectorAll('body *')];
  let visible = 0;

  for (const el of els) {
    const r = el.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (parseFloat(cs.opacity) === 0) continue;
    visible++;

    const txt = (el.textContent || '').trim();
    if (txt && el.children.length === 0) {
      freq(fonts, cs.fontFamily);
      freq(sizes, Math.round(parseFloat(cs.fontSize)) + 'px');
      freq(weights, cs.fontWeight);
      freq(colors, cs.color);
      freq(lineHeights, cs.lineHeight);
      freq(letters, cs.letterSpacing);
    }
    const bg = cs.backgroundColor;
    if (bg && bg !== 'rgba(0, 0, 0, 0)') freq(colors, bg);
    if (cs.borderRadius && cs.borderRadius !== '0px') {
      freq(radii, cs.borderRadius.split(' / ')[0]);
    }
    if (cs.boxShadow && cs.boxShadow !== 'none') freq(shadows, cs.boxShadow);
    const bi = cs.backgroundImage;
    if (bi && bi !== 'none' && gradients && Object.keys(gradients).length < 60) {
      freq(gradients, bi.slice(0, 90));
    }
  }

  // CSS custom properties (design token asli dari Framer)
  const vars = {};
  let seen = 0;
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules } catch (e) { continue }
    if (!rules) continue;
    for (const rule of rules) {
      if (!rule.style) continue;
      for (const p of rule.style) {
        if (p.startsWith('--')) {
          vars[p] = rule.style.getPropertyValue(p).trim().slice(0, 120);
          if (++seen > 300) break;
        }
      }
      if (seen > 300) break;
    }
    if (seen > 300) break;
  }

  const top = (o, n) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n)
                       .map(([k, v]) => ({ value: k, count: v }));

  const txt = s => (s || '').replace(/\s+/g, ' ').trim().slice(0, 160);
  const headings = [...document.querySelectorAll('h1,h2,h3')]
    .filter(e => e.getBoundingClientRect().height > 0)
    .slice(0, 30)
    .map(e => ({ tag: e.tagName.toLowerCase(), text: txt(e.textContent),
                 size: getComputedStyle(e).fontSize, weight: getComputedStyle(e).fontWeight }));

  const nav = [...document.querySelectorAll('nav a, header a')]
    .slice(0, 20).map(a => txt(a.textContent)).filter(Boolean);

  const ctas = [...document.querySelectorAll('a,button')]
    .filter(e => e.getBoundingClientRect().height > 0)
    .map(e => ({ text: txt(e.textContent),
                 bg: getComputedStyle(e).backgroundColor,
                 color: getComputedStyle(e).color,
                 radius: getComputedStyle(e).borderRadius }))
    .filter(c => c.text && c.text.length < 40 && c.bg !== 'rgba(0, 0, 0, 0)')
    .slice(0, 15);

  return {
    title: document.title,
    description: (document.querySelector('meta[name=description]') || {}).content || '',
    viewport: { w: innerWidth, h: innerHeight, pageH: document.body.scrollHeight },
    sections: document.querySelectorAll('section').length,
    visibleElements: visible,
    fonts: top(fonts, 6), sizes: top(sizes, 14), weights: top(weights, 5),
    colors: top(colors, 14), radii: top(radii, 8), shadows: top(shadows, 5),
    gradients: top(gradients, 5), lineHeights: top(lineHeights, 5),
    letters: top(letters, 5), cssVars: vars,
    headings, nav, ctas,
    images: [...document.images].slice(0, 12).map(i => ({
      src: (i.currentSrc || i.src || '').slice(0, 200),
      w: i.naturalWidth, h: i.naturalHeight, alt: txt(i.alt)
    })),
  };
}
"""


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html,application/xhtml+xml"})
    with urllib.request.urlopen(req, timeout=40) as r:
        raw = r.read(MAX_PAGE_HTML)
    return raw.decode("utf-8", "replace")


def slugify(url: str) -> str:
    p = urllib.parse.urlparse(url)
    base = (p.netloc + p.path).strip("/").replace("/", "-").replace(".", "-")
    base = re.sub(r"[^a-zA-Z0-9-]+", "-", base).strip("-").lower()
    return (base or "ref")[:60]


def hexify(css_color: str) -> str:
    m = re.match(r"rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?", css_color)
    if not m:
        return css_color
    r, g, b = (int(float(m.group(i))) for i in (1, 2, 3))
    a = float(m.group(4)) if m.group(4) else 1.0
    hx = f"#{r:02x}{g:02x}{b:02x}"
    return hx if a >= 0.99 else f"{hx} ({a:.2f} alpha)"


def luminance(hx: str) -> float:
    hx = hx.lstrip("#")[:6]
    if len(hx) != 6:
        return 0.5
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def analyze(url: str, no_shot: bool = False) -> int:
    os.makedirs(REFS, exist_ok=True)
    slug = slugify(url)
    out = os.path.join(REFS, slug)
    os.makedirs(out, exist_ok=True)

    try:
        html = fetch(url)
    except Exception as e:
        print(f"GAGAL ambil {url}: {e}", file=sys.stderr)
        return 2
    with open(os.path.join(out, "page.html"), "w", encoding="utf-8") as f:
        f.write(html)

    data = {}
    shots = []
    if not no_shot:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch()
                for name, vp, scale in (("desktop", {"width": 1440, "height": 900}, 1),
                                        ("mobile", {"width": 390, "height": 844}, 2)):
                    ctx = browser.new_context(viewport=vp, device_scale_factor=scale,
                                              user_agent=UA)
                    page = ctx.new_page()
                    page.goto(url, wait_until="domcontentloaded", timeout=45_000)
                    try:
                        page.wait_for_load_state("networkidle", timeout=8_000)
                    except Exception:
                        pass
                    # trigger lazy-load
                    page.evaluate("""async () => {
                        await new Promise(r => {
                          let y = 0;
                          const t = setInterval(() => {
                            y += innerHeight; scrollTo(0, y);
                            if (y > document.body.scrollHeight || y > 30000) {
                              clearInterval(t); scrollTo(0, 0); r();
                            }
                          }, 120);
                        });
                        await new Promise(r => setTimeout(r, 900));
                    }""")
                    path = os.path.join(out, f"{name}.png")
                    page.screenshot(path=path, full_page=True)
                    shots.append(path)
                    if name == "desktop":
                        hero = os.path.join(out, "desktop-hero.png")
                        page.screenshot(path=hero)
                        shots.append(hero)
                        data = page.evaluate(EXTRACT_JS)
                    ctx.close()
                browser.close()
        except Exception as e:
            print(f"PERINGATAN screenshot gagal ({e}); lanjut token dari HTML", file=sys.stderr)

    if not data:
        data = {"title": (re.search(r"<title[^>]*>(.*?)</title>", html, re.S) or ["", ""])[1].strip(),
                "visibleElements": 0,
                "fonts": [], "sizes": [], "colors": [], "radii": [], "shadows": [],
                "gradients": [], "weights": [], "lineHeights": [], "letters": [],
                "cssVars": {}, "headings": [], "nav": [], "ctas": [], "images": [],
                "sections": html.count("<section"), "viewport": {}, "description": ""}

    data["url"] = url
    data["slug"] = slug
    data["screenshots"] = shots
    data["fetchedAt"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    data["pageBytes"] = len(html)
    with open(os.path.join(out, "tokens.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)

    notes = render_notes(data, out)
    with open(os.path.join(out, "notes.md"), "w", encoding="utf-8") as f:
        f.write(notes)
    print(f"OK {url}\n-> {out}")
    print(json.dumps({"slug": slug, "dir": out, "sections": data.get("sections"),
                      "elements": data.get("visibleElements"),
                      "shots": [os.path.basename(s) for s in shots]}, ensure_ascii=False))
    return 0


def render_notes(d: dict, out: str) -> str:
    L = [f"# Referensi UI — {d.get('title') or d['url']}", "",
         f"- URL: {d['url']}", f"- Diambil: {d.get('fetchedAt')}",
         f"- Section: {d.get('sections')} · Elemen terlihat: {d.get('visibleElements')}",
         f"- Viewport: {d.get('viewport')}", ""]

    if d.get("description"):
        L += [f"> {d['description']}", ""]

    L += ["## Palet (urut pemakaian)", ""]
    for c in d.get("colors", [])[:12]:
        hx = hexify(c["value"])
        lum = luminance(hx) if hx.startswith("#") else 0.5
        role = "background/gelap" if lum < 0.25 else ("background/terang" if lum > 0.85 else "aksen/teks")
        L.append(f"- `{hx}` ×{c['count']} — {role}")
    L.append("")

    L += ["## Tipografi", ""]
    for f in d.get("fonts", [])[:4]:
        L.append(f"- family: `{f['value']}` ({f['count']} elemen)")
    if d.get("sizes"):
        L.append(f"- skala ukuran: {', '.join(s['value'] for s in d['sizes'][:12])}")
    if d.get("weights"):
        L.append(f"- weight: {', '.join(w['value'] for w in d['weights'])}")
    if d.get("lineHeights"):
        L.append(f"- line-height: {', '.join(x['value'] for x in d['lineHeights'])}")
    if d.get("letters"):
        L.append(f"- letter-spacing: {', '.join(x['value'] for x in d['letters'])}")
    L.append("")

    if d.get("radii"):
        L += ["## Radius", ""] + [f"- {r['value']} ×{r['count']}" for r in d["radii"]] + [""]
    if d.get("shadows"):
        L += ["## Shadow", ""] + [f"- `{s['value'][:70]}`" for s in d["shadows"]] + [""]
    if d.get("gradients"):
        L += ["## Gradient", ""] + [f"- `{g['value'][:90]}`" for g in d["gradients"]] + [""]

    if d.get("headings"):
        L += ["## Hierarki heading (struktur halaman)", ""]
        for h in d["headings"]:
            pad = "  " * (int(h["tag"][1]) - 1)
            L.append(f"{pad}- {h['tag'].upper()} {h['size']}/{h['weight']} — {h['text']}")
        L.append("")

    if d.get("nav"):
        L += ["## Navigasi", ""] + [f"- {n}" for n in d["nav"]] + [""]
    if d.get("ctas"):
        L += ["## CTA / tombol (bg, warna teks, radius)", ""]
        for c in d["ctas"]:
            L.append(f"- {c['text']} · bg `{hexify(c['bg'])}` · teks `{hexify(c['color'])}` · r {c['radius']}")
        L.append("")

    if d.get("cssVars"):
        L += ["## CSS variables asli (token Framer)", ""]
        for k, v in list(d["cssVars"].items())[:30]:
            L.append(f"- `{k}: {v}`")
        L.append("")

    if d.get("images"):
        L += ["## Aset gambar", ""]
        for i in d["images"][:8]:
            L.append(f"- {i['w']}×{i['h']} {i['src']}")
        L.append("")

    L += ["## File", "",
          f"- `{out}/desktop.png` (full page 1440)",
          f"- `{out}/desktop-hero.png` (viewport atas — wajib dilihat AI)",
          f"- `{out}/mobile.png` (full page 390)",
          f"- `{out}/tokens.json` (data mentah)", "",
          "## Cara pakai oleh AI", "",
          "1. Lihat `desktop-hero.png` dulu (layout, hierarki, density).",
          "2. Cocokkan dengan palet + skala tipografi di atas.",
          "3. Tiru **prinsip** (grid, spacing, kontras, radius), bukan copy teks/brand.",
          "4. Cek `mobile.png` untuk perilaku responsif.", ""]
    return "\n".join(L)


def gallery(kategori: str = "", n: int = 12) -> int:
    url = GALLERY + (f"categories/{kategori}/" if kategori else "")
    try:
        html = fetch(url)
    except Exception as e:
        print(f"GAGAL ambil gallery {url}: {e}", file=sys.stderr)
        return 2
    slugs = []
    for m in re.finditer(r'/community/gallery/([a-z0-9][a-z0-9._-]*)/', html):
        s = m.group(1)
        if s not in ("categories",) and s not in slugs:
            slugs.append(s)
    show = slugs[:n]
    print(f"# Gallery Framer{' / ' + kategori if kategori else ''} — {len(show)} dari {len(slugs)}\n")
    for s in show:
        entry = f"https://www.framer.com/community/gallery/{s}/"
        live = ""
        try:
            h = fetch(entry)
            m = re.search(r'<a[^>]+href="(https?://(?!www\.framer\.com|framer\.com)[^"]+)"[^>]*>\s*'
                          r'(?:<[^>]+>\s*)*Visit Site', h)
            if m:
                live = m.group(1)
        except Exception:
            pass
        print(f"- {s}\n  gallery: {entry}" + (f"\n  live: {live}" if live else ""))
    print("\nAnalisa: `framer-ref.sh <live-url>`")
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:]]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 1
    no_shot = "--no-shot" in args
    args = [a for a in args if not a.startswith("--")]
    if sys.argv[1] == "--gallery" or (args and args[0] == "gallery"):
        rest = [a for a in args if a not in ("--gallery", "gallery")]
        return gallery(rest[0] if rest else "")
    url = args[0]
    if not url.startswith("http"):
        url = "https://" + url
    return analyze(url, no_shot)


if __name__ == "__main__":
    sys.exit(main())
