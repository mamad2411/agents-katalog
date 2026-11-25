---
name: use-poll
description: Use the Poll JoAi app plugin when the task needs Poll tools or workflows.
---

# Poll

Connect Poll to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Poll tools available in this app.
- Explain what setup or authentication Poll needs before I run an action.
- Use Poll to help me with the task I describe next.

## Action Inventory

- `poll-admin-transfer` (contract) — Hand over group admin rights to another member.
- `poll-create` (contract) — Add a new question to an existing group for members to vote on. Requires a group to already exist. Provide a question, optional deadline, and 2–7 answer options.
- `poll-detail` (query) — Query details of a specific poll.
- `poll-group` (query) — Query details about a voting group.
- `poll-group-create` (contract) — Set up a new on-chain voting community — a DAO, HOA, team, or any group. Required first step before any polls can be created or voted on. You become admin.
- `poll-group-polls` (query) — Query all poll IDs belonging to a group (active and expired).
- `poll-groups` (query) — View your voting group and manage membership.
- `poll-invite` (query) — Check if an invite code is still valid and how many uses remain.
- `poll-invite-create` (contract) — Generate an invite code that lets people join your space directly without approval.
- `poll-invite-join` (contract) — Use an invite code to join a group instantly without waiting for approval.
- `poll-invite-revoke` (contract) — Revoke an active invite code so it can no longer be used.
- `poll-member-approve` (contract) — Approve a pending membership request and add the person to the group.
- ...and 14 more actions exposed by the hosted MCP app server.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
