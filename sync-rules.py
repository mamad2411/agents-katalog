#!/usr/bin/env python3
"""sync-rules — satu sumber aturan untuk SEMUA AI CLI.

Sumber kanonik : ~/.agents/RULES.md
Tambahan/tool  : ~/.agents/rules/<tool>.md  (opsional)

Menulis ulang file aturan tiap tool supaya isinya identik dan ramping.
File asli di-backup sekali ke ~/.agents/rules-backup-<tanggal>/.

pakai: python3 ~/.agents/sync-rules.py [--check]
"""
import os
import shutil
import subprocess
import sys
from datetime import date

HOME = os.path.expanduser("~")
AGENTS = f"{HOME}/.agents"
CANON = f"{AGENTS}/RULES.md"
BACKUP = f"{AGENTS}/rules-backup-{date.today().strftime('%Y%m%d')}"

POINTER = """# Aturan global AI

Semua aturan ada di `~/.agents/RULES.md` (kanonik, dipakai semua AI CLI).
Baca file itu sekali di awal sesi, lalu ikuti. Jangan menyalin isinya ke sini.

Ringkas: skill dicari lewat `python3 ~/.agents/skillq.py "<tugas>" -n 5` (0 token prompt),
output ≤15 baris, rencana dulu, verifikasi sebelum bilang selesai, MCP on-demand saja.
"""

# target -> (judul opsional, extras key atau None)
TARGETS = {
    f"{HOME}/.claude/CLAUDE.md": ("# CLAUDE.md", "claude"),
    f"{HOME}/.codex/AGENTS.md": ("# AGENTS.md (Codex)", "codex"),
    f"{HOME}/.gemini/GEMINI.md": ("# Gemini CLI — aturan", "gemini"),
    f"{HOME}/.codebuddy/AGENTS.md": ("# AGENTS.md (CodeBuddy)", "codebuddy"),
    f"{HOME}/.cline/.clinerules": ("# Cline rules", None),
    f"{HOME}/.copilot/custom-instructions.md": ("# Copilot custom instructions", None),
}

POINTER_ONLY = [
    f"{HOME}/.gemini/AGENTS.md",
    f"{HOME}/AI_TOKEN_GUARD.md",
]


def read(p):
    try:
        with open(p) as f:
            return f.read()
    except OSError:
        return ""


def build(title, extras_key):
    canon = read(CANON).strip()
    if canon.startswith("# "):
        canon = canon.split("\n", 1)[1].lstrip()
    parts = [title.strip(), "", canon]
    if extras_key:
        extra = read(f"{AGENTS}/rules/{extras_key}.md").strip()
        if extra:
            parts += ["", extra]
    lessons = read(f"{AGENTS}/rules/lessons.md").strip()
    if lessons:
        parts += ["", "## Pelajaran (otomatis dari kegagalan)", lessons]
    parts += [
        "",
        "---",
        f"_Sumber: `~/.agents/RULES.md` + `~/.agents/rules/{extras_key or 'umum'}.md`. "
        "Jangan edit file ini langsung — edit sumbernya lalu jalankan "
        "`python3 ~/.agents/sync-rules.py`._",
        "",
    ]
    return "\n".join(parts)


def backup(path):
    if not os.path.exists(path):
        return
    os.makedirs(BACKUP, exist_ok=True)
    dst = os.path.join(BACKUP, path.replace(HOME + "/", "").replace("/", "__"))
    if not os.path.exists(dst):
        shutil.copy2(path, dst)


def main():
    check = "--check" in sys.argv
    if not os.path.exists(CANON):
        sys.exit(f"sumber tidak ada: {CANON}")
    rows = []
    planned = []
    for path, (title, key) in TARGETS.items():
        new = build(title, key)
        old = read(path)
        rows.append((path, len(old), len(new)))
        planned.append((path, new, old))
    if not check and any(o != n for _, n, o in planned):
        subprocess.run(
            [os.path.expanduser("~/.local/bin/mamat-backup")],
            capture_output=True,
        )
    for path, new, old in planned:
        if not check:
            backup(path)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(new)
    for path in POINTER_ONLY:
        old = read(path)
        rows.append((path, len(old), len(POINTER)))
        if not check:
            backup(path)
            with open(path, "w") as f:
                f.write(POINTER)

    # Cursor: satu file aturan, sisanya dipindah ke backup
    cur = f"{HOME}/.cursor/rules"
    if os.path.isdir(cur):
        for name in sorted(os.listdir(cur)):
            if not name.endswith(".mdc") or name == "mamat-rules.mdc":
                continue
            src = os.path.join(cur, name)
            rows.append((src, os.path.getsize(src), 0))
            if not check:
                backup(src)
                os.remove(src)
        dst = os.path.join(cur, "mamat-rules.mdc")
        new = "---\ndescription: aturan global AI\nalwaysApply: true\n---\n\n" + build("", "cursor")
        old = read(dst)
        rows.append((dst, len(old), len(new)))
        if not check:
            backup(dst)
            with open(dst, "w") as f:
                f.write(new)

    total_old = total_new = 0
    for path, o, n in rows:
        total_old += o
        total_new += n
        print(f"{o:6d} -> {n:6d}  {path.replace(HOME, '~')}")
    print(f"\ntotal {total_old} -> {total_new} char "
          f"(hemat ~{(total_old - total_new) // 4} token per request per tool)")
    if check:
        print("(mode --check: tidak menulis apa pun)")


if __name__ == "__main__":
    main()
