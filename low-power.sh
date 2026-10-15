#!/bin/bash
# low-power.sh — toggle mode hemat panas (reversible)
# pakai:  low-power.sh on [--docker]   # pause job latar + (opsi) stop Docker
#         low-power.sh off              # lanjutkan job latar
#         low-power.sh status           # lihat keadaan
JOBS="orchestrate-200k.py skill-miner.py cap-crawler.py"
DOCKER_APP="Docker"

sig() {  # sig <STOP|CONT>
  local s="$1" n=0
  for j in $JOBS; do
    for p in $(pgrep -f "$j" 2>/dev/null); do kill -"$s" "$p" 2>/dev/null && n=$((n+1)); done
  done
  echo "  job $s: $n proses"
}

case "$1" in
  on)
    echo "== MODE HEMAT =="
    sig STOP
    if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
      c=$(docker ps -q 2>/dev/null | wc -l | tr -d ' ')
      if [ "$c" -gt 0 ]; then docker stop $(docker ps -q) >/dev/null 2>&1 && echo "  docker: $c container di-stop"; fi
    fi
    if [ "$2" = "--docker" ]; then
      osascript -e "quit app \"$DOCKER_APP\"" 2>/dev/null && echo "  Docker Desktop di-quit"
    fi
    echo "  (lanjut: low-power.sh off ; Docker Desktop buka manual)"
    ;;
  off)
    echo "== MODE NORMAL =="
    sig CONT
    ;;
  status)
    echo "== STATUS =="
    for j in $JOBS; do
      for p in $(pgrep -f "$j" 2>/dev/null); do
        st=$(ps -o stat= -p "$p" 2>/dev/null)
        echo "  $j pid=$p state=$st"
      done
    done
    pgrep -f "$JOBS" >/dev/null || echo "  (tidak ada job latar jalan)"
    command -v docker >/dev/null 2>&1 && echo "  docker container jalan: $(docker ps -q 2>/dev/null | wc -l | tr -d ' ')"
    echo "  top CPU:"; ps -Aceo pcpu,comm -r 2>/dev/null | head -6
    ;;
  *)
    echo "pakai: low-power.sh on [--docker] | off | status"
    ;;
esac
