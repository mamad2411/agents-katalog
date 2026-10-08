#!/bin/bash
# legakan.sh — 1x klik: matikan renderer hantu, flush cache aman, lapor.
# Otomatis: jalan tiap 30 menit via launchd (Nice 19, beban ~0%).
# Manual: ~/.agents/skills/device-cool/scripts/legakan.sh

# 0. Rotasi log (launchd menulis append; kalau >500 KB → arsipkan & kosongkan)
LOG=/tmp/legakan.log
if [ -f "$LOG" ] && [ "$(stat -f%z "$LOG" 2>/dev/null || echo 0)" -gt 512000 ]; then
  cp "$LOG" "$LOG.1" 2>/dev/null && : > "$LOG"   # copy+truncate: launchd fd tetap ke inode yang sama
fi

# 1. Kill helper hantu (CPU >100% lebih dari 1 proses sama = 1 dibiarkan, sisanya kill)
for app in "CodeBuddy Helper (Renderer)" "Trae Helper (Renderer)"; do
  pids=$(ps -ax -o pid,%cpu,comm | grep -F "$app" | grep -v grep | sort -rn -k2 | awk '{print $1}')
  n=$(echo "$pids" | grep -c . 2>/dev/null)
  if [ "$n" -gt 2 ]; then
    echo "$app: $n proses, kill sisanya..."
    echo "$pids" | tail -n +3 | xargs kill 2>/dev/null
  fi
done

# 2. Flush cache aman (sama kayak clean.sh, versi cepat)
rm -rf ~/Library/Caches/pip/* ~/.npm/_cacache/tmp* ~/.cache/pip/* 2>/dev/null
find /tmp -user "$USER" -mtime +3 -delete 2>/dev/null
rm -rf ~/Documents/AgentsMemory/.obsidian/cache/* 2>/dev/null

# 3. Lapor singkat
echo "--- CPU TOP5 ---"
ps -ax -o %cpu,comm | sort -rn | head -n 5
echo "--- RAM free ---"
vm_stat | grep -E "free|inactive" | head -n 3
echo "--- DISK ---"
df -h ~ | tail -n 1
echo "legakan done: $(date '+%H:%M')"
