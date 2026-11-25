#!/usr/bin/env bash
# memory-recall.sh — SessionStart hook: suntik memori lintas sesi (≤1200 char).
# Sumber: ~/.agents/memory/MEMORY.md + sesi terakhir + memori proyek. 0 token kalau kosong.
python3 "$HOME/.agents/memory-store.py" recall --project "${CLAUDE_PROJECT_DIR:-$PWD}" 2>/dev/null
exit 0
