#!/usr/bin/env bash
# session-brief.sh — digest sesi versi RINGKAS (progressive disclosure).
# Dulu 19 baris/~1.2 KB tiap sesi → AI merasa berat; kini ~9 baris/~700 B.
# Detail protokol TIDAK di-inject: dibaca on-demand dari ~/.agents/SKILL-FIRST.md.
# Output = teks polos. Aman: tidak menulis apa pun, cepat (<1s).
set -uo pipefail

AG="$HOME/.agents"
J="$AG/skills-index.json"

if [ ! -f "$J" ]; then
  echo "[skills] katalog belum dibangun — jalankan: python3 ~/.agents/skills-router.py"
  exit 0
fi

python3 - "$J" <<'PY'
import json, os, sys, re, glob
j = sys.argv[1]
d = json.load(open(j))
print("## Auto-Skill (MANDIRI — tanpa harus diminta user)")
print("%d skill siap pakai (curated %d) di ~/.agents — SEBELUM kerja apa pun: skill_for_task(\"<tugas>\"); cocok → skill_load & ikuti."
      % (d.get("tier1_count", 0), d.get("total_curated", 0)))
print("DEFAULT: jawaban hemat token (caveman-token-optimizer / token-budget-advisor) · UI/design → self-check anti-ui-slop + de-sloppify.")
print("Skill mined punya REPO-REF.md (repo sumber) untuk telusuri workflow/struktur. Tak ada skill cocok → kerja dari nol; berulang → usulkan SKILL.md baru.")
print("")
print("## Anti-ngarang (ringkas)")
print("Klaim wajib sebut sumber (skill/MCP/file+baris); DILARANG menulis angka dari ingatan; file .md baru wajib ada '## Sumber'.")
print("Sumber primer tak terjangkau → BERHENTI + tanya user (jangan nebak). Skill belum ada → MINER_LIMIT=120 python3 ~/.agents/skill-miner.py")
cfg = os.path.expanduser("~/.codex/config.toml")
n = 0
if os.path.exists(cfg):
    with open(cfg, errors="ignore") as f:
        n = len(set(re.findall(r"^\[mcp_servers\.([^\.\]]+)", f.read(), re.M)))
for jf in glob.glob(os.path.expanduser("~/.*/mcp.json")) + [os.path.expanduser("~/.claude.json")]:
    try:
        n += len(json.load(open(jf)).get("mcpServers", {}))
    except Exception:
        pass
print("MCP: %d server terdaftar (semua provider) · nyala-mati: python3 ~/.agents/mcp-lifecycle.py" % n)
try:
    import subprocess
    subprocess.run(["python3", os.path.expanduser("~/.agents/mcp-lifecycle.py"), "--gc-if-due", "14"],
                   capture_output=True, timeout=30)  # ringan: cek murah, GC beneran maks 1x/minggu
except Exception:
    pass
PY
