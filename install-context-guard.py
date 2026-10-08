#!/usr/bin/env python3
"""install-context-guard.py — pasang blok aturan "hemat konteks" ke file rules
SEMUA tool AI, dengan pola yang sama seperti install-skill-contract.py.

Kenapa: penyebab limit cepat habis bukan model, tapi kebiasaan sesi panjang +
gambar base64 + pembacaan file raksasa (terukur: Claude 4,42 M token; Cline
4,5 M token; 1 sesi = 50 gambar = ±7,5 jt token/hari diulang). Hook hanya
mengingatkan; file rules = satu-satunya mekanisme yang dimiliki tool tanpa hook
(Cursor, Windsurf, Aider, Continue, Roo, Qwen, OpenCode, Trae, CodeBuddy, Hermes).

Idempotent: blok di antara marker context-guard:start/end diganti, bukan ditumpuk.
Backup sekali per hari (.bak-YYYYMMDD). Tidak pernah menghapus file.

Pakai:
  python3 ~/.agents/install-context-guard.py            # dry-run (rencana)
  python3 ~/.agents/install-context-guard.py --apply     # pasang
  python3 ~/.agents/install-context-guard.py --check     # status semua target
"""
import datetime
import os
import shutil
import sys

HOME = os.path.expanduser("~")
START = "<!-- context-guard:start -->"
END = "<!-- context-guard:end -->"
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")

# (tool, kandidat path rules — yang ada/diregistrasi saja yang disentuh)
TARGETS = [
    ("claude",     [HOME + "/.claude/CLAUDE.md", HOME + "/.claude/CLAUDE.md"]),
    ("codex",      [HOME + "/.codex/AGENTS.md"]),
    ("gemini",     [HOME + "/.gemini/GEMINI.md"]),
    ("cline",      [HOME + "/.cline/.clinerules"]),
    ("cursor",     [HOME + "/.cursorrules", HOME + "/.cursor/rules"] ),
    ("windsurf",   [HOME + "/.windsurf/.windsurfrules"]),
    ("continue",   [HOME + "/.continue/.continuerules"]),
    ("roo",        [HOME + "/.roo/.roorules"]),
    ("qwen",       [HOME + "/.qwen/QWEN.md"]),
    ("aider",      [HOME + "/.aider/CONVENTIONS.md"]),
    ("opencode",   [HOME + "/.opencode/AGENTS.md", HOME + "/.config/opencode/AGENTS.md"]),
    ("codebuddy",  [HOME + "/.codebuddy/AGENTS.md"]),
    ("hermes",     [HOME + "/.hermes/AGENTS.md"]),
    ("trae",       [HOME + "/.trae/AGENTS.md"]),
    ("openclaude", [HOME + "/.openclaude/CLAUDE.md"]),
    ("iflow",      [HOME + "/.iflow/AGENTS.md"]),
    ("repo",       [HOME + "/receptor/CLAUDE.md", HOME + "/receptor/AGENTS.md"]),
]

BLOCK = START + """
## ⛔ Hemat konteks (WAJIB — inilah penyebab limit cepat habis)

Terukur di mesin ini: riwayat sesi dikirim ulang pada SETIAP request, sehingga
satu sesi panjang menghabiskan ratusan juta token (±0,5 juta token per pesan).

- **Satu sesi = satu tugas.** >200 pesan atau transcript >10 MB → tutup sesi,
  buka baru dengan catatan handoff singkat. Jangan `--resume` sesi raksasa.
- **Jangan tempel gambar di sesi panjang.** Base64 menempel di riwayat dan ikut
  terkirim selamanya (terukur: 50 gambar = 22 MB ≈ ±7,5 jt token diulang tiap
  request). Simpan gambar ke file, rujuk path-nya, lalu tutup sesinya.
- **DILARANG baca penuh**: `vendor/`, `node_modules/`, `dist/`, `build/`,
  `*.min.js`, `public/template/`, `skills-expanded/`. Butuh 1 baris →
  `grep -n` / `sed -n`, jangan baca file utuh.
- **Muat skill secara ringan**: `bash ~/.agents/skill-load-lite.sh <nama>`
  (≤80 baris / ≤2 KB), BUKAN SKILL.md penuh (~9 KB). Jangan muat ulang skill
  yang sudah dimuat di sesi yang sama.
- **Output tool diringkas** ±800 karakter; jangan dump mentah; jangan baca ulang
  file yang sudah dibaca; paralelkan call yang saling bebas.
- **MCP cukup** `skill-catalog` + `mcp-router`. Server lain diparkir di
  `~/.agents/mcp-parked.json` → hidupkan on-demand:
  `python3 ~/.agents/mcp-lifecycle.py --on <nama>`.
- **Teams/spawn**: tiap agen punya konteks sendiri (pengali token) — pakai hanya
  kalau benar-benar perlu parallel.
- **Ukur, jangan tebak**: `python3 ~/.agents/ai-context-audit.py` (semua tool),
  `python3 ~/.agents/usage-audit.py` (Claude), `python3 ~/.agents/audit-cline.py`.
""" + END + "\n"


def pick(paths):
    """Path pertama yang filenya ada; kalau belum, path yang direktorinya ada."""
    for p in paths:
        if os.path.isfile(p):
            return p
    for p in paths:
        if os.path.isdir(os.path.dirname(p)) and not os.path.isdir(p):
            return p
    return None


# target yang hanya boleh disentuh kalau file sudah ada (jangan bikin file baru)
EXISTING_ONLY = {"repo"}
# penanda substansi: minimal DUA harus ada supaya dianggap sudah punya aturan hemat
PENANDA = ["vendor", "skill-load-lite", "tutup sesi", "sesi baru", "base64", "context-guard", "session hygiene"]
MIN_PENANDA = 2


def state(path, tool=""):
    """Content-aware: 'sudah' kalau blok/penanda substansial sudah ada; 'upgrade'
    kalau blok lama beda dari BLOCK terbaru; 'perlu' kalau belum; 'baru' kalau file
    belum ada; 'lewat' untuk target yang tidak boleh dibuat baru."""
    if not os.path.isfile(path):
        return "lewat" if tool in EXISTING_ONLY else "baru"
    txt = open(path, encoding="utf-8", errors="ignore").read()
    low = txt.lower()
    if START in txt:
        return "sudah" if BLOCK.strip() in txt else "upgrade"
    if sum(1 for k in PENANDA if k in low) >= MIN_PENANDA:
        return "sudah"
    return "perlu"


def render(old):
    if START in old and END in old:
        i = old.index(START)
        j = old.index(END) + len(END)
        return old[:i] + BLOCK.rstrip("\n") + old[j:]
    return (old.rstrip("\n") + "\n\n" if old.strip() else "") + BLOCK


def backup(path):
    b = "%s.bak-%s" % (path, STAMP)
    if not os.path.exists(b):
        shutil.copy2(path, b)
    return b


def main():
    apply = "--apply" in sys.argv
    check = "--check" in sys.argv
    print("=== PEMASANGAN ATURAN HEMAT KONTEKS (%s) ===" % ("APPLY" if apply else "dry-run" if not check else "CHECK"))
    n_write = n_ok = n_skip = 0
    for tool, paths in TARGETS:
        p = pick(paths)
        if not p:
            n_skip += 1
            print("  %-11s %-52s alat tidak terpasang" % (tool, "-"))
            continue
        st = state(p, tool)
        if st == "sudah":
            n_ok += 1
            print("  %-11s %-52s sudah rapi (aturan hemat sudah ada)" % (tool, p.replace(HOME, "~")))
            continue
        if st == "lewat":
            n_skip += 1
            print("  %-11s %-52s dilewati (file belum ada, tidak akan dibuat)" % (tool, p.replace(HOME, "~")))
            continue
        old = open(p, encoding="utf-8", errors="ignore").read() if os.path.isfile(p) else ""
        new = render(old)
        if apply and new != old:
            if old:
                backup(p)
            with open(p, "w", encoding="utf-8") as f:
                f.write(new)
        label = {"perlu": "akan ditulis", "baru": "akan dibuat", "upgrade": "akan diperbarui"}[st]
        n_write += 1
        print("  %-11s %-52s %s %+d B" % (tool, p.replace(HOME, "~"), label, len(new) - len(old)))
    print("\ntotal: %d perlu ditulis, %d sudah rapi, %d dilewati (tool tak terpasang)" % (n_write, n_ok, n_skip))
    if not apply:
        print("jalankan: python3 ~/.agents/install-context-guard.py --apply")
    else:
        print("blok ditandai %s … %s — idempotent, backup .bak-%s" % (START, END, STAMP))
    return 0


if __name__ == "__main__":
    sys.exit(main())

