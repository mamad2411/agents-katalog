---
name: shell-scripting
description: Writes, reviews and fixes shell scripts (bash and sh) so they are safe, portable and testable. Use whenever the user asks for a bash or sh script, shares one to review or debug, hits errors like unbound variable, command not found, bad interpreter or broken quoting, wants a script to run in Termux, Linux and macOS, or asks to automate a task from the command line, even if they only say "write me a script that does X". Lints with a script and uses a safe template with dry-run and cleanup.
---

# shell-scripting

Shell scripts fail in quiet, destructive ways: an empty variable in `rm -rf`, a failed `cd`, unquoted spaces. This skill writes scripts that stop early, clean up after themselves and can be tested without risk.

```
shell-scripting/
├── SKILL.md
├── scripts/
│   └── lint_shell.sh        syntax, CRLF, dangerous rm, unchecked cd, unquoted tests, eval, bashisms, shellcheck
└── references/
    └── safe-patterns.md     template, rules, pipefail pitfall, portability, args, logging, testing
```

## When to use

- Writing a new automation script
- Reviewing, debugging or hardening an existing script
- A script works on one machine but not another (Linux, macOS, Termux, `sh` versus `bash`)
- Errors about quoting, unbound variables, `\r`, interpreters or permissions

## Workflow

1. **Clarify the task** in one sentence: inputs, outputs, what may be deleted or changed, where it runs (Fedora, Termux, CI). Ask only what you cannot infer.
2. **Start from the template** in `references/safe-patterns.md`: strict mode, usage text, `--dry-run`, `mktemp` with `trap` cleanup, quoted expansions.
3. **Write small, named functions** and keep data on stdout and messages on stderr.
4. **Lint**: `bash scripts/lint_shell.sh script.sh` (or a folder). It checks syntax, CRLF line endings, `rm -rf` on variables, unchecked `cd`, unquoted tests, `for f in $(ls)`, `eval`, pipe to shell, bashisms in `#!/bin/sh`, and runs shellcheck when installed.
5. **Test safely**: run with `--dry-run`, then on a scratch directory, with an empty value, a path with spaces and a missing file. Say which of these you could not test.
6. **Explain risk** for any destructive step, and show the exact command to run and what output to expect.
7. **Know when to stop**: if the script needs JSON, data structures, retries or more than about 150 lines, recommend Python.

## Rules

- Always `set -euo pipefail` unless you handle errors explicitly and say why
- Quote every expansion; use `"${var:?}"` before deleting
- Never build commands from user input with `eval`; use arrays
- Do not use `sudo` inside scripts unless needed and documented; Termux has none
- Use `#!/usr/bin/env bash`; do not hardcode `/bin/bash`
- Avoid `cmd | grep -q` under `pipefail`; capture first or use a here-string
- Provide `--dry-run` for anything that deletes, overwrites or pushes
- Do not claim a script was run unless it was

## What to report back

| Field | Content |
|-------|---------|
| Script | the file, with usage and options |
| Safety | strict mode, dry run, cleanup, what it can delete |
| Lint result | findings fixed and any accepted, with reasons |
| Tested | the cases you ran, and the ones left to the user |
| Portability | where it runs and what would break elsewhere |

## Related skills

- `termux-setup`: running scripts on Android
- `linux-troubleshooting`: the commands worth turning into scripts
- `systematic-debugging`: when a script misbehaves and the cause is unclear
- `code-review`: review a script change before merging
