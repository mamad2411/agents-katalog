#!/usr/bin/env bash
# wire-skills-role.sh — "role pack": tautkan HANYA skill relevan ke sebuah repo
# (symlink relatif, portable) supaya konteks sesi lebih ramping & tetap pintar.
#
# Kenapa: 82 skill ter-link di scope project = 82 deskripsi skill ikut ke konteks.
# Repo Vue+Go tidak butuh skill blockchain/game/mobile. Preset di bawah memilih
# skill dari DB katalog (tier=curated, kolom category) — bukan dari role-skill-map.json
# (file itu berisi nama tier expanded yg banyak sampah).
#
# Pakai:
#   bash ~/.agents/wire-skills-role.sh --list
#   bash ~/.agents/wire-skills-role.sh backend /path/ke/repo          # dry-run
#   bash ~/.agents/wire-skills-role.sh backend /path/ke/repo --apply  # tulis symlink
#   CAP_PER_KAT=8 bash ~/.agents/wire-skills-role.sh fullstack /repo --apply
#
# Aman: TIDAK menghapus apa pun; yang sudah ada (file/folder/symlink lain) dibiarkan.
set -uo pipefail

AG="${HOME}/.agents"
DB="${AG}/skills-index.db"
STORE="${AG}/skills-store"
CAP_PER_KAT="${CAP_PER_KAT:-10}"

preset_cats() {
  case "$1" in
    backend)    echo "backend-developer devops-engineer security-specialist" ;;
    frontend)   echo "frontend-developer designer qa-engineer" ;;
    fullstack)  echo "backend-developer frontend-developer devops-engineer qa-engineer" ;;
    data)       echo "data-scientist data-engineer analyst" ;;
    ai)         echo "ai-engineer agent-orchestrator agent-memory agent-ux data-scientist" ;;
    agent)      echo "agent-orchestrator agent-memory agent-ux ai-engineer" ;;
    design)     echo "designer creative-producer frontend-developer" ;;
    qa)         echo "qa-engineer devtools-engineer security-specialist" ;;
    devops)     echo "devops-engineer security-specialist backend-developer" ;;
    security)   echo "security-specialist backend-developer devops-engineer" ;;
    mobile)     echo "mobile-developer frontend-developer" ;;
    docs)       echo "tech-writer product-manager" ;;
    core)       echo "backend-developer frontend-developer qa-engineer" ;;
    *) return 1 ;;
  esac
}

if [ "${1:-}" = "--list" ]; then
  echo "preset → kategori curated (cap ${CAP_PER_KAT}/kategori):"
  for p in backend frontend fullstack data ai agent design qa devops security mobile docs core; do
    cats=$(preset_cats "$p")
    tot=0
    for c in $cats; do
      n=$(sqlite3 -readonly "$DB" "SELECT COUNT(*) FROM skills WHERE tier='curated' AND category='$c';")
      [ "${n:-0}" -gt "$CAP_PER_KAT" ] && n=$CAP_PER_KAT
      tot=$((tot + n))
    done
    printf '  %-11s %-52s ±%s skill\n' "$p" "$cats" "$tot"
  done
  echo
  echo "pakai: bash ~/.agents/wire-skills-role.sh <preset> <repo> [--apply]"
  exit 0
fi

PRESET="${1:-}"; REPO="${2:-}"; APPLY=0
[ "${3:-}" = "--apply" ] && APPLY=1
if [ -z "$PRESET" ] || [ -z "$REPO" ]; then
  sed -n '2,18p' "$0"; exit 2
fi
CATS=$(preset_cats "$PRESET") || { echo "preset tidak dikenal: $PRESET (lihat --list)"; exit 1; }
[ -d "$REPO" ] || { echo "ERROR: $REPO bukan folder"; exit 1; }
[ -d "$STORE" ] && [ -f "$DB" ] || { echo "ERROR: katalog tidak ada ($DB)"; exit 1; }

DEST="$REPO/.claude/skills"
[ "$APPLY" = 1 ] && mkdir -p "$DEST"

echo "preset=$PRESET | repo=$REPO | mode=$([ "$APPLY" = 1 ] && echo APPLY || echo dry-run)"
n_selected=0; n_linked=0; n_skip=0
for c in $CATS; do
  names=$(sqlite3 -readonly "$DB" \
    "SELECT name FROM skills WHERE tier='curated' AND category='$c' ORDER BY name LIMIT $CAP_PER_KAT;")
  for n in $names; do
    src="$STORE/$n"
    [ -d "$src" ] || continue
    n_selected=$((n_selected + 1))
    dst="$DEST/$n"
    if [ -L "$dst" ]; then n_skip=$((n_skip + 1)); continue; fi
    if [ -e "$dst" ]; then n_skip=$((n_skip + 1)); continue; fi
    if [ "$APPLY" = 1 ]; then
      # path relatif HARUS dihitung dari lokasi tujuan (repo bisa di mana saja);
      # hardcode "../../../.agents/..." SALAH kecuali repo tepat 3 level di bawah $HOME.
      rel=$(python3 -c "
import os,sys
src=os.path.realpath(sys.argv[1]); dst=os.path.realpath(sys.argv[2])
r=os.path.relpath(src,dst)
print(r if r.count('..')<=6 else src)" "$src" "$DEST")
      ln -s "$rel" "$dst" && n_linked=$((n_linked + 1))
    else
      echo "  + $n"
    fi
  done
done
echo "skill terpilih: $n_selected | baru ditautkan: $n_linked | dilewati (sudah ada): $n_skip"
[ "$APPLY" = 1 ] || echo "jalankan ulang dengan --apply untuk menulis symlink."