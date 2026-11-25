---
name: shell-script-hardening
description: Hardens bash scripts with strict mode, safe quoting, cleanup traps and clean shellcheck results, without changing what the script does.
---

# Shell script hardening

Keep behavior identical. Remove ways for the script to fail silently or do damage.

## Steps

1. Read the script fully and note what it does. If there are no tests, write a small harness or a dry-run first.
2. Check the shebang: `#!/usr/bin/env bash`. If it uses bash features, do not claim POSIX sh.
3. Add strict mode after the shebang: `set -Eeuo pipefail`, and a safe `IFS=$'\n\t'` only if the script relies on word splitting you have verified.
4. Quote every expansion: `"$var"`, `"${arr[@]}"`. Use arrays for command arguments, never strings. Prefer `$(...)` to backticks and `[[ ]]` to `[ ]`.
5. Validate input: required arguments with `${1:?usage: script <dir>}`, existence of files and tools (`command -v jq >/dev/null`), and refuse empty variables in `rm -rf "${dir:?}"/`.
6. Create temp files with `mktemp` and register `trap 'rm -rf "$tmp"' EXIT`. Add `trap ... ERR` to print the failing line when useful.
7. Handle expected failures explicitly with `if cmd; then` or `cmd || true` and a comment. Do not hide errors with `2>/dev/null`.
8. Run `shellcheck -x script.sh` until clean. Fix the cause; use a disable comment only with a reason.
9. Test with file names that contain spaces, quotes and a leading dash, an unset variable and a failing middle command in a pipe.

## Rules

- Never add features while hardening.
- Use `--` before file arguments to commands that accept options.

## Report

Changes grouped by risk fixed, the shellcheck result, and the tests run.
