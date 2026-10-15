#!/usr/bin/env bash
# rebuild-all.sh — pipeline rebuild katalog skill LENGKAP & IDEMPOTENT (aman 2x).
# Urutan WAJIB (AGENTS.md): build_skills_index -> skills-index-md -> skills-router
# (dua terakhir membaca DB, jadi harus setelah index jadi).
#
# Pakai:
#   bash ~/.agents/rebuild-all.sh          # rebuild penuh
#   bash ~/.agents/rebuild-all.sh --mine   # tambang dulu (registry) lalu rebuild
set -euo pipefail
AG="$HOME/.agents"
LOG="$AG/rebuild-all.log"
ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

{
echo "===== $(ts) rebuild-all start ====="

if [ "${1:-}" = "--mine" ]; then
  echo "[1/4] mining registry (quality gate stars>=${REG_MIN_STARS:-100}, max ${REG_MAX_REPOS:-40} repo)..."
  REG_MIN_STARS="${REG_MIN_STARS:-100}" REG_MAX_REPOS="${REG_MAX_REPOS:-40}" \
  REG_LIMIT_PER_REPO="${REG_LIMIT_PER_REPO:-60}" \
    python3 "$AG/skill-miner.py" --registry || echo "  mining: ada error (dilanjutkan)"
else
  echo "[1/4] mining dilewati (pakai --mine untuk tambang dulu)"
fi

echo "[2/4] build_skills_index.py (scan SKILL.md -> DB)..."
python3 "$AG/build_skills_index.py"

echo "[3/4] skills-index-md.py (regenerate SKILLS-INDEX.md)..."
python3 "$AG/skills-index-md.py"

echo "[4/4] skills-router.py (regenerate SKILLS-AVAILABLE.md + skills-index.json)..."
python3 "$AG/skills-router.py"

echo "===== $(ts) rebuild-all done ====="
} 2>&1 | tee -a "$LOG"
