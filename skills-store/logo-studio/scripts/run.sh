#!/usr/bin/env bash
# Satu pintu masuk untuk logo-studio. Pilih interpreter yang benar sendiri.
#
#   run.sh build spec.json -o out/ [--trim] [--mono '#0a1420']
#   run.sh proof out/mark.svg -o out/proof.png
#   run.sh fonts list DIN
#
# logo.py + fonts.py butuh venv (fontTools, skia-pathops).
# proof.py butuh python3 sistem (playwright + Chromium sudah terpasang di sana).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$HOME/.agents/vendor/logo-venv/bin/python"

if [[ ! -x "$VENV" ]]; then
  echo "venv belum ada. Jalankan:" >&2
  echo "  python3 -m venv ~/.agents/vendor/logo-venv" >&2
  echo "  ~/.agents/vendor/logo-venv/bin/pip install fonttools skia-pathops" >&2
  exit 1
fi

cmd="${1:-}"
shift || true

case "$cmd" in
  build) exec "$VENV" "$HERE/logo.py" build "$@" ;;
  fonts) exec "$VENV" "$HERE/fonts.py" "$@" ;;
  proof)
    python3 - "$@" <<'PY' || exit $?
import sys
try:
    import playwright.sync_api  # noqa: F401
except ModuleNotFoundError:
    sys.exit("proof.py butuh playwright. Install: python3 -m pip install --user playwright && python3 -m playwright install chromium")
PY
    exec python3 "$HERE/proof.py" "$@"
    ;;
  *)
    echo "pakai: run.sh {build|proof|fonts} ..." >&2
    exit 2
    ;;
esac
