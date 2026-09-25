#!/usr/bin/env python3
"""install-skill-contract.py — pasang KONTRAK SKILL ke semua AI yang tidak punya hook.

Kenapa perlu: Claude/Cline/Gemini/Codex punya hook UserPromptSubmit yang menyuntik
skill otomatis tiap prompt. 9 AI lain (Cursor, Windsurf, Aider, Continue, Trae, Roo,
Qwen, OpenCode, Pi) TIDAK punya hook -> andalkan file rules. File rules = "ingat"
persisten selama sesi, jadi isinya harus berupa PERINTAH tegas, bukan saran.

Idempotent: blok di antara marker skill-contract:start/end diganti, bukan ditumpuk.
Backup: sekali per hari (.bak-YYYYMMDD). Tidak menghapus file lain.

Pakai:
  python3 ~/.agents/install-skill-contract.py           # pasang/update semua
  python3 ~/.agents/install-skill-contract.py --check   # audit: mana sudah punya kontrak
"""
import argparse
import os
import shutil
import sys
from datetime import datetime, timezone

AG = os.path.expanduser("~/.agents")
START = "<!-- skill-contract:start -->"
END = "<!-- skill-contract:end -->"

CONTRACT = """<!-- skill-contract:start -->
## ⚡ WAJIB: CARI & MUAT SKILL SEBELUM BEKERJA

Katalog **3.176 skill curated** di `~/.agents/` + MCP `skill-catalog`
(`skill_for_task`, `skill_search`, `skill_load`, `agent_context`).

**LANGKAH WAJIB sebelum menulis kode / menjawab / menjalankan perintah:**

1. **Cari skill** — pilih salah satu:
   - MCP: `skill_for_task(task="<deskripsi tugas>")`  ← paling cepat
   - Shell: `~/.agents/skill-search.sh "<kata kunci>"`
2. **Kalau ada yang cocok** → `skill_load("<nama>")` (atau baca
   `~/.agents/skills-store/<nama>/SKILL.md`) lalu **IKUTI** isi SKILL.md itu.
   Skill punya `scripts/` — jalankan scriptnya, jangan tulis ulang dari nol.
3. **Kalau tidak ada** → kerja dari nol; kalau polanya bakal berulang,
   usulkan SKILL.md baru (jangan mengarang skill yang sudah ada).
4. **Hanya muat 1-2 skill yang relevan.** JANGAN muat daftar/katalog lengkap.

**Alur kerja:** pahami → pilih skill → rujuk sumber asli → rencana → eksekusi →
verifikasi → poles (UI: `anti-ui-slop` + `de-sloppify`) → lapor jujur.

**Selalu:** `caveman-token-optimizer` (jawaban ringkas, tanpa basa-basi) +
`verification-loop` (uji sebelum menyatakan selesai).

Detail lengkap (baca on-demand, bukan sekarang): `~/.agents/SKILL-FLOW.md`
Aturan katalog: `~/.agents/AGENTS.md`
<!-- skill-contract:end -->"""

# (path, label) — file yang dibaca tool tsb
TARGETS = [
    ("~/.cursor/rules/skill-catalog.mdc", "Cursor (alwaysApply)"),
    ("~/.windsurf/.windsurfrules", "Windsurf"),
    ("~/.aider/CONVENTIONS.md", "Aider"),
    ("~/.continue/.continuerules", "Continue"),
    ("~/.trae/AGENTS.md", "Trae"),
    ("~/.roo/rules/00-auto-skill.md", "Roo"),
    ("~/.roo/.roorules", "Roo (global)"),
    ("~/.qwen/QWEN.md", "Qwen"),
    ("~/.opencode/AGENTS.md", "OpenCode (data)"),
    ("~/.config/opencode/AGENTS.md", "OpenCode (config)"),
    ("~/.pi/AGENTS.md", "Pi"),
    ("~/.kilocode/AGENTS.md", "KiloCode"),
    ("~/.clinerules", "Cline (global rules)"),
    ("~/.cline/.clinerules", "Cline (dir rules)"),
]


def backup_once(p):
    if not os.path.exists(p):
        return
    bak = f"{p}.bak-{datetime.now(timezone.utc):%Y%m%d}"
    if not os.path.exists(bak):
        shutil.copy2(p, bak)


def install(path, label):
    """Sisipkan kontrak (idempotent). Return (status, detail)."""
    full = os.path.expanduser(path)
    if os.path.exists(full):
        backup_once(full)
        with open(full, encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        if START in txt and END in txt:
            pre = txt[:txt.index(START)]
            post = txt[txt.index(END) + len(END):]
            new = pre + CONTRACT + post
            if new == txt:
                return "sudah", label
        else:
            # buang sisa angka lama yang menyesatkan
            clean = txt
            for old in ("≈63,436", "≈25,474", "≈30.000", "≈14.916",
                        "63,436", "14.916"):
                clean = clean.replace(old, "3.176")
            new = clean.rstrip() + "\n\n" + CONTRACT + "\n"
        with open(full, "w", encoding="utf-8") as f:
            f.write(new)
        return "diupdate", label
    else:
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(CONTRACT + "\n")
        return "dibuat", label


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    if a.check:
        print("=== AUDIT KONTRAK SKILL ===")
        ok = miss = 0
        for path, label in TARGETS:
            full = os.path.expanduser(path)
            if not os.path.exists(full):
                print(f"  ✗ {label:26s} file tidak ada: {path}")
                miss += 1
            elif START in open(full, encoding="utf-8", errors="ignore").read():
                print(f"  ✓ {label:26s} kontrak terpasang")
                ok += 1
            else:
                print(f"  ✗ {label:26s} kontrak belum ada")
                miss += 1
        print(f"\nlengkap: {ok} | kurang: {miss}")
        return 0

    print("=== PASANG KONTRAK SKILL ===")
    for path, label in TARGETS:
        try:
            status, lb = install(path, label)
            print(f"  {status:9s} {lb}")
        except Exception as e:
            print(f"  GAGAL     {lb}: {e}", file=sys.stderr)
    print("\nSemua AI tanpa hook sekarang punya kontrak skill di file rules-nya.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())