---
name: tooling-ripgrep
description: Use when searching code with ripgrep (rg) — patterns, globs, file types, JSON output, in-place replacement, and why it beats grep/ack/ag for source trees.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: tooling
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [tooling-shell-fish, tooling-jq, tooling-fzf, tooling-git-advanced]
---

# ripgrep (rg) — Fast Code Search

`rg` is the search tool you should reach for in a source tree. It respects `.gitignore` by default, skips binary files automatically, supports proper PCRE regex with `-P`, and is faster than `grep` / `ack` / `ag` on every benchmark that matters. Even when there's no clear winner on speed, the defaults are saner.

**Core principle:** the right default is "search what's tracked in git, skip vendored junk, output is parseable." `rg` is that default. `grep` is fine for ad-hoc text; for code, prefer `rg`.

## Default behavior (and why it's right)

```sh
rg "TODO"
```

- Searches recursively from `.`
- Respects `.gitignore`, `.ignore`, and global ignore files
- Skips hidden files and binary files
- Output is colored line-numbered file:line:match

You'd need `grep -rn --include='*' --exclude-dir=node_modules ...` to approximate this, and you'd still get `.git/` noise.

To **opt out**: `--no-ignore` (search ignored files too — surfaces `.env`, secrets, key files), `--hidden` (include dotfiles), `-uuu` (all of the above + binary scan). Both `--no-ignore` and `-uuu` will dump credential file contents to stdout if your pattern matches them — never pipe their output to logs, CI artifacts, or chat. Use sparingly; usually you want the defaults.

## Patterns — fixed strings vs regex

```sh
rg "TODO"                # default: regex (TODO is a literal here)
rg -F "a.b[c]"           # fixed-string (no regex interpretation)
rg -e "^class" -e "^def" # multiple patterns
rg -P '(?<=foo)bar'      # PCRE2 (lookarounds, etc.) — slower
rg -w "user"             # whole word only
rg -i "user"             # case-insensitive
rg -S "User"             # smart-case (case-insensitive if pattern is all-lowercase)
```

`-S` (smart case) is the right default for interactive use. Add it to your alias.

## Scoping — globs and file types

```sh
rg "useState" -g "*.tsx" -g "*.ts"           # include patterns
rg "TODO" -g '!**/test/**'                   # exclude pattern (note the leading !)
rg "import" -t py                            # builtin type: python
rg "import" -t js -t ts                      # multiple builtin types
rg "import" -T test                          # exclude type
rg --type-list                               # see all builtin types
```

`-t/-T` is shorter than `-g '*.py'` and covers the right extensions per language. `--type-add 'tf:*.tf,*.tfvars'` registers a custom type for the session (or in `~/.ripgreprc`).

## Output — parseable, scriptable

```sh
rg "TODO" --json                # ndjson — one event per line; perfect for jq
rg -l "TODO"                    # files-with-matches (just filenames)
rg --files-without-match "TODO" # files without any match
rg -c "TODO"                    # count per file
rg --count-matches "TODO"       # total count per file (matches, not lines)
rg --vimgrep                    # filename:line:col:text for editor jump
rg --no-heading --line-number   # legacy grep-style output for older tooling
```

`--json` is the right answer when piping to another tool:

```sh
rg "panic" --json | jq -r 'select(.type=="match") | .data.path.text'
```

This gives you a list of files that match without parsing colon-delimited text.

## Context — surrounding lines

```sh
rg "panic" -A 5         # 5 lines after
rg "panic" -B 3         # 3 lines before
rg "panic" -C 3         # 3 lines before AND after
rg "panic" -A 1000 | less  # paged with lots of context
```

## Replacement — `--replace` for previews, `sed`/IDE for actual writes

```sh
rg "OldName" --replace "NewName"               # prints what the substitution would look like
rg "OldName" --replace "NewName" --passthru    # also prints non-matching lines (full-file diff preview)
```

`rg --replace` **doesn't modify files** — it shows the substituted output. For in-place edits use `sed -i`, your editor's find-and-replace, or a script that writes the file back.

Capture groups work: `rg '(\w+)@example.com' --replace '$1@new.com'`.

## Boolean searches — `--multiline` and combinations

```sh
rg -U "^class.*\n.*def __init__"           # cross-line regex (-U enables multiline)
rg -U "^class[\s\S]*?^def"                 # non-greedy until next top-level def

# Files matching A AND B (intersection of two -l outputs)
comm -12 <(rg -l "import asyncio" | sort) <(rg -l "import logging" | sort)
```

`rg` doesn't have built-in boolean operators; pipe and combine with `comm`/`sort`/`uniq`.

## Config — `~/.ripgreprc`

```
--smart-case
--hidden
--glob=!.git/
--glob=!node_modules/
--type-add=svelte:*.svelte
--type-add=astro:*.astro
```

Set `RIPGREP_CONFIG_PATH=~/.ripgreprc` in your shell init. Now `rg` everywhere has your defaults.

## Performance — measurable knobs

- `-j N` — thread count (default = logical cores)
- `--mmap` — memory-map files (sometimes faster on Linux for large files)
- `--no-mmap` — disable when search is bottlenecked on small-file overhead
- `--max-filesize 10M` — skip huge files (logs, vendored bundles)

For a 100k-file tree, `rg` is typically 2–10× faster than `grep -r` and comparable to `ag` but with better defaults. Don't micro-optimize unless searching gigabytes.

## Common patterns

```sh
# Find a function definition across the repo
rg "^(func|def|fn|function)\s+myFunc\b"

# Find usages but not the definition
rg "myFunc\b" -g '!**/myfile.go'

# All files that import a specific package
rg -l '"github.com/me/pkg"' -t go

# Strings that look like API tokens (sample heuristic; not a real scanner)
rg -P '\b[A-Za-z0-9+/]{40,}={0,2}\b' --type-not lock

# Recent additions: files modified in the last day, then search
fd -t f --changed-within 1d | xargs rg "TODO"
```

For real secret detection, use a purpose-built scanner (`gitleaks`, `trufflehog`) — see `Skill(security)`.

## When NOT to use rg

- AST-aware refactoring → use `ast-grep`, `comby`, or the language's LSP
- Multi-file structural edits → editor / IDE find-and-replace
- Searching giant logs (gigabytes) → `grep` with `LC_ALL=C` may beat `rg` on pure linear scan
- Binary files (PDFs, etc.) → `pdfgrep`, `strings | rg`

## Anti-patterns

- `grep -r` in a node_modules-having tree
- `find . -name '*.py' -exec grep ...` — `rg -t py` does the same, faster, with smart filtering
- `rg --replace` and assuming files changed — it only previews
- Forgetting `-F` and getting regex interpretation of input that contains `.` `*` `[` `(`
- Piping `rg | grep` to add a second filter — combine: `rg '(foo).*bar'` or use `-e` twice
- Re-searching the whole tree when you already know the file — pass the path

## Hand-off

For interactive fuzzy selection over `rg --files` output, `Skill(tooling-fzf)`. For JSON munging when piping `rg --json`, `Skill(tooling-jq)`. For shell aliases and abbreviations to set defaults, `Skill(tooling-shell-fish)`. For finding git-tracked-only files (when `.gitignore` is wrong), `Skill(tooling-git-advanced)`.
