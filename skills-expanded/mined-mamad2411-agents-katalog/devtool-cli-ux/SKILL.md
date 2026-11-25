---
name: devtool-cli-ux
description: CLI ergonomics specialist. Owns flag naming, output format, error messages, progress indicators, interactivity, and shell integration. Auto-invoked when designing or refining any CLI command, flag, or user-facing output.
---

# DevTool CLI UX

A CLI is an interface for tired people at 2am — and for scripts that never sleep.
Clear errors, predictable output, and pipe-safe behavior beat clever tricks every time.

## When to reach for this

- Naming a new command or flag, or reconciling inconsistent existing ones
- Writing user-facing output: errors, progress, tables, `--json` mode
- Deciding TTY vs non-TTY behavior, exit codes, or stdin/stdout/stderr discipline
- Adding shell completion, interactive prompts, or config-file support

## Principles

1. **Scriptable by default.** stdout is data, stderr is everything else (status,
   progress, warnings). `cmd | jq` and `cmd > out.txt` must never capture spinners.
2. **Human mode is layered on top.** Colors, spinners, and tables activate only when
   stdout is a TTY; also honor `NO_COLOR` and a `--no-color` flag. `--json` forces
   machine output regardless of TTY.
3. **Exit codes are an API.** 0 success, 1 generic failure, 2 usage error (matching
   getopt convention); document any others. Scripts branch on them — never reuse codes.
4. **Errors triage themselves.** Every error states what happened, why, and the next
   action — ideally the exact command to run. "Permission denied" is a stack trace;
   "Cannot write ~/.tool/config — run `tool init` or check ownership" is an error message.
5. **Confirm destructive actions, but never block automation.** Prompt on TTY; require
   `--yes`/`--force` when stdin is not a TTY instead of hanging or silently proceeding.
6. **Config precedence is boring and tested:** flag > env var > project config > user
   config > default. Document it once; cover it with a test per layer.
7. **Flags stay consistent across subcommands.** `--output`, `--quiet`, `--verbose`,
   `--yes` mean the same thing everywhere; short flags only for the most-used 4–5.

## Command UX checklist

- [ ] `--help` on every command/subcommand: one-line summary, usage, examples
- [ ] `--version` prints version to stdout and exits 0
- [ ] `--json` (or `--output json`) emits one parseable document, nothing else on stdout
- [ ] Non-TTY run: no color codes, no spinner frames, no interactive prompt hangs
- [ ] Exit codes documented and distinct per failure class
- [ ] Every error message includes a suggested next action
- [ ] Destructive commands prompt on TTY, require `--yes` otherwise
- [ ] Long operations (>2 s) show progress on stderr; silent under `--quiet`
- [ ] Completion scripts for bash/zsh/fish generated from the command definition,
      not hand-maintained
- [ ] `--` terminates flag parsing so positional args starting with `-` work

## Pitfalls

- Progress/log lines on stdout corrupting piped JSON — the classic `cmd | jq` failure
- Interactive prompt with no non-TTY fallback, hanging CI forever
- Renaming a flag without an aliased deprecation period (breaks every existing script)
- Color/spinner escape codes detected by checking an env var instead of `isatty()`
- Error text that restates the exception instead of the fix
- Exit code 0 on partial failure — automation can't see the problem

---
*Related: `devtool-library-api` (when the CLI wraps a public library surface),
`devtool-packaging` (completion-script install, distribution), `devtool-docgen`
(generated command reference) · domain agent: `devtool-architect` (command taxonomy,
versioning) · output/ADR format: `playbook-conventions`*
