#!/usr/bin/env python3
"""cline-guard.py — penjaga konteks untuk Cline (CLI/VSCode), dipasang di hook
UserPromptSubmit (~/.cline/hooks/UserPromptSubmit.py).

Khusus Cline, pemboros terbesar bukan tool call: gambar yang ditempel user
tersimpan base64 di messages.json dan DIKIRIM ULANG tiap request. Ukuran nyata
di mesin ini: 1 sesi = 50 gambar = 22 MB base64 = ±5,5 juta token.

Output: 0 baris kalau sesi sehat (hemat token), 1 baris peringatan kalau lewat
ambang. Ambang: pesan >200, file >10 MB, atau base64 gambar >2 MB.
Setting: CLINE_GUARD_MSGS, CLINE_GUARD_MB, CLINE_GUARD_IMG_MB.
"""
import glob
import json
import os
import sys

SESS = os.path.expanduser("~/.cline/data/sessions")
MAX_MSGS = int(os.environ.get("CLINE_GUARD_MSGS", "200"))
MAX_MB = float(os.environ.get("CLINE_GUARD_MB", "10"))
MAX_IMG_MB = float(os.environ.get("CLINE_GUARD_IMG_MB", "2"))


def current_session():
    """messages.json paling baru diubah = sesi yang sedang jalan."""
    files = glob.glob(os.path.join(SESS, "*", "*.messages.json"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def measure(path):
    size_mb = os.path.getsize(path) / 2**20
    if size_mb > 25:  # file sudah jelas lewat ambang: jangan parse (biarkan hook tetap cepat)
        return -1, size_mb, 0, 0
    d = json.load(open(path, encoding="utf-8"))
    msgs = d.get("messages", [])
    n = len(msgs)
    base64_chars = 0
    n_img = 0
    for m in msgs:
        for c in (m.get("content") or []):
            if not isinstance(c, dict):
                continue
            for k in ("data", "image", "base64", "source"):
                v = c.get(k)
                if isinstance(v, str) and len(v) > 4096:
                    base64_chars += len(v)
                elif isinstance(v, dict) and isinstance(v.get("data"), str):
                    base64_chars += len(v["data"])
            if c.get("type") in ("image", "image_url") or ("data" in c and len(str(c.get("data"))) > 4096):
                n_img += 1
    return n, size_mb, base64_chars / 4, n_img


def warn():
    """Kembalikan string peringatan (bisa kosong). Tidak pernah raise."""
    try:
        p = current_session()
        if not p:
            return ""
        n, mb, img_tok, n_img = measure(p)
    except Exception:
        return ""
    bad = []
    if n < 0:
        bad.append("%.0f MB (terlalu besar untuk diperiksa)" % mb)
    else:
        if n > MAX_MSGS:
            bad.append("%d pesan" % n)
        if mb > MAX_MB:
            bad.append("%.0f MB" % mb)
        if img_tok / 2**20 > MAX_IMG_MB:
            bad.append("%d gambar ≈ %.1f jt token" % (n_img, img_tok / 1e6))
    if not bad:
        return ""
    return ("[context-guard] Sesi Cline ini: %s. Riwayat dikirim ulang tiap request "
            "— dan gambar yang sudah lewat dipakai tetap ikut terkirim selamanya. "
            "Tutup sesi sekarang (mulai sesi baru per tugas). Ke depan: jangan tempel "
            "gambar di sesi panjang; simpan gambar ke file lalu rujuk path-nya." % ", ".join(bad))


def main():
    sys.stdout.write(warn())
    return 0


if __name__ == "__main__":
    sys.exit(main())
