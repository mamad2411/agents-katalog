#!/bin/bash
# chain v4: zip visible-root -> upload -> verifikasi -> tulis link -> buka browser
LOG=/tmp/upload-v4.log
mkdir -p /tmp/agentszipview
ln -sfn /Users/chaali0324/.agents /tmp/agentszipview/agents
rm -f /Users/chaali0324/agents-backup.zip
cd /tmp/agentszipview
zip -r -1 -q /Users/chaali0324/agents-backup.zip agents -x '*.DS_Store'
echo "ZIP-DONE $(date)" >> $LOG
LOCAL=$(stat -f %z /Users/chaali0324/agents-backup.zip)
echo "local size: $LOCAL" >> $LOG
rclone copy /Users/chaali0324/agents-backup.zip gdrive:agents/ --log-level INFO --stats-one-line --stats 60s --drive-chunk-size 128M --tpslimit 5 --retries 5 --low-level-retries 10 --log-file /tmp/rclone-upload3.log
sleep 10
SIZE=$(rclone lsjson gdrive:agents --contimeout 10s --timeout 30s --retries 3 2>/dev/null | python3 -c "import json,sys
try:
    print(next((e['Size'] for e in json.load(sys.stdin) if e['Name']=='agents-backup.zip'), ''))
except Exception: print('')")
echo "drive size: $SIZE" >> $LOG
if [ "$SIZE" = "$LOCAL" ] && [ -n "$SIZE" ]; then
  FID=$(rclone lsjson gdrive:agents --contimeout 10s --timeout 30s --retries 3 2>/dev/null | python3 -c "import json,sys
print(next(e['ID'] for e in json.load(sys.stdin) if e['Name']=='agents-backup.zip'))" 2>/dev/null)
  DID=$(rclone lsjson gdrive: --dirs-only --contimeout 10s --timeout 30s --retries 3 2>/dev/null | python3 -c "import json,sys
print(next(e['ID'] for e in json.load(sys.stdin) if e['Name']=='agents'))" 2>/dev/null)
  {
    echo "Folder  : https://drive.google.com/drive/folders/$DID"
    echo "File    : https://drive.google.com/file/d/$FID/view"
    echo "Download: https://drive.google.com/uc?export=download&id=$FID"
    echo "VERIFY-OK $(date) size=$SIZE (root visible: agents/)"
  } > /Users/chaali0324/.agents/upload-links.txt
  echo "LINKS-WRITTEN $(date)" >> $LOG
  open "https://drive.google.com/drive/folders/$DID" 2>/dev/null || true
else
  echo "UPLOAD-INCOMPLETE $(date)" >> $LOG
fi
