#!/usr/bin/env bash
# stop-berat.sh — matikan service berat yang lagi idle (REVERSIBLE, data aman).
# Dipakai pas laptop panas/kipas rame. Data database & container TIDAK dihapus —
# tinggal jalankan lagi dev stack / `brew services start mysql` /
# buka Docker Desktop + `docker start <nama>` buat nyalain kembali.
set -u

echo "== 1/5 Container Docker yang Up -> stop (data tetap ada) =="
up=$(docker ps --format '{{.Names}}' 2>/dev/null)
if [ -n "$up" ]; then
  echo "$up" | xargs docker stop
else
  echo "  tidak ada container Up"
fi

echo "== 2/5 Docker Desktop -> quit =="
if pgrep -f 'Docker Desktop' >/dev/null 2>&1; then
  osascript -e 'quit app "Docker"' 2>/dev/null && echo "  quit OK"
else
  echo "  memang tidak jalan"
fi

echo "== 3/5 MySQL (brew services) -> stop =="
brew services stop mysql 2>/dev/null || echo "  sudah mati / tidak terpasang"

echo "== 4/5 Stack dev (artisan serve/queue/reverb/vite/concurrently) -> kill =="
pkill -f 'php artisan serve' 2>/dev/null
pkill -f 'php artisan schedule:work' 2>/dev/null
pkill -f 'php artisan queue:work' 2>/dev/null
pkill -f 'php artisan reverb:start' 2>/dev/null
pkill -f 'node_modules/.bin/concurrently' 2>/dev/null
pkill -f 'node_modules/.bin/vite' 2>/dev/null
echo "  selesai"

echo "== 5/5 MCP yatim (induk PID 1 & hidup >2 jam) -> kill =="
n=0
for pid in $(ps -ax -o pid,ppid,etime,command | grep -E 'npm exec|node_modules/\.bin/' | grep -v grep | awk '$2==1 { split($3,t,":"); if ($3 ~ /-/ || t[1]+0>=2) print $1 }'); do
  kill "$pid" 2>/dev/null && { echo "  kill $pid"; n=$((n+1)); }
done
[ "$n" -eq 0 ] && echo "  tidak ada MCP yatim"

echo "== Selesai. Cek suhu beban: vm_stat | head -4 ; sysctl vm.loadavg =="