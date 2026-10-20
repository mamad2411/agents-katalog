#!/usr/bin/env python3
"""browse.py — AI browsing interaktif via Playwright:
buka URL, screenshot, klik, isi form, baca teks, scroll.
Dipakai AI buat situs JS-berat / login manual / eksplorasi.
"""
import argparse, json, sys

STATE = {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["open", "shot", "text", "click",
                                    "fill", "scroll", "wait", "eval", "close"])
    ap.add_argument("--url")
    ap.add_argument("--out", default="./assets")
    ap.add_argument("--sel", help="CSS selector buat click/fill")
    ap.add_argument("--value", help="nilai buat fill/eval JS")
    ap.add_argument("--file", help="path output shot/text")
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    import os
    os.makedirs(a.out, exist_ok=True)
    pw = sync_playwright().start()
    b = pw.chromium.launch(headless=True)
    pg = b.new_page(user_agent="internet-asset-fetcher/1.0 (AI-agent; local)")
    out = {}
    if a.cmd == "open":
        pg.goto(a.url, wait_until="networkidle", timeout=45000)
        out = {"title": pg.title(), "url": pg.url}
    elif a.cmd == "shot":
        if a.url:
            pg.goto(a.url, wait_until="networkidle", timeout=45000)
        f = a.file or os.path.join(a.out, "shot.png")
        pg.screenshot(path=f, full_page=True)
        out = {"shot": f}
    elif a.cmd == "text":
        if a.url:
            pg.goto(a.url, wait_until="networkidle", timeout=45000)
        t = pg.evaluate("() => document.body ? document.body.innerText : ''")
        f = a.file or os.path.join(a.out, "page.txt")
        open(f, "w").write(t)
        out = {"chars": len(t), "file": f, "preview": t[:800]}
    elif a.cmd == "click":
        pg.goto(a.url, wait_until="networkidle", timeout=45000)
        pg.click(a.sel, timeout=15000)
        pg.wait_for_timeout(2000)
        out = {"clicked": a.sel, "url_now": pg.url, "title": pg.title()}
    elif a.cmd == "fill":
        pg.goto(a.url, wait_until="networkidle", timeout=45000)
        pg.fill(a.sel, a.value or "", timeout=15000)
        out = {"filled": a.sel}
    elif a.cmd == "scroll":
        if a.url:
            pg.goto(a.url, wait_until="networkidle", timeout=45000)
        n = int(a.value or "3")
        for _ in range(n):
            pg.mouse.wheel(0, 2000)
            pg.wait_for_timeout(1000)
        t = pg.evaluate("() => document.body.innerText")
        out = {"chars_after_scroll": len(t)}
    elif a.cmd == "wait":
        pg.goto(a.url, wait_until="networkidle", timeout=45000)
        pg.wait_for_selector(a.sel, timeout=int(a.value or "15000"))
        out = {"appeared": a.sel}
    elif a.cmd == "eval":
        pg.goto(a.url, wait_until="networkidle", timeout=45000)
        out = {"result": str(pg.evaluate(a.value or "document.title"))[:2000]}
    elif a.cmd == "close":
        out = {"closed": True}
    b.close()
    pw.stop()
    print(json.dumps(out, indent=1)[:3000])


if __name__ == "__main__":
    main()
