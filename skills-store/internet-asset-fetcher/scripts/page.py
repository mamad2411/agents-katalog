#!/usr/bin/env python3
"""page.py — halaman web -> markdown + teks + screenshot.
Coba Playwright dulu (JS-rendered), fallback curl + strip-tags.
"""
import argparse, datetime, hashlib, json, os, re, subprocess, sys, urllib.parse


def slug(url):
    h = hashlib.md5(url.encode()).hexdigest()[:6]
    host = urllib.parse.urlparse(url).netloc.replace(".", "-")[:30]
    return f"page-{host}-{h}"


def via_playwright(url, outdir, base):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        pg = b.new_page(user_agent="internet-asset-fetcher/1.0 (AI-agent; local)")
        pg.goto(url, wait_until="networkidle", timeout=45000)
        pg.wait_for_timeout(1500)
        html = pg.content()
        text = pg.evaluate("() => document.body ? document.body.innerText : ''")
        md = pg.evaluate("""() => { const t=[]; document.querySelectorAll(
          'h1,h2,h3,p,li,a,pre,code,blockquote').forEach(e=>{ const v=e.innerText.trim();
          if(v) t.push((/^H[1-3]$/.test(e.tagName)?'#'.repeat(+e.tagName[1])+' ':'- ')+v);});
          return t.join('\\n\\n'); }""")
        shot = os.path.join(outdir, base + ".png")
        pg.screenshot(path=shot, full_page=True)
        b.close()
        return html, text, md, shot


def via_curl(url):
    r = subprocess.run(["curl", "-sL", "-A", "internet-asset-fetcher/1.0",
                        "--max-time", "60", url],
                       capture_output=True, text=True, timeout=75)
    html = r.stdout or ""
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=S | I)
    text = re.sub(r"<[^>]+>", " ", text)
    return html, re.sub(r"\s+", " ", text).strip(), "", ""


from re import S, I  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", default="./assets")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    base = slug(a.url)
    got = None
    try:
        got = via_playwright(a.url, a.out, base)
    except Exception as e:
        print(f"playwright gagal ({str(e)[:80]}), fallback curl...")
    if got is None:
        html, text, md, shot = via_curl(a.url)
    else:
        html, text, md, shot = got
    open(os.path.join(a.out, base + ".html"), "w").write(html)
    open(os.path.join(a.out, base + ".txt"), "w").write(text)
    if md:
        open(os.path.join(a.out, base + ".md"), "w").write(md)
    man_p = os.path.join(a.out, "manifest.json")
    man = json.load(open(man_p)) if os.path.exists(man_p) else []
    man.append({"url": a.url, "path": os.path.join(a.out, base + ".txt"),
                "html": base + ".html", "markdown": base + ".md" if md else None,
                "screenshot": shot or None, "chars": len(text),
                "at": datetime.datetime.now(datetime.timezone.utc).isoformat()})
    json.dump(man, open(man_p, "w"), indent=1)
    print(f"OK {base} ({len(text)} chars teks)" + (f" + {shot}" if shot else ""))


if __name__ == "__main__":
    main()
