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
print("Katalog %d skill curated: skill_for_task/skill_search; muat ringkas: bash ~/.agents/skill-load-lite.sh <nama>."
      % d.get("total_curated", 0))
print("")
print("## Anti-ngarang (ringkas)")
print("Klaim wajib sebut sumber (skill/MCP/file+baris); DILARANG menulis angka dari ingatan; file .md baru wajib ada '## Sumber'.")
print("Sumber primer tak terjangkau → BERHENTI + tanya user (jangan nebak). Skill belum ada → MINER_LIMIT=120 python3 ~/.agents/skill-miner.py")
print("MCP aktif: skill-catalog + mcp-router (2); lainnya diparkir di mcp-parked.json → python3 ~/.agents/mcp-lifecycle.py --on <nama>")
try:
    import subprocess
    subprocess.run(["python3", os.path.expanduser("~/.agents/mcp-lifecycle.py"), "--gc-if-due", "14"],
                   capture_output=True, timeout=30)  # ringan: cek murah, GC beneran maks 1x/minggu
    subprocess.run(["python3", os.path.expanduser("~/.agents/archive-sessions.py")],
                   capture_output=True, timeout=60)  # arsip sesi >7 hari, maks 1x/minggu, sunyi
except Exception:
    pass
PY
