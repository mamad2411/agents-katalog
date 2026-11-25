---
name: shell-safety
description: Shell-safety discipline for bash/sh scripts — set -euo pipefail boilerplate, proper quoting, array handling, error patterns. Use when writing, modifying, or reviewing any shell script, Makefile, or .bashrc/.zshrc.
license: MIT
---

# Shell safety

Apply to every shell script written or modified.

## Boilerplate every script needs

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

## Always

- Quote variable expansions: `"$var"`, `"$@"`
- `[[ ... ]]` over `[ ... ]`
- `(( ... ))` for numeric
- Arrays for argument lists, expand `"${args[@]}"`
- `done < <(cmd)` not `cmd | while read`
- `rm -rf "${var:?}/..."` for destructive ops

## Never

- Missing shebang
- Missing `set -euo pipefail`
- Unquoted variable expansion
- `cd` without check
- `rm -rf "$var/"` without `${var:?}`
- `eval` (almost always wrong)
- `for line in $(cat file)` — use `while IFS= read -r line < file`
- `echo` on untrusted data — use `printf '%s\n'`

---

Full content + 15 worked failure-mode examples at https://github.com/HermeticOrmus/shell-safety-skills.
