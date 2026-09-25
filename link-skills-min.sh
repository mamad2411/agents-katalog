#!/usr/bin/env bash
# link-skills-min.sh — wire skill via SYMLINK (bukan klon). Idempotent & tidak pernah
# menghapus apa pun. Ini yang menggantikan pola "salin 24k entri ke tiap tool".
#
# Pakai:
#   link-skills-min.sh --repo /path/ke/repo      # project-scope: <repo>/skills/* -> <repo>/.claude/skills/
#   link-skills-min.sh --tool ~/.claude/skills   # user-scope: set "starter" (default)
#   link-skills-min.sh --tool ~/.claude/skills starter | all-curated
#   link-skills-min.sh --status                  # lihat kondisi wiring tiap tool
set -euo pipefail

AGENTS_SKILLS="$HOME/.agents/skills-store"

# Set minimal & relevan untuk kerja sehari-hari (Go/DB/Vue/QA/docs).
STARTER="postgresql-database-engineering unit-test-generator api-test-suite-generator \
code-review systematic-debugging documentation-writer docker-patterns git-commit \
security-review performance-optimization create-implementation-plan refactor"

link_one() { # $1=src $2=dst
  local src="$1" dst="$2"
  if [ -L "$dst" ]; then
    if [ "$(readlink "$dst")" = "$src" ]; then echo "  = ok  $(basename "$dst")"; return 0; fi
    echo "  ! ada   $(basename "$dst") (symlink lain, dibiarkan)"; return 0
  fi
  if [ -e "$dst" ]; then echo "  ! ada   $(basename "$dst") (bukan symlink, dibiarkan)"; return 0; fi
  ln -s "$src" "$dst" && echo "  + link $(basename "$dst")"
}

case "${1:-}" in
  --repo)
    target="${2:?Pakai: --repo <path>}"
    [ -d "$target" ] || { echo "ERROR: $target bukan folder"; exit 1; }
    mkdir -p "$target/.claude/skills"
    n=0
    for d in "$target"/skills/*/; do
      [ -f "$d/SKILL.md" ] || continue
      link_one "../../skills/$(basename "$d")" "$target/.claude/skills/$(basename "$d")"
      n=$((n + 1))
    done
    echo "repo-scope: $n skill → $target/.claude/skills (symlink relatif, portable)"
    ;;

  --tool)
    target="${2:?Pakai: --tool <dir> [starter|all-curated]}"
    set_name="${3:-starter}"
    [ -d "$target" ] || { echo "ERROR: $target bukan folder"; exit 1; }
    names=""
    case "$set_name" in
      starter) names="$STARTER" ;;
      all-curated) for d in "$AGENTS_SKILLS"/*/; do names="$names $(basename "$d")"; done ;;
      *) echo "set tidak dikenal: $set_name"; exit 1 ;;
    esac
    for n in $names; do
      if [ -d "$AGENTS_SKILLS/$n" ]; then
        link_one "$AGENTS_SKILLS/$n" "$target/$n"
      else
        echo "  - lewat (tidak ada di curated): $n"
      fi
    done
    echo "user-scope: set=$set_name → $target"
    ;;

  --status)
    echo "== sumber: $AGENTS_SKILLS ($(ls -1 "$AGENTS_SKILLS" 2>/dev/null | wc -l | tr -d ' ') entri) =="
    python3 - "$HOME" <<'PYSTATUS'
import os, sys
home = sys.argv[1]
rows = []
for name in sorted(os.listdir(home)):
    d = os.path.join(home, name, "skills")
    if not os.path.isdir(d):
        continue
    links = dirs = files = 0
    try:
        with os.scandir(d) as it:      # d_type dari dirent: cepat, tanpa stat
            for e in it:
                if e.is_symlink():
                    links += 1
                elif e.is_dir():
                    dirs += 1
                else:
                    files += 1
    except OSError:
        continue
    rows.append((name, links, dirs, files))
print(f"  {'tool':<18} {'symlink':>8} {'real-dir':>9} {'file':>7}")
for name, links, dirs, files in rows:
    print(f"  {name:<18} {links:>8} {dirs:>9} {files:>7}")
print("\n  Catatan: 'real-dir' besar = masih klon (boros & tidak auto-update).")
print("  Sehat = symlink. Perbaiki dengan: link-skills-min.sh --tool <dir>")
PYSTATUS
    ;;


  *)
    echo "Pakai: $0 --repo <path> | --tool <dir> [starter|all-curated] | --status"
    exit 1
    ;;
esac
