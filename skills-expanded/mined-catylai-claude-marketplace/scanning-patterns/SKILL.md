---
name: scanning-patterns
description: "Use when writing a regex or grep detection pattern for a hook, lint rule or review check, or wiring a scanner into a shell script. Prefer an existing tool, prove the pattern fires, and keep scripts portable. Not for running a security audit (use dev-guardrails:security-scan)."
license: MIT
---

# Scanning Patterns

## Run the tool when one covers the case

A linter or scanner gives a rule id, a location and a documentation link per finding; a
hand-written grep gives a line. Write a pattern only for what no installed tool covers, and say
which tool is missing when you do: "no TS linter is installed here" is useful review context,
while a silent fallback to grep hides a gap.

| Class of finding | Tool |
| --- | --- |
| Credentials, private keys | A secret scanner (`gitleaks`, `trivy fs --scanners secret`) |
| Python injection, `shell=True`, bare `except` | `bandit`, `ruff` |
| Shell quoting and portability | `shellcheck` |
| Infrastructure-as-code misconfiguration | `tflint`, `checkov` |
| TypeScript/JavaScript correctness | `tsc --noEmit`, `eslint` |

Scope a scan to the changed files (see `file-scope-rules` for why pre-existing code is out of
scope). In Claude Code, the Grep and Glob tools take a path list directly.

### Wiring a scanner into a script

Check presence with an explicit `if`, because `A && B || C` is `(A && B) || C`: when the scanner
runs and finds something, `B` exits non-zero, `C` runs, and the finding is reported as a missing
tool with exit 0.

```sh
if command -v gitleaks >/dev/null 2>&1; then
    gitleaks dir . --redact --no-banner
else
    echo "gitleaks not installed: secret scan SKIPPED" >&2
fi
```

Three more team rules for any script or hook that wraps a scanner:

- **Portable to bash 3.2 and zsh.** macOS ships bash 3.2, so leave out bash-4 features
  (associative arrays, `${var,,}`, `mapfile`) and use `#!/usr/bin/env bash`, not `/bin/bash`.
- **Strict mode by role.** A script starts with `set -euo pipefail`. A hook uses
  `set -uo pipefail` without `-e`, because it must reach its own `exit 0` / `exit 2` decision
  instead of dying on the first non-zero command (a scanner reporting a finding, for instance).
- **Parse user-authored JSON with python3 in non-strict mode, not jq.** A field carrying user text
  (a commit title, an MR description, a comment body) can hold raw control characters. jq rejects
  them at parse time, and so does Python's `json` by default, so the pipeline fails on some records
  and not others. Save the response to a temp file and read it with
  `python3 -c 'import json,sys; d=json.loads(open(sys.argv[1]).read(), strict=False); ...' "$tmp"`.
  Keep jq for JSON your own code produced.

## Validate every pattern you write

A pattern that has never been shown to fire reads as coverage while providing none. Before
keeping one, prove both halves with fixtures committed beside it:

- it matches a fixture that should match;
- it stays silent on a fixture that should not.

Three failure modes account for most broken patterns:

- **`\n` inside a line-oriented pattern.** `grep` matches one line at a time, so
  `async def.*:\n.*open\(` can never fire. Use a parser, `rg -U` for multiline, or `grep -A` plus
  a second filter.
- **PCRE syntax in `grep -E`.** Lookaround (`(?!…)`, `(?<=…)`) is not POSIX ERE. GNU grep
  misreads some of it and BSD grep on macOS exits 2 with `repetition-operator operand invalid`,
  so the pattern never ran. Use `grep -P` or `rg -P`, and check the exit code.
- **Patterns that match ordinary code.** `\.(all|filter)\(\)` flags routine ORM use. If the hit
  rate on healthy code is not near zero, it is not a detector.

Treat exit codes as three states: `grep` and `rg` return 0 on a match, 1 on no match, and 2 on
error. A caller that reads 2 as "clean" lets a broken pattern report success forever.

## Verify

Run the pattern against both fixtures and confirm exit 0 on the positive, exit 1 on the
negative, and never exit 2.

Without a checkout, review a pasted pattern and fixtures by reading, and give the user the fixture
commands to run.
