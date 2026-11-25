---
name: cmux-orchestration
description: >-
  Verified corrections and recipes for driving cmux agent fleets from the CLI
  (workspaces, panes, surfaces, send/read, notify, browser). Layers on top of
  the cmux-shipped skills (cmux-cli, cmux-workspace) with the gotchas that
  actually bite. Use when spawning or orchestrating cmux workspaces/panes/agents
  programmatically, building an agent team, driving cmux from an external
  terminal, or when a cmux CLI call returns "not_found: Surface not found",
  "Access denied", "Unsupported browser subcommand", or a deprecation hint.
---

# cmux-orchestration

Durable, machine-verified rules for driving cmux (manaflow-ai/cmux) agent fleets
over its Unix socket. The upstream `cmux-cli` and `cmux-workspace` skills are the
full reference, but they install as **unversioned real dirs that get wiped on
every cmux update** and they omit the footguns below. This file lives in dotfiles
(git-tracked, survives updates) and is the source of truth for the corrections.

Always discover exact syntax live first: `cmux --help`, `cmux <command> --help`,
`cmux docs api`. Then apply these rules. Set `CMUX_QUIET=1` to silence deprecation
hints. Run every mutation with `--focus false` so you never steal the user's focus.

## The #1 footgun: refs resolve relative to the CALLER workspace

Targeting a surface/pane in **another** workspace fails with
`not_found: Surface not found` unless you also pass `--workspace <ref>`. This bites
constantly once you have more than one workspace open.

```bash
# WRONG (resolves surface:5 inside the caller's workspace, which may not exist)
cmux send --surface surface:5 'ls\n'
# RIGHT
cmux send --workspace workspace:3 --surface surface:5 'ls\n'
```

## Correct vs wrong (all verified)

| Intent | Correct | Wrong / gotcha |
|---|---|---|
| Create/list/close workspace | `cmux workspace create\|list\|close` | `new-workspace` etc. still work but print a deprecation (use `CMUX_QUIET=1`) |
| Target another ws's surface | `... --workspace workspace:N --surface surface:M` | omit `--workspace` → `not_found: Surface not found` |
| Reference a workspace | `workspace:N`, numeric index, or uuid | by name (`--workspace "security fleet"`) → **silently empty** |
| Close one pane | `cmux close-surface --surface surface:M` | `close-pane` / `kill-pane` do not exist |
| Close everything | `cmux workspace close <ws>` / `cmux close-window` | (there is no bulk pane close) |
| Browser state/nav | `cmux browser <sub> --surface surface:M` | `--workspace …` → `Unsupported browser subcommand: --workspace` |
| N-pane grid | explicit `cmux new-split left\|right\|up\|down` calls | `--layout` JSON direction semantics are undocumented/unreliable |

## Core drive loop (topology + send + read)

```bash
export CMUX_QUIET=1
WS=$(cmux workspace create --name my-team --focus false)          # -> workspace:N
S=$(cmux list-pane-surfaces --workspace "$WS" --json | jq -r '.[0].ref')
cmux send        --workspace "$WS" --surface "$S" 'echo hello\n'   # send text (\n runs it)
cmux read-screen --workspace "$WS" --surface "$S" --lines 60       # read result back
```

## Deterministic grid via new-split (not --layout)

```bash
TL=$S
TR=$(cmux new-split right --workspace "$WS" --surface "$TL" --focus false)
BL=$(cmux new-split down  --workspace "$WS" --surface "$TL" --focus false)
BR=$(cmux new-split down  --workspace "$WS" --surface "$TR" --focus false)
cmux workspace rename "$WS" --title 'grid | TL:top TR:shell BL:counter BR:clock'
```

## Lifecycle, notify, teardown

```bash
cmux workspace rename "$WS" --title retired
cmux trigger-flash --workspace "$WS" --surface "$S"
cmux notify --workspace workspace:1 --title "fleet done" --body "winner: agent 3"
cmux close-surface --surface surface:M        # one pane
cmux workspace close "$WS"                     # whole team
```

## Running agents in a pane: headless vs interactive

**Headless** (one-shot, prints, exits): best for parallel fan-out you capture programmatically.

```bash
cmux send --surface "$S" 'Codex -p "your question" | tee /tmp/out.txt; echo DONE >> /tmp/out.txt\n'
# then poll /tmp/out.txt for DONE
```

**Interactive** (the video's "agents side by side": persistent, stateful REPL):

```bash
cmux send     --surface "$S" 'Codex\n'        # launch REPL (no -p)
# wait ~20-40s until the input box renders: a "❯" inside ─── rules with an
# "Opus 4.8 · bypass permissions" footer (it boots the full config first).
cmux send     --surface "$S" 'your prompt text' # types into the box; does NOT submit
cmux send-key --surface "$S" enter              # a SEPARATE Enter submits
cmux read-screen --surface "$S" --lines 45      # read the streaming answer
# follow-ups reuse the SAME session; context persists.
cmux send --surface "$S" '/exit'; cmux send-key --surface "$S" enter   # or close-surface
```

**Key rule for TUIs: `send` types, `send-key enter` submits.** Keep them separate;
a single `'...\n'` is unreliable for interactive agents (fine for plain shells).

## Driving cmux from an EXTERNAL terminal (Ghostty, not a cmux child)

Under the default `socketControlMode: cmuxOnly`, only processes started **inside**
cmux can connect ("Access denied — only processes started inside cmux can connect").
The robust, most-secure setup is to run the orchestrator as a Codex launched
inside a cmux terminal surface. If you must drive from an external terminal, set
`automation.socketControlMode` to `password` (or `full`) and **restart cmux** (the
mode is read at launch, not on config reload), then authenticate with `--password`
or `CMUX_SOCKET_PASSWORD`. When external, there is no caller workspace and no
`$CMUX_WORKSPACE_ID`: pass **explicit refs everywhere**.

## Config safety

`~/.config/cmux/cmux.json` is a stow symlink into dotfiles. **Never use the
`cmux-config` helper's `set`/`unset`** on it: its atomic write replaces the symlink
with a plain file and strips comments. Edit the dotfiles file directly. Reads
(`cmux-config` get/dump/validate, `cmux config doctor`) are safe.
