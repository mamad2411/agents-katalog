---
name: pericles-notifications
version: 2026.10.0
description: >
  How to deliver platform notifications (email, SMS, Slack, Teams) reliably and safely.
  Use this WHENEVER you send an alert/notification, build a delivery channel, or handle
  retries. Encodes dispatch via the MessageQueue, delivery through the deterministic
  NotificationHandler (trial vs run mode), retries with backoff (attempts/max_attempts),
  and the rule that external communications are never auto-sent without an Execution Node
  and approval gate.
doctrine_refs: [§3; Ops §3]
depends_on: [pericles-execution-node, pericles-postgres-queue, pericles-functional-agent]
last_reconciled: 2026-10-09
---

# Pericles Notifications (build skill)

Notifications are consequential, external-facing actions — so they follow §3 exactly: a
supervisor agent or a deterministic trigger (for example an event lifecycle change or a
Plans step; neither is implemented yet) **proposes**, a deterministic Execution Node
commits, and external comms are **never auto-sent**. The substrate exists: the `NotificationHandler`
in the Workflow engine and the `MessageQueue`.

## When to use this skill

Sending an alert/notification; building a channel (email/SMS/Slack/Teams); handling
delivery retries or failures.

## Dispatch via the queue

A notification is enqueued as a `MessageQueue` message (`message_type: notification`,
`pericles-postgres-queue`) — publishing never blocks the proposing path. A worker hands
the message to the deterministic handler.

## Delivery via the NotificationHandler (deterministic)

`backend/src/workflow/handlers/notification-handler.ts` (extends `BaseNodeHandler`,
`NodeType.NOTIFICATION`) is the committer. Crucially it honors **trial vs run mode**: in
trial mode it **simulates** ("would send"); in run mode it actually sends. New channels
follow this handler pattern and honor trial mode (`pericles-execution-node`).

## Retries & failure (Ops §3)

Use the queue's `attempts`/`max_attempts` (default 3) with exponential backoff. Delivery
retries up to 3 times; on exhaustion mark `FAILED` with `error_message`/`failed_at` and
**alert the Plan Admin**. One channel's failure must not silently drop the notification.

## External comms are never auto-sent

Sending a message to a customer, supplier, or external stakeholder requires the approval
gate per deployment shape (`pericles-deployment-shapes`). The proposing agent or trigger
raises the notification; a human confirms; the Execution Node commits. Internal/system alerts
may run automatically within policy, but anything leaving the org needs the gate.

## What this forbids

Auto-sending external communications without an Execution Node + approval; sending
directly from an agent/prompt or a tool's `execute()`; a channel that ignores trial mode;
unbounded retries or silently dropping a failed notification; putting recipient PII in
logs/URLs.

## Verification

Notifications dispatch via `MessageQueue` and commit via the `NotificationHandler`; trial
mode simulates and run mode sends; retries back off and cap at `max_attempts` then alert
the Plan Admin; external comms pass the approval gate; each send writes an `ExecutionLog`.

## Existing standards (read alongside)

`backend/src/workflow/handlers/notification-handler.ts`; Ops §3; `pericles-execution-node`,
`pericles-postgres-queue`.

## Open questions

- Channel provider choices (email/SMS/Slack/Teams) and their secret handling — confirm
  with the platform team; keep secrets in the secret store.
- Per-recipient notification preferences storage (`OrganizationSettings`?) — confirm with
  `pericles-data-model`.
- Notification policy from the deprecated Controller rule (removed 2026.10.0; find it with
  `git log --all -- .cursor/rules/001-application/001-agents/005-controller-agent-core-standards-auto.mdc`)
  that this skill does not yet specify: quiet hours and locale; per-user channel
  preferences; escalation rules; rate limits; channel fallback; an in-app channel;
  acknowledge, snooze and escalate endpoints; a per-event notification state machine
  (NEW → NOTIFYING → WAITING_ACK → ACKED/SNOOZED/ESCALATED → CLOSED); a per-tenant SLA for
  notify dispatch; dead-letter handling beyond the FAILED status; webhook payload signing
  and replay protection (timestamps and nonces); an idempotency key so retries do not
  re-send (the old rule used `hash(event_id|tenant_id|channel|template_version)`);
  tenant-scoped delivery (`organization_id` on every notification); and redaction of
  sensitive content on channels that do not allow it. Confirm which of these are still
  required before building them.

## Changelog

- 2026.10.0 — Removed the deprecated Controller agent. Notifications are proposed by the
  owning agent or a deterministic trigger and committed by the NotificationHandler.

- 2026.05.0 — Initial draft; dispatch via MessageQueue + delivery via the existing
  NotificationHandler (trial/run), retries, and the no-auto-send rule for external comms.
