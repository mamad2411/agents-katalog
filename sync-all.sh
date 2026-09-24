#!/usr/bin/env bash
# sync-all.sh — SATU PERINTAH: segarkan katalog + hapus pemakaian kadaluarsa +
# symlink ke semua AI + MCP skill-catalog + eval kesehatan. Idempotent (aman diulang).
#
#   bash ~/.agents/sync-all.sh          # full
#   bash ~/.agents/sync-all.sh --fast   # tanpa rebuild katalog (wiring saja)
set -uo pipefail
AG="$HOME/.agents"

echo "=== [1/5] Katalog segar ==="
if [ "${1:-}" != "--fast" ]; then
  python3 "$AG/build_skills_index.py" 2>&1 | tail -2
  python3 "$AG/skills-index-md.py" 2>&1 | tail -2   # regen skills-INDEX.md (dulu sering kelewat → basi)
  python3 "$AG/skills-router.py" 2>&1 | tail -2
else
  echo "  (lewati — --fast)"
fi

echo "=== [2/5] Bersihkan kadaluarsa + symlink semua AI + MCP ==="
python3 "$AG/sync-wire.py"

echo "=== [3/5] Project scope (repo kerja) ==="
for repo in "$HOME/receptor/voralens-v2"; do
  [ -d "$repo/skills" ] && bash "$AG/link-skills-min.sh" --repo "$repo" 2>&1 | tail -1
done

echo "=== [4/5] Lifecycle MCP (parkir idle, tanpa daemon) ==="
python3 "$AG/mcp-lifecycle.py" 2>&1 | tail -2

echo "=== [5/5] Eval kesehatan ==="
python3 "$AG/skill-eval.py" 2>&1 | tail -4 || echo "  (eval ada isu — lihat di atas)"
echo "SELESAI: bash ~/.agents/sync-all.sh"