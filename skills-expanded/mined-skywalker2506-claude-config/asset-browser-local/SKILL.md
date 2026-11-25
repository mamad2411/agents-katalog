---
name: asset-browser-local
description: "Asset browser lokal dev sunucusu başlat ve tarayıcıda aç. Triggers: asset browser local, asset browser dev, local asset browser, lokal browser"
---

# /asset-browser-local — Local Dev Server

## Çalıştır

```bash
if [ -f "asset-browser/config.json" ]; then
  PROJECT_DIR="$(pwd)"
elif [ -f "${HOME}/Projects/MedievalFactory/asset-browser/config.json" ]; then
  PROJECT_DIR="${HOME}/Projects/MedievalFactory"
elif [ -f "${HOME}/Projects/GameFactory/asset-browser/config.json" ]; then
  PROJECT_DIR="${HOME}/Projects/GameFactory"
else
  echo "ERROR: asset-browser/config.json bulunamadı."
  exit 1
fi

LOCAL_PORT=3001

if lsof -ti:${LOCAL_PORT} > /dev/null 2>&1; then
  echo "Dev server already running on port ${LOCAL_PORT}"
else
  echo "Starting dev server at ${PROJECT_DIR}/asset-browser ..."
  (cd "${PROJECT_DIR}/asset-browser" && npm run dev -- --port ${LOCAL_PORT}) &
  sleep 2
fi

open "http://localhost:${LOCAL_PORT}"
```
