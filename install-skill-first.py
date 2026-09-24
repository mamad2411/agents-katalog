#!/usr/bin/env python3
"""install-skill-first.py — pasang "skill-first protocol" ke SEMUA agen (idempotent).

Yang dipasang:
  1. MCP server `skill-catalog` (tools: skills_available, skill_search, skill_for_task,
     skill_load, agent_context) ke SEMUA provider yang punya config MCP
     (codex TOML, gemini/codebuddy/hermes/trae/opencode/aider/cline/windsurf/continue/roo JSON).
     Claude Code: didaftarkan lewat `claude mcp add --scope user skill-catalog -- python3 ~/.agents/skill-mcp.py`
  2. Blok "Skill-First Protocol" (dengan marker <!-- skill-first:start/end -->) ke file aturan
     tiap provider, jadi AI-nya BENAR-BENAR tahu ada N skill siap pakai.
     Angka N dibaca dari skills-index.json/db (auto-refresh, tidak pernah basi).
  3. Hook SessionStart di ~/.claude/settings.json → session-brief.sh tiap sesi.

Semua penulisan: backup .bak-YYYYMMDD + validasi (tomllib/json) sebelum ganti.
Pakai: python3 ~/.agents/install-skill-first.py [--apply]
"""
import json
import os
import shutil
import sys
import tomllib
from datetime import datetime

HOME = os.path.expanduser("~")
SCRIPT = os.path.join(HOME, ".agents", "skill-mcp.py")
BRIEF = os.path.join(HOME, ".agents", "session-brief.sh")
CODEX = os.path.join(HOME, ".codex", "config.toml")
CLAUDE_SETTINGS = os.path.join(HOME, ".claude", "settings.json")
NAME = "skill-catalog"
APPLY = "--apply" in sys.argv
STAMP = datetime.now().strftime("%Y%m%d")
done, skip, todo = [], [], []

# (label, mcp_config, "json"/"toml"/"claude", file_aturan_skill_first)
PROVIDERS = [
    ("claude",    None,                                          "claude", os.path.join(HOME, ".claude", "CLAUDE.md")),
    ("codex",     CODEX,                                        "toml", os.path.join(HOME, ".codex", "AGENTS.md")),
    ("gemini",    os.path.join(HOME, ".gemini", "settings.json"), "json", os.path.join(HOME, ".gemini", "GEMINI.md")),
    ("codebuddy", os.path.join(HOME, ".codebuddy", "mcp.json"),  "json", os.path.join(HOME, ".codebuddy", "AGENTS.md")),
    ("hermes",    os.path.join(HOME, ".hermes", "mcp.json"),     "json", os.path.join(HOME, ".hermes", "AGENTS.md")),
    ("trae",      os.path.join(HOME, ".trae", "mcp.json"),       "json", os.path.join(HOME, ".trae", "AGENTS.md")),
    ("opencode",  os.path.join(HOME, ".opencode", "mcp.json"),   "json", os.path.join(HOME, ".opencode", "AGENTS.md")),
    ("aider",     os.path.join(HOME, ".aider", "mcp.json"),      "json", os.path.join(HOME, ".aider", "CONVENTIONS.md")),
    ("cline",     os.path.join(HOME, ".cline", "mcp.json"),      "json", os.path.join(HOME, ".cline", ".clinerules")),
    ("windsurf",  os.path.join(HOME, ".windsurf", "mcp.json"),   "json", os.path.join(HOME, ".windsurf", ".windsurfrules")),
    ("continue",  os.path.join(HOME, ".continue", "mcp.json"),   "json", os.path.join(HOME, ".continue", ".continuerules")),
    ("roo",       os.path.join(HOME, ".roo", "mcp.json"),        "json", os.path.join(HOME, ".roo", ".roorules")),
    ("qwen",      os.path.join(HOME, ".qwen", "mcp.json"),       "json", os.path.join(HOME, ".qwen", "QWEN.md")),
    ("opencode2", os.path.join(HOME, ".config", "opencode", "opencode.json"), "json",
                  os.path.join(HOME, ".config", "opencode", "AGENTS.md")),
]
RULE_BEGIN = "<!-- skill-first:start -->"
RULE_END = "<!-- skill-first:end -->"


def backup(p):
    b = "%s.bak-%s" % (p, STAMP)
    if not os.path.exists(b):
        shutil.copy2(p, b)
    return b


def live_numbers():
    """Angka nyata dari indeks (bukan hardcode) supaya tidak basi lagi."""
    n_skills = n_curated = n_repos = 0
    try:
        d = json.load(open(os.path.join(HOME, ".agents", "skills-index.json"), encoding="utf-8"))
        n_skills = d.get("tier1_count") or 0
        n_curated = d.get("total_curated") or 0
    except Exception:
        pass
    if not n_skills:
        try:
            import sqlite3
            con = sqlite3.connect(os.path.join(HOME, ".agents", "skills-index.db"))
            n_skills = con.execute("SELECT COUNT(*) FROM skills WHERE tier!='junk'").fetchone()[0]
            n_curated = con.execute("SELECT COUNT(*) FROM skills WHERE tier='curated'").fetchone()[0]
            con.close()
        except Exception:
            pass
    try:
        n_repos = len(os.listdir(os.path.join(HOME, ".agents", "repo-refs")))
    except Exception:
        pass
    return n_skills or 0, n_curated or 0, n_repos or 0


def rule_block(n_skills, n_curated, n_repos, skills_dir=None):
    """Blok RINGKAS yang selalu-on (~3 baris) — progressive disclosure.

    Dulu blok ini 11 baris/~800 B × 12 provider (~10 KB) dan membuat AI
    "keberatan". Kini yang di-inject permanen cuma 80/20-nya: ada N skill →
    cari dulu + caranya. Detail (protokol penuh, anti-ngarang, cara
    tambang/buat skill) TIDAK di-inject — AI membacanya on-demand dari
    ~/.agents/SKILL-FIRST.md hanya saat dibutuhkan.
    """
    local = (" — termasuk skill lokal `%s` (symlink ke `~/.agents/skills/`)" % skills_dir) if skills_dir else ""
    body = (
        "## Auto-Skill (MANDIRI — tanpa harus diminta user)\n\n"
        "Katalog **≈{n:,} skill** di `~/.agents/`{local} + MCP `skill-catalog` (tools: `skill_for_task`, `skill_search`, `skill_load`, `agent_context`).\n"
        "Cara kerja default-mu — JANGAN tunggu disuruh:\n\n"
        "1. **Sebelum kerja apa pun** → `skill_for_task(\"<tugas>\")`. Ada yang cocok → `skill_load` dan ikuti. Skill mined punya `REPO-REF.md` (repo + path + branch sumber) — telusuri kalau butuh workflow/struktur lebih dalam.\n"
        "2. **Gaya jawaban default: hemat token** → ikuti `caveman-token-optimizer` / `token-budget-advisor` (ringkas, tanpa basa-basi, tanpa mengulang konteks user). Butuh varian lain (kompres konteks, budget khusus, dsb) → daftar lengkap SEMUA skill hemat token: `~/.agents/STYLE-TOKEN-SAVER.md` (108 skill + path, JANGAN hanya 2 bintang itu).\n"
        "3. **Apa pun keluaran UI/design** → self-check `anti-ui-slop` + `de-sloppify` sebelum dikirim; ada gejala slop → perbaiki dulu, jangan dikirim mentah. Butuh reviewer/pendekatan lain → daftar lengkap SEMUA skill anti-slop & design taste: `~/.agents/STYLE-DESIGN-QUALITY.md` (44 skill + path, JANGAN hanya 2 itu).\n"
        "4. Tidak ada skill cocok → baru kerja dari nol; kalau polanya bakal berulang, usulkan SKILL.md baru.\n"
    ).format(n=n_skills, local=local)
    return RULE_BEGIN + "\n" + body + RULE_END + "\n"


def install_rule_file(path, label, n_skills, n_curated, n_repos, skills_dir=None):
    """Tulis/ganti blok skill-first di file aturan provider (marker = idempotent)."""
    if not path:
        return
    if not os.path.isdir(os.path.dirname(path)):
        return todo.append("%s: dir aturan tidak ada" % label)
    block = rule_block(n_skills, n_curated, n_repos, skills_dir)
    old = open(path, encoding="utf-8", errors="ignore").read() if os.path.exists(path) else ""
    if RULE_BEGIN in old and RULE_END in old:
        i, j = old.index(RULE_BEGIN), old.index(RULE_END) + len(RULE_END)
        new, state = old[:i] + block.rstrip("\n") + old[j:], "diperbarui"
    elif old.strip():
        new, state = old.rstrip("\n") + "\n\n" + block, "ditambahkan"
    else:
        new, state = block, "dibuat"
    if new == old:
        return skip.append("%s: aturan sudah terbaru" % label)
    if APPLY:
        if os.path.exists(path):
            backup(path)
        open(path, "w", encoding="utf-8").write(new)
    done.append("%s: aturan skill-first %s (%s)" % (label, state, "ditulis" if APPLY else "dry-run"))


def ensure_json(path, label):
    """Buat file config JSON kalau belum ada."""
    if os.path.exists(path):
        return True
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        todo.append("%s: dir tidak ada (%s)" % (label, d))
        return False
    if APPLY:
        json.dump({"mcpServers": {}}, open(path, "w", encoding="utf-8"), indent=2)
        done.append("%s: mcp.json baru dibuat" % label)
    else:
        done.append("%s: mcp.json akan dibuat" % label)
    return True


def register_codex():
    if not os.path.exists(CODEX):
        return todo.append("codex: config.toml tidak ada")
    text = open(CODEX, encoding="utf-8").read()
    if "[mcp_servers.%s]" % NAME in text:
        return skip.append("codex: sudah terpasang")
    block = ('\n[mcp_servers.%s]\ncommand = "python3"\nargs = ["%s"]\n' % (NAME, SCRIPT))
    new = text + block
    try:
        tomllib.loads(new)
    except Exception as e:
        return todo.append("codex: ABORT invalid TOML (%s)" % e)
    if APPLY:
        backup(CODEX)
        open(CODEX, "w", encoding="utf-8").write(new)
    done.append("codex: mcp_servers.%s %s" % (NAME, "ditulis" if APPLY else "(dry-run)"))


def register_json(path, label, root="mcpServers"):
    if not ensure_json(path, label):
        return
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return todo.append("%s: JSON rusak (%s)" % (label, e))
    servers = d.setdefault(root, {})
    if NAME in servers:
        return skip.append("%s: MCP sudah terpasang" % label)
    servers[NAME] = {"command": "python3", "args": [SCRIPT]}
    if APPLY:
        backup(path)
        json.dump(d, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    done.append("%s: MCP %s %s" % (label, NAME, "ditulis" if APPLY else "(dry-run)"))


def install_hook():
    if not os.path.exists(CLAUDE_SETTINGS):
        return todo.append("claude: settings.json tidak ada")
    try:
        d = json.load(open(CLAUDE_SETTINGS, encoding="utf-8"))
    except Exception as e:
        return todo.append("claude: settings.json rusak (%s)" % e)
    hooks = d.setdefault("hooks", {}).setdefault("SessionStart", [])
    blob = json.dumps(hooks)
    if "session-brief.sh" in blob:
        return skip.append("claude: SessionStart hook sudah ada")
    hooks.append({"hooks": [{"type": "command",
                             "command": "bash %s" % BRIEF, "timeout": 10}]})
    if APPLY:
        backup(CLAUDE_SETTINGS)
        json.dump(d, open(CLAUDE_SETTINGS, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    done.append("claude: SessionStart → session-brief.sh %s" % ("ditulis" if APPLY else "(dry-run)"))


def main():
    n_skills, n_curated, n_repos = live_numbers()
    print("angka nyata: %d skill siap pakai (%d curated) \u00b7 %d repo rujukan"
          % (n_skills, n_curated, n_repos))
    print()
    for label, mcp_path, kind, rule_path in PROVIDERS:
        if kind == "toml":
            register_codex()
        elif mcp_path:
            register_json(mcp_path, label)
        skills_dir = None
        if label in ("cline", "windsurf", "roo"):
            skills_dir = os.path.join(HOME, "." + label, "skills")
        install_rule_file(rule_path, label, n_skills, n_curated, n_repos, skills_dir)
    install_hook()
    for line in done + skip:
        print("  ok   " + line)
    for line in todo:
        print("  !!   " + line)
    print()
    print("catatan: provider yang belum punya mcp.json akan dibuatkan otomatis.")
    if not APPLY:
        print("\ndry-run \u2014 jalankan dengan --apply untuk menulis (backup otomatis).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())