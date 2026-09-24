#!/bin/bash
# save.sh "Judul" "tag1,tag2" "isi singkat" [subdir]
VAULT="$HOME/Documents/AgentsMemory"
SUB="${4:-Memory}"
DATE=$(date +%Y-%m-%d); TS=$(date +%Y%m%d-%H%M%S)
SLUG=$(echo "$1" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | cut -c1-40)
DIR="$VAULT/$SUB"; mkdir -p "$DIR" "$VAULT/Daily"
FILE="$DIR/$DATE-$SLUG.md"
TAGS=$(echo "$2" | sed 's/,/, /g')
cat > "$FILE" <<EOF
---
id: $TS
created: $(date +%Y-%m-%dT%H:%M:%S%z)
tags: [$TAGS]
links: ["[[00-Index]]"]
score: 1.0
source: chat
---

# $1

$3
EOF
DAILY="$VAULT/Daily/$DATE.md"
[ -f "$DAILY" ] || echo -e "# $DATE\n" > "$DAILY"
echo "- [[$(basename "$FILE" .md)]] — $1" >> "$DAILY"
echo "saved: $FILE"
