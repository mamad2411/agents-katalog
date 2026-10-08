#!/usr/bin/env bash
# skillsh-fullpass.sh — FULL pass skills.sh (20.000 entri) dengan checkpoint resume.
# Loop chunk 400 entri; simpan offset ke ~/.agents/.skillsh-progress;
# sleep 15 detik antar chunk (hemat & hormati raw.githubusercontent).
set -uo pipefail
A="$HOME/.agents"
PROG="$A/.skillsh-progress"
LOG=/tmp/skillsh-fullpass.log
CHUNK="${CHUNK:-400}"
[ -f "$PROG" ] || echo 0 > "$PROG"

while :; do
  OFF=$(cat "$PROG" 2>/dev/null || echo 0)
  [ "$OFF" -ge 20000 ] && { echo "=== SELESAI semua entri (offset $OFF) ==="; break; }
  echo "### chunk offset=$OFF limit=$CHUNK $(date -u +%FT%TZ)"
  python3 -u "$A/skill-miner-skillsh.py" --offset "$OFF" --limit "$CHUNK" 2>&1 | tail -2
  echo "$((OFF + CHUNK))" > "$PROG"
  sleep 15
done
