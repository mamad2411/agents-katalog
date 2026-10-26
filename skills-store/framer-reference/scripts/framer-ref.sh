#!/usr/bin/env bash
# framer-ref.sh — referensi UI/UX dari site Framer (atau site apa pun).
#   framer-ref.sh <url>                 analisa site -> ~/.agents/refs/<slug>/
#   framer-ref.sh <url> --no-shot       token saja, tanpa screenshot
#   framer-ref.sh --gallery [kategori]  daftar site Framer bagus
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$(command -v python3 || true)"
if [ -z "$PY" ]; then echo "python3 tidak ada" >&2; exit 1; fi
exec "$PY" "$DIR/framer_ref.py" "$@"
