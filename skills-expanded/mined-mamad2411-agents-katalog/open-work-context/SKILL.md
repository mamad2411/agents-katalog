---
name: open-work-context
description: Switch to an external linked workspace on paid Connection Hub plans. Not required for Community Personal Workspace (auto-active). Do not coach normal users to pass context_id.
---

# Open Work Context — External Workspace Switch

This skill is for **switching to an external linked workspace** on plans that allow additional links.

It is **not** part of Community onboarding. After signup/login, **Personal Workspace is already Active** — start using tools without this skill.

## After an organization invite

If the user **just accepted an invitation** to an organization workspace:

1. Call `ops_accounts_list` — the org workspace may **already be linked** (same email + Developer+ Hub).
2. If it appears, offer to **switch** with this skill when they want to work there.
3. If it does **not** appear, check `ops_my_usage` (plan, Hub, quota) and point to **`link-account`** for manual linking or upgrade — do not treat a failed list as "invite broken"; membership may still be active in the admin portal.

## Concepts

| Term | Meaning |
|------|---------|
| **Personal Workspace** | Default operational workspace — automatic; no manual open |
| **External Workspace** | Extra linked workspace — switch only when user asks |
| **Work Context** | Provider/stack notes (`ops_set_work_context`) — unrelated to this skill |

> **Community:** Skip this skill for normal work. If `ops_my_usage` shows Personal Workspace active, you are done.
>
> **Legacy single-tenant:** If `ops_context_open` is **not** in `tools/list`, skip this skill.

## When to run

1. User on a **paid** Hub explicitly asks to work on a **different linked** (external) workspace.
2. User says _"switch to [client]"_ and `ops_accounts_list` shows multiple non-personal connections.
3. Do **not** run after Community signup, returning login, or when only Personal Workspace exists.

A resource lookup is not an implicit switch request. For example, asking for a
Jira ticket in workspace **Acme** while workspace **Beta Corp** is active means: explain the likely workspace
mismatch and ask whether to switch to Acme. Do not call `ops_context_open` until
the user explicitly confirms the named target.

## When NOT to run

- Community first-time or returning login
- "Make me operational" / setup — use `/opsphere-setup` status steps instead
- Coaching the user to copy or paste internal session IDs
- Fixing missing tools by inventing manual context steps (prefer `/opsphere-reconnect`)

## Tools (advanced / paid switch)

| Tool | Purpose |
|------|---------|
| `ops_accounts_list` | List personal + external connections |
| `ops_context_open` | Atomically replace this conversation's active workspace with the chosen **external** link |
| `ops_context_close` | Explicitly leave the active workspace when the user asks to close it |

Prefer describing outcomes to the user as **"switched to workspace X"** — not as "here is your context_id".

Internal IDs may appear in tool payloads for the model; **do not** teach end users to pass them on every call for Community Personal Workspace work.

## Switch flow (paid / multi-external)

1. Call `ops_accounts_list`. Identify Personal vs external from the tool result.
2. Ask which **external** workspace if more than one (labels/slugs only).
3. Call `ops_context_open` with that `linked_connection_id` only after explicit user confirmation. It persistently changes the active workspace and client preference, and closes/replaces the previous context atomically; do not close first. Only pass a stable `chat_session_key` supplied by the host—never invent one.
4. If `tools_discovery.mode` is `stable`, do not refresh or reconnect. Use `workspace_availability` and, when needed, `ops_list_integrations`: the public tools list is not permission to execute. If availability is unknown, do not infer missing credentials. Only legacy `tools_discovery.stale: true` calls for a host catalog refresh; if the host does not expose `tools/list`, do not invent an invocable tool.
5. Confirm to the user which workspace is active by **label/slug**.
6. Continue operational tools. Do not narrate broker internals (`expires_at`, pinning, etc.) unless the user asks for diagnostics.

If a resource belongs elsewhere or a provider tool is absent from the active catalog, explain the mismatch and offer a workspace switch. Never switch automatically: retain the selected workspace until the user confirms another one. There is no temporary lookup mode: after a confirmed switch, remain in the new workspace until the user asks to change it again.

## Community / auto-context

If the user only has Personal Workspace:

> "Your **Personal Workspace** is already active. You can call Opsphere tools now — no extra open step."

If they want additional workspaces → skill **`link-account`** (upgrade CTA on Community).

## Errors

| Code | Action |
|------|--------|
| `BROKER_CONTEXT_REQUIRED` / invalid | Prefer `/opsphere-reconnect`. For paid external switch only, retry open. Do not coach Community users to manually attach IDs. |
| `LINKED_CONNECTION_NOT_FOUND` | `ops_accounts_list`; may need `link-account` on paid plans |
| `BROKER_LINK_LIMIT_EXCEEDED` | Upgrade CTA — Personal Workspace remains included |
| `MCP_SESSION_REQUIRED` | `/opsphere-reconnect` |
| `HUB_OPERATIONAL_DENIED` | Reconnect; ensure Personal Workspace / correct external is active |

## Avoid

- Presenting this skill as required after Sign up free / login
- "Pass context_id to every tenant-scoped tool" as Community guidance
- Automatically switching workspaces because a provider tool is absent
- Treating a cross-workspace ticket, zone, repo, project, or provider request as confirmation
- Switching temporarily to answer and switching back without a second explicit request
- Closing the current context before a normal confirmed switch
- Confusing this with **Work Context** (`ops_set_work_context`)
- Unlinking or "opening" Personal Workspace as if it were missing
