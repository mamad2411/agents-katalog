---
name: hunter-cli-probe
description: >-
  Drive a CLI or binary to hunt deviations and capture every invocation. Load
  when the target is a command-line tool and you must execute it, not read its
  source. Specifies the --help tree walk, exit-code correctness, stdin/stdout/
  stderr stream discipline, the flag-combination matrix, argument validation and
  error-message quality, idempotency and re-run safety, TTY vs piped behaviour,
  signal handling, and config-file precedence. Defines the argv+exit+streams
  artifact format. Use to probe a command, walk its subcommands, test flag
  combinations, check exit codes, or capture CLI evidence for a Sign or Trail.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Hunter CLI Probe

Assumes `hunter-doctrine` is loaded. A CLI deviation you cannot reproduce by
running the binary is not a Find. Reading the argument parser tells you what
should happen; this skill records what does. Every claim carries exact argv, the
exit code, and complete stdout and stderr.

## Inputs

- The binary/entrypoint and how to invoke it (path, package script, container).
- The declared contract when one exists: `--help` output, a man page, docs, or a
  recorded baseline of prior behaviour. Presence sets `hunt_mode = conformance`
  (help text is a spec the tool must honour); a baseline sets `regression`;
  absence leaves `defect`.
- A disposable working directory. **Assume every invocation may write, move, or
  delete files.** Run in an isolated temp dir seeded per case; never probe a
  destructive command against real user data.

## The invocation artifact

Every invocation is captured whole — the addressable evidence unit for every CLI
Sign and Trail. Store under `run/<hunt-id>/cli/<case-slug>/`:

```json
{
  "invocation_id": "cli/init/004",
  "at": "2026-08-07T14:02:11Z",
  "argv": ["mytool", "init", "--force", "./proj"],
  "cwd": "/tmp/hunt/cli/init-004",
  "env_overrides": { "MYTOOL_CONFIG": "/tmp/.../config.toml" },
  "stdin": "@stdin.txt",
  "tty": false,
  "exit_code": 0,
  "stdout": "@stdout.txt",
  "stderr": "@stderr.txt",
  "duration_ms": 143,
  "fs_effect": "@fs-diff.txt",
  "expectation": {
    "authority": "help:init",
    "expected_exit": 0,
    "expected": "creates ./proj with a config, prints the path to stdout"
  }
}
```

Capture pattern that keeps streams separate (never merge them — the split is
the probe):

```bash
mytool init --force ./proj >stdout.txt 2>stderr.txt; echo "exit=$?" >exit.txt
```

`fs_effect` is a diff of the working dir before/after (`find . -type f` snapshot
delta) whenever the command may touch the filesystem. A referenced stream file
must exist on disk; an absent one is a fabrication.

## Probe classes

### 1. --help tree walk

`--help` is the tool's own contract. Walk it exhaustively to build the surface
map:

1. Run the top-level `--help` (and `-h`, and no-args if it prints usage).
2. Enumerate every subcommand; recurse `--help` into each, and into their
   subcommands, to the leaves.
3. Record every subcommand and every documented flag as a surface. A flag that
   `--help` documents becomes an expectation you will probe; a subcommand you
   never ran is **dark**, never assumed working.
4. Deviation checks during the walk: `--help` that exits non-zero, that writes
   usage to stderr instead of stdout, subcommands mentioned in prose but absent
   from the tree, or flags documented but rejected when used.

### 2. Exit-code correctness

Exit codes are the CLI's contract with every script and CI pipeline. Verify:
- success path → `0`
- usage/argument error → a stable non-zero (conventionally `2`), not `1`
- runtime failure → non-zero, distinct from usage error where the tool claims to
  distinguish them
- `--help`/`--version` → `0`
A command that fails but exits `0`, or succeeds but exits non-zero, is a Sign —
it silently breaks `set -e` scripts and CI gates. Confirm the code matches any
documented exit-code table verbatim.

### 3. Stream discipline

stdout carries data; stderr carries diagnostics. Probe the split:
- machine output (the result) goes to **stdout** and is pipeable clean
- logs, progress, warnings, prompts go to **stderr**
- errors never leak onto stdout (would corrupt `| jq`, `| grep`)
- with `--quiet`/`--json`, stdout carries only the payload; no stray banner
A tool that prints its result to stderr, or mixes a progress spinner into piped
stdout, is a Sign. Verify by piping stdout alone and asserting it parses.

### 4. Flag-combination matrix

Single flags rarely break; combinations do. Build a matrix of the documented
flags and probe:
- each flag alone (baseline)
- mutually-exclusive pairs together (`--json --quiet`, `--verbose --silent`) —
  the tool must reject or define precedence, not silently pick one and mislead
- accumulating flags (`-vvv`), repeated flags (last-wins vs error), and
  `--flag=x` vs `--flag x` equivalence
- flags after positionals, and `--` end-of-options handling
The matrix denominator (combinations probed / combinations planned) is your flag
coverage fraction. Unprobed combinations are dark.

### 5. Argument validation and error messages

Send bad input per argument: missing required arg, unknown flag, wrong type
(string for int), out-of-range, nonexistent path, malformed value. Each must
produce a **non-zero exit and an actionable stderr message** naming what was
wrong and, ideally, how to fix it. Checks:
- unknown flag → clear error, not a stack trace or silent ignore
- missing required arg → names the missing arg, not "panic" / "index out of
  range"
- a raw language traceback on bad input is a Sign (poor UX and often
  information disclosure)

### 6. Idempotency and re-run safety

Run the same command twice in the same state and diff the effect:
- an `init`/`create` re-run must refuse cleanly or be a no-op, not corrupt or
  half-write
- `--force`/`--overwrite` must be the documented, opt-in path
- a command that succeeds once then errors or double-applies on identical re-run
  is a Sign
Capture both `fs_effect` diffs.

### 7. TTY vs piped behaviour

Many tools change behaviour on a pipe. Run each key command twice — once with a
TTY, once piped — and diff:

```bash
mytool ls                 # TTY: colour, table, pager acceptable
mytool ls | cat           # piped: must be plain, parseable, no ANSI, no pager hang
```

Deviations: ANSI colour codes leaking into piped output, a pager that blocks
waiting for a keypress under a pipe (hangs CI), or a prompt that has no non-
interactive path. A command that hangs when piped is CRITICAL.

### 8. Signal handling

Send `SIGINT` (Ctrl-C) and `SIGTERM` mid-run to a long-running command. Verify:
graceful shutdown, no half-written output file left behind, temp files cleaned,
and an exit code that signals interruption (conventionally `130` for SIGINT).
A tool that ignores SIGINT, or leaves a corrupt partial file, is a Sign.

### 9. Config-file precedence

When the tool reads config, probe the documented precedence chain — typically
**defaults < config file < environment variable < command-line flag**. Set a
conflicting value at each layer and assert the winning value:

```
config.toml: level = "info"
MYTOOL_LEVEL=debug
mytool run --level=warn      # expect: warn wins (flag > env > file)
```

A flag that loses to a config file, or an env var silently ignored, is a Sign.
Also probe: a missing config file (clean default vs crash), and a malformed
config file (actionable error vs traceback).

## Outputs

Per command, a Sign record referencing invocation artifacts:

```json
{
  "sign_id": "sign/2c9d",
  "surface": "mytool export (piped)",
  "observed": "prints ANSI colour codes to stdout when piped, breaking `| jq`",
  "raw_steps": ["mytool export --json | cat  -> stdout contains \\x1b[32m"],
  "authority": "implicit",
  "artifacts": ["cli/export-piped/stdout.txt", "cli/export-piped/exit.txt"],
  "probe_class": "tty-vs-piped"
}
```

Plus a per-surface coverage line as a real fraction, naming dark surfaces:
`cli coverage: 22/26 subcommands probed · flag matrix 40/58 · 4 dark
(migrate destructive-unauthorised, ...)`.

## Handoff

- Confirmed Signs → `hunter-repro`; `min_steps` become the exact argv the fixer
  replays under the recorded env.
- `--help` tree → the surface map / report coverage (§12 §2).
- `regression` Signs cite the baseline id as authority.

## Never

- **NEVER** run a destructive subcommand against real data; isolate in a temp
  dir, and escalate destructive-but-required cases via `hunter-ask`.
- **NEVER** merge stdout and stderr; the split is itself under test.
- **NEVER** mark an unrun subcommand or flag combination cold. Unprobed is dark.
- **NEVER** report from reading the argument parser. Only execution is evidence.
