---
name: level-editor
description: "Level editor aç veya güncelle — yerel sunucu başlat, Vercel online versiyonunu aç, veya canvas-level-editor paketini güncelle. Triggers: level editor, editör aç, editor open, online editor, vercel editor, level editor update, editor güncelle, update editor"
argument-hint: "[local|online|update]"
---

# /level-editor — Level Editor'ı Aç / Güncelle

| Argüman | Eylem |
|---------|-------|
| (yok) / `local` | Yerel sunucu başlatır ve açar |
| `online` | Vercel canlı URL'i açar |
| `update` | Paketten kodu çeker, commit eder |

## Kullanım

```
/level-editor          # local (varsayılan)
/level-editor local    # local sunucu
/level-editor online   # Vercel canlı
/level-editor update   # paket güncellemesi
```

## Çalıştır

```bash
ARG="${1:-local}"
EDITOR_PAGE="editor.html"
VERCEL_URL="https://golf-paper-craft.vercel.app/${EDITOR_PAGE}"
LOCAL_PORT=8000
PKG_DIR="${HOME}/Projects/canvas-level-editor"

# Proje tespiti
if [ -f "www/${EDITOR_PAGE}" ]; then
  PROJECT_DIR="$(pwd)"
elif [ -f "${HOME}/Projects/golf-paper-craft/www/${EDITOR_PAGE}" ]; then
  PROJECT_DIR="${HOME}/Projects/golf-paper-craft"
else
  PROJECT_DIR=""
fi

if [ "$ARG" = "online" ]; then
  echo "Opening online editor: $VERCEL_URL"
  open "$VERCEL_URL"

elif [ "$ARG" = "update" ]; then
  [ -z "$PROJECT_DIR" ] && { echo "ERROR: project not found."; exit 1; }
  SUBDIR="tools/canvas-level-editor"
  DEST="$PROJECT_DIR/$SUBDIR"
  [ ! -d "$DEST" ] && { echo "ERROR: canvas-level-editor not installed at $DEST"; exit 1; }

  echo "=== canvas-level-editor update: $PROJECT_DIR ==="

  # 1. Paketi pull
  echo "Pulling latest package..."
  (cd "$PKG_DIR" && git pull --quiet) || echo "WARN: pkg pull failed, using local"

  # 2. Kod dosyalarını kopyala
  echo "Copying code files..."
  cp "$PKG_DIR/editor-core.js"  "$DEST/"
  cp "$PKG_DIR/editor-core.css" "$DEST/"

  # 3. Git commit
  echo "Committing..."
  (cd "$PROJECT_DIR" && \
    git add "$SUBDIR/" && \
    git diff --cached --quiet || git commit -m "chore: sync canvas-level-editor with latest package" && \
    git push)

  echo ""
  echo "Done! Restart local server to see changes."

else
  [ -z "$PROJECT_DIR" ] && { echo "ERROR: editor.html not found. Run from project directory."; exit 1; }

  if lsof -ti:${LOCAL_PORT} > /dev/null 2>&1; then
    echo "Server already running on port ${LOCAL_PORT}"
  else
    echo "Starting server at ${PROJECT_DIR}/www ..."
    python3 -m http.server ${LOCAL_PORT} --directory "${PROJECT_DIR}/www" &
    sleep 1
    echo "Server started."
  fi

  LOCAL_URL="http://localhost:${LOCAL_PORT}/${EDITOR_PAGE}"
  echo "Opening local editor: $LOCAL_URL"
  open "$LOCAL_URL"
fi
```
