#!/usr/bin/env python3
"""context-guard.py — penjaga konteks sesi (hook Claude Code / CLI).

Masalah nyata yang diperbaiki (audit 2026-09-26): sesi tidak pernah di-clear
sampai konteks ±500.000 token/pesan (3 sesi @ 59/54/18 MB jsonl) → 4,42 M token
terbakar. Hook ini mencegah pengulangan itu dengan biaya ±0 token.

Dipakai sebagai hook `SessionStart` + `UserPromptSubmit` (stdin = JSON hook),
atau manual:  python3 ~/.agents/context-guard.py --report

Keluaran sengaja 1 baris pendek supaya TIDAK menambah konteks:
  - di bawah ambang  → cetak TIDAK ADA apa-apa (0 token)
  - > WARN_MB        → 1 baris peringatan (maks sekali per kenaikan 5 MB)
  - > URGENT_MB      → 1 baris instruksi tegas /clear

Tidak menulis apa pun ke repo; state kecil di /tmp (hapus sendiri kalau sesi
berakhir). Aman dijalankan berulang (idempoten).
"""
import json
import os
import sys

WARN_MB = float(os.environ.get("CONTEXT_WARN_MB", "10"))
URGENT_MB = float(os.environ.get("CONTEXT_URGENT_MB", "25"))
STEP_MB = float(os.environ.get("CONTEXT_STEP_MB", "5"))  # jeda minimal antar-peringatan
STATE_DIR = os.environ.get("CONTEXT_GUARD_DIR", "/tmp/voralens-context-guard")


def human(n):
    if n >= 1 << 30:
        return "%.1f GB" % (n / float(1 << 30))
    if n >= 1 << 20:
        return "%.1f MB" % (n / float(1 << 20))
    if n >= 1 << 10:
        return "%.0f KB" % (n / float(1 << 10))
    return "%d B" % n


def session_key(payload):
    """Kunci sesi dari JSON hook; fallback ke transcript_path; fallback 'default'."""
    sid = payload.get("session_id") or ""
    if sid:
        return str(sid)
    tp = payload.get("transcript_path") or ""
    if tp:
        return os.path.basename(tp).replace(".jsonl", "") or "default"
    return "default"


def state_path(key):
    return os.path.join(STATE_DIR, "lastwarn-" + "".join(c for c in key if c.isalnum() or c in "-_")[:64])


def read_last(key):
    try:
        with open(state_path(key)) as f:
            return float(f.read().strip() or 0)
    except Exception:
        return 0.0


def write_last(key, mb):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        tmp = state_path(key) + ".tmp%d" % os.getpid()
        with open(tmp, "w") as f:
            f.write("%.1f" % mb)
        os.replace(tmp, state_path(key))
    except Exception:
        pass  # state gagal ditulis: lebih baik tidak pernah memblokir sesi


def check(transcript_path, key):
    if not transcript_path or not os.path.isfile(transcript_path):
        return ""
    size = os.path.getsize(transcript_path)
    mb = size / float(1 << 20)
    if mb < WARN_MB:
        return ""
    last = read_last(key)
    if mb - last < STEP_MB:
        return ""  # sudah diperingatkan di level ini, jangan ulang tiap prompt
    write_last(key, mb)
    if mb >= URGENT_MB:
        return ("KONTEKS KITIS: %s (%s) — SELESAIKAN langkah ini lalu /clear; "
                "jangan lanjut tugas baru di sesi ini." % (human(size), transcript_path))
    return ("Konteks %s — pertimbangkan /clear di batas tugas berikutnya "
            "(sesi >10 MB = tiap pesan baca ±0,5 jt token)." % human(size))


def report():
    """--report: daftar sesi terbesar + kelompokkan (read-only, untuk manusia)."""
    base = os.path.expanduser("~/.claude/projects")
    rows = []
    if os.path.isdir(base):
        for proj in os.listdir(base):
            pdir = os.path.join(base, proj)
            if not os.path.isdir(pdir):
                continue
            for fn in os.listdir(pdir):
                if not fn.endswith(".jsonl"):
                    continue
                p = os.path.join(pdir, fn)
                try:
                    rows.append((os.path.getsize(p), proj, fn))
                except OSError:
                    continue
    rows.sort(reverse=True)
    warn = sum(1 for s, _, _ in rows if s / float(1 << 20) >= WARN_MB)
    print("ambang: WARN %.0f MB · URGENT %.0f MB · jeda peringatan %.0f MB"
          % (WARN_MB, URGENT_MB, STEP_MB))
    print("total sesi: %d | di atas WARN: %d" % (len(rows), warn))
    for size, proj, fn in rows[:10]:
        print("  %9s  %s/%s" % (human(size), proj.replace("-Users-chaali0324", "~"), fn[:36]))
    return 0


def main():
    args = sys.argv[1:]
    if args[:1] == ["--report"]:
        return report()
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # tanpa JSON hook: diam (jangan pernah mengganggu sesi)
    tip = "transcript_path" if payload.get("transcript_path") else "transcriptPath"
    out = check(payload.get(tip, ""), session_key(payload))
    if out:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
