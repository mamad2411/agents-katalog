---
name: shell-script-standards
description: Write safe, portable shell scripts with error handling and clear control flow.
---

# Shell script standards

Without `set -euo pipefail` and quoting, a script keeps running after a failed command and an unset or word-split variable can delete or overwrite the wrong path. Run `shellcheck` in CI so these footguns fail the build, not production.

## Safety and error handling

- Start every script with `#!/bin/bash` or `#!/bin/sh` (portable).
- Always use `set -euo pipefail` at the top:
  - `set -e`: exit on error
  - `set -u`: error on undefined variables
  - `set -o pipefail`: exit if any command in a pipe fails
- Declare variables as `local` inside functions to avoid pollution.
- Quote all variables: `"$var"` not `$var` (prevents word splitting and globbing).

## Command substitution and utilities

- Use `$(command)` not backticks `` `command` ``.
- Never parse output of `ls`, `find`, `grep` in loops; use proper iteration.
- Prefer built-in tools: `parameter expansion` over `sed`, `printf` over `echo -e`.
- Always pass `--` before filenames in commands that accept it (e.g., `rm -- "$file"`).

## Readability and structure

- Use functions for logic >20 lines; name them with verbs: `check_dependencies()`, not `deps()`.
- Add comments explaining *why*, not *what* — code is readable, intent is not.
- Indent with two spaces; keep lines under 100 characters.
- Exit with meaningful codes: `0` on success, non-zero with a reason on failure.

## Validation

- Run scripts through `shellcheck` before committing; fix all warnings.
- Test on both `bash` and `sh` if portability is claimed.
- For scripts managing infrastructure, test with `set -x` to trace execution.
- Document required arguments and environment variables at the top of the script.

## Examples

```sh
# BAD — no shebang, no safety flags, unquoted variable
deploy() {
  cp $config /etc/app/
  service app restart
}

# GOOD — safety flags, quoted variables, meaningful exit code
#!/bin/bash
set -euo pipefail

# Usage: deploy.sh <config-path>
# Requires: APP_ENV (environment name)
deploy() {
  local config="$1"
  cp -- "$config" /etc/app/
  systemctl restart app || { echo "Failed to restart app"; exit 1; }
}

deploy "${1:?config path required}"
```
