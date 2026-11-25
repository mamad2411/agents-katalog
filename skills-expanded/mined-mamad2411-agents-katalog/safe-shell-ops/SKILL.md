---
name: safe-shell-ops
description: Prevent shell quoting, heredoc, globbing, interpreter-boundary, and generated-file mistakes. Use when writing files through shell, generating Markdown/docs with backticks or dollar signs, creating temp scripts, running bash/zsh snippets, generating SSM RunShellScript or remote wrappers, or fixing failures caused by heredoc expansion, command substitution, word splitting, shell quoting, or the wrong shell parsing a payload.
---

# Safe Shell Ops

Use this skill before shell operations where quoting or generated files can fail.

## Default Decision

For file edits:

1. Use `apply_patch` for repo/docs/config/code edits.
2. Use a temp script under `~/.AGENTS-temp/<repo>/` only when execution logic is needed.
3. Use Python/Node only for structured transforms.
4. Use shell heredoc only for tiny low-risk temp files.

## Markdown / Docs Rule

Avoid writing Markdown that needs literal backticks or `$` when plain wording is enough.

If Markdown/docs must include shell-sensitive text such as backticks, `$VAR`,
`$(cmd)`, quotes, or placeholders:

- use `apply_patch`
- do not use inline `bash -lc 'cat <<EOF ...'`
- read the file back after writing

## Heredoc Rule

Do not put a quoted heredoc delimiter inside an outer single-quoted `bash -lc`
string.

Bad pattern:

```bash
bash -lc 'cat > file <<'EOF'
... text with `cmd` or $VAR ...
EOF'
```

Safer choices:

- `apply_patch`
- temp script created by `apply_patch`, then `bash -n`, then execute
- if a heredoc is truly needed, ensure the delimiter is quoted in the shell
  that actually receives it: `<<'EOF'`

## Script Rule

For edited or generated shell scripts:

1. write the script file first
2. run `bash -n <script>` or `zsh -n <script>`
3. execute only after syntax validation passes

## Command Rule

- Use explicit `shell=/bin/bash` and `login=false` for agent command execution
  unless testing zsh itself.
- Do not wrap a command in nested `bash -lc`; invoke the command directly or
  use one temporary Bash script for complex logic.
- Quote variable expansions.
- Prefer arrays over string-built commands.
- Avoid `eval`.
- Pass dynamic jq values with `--arg` (or `--argjson` for JSON), never by
  interpolating them into a jq program.
- Avoid complex one-liners; make a temporary script when logic grows past a
  few simple commands.

For infra mutation helpers, prefer invoking repo-owned Terraform/Terragrunt
commands or the owning repo cleanup runner over ad-hoc generated AWS CLI scripts.

## Remote And Generated Shell Boundary

A Bash agent shell does not prove that SSM RunShellScript, cloud-init, CI, SSH,
or another generated remote wrapper uses Bash.

Use two explicit layers:

1. Keep the outer wrapper POSIX-safe.
2. Stage the real Bash script separately, verify its checksum, validate it with
   `/usr/bin/bash -n`, and execute it with `/usr/bin/bash`.

Never place process substitution, arrays, `[[ ]]`, here-strings, or Bash
functions anywhere in a file parsed by `/bin/sh`, even after an
`exec /usr/bin/bash` line. The parser can reject the file before `exec` runs.

Validate both layers:

```text
/bin/sh -n outer-wrapper
/usr/bin/bash -n inner-script
```

For SSM, validate the final rendered `commands` payload in addition to the
source files. Preserve the terminal command status, stdout, stderr, and return
code as evidence.

## Prove the Assembled Execution Boundary

For changed remote commands, generated wrappers or shared helpers:

1. Inspect the **final rendered command** as the receiving shell will parse it,
   including line joins, quoting, exported environment and helper/prologue
   order. Syntax-check the exact outer and inner scripts with their real
   interpreters, then exercise the assembled boundary once with harmless
   fixture data. Syntax success alone misses runtime collisions.
2. Do not assume `HOME` exists in a non-login, SSM, CI or `sudo` environment.
   Resolve the effective user's home only when necessary; use a task-specific
   variable such as `effective_user_home`. Do not change login, credentials
   or global shell configuration to make the check pass.
3. Inspect `readonly` or globally assigned names across sourced helpers.
   A `local id` or `local name` may fail if the caller declared that name
   readonly. Prefer uniquely named immutable constants, and exercise the
   real shared-helper call path before declaring the correction proven.
4. When another process initializes state, wait for its documented **done**
   condition and absence of a still-running initializer, with a bounded
   timeout and first-failure evidence. A successful connection or `SELECT 1`
   may be too early for a dependent restore.
5. On failure, report the first failing operation and a fixed, sanitized
   error category with bounded context; keep raw secret-bearing output private.
   Bound diagnostic input, execution time and output. Do not impose a memory
   limit smaller than the already loaded interpreter's address space;
   classifier `MemoryError` is not workload evidence.

Follow the [shared testing policy](https://github.com/amitkarpe/dotfiles/blob/main/agent/.agent/TESTING.md):
zero new tests by default, one focused actual-boundary check for a concrete
defect, and stop after sufficient proof. No AWS calls or new orchestration
framework merely to check a generated shell command.

## Validation

Save time and tokens. Do not run validation/check commands for low-risk local
Markdown, context, notes, or response-file edits unless the user asks or the
change is about to be committed/pushed.

Run the smallest relevant check when risk is higher:

- `git diff --check` before commit/push/PR-ready handoff, or after suspicious
  patches and large multi-file edits
- `bash -n` for edited bash scripts
- `zsh -n` for edited zsh files
- targeted syntax/parsing checks for YAML, Terraform, code, or generated files
- read back generated text files only when they contain shell-sensitive
  characters or the write path was fragile
