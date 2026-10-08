#!/usr/bin/env python3
"""ai-context-audit.py — audit ukuran sesi/riwayat SEMUA tool AI di mesin ini.

Kenapa: penyebab limit cepat habis hampir selalu sama di tool mana pun —
riwayat yang dikirim ulang tiap request (dan gambar base64 yang menempel
selamanya). Tiap tool menyimpan di tempat berbeda; skrip ini menyatukannya.

Baca-saja, tidak mengubah apa pun. Idempotent.

Pakai:
  python3 ~/.agents/ai-context-audit.py            # tabel semua tool
  python3 ~/.agents/ai-context-audit.py --json     # mesin (untuk hook/cron)
Ambang: AMBANG_MB (default 10 MB per sesi), AMBANG_PESAN (default 200).
"""
import glob
import json
import os
import sys

HOME = os.path.expanduser("~")
MB = 2**20
AMBANG_MB = float(os.environ.get("AMBANG_MB", "10"))
AMBANG_PESAN = int(os.environ.get("AMBANG_PESAN", "200"))
BIG_STR = 16384  # string sepanjang ini = kandidat lampiran base64

# (tool, pola file riwayat)
LOKASI = [
    ("Claude Code", [HOME + "/.claude/projects/*/*.jsonl"]),
    ("Cline CLI",   [HOME + "/.cline/data/sessions/*/*.messages.json"]),
    ("Gemini CLI",  [HOME + "/.gemini/tmp/*/chats/*.json", HOME + "/.gemini/history/*/*.json"]),
    ("Qwen Code",   [HOME + "/.qwen/tmp/*/chats/*.json", HOME + "/.qwen/tmp/*/*.json"]),
    ("Codex CLI",   [HOME + "/.codex/sessions/**/*.jsonl", HOME + "/.codex/history*.jsonl"]),
    ("OpenCode",    [HOME + "/.local/share/opencode/storage/**/*.json"]),
    ("OpenClaude",  [HOME + "/.openclaude/projects/*/*.jsonl"]),
    ("iFlow",       [HOME + "/.iflow/projects/*/*.jsonl"]),
    ("Aider",       [HOME + "/.aider.chat.history.md", HOME + "/.aider.history"]),
]
# penyimpanan tool berbasis VS Code — ukur berat saja, tidak diparse
VSCDB = [
    ("Cursor",    [HOME + "/Library/Application Support/Cursor/User/globalStorage/state.vscdb"]),
    ("Roo Code",  [HOME + "/Library/Application Support/Code/User/globalStorage/roovetech.roo-code/**"]),
    ("Kilo Code", [HOME + "/Library/Application Support/Code/User/globalStorage/kilocode.kilo-code/**"]),
    ("Cline ext", [HOME + "/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/**"]),
]


def walk(node, acc):
    """Hitung pesan (objek ber-'role'), char lampiran base64, dan jumlah gambar."""
    if isinstance(node, dict):
        if isinstance(node.get("role"), str):
            acc[0] += 1
        if node.get("type") in ("image", "image_url", "input_image") or "source" in node and isinstance(node.get("source"), dict):
            acc[2] += 1
        for k, v in node.items():
            if k in ("data", "base64", "imageData") and isinstance(v, str):
                acc[1] += len(v)
            else:
                walk(v, acc)
    elif isinstance(node, list):
        for v in node:
            walk(v, acc)
    elif isinstance(node, str) and len(node) > BIG_STR:
        acc[1] += len(node)  # string raksasa terselip di teks = lampiran


def scan(path):
    """(pesan, char_base64, n_gambar) dari satu file riwayat; toleran jsonl/json."""
    acc = [0, 0, 0]
    try:
        if path.endswith(".jsonl"):
            with open(path, encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if len(line) > 2:
                        try:
                            walk(json.loads(line), acc)
                        except Exception:
                            pass
        elif path.endswith(".json"):
            if os.path.getsize(path) > 120 * MB:
                return -1, 0, 0  # terlalu besar untuk diparse; cukup ukur berat
            with open(path, encoding="utf-8", errors="ignore") as f:
                walk(json.load(f), acc)
    except RecursionError:
        pass
    except Exception:
        pass
    return acc[0], acc[1], acc[2]


sys.setrecursionlimit(20000)


def measure(patterns):
    files = []
    for pat in patterns:
        files += glob.glob(pat, recursive=True)
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        return None
    total = sum(os.path.getsize(f) for f in files)
    big = max(files, key=os.path.getsize)
    msgs, b64, imgs = scan(big)
    return dict(n=len(files), total=total, big=os.path.basename(big),
                big_mb=os.path.getsize(big) / MB, msgs=msgs, b64=b64, imgs=imgs)


def main():
    as_json = "--json" in sys.argv
    rows, warnings = [], []
    for tool, pats in LOKASI:
        m = measure(pats)
        if not m:
            rows.append(dict(tool=tool, status="kosong"))
            continue
        flags = []
        if m["big_mb"] > AMBANG_MB:
            flags.append("sesi terbesar %.0f MB" % m["big_mb"])
        if m["msgs"] > AMBANG_PESAN:
            flags.append("%d pesan" % m["msgs"])
        if m["b64"] / MB > 2:
            # jujur: gambar ditagih per tile (±1.000-1.600 token/gambar), BUKAN per
            # karakter base64 — tapi payload-nya ikut terkirim di tiap request.
            flags.append("%d gambar (base64 %.0f MB) ≈ ±%.1f jt token, diulang tiap request"
                         % (m["imgs"], m["b64"] / MB, m["imgs"] * 1500 / 1e6))
        rows.append(dict(tool=tool, status="ada", files=m["n"], total_mb=round(m["total"] / MB, 1),
                         big_mb=round(m["big_mb"], 1), msgs=m["msgs"], imgs=m["imgs"], flags=flags))
        if flags:
            warnings.append("%s — %s" % (tool, ", ".join(flags)))
    for tool, pats in VSCDB:
        tot = sum(os.path.getsize(f) for pat in pats for f in glob.glob(pat, recursive=True) if os.path.isfile(f))
        rows.append(dict(tool=tool, status="sqlite/biner", total_mb=round(tot / MB, 1)))

    if as_json:
        print(json.dumps(dict(tools=rows, perlu_perhatian=warnings), ensure_ascii=False))
        return 0
    print("=== RIWAYAT/SESI SEMUA TOOL AI ===")
    print("ambang: sesi >%.0f MB atau >%d pesan; lampiran base64 >2 MB\n" % (AMBANG_MB, AMBANG_PESAN))
    print("  %-12s %-14s %6s %9s %9s %8s  %s" % ("tool", "status", "sesi", "total MB", "MB sesi*", "pesan", "catatan"))
    for r in rows:
        if r["status"] == "kosong":
            print("  %-12s %-14s" % (r["tool"], "tidak ada riwayat"))
        else:
            print("  %-12s %-14s %6s %9s %9s %8s  %s" % (
                r["tool"], r["status"], r.get("files", "-"), r.get("total_mb", "-"),
                r.get("big_mb", "-"), r.get("msgs", "-"), ", ".join(r.get("flags", [])) or "sehat"))
    print("\n* MB sesi terbesar")
    if warnings:
        print("\nPERLU PERHATIAN (riwayat dikirim ulang pada SETIAP request):")
        for w in warnings:
            print("  ⚠ " + w)
        print("\n  Tindakan: tutup sesi itu dan buka sesi baru per tugas; jangan tempel")
        print("  gambar di sesi panjang (base64 ikut terkirim selamanya).")
    else:
        print("\nSemua tool di bawah ambang.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

