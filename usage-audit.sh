#!/usr/bin/env bash
# usage-audit.sh — pembungkus usage-audit.py supaya bisa dipanggil gaya repo.
exec python3 "$HOME/.agents/usage-audit.py" "$@"
