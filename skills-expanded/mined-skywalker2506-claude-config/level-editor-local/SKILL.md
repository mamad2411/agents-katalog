---
name: level-editor-local
description: "Level editor lokal sunucusu başlat ve tarayıcıda aç. Triggers: level editor local, editor local, lokal editor"
---

# /level-editor-local — Local Server

## Çalıştır

```bash
EDITOR_PAGE="editor.html"
LOCAL_PORT=8000

if [ -f "www/${EDITOR_PAGE}" ]; then
  PROJECT_DIR="$(pwd)"
elif [ -f "${HOME}/Projects/golf-paper-craft/www/${EDITOR_PAGE}" ]; then
  PROJECT_DIR="${HOME}/Projects/golf-paper-craft"
else
  echo "ERROR: editor.html bulunamadı."
  exit 1
fi

if lsof -ti:${LOCAL_PORT} > /dev/null 2>&1; then
  echo "Server already running on port ${LOCAL_PORT}"
else
  echo "Starting server at ${PROJECT_DIR}/www ..."
  python3 -m http.server ${LOCAL_PORT} --directory "${PROJECT_DIR}/www" &
  sleep 1
fi

open "http://localhost:${LOCAL_PORT}/${EDITOR_PAGE}"
```
