#!/bin/bash
# make_index.sh — rebuild .index.json.gz + 00-Index.md (1x/hari saja)
VAULT="$HOME/Documents/AgentsMemory"
mkdir -p "$VAULT/LinkedIn" "$VAULT/Memory" "$VAULT/Daily"
IDX_TMP="$VAULT/.index.json"
echo "[" > "$IDX_TMP"; FIRST=1
for f in $(find "$VAULT/LinkedIn" "$VAULT/Memory" -name "*.md" 2>/dev/null | head -n 10000); do
  rel="${f#$VAULT/}"
  title=$(head -n 30 "$f" | grep -m1 "^# " | sed 's/^# //')
  [ $FIRST -eq 0 ] && echo "," >> "$IDX_TMP"
  FIRST=0
  printf '{"path": "%s", "title": "%s"}\n' "$rel" "$title" >> "$IDX_TMP"
done
echo "]" >> "$IDX_TMP"
gzip -kf "$IDX_TMP" && rm "$IDX_TMP"
{
  echo "# Index — AgentsMemory"
  echo ""
  echo "## LinkedIn"
  for f in "$VAULT"/LinkedIn/*.md; do [ -f "$f" ] && echo "- [[$(basename "$f" .md)]]"; done
  echo ""
  echo "## Memory"
  for f in "$VAULT"/Memory/*.md; do [ -f "$f" ] && echo "- [[$(basename "$f" .md)]]"; done
} > "$VAULT/00-Index.md"
echo "index done: $(gzip -dc "$VAULT/.index.json.gz" | grep -c path) entries"
