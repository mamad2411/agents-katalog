#!/bin/bash
echo "== SUHU =="
sudo -n powermetrics --samplers smc -n 1 2>/dev/null | grep -i -E "temp|cpu die" | head -n 10 || echo "(butuh sudo sekali: jalankan manual bila perlu)"
sysctl -n machdep.cpu.brand_string 2>/dev/null
sysctl -n hw.logicalcpu | xargs echo "cores:"
echo "== RAM =="
vm_stat | head -n 8
top -l 1 -s 0 -o mem -n 5 2>/dev/null | tail -n 8 || ps -axm -o %mem,rss,comm | sort -rn | head -n 8
echo "== CPU TOP =="
ps -ax -o %cpu,comm | sort -rn | head -n 10
echo "== DISK =="
df -h ~ | head -n 2
du -sh ~/Library/Caches ~/Documents/AgentsMemory 2>/dev/null
echo "== OBSIDIAN PLUGINS =="
ls ~/Documents/AgentsMemory/.obsidian/plugins/ 2>/dev/null | wc -l | xargs echo "plugin count:"
