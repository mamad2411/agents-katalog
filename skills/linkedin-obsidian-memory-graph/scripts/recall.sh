#!/bin/bash
# recall.sh "keyword" — lazy: index dulu, rg fallback. Max 20 hasil.
VAULT="$HOME/Documents/AgentsMemory"
Q="$1"; [ -z "$Q" ] && { echo "usage: recall.sh <keyword>"; exit 1; }
IDX="$VAULT/.index.json.gz"
if [ -f "$IDX" ]; then
  echo "== index =="
  zgrep -i -m 20 "$Q" "$IDX" 2>/dev/null | cut -c1-220
fi
echo "== files =="
command -v rg >/dev/null && RG="rg -l -i -m 5" || RG="grep -rli"
$RG "$Q" "$VAULT/LinkedIn" "$VAULT/Memory" "$VAULT/Daily" 2>/dev/null | head -n 20
