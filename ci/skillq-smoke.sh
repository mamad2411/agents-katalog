#!/usr/bin/env bash
# ci/skillq-smoke.sh — buktikan skillq.py masih bisa baca index (pakai DB fixture).
# DB asli (skills-index.db, 208 MB) tidak masuk git, jadi dibangun ulang di sini.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
repo=$(dirname "$here")
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/.agents" "$tmp/fixture"
cp "$repo/skillq.py" "$tmp/.agents/skillq.py"
printf -- '---\nname: smoke-skill\ndescription: skill uji CI\n---\nisi smoke\n' > "$tmp/fixture/SKILL.md"

python3 - "$tmp/.agents/skills-index.db" "$tmp/fixture/SKILL.md" <<'PY'
import sqlite3, sys
db, path = sys.argv[1], sys.argv[2]
c = sqlite3.connect(db)
c.execute("CREATE VIRTUAL TABLE skills USING fts5(name, description, tier, category, path, source)")
c.execute("INSERT INTO skills VALUES (?,?,?,?,?,?)",
          ("smoke-skill", "skill uji untuk cek push hijau", "curated", "qa", path, ""))
c.commit()
PY

out=$(HOME="$tmp" python3 "$tmp/.agents/skillq.py" "uji cek push hijau" -n 3)
printf '%s\n' "$out"
printf '%s\n' "$out" | grep -q "smoke-skill" || { echo "✗ pencarian FTS gagal"; exit 1; }

load=$(HOME="$tmp" python3 "$tmp/.agents/skillq.py" -l smoke-skill)
printf '%s\n' "$load" | grep -q "isi smoke" || { echo "✗ mode -l gagal"; exit 1; }

echo "✓ skillq smoke lulus (cari + load)"
