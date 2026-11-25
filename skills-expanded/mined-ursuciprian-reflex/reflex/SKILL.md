---
name: reflex
description: How to work with the Reflex pre-execution gate in Claude Code or Codex CLI. Use when a shell command was denied or asked by Reflex, when unsure whether a shell command is risky before running it, or when the user asks what Reflex would have blocked in past sessions.
---

Reflex judges every shell command and subagent spawn before it runs (PreToolUse hook) and screens
web, MCP and Read results and user prompts for prompt injection. In the Claude Code plugin, run its
read-only scripts from the plugin directory, as below.
<!-- @reflex:setup-only begin -->
If a script path below is not an absolute
path (Codex CLI does not fill in the plugin root), the same commands are `reflex check`,
`reflex replay`, `reflex status` and `reflex report`, available after `npm install -g @ursuciprian/reflex`;
if `reflex` is not found, tell the user and do not search the disk for it.
<!-- @reflex:setup-only end -->

When to use which command:

- `"${CLAUDE_PLUGIN_ROOT}/scripts/check.sh" '<command>'`: before running a shell command whose risk
  is unclear (a delete, a push, a deploy, anything touching production or credentials), ask the gate
  how it would judge it. It only judges; it never runs the command. Quote the command in single quotes.
- `"${CLAUDE_PLUGIN_ROOT}/scripts/replay.sh" claude --since 7d`: when the user asks what Reflex would
  have blocked or asked in past sessions, or before switching from shadow to enforce mode. It reads
  transcripts; nothing runs.
- `"${CLAUDE_PLUGIN_ROOT}/scripts/status.sh"`: when the user asks whether Reflex is on, which mode it
  is in, or whether a plugin or `reflex setup` runs the hooks.
- `"${CLAUDE_PLUGIN_ROOT}/scripts/report.sh"`: what the gate decided recently.

When Reflex denies or asks for a command:

- Read the reason in the hook message. Do not retry the same command with small changes to get past a
  rule, and do not wrap it in a script, an `eval`, another shell or a different tool to avoid the gate.
- Explain the decision to the user and offer a safer alternative, or let the user run it themselves.

Never change Reflex's own configuration: do not edit `~/.config/reflex/`, the Claude Code settings
files, `~/.codex/hooks.json` or `~/.codex/config.toml`, or the plugin's files, and do not run
`reflex setup`, `reflex install`, `reflex uninstall`, `reflex queue approve|deny|clear`,
`reflex suggest --write`, or the `claude plugin` and `codex plugin` commands that disable or remove
it. Those are the user's decisions. The plugin's mode, engine and key are its options (`/plugin`,
reflex, Configure); show the user where to change them instead.
