---
name: codebase-text-replacement
description: Safe find-and-replace across a multi-file codebase — rebranding, renaming APIs, updating constants, and any project-wide text substitution. Covers bulk replacement strategy, HTML/JS fragility, and post-replace verification.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [find-replace, codebase-refactoring, bulk-edit, rename]
    triggers:
      - "rename X to Y across the project"
      - "replace all occurrences of X"
      - "rebrand everything from X to Y"
      - "update constant/import/reference name throughout"
      - "find and replace across all files"
    related_skills: [systematic-debugging, github]
---
# Codebase Text Replacement

Class-level workflow for safe project-wide text substitution. Two-phase approach: **bulk** (Python) + **manual** (patch) with verification.

## Phase 1: Inventory

Find all occurrences before making changes. Use `execute_code` with Python `os.walk` — the built-in `search_files` can miss files in complex directory trees.

```python
import os
target_dir = "/path/to/project"
exclude_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}
exclude_ext = {'.pyc', '.exe', '.png', '.jpg', '.gif', '.ico', '.svg'}

files = []
for root, dirs, fnames in os.walk(target_dir):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for fname in fnames:
        ext = os.path.splitext(fname)[1].lower()
        if ext in exclude_ext: continue
        with open(os.path.join(root, fname), 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if 'OLD_TEXT' in content:
            files.append(os.path.relpath(os.path.join(root, fname), target_dir))
            print(f"  {relpath}: {content.count('OLD_TEXT')} matches")
print(f"\n{len(files)} files total")
```

## Phase 2: Bulk Replacement (Python)

For 10+ files, use Python to walk and replace. This is safer than `sed` (avoids MSYS path issues on Windows) and gives you a clean count.

```python
import os
target_dir = "/path/to/project"
# ... same walk as Phase 1 ...
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    count = content.count('OLD_TEXT')
    if count > 0:
        new_content = content.replace('OLD_TEXT', 'NEW_TEXT')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
```

**Always use `content.replace(old, new)` — never `string.replace_all` or shell sed with global flags for the initial bulk pass.**

## Phase 3: Manual Edits (patch)

After bulk pass, use `patch` (find-and-replace) for remaining manual edits in specific files:

- **Always provide unique surrounding context** (3-5 lines). This ensures the match is unique and you don't accidentally replace unintended text.
- **Prefer inline patch calls** over `replace_all=True` for files with closing braces.

### ⚠️ CRITICAL PITFALL: Never use `replace_all=True` on HTML or JS files

`replace_all=True` with a string that ends in `}` (or contains `}`, `]`, `)`, `;`, or any common CSS/JS token) **will destroy the file**. On HTML files, `}` appears in:
- CSS closing braces (hundreds of them)
- JS function/block closing braces
- Template literal interpolation `${}`
- JSX expressions

These `}` characters will be matched by `replace_all` when they appear as substrings inside larger patterns, replacing them with your target string. This corrupts every CSS rule, every JS block, and every HTML tag that happens to contain the matched substring.

**Safe approach:** use unique context strings with `replace_all=False` (default). Make the `old_string` include unique surrounding code so the match is unambiguous.

```python
# SAFE — unique context match
patch(path="file.html",
      old_string="      <div class=\"header-logo-text\">AI<span>Sharp</span></div>\n      <div class=\"header-status\">",
      new_string="      <div class=\"header-logo-text\">New<span>Name</span></div>\n      <div class=\"header-status\">")

# DANGEROUS — any ```}``` in file will match
patch(path="file.html",
      old_string="AI Sharp",
      new_string="New Name",
      replace_all=True)  # ← DO NOT DO THIS ON HTML/JS
```

## Phase 4: Check Related References

After the primary replacement, search for **related** identifiers that may need updating:

- `PascalCase` → `PascalCase` (brand name casing)
- `snake_case` → `snake_case` (variable names, API routes, localStorage keys)
- `kebab-case` → `kebab-case` (URL paths, Docker names — evaluate per case)
- `UPPER_CASE` → `UPPER_CASE` (environment variables, constants)

Not all of these should change (repo names, directory names, package names may stay), but all should be evaluated.

```python
for variant in ["old_name", "OLD_NAME", "old-name", "oldName"]:
    # search for each variant across project
    ...
```

## Phase 5: Verification

After all replacements, verify:

1. **No stale references** — re-scan project for the old string
2. **New references present** — confirm new string exists where expected
3. **Syntax check** — compile Python files, check JS syntax, check HTML tag balance

```python
# Syntax check
try:
    compile(content, path, "exec")
except SyntaxError as e:
    errors.append(f"syntax error: {e}")

# HTML div balance check
open_divs = len(re.findall(r'<div\b', html))
close_divs = len(re.findall(r'</div>', html))
if open_divs != close_divs:
    errors.append(f"div mismatch {open_divs}/{close_divs}")
```

4. **Git diff review** — read the diff to confirm no unexpected changes snuck in

## Pitfalls

- **`replace_all=True` on HTML/JS** — will corrupt the file. Always use unique context matching instead.
- **Binary files** — skip images, compiled files, archives. Python `open(..., errors='ignore')` can still corrupt binary files; check extension before reading.
- **Git-controlled files** — always commit before starting so you can `git checkout` a corrupted file.
- **Case sensitivity** — `content.replace('Old', 'New')` is case-sensitive. If you need case-insensitive, use `re.sub(re.escape('Old'), 'New', content, flags=re.IGNORECASE)`.
- **Partial matches** — replacing 'Sharp' would match 'SharpEdge' too. Add word boundaries or check context.
- **MSYS/git-bash sed** — on Windows, `sed -i` can corrupt line endings. Python is more reliable for bulk changes.
- **Interrupted patch series** — if a multi-patch session is interrupted (compaction, transport error), the file may hold duplicate/overlapping blocks. Do NOT keep patching — follow `references/interrupted-edit-recovery.md`: read the whole file, excise duplicates or rewrite head+body+tail, then syntax-check (`ast.parse` / `npm run build`) before any further edit.
