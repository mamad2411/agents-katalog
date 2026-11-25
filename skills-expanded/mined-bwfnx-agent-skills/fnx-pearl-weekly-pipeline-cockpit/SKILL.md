---
name: fnx-pearl-weekly-pipeline-cockpit
description: Weekly FNX Pearl pipeline, proposal, invoice, and follow-up cockpit
---

> **Schedule:** Weekly FNX Pearl pipeline
> **Needs:** Gmail, Google Calendar, Drive
> **Helper scripts (yours, not included):** none

# FNX Pearl Weekly Pipeline Cockpit

## Objective

Create a weekly operating cockpit for FNX Pearl that helps {{USER}} see active leads, proposal-to-close gaps, outstanding invoices, client delivery obligations, and next follow-ups. This is a draft/report workflow only; it should reduce pipeline memory load without sending messages or changing records automatically.

## Account And Data Boundaries

- Use FNX Pearl context: `{{YOUR_EMAIL}}`, FNX Pearl Google Calendar, Gmail, Google Drive, and HubSpot if connected.
- Do not use University of Maryland / SBDC client data unless the item is explicitly a separate FNX Pearl opportunity and already present in FNX Pearl context.
- Do not send email, create invoices, update HubSpot, edit calendar events, or modify Drive files.
- Draft messages and action recommendations only.
- Treat client financial, proposal, and contract information as confidential.
- Do not invent deal terms, invoice amounts, or commitments. Mark missing facts as `[not found - confirm]`.

## Inputs To Review

### Gmail

Search FNX Pearl Gmail for the last 90 days, with special attention to the last 14 days.

Useful searches:

- proposal, SOW, statement of work, contract, MSA, retainer, invoice, payment, overdue, QuickBooks, estimate, scope, kickoff, follow up, next steps, intro, referral
- Emails to/from [partner] at `{{COLLEAGUE_EMAIL}}`
- Emails involving known FNX Pearl clients or leads

### Calendar

Search FNX Pearl Calendar for:

- Last 30 days: completed consultations, client calls, proposal meetings, delivery meetings
- Next 30 days: upcoming client obligations, proposal calls, kickoff meetings, renewals, deadlines

### Drive

Search FNX Pearl Drive and local workspace:

- `fnx-pearl-consulting/outputs/`
- `fnx-pearl-consulting/wiki/`
- Proposal, SOW, MSA, deliverable, invoice, onboarding, strategy, scope, kickoff, client names

### HubSpot

If HubSpot is connected, review active deals, stale deals, recent contact activity, proposal stage, close dates, and owner notes. If not connected, state `HubSpot not available in this run`.

## Output Format

Use this exact structure.

```
# FNX Pearl Weekly Pipeline Cockpit - Week of YYYY-MM-DD

## Executive Snapshot
- Active revenue conversations:
- Proposal/SOW items needing movement:
- Invoice/payment risks:
- Delivery obligations this week:
- Highest-value next action:

## Pipeline Table

| Priority | Client / Lead | Stage | Last signal | Next action | Owner | Risk | Source |
|----------|---------------|-------|-------------|-------------|-------|------|--------|

## Proposal-To-Close Watchlist

| Client / Lead | Artifact needed | Current blocker | Suggested next move | Draft ready? |
|---------------|-----------------|-----------------|---------------------|--------------|

## Invoice / Payment Watchlist

| Client | Amount | Due / aging | Evidence found | Recommended action |
|--------|--------|-------------|----------------|--------------------|

## Delivery Commitments

| Client / Project | Commitment | Due date | Evidence | Next step |
|------------------|------------|----------|----------|-----------|

## [partner] Collaboration Queue

| Item | Context | Needs from [partner] | Needs from {{USER}} | Suggested handoff |
|------|---------|------------------|--------------------|-------------------|

## Draft Follow-Ups

### [Recipient / Client]
Subject:

[Draft email in {{USER}}'s voice]

## Decisions {{USER}} Needs To Make
- [Decision] - why it matters - recommended default

## Internal Notes
- [Pattern, bottleneck, or operating improvement worth noticing]
```

## Follow-Up Voice

Use {{USER}}'s style:

- Direct and warm
- Short, action-oriented sentences
- Specific next step, not vague checking in
- No corporate filler
- Honest about uncertainty
- One path at a time

For proposals, prefer:

- "I think the clean next step is..."
- "Here is the simplest way to scope this..."
- "The thing I want to avoid is..."

## Ranking Logic

Prioritize:

1. Money already earned or at risk: invoices, overdue payments, renewal conversations.
2. Proposals/SOWs that could close within 30 days.
3. Client delivery commitments due in the next 14 days.
4. Warm referrals or active introductions.
5. [partner] handoffs that unblock revenue or delivery.

## Early Exit

If no active FNX Pearl signals are found:

```
# FNX Pearl Weekly Pipeline Cockpit - Week of YYYY-MM-DD

No active FNX Pearl pipeline, proposal, invoice, or delivery signals found in the searched window.

## Maintenance Suggestions
- [One useful cleanup or business-development action based on the wiki.]
```

## Portability Notes

When installing in another ChatGPT instance:

- Connect FNX Pearl Gmail, Calendar, Drive, and HubSpot if available.
- Verify the active account is `{{YOUR_EMAIL}}`.
- Paste this file as the scheduled task instruction.
- Keep the workflow draft-only unless {{USER}} explicitly authorizes system changes.
