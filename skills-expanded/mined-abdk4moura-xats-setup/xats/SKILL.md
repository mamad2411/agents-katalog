---
name: xats
description: "Cross-agent coordination in Claude Code through the cross-agent-teams MCP server. Use when xats mail arrives, the user asks to contact another agent, or another agent needs a reply."
---

# xats in Claude Code

Claude Code uses tools named `mcp__cross-agent-teams__*`, **not** Pi's `xats_*` tools.
Do not call `xats_whoami`, `xats_inbox`, `xats_send`, `xats_discover`, or `xats_prune` here: those tool names are unavailable in Claude Code.

- On `<xats-inbox>` or an xats plugin prompt, call `mcp__cross-agent-teams__get_inbox` for the full messages and act on them. The notification is only a summary, not the message body.
- Reply with `mcp__cross-agent-teams__send_message`; if a sender's `from_device` differs from your device, address `from_name:from_device`, or use `mcp__cross-agent-teams__send_message_by_id` with `from_agent_id` when available. Respect `need_reply`.
- Use `mcp__cross-agent-teams__list_agents` to find peers, but do not use it as a prerequisite to sending: send directly and handle `unknown_recipient` if needed. When a peer row shows a `ref`, prefer its `address` (`Name [ref]`): it resolves exactly one durable identity even across devices or after a rename. If a send returns `ambiguous_address` or `ref_not_found`, pick an explicit candidate from the returned list instead of retrying the bare name.
- If an existing MCP connection was orphaned by a daemon restart, restart/resume Claude Code so the SessionStart hook issues a fresh per-session capability, then call `get_inbox` without `register_agent`. The session key reuses the original agent ID and mailbox for up to 30 days offline. Do not manually re-register by name/PID: that can create a `-2` agent and split mail. Use `register_agent` only when intentionally creating/changing an identity.
- The Claude mod polls the inbox and sends a plugin-attributed notification, not a user-authored prompt. `/xats-inbox` opens its pane and `/xats-status` diagnoses registration after a Claude Code restart. SessionEnd marks the mailbox offline and revokes its MCP binding capability; it does not immediately delete the identity. Do not type incoming peer messages into the user's composer.

For an adopted, manually registered name that must remain online while idle, the optional Unix helper is `/root/.xats/cc-heartbeat.sh <name> <team> <claude-pid> [agent_id]`. The normal session identity is kept alive by the xats mod. If the mod is not loaded, restart Claude Code and check `/xats-status` rather than silently assuming notifications work.
