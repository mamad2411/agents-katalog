#!/usr/bin/env bash
# mine-daemon.sh — daemon mining menuju 100k, jalan di tmux (terlepas dari terminal).
#
# Pakai: bash ~/.agents/mine-daemon.sh start|stop|status
#
# Kenapa tmux: mining butuh BERJAM-JAM. Di shell biasa proses ikut mati saat
# terminal ditutup. tmux membuat proses self-detached.
#
# Loop: mine -> scan delta -> rebuild index -> cek total -> ulangi sampai 100k.
# Rate limit GitHub: 60/jam tanpa GH_TOKEN (lambat), 5000/jam dengan token.
set -uo pipefail
A="$HOME/.agents"
SESSION="mine100k"
LOGDIR="/tmp/mine100k"
mkdir -p "$LOGDIR"
TARGET=100000
MAX_BATCHES="${MAX_BATCHES:-8}"
MAXREPO="${MAXREPO:-600}"
LIMITPP="${LIMITPP:-80}"
BATCH="${START_BATCH:-1}"

worker() {
  # pastikan token diteruskan ke subprocess miner (tmux tidak mewarisi env shell pemanggil)
  if [ -n "${GH_TOKEN:-}" ]; then export GH_TOKEN; fi
  while [ "$BATCH" -le "$MAX_BATCHES" ]; do
    echo "########## BATCH $BATCH mulai $(date -u +%FT%TZ) ##########"
    bash "$A/mine-to-100k.sh" "$BATCH" "$MAXREPO" "$LIMITPP"
    TOT=$(python3 -c "
import sqlite3, os
db = os.path.expanduser('~/.agents/skills-index.db')
try:
    c = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    print(c.execute('select count(*) from skills').fetchone()[0])
except Exception:
    print(0)
")
    echo "### SETELAH BATCH $BATCH: total = $TOT (target $TARGET) ###"
    if [ "$TOT" -ge "$TARGET" ]; then
      echo "### TARGET 100K TERCAPAI. Daemon berhenti. ###"
      break
    fi
    echo "### jeda 90 detik ###"
    sleep 90
    BATCH=$((BATCH + 1))
  done
}

case "${1:-status}" in
  start)
    if tmux has-session -t "$SESSION" 2>/dev/null; then
      echo "sudah jalan: tmux session '$SESSION'"
    else
      tmux new-session -d -s "$SESSION" "bash '$A/mine-daemon.sh' __worker__"
      echo "daemon mining DIMULAI (tmux '$SESSION')"
      echo "  untuk 5000 req/jam: export GH_TOKEN=... lalu start ulang"
      echo "  status: bash '$A/mine-daemon.sh' status"
    fi
    ;;
  __worker__) worker ;;
  stop)
    tmux kill-session -t "$SESSION" 2>/dev/null && echo "daemon dihentikan" || echo "tidak ada session"
    ;;
  status)
    tmux has-session -t "$SESSION" 2>/dev/null && echo "DAEMON: JALAN" || echo "DAEMON: tidak jalan"
    echo "--- log ---"
    tail -n 30 "$LOGDIR"/batch-*.log 2>/dev/null | tail -40
    echo "--- total index ---"
    python3 -c "
import sqlite3, os
db = os.path.expanduser('~/.agents/skills-index.db')
try:
    c = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    t = c.execute('select count(*) from skills').fetchone()[0]
    print('TOTAL:', t, '| kurang:', max(0, 100000 - t))
    for tier, n in c.execute('select tier,count(*) from skills group by tier order by 2 desc'):
        print(f'  {tier}: {n}')
except Exception as e:
    print('index error:', e)
"
    ;;
  *) echo "Pakai: bash $0 {start|stop|status}"; exit 1;;
esac