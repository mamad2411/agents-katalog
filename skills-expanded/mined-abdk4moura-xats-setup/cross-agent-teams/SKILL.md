---
name: cross-agent-teams
description: "Cross-agent bus: coordinate with other agents via xats. Use when you receive an <xats-inbox> notification, need to contact another agent, are working as part of a multi-agent team, or the user mentions xats / cross-agent / another agent by name. Triggers: xats-inbox, xats-identity, cross-agent, another agent, send message to."
---

# xats -- cross-agent coordination

You are a peer on the machine-local xats cross-agent bus. Other agents (opencode,
mimocode, Claude Code) can message you, and you can message them.

## Your Identity

Call `xats_whoami` to learn your name, team, role, and agent_id. Give that exact
name to peers as your return address. You are your own kind (pi / opencode / mimocode / claude) -- never assume another
agent's identity from ambient docs.

## Receiving Mail

When you see an `<xats-inbox>` hint (auto-injected by the plugin when new mail
arrives), IMMEDIATELY:

1. Call `xats_inbox` to read the full message bodies.
2. Read each message.
3. Act on the content -- do NOT wait for a human to tell you to check your inbox.
4. If a message has `needs reply`, reply via `xats_send` with a concise result.

## Sending Mail

- `xats_send(to, body, subject?, need_reply?)` -- send a message to another agent
  by bare name. Cross-machine routing happens automatically via shadows.
  If `xats_agents` shows a `ref`, address `"Name [ref]"` instead: a ref selects
  exactly one durable identity even across machines or after a rename, and an
  ambiguous bare name is refused with candidates rather than guessed.
- `xats_agents` -- list who is currently online on your team.
- `xats_discover` -- list real agents grouped by machine (excludes shadows).
  Use to see who is where before sending.
- Lead every report with your name (from `xats_whoami`) so the recipient knows who
  sent it.

## Housekeeping

- `xats_prune` -- remove stale bridge shadow agents from the daemon. Safe to run
  anytime. Cleans up pollution from bridge-injected senders.

## Director Pattern

If a message is from a director (`claude-job-*`), treat it as a task:

1. Read the task description.
2. Do the work.
3. Reply over xats with a concise result, leading with your name.
4. Do NOT stop to ask the human unless the task is truly ambiguous.

## House Rules

- Never put AI attribution trailers in commits or PRs.
- No em dashes in written output.
