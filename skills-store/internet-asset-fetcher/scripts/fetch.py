#!/usr/bin/env python3
"""fetch.py — entry utama internet-asset-fetcher.
Auto-deteksi tipe dari extension + Content-Type, download via curl,
catat manifest.json. Idempotent: file sama (sha256) tidak diunduh ulang.
"""
import argparse, datetime, hashlib, json, mimetypes, os, re, subprocess, sys, time, urllib.parse

UA = "internet-asset-fetcher/1.0 (AI-agent; local)"
EXT_MAP = {".jpg": ".jpg", ".jpeg": ".jpg", ".png": ".png", ".gif": ".gif",
           ".webp": ".webp", ".svg": ".svg", ".avif": ".avif", ".bmp": ".bmp",
           ".ico": ".ico", ".pdf": ".pdf", ".doc": ".doc", ".docx": ".docx",
           ".xls": ".xls", ".xlsx": ".xlsx", ".ppt": ".ppt", ".pptx": ".pptx",
           ".csv": ".csv", ".txt": ".txt", ".md": ".md", ".json": ".json",
           ".mp3": ".mp3", ".wav": ".wav", ".ogg": ".ogg", ".m4a": ".m4a",
           ".mp4": ".mp4", ".webm": ".webm", ".mov": ".mov"}
CT_MAP = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
          "image/webp": ".webp", "image/svg+xml": ".svg",
          "application/pdf": ".pdf", "text/html": ".html", "text/plain": ".txt",
          "text/markdown": ".md", "application/json": ".json",
          "audio/mpeg": ".mp3", "video/mp4": ".mp4"}


def slug(url):
    p = urllib.parse.urlparse(url).path.rstrip("/") or "index"
    base = re.sub(r"[^a-z0-9]+", "-", p.split("/")[-1].lower()).strip("-")[:50] or "asset"
    h = hashlib.md5(url.encode()).hexdigest()[:6]
    return f"{base}-{h}"


def head_ctype(url):
    try:
        r = subprocess.run(["curl", "-sIL", "-A", UA, "--max-time", "20", "-o", "/dev/null",
                            "-w", "%{content_type}", url], capture_output=True, text=True, timeout=30)
        return (r.stdout or "").split(";")[0].strip().lower()
    except Exception:
        return ""


def download(url, dest):
    r = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "120", "--retry", "2",
                        "-o", dest, "-w", "%{http_code}", url],
                       capture_output=True, text=True, timeout=150)
    return r.stdout.strip()


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def one(url, outdir):
    os.makedirs(outdir, exist_ok=True)
    man_p = os.path.join(outdir, "manifest.json")
    man = json.load(open(man_p)) if os.path.exists(man_p) else []
    if any(m.get("url") == url and os.path.exists(m.get("path", "")) for m in man):
        print(f"SKIP (sudah ada): {url}")
        return True
    path_part = urllib.parse.urlparse(url).path
    ext = os.path.splitext(path_part)[1].lower()
    if ext not in EXT_MAP:
        ct = head_ctype(url)
        ext = CT_MAP.get(ct, "")
        if ct.startswith("text/html"):
            print(f"PAGE (bukan file): {url} -> pakai scripts/page.py")
            man.append({"url": url, "type": "page", "hint": "use page.py",
                        "at": datetime.datetime.now(datetime.timezone.utc).isoformat()})
            json.dump(man, open(man_p, "w"), indent=1)
            return False
    if not ext:
        ext = ".bin"
    dest = os.path.join(outdir, slug(url) + ext)
    code = download(url, dest)
    if code != "200" or not os.path.exists(dest) or os.path.getsize(dest) == 0:
        if os.path.exists(dest):
            os.remove(dest)
        print(f"GAGAL http={code}: {url}")
        man.append({"url": url, "error": f"http_{code}",
                    "at": datetime.datetime.now(datetime.timezone.utc).isoformat()})
        json.dump(man, open(man_p, "w"), indent=1)
        return False
    entry = {"url": url, "path": dest, "bytes": os.path.getsize(dest),
             "sha256": sha256(dest), "ext": ext,
             "at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    man.append(entry)
    json.dump(man, open(man_p, "w"), indent=1)
    print(f"OK {dest} ({entry['bytes']}B)")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url")
    ap.add_argument("--list")
    ap.add_argument("--out", default="./assets")
    ap.add_argument("--page", action="store_true",
                    help="paksa via page.py (Playwright)")
    ap.add_argument("--sleep", type=float, default=1.0)
    a = ap.parse_args()
    if a.page and a.url:
        sys.exit(subprocess.call(
            [sys.executable, os.path.join(os.path.dirname(__file__), "page.py"),
             "--url", a.url, "--out", a.out]))
    urls = []
    if a.url:
        urls = [a.url]
    elif a.list:
        urls = [l.strip() for l in open(a.list) if l.strip() and not l.startswith("#")]
    else:
        ap.error("butuh --url atau --list")
    ok = 0
    for i, u in enumerate(urls):
        if i:
            time.sleep(a.sleep)
        ok += one(u, a.out)
    print(f"selesai: {ok}/{len(urls)} berhasil -> {a.out}/manifest.json")


if __name__ == "__main__":
    main()
