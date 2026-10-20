---
name: shell-scripting-best-practices
description: >
  Writes robust, portable Bash/POSIX shell scripts for ops automation,
  covering strict-mode error handling (set -euo pipefail), correct
  quoting, trap-based cleanup, portability between bash and POSIX sh, and
  testing scripts with shellcheck and bats. Use when the user asks to
  "write a bash script to X," "make this shell script safer/more robust,"
  "this script fails silently / half-runs," "make this script POSIX
  portable," or "add tests/lint for a shell script."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: iac-and-automation-tooling
  maturity: stable
---

# Shell Scripting Best Practices

## Purpose

Shell scripts are the connective tissue of ops automation — glue between
CLI tools, CI steps, and cron jobs — but Bash's defaults are unsafe for
that role: a failed command doesn't stop the script, an unset variable
silently expands to empty, and a failure in the middle of a pipeline is
invisible unless explicitly checked. Getting the strict-mode/error-handling
foundation right is what separates a script that fails loudly and safely
from one that silently corrupts state, deletes the wrong path, or
half-completes a multi-step operation and leaves the system in an unknown
state.

## When to use

- Writing a new operational script (deployment helper, cleanup job, CI
  step, cron task) from scratch.
- Hardening an existing script that has failed unexpectedly, silently, or
  partially.
- Deciding whether a script needs to be portable to POSIX `sh` (e.g. for
  Alpine-based containers using `dash`, or minimal init systems) versus
  relying on Bash-only features.
- Adding lint/test coverage (`shellcheck`, `bats`) to a script before it's
  trusted in a production pipeline.
- Reviewing a script for destructive operations (`rm`, `mv`, bulk cloud
  CLI calls) before it runs unattended.

## Prerequisites & environment

- Bash ≥ 4.4 for `set -o pipefail` plus associative arrays and
  `${var@Q}`-style quoting expansions if used; Bash 3.2 (macOS's shipped
  default for a long time) lacks associative arrays entirely — confirm
  the target shell/version before relying on Bash 4+ features, or target
  POSIX `sh` explicitly if the script must run on minimal images.
- `shellcheck` (static analysis) and `shfmt` (formatting) installed
  locally and in CI.
- `bats-core` for behavioral tests when a script has any nontrivial logic
  (argument parsing, conditional branches, retry logic) worth asserting
  against.
- Know the actual execution environment: which shell `#!/bin/sh` resolves
  to (`dash` on Debian/Ubuntu, `bash` on many other distros, `busybox sh`
  in minimal containers) — behavior differs on `[[ ]]`, arrays, and
  `local`, none of which are POSIX.

## Step-by-step guidance

1. **Start every Bash script with strict mode and a clear shebang**:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   IFS=$'\n\t'
   ```
   - `set -e`: exit immediately if any command fails (returns non-zero),
     instead of continuing past it.
   - `set -u`: treat an unset variable as an error instead of silently
     expanding to an empty string — catches typos in variable names.
   - `set -o pipefail`: a pipeline (`cmd1 | cmd2`) fails if *any* stage
     fails, not just the last one — without this, `false | true` reports
     success.
   - `IFS=$'\n\t'`: narrows word-splitting to newlines/tabs instead of
     also splitting on spaces, reducing surprises when iterating over
     filenames.

2. **Quote every variable expansion and command substitution** unless
   word-splitting is explicitly wanted:
   ```bash
   # Wrong — breaks on filenames with spaces, and is subject to globbing
   rm -rf $target_dir/*

   # Right
   rm -rf -- "${target_dir:?}"/*
   ```
   `"${target_dir:?}"` fails loudly with an error if `target_dir` is
   unset or empty, instead of silently expanding `rm -rf /*` against the
   filesystem root — critical for any variable feeding a destructive
   command.
   > **Warning:** An unquoted variable in `rm`, `mv`, or similar is one of
   > the most common causes of catastrophic ops incidents. Always quote,
   > always use `:?` on any variable that gates a destructive path, and
   > prefer `--` before the path argument so a value starting with `-`
   > can't be parsed as a flag.

3. **Use traps for guaranteed cleanup**, so temp files/locks are removed
   even if the script exits early or is interrupted:
   ```bash
   tmp_dir="$(mktemp -d)"
   cleanup() {
     rm -rf -- "${tmp_dir}"
   }
   trap cleanup EXIT
   trap 'echo "Interrupted" >&2; exit 130' INT TERM
   ```
   The `EXIT` trap fires on normal exit, an error under `set -e`, or
   `exit` called explicitly — one cleanup path instead of duplicating
   cleanup logic before every possible exit point.

4. **Check preconditions explicitly instead of assuming they hold**:
   ```bash
   require_cmd() {
     command -v "$1" >/dev/null 2>&1 || {
       echo "Error: required command '$1' not found in PATH" >&2
       exit 1
     }
   }
   require_cmd aws
   require_cmd jq
   ```

5. **Handle errors with context, not just `set -e`'s bare exit.** For
   commands where failure needs a specific message or retry, check
   explicitly rather than relying only on strict mode:
   ```bash
   if ! aws s3 cp "${local_file}" "s3://${bucket}/${key}"; then
     echo "Error: failed to upload ${local_file} to s3://${bucket}/${key}" >&2
     exit 1
   fi
   ```
   For transient failures (network calls, cloud API rate limits), wrap
   with a bounded retry instead of failing on the first blip:
   ```bash
   retry() {
     local -r max_attempts="$1"; shift
     local attempt=1
     until "$@"; do
       if (( attempt >= max_attempts )); then
         echo "Error: '$*' failed after ${max_attempts} attempts" >&2
         return 1
       fi
       echo "Attempt ${attempt} failed, retrying in $((attempt * 2))s..." >&2
       sleep "$((attempt * 2))"
       (( attempt++ ))
     done
   }
   retry 3 aws s3 cp "${local_file}" "s3://${bucket}/${key}"
   ```

6. **Decide Bash vs. POSIX `sh` deliberately, not by accident.** If the
   script needs arrays, `[[ ]]`, `local -r`, process substitution, or
   `set -o pipefail`, it is a Bash script — use `#!/usr/bin/env bash` and
   don't claim POSIX compatibility. If it must run under a minimal `sh`
   (e.g. `dash` in an Alpine container's entrypoint), write to the POSIX
   subset deliberately:
   ```sh
   #!/bin/sh
   set -eu
   # No arrays, no [[ ]] — use [ ] and case statements instead.
   if [ -z "${TARGET_DIR:-}" ]; then
     echo "Error: TARGET_DIR must be set" >&2
     exit 1
   fi
   case "$1" in
     start|stop|restart) action="$1" ;;
     *) echo "Usage: $0 {start|stop|restart}" >&2; exit 2 ;;
   esac
   ```
   Note POSIX `sh` has no `pipefail` — check pipeline stages individually
   via `PIPESTATUS`-free patterns (e.g. write intermediate output to a
   temp file and check each command's exit status separately) if a
   pipeline's middle-stage failure must be caught.

7. **Lint and test before trusting a script in a pipeline**:
   ```bash
   shellcheck deploy.sh
   shfmt -d deploy.sh
   bats tests/deploy.bats
   ```
   A minimal `bats` test asserting both correct behavior and safe
   failure:
   ```bash
   # tests/deploy.bats
   @test "fails when TARGET_DIR is unset" {
     run env -u TARGET_DIR ./deploy.sh
     [ "$status" -ne 0 ]
     [[ "$output" == *"TARGET_DIR must be set"* ]]
   }

   @test "uploads the built artifact" {
     run env TARGET_DIR=/tmp/build ./deploy.sh
     [ "$status" -eq 0 ]
   }
   ```

## Best practices

- Prefer `$(...)` over backticks for command substitution — nestable and
  more readable, with identical semantics.
- Use `local` for every function-scoped variable in Bash so functions
  don't leak state into the caller's scope.
- Favor `printf` over `echo` when output must be exact/portable — `echo`'s
  handling of backslash escapes and flags differs across shells.
- Give scripts a `--dry-run` mode for anything destructive or
  state-changing, printing what would happen without executing it —
  mirrors the review-before-apply pattern used for
  `terraform plan`/CloudFormation change sets/`ansible-playbook --check`.
- Set explicit, descriptive exit codes (`exit 2` for usage errors, `exit 1`
  for runtime failures) instead of always `exit 1`, so calling automation
  (CI, cron alerting) can distinguish failure classes.
- Log to stderr for diagnostics/progress and reserve stdout for the
  script's actual output, so a script's output remains pipeable/parseable
  by other tools without diagnostic noise mixed in.
- Version-pin any tool a script shells out to when behavior differs
  across versions (e.g. `aws --version`, `jq --version` in a preflight
  check) rather than assuming whatever's on `PATH` behaves identically
  everywhere the script runs.
- For anything beyond simple glue logic — real data structures, HTTP
  calls with retries/backoff, structured logging, unit-testable business
  logic — reach for
  [python-automation-scripting-for-ops](../python-automation-scripting-for-ops/SKILL.md)
  instead of stretching Bash past what it's good at.

## Common pitfalls

- **Symptom:** A script deletes far more than intended after a variable
  ended up empty.
  **Fix:** This is the classic unquoted/unguarded `rm -rf $var/*` failure
  mode — `set -u` alone doesn't catch a variable that's *set but empty*.
  Use `"${var:?variable must be set}"` on any variable feeding a
  destructive command, quote every expansion, and add a `--dry-run` mode
  used for the first run against anything unfamiliar.

- **Symptom:** A script "succeeds" (exit code 0) but a step in the middle
  of a pipeline clearly failed based on the output.
  **Fix:** Missing `set -o pipefail` — without it, only the last
  command's exit status counts. Add `set -o pipefail`, and note it's
  Bash-only (not POSIX `sh`); for POSIX scripts, break the pipeline into
  separate steps with intermediate files/status checks.

- **Symptom:** A script that ran fine locally fails on a colleague's
  machine or in a minimal container with "command not found" for `[[` or
  arrays.
  **Fix:** The script is Bash-flavored but is being invoked via `sh` (a
  symlink to `dash`/`busybox` on many systems), or Bash-specific syntax
  leaked into a script declared `#!/bin/sh`. Make the shebang match the
  actual language used (`#!/usr/bin/env bash` for Bash features), and
  don't mix POSIX and Bash-only syntax in the same file.

- **Symptom:** A script silently continues after a command fails, even
  though `set -e` is present.
  **Fix:** `set -e` doesn't trigger inside `if`/`while` conditions, the
  left side of `&&`/`||`, or a pipeline's non-last stage without
  `pipefail` — these are well-known `set -e` blind spots. Check
  command results explicitly in those contexts rather than relying on
  `set -e` to catch everything.

- **Symptom:** Temp files pile up in `/tmp` after a script errors out
  partway through.
  **Fix:** Cleanup logic was only placed at the end of the script's
  "happy path," never reached on early exit. Move cleanup into an `EXIT`
  trap (step 3) so it always runs regardless of how/where the script
  exits.

## Worked example

**Scenario:** A deployment helper that packages a build directory, dry-run
capable, uploads to S3 with retry, and cleans up its temp workspace no
matter how it exits.

`deploy.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

usage() {
  echo "Usage: $0 [--dry-run] <build_dir> <s3_bucket>" >&2
  exit 2
}

dry_run=false
if [[ "${1:-}" == "--dry-run" ]]; then
  dry_run=true
  shift
fi

build_dir="${1:?build_dir is required}"
bucket="${2:?s3_bucket is required}"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Error: required command '$1' not found in PATH" >&2
    exit 1
  }
}
require_cmd aws
require_cmd tar

[[ -d "${build_dir}" ]] || { echo "Error: ${build_dir} is not a directory" >&2; exit 1; }

tmp_dir="$(mktemp -d)"
cleanup() { rm -rf -- "${tmp_dir}"; }
trap cleanup EXIT
trap 'echo "Interrupted" >&2; exit 130' INT TERM

archive="${tmp_dir}/build-$(date +%Y%m%d%H%M%S).tar.gz"
tar -czf "${archive}" -C "${build_dir}" .

retry() {
  local -r max_attempts="$1"; shift
  local attempt=1
  until "$@"; do
    if (( attempt >= max_attempts )); then
      echo "Error: '$*' failed after ${max_attempts} attempts" >&2
      return 1
    fi
    echo "Attempt ${attempt} failed, retrying in $((attempt * 2))s..." >&2
    sleep "$((attempt * 2))"
    (( attempt++ ))
  done
}

if "${dry_run}"; then
  echo "[dry-run] would upload ${archive} to s3://${bucket}/builds/"
else
  retry 3 aws s3 cp "${archive}" "s3://${bucket}/builds/"
  echo "Uploaded $(basename "${archive}") to s3://${bucket}/builds/"
fi
```

Lint and test:
```bash
shellcheck deploy.sh
bats tests/deploy.bats
```
```
tests/deploy.bats
@test "fails with usage error on missing args" {
  run ./deploy.sh
  [ "$status" -eq 2 ]
}

@test "dry-run does not call aws" {
  run ./deploy.sh --dry-run ./fixtures/build example-bucket
  [ "$status" -eq 0 ]
  [[ "$output" == *"[dry-run] would upload"* ]]
}
```

## Cross-references

- [python-automation-scripting-for-ops](../python-automation-scripting-for-ops/SKILL.md)
- [ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md)
- [aws-cloudformation-templates](../aws-cloudformation-templates/SKILL.md)
