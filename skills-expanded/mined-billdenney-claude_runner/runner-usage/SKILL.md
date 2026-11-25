---
name: runner-usage
description: |
  Use this skill when the user wants to see Claude Code's usage
  numbers — current 5-hour and 7-day utilization with reset times.
  Triggers: "/runner-usage", "show usage", "how much is left in the
  5h window?", "am I close to the weekly cap?", "what's my Claude
  usage?". Also triggers on parser-format-drift investigation:
  "format check", "/runner-format-check", "did the usage parser
  break?", "verify parser still works".
---

# /runner-usage — show + verify Claude usage

Two related modes, both backed by the same `claude-task-runner usage`
subcommand.

## Mode 1: render the current snapshot (default)

For "what's my usage?" / "/runner-usage" prompts:

1. Run `claude-task-runner usage render`. This spawns `claude /usage`
   under pyte, parses the rendered TUI, and prints a colored block
   with the 5-hour and 7-day windows + any per-model extra windows the
   plan exposes (e.g. "7-day Fable"). A plan with no 5-hour window
   shows "not reported" for it (ADR-0040).

2. Report the output as-is. The colors carry meaning (green < 70%,
   yellow 70-90%, red >= 90%) so don't paraphrase; show the rendered
   text.

3. Add a one-line interpretation for the user:
   - All green → "Plenty of headroom."
   - Yellow on 5h → "5h is in slowdown band; new dispatches will be
     throttled."
   - Red on either → "At/over cap; new dispatches blocked."

If the user wants JSON instead, run `claude-task-runner usage json`.

## Mode 2: drift / format check

For "/runner-format-check" / "did the parser break?" prompts:

1. Run `claude-task-runner usage healthcheck`. Exit codes signal:
   - `0` clean
   - `1` parse drift (TUI layout changed)
   - `2` capture timeout (claude didn't respond), or a usage error:
     with `--config` for a queue of several accounts, `--account` is
     missing or names no account (the output says `Invalid value for
     '--account'`)
   - `3` spawn error (claude binary missing)

   With `--config`, every `usage` command loads that TOML first. When
   it does not load, the command prints `configuration error: ...` and
   exits `78` (the content is wrong) or `1` (the file could not be read
   for now). So read exit `1` as parse drift only when the output does
   not start with `configuration error:`.

2. On non-zero, **don't try to fix the parser yourself**. Surface the
   exit code + stderr, and recommend:
   - Capture the raw output for forensics:
     `claude-task-runner usage capture --save /tmp/drift.cap`
   - Inspect with: `claude-task-runner usage parse-file /tmp/drift.cap`
   - File the result for the operator to update fixtures.

3. On clean exit, just report "PASS — usage parser is current."

## Account verification

If the user asks "which account am I reading?" or there's confusion
about whose usage is being shown, run
`claude-task-runner usage whoami`. This reports `subscriptionType`
(team / pro / max20 / etc.) and the welcome panel's org label so the
user can confirm.

`usage` reads one account. With `--config <queue>/claude_runner.toml`
that is the queue's only `[[accounts]]` entry; a queue of several needs
`--account <name>` before the subcommand (`usage --config ... --account
work whoami`), and without it the command stops with a usage error
(exit 2) naming the accounts.

## Settings to know

- Each `[[accounts]]` entry's `config_dir` selects whose credentials
  are used, for the supervisor's polls and for `usage`. With no
  `[[accounts]]`, the legacy `[claude].config_dir` does (empty means
  `~/.claude`); once `[[accounts]]` is declared, `[claude].config_dir`
  is ignored.
- `[usage].capture_usage_timeout_s` (default 15) bounds the wait for
  the `/usage` panel to finish its own fetch: its `Refreshing…` line
  gone and its closing line `Esc to cancel` alone. A capture that times
  out names what the panel still showed.
- `[usage].capture_post_data_pad_ms` (default 4000) is how long the
  capture keeps reading after that; the screen after it is read when it
  still shows every section.
