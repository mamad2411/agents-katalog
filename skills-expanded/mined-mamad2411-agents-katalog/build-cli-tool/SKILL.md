---
name: build-cli-tool
description: Designs the UX and contract of a command-line program in any language — argument parsing via a real lib (commander/yargs, click/typer, cobra, clap), meaningful exit codes, the stdout=data / stderr=logs split so the tool pipes cleanly, TTY-aware color/spinners that auto-plain when redirected, a --json machine mode, layered config precedence, signal cleanup, and shell completion. Covers the whole interface contract that makes a CLI scriptable, composable, and safe — not the language-internal logic.
when_to_use: Building a new CLI/terminal program or fixing one that misbehaves in pipes, CI, or non-TTY contexts (logs on stdout, colors in files, wrong exit codes, secrets in flags). Distinct from shell-script-robust (writing a robust Bash script — set -euo pipefail, quoting, traps; this skill DESIGNS the CLI program/UX in any language) and publish-package-registry (PUBLISHING the finished tool to npm/PyPI/crates; this skill DESIGNS it).
---

## When to Use

- "I'm writing a CLI — how should I structure subcommands, flags, and help?"
- "My tool breaks when I pipe it (`tool | jq`) or redirect to a file — output is garbled / has color codes."
- "CI can't tell why my command failed — every error exits 1."
- "I need a `--json` mode so scripts can parse my output."
- "Colors/spinners show up in log files but shouldn't" / "respect `NO_COLOR`."
- "How do I take a secret without it leaking in `ps` / shell history?"
- "Add shell completion / a `--dry-run` / proper Ctrl-C cleanup."

NOT this skill:
- Writing a robust **Bash** script (strict mode, quoting, trap cleanup) → **shell-script-robust** (that's a shell *implementation*; this is CLI *interface design* in any language).
- **Publishing** the built tool to npm/PyPI/crates (bin field, OIDC, semver) → **publish-package-registry**.
- The exact **wording** of a failure string (what/why/next) → **error-message** (use it for message copy; this skill decides the *channel* and *exit code*).
- Choosing **names** for commands/flags/config keys → **naming-helper**.
- Hardening the language-internal correctness (concurrency, types, money math) → the respective domain skills.

## Steps

The contract in one line: **stdout = data, stderr = everything else, exit code = the verdict.** Get those three right and the tool composes with Unix.

1. **Pick a parser library, never hand-roll.** Hand-rolled `process.argv` parsing misses `--`, `=`, bundled short flags, and negation. Use the idiomatic one:

   | Lang | Library | Notes |
   |---|---|---|
   | Node | **commander** (simple) / **yargs** (rich) / **clipanion** (class-based, typed) | commander for most; yargs for middleware/completion |
   | Python | **typer** (type-hint driven) / **click** / `argparse` (stdlib, zero-dep) | typer = click + types; argparse if no deps allowed |
   | Go | **cobra** (+ pflag/viper) | kubectl/gh use it; gives completion + config for free |
   | Rust | **clap** (derive) | derive macro → struct = the CLI |

   Define subcommands (`tool sync`, `tool config get`), flags with **both short and long** (`-v/--verbose`), positionals, and let the lib handle `--` (everything after it is a positional, never a flag — so `rm -- -weird-file`). Support `--flag=value` and `--flag value`.

2. **Generate `--help` and include examples + a one-line summary.** Every command and subcommand needs `--help`; the lib auto-generates usage from the spec — your job is to add a one-line summary and **real examples** (most help is useless without them):
   ```
   sync — mirror a local dir to remote storage

   Usage: tool sync [options] <src> <dest>
   Examples:
     tool sync ./build s3://bucket/site      # one-shot
     tool sync --dry-run ./build s3://...    # preview, no writes
   ```
   Provide `--version` (print version + exit 0). Unknown flag → usage error on **stderr** + exit 2, not a stack trace.

3. **Define exit codes that mean something.** Scripts and CI branch on `$?`. Don't return 1 for everything:

   | Code | Meaning |
   |---|---|
   | 0 | success |
   | 1 | generic/expected failure (operation didn't succeed) |
   | 2 | **usage error** (bad flag/arg) — convention; argparse/clap use it |
   | 3+ | distinct codes per failure class (e.g. 3 = network, 4 = auth, 5 = not-found) — document them |
   | 130 | interrupted by SIGINT (128 + 2); 143 for SIGTERM (128 + 15) |

   Document the table in `--help` or the README so callers can `case $? in ...`.

4. **Enforce stdout=data / stderr=logs (the cardinal rule).** Primary results → **stdout**. Logs, progress, spinners, prompts, warnings, errors → **stderr**. This is what makes `tool | jq`, `tool > out.json`, and `tool 2>/dev/null` work. **Never** print a log line, banner, or "✓ done" to stdout — it corrupts the data stream. A `--quiet` run with a clean pipe should emit *only* the payload on stdout.

5. **Detect TTY; degrade gracefully when not interactive.** Color, spinners, progress bars, and interactive prompts are only valid on a terminal. Check before emitting them:
   - Node: `process.stdout.isTTY` / `process.stderr.isTTY`
   - Python: `sys.stdout.isatty()`
   - Go: `term.IsTerminal(int(os.Stdout.Fd()))`

   Piped/redirected (not a TTY) → auto-plain: no ANSI, no spinner, no prompt (instead error: "stdin is not a tty; pass --yes or --input"). Honor env + flag precedence for color: **`--color=never` > `NO_COLOR` (any value disables) > `--color=always`/`FORCE_COLOR` > `--color=auto` (default: color only if stdout isTTY).**

6. **Add a `--json` / machine-readable mode.** Human tables for the TTY, structured output for scripts. `--json` emits one JSON document (or NDJSON per record for streams) to stdout, *nothing else* — no log noise, no color. This is more robust than asking users to `grep`/`awk` your pretty output. Keep the schema stable; version it if it may change.

7. **Stream output; don't buffer huge results.** Write records as you produce them (NDJSON line-by-line, or flush rows incrementally) so `tool export | head` exits fast and memory stays flat on large datasets. Buffering everything then printing at the end breaks `head`/`less` and OOMs on big runs.

8. **Layer config with a documented precedence.** Highest wins, document the order:
   ```
   CLI flags  >  env vars  >  project config (./.toolrc)  >  user config (~/.config/tool/config.toml)  >  built-in defaults
   ```
   viper (Go), a small merge (Node/Python), or click's `auto_envvar_prefix` give this. Print the resolved source on `--verbose` so users can debug "why is this value set?".

9. **Never accept secrets as CLI flags.** `--password hunter2` leaks into `ps aux`, shell history, and CI logs. Accept secrets via **env var** (`TOOL_TOKEN`), a **file** (`--token-file`), or **stdin** (`--password-stdin`, like `docker login`). If a flag like `--token` must exist, mark it deprecated and warn on use.

10. **Handle signals and clean up.** On SIGINT/SIGTERM: remove temp files, restore terminal state (cursor, raw mode, `\e[?25h` to show cursor), flush partial output, then exit 130/143 — don't leave a half-written file or a hidden cursor. Node: `process.on('SIGINT', cleanup)`; Python: `signal.signal` / `try/finally` + `KeyboardInterrupt`; Go: `signal.NotifyContext`. Make operations idempotent so a re-run after interruption is safe.

11. **Verbosity, dry-run, and destructive guards.** Levels: `-q/--quiet` (errors only), default, `-v`, `-vv` (stackable → log level). Destructive actions (`delete`, `reset`, overwrite) require `--dry-run` (print exactly what *would* happen, change nothing) and either an interactive confirm (TTY only) or an explicit `--yes`/`--force` for non-interactive use. Prefer idempotent operations so partial failures are recoverable.

12. **Ship shell completion + handle cross-platform.** Generate completion for bash/zsh/fish (cobra/clap/yargs do this; expose `tool completion zsh`). Cross-platform care: use the lib's path join (not hard-coded `/`), write `\n` not `\r\n` to data streams, and on Windows enable ANSI (modern terminals support it; older need a `colorama`-style shim or `FORCE_COLOR`). Distribution is a separate step — `bin` in package.json + npx, `pipx`, a single static binary (Go/Rust), or a Homebrew formula — but PUBLISHING is **publish-package-registry**.

## Common Errors

- **Logs on stdout.** A `console.log("Done!")` or progress bar to stdout silently corrupts `tool | jq` and `tool > file`. The single most common CLI bug — route all non-data to stderr.
- **Everything exits 1.** CI can't distinguish "bad input" from "network down". Use distinct codes (Step 3) and 2 for usage errors.
- **Color codes in files.** Forgetting the isTTY check writes raw `\e[31m` into redirected output. Auto-plain when not a TTY; honor `NO_COLOR`.
- **Secret in a flag.** `--api-key sk-...` is visible to every user via `ps` and saved in `~/.zsh_history`. Use env/file/stdin (Step 9).
- **Buffering huge output** then printing at the end → `head` hangs, memory blows up. Stream (Step 7).
- **No `--` handling** → `tool rm -weird-name` treats the filename as a flag. The parser lib handles `--`; don't hand-roll past it.
- **Prompting in a non-TTY** → CI hangs forever waiting on stdin. Detect TTY; require `--yes`/`--input` otherwise.
- **Leaving temp files / a hidden cursor on Ctrl-C** — register signal cleanup (Step 10) before creating temps.

## Verify

- `tool sub --json | jq .` succeeds and `tool sub > out.txt` produces clean data — **zero** log lines or ANSI in stdout.
- `tool sub 2>/dev/null` still prints the full payload; `tool sub >/dev/null` still shows progress (proves the stream split).
- `tool --color=never | cat` has no escape codes; `NO_COLOR=1 tool` is plain; piped output auto-plains without any flag.
- Bad flag → exit 2 + usage on stderr; a real failure → documented non-zero code; success → 0. `echo $?` after each.
- Ctrl-C mid-run → exit 130, no temp file left, cursor visible, terminal usable.
- `ps aux | grep tool` during a run shows **no** secret; `--help` lists examples, exit codes, and config precedence.
- `tool completion zsh` emits a valid script; a non-TTY run with a destructive command refuses without `--yes`/`--dry-run`.
