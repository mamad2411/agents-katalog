---
name: claude-statusline
description: Install or customize the Claude Code status line — the one-line bar under the prompt that shows the model name, reasoning effort, current directory, git branch and dirty flag, and context used. Bundles a ready-made colorized bash script plus a one-command installer that wires up settings.json, and documents the stdin JSON contract so segments and colors can be changed with confidence. Use this whenever the user mentions their statusline / status line / statusLine setting, asks to show the model, effort level, working directory, git branch, or context percentage in their prompt bar, wants to restyle or reorder what is already there, wants the same status line set up on another machine or shared with a repo, or reports that their status line is blank, broken, or showing stale or wrong information — even when they never say the word "statusline".
---

# Claude Code status line

Claude Code renders a single line under the prompt by running a command you
choose, feeding it a JSON blob about the current session on stdin, and printing
the first line of stdout. This skill ships a known-good implementation of that
command and the pieces needed to install, verify, and modify it.

## What it renders

```
[Claude Opus 5 - high] preditor-lite  ⎇ main* | ctx 28% used
```

| Segment | Source | Behavior |
|---|---|---|
| `[Claude Opus 5` | `model.display_name` | magenta + bold, brackets included; falls back to `Claude` |
| `- high]` | `effort.level` | cyan, lowercased; the whole segment disappears on models that report no effort |
| `preditor-lite` | `workspace.current_dir` | blue, basename only |
| `⎇ main` | `git symbolic-ref` | green; absent outside a work tree |
| `*` | `git status --porcelain` | red, only when the tree is dirty |
| `ctx 28% used` | `context_window.remaining_percentage` | inverted to *used*; green under 50, yellow 50–79, red 80+ |

Every segment is conditional. That is deliberate — a status line that prints
empty brackets and stray separators when a field is missing is noisier than one
that shrinks, and missing fields are normal (no repo, no context data yet).

## Installing it

```bash
bash scripts/install.sh              # personal: ~/.claude/, applies to every project
bash scripts/install.sh --project    # ./.claude/, committed and shared with the repo
bash scripts/install.sh --dir DIR    # explicit target
```

The installer copies `assets/statusline-command.sh` into the target directory,
sets `statusLine` in that directory's `settings.json`, and prints a rendered
preview so a failure surfaces immediately. It backs up anything it replaces
with a `.bak-<timestamp>` suffix, rewrites only the `statusLine` key so the rest
of `settings.json` survives, and refuses to run rather than clobbering a
`settings.json` it cannot parse.

Prefer the installer over doing this by hand. Hand-editing JSON settings is
where this goes wrong: a trailing comma or a replaced-wholesale settings file
costs the user their other configuration, and the failure is silent.

Two things to tell the user afterward: the change takes effect in a **new**
session (or after `/statusline`), and the script needs `node` on PATH, which is
how it parses JSON without depending on `jq`.

## Verifying and iterating

```bash
bash scripts/preview.sh                       # renders ~/.claude/statusline-command.sh
bash scripts/preview.sh path/to/script.sh     # or any candidate
```

This renders the script against nine sample inputs — every field present, each
field missing, each context-color threshold, and malformed input — and prints
each result. Use it after **every** edit.

The reason to be disciplined here: when a status line command errors or exits
non-zero, Claude Code shows a blank line. There is no error message, no log the
user will find. A broken status line and a status line that has nothing to say
look identical, so the only way to know a change is good is to render it.

## How the script works

Claude Code pipes a JSON object to the command on stdin. The fields this script
reads:

```
model.display_name                       "Claude Opus 5"
workspace.current_dir                    absolute path
context_window.remaining_percentage      number, may be fractional
effort.level                             "high" | "medium" | "low" | absent
```

More fields are available than these. To see exactly what the running version
of Claude Code sends, capture one real invocation instead of guessing:

```bash
# temporarily point statusLine at this, start a session, then read the file
cat > /tmp/dump-statusline.sh <<'EOF'
#!/usr/bin/env bash
tee /tmp/statusline-input.json | node -e 'process.stdout.write("captured")'
EOF
```

The script's shape is three stages, and edits are easiest when you keep them:

1. **Parse once, in node.** A single `node -e` reads stdin and writes the
   fields it wants one per line; bash picks them apart with `sed -n 'Np'`.
   Rounding happens in node too — bash's `printf '%.0f'` interprets `72.4`
   against the shell locale and errors out wherever the decimal separator is a
   comma, which is a real bug that only appears on some machines.
2. **Collect state.** Git lookups use `--no-optional-locks` so a status line
   firing on every render never contends with a command the user is running.
3. **Assemble.** Named color variables, then string concatenation, one
   conditional per optional segment.

## Customizing

Edit the installed script, then run `preview.sh` on it. Common changes:

- **A color** — the palette is one block of named `$'\033[38;5;N'` variables
  with a comment naming each one's job. Change the number, not the call sites.
  256-color codes keep the line readable across terminal themes in a way that
  the 8 basic colors do not.
- **A segment's text or separator** — the assembly block near the bottom.
  Keep each optional segment inside its `[ -n "$var" ]` guard.
- **Context thresholds** — the `-ge 80` / `-ge 50` comparisons.
- **A new segment** — add the field to the node `process.stdout.write` line,
  add a matching `sed -n` extraction with the next line number, then append to
  `$parts` under a guard. Keep it cheap: this runs on every render, so no
  network calls and nothing that walks a large tree.

If a customization should survive a future reinstall, copy the edited script
back over `assets/statusline-command.sh` in this skill. Otherwise `install.sh`
will overwrite it — say so when handing customizations back, because the loss
would show up much later and look inexplicable.

## Notes

- Only the first line of stdout is displayed; anything on stderr is discarded.
- ANSI color and style codes work. Nothing interactive does — it is a printed
  line, not a widget.
- A project `.claude/settings.json` takes precedence over the personal one, so
  a `--project` install overrides a personal status line inside that repo.
- Claude Code also ships a built-in `statusline-setup` agent. It edits the
  user's script directly and is a fine way to make a small tweak; this skill is
  the reproducible path — a pinned script, an installer, and a renderer to
  check the result.
