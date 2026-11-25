---
name: cs-ticket-triage
version: 1.0.0
description: Triage an incoming ticket — set priority P1-P4 by impact x reach, route it, catch duplicates and known issues, and state the first-response SLA.
author: matrixx0070
tags: [customer-support, triage, prioritization, routing, sla, deduplication]
capabilities: []
---

## When to use

Use this the moment a new ticket arrives and must be sorted before work begins: set priority, route to the right team, and avoid re-solving something already tracked.

**Not for:** issues already prioritized and assigned, writing the customer reply (cs-draft-response), or escalating a scoped incident (cs-escalation). If it is clearly one known issue, link and move on rather than re-triage.

## Method

1. Extract essentials: what broke, for whom (plan tier, account value), scope (one user vs. many), business impact, and any time pressure (deadline, event, renewal).
2. Assign priority by impact x reach:
   - **P1:** outage, data loss, security, or many/high-value accounts blocked — respond now.
   - **P2:** major feature broken for one account or degraded for many, no workaround.
   - **P3:** broken but has a workaround, or single-user non-critical.
   - **P4:** cosmetic, minor, or feature request.
3. Search open tickets and known-issue lists for the same symptom. **Decision point:** if found, link/merge and attach the customer — do not open a parallel thread.
4. Check recent releases; if it matches a tracked bug, tag it so the customer gets updates.
5. Route to the owning team (support tier, billing, eng, security) with a one-line reason, and state the SLA / first-response deadline.
6. **Decision point:** if you cannot set priority confidently, list the exact questions to ask the customer before routing.

## Example

> **Ticket:** "Login page 500s for our whole team since this morning" (Enterprise, 40 seats).
> **Priority:** P1 — outage blocking a high-value account.
> **Category/route:** Auth → eng-oncall.
> **Duplicate/known-issue:** matches INC-3391 (auth deploy regression) — linked, customer attached.
> **SLA:** P1 first response 15 min.

## Pitfalls

- Priority by tone, not impact — a calm ticket can be a P1; an angry one can be a P4.
- Skipping the duplicate search — parallel threads split context and waste eng time.
- Routing without a reason — the receiving team re-triages from scratch.
- Guessing priority on thin info instead of asking two sharp questions.

## Output format

```
Priority: P1-P4 — <one-line justification>
Category + route: <team / queue>
Duplicate / known-issue: <link or "none found">
SLA / first-response: <deadline>
Missing info to request: <or "none">
```
