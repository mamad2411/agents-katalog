---
name: asset-browser-update
description: "Asset browser paket kodunu projeye çek + redeploy. Triggers: asset browser update, browser güncelle, update asset browser, asset browser paket güncelle"
---

# /asset-browser-update — Paketi Güncelle + Redeploy

Paketten (`~/Projects/asset-browser`) en son kodu projeye çeker, bağımlılıkları yükler, commit+push ve Vercel'e redeploy eder. `config.json` ve `data/` korunur.

## Çalıştır

```bash
# Proje tespiti
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

CONFIG="${PROJECT_DIR}/asset-browser/config.json"
PKG_DIR="${HOME}/Projects/asset-browser"
TITLE=$(python3 -c "import json; c=json.load(open('${CONFIG}')); print(c['title'].lower())" 2>/dev/null)
SLUG=$(echo "$TITLE" | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
VERCEL_URL="https://asset-browser-${SLUG}.vercel.app"

echo "=== asset-browser update: $PROJECT_DIR ==="

echo "Pulling latest package..."
(cd "$PKG_DIR" && git pull --quiet) || echo "WARN: pkg pull failed"

echo "Copying code files..."
cp "$PKG_DIR/api/"*.js "$PROJECT_DIR/asset-browser/api/"
cp "$PKG_DIR/public/index.html" "$PROJECT_DIR/asset-browser/public/"
cp "$PKG_DIR/vercel.json" "$PROJECT_DIR/asset-browser/"
cp "$PKG_DIR/package.json" "$PROJECT_DIR/asset-browser/"
cp "$PKG_DIR/deploy.sh" "$PROJECT_DIR/asset-browser/"
chmod +x "$PROJECT_DIR/asset-browser/deploy.sh"
[ -d "$PKG_DIR/scripts" ] && cp "$PKG_DIR/scripts/"*.mjs "$PROJECT_DIR/asset-browser/scripts/" 2>/dev/null || true

echo "Installing dependencies..."
(cd "$PROJECT_DIR/asset-browser" && npm install --silent)

echo "Committing..."
(cd "$PROJECT_DIR" && \
  git add asset-browser/ && \
  git diff --cached --quiet || git commit -m "chore: sync asset-browser with latest package" && \
  git push)

echo "Deploying to Vercel..."
(cd "$PROJECT_DIR/asset-browser" && bash deploy.sh)

echo ""
echo "Done! Live: $VERCEL_URL"
```
