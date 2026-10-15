---
name: bash-script
description: >
  Conventions for writing robust, safe shell scripts for system administration
  and automation. Use when creating or reviewing a bash or POSIX shell script,
  an automation script, a cron job, or a CI step, or when the user mentions
  shell scripts, bash, or "a script to automate" a task.
metadata:
  version: "1.0.0"
---

# Robust shell scripts

A shell script that runs unattended must fail loudly and predictably. Most
scripts that "work on my machine" are one unset variable away from doing
damage. These conventions close the common gaps.

## Script skeleton

Start every bash script from this shape:

```bash
#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# what-this-does.sh - one-line description

usage() {
    cat <<'EOF'
Usage: what-this-does.sh [options] <arg>

  -h, --help     Show this help and exit
  -v, --verbose  Print each step
EOF
}

main() {
    # script logic here
    :
}

main "$@"
```

What the header does:

- `set -e` - exit the moment a command fails instead of charging ahead.
- `set -u` - treat an unset variable as an error, not as an empty string.
  This is what stops `rm -rf "$DIR/"` from becoming `rm -rf /` when `DIR`
  is unset.
- `set -o pipefail` - a pipeline fails if any stage fails, not just the last.
- `IFS=$'\n\t'` - split on newline and tab only, so spaces in filenames do
  not break word splitting.

## Quoting

Quote every expansion. Unquoted expansions are the single largest source of
shell bugs.

```bash
cp "$src" "$dest"               # correct
cp $src $dest                   # wrong: breaks on spaces, globs

for f in "$dir"/*.log; do       # correct
    process "$f"
done

if [ -z "${VALUE:-}" ]; then    # safe even under set -u
    echo "VALUE is empty"
fi
```

Use `"${VAR:-default}"` to read a variable that may be unset without
tripping `set -u`.

## Argument parsing

Parse arguments explicitly. Do not rely on positional `$1` scattered through
the script.

```bash
verbose=0
while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help)    usage; exit 0 ;;
        -v|--verbose) verbose=1; shift ;;
        --)           shift; break ;;
        -*)           echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
        *)            break ;;
    esac
done

if [ $# -lt 1 ]; then
    echo "error: missing required argument" >&2
    usage >&2
    exit 2
fi
target="$1"
```

## Cleanup with trap

If a script creates temporary files, remove them on every exit path,
including failure and interruption:

```bash
tmpdir=$(mktemp -d)
cleanup() { rm -rf "$tmpdir"; }
trap cleanup EXIT

# ... work inside "$tmpdir" ...
```

`trap ... EXIT` runs the handler whether the script ends normally, hits
`set -e`, or is killed. Always create temp paths with `mktemp`, never a
fixed `/tmp/myfile` name.

## Errors and diagnostics

- Send errors and progress messages to stderr (`>&2`); keep stdout for the
  script's real output, so it can be piped.
- Give an error message that says what failed and what to do, then exit with
  a non-zero status. Reserve specific codes if callers need to branch on them.
- Check that required commands exist before using them:

```bash
for cmd in jq curl; do
    command -v "$cmd" >/dev/null 2>&1 || {
        echo "error: required command not found: $cmd" >&2
        exit 1
    }
done
```

## Idempotency

A script that may be re-run (cron, CI, retries) should reach the same end
state each time. "Create if missing" beats "create and fail if it exists".

```bash
mkdir -p "$target_dir"                       # no error if it exists
[ -f "$config" ] || cp "$default_config" "$config"
```

## Validate before you run

Lint every script with ShellCheck. It catches quoting bugs, unset variables,
and unsafe patterns before they reach production:

```bash
shellcheck what-this-does.sh
```

Format with `shfmt -w what-this-does.sh` for consistent indentation.

## When to stop using bash

Bash is right for gluing commands together and short automation. Move to
Python when the script needs data structures, real error handling, JSON or
HTTP work, or non-trivial string processing. A 200-line bash script with
nested logic is usually a Python script that has not been rewritten yet.

## Gotchas

- Without `set -u`, a typo in a variable name expands to empty and the script
  continues with wrong values. With it, the script stops.
- `set -e` does not trigger inside a command used as a condition
  (`if cmd; then`) or before `&&` / `||`. Do not assume it catches
  everything.
- A pipeline's exit status is the last command's unless `pipefail` is set.
  `false | true` succeeds without it.
- `cd` inside a script can fail silently. Use `cd "$dir" || exit 1`.
- Parsing `ls` output is fragile. Glob directly (`for f in *.txt`) or use
  `find ... -print0` with `read -d ''`.
- A fixed temp filename is a race and a collision risk. Use `mktemp`.
