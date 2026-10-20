---
name: link-account
description: Link or unlink an external workspace on Connection Hub (paid plans). Community users get an upgrade CTA — Personal Workspace is already included and must not be linked manually.
---

# Link Account (Connection Hub)

Guide linking or unlinking **external workspaces** on a Connection Hub. Personal Workspace is automatic and separate.

## Organization invite — automatic link (same email)

When someone **accepts an invitation** to join an organization workspace as administrator:

| Situation | What happens |
|-----------|----------------|
| **Same email** as your Connection Hub + **Developer** (or higher) plan with link quota | The organization workspace is **linked automatically** when you accept the invitation — no `/link-account` step. |
| **Same email**, but you do not have a Connection Hub yet | Your account is ready; the workspace links when you **create a Hub** with that email (Sign up free in the plugin). |
| **Same email**, Hub on **Community** only | Your account is ready; the workspace links after you **upgrade** to Developer or higher. |
| **Same email**, Hub link quota is full | Your account is ready; the workspace links when a slot is free (remove an old external link or upgrade). |
| **Different email** than your Hub | Accepting still activates your org access; use **`/link-account`** in the plugin to link manually. |

After accepting, run `ops_accounts_list` in chat to see Personal Workspace + any organization workspaces. Use **`open-work-context`** to switch to an external workspace when you have more than one.

> **`/link-account`** remains the manual path: different emails, retry after quota, or linking workspaces you joined before creating a Hub.

## Concepts (mandatory)

| Concept | Meaning |
|---------|---------|
| **Personal Workspace** | Product-managed workspace created at signup — already linked; never "add" or unlink it |
| **External Workspace** | Extra workspace via OAuth link — counts against plan quota |
| **Work Context** | Optional provider/stack notes (`ops_set_work_context`) — not a workspace link |

> If `tools/list` does **not** include `ops_accounts_list`, this skill does not apply — use normal OAuth via `/opsphere-setup`.

## Tools

| Tool | Purpose |
|------|---------|
| `ops_accounts_list` | List connections (personal + external) |
| `ops_account_link_start` | Returns `authorization_url` for an **external** link |
| `ops_account_unlink` | Revoke an **external** link only |
| `ops_my_usage` | Plan, Personal Workspace status, additional-workspace quota |

## Security (mandatory)

1. **Never** ask the user to paste OAuth codes, refresh tokens, or passwords into chat.
2. **Never** store link credentials in `memory_store`, `ops_set_work_context`, or local files.
3. Show only the **authorization URL** from `ops_account_link_start`.
4. Confirm success with connection **label / slug** — do not echo tokens.

## When to run

1. User says _"link another workspace"_, _"add an organization workspace"_, _"connect another Opsphere workspace"_ on a plan that allows external links — **or** accepted an org invite with a **different email** than their Hub.
2. User wants to **remove an external** workspace → `ops_account_unlink` (never the Personal Workspace).

**Skip OAuth** if the user **just accepted an org invite** with the **same email** as their Hub on Developer+ — call `ops_accounts_list` first; the workspace may already be linked.

## Community / zero external quota (mandatory)

1. Call `ops_my_usage` (and optionally `ops_accounts_list`).
2. If Personal Workspace is active and additional linked workspaces are **not** available (Community / `BROKER_LINK_LIMIT_EXCEEDED` / max external = 0):

> "You're connected on **Community**. Your **Personal Workspace** is included and already active — you can use Opsphere tools now.
>
> Linking **additional** workspaces requires **Developer** or higher. See [opsphere.io/pricing](https://opsphere.io/pricing)."

3. Do **not** call `ops_account_link_start`.
4. Do **not** imply the Personal Workspace is missing or blocked.
5. Do **not** present raw "0/0" without the upgrade explanation.
6. Preserve code `BROKER_LINK_LIMIT_EXCEEDED` for diagnostics/support if the tool returned it.

## Do not treat Personal Workspace as empty Hub

- `ops_accounts_list` showing only the Personal Workspace is **success**, not a reason to link.
- Never say the Hub is "not an operational workspace" after Community signup.
- Never ask the user to copy `linked_connection_id` or open a manual context for normal use.

## External link flow (paid / quota available)

1. Call `ops_accounts_list` — show personal vs external clearly from labels/kinds in the tool result.
2. Confirm plan allows another external link via `ops_my_usage`.
3. Call `ops_account_link_start` (no parameters).
4. Give the user `authorization_url` to open in a browser.
5. After confirmation, call `ops_accounts_list` again.
6. Offer to continue working — Personal Workspace stays default; switching to the new external workspace is only if the user asks (**`open-work-context`**).

## Unlink flow (external only)

1. Call `ops_accounts_list` — user picks an **external** connection.
2. If the target is Personal Workspace / protected personal → refuse with:

> "Your Personal Workspace is part of your Opsphere account and cannot be unlinked."

   Keep code `PERSONAL_WORKSPACE_UNLINK_FORBIDDEN` for diagnostics if returned.
3. Otherwise confirm and call `ops_account_unlink(linked_connection_id: "<uuid>")`.

## Errors

| Code | Action |
|------|--------|
| `BROKER_LINK_LIMIT_EXCEEDED` | Upgrade CTA (Personal Workspace included). |
| `PERSONAL_WORKSPACE_UNLINK_FORBIDDEN` | Explain personal cannot be removed. |
| `PLAN_WORKSPACE_NOT_INCLUDED` | Feature not on current plan — pricing. |
| `BROKER_DISABLED` | Contact Opsphere support. |
| `MCP_SESSION_REQUIRED` | `/opsphere-reconnect`. |

## Avoid

- Linking because "accounts look empty" after signup.
- Teaching `context_id` / `ops_context_open` as part of Community onboarding.
- Promising **Developer** features unless plan status shows Developer is active.
- Inventing connection IDs — always from live tool output.
