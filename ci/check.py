#!/usr/bin/env python3
"""ci/check.py — validasi repo agents-katalog tanpa model, tanpa jaringan.

Cek:
  1. semua *.json yang di-track bisa di-parse
  2. semua *.py yang di-track lolos compile (syntax)
  3. semua *.sh yang di-track lolos `bash -n`
  4. skills-store/*/SKILL.md punya frontmatter `name:` + `description:`
  5. RULES.md ada dan punya >= 8 bagian `## `

exit 0 = hijau, exit 1 = merah. Output maksimal 12 baris + detail error.
"""
import json
import os
import subprocess
import sys
import warnings

warnings.simplefilter("ignore")  # hanya peduli SyntaxError, bukan SyntaxWarning

MAX_DETAIL = 10
fails = []


def tracked(pattern):
    out = subprocess.run(["git", "ls-files", pattern], capture_output=True, text=True)
    return [f for f in out.stdout.splitlines() if f and os.path.isfile(f)]


def report(label, bad, total):
    mark = "✓" if not bad else "✗"
    print(f"{mark} {label}: {total - len(bad)}/{total}")
    for b in bad[:MAX_DETAIL]:
        print(f"    - {b}")
    if len(bad) > MAX_DETAIL:
        print(f"    ... +{len(bad) - MAX_DETAIL} lagi")
    if bad:
        fails.append(label)


# 1. JSON
bad, files = [], tracked("*.json")
for f in files:
    if os.path.getsize(f) > 2_000_000:
        continue
    try:
        with open(f, encoding="utf-8") as fh:
            json.load(fh)
    except Exception as e:
        bad.append(f"{f}: {str(e)[:80]}")
report("JSON valid", bad, len(files))

# 2. Python syntax
bad, files = [], tracked("*.py")
for f in files:
    try:
        compile(open(f, encoding="utf-8", errors="ignore").read(), f, "exec")
    except SyntaxError as e:
        bad.append(f"{f}:{e.lineno}: {e.msg}")
    except Exception as e:
        bad.append(f"{f}: {str(e)[:80]}")
report("Python compile", bad, len(files))

# 3. Bash syntax
bad, files = [], tracked("*.sh")
for f in files:
    r = subprocess.run(["bash", "-n", f], capture_output=True, text=True)
    if r.returncode != 0:
        bad.append(f"{f}: {(r.stderr or '').strip().splitlines()[-1][:80] if r.stderr.strip() else 'gagal'}")
report("bash -n", bad, len(files))

# 4. SKILL.md frontmatter
bad, files = [], tracked("skills-store/*/SKILL.md")
for f in files:
    try:
        head = open(f, encoding="utf-8", errors="ignore").read(2000)
    except OSError as e:
        bad.append(f"{f}: {e}")
        continue
    if not head.startswith("---"):
        bad.append(f"{f}: tidak ada frontmatter")
    elif "name:" not in head or "description:" not in head:
        bad.append(f"{f}: frontmatter kurang name/description")
report("SKILL.md frontmatter", bad, len(files))

# 5. RULES.md
bad = []
if not os.path.isfile("RULES.md"):
    bad.append("RULES.md tidak ada")
else:
    txt = open("RULES.md", encoding="utf-8", errors="ignore").read()
    n = sum(1 for line in txt.splitlines() if line.startswith("## "))
    if n < 8:
        bad.append(f"RULES.md cuma {n} bagian '## ' (harap >= 8)")
report("RULES.md", bad, 1)

print("—")
if fails:
    print(f"MERAH — gagal: {', '.join(fails)}")
    sys.exit(1)
print("HIJAU — semua cek lulus")
