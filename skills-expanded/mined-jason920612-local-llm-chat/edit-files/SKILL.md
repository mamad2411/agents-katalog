---
name: edit-files
description: Safely create and edit plain-text and code files in the sandbox (source code, configs, JSON/YAML/TOML, .txt, .md, .env, scripts, Dockerfiles, etc.) using run_code. Use whenever the user asks to write, create, modify, patch, refactor, rename, append to, or fix a non-document file — or when you need to change a file you cloned or generated. Do NOT use for Word/Excel/PowerPoint/PDF — use the docx / xlsx / pptx / pdf skills for those.
---

# Create & edit files safely in the sandbox

You edit files by running shell/Python through `run_code` (bash + `python3` are
available; on the local driver bash is Git Bash on Windows, on the microVM it is
Linux). There is no interactive editor — every change is a scripted operation, so
do it precisely and verify it. The cardinal sin is **clobbering** a file (losing
content with a careless `>` or a wrong replace). Follow the rules below.

## Golden rules

1. **Read before you edit.** Never edit a file you haven't just looked at — its
   real content may differ from what you assume.
2. **Edit surgically.** Change only the bytes you mean to. Don't rewrite a whole
   file to change one line.
3. **Match must be unique.** When replacing text, the target string must occur
   exactly once. If it doesn't, add surrounding context until it does.
4. **Verify after every edit.** Re-read the changed region and run a syntax/lint
   check. An edit you didn't verify is not done.
5. **`>` overwrites, `>>` appends.** Use `>` only to create or fully replace a
   file on purpose. Never use `>` on a file you meant to edit in place.

## Read first (with line numbers)

```bash
ls -la path/to                       # exists? size?
cat -n path/to/file.ts               # whole small file with line numbers
sed -n '40,90p' path/to/file.ts      # only lines 40-90 of a big file
grep -n "anchorText" path/to/file.ts # find the line(s) you'll target
```

## Create a NEW file

Use a **quoted** heredoc (`<<'EOF'`) so `$`, backticks, etc. are written
literally and nothing is expanded. Make parent dirs first.

```bash
mkdir -p src/config
cat > src/config/app.json <<'EOF'
{
  "name": "demo",
  "port": 3000
}
EOF
```

For binary-ish or tricky content, or to guarantee UTF-8, use Python:

```bash
python3 - <<'PY'
from pathlib import Path
Path("src/config").mkdir(parents=True, exist_ok=True)
Path("src/config/app.json").write_text('{\n  "name": "demo"\n}\n', encoding="utf-8")
print("written")
PY
```

## Edit an EXISTING file — exact-string replace (preferred)

This is the safest, most predictable edit: replace one unique exact string with
another, failing loudly if the target is missing or ambiguous. Paste this helper
and call it for each change.

```bash
python3 - <<'PY'
from pathlib import Path

def patch(path, old, new, count=1):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n == 0:
        raise SystemExit(f"NO MATCH in {path}: {old!r}")
    if count == 1 and n > 1:
        raise SystemExit(f"AMBIGUOUS ({n} matches) in {path}: {old!r} — add context")
    p.write_text(s.replace(old, new), encoding="utf-8")
    print(f"patched {path}: {n} change(s)")

# Example: change a value. Include enough context to be unique.
patch("src/config/app.json", '"port": 3000', '"port": 8080')
PY
```

Tips:
- Copy `old` **verbatim** from what you just read (exact indentation/whitespace).
- If a string repeats, widen `old` to include a unique neighbouring line, or pass
  `count=` to replace all intentionally.
- To insert near an anchor, replace the anchor with `anchor + "\n" + new_line`.

## Other edit patterns

**Append** to a file:
```bash
printf '\nexport const FLAG = true;\n' >> src/flags.ts
```

**Replace a line range** (drop lines 10-12, splice in new text) with Python:
```bash
python3 - <<'PY'
from pathlib import Path
p = Path("notes.txt"); lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
lines[9:12] = ["new line A\n", "new line B\n"]   # 0-based: lines 10..12
p.write_text("".join(lines), encoding="utf-8")
PY
```

**Simple literal swap with sed** is fine for trivial, unique, metacharacter-free
edits, but Python is safer for anything with `/ & . * [ ]` or indentation:
```bash
cp file.txt file.txt.bak                     # cheap backup for risky edits
sed -i 's/oldword/newword/g' file.txt        # note: regex — escape specials
```

## Verify after editing (do not skip)

Re-read the region, then check it parses for its language:
```bash
sed -n '1,40p' path/to/file          # eyeball the result
python3 -m py_compile script.py      # Python
node --check app.js                  # JS
bash -n script.sh                    # bash
python3 -c "import json;json.load(open('app.json'))"   # JSON
python3 -c "import tomllib;tomllib.load(open('x.toml','rb'))"  # TOML (3.11+)
```
In a git repo, `git diff -- path` shows exactly what changed — use it to confirm.

## Common pitfalls

- **Unquoted heredoc** (`<<EOF`) expands `$VAR`/backticks and mangles code. Use
  `<<'EOF'` unless you specifically want expansion.
- **`>` instead of `>>`** wipes the file. Double-check the redirection.
- **Non-unique replace target** silently changes the wrong place — the helper
  above guards against this; honour its errors instead of forcing the edit.
- **Lost indentation / tabs vs spaces** — copy `old` exactly; don't retype it.
- For large multi-file changes, do them in **one** `run_code` script so they
  apply atomically and you can verify together.

## When NOT to use this skill

Word (`.docx`), Excel (`.xlsx/.csv`), PowerPoint (`.pptx`), and PDF files are not
plain text — use the **docx**, **xlsx**, **pptx**, or **pdf** skills instead.
