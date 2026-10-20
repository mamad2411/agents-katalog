#!/usr/bin/env python3
"""media.py — audio/video via ffmpeg: download + thumbnail + info.
Untuk stream (yt/dll) butuh yt-dlp; kalau tidak ada, beri pesan jelas.
"""
import argparse, json, os, shutil, subprocess, sys


def run(*args):
    r = subprocess.run(list(args), capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout, r.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", default="./assets")
    ap.add_argument("--thumb", action="store_true", help="buat thumbnail jpg")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if not shutil.which("ffmpeg"):
        sys.exit("butuh ffmpeg: brew install ffmpeg")
    # stream site? delegasi yt-dlp
    if any(d in a.url for d in ("youtube.com", "youtu.be", "tiktok.com",
                                "instagram.com", "twitter.com", "x.com")):
        if not shutil.which("yt-dlp"):
            sys.exit("stream site butuh yt-dlp: brew install yt-dlp")
        code, out, err = run("yt-dlp", "--no-playlist", "-o",
                             os.path.join(a.out, "%(title).50s-%(id)s.%(ext)s"),
                             a.url)
        print(out[-500:] if out else err[-500:])
        sys.exit(code)
    # file langsung
    from pathlib import Path
    sys.path.insert(0, os.path.dirname(__file__))
    import fetch
    ok = fetch.one(a.url, a.out)
    if ok and a.thumb:
        man = json.load(open(os.path.join(a.out, "manifest.json")))
        last = [m for m in man if m.get("url") == a.url and m.get("path")][-1]
        src = last["path"]
        th = os.path.splitext(src)[0] + "-thumb.jpg"
        code, _, err = run("ffmpeg", "-y", "-i", src, "-vframes", "1",
                           "-q:v", "3", th)
        print("thumb:", th if code == 0 else err[-200:])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
