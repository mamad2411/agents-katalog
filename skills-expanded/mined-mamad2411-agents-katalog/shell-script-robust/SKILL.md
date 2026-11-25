---
name: shell-script-robust
description: Writes and reviews production-grade Bash/POSIX shell scripts with safety rails — set -euo pipefail, quoting, trap cleanup, shellcheck-clean, idempotency, and clear error handling. Triggers when authoring or hardening a shell/automation script, fixing a fragile script, or a shellcheck failure.
when_to_use: เขียน/แก้ bash script, automation/glue script เปราะ, ต้องการ shellcheck-clean หรือ idempotent
---

## When to Use

- Authoring a new Bash/POSIX script (CI step, deploy glue, cron job, build wrapper).
- Hardening a fragile script: silent failures, partial runs, "works on my machine", race on temp files.
- A `shellcheck` run reports SC-codes and the script must pass clean.
- Making a script safe to re-run (idempotent) or adding a `--dry-run` path.

Do NOT use for: one-off interactive commands, or when the task is genuinely a 3-line throwaway that nobody re-runs.

## Steps

1. **Pick the interpreter, declare it.** Bash unless POSIX `sh` is required (Alpine/BusyBox, `/bin/sh`-only targets). Shebang `#!/usr/bin/env bash` (or `#!/bin/sh` for POSIX). For Bash, set the strict header as the first executable lines:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   IFS=$'\n\t'
   ```
   - `-e` exit on error, `-u` error on unset var, `-o pipefail` so `a | b` fails if `a` fails. `IFS=$'\n\t'` removes space as a field separator → kills most word-splitting bugs.
   - POSIX `sh` has no `pipefail`/`set -o`; use `set -eu` only and check pipe exit manually.

2. **Quote every expansion.** `"$var"`, `"$@"` (never `$*` for arg lists), `"${arr[@]}"`, `"$(cmd)"`. Unquoted `$x` undergoes word-splitting + glob expansion — the #1 source of breakage on paths with spaces. Use `"${var:?missing VAR}"` to fail loud on required vars, `"${var:-default}"` for optional.

3. **Set up trap cleanup before creating any temp/lock.** Create temp via `mktemp`, register cleanup that runs on every exit path:
   ```bash
   tmpdir="$(mktemp -d)"
   cleanup() { rm -rf "$tmpdir"; }
   trap cleanup EXIT INT TERM
   ```
   - `EXIT` covers normal + error exit; add `INT TERM` so Ctrl-C / kill also cleans. For a lock dir/file use the same pattern so a crash never leaves a stale lock.

4. **Handle errors with meaningful exit codes + usage.** Reserve distinct codes (`64` usage, `65` data error, `69` unavailable, `1` generic — or your own scheme, documented). Add a `usage()` and `die()`:
   ```bash
   die() { printf 'error: %s\n' "$*" >&2; exit 1; }
   usage() { printf 'usage: %s [--dry-run] <arg>\n' "$0" >&2; exit 64; }
   ```
   - Write diagnostics to **stderr** (`>&2`), data to stdout, so the script composes in pipelines. Check command presence up front: `command -v jq >/dev/null || die "jq not found"`.

5. **Make it idempotent + add `--dry-run`.** Re-running must not double-apply or fail. Guard mutations: `[ -d "$d" ] || mkdir -p "$d"`, `mkdir -p` over bare `mkdir`, `ln -sfn`, append only if the line is absent (`grep -qF -- "$line" "$f" || printf '%s\n' "$line" >> "$f"`). Thread a `DRY_RUN` flag and a `run()` wrapper:
   ```bash
   run() { if [ -n "${DRY_RUN:-}" ]; then printf '+ %s\n' "$*"; else "$@"; fi; }
   ```

6. **Run shellcheck until clean; lock down portability.** `shellcheck -x script.sh` (and `-s sh` if targeting POSIX). Fix at root cause — don't blanket-disable. Only add a scoped `# shellcheck disable=SCXXXX` with a one-line reason directly above the offending line. Bash-only features (arrays, `[[ ]]`, `${var//}`, `local`) are invalid in POSIX `sh` — if shebang is `/bin/sh`, shellcheck `-s sh` will flag them; either switch to Bash or rewrite.

7. **Test with real + edge inputs.** Run against: a path with spaces, an empty arg, a missing file, and a second consecutive run (idempotency). Verify exit codes (`echo $?`). For destructive scripts, prove `--dry-run` makes zero changes before running for real.

## Common Errors

- **`set -e` doesn't fire where you expect.** It's suppressed inside `if`/`while`/`&&`/`||` conditions and for the left side of a pipe (without `pipefail`). A failing command in `cmd | grep x` is invisible without `-o pipefail`. Also `local x=$(cmd)` masks `cmd`'s exit status (the `local` succeeds) — split into `local x; x=$(cmd)`.
- **Unquoted `$(...)` in a `for`.** `for f in $(ls)` breaks on spaces/newlines and globs. Use `for f in *.txt` (glob, with `shopt -s nullglob` so no-match expands to nothing) or `find ... -print0 | while IFS= read -r -d '' f`.
- **`read` eats backslashes / trims whitespace.** Always `read -r`, and `IFS= read -r line` to preserve leading/trailing spaces.
- **`cd` without guard.** `cd "$dir" && do_thing` — if the bare `cd` fails under `set -e` you may still be in the wrong dir. Guard it: `cd "$dir" || die "cd failed"`.
- **`rm -rf "$base/$sub"` with unset vars.** If `base` is empty, this can become `rm -rf /...`. `set -u` + `"${base:?}"` prevents the empty-expansion footgun. Never `rm -rf` a variable you didn't validate.
- **`trap` registered after the temp is made.** If creation succeeds but the next line fails, cleanup never registered → leak. Register the trap immediately after `mktemp`.
- **`echo` with flags/backslashes is non-portable.** Prefer `printf '%s\n' "$x"`.
- **Shebang lies.** `#!/bin/sh` + bash arrays → silently broken on dash. Match shebang to the features you actually use.

## Verify

- `shellcheck -x script.sh` (add `-s sh` for POSIX targets) → zero warnings, or only scoped disables each with a reason comment.
- `bash -n script.sh` parses clean (syntax check, no execution).
- Run the strict header check: confirm `set -euo pipefail` (Bash) is present and the script still completes on valid input.
- Idempotency: run twice in a row → second run is a no-op or succeeds identically; no stale temp/lock left behind (`ls` the temp dir after — gone).
- Edge inputs pass: path with a space, missing required arg exits non-zero with usage on stderr, `--dry-run` produces zero side effects.
- `command -v` preflight catches missing dependencies before any mutation runs.
