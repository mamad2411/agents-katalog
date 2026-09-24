#!/bin/bash
# watcher v2: tunggu rclone copy selesai -> verifikasi ukuran -> tulis link -> buka browser
LOCAL=683671447
while pgrep -f 'rclone copy /Users/chaali0324/agents.zip' >/dev/null; do sleep 30; done
sleep 10
SIZE=$(rclone lsjson gdrive:agents --contimeout 10s --timeout 30s --retries 3 2>/dev/null | python3 -c "import json,sys
try:
    print(next((e['Size'] for e in json.load(sys.stdin) if e['Name']=='agents.zip'), ''))
except Exception: print('')")
if [ "$SIZE" = "$LOCAL" ]; then
  rclone lsjson gdrive:agents --contimeout 10s --timeout 30s --retries 3 > /tmp/agents-files.json 2>/dev/null
  rclone lsjson gdrive: --dirs-only --contimeout 10s --timeout 30s --retries 3 > /tmp/agents-dirs.json 2>/dev/null
  python3 /Users/chaali0324/.agents/upload-links.py
  echo "VERIFY-OK $(date) size=$SIZE" >> /tmp/rclone-upload2.log
  LINK=$(grep -o 'https://drive.google.com/drive/folders/[A-Za-z0-9_-]*' /Users/chaali0324/.agents/upload-links.txt | head -1)
  [ -n "$LINK" ] && open "$LINK"
else
  echo "UPLOAD-INCOMPLETE $(date) size=$SIZE" >> /tmp/rclone-upload2.log
fi
