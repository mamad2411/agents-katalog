---
name: rotator
description: "Rotate to the next connected account with proven headroom when a usage limit hits. Triggers: /rotator, rotate the account, hit my session limit, hit the weekly limit, out of usage, switch account, no headroom left, which account has capacity. Uses the headroom CLI to pick the next eligible login in your configured preference order and cool the exhausted one down until its window resets."
---

# rotator

Rotate BETWEEN connected logins for the same provider when one hits a usage
limit. Powered by the `headroom` CLI (https://github.com/domanski-ai/headroom).

## When to fire

- The user types `/rotator` (optionally `/rotator <model>`, default `claude`).
- A command or session fails with a session/weekly/usage-limit or 429 error.
- The user asks which account has capacity, or says they are out of usage.

## What to do

1. Run `headroom rotate <model>` (default model family: `claude`).
   It cools the current account down until its window resets, picks the next
   login with PROVEN headroom, and prints the export line for the new account.
2. Relay the one-line result to the user exactly:
   `rotated <old> -> <new> (<family>); <old> cools until <reset>`.
3. If it exits 2, every account is limited. Report the earliest reset time it
   printed — never silently fail, never downgrade the model.
4. For a status view first, run `headroom status <model>` and show the table.

## Guardrails

- Never edit `~/.headroom/config.json` by hand from this skill; account
  changes go through `headroom connect` / `headroom setup`.
- Cooldowns are fail-closed: if headroom says nobody has proven capacity,
  believe it. Do not retry the limited account "just in case".
- The new account takes effect for NEW sessions/processes that inherit
  `CLAUDE_CONFIG_DIR` (or `CODEX_HOME`). The current interactive session keeps
  its own login; tell the user to restart the session if they want it moved.
