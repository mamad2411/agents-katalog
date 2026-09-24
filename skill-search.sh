#!/usr/bin/env bash
# skill-search.sh — cari skill di katalog ~/.agents tanpa MCP proxy (pengganti ringan
# untuk mcp-dynamic-proxy.json yang mati). Baca langsung SQLite FTS5.
#
# Pakai:
#   skill-search.sh "postgres index"
#   skill-search.sh --tier curated "vue page"
#   skill-search.sh --tier reference "mcp server"
#   skill-search.sh -p "docker"          # tampilkan path lengkap SKILL.md
#   skill-search.sh --load "playwright"  # tampilkan isi SKILL.md teratas (head 60)
set -euo pipefail

DB="$HOME/.agents/skills-index.db"
TIER=""
SHOW_PATH=0
LOAD=0

while [ $# -gt 0 ]; do
  case "$1" in
    --tier) TIER="${2:-}"; shift 2 ;;
    -p|--path) SHOW_PATH=1; shift ;;
    --load) LOAD=1; shift ;;
    *) break ;;
  esac
done

Q="${*:-}"
if [ -z "$Q" ]; then
  echo "Pakai: skill-search.sh [--tier curated|reference|docs] [-p] [--load] <kata kunci>"
  echo "Tier: curated = 3.172 skill terpilih (bisa di-invoke) | reference = punya deskripsi"
  echo "      docs = hasil scraping tanpa deskripsi (bukan skill sungguhan)"
  exit 1
fi
[ -f "$DB" ] || { echo "ERROR: $DB belum ada — jalankan: python3 ~/.agents/build_skills_index.py"; exit 1; }

# Query FTS5: OR antar token (biar kalimat natural tetap dapat hasil), + stopword,
# + fallback LIKE kalau FTS tidak kena.
STOP="yang dan dengan untuk dari pada ini itu saya mau bikin buat tambah tambahkan tolong bisa gimana cara agar supaya the and for with using use add create make new how please want need into that this from"
TERMS=""
for t in $Q; do
  t=$(printf '%s' "$t" | tr -cd 'a-zA-Z0-9._-' | tr 'A-Z' 'a-z')
  [ -z "$t" ] && continue
  case " $STOP " in *" $t "*) continue ;; esac
  if [ ${#t} -lt 3 ]; then
    case " go db ci ui ux ai ml qa js ts k8s ws api " in *" $t "*) ;; *) continue ;; esac
  fi
  [ -n "$TERMS" ] && TERMS="$TERMS OR "
  TERMS="$TERMS\"$t\"*"
done
[ -z "$TERMS" ] && { echo "Query kosong setelah sanitasi."; exit 1; }

FILTER=""
[ -n "$TIER" ] && FILTER="AND tier = '$TIER'"

if [ "$LOAD" = "1" ]; then
  P=$(sqlite3 -readonly "$DB" "SELECT path FROM skills WHERE skills MATCH '$TERMS' $FILTER ORDER BY (tier='curated') DESC LIMIT 1;")
  [ -z "$P" ] && { echo "(tidak ketemu)"; exit 1; }
  echo "== $P =="; head -60 "$P"; exit 0
fi

if [ "$SHOW_PATH" = "1" ]; then
  sqlite3 -readonly -header -column "$DB" \
    "SELECT name, tier, category, path FROM skills WHERE skills MATCH '$TERMS' $FILTER ORDER BY bm25(skills) + (CASE WHEN tier='curated' THEN 0.0 ELSE 1.5 END), name LIMIT 25;"
else
  sqlite3 -readonly -header -column "$DB" \
    "SELECT name, tier, category FROM skills WHERE skills MATCH '$TERMS' $FILTER ORDER BY bm25(skills) + (CASE WHEN tier='curated' THEN 0.0 ELSE 1.5 END), name LIMIT 25;"
fi
