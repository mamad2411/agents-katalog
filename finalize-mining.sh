#!/bin/bash
# finalize-mining.sh — tunggu miner selesai, lalu rebuild index + laporkan angka.
# Aman dijalankan berkali-kali; keluar sendiri kalau tidak ada miner.
cd "$HOME/.agents" || exit 1

while pgrep -f "mine-domains.py|mine-agent-assets.py" >/dev/null 2>&1; do
  sleep 300
done

echo "=== miner selesai $(date '+%Y-%m-%d %H:%M') ===" >> mine-final.log

# scan ulang SELURUH hasil mining sebelum masuk index
/usr/bin/grep -rlE 'L2Jpbi9iYXNoIC1jIC|91\.92\.242\.30|54\.91\.154\.110|6x8c0trkp4l9uugo|swcdn\.apple\.com[^\n]{0,80}\| *base64|base64 *(-D|--decode) *\| *(ba)?sh|/dev/tcp/|nc -e /bin|bash -i >&' \
  skills-expanded/mined-* agent-assets 2>/dev/null > scan-final.txt
echo -n "SCAN_HITS=" >> mine-final.log
wc -l < scan-final.txt >> mine-final.log

taskpolicy -b nice -n 19 python3 build_skills_index.py >> mine-final.log 2>&1
taskpolicy -b nice -n 19 python3 build-retrieve-index.py >> mine-final.log 2>&1
{
  echo -n "SKILLS="
  sqlite3 skills-index.db "select count(*) from skills"
  echo -n "ASSETS="
  sqlite3 retrieve.db "select count(*) from assets"
  echo -n "BLOCKED="
  cat domain-blocked-files.jsonl asset-blocked-files.jsonl 2>/dev/null | wc -l
} >> mine-final.log
echo "=== selesai $(date '+%H:%M') ===" >> mine-final.log
