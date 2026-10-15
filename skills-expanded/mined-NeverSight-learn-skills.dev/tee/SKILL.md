---
name: tee
description: >-
  Replaces the agent's reflex of piping a command straight through
  `tail -n N` or `head -n N` with `tee` to a file inside a
  `mktemp -d` directory followed by the same `tail` / `head`. The
  truncated view stays the same; the full output stays recoverable.
  Skipped for outputs expected to be very long.
when_to_use: >-
  Use whenever about to run a command from the `Bash` tool and the
  reflex is to add `| tail -n N` (or `| head -n N`) to keep the chat
  short — test suites, builds, linters, type-checkers, formatters,
  package installs, server boots, log readers. Triggers: «запусти
  тесты», «прогон», «билд», «линт», «логи», «вывод обрезается»,
  «не вижу всю ошибку», «run tests», «run the build», «check logs»,
  «output truncated», `| tail -n`, `| head -n`.
---

# tee

When the agent runs a command, piping straight to `tail -n N` keeps
the chat readable —
and silently drops every line above the tail,
including the first error of a cascading failure,
the warning that produced the summary,
or any earlier hint.

The fix is a one-token splice:
add `tee "$log"` before the `tail`/`head` stage
so the full output lands in a file inside a `mktemp -d` directory.
The visible slice stays exactly as it was.
The file is there for follow-up `Read`, `grep`, `tail`, `head`.

## Rule

```sh
log=$(mktemp -d)/out.log
cmd 2>&1 | tee "$log" | tail -n 100
echo "full log: $log"
```

- Allocate the directory with `mktemp -d`,
  not a hardcoded `/tmp/...` path —
  `mktemp -d` returns a unique private directory on stdout each call;
  hardcoded paths collide with concurrent runs
  and leftover state from prior ones.
- Redirect stderr to stdout (`2>&1`) before `tee`,
  so errors and warnings land in the file too.
- Pipe through `tail -n N` (or `head -n N`) for the visible slice;
  pick `tail` for failure tails and summaries,
  `head` when the first lines carry the signal.
- Print the full log path on the last line
  so the file can be re-opened with `Read`, `grep`, `tail`, `head`.

## When NOT to use

- **Short, bounded output.**
  The `| tail -n N` reflex was never needed —
  drop the pipe entirely
  (`git status`, `git rev-parse`, `command -v foo`,
  a single-line `jq` query).
- **Output expected to be very long** —
  e.g. `find /`, `grep -r` over a huge tree,
  verbose package installs that dump tens of MB.
  Capturing the full stream into a temp file fills disk for no real
  gain.
  Leave the command as the reflex would write it
  (`| tail -n N` and accept the loss),
  or narrow the output at the source first
  (`--quiet`, `--summary`, `-q`,
  per-tool filters).
- **Interactive commands** (`vim`, `less`, REPL) —
  pipes break their UI.
- **Output the human is following live** —
  e.g. a `tail -f` on a server log the user is reading.

## Examples

Bad — straight pipe to `tail` discards earlier output:

```sh
npm test 2>&1 | tail -n 100
```

Good — splice in `tee` to a temp file:

```sh
log=$(mktemp -d)/out.log
npm test 2>&1 | tee "$log" | tail -n 100
echo "full log: $log"
```

Same shape with `head` when the first lines carry the signal:

```sh
log=$(mktemp -d)/out.log
make build 2>&1 | tee "$log" | head -n 50
echo "full log: $log"
```

After the command, the printed path can be read directly —
e.g. widen the same slice (`tail`/`head` with a bigger `N`),
search by keyword (`grep`),
or read a known line range (`Read`):

```sh
tail -n 500 "$log"
head -n 200 "$log"
grep -nE 'error|fail|warning' "$log"
```

## Scope

Applies to commands the agent runs —
primarily `Bash` tool invocations
and shell snippets under `scripts/` that the agent itself executes.
Snippets shown to a human reader
(install instructions, copy-paste examples)
stay free of this pattern
unless the human asked for output capture too.
