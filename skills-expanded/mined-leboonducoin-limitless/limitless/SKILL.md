---
name: limitless
description: Follow a real local agent task with Limitless keep-awake protection, or check the installed skill, hooks and power state when protection is unclear.
---

# Limitless

Limitless follows real task events from Codex, Claude Code, Cursor and Gemini CLI.
Tasks use one shared session through the installed hooks. Each task releases its
own request and keeps its own limits. Thinking, tool calls and waiting for delegated work remain
part of the turn. Detached work that outlives a turn needs its own explicit
session with the `run` or `watch` subcommand.

## Use the protected executable

```sh
{{LIMITLESS_CLI}}
```

Use this exact absolute executable with the subcommands below. If the path
is unavailable or setup has not filled it in, ask the user to finish
setting up the integration. Keep using the same path for all Limitless commands.

## Confirm protection

- Use `status --json` when the user asks whether the Mac is being kept
  awake. Check the helper's observed state, its fault and the session suspension
  reason. A hook event or an armed session alone cannot confirm protection.
- Use `doctor` when the helper is unavailable or a session stopped.
  Explain what was observed and give the user a specific next action. A cutoff
  ends protection while the underlying task continues.
- Use `setup PROVIDER --check` to verify the installed skill and hook
  files without editing them. For setup or repair requested by the user, follow
  the [provider instructions](https://github.com/leboonducoin/Limitless/blob/main/docs/cli.md#ai-agent-setup).
  Setup may require an agent restart and its normal hook approval.

## Respect session ownership

The app's power-source limits apply, with at least 20% battery reserved for agent
tasks. A manual session takes priority. Use the installed hooks as the sole
automatic source of task activity. Never synthesize lifecycle events, inspect
transcripts to infer activity, change power preferences, use sudo, or reacquire
protection after a stop. If cancellation was missed, tell the user how to stop
the session in Limitless.
