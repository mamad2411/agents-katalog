---
name: "rule-list"
description: "Enumerate the existing Outlook inbox message rules — name, criteria, and target folder — in readable terms. Read-only. Use to understand the current mail organisation before proposing changes, or to find a rule's id for rule-remove (via --format detailed). Outlook message rules are mailbox settings, so this needs MailboxSettings.Read — which the default read-only sign-in already grants; no write capability is involved. Requires a prior read sign-in (run /msgraph-auth-login)."
argument-hint: "[--format concise|detailed]"
user-invocable: true
disable-model-invocation: false
annotations:
  readOnlyHint: true
  destructiveHint: false
  idempotentHint: true
  openWorldHint: true
---

## What this does

Lists existing inbox rules via `GET /me/mailFolders/inbox/messageRules`, shaping each into a readable
line (name, enabled state, header criteria, target folder). Read-only.

**Scope note:** Outlook message *rules* are stored as **mailbox settings**, so reading them needs
`MailboxSettings.Read` — not plain `Mail.Read`. That scope is included in the default read-only
sign-in, so `rule-list` works without any escalation while still holding **no** write capability
(`MailboxSettings.Read` ≠ `MailboxSettings.ReadWrite`).

Use it for situational awareness before `rule-create`, and to get a rule `id` (via
`--format detailed`) for `rule-remove`.

## Discoverability

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/src/msgraph/client.py" describe --name rule-list
```

## How it runs

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/src/msgraph/client.py" rule-list --format concise
# or:  python3 -m msgraph.client rule-list --format detailed
```

## Output (agent-legible)

```
- "Newsletters"  enabled
    if header contains: ['List-Unsubscribe']
    → move to folder id: AAMk...
1 rule(s). Pass --format detailed for ids needed by rule-remove.
```

`No inbox message rules.` is printed clearly when there are none.

## Errors steer the agent

```
error: not signed in — run /msgraph-auth-login first, then retry.
```
