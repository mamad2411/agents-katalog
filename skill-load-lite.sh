#!/usr/bin/env bash
# skill-load-lite.sh — ambil skill TANPA membanjiri konteks.
#
# Masalah: `cat SKILL.md` bisa 3–15 KB (±1–4 rb token) per skill; beberapa skill
# sekaligus = konteks meledak. Skrip ini mencetak bagian ESENSIAL saja
# (frontmatter + N baris awal, maksimum B byte) sehingga skill tetap dipakai,
# tapi hemat 5–8× dibanding membaca penuh.
#
# Pakai:
#   bash ~/.agents/skill-load-lite.sh <nama-skill>              # 80 baris / 2 KB
#   bash ~/.agents/skill-load-lite.sh <nama> --lines 40         # lebih ringkas
#   bash ~/.agents/skill-load-lite.sh <nama> --bytes 4096       # lebih longgar
#   bash ~/.agents/skill-load-lite.sh <nama> --full             # baca penuh (sadar biaya)
#   bash ~/.agents/skill-load-lite.sh --list "<kata kunci>"     # kandidat dulu, baru muat
#
# Sumber tunggal: ~/.agents/skills-store/<nama>/SKILL.md (AGENTS.md §aturan keras).
set -uo pipefail

AG="${HOME}/.agents"
STORE="${AG}/skills-store"
LINES=80
BYTES=2048
FULL=0
NAME=""
KEY=""

while [ $# -gt 0 ]; do
  case "$1" in
    --lines) LINES="${2:?}"; shift 2 ;;
    --bytes) BYTES="${2:?}"; shift 2 ;;
    --full)  FULL=1; shift ;;
    --list)  KEY="${2:?}"; shift 2 ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) [ -z "$NAME" ] && NAME="$1"; shift ;;
  esac
done

if [ -n "$KEY" ]; then
  # Cukup cetak 5 kandidat (nama + 1 baris), bukan seluruh katalog.
  bash "${AG}/skill-search.sh" --tier curated "$KEY" 2>/dev/null | head -5
  echo "(muat: bash ~/.agents/skill-load-lite.sh <nama>)"
  exit 0
fi

[ -n "$NAME" ] || { echo "Pakai: skill-load-lite.sh <nama-skill> [--lines N] [--bytes N] [--full]" >&2; exit 2; }

P=""
for c in "${STORE}/${NAME}/SKILL.md" "${HOME}/.claude/skills/${NAME}/SKILL.md" "${AG}/skills/${NAME}/SKILL.md"; do
  [ -f "$c" ] && { P="$c"; break; }
done
if [ -z "$P" ]; then
  echo "Skill '$NAME' tidak ada di skills-store. Cari dulu:" >&2
  bash "${AG}/skill-search.sh" --tier curated "$NAME" 2>/dev/null | head -5 >&2
  exit 1
fi

TOTAL=$(wc -c < "$P" | tr -d ' ')
if [ "$FULL" = "1" ]; then
  cat "$P"
  exit 0
fi

head -n "$LINES" "$P" | head -c "$BYTES"
CUT=$(head -n "$LINES" "$P" | head -c "$BYTES" | wc -c | tr -d ' ')
echo
echo "[lite] ${P} — ${CUT}B dari ${TOTAL}B"
echo "[lite] perlu detail? baca baris spesifik: sed -n 'A,Bp' ${P}"
