#!/bin/bash
while ! grep -q "VERIFY-OK" /tmp/rclone-upload.log 2>/dev/null; do sleep 30; done
sleep 5
rclone lsjson gdrive:agents > /tmp/agents-files.json 2>/dev/null
rclone lsjson gdrive: --dirs-only > /tmp/agents-dirs.json 2>/dev/null
python3 /Users/chaali0324/.agents/upload-links.py
LINK=$(grep -o 'https://drive.google.com/drive/folders/[A-Za-z0-9_-]*' /Users/chaali0324/.agents/upload-links.txt | head -1)
[ -n "$LINK" ] && open "$LINK"
