---
name: asset-browser-online
description: "Asset browser Vercel canlı URL'ini tarayıcıda aç. Triggers: asset browser online, asset browser vercel, online asset browser, canlı browser"
---

# /asset-browser-online — Vercel Canlı URL

## Çalıştır

```bash
if [ -f "asset-browser/config.json" ]; then
  CONFIG="$(pwd)/asset-browser/config.json"
elif [ -f "${HOME}/Projects/MedievalFactory/asset-browser/config.json" ]; then
  CONFIG="${HOME}/Projects/MedievalFactory/asset-browser/config.json"
elif [ -f "${HOME}/Projects/GameFactory/asset-browser/config.json" ]; then
  CONFIG="${HOME}/Projects/GameFactory/asset-browser/config.json"
else
  echo "ERROR: asset-browser/config.json bulunamadı."
  exit 1
fi

TITLE=$(python3 -c "import json; c=json.load(open('${CONFIG}')); print(c['title'].lower())" 2>/dev/null)
SLUG=$(echo "$TITLE" | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
VERCEL_URL="https://asset-browser-${SLUG}.vercel.app"

echo "Opening: $VERCEL_URL"
open "$VERCEL_URL"
```
