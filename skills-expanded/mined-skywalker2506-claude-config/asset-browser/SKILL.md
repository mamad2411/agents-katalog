---
name: asset-browser
description: "Asset browser aç, güncelle veya lokal dosya yükle — Vercel URL'i aç, local dev sunucusu başlat, paket kodunu güncelle + redeploy, veya lokal PNG'leri işleyip runtime'a ekle. Triggers: asset browser aç, asset browser open, browse assets, open browser, asset browser update, browser güncelle, update browser, asset upload, lokal dosya yükle, generated assets işle"
argument-hint: "[local|online|update|upload [dir]]"
---

# /asset-browser — Aç / Güncelle / Lokal Yükle

| Argüman | Eylem |
|---------|-------|
| (yok) / `online` | Vercel canlı URL'i açar |
| `local` | Yerel dev sunucusu başlatır ve açar |
| `update` | Paketten kodu çeker, redeploy eder |
| `upload [dir]` | Lokal PNG'leri işler → WebP → runtime → missing.json approved |

## Kullanım

```
/asset-browser                        # online (varsayılan)
/asset-browser online                 # Vercel canlı
/asset-browser local                  # local dev sunucusu
/asset-browser update                 # paket güncellemesi + redeploy
/asset-browser upload                 # 07_generated_assets/ klasörünü işle (varsayılan)
/asset-browser upload path/to/dir     # belirli klasörü işle
```

## Çalıştır

```bash
ARG="${1:-online}"

# Proje tespiti — CWD veya bilinen projeler
if [ -f "asset-browser/config.json" ]; then
  PROJECT_DIR="$(pwd)"
elif [ -f "${HOME}/Projects/MedievalFactory/asset-browser/config.json" ]; then
  PROJECT_DIR="${HOME}/Projects/MedievalFactory"
elif [ -f "${HOME}/Projects/GameFactory/asset-browser/config.json" ]; then
  PROJECT_DIR="${HOME}/Projects/GameFactory"
else
  echo "ERROR: asset-browser/config.json not found. Run from project directory."
  exit 1
fi

CONFIG="${PROJECT_DIR}/asset-browser/config.json"
PKG_DIR="${HOME}/Projects/asset-browser"

# Vercel alias: title lowercase, non-alnum -> dash
TITLE=$(python3 -c "import json; c=json.load(open('${CONFIG}')); print(c['title'].lower())" 2>/dev/null)
SLUG=$(echo "$TITLE" | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
VERCEL_URL="https://asset-browser-${SLUG}.vercel.app"
LOCAL_PORT=3001

if [ "$ARG" = "update" ]; then
  # Paketi güncelle + redeploy
  echo "=== asset-browser update: $PROJECT_DIR ==="

  # 1. Paketi pull
  echo "Pulling latest package..."
  (cd "$PKG_DIR" && git pull --quiet) || echo "WARN: pkg pull failed, using local"

  # 2. Kod dosyalarını kopyala (config.json ve data/ korunur)
  echo "Copying code files..."
  cp "$PKG_DIR/api/"*.js  "$PROJECT_DIR/asset-browser/api/"
  cp "$PKG_DIR/public/index.html" "$PROJECT_DIR/asset-browser/public/"
  cp "$PKG_DIR/vercel.json" "$PROJECT_DIR/asset-browser/"
  cp "$PKG_DIR/package.json" "$PROJECT_DIR/asset-browser/"
  cp "$PKG_DIR/deploy.sh"   "$PROJECT_DIR/asset-browser/"
  chmod +x "$PROJECT_DIR/asset-browser/deploy.sh"
  [ -d "$PKG_DIR/scripts" ] && cp "$PKG_DIR/scripts/"*.mjs "$PROJECT_DIR/asset-browser/scripts/" 2>/dev/null || true

  # 3. npm install
  echo "Installing dependencies..."
  (cd "$PROJECT_DIR/asset-browser" && npm install --silent)

  # 4. Git commit
  echo "Committing..."
  (cd "$PROJECT_DIR" && \
    git add asset-browser/ && \
    git diff --cached --quiet || git commit -m "chore: sync asset-browser with latest package" && \
    git push)

  # 5. Redeploy
  echo "Deploying to Vercel..."
  (cd "$PROJECT_DIR/asset-browser" && bash deploy.sh)

  echo ""
  echo "Done! Live: $VERCEL_URL"

elif [ "$ARG" = "upload" ]; then
  # Lokal PNG'leri işle → WebP → runtime → missing.json approved
  UPLOAD_DIR="${2:-}"
  [ -z "$UPLOAD_DIR" ] && UPLOAD_DIR="${PROJECT_DIR}/07_generated_assets"
  [ ! -d "$UPLOAD_DIR" ] && { echo "ERROR: dir not found: $UPLOAD_DIR"; exit 1; }

  RUNTIME_DIR=$(python3 -c "
import json
c=json.load(open('${CONFIG}'))
src=next((s for s in c.get('sources',[]) if 'game' in s.get('category','').lower() or 'in' in s.get('category','').lower()), c.get('sources',[{}])[0])
print(src.get('dir','game/public/assets'))
" 2>/dev/null)
  RUNTIME="${PROJECT_DIR}/${RUNTIME_DIR}"
  ALIAS="https://asset-browser-${SLUG}.vercel.app"
  TMPDIR="/tmp/ab_upload_$$"
  mkdir -p "$TMPDIR"

  echo "=== asset-browser upload: $UPLOAD_DIR → $RUNTIME ==="
  APPROVED=()

  for PNG in "$UPLOAD_DIR"/*.png "$UPLOAD_DIR"/*.PNG; do
    [ -f "$PNG" ] || continue
    BASENAME=$(basename "$PNG")
    NAME="${BASENAME%.*}"
    TMPFRAMES="$TMPDIR/frames_${NAME}"
    mkdir -p "$TMPFRAMES"

    # Frame sayısını isimden çıkar (_Nf pattern)
    FRAMES=$(echo "$NAME" | grep -oE '_([0-9]+)f$' | grep -oE '[0-9]+' || echo "")

    if [ -n "$FRAMES" ]; then
      # Animasyon: magenta kaldır, frame böl, trim+center 256x256, strip birleştir
      magick "$PNG" -fuzz 35% -transparent magenta \
        -crop ${FRAMES}x1@ +repage \
        "$TMPFRAMES/f_%02d.png" 2>/dev/null

      # Siyah bg desteği (smoke vb.)
      if [ $(ls "$TMPFRAMES"/f_*.png 2>/dev/null | wc -l) -eq 0 ]; then
        magick "$PNG" -fuzz 20% -transparent black \
          -crop ${FRAMES}x1@ +repage \
          "$TMPFRAMES/f_%02d.png" 2>/dev/null
      fi

      FCOUNT=$(ls "$TMPFRAMES"/f_*.png 2>/dev/null | wc -l | tr -d ' ')
      if [ "$FCOUNT" -eq 0 ]; then
        echo "SKIP $NAME — frame split failed"
        continue
      fi

      for F in "$TMPFRAMES"/f_*.png; do
        magick "$F" -trim +repage \
          -background none -gravity center -extent 256x256 "$F" 2>/dev/null
      done

      FLIST=()
      while IFS= read -r F; do FLIST+=("$F"); done < <(ls "$TMPFRAMES"/f_*.png | sort)
      magick "${FLIST[@]}" +append "$TMPDIR/${NAME}.png"
    else
      # Statik resim: max 512px resize
      magick "$PNG" -resize '512x512>' "$TMPDIR/${NAME}.png"
    fi

    # WebP dönüşüm
    cwebp -q 90 -alpha_q 100 "$TMPDIR/${NAME}.png" -o "$TMPDIR/${NAME}.webp" -quiet 2>/dev/null
    [ ! -f "$TMPDIR/${NAME}.webp" ] && { echo "SKIP $NAME — webp failed"; continue; }

    # Runtime'a kopyala
    cp "$TMPDIR/${NAME}.webp" "$RUNTIME/${NAME}.webp"
    echo "✓ $NAME → $RUNTIME_DIR/${NAME}.webp"

    APPROVED+=("$NAME")
  done

  if [ ${#APPROVED[@]} -eq 0 ]; then
    echo "No assets processed."
    rm -rf "$TMPDIR"
    exit 0
  fi

  # missing.json'da todo olanları approved yap
  for NAME in "${APPROVED[@]}"; do
    RESP=$(curl -s -X POST "$ALIAS/api/missing-patch" \
      -H "Content-Type: application/json" \
      -d "{\"name\":\"$NAME\",\"patch\":{\"status\":\"approved\"}}" 2>/dev/null)
    echo "$NAME status: $RESP"
    sleep 0.2
  done

  # Git commit + push
  (cd "$PROJECT_DIR" && \
    git add "$RUNTIME_DIR"/ && \
    git diff --cached --quiet || \
    git commit -m "feat: approve $(echo "${APPROVED[@]}" | tr ' ' '\n' | wc -l | tr -d ' ') local assets" && \
    git push)

  rm -rf "$TMPDIR"
  echo ""
  echo "Done! ${#APPROVED[@]} asset(s) added to $RUNTIME_DIR/"

elif [ "$ARG" = "local" ]; then
  # Local dev sunucusu
  if lsof -ti:${LOCAL_PORT} > /dev/null 2>&1; then
    echo "Dev server already running on port ${LOCAL_PORT}"
  else
    echo "Starting asset-browser dev server at ${PROJECT_DIR}/asset-browser ..."
    cd "${PROJECT_DIR}/asset-browser" && npm run dev -- --port ${LOCAL_PORT} &
    sleep 2
    echo "Server started."
  fi
  LOCAL_URL="http://localhost:${LOCAL_PORT}"
  echo "Opening local asset-browser: $LOCAL_URL"
  open "$LOCAL_URL"

else
  echo "Opening asset-browser: $VERCEL_URL"
  open "$VERCEL_URL"
fi
```
