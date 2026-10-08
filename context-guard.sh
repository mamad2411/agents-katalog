#!/usr/bin/env bash
# context-guard.sh — pembungkus hook untuk context-guard.py (lihat header .py).
# Biaya nyata: 0 token saat masih di bawah ambang.
exec python3 "$HOME/.agents/context-guard.py"
