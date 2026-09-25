#!/usr/bin/env bash
# mine-to-100k.sh — orchestrasi penambahan skill toward 100k, DENGAN security gate.
#
# Alur per batch:
#   1. mine (skills-expanded = tier reference, belum native-wired -> kuarsa alami)
#   2. scan delta (skill-sec-scan.py --since <tanggal batch>) -> security-scan file
#   3. rebuild index (build_skills_index.py) supaya entry baru terdaftar
#
# PENTING:
#   * butuh GH_TOKEN (gratis) untuk 5.000 req/jam. Tanpa: 60/jam = ~43 jam.
#   * registry miner: REG_MIN_STARS=0 (semua repo) — handalan stars>=100 hanya 47 repo,
#     tidak akan mencapai 100k. Ini menaikkan VOLUME konten tak-terawat (kwuarsa lewat scan).
#   * TIDAK ada file dihapus. Semua bisa dibalik.
#
# Pakai: bash ~/.agents/mine-to-100k.sh [batch_ke] [max_repo] [limit_per_repo]
set -uo pipefail
A="$HOME/.agents"
cd "$A" || exit 1

BATCH="${1:-1}"
MAXREPO="${2:-600}"
LIMITPP="${3:-80}"
LOGDIR="/tmp/mine100k"
mkdir -p "$LOGDIR"
LOG="$LOGDIR/batch-$BATCH.log"
DAY="$(date -u +%Y%m%d)"

if [ -z "${GH_TOKEN:-}" ]; then
  echo "PERINGATAN: GH_TOKEN kosong -> limit GitHub 60 req/jam, akan sangat lambat." >&2
fi

{
  echo "=== BATCH $BATCH mulai $(date -u +%FT%TZ) ==="
  echo "registry: stars>=0 max_repo=$MAXREPO limit/repo=$LIMITPP"

  echo "--- 1. MINE ---"
  REG_MIN_STARS=0 REG_MAX_REPOS="$MAXREPO" REG_LIMIT_PER_REPO="$LIMITPP" \
    python3 "$A/skill-miner.py" --registry 2>&1 | tail -20

  echo "--- 2. SCAN DELTA (mulai $DAY) ---"
  python3 "$A/skill-sec-scan.py" --since "$DAY" 2>&1 | tail -12

  echo "--- 3. REBUILD INDEX ---"
  python3 "$A/build_skills_index.py" 2>&1 | tail -8

  echo "--- 4. TOTAL ---"
  python3 - <<'PY'
import sqlite3, os
db = os.path.expanduser("~/.agents/skills-index.db")
try:
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    tot = c.execute("select count(*) from skills").fetchone()[0]
    print("TOTAL index:", tot, "| target 100k | kurang:", max(0, 100000 - tot))
    for t, n in c.execute("select tier,count(*) from skills group by tier order by 2 desc"):
        print(f"  {t}: {n}")
except Exception as e:
    print("index belum ada:", e)
PY
  echo "=== BATCH $BATCH selesai $(date -u +%FT%TZ) ==="
} >> "$LOG" 2>&1

tail -30 "$LOG"
echo "log: $LOG"
