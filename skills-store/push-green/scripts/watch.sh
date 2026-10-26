#!/usr/bin/env bash
# watch.sh — pantau CI GitHub sampai hijau. exit 1 kalau merah.
# pakai: watch.sh [--report] [--timeout DETIK]
set -uo pipefail

timeout=900
report=0
while [ $# -gt 0 ]; do
  case "$1" in
    --report) report=1 ;;
    --timeout) timeout=${2:-900}; shift ;;
    -h|--help) echo "watch.sh [--report] [--timeout DETIK]"; exit 0 ;;
  esac
  shift
done

command -v gh >/dev/null 2>&1 || { echo "✗ gh tidak terpasang"; exit 1; }
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "· bukan git repo"; exit 0; }

branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
sha=$(git rev-parse HEAD 2>/dev/null)

json=$(gh run list --branch "$branch" --limit 1 \
        --json databaseId,status,conclusion,workflowName,url,headSha 2>/dev/null)

if [ -z "$json" ] || [ "$json" = "[]" ]; then
  echo "· tidak ada workflow CI di branch '$branch' — tidak ada yang dipantau"
  exit 0
fi

get() { printf '%s' "$json" | python3 -c "import json,sys;d=json.load(sys.stdin)[0];print(d.get('$1') or '')" 2>/dev/null; }
id=$(get databaseId); wf=$(get workflowName); url=$(get url); hsha=$(get headSha)

if [ "$hsha" != "$sha" ]; then
  echo "· run terakhir ($wf) untuk commit ${hsha:0:7}, HEAD sekarang ${sha:0:7}"
  echo "  jalankan watch.sh lagi setelah run baru muncul"
fi

printf 'memantau: %s (branch %s)\n' "${wf:-workflow}" "$branch"

start=$(date +%s)
while :; do
  json=$(gh run list --branch "$branch" --limit 1 \
          --json databaseId,status,conclusion,workflowName,url,headSha 2>/dev/null)
  st=$(get status); cc=$(get conclusion); url=$(get url); id=$(get databaseId)
  printf '  %s  %-12s %s\n' "$(date +%H:%M:%S)" "${st:-?}" "${cc:-…}"

  case "$st" in
    completed)
      if [ "$cc" = "success" ]; then
        echo "✓ HIJAU — $url"
        exit 0
      fi
      echo "✗ MERAH ($cc) — $url"
      echo "--- 40 baris log gagal ---"
      gh run view "$id" --log-failed 2>/dev/null | tail -40
      echo "---"
      echo "Perbaiki akar masalah, commit, ulangi preflight.sh → push → watch.sh."
      exit 1
      ;;
  esac

  if [ $(( $(date +%s) - start )) -ge "$timeout" ]; then
    echo "· timeout ${timeout}s — masih '$st', belum selesai. Bukan hijau: jangan bilang selesai."
    exit 2
  fi
  sleep 10
done
