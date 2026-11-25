---
name: google-workspace-mcp-account-switch
description: Base protocol — switch the account of the google-workspace MCP session: auth_clear, trigger browser re-login with a follow-up API call, and verify the active identity via people_getMe.
category: Tool-Infrastructure
---

# Google Workspace MCP Account Switch Skill (v1) — Base Protocol

> **Skill ID:** `google-workspace-mcp-account-switch`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (procedural — per [`skill-factory` §2.0 Layering Decision](../../skill-factory/SKILL.md))

This is the **base protocol** for switching the account of a configured google-workspace MCP
session at runtime. It is procedural (no script): the flow is exactly two MCP calls with a
strict ordering constraint, plus identity verification.

It is consumed by the calendar composers (and any google-workspace workflow that must act on
a different identity) whenever the active account does not own the target mail or calendar.

***

## 1. Composition Rationale

This skill is a **base primitive** — it owns ONLY the clear → re-login → verify sequence and
its failure modes. It does not configure servers or manage credential files.

Consumers:

| Composer | Role |
| :--- | :--- |
| [`gmail-event-email-to-ics`](../../calendar/gmail-event-email-to-ics/SKILL.md) | Account preflight before reading another identity's Gmail content |
| [`ics-to-google-calendar-event`](../../calendar/ics-to-google-calendar-event/SKILL.md) | Account preflight before creating on another identity's calendar |

The protocol was extracted because the two-call ordering constraint is easy to get wrong
(batching the calls races the credential clear) and was corrected live during the source
session.

***

## 2. Scope & Intent

**Does:** clear the google-workspace MCP session credentials, trigger the browser re-login via
a dependent follow-up call, and verify the resulting identity.

**Does NOT:**

- Add/configure/verify the MCP server itself — that is [`mcp-management`](../../mcp-management/SKILL.md).
- Manage the REST/PKCE credential layer — that is [`google-oauth-setup`](../../google-oauth-setup/SKILL.md).
- Refresh the current account's token — `auth_refreshToken` is NOT an account switch.

***

## 3. Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| google-workspace MCP tools | `auth_clear`, `people_getMe` (the flow); `auth_refreshToken` exists but is not part of this flow |
| Browser access | The re-login opens the provider's browser login on the user's machine |

***

## 4. Protocol (the two-call sequence)

1. **Clear** — call `google-workspace_auth_clear` as a SINGLE call. Nothing else in the same
   message.
2. **Trigger + verify** — immediately issue the dependent follow-up call:
   `google-workspace_people_getMe` (preferred — it both triggers the browser login and
   returns the resulting identity). The two calls MUST NOT be batched: the tool-call
   framework runs batched calls in parallel, and a parallel `people_getMe` can race the clear
   and return the OLD identity.
3. **Report** — read the identity (name + email) from the `people_getMe` response and report
   it. Never assume which account is active.
4. **Switch back** — switching back requires the same clear → call cycle.

***

## 5. Edge Cases

- **"I don't see a login prompt"** right after `auth_clear` — expected: the prompt appears
  only on the NEXT request after the clear. Issue the follow-up call.
- **`auth_refreshToken`** refreshes the CURRENT account's token and is NOT an account switch.
- **Follow-up returns the OLD identity** — the clear did not land (e.g. the calls were
  batched); re-run the cycle.
- **User cancels the browser login** — the session stays cleared; report the state and stop.
- **No dependent call issued** — the session remains cleared but no login is ever prompted;
  the switch silently does not happen.

***

## 6. Prohibited Actions

- Never batch `auth_clear` with the follow-up call (dependent sequence).
- Never assume the active account — always verify via `people_getMe` and report the identity.
- Never use `auth_refreshToken` as a substitute for switching.
- Never record or echo credential material (tokens, secrets) — report the identity (name +
  email) only.

***

## 7. Verification

The switch is proven by the `people_getMe` response: report the name + email read from it. A
switch is NOT complete until the identity has been read and reported.

***

## 8. Related Skills

- [`mcp-management`](../../mcp-management/SKILL.md) — the add/configure/verify server
  lifecycle; this skill is the runtime auth operation on an already-configured server.
- [`google-oauth-setup`](../../google-oauth-setup/SKILL.md) — the REST/PKCE credential layer
  (a different layer than the MCP session).
- [`skill-factory`](../../skill-factory/SKILL.md) — §2.0 layering decision governing this
  procedural base.
