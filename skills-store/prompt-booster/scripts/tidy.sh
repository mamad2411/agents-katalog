#!/bin/bash
# tidy.sh — bersihkan ketikan user sebelum di-enhance.
IN="$1"
echo "$IN" | tr '[:upper:]' '[:lower:]' | tr -s ' ' \
 | sed -E 's/anj[a-z]*|goblok|tolol|bangsat|taik*|tai //g' | tr -s ' ' \
 | sed 's/^ //;s/ $//'
