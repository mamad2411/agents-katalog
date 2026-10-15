---
name: questlog
description: "Company-wide task queue for humans and agents. TRIGGER when: checking what work needs doing, picking up tasks, reporting progress, assigning work, or asking 'what should I work on next?' Check Questlog before starting work to see if there are pending tasks."
metadata:
  version: "0.5"
---

# Quest Log

Quest Log is an event-sourced task system where agents pass work back and forth. Every action is an immutable event, and every task has at most one owner — the agent who currently has the ball.

## Bootstrap

The `ql` CLI is provided by the `questlog-ai` npm package:

```bash
# Check if ql is available
which ql || ql --version

# If not installed, install it globally
npm install -g questlog-ai
```

If `ql` is already configured (check `~/.ql/config` for host and token), you're ready to go.

**Note:** In containerized environments, `ql` may be lost on rebuild. Just `npm install -g questlog-ai` again. Your config in `~/.ql/` persists separately.

## Connecting

### MCP (preferred for Claude Code and MCP-compatible agents)

If the MCP server is configured, call tools directly. The server URL and auth token are set up during installation.

### CLI — New registration

```bash
ql init --host https://quest-log.your-org.com
ql register --name "Your Name"
# If auto-approved, you're logged in. Otherwise, after admin approval:
ql auth login
ql install   # adds MCP server + skill to Claude Code
```

### CLI — Adding a device to an existing account

If the user already has a Quest Log account and wants to connect from a new machine or container, use device pairing instead of re-registering:

**On the existing device** (already logged in):
```bash
ql devices add
# Prints a pairing code like ABCD-1234 (valid for 10 minutes)
```

**On the new device:**
```bash
ql init --host https://quest-log.your-org.com
ql devices pair ABCD-1234
# Automatically links to the existing account and saves a token
ql install
```

This avoids creating duplicate users and doesn't require admin approval — the pairing code proves the user controls an authenticated device.

## Core Concepts

**Three task states:** `open`, `done`, `cancelled`. That's it.

**Events are append-only.** Every action (progress, handoff, completion) is recorded as an immutable event. The task's current state is a projection of its event history.

**Ownership = who has the ball.** Every open task has at most one owner. When you own a task, you're expected to work it or hand it off.

**The triage pool.** Open tasks with no owner sit in the triage pool. Query with `list_tasks` using `owner_id: null`.

**Attachments.** Files can be attached to tasks for context — screenshots, logs, design mockups, configs. Use `attach_file` (MCP) or `ql attach` (CLI). Description is required so AI can reference attachments without viewing them.

When to attach: If the user shares images, files, or other artifacts that are relevant to a task (or will be relevant to whoever works on it next), proactively attach them. Read the file, base64-encode it, and call `attach_file` with `file_data` and `filename`.

The server base URL is in your ql config (`~/.ql/config` → `server_url`). Strip the `/mcp` suffix to get the base. Attachments are served at `<base_url>/attachments/<attachment_id>`. When referencing an attachment in notes, handoffs, or progress updates, always include the full public URL so anyone reading the task can access it directly.

## Good Task Descriptions

**Title:** what needs to be done, imperative voice.
- Bad: "Login bug" or "Fix the thing"
- Good: "Fix login redirect loop on mobile Safari"

**Body:** context, acceptance criteria, relevant links. Give the person claiming this task enough to start working without asking questions.

## Handoff Etiquette

- Always explain what you did and what remains.
- Include relevant context: error logs, partial work, decisions you made and why.
- Don't hand off empty-handed. Do what you can first, then transfer with a clear picture.

## Reporting Capability Gaps

Use `blocked` with `metadata.capability_gap: true` when you can't do something:

- No access to a required API or service
- Need human judgment on a business decision
- Don't have credentials for a third-party platform

This is not failure. It's a signal to route the task to someone who can handle it.

## Additional Resources

- For MCP tool parameters and usage, see [MCP_REFERENCE.md](MCP_REFERENCE.md)
- For event type details, see [EVENT_TYPES.md](EVENT_TYPES.md)
- For full CLI command reference, see [CLI_REFERENCE.md](CLI_REFERENCE.md)
