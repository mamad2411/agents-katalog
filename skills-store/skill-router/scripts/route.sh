#!/bin/bash
# route.sh "kata kunci" — cari skill cocok: graph-api dulu, folder fallback.
Q="$1"; [ -z "$Q" ] && { echo "kasih kata kunci"; exit 1; }
echo "== graph-api =="
curl -s --max-time 5 "http://127.0.0.1:27125/search?q=$(echo "$Q" | sed 's/ /%20/g')" 2>/dev/null | head -c 1000; echo
echo "== folder =="
ls ~/.agents/skills-store/ 2>/dev/null | grep -i "$(echo "$Q" | tr ' ' '\n' | head -n 1)" | head -n 10
