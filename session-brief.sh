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
print("Katalog %d skill (%d curated + %d reference): cari via skill_for_task/skill_search, muat ≤2 via skill_load/skill-load-lite.sh."
      % (d.get("total_curated", 0) + d.get("total_reference", 0), d.get("total_curated", 0), d.get("total_reference", 0)))
print("")
print("## Anti-ngarang (ringkas)")
print("Klaim wajib sebut sumber (skill/MCP/file+baris); DILARANG menulis angka dari ingatan; file .md baru wajib ada '## Sumber'.")
print("Sumber primer tak terjangkau → BERHENTI + tanya user (jangan nebak). Skill belum ada → MINER_LIMIT=120 python3 ~/.agents/skill-miner.py")
print("MCP: skill-catalog + mcp-router (survivor); butuh lain -> mcp_use via mcp-router (on-demand, mati 300s idle).")
try:
    import subprocess
    subprocess.run(["python3", os.path.expanduser("~/.agents/mcp-lifecycle.py"), "--gc-if-due", "14"],
                   capture_output=True, timeout=10)  # murah: skip kalau baru jalan <14 hari
except Exception:
    pass
PY
