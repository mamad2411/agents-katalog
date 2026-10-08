#!/usr/bin/env bash
# ghscan-enum.sh — enumerasi repo penghasil SKILL.md via GitHub code search.
# Pakai PAGINASI (page 1..N) untuk menembus batas 1.000 hasil/query.
# Satu query = satu file JSON di /tmp/ghscan-raw/. Jeda 7 detik (limit 10/menit).
set -uo pipefail
PAGES="${1:-5}"          # 5 halaman per path
OUT=/tmp/ghscan-raw
mkdir -p "$OUT"
PATHS=(skills .claude claude agent agents prompts mcp plugin plugins toolkit tool prompt commands rules workspace packages src docs examples skillsets .agents cursor openai gemini config lib bin data content knowledge)
n=0
for p in "${PATHS[@]}"; do
  for ((pg=1; pg<=PAGES; pg++)); do
    q="filename:SKILL.md path:$p"
    enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")
    f="$OUT/$(printf '%03d' $n).json"
    [ -s "$f" ] && { n=$((n+1)); continue; }   # skip yang sudah ada (resume)
    curl -s --max-time 30 -H "Accept: application/vnd.github+json" \
         -H "Authorization: Bearer ${GH_TOKEN:-}" \
         "https://api.github.com/search/code?q=$enc&per_page=100&page=$pg" -o "$f"
    n=$((n+1))
    echo "[$n] $q page$pg -> $(wc -c < "$f" 2>/dev/null) bytes"
    sleep 7
  done
done
echo "=== enumerasi selesai: $n query ==="
