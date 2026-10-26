#!/usr/bin/env bash
# preflight.sh — gerbang wajib sebelum git push. exit != 0 = JANGAN PUSH.
set -uo pipefail

fail=0
say() { printf '%s\n' "$*"; }
bad() { printf '✗ %s\n' "$*"; fail=1; }
ok()  { printf '✓ %s\n' "$*"; }

# harus di dalam repo git
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  say "bukan git repo — tidak ada yang bisa di-push"
  exit 0
fi

root=$(git rev-parse --show-toplevel)
cd "$root" || exit 1

# 1. konflik merge tertinggal (termasuk file untracked)
files=$( { git diff --cached --name-only; git diff --name-only; \
           git ls-files --others --exclude-standard; } | sort -u | sed '/^$/d')
if [ -n "$files" ]; then
  if printf '%s\n' "$files" | while IFS= read -r f; do
       [ -f "$f" ] && /usr/bin/grep -lE '^(<<<<<<<|>>>>>>>) ' "$f" 2>/dev/null
     done | /usr/bin/grep -q .; then
    bad "konflik merge tertinggal (<<<<<<<) — selesaikan dulu"
  else
    ok "tidak ada konflik merge"
  fi
else
  ok "tidak ada file berubah"
fi

# 2. whitespace error
if git diff --check >/tmp/pg_diffcheck 2>&1; then
  ok "git diff --check bersih"
else
  bad "git diff --check: $(head -3 /tmp/pg_diffcheck | tr '\n' ' ')"
fi

# 3. lint / typecheck / test / build (mode penuh — CI menjalankan semua ini)
if command -v mamat-eval >/dev/null 2>&1; then
  if [ "${PUSH_GREEN_FAST:-0}" = "1" ]; then
    eval_args="--fast"
  else
    eval_args=""
  fi
  say "— cek stack (mamat-eval $eval_args) —"
  if mamat-eval $eval_args; then
    ok "semua cek stack lulus"
  else
    bad "ada cek stack yang gagal (lihat tabel di atas)"
  fi
else
  say "· mamat-eval tidak ada — lewati cek stack"
fi

# 4. commit yang belum dibuat
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  say "· masih ada perubahan belum di-commit (bukan kegagalan)"
fi

say "—"
if [ "$fail" -ne 0 ]; then
  say "HASIL: MERAH — jangan push. Perbaiki dulu."
  exit 1
fi
say "HASIL: HIJAU — aman untuk push."
exit 0
