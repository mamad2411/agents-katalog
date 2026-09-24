#!/bin/bash
# Arsipin (bukan hapus) symlink junk hasil skill-auto-symlink.py dari semua tool.
# Isi asli tetap aman di ~/.agents/skills* - ini cuma buang duplikat symlink.
mkdir -p ~/.agents/_symlink-farm-archive
moved=0
for d in "$HOME"/.[!.]*; do
  [ -d "$d" ] || continue
  name=$(basename "$d")
  [ "$name" = ".agents" ] && continue
  sp="$d/skills"
  if [ -d "$sp" ] && [ ! -L "$sp" ]; then
    realdirs=$(find "$sp" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    total=$(find "$sp" -mindepth 1 -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')
    if [ "$total" -gt 0 ] && [ "$realdirs" -eq 0 ]; then
      mv "$sp" ~/.agents/_symlink-farm-archive/"${name#.}-skills-$(date +%s)" && moved=$((moved+1)) && echo "archived: $name"
    fi
  fi
done
echo "Selesai. $moved folder diarsipin ke ~/.agents/_symlink-farm-archive"
echo "Kalau mau bener2 hapus arsipnya nanti (opsional): rm -rf ~/.agents/_symlink-farm-archive"
