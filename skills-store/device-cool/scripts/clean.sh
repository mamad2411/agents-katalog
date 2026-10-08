#!/bin/bash
# clean.sh — hapus cache AMAN saja. Tidak sentuh vault/skills/login.
before=$(du -sk ~/Library/Caches 2>/dev/null | cut -f1)
rm -rf ~/Library/Caches/com.apple.Safari/WebKitCache/* 2>/dev/null
rm -rf ~/Library/Caches/Google/Chrome/*"Cache*" 2>/dev/null
rm -rf ~/Library/Caches/pip/* ~/Library/Caches/pnpm/* ~/Library/Caches/npm/*_cacache/tmp* 2>/dev/null
rm -rf ~/Library/Developer/Xcode/DerivedData/* 2>/dev/null
rm -rf ~/.npm/_cacache/tmp* ~/.cache/pip/* 2>/dev/null
find ~/Library/Caches -name "*.tmp" -mtime +7 -delete 2>/dev/null
find /tmp -user "$USER" -mtime +3 -delete 2>/dev/null
rm -rf ~/Documents/AgentsMemory/.obsidian/cache/* 2>/dev/null
rm -rf ~/Documents/AgentsMemory/.obsidian/workspace-mobile.json.bak 2>/dev/null
after=$(du -sk ~/Library/Caches 2>/dev/null | cut -f1)
echo "cache sebelum: $((before/1024))MB sesudah: $((after/1024))MB bebas: $(((before-after)/1024))MB"
