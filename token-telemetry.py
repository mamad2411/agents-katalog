#!/usr/bin/env python3
"""token-telemetry.py — ukur pemborosan token per sesi (semua AI tool).

Pakai:  python3 token-telemetry.py [--top 15]

Scan transcript sesi, estimasi token (bytes/4), tandai pemboros:
  * sesi raksasa (riwayat dikirim ulang tiap request)
  * gambar/base64 di riwayat (menempel permanen)
  * file besar yang dibaca penuh
Tujuan: AI/user tahu di mana token bocor, lalu hindari (bukan tebak-tebakan).
"""
import glob, json, os, sys
from pathlib import Path

HOME = Path.home()
DIRS = [
    str(HOME / ".codebuddy" / "projects" / "*" / "sessions" / "*.jsonl"),
    str(HOME / ".claude" / "projects" / "*" / "*.jsonl"),
    str(HOME / ".cursor" / "chats" / "*"),
    str(HOME / ".gemini" / "tmp" / "*"),
]
IMG = ("data:image", "iVBORw0KGgo", "/9j/4AAQ", "base64,")


def scan(path):
    try:
        sz = os.path.getsize(path)
    except OSError:
        return None
    imgs = 0
    try:
        with open(path, "rb") as f:
            data = f.read()
        low = data.lower()
        for m in IMG:
            imgs += low.count(m.encode())
    except Exception:
        data = b""
    return {"path": path, "mb": sz / 1048576, "tok": sz // 4, "imgs": imgs}


def main():
    top = 15
    if "--top" in sys.argv:
        try:
            top = int(sys.argv[sys.argv.index("--top") + 1])
        except Exception:
            pass
    files = []
    for pat in DIRS:
        files += glob.glob(pat)
    rows = [r for r in (scan(p) for p in files) if r]
    rows.sort(key=lambda r: -r["tok"])
    tot_tok = sum(r["tok"] for r in rows)
    tot_img = sum(r["imgs"] for r in rows)
    print("SESI: %d file | ~%s token total | %d blob gambar"
          % (len(rows), f"{tot_tok:,}", tot_img))
    print("(catatan: riwayat dikirim ulang TIAP request → sesi besar = biaya berulang)")
    print("-" * 62)
    for r in rows[:top]:
        flag = ""
        if r["mb"] > 10:
            flag += " ⚠BESAR"
        if r["imgs"]:
            flag += " 🖼%d" % r["imgs"]
        print("%6.1f MB  ~%8s tok  %s%s"
              % (r["mb"], f"{r['tok']:,}", Path(r["path"]).name[:34], flag))
    big = [r for r in rows if r["mb"] > 10]
    if big:
        print("-" * 62)
        print("Saran: %d sesi >10MB — tutup (/clear), jangan --resume." % len(big))
    if tot_img:
        print("Saran: %d gambar di riwayat — simpan ke file, rujuk path, tutup sesi." % tot_img)


if __name__ == "__main__":
    main()
