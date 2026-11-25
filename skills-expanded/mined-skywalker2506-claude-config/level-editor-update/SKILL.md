---
name: level-editor-update
description: "Canvas level editor paket kodunu projeye çek + commit. Triggers: level editor update, editor güncelle, update level editor, canvas editor güncelle"
---

# /level-editor-update — Paketi Güncelle

Paketten (`~/Projects/canvas-level-editor`) en son `editor-core.js` ve `editor-core.css` dosyalarını projeye çeker, commit+push eder.

## Çalıştır

```bash
PKG_DIR="${HOME}/Projects/canvas-level-editor"
EDITOR_PAGE="editor.html"

if [ -f "www/${EDITOR_PAGE}" ]; then
  PROJECT_DIR="$(pwd)"
elif [ -f "${HOME}/Projects/golf-paper-craft/www/${EDITOR_PAGE}" ]; then
  PROJECT_DIR="${HOME}/Projects/golf-paper-craft"
else
  echo "ERROR: project bulunamadı."
  exit 1
fi

SUBDIR="tools/canvas-level-editor"
DEST="$PROJECT_DIR/$SUBDIR"
[ ! -d "$DEST" ] && { echo "ERROR: canvas-level-editor not installed at $DEST"; exit 1; }

echo "=== canvas-level-editor update: $PROJECT_DIR ==="

(cd "$PKG_DIR" && git pull --quiet) || echo "WARN: pkg pull failed"

cp "$PKG_DIR/editor-core.js"  "$DEST/"
cp "$PKG_DIR/editor-core.css" "$DEST/"

(cd "$PROJECT_DIR" && \
  git add "$SUBDIR/" && \
  git diff --cached --quiet || git commit -m "chore: sync canvas-level-editor with latest package" && \
  git push)

echo ""
echo "Done! Restart local server to see changes."
```
