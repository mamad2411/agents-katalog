#!/usr/bin/env bash
# topic-chain.sh — topic-mine -> rebuild -> regenerate -> lapor. Hemat panas (nice).
set -uo pipefail
A="$HOME/.agents"
export GH_TOKEN="$(gh auth token 2>/dev/null)"
nice -n 15 python3 "$A/topic-mine.py" --pages 5 2>&1 | tail -6
nice -n 15 python3 "$A/build_skills_index.py" 2>&1 | tail -6
nice -n 15 python3 "$A/skills-index-md.py" 2>&1 | tail -2
nice -n 15 python3 "$A/skills-router.py" 2>&1 | tail -2
python3 "$A/topic-report.py" 2>&1 | tail -8