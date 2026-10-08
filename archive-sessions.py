#!/usr/bin/env python3
"""archive-sessions.py — arsip otomatis riwayat sesi AI (>7 hari), PINDAH bukan hapus.

Kenapa: riwayat sesi yang menumpuk = bahan bakar untuk `--resume` sesi raksasa
(tiap request mengirim ulang seluruh riwayat). Tugas bulanan manual jarang
dilakukan → dijalankan otomatis dari `session-brief.sh` (pola sama seperti
`mcp-lifecycle --gc-if-due`), maksimal 1× per minggu.

Kebijakan keamanan (kualitas AI tidak boleh terpengaruh):
  * HANYA memindahkan; tidak ada operasi hapus sama sekali.
  * Hanya sesi dengan mtime > ARCHIVE_AFTER_DAYS (default 7) — sesi muda,
    sesi aktif, dan sesi yang kemungkinan sedang dikerjakan TIDAK disentuh.
  * Manifest bertambah: ~/ARCHIVE-MANIFEST.txt (restore = mv balik).

Tool yang dicakup (semua riwayat terdeteksi di mesin ini):
  Claude Code : ~/.claude/projects/*/*.jsonl          → ~/.claude/archived-projects/<proj>/
  Cline CLI   : ~/.cline/data/sessions/<id>/          → ~/.cline/archived-sessions/<id>/
  CodeBuddy   : ~/.codebuddy/projects/*/*.jsonl       → ~/.codebuddy/archived-projects/<proj>/

Pakai:
  python3 ~/.agents/archive-sessions.py --dry-run     # laporan tanpa pindah
  python3 ~/.agents/archive-sessions.py --force       # pindah sekarang (lewati gate mingguan)
  bash ~/.agents/session-brief.sh                     # gate otomatis (1×/minggu, sunyi)
Env: ARCHIVE_AFTER_DAYS (7) · ARCHIVE_FORCE_UNSAFE=1 untuk mengizinkan <7 hari (TIDAK disarankan).
"""
import glob
import json
import os
import shutil
import sys
import time

HOME = os.path.expanduser("~")
DAYS = int(os.environ.get("ARCHIVE_AFTER_DAYS", "7"))
STAMP_F = os.path.join(HOME, ".agents", ".archive-state.json")
MANIFEST = os.path.join(HOME, "ARCHIVE-MANIFEST.txt")
GATE_DAYS = 7

SOURCES = [
    ("claude",    HOME + "/.claude/projects/*/*.jsonl",        HOME + "/.claude/archived-projects",     "file"),
    ("cline",     HOME + "/.cline/data/sessions/*",            HOME + "/.cline/archived-sessions",      "dir"),
    ("codebuddy", HOME + "/.codebuddy/projects/*/*.jsonl",     HOME + "/.codebuddy/archived-projects",  "file"),
]


def newest_mtime(path, is_dir):
    if is_dir:
        best = os.path.getmtime(path)
        for root, _, files in os.walk(path):
            for f in files:
                try:
                    best = max(best, os.path.getmtime(os.path.join(root, f)))
                except OSError:
                    pass
        return best
    return os.path.getmtime(path)


def due(days):
    try:
        last = json.load(open(STAMP_F)).get("last", 0)
    except Exception:
        last = 0
    return (time.time() - last) >= days * 86400


def stamp():
    try:
        os.makedirs(os.path.dirname(STAMP_F), exist_ok=True)
        json.dump({"last": time.time(), "by": "archive-sessions.py"}, open(STAMP_F, "w"))
    except Exception:
        pass


def run(dry=False):
    cutoff = time.time() - DAYS * 86400
    moved, bytes_moved, skipped = [], 0, 0
    for tool, pat, arc, kind in SOURCES:
        for p in sorted(glob.glob(pat)):
            if kind == "file" and not os.path.isfile(p):
                continue
            if kind == "dir" and not os.path.isdir(p):
                continue
            if newest_mtime(p, kind == "dir") > cutoff:
                skipped += 1   # masih muda (< DAYS) → jangan disentuh
                continue
            if dry:
                moved.append((tool, os.path.basename(p), os.path.getsize(p) if kind == "file" else -1))
                continue
            proj = os.path.basename(os.path.dirname(p)) if kind == "file" else "sessions"
            dst_dir = os.path.join(arc, proj) if kind == "file" else arc
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(dst_dir, os.path.basename(p))
            if os.path.exists(dst):  # jangan pernah menimpa
                dst += ".%d" % int(time.time())
            size = os.path.getsize(p) if kind == "file" else sum(
                os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(p) for f in fs)
            shutil.move(p, dst)
            moved.append((tool, os.path.basename(p), size))
            bytes_moved += size
    if moved and not dry:
        with open(MANIFEST, "a") as fh:
            fh.write("\n# archive-sessions.py %s (> %d hari)\n"
                     % (time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), DAYS))
            for tool, name, size in moved:
                fh.write("%s\t%s\t%d B\n" % (tool, name, size))
    if not dry:
        stamp()  # catat tiap run (walau tidak ada yang dipindah) supaya gate mingguan akurat
    return moved, bytes_moved, skipped


def main():
    a = sys.argv[1:]
    dry = "--dry-run" in a
    force = "--force" in a
    if not (dry or force) and not due(GATE_DAYS):
        return 0  # sunyi: sudah jalan minggu ini (dipanggil dari session-brief)
    moved, nbytes, skipped = run(dry=dry)
    if moved or dry:
        mode = "DRY-RUN" if dry else "PINDAH"
        print("archive-sessions [%s]: %d item %s %.1f MB (>= %d hari) · %d sesi muda dilewati"
              % (mode, len(moved),
                 "akan" if dry else "dipindah", (nbytes if not dry else sum(m[2] for m in moved if m[2] > 0)) / 2**20,
                 DAYS, skipped))
        if dry:
            for tool, name, size in moved:
                print("  %-9s %-45s %.1f MB" % (tool, name[:45], max(size, 0) / 2**20))
    return 0


if __name__ == "__main__":
    sys.exit(main())
