---
name: smb-crm-maintenance
version: 1.0.0
description: Keep the CRM current from email and calendar context — propose new contacts, deal updates, activity notes, and stale flags for owner approval before writing.
author: matrixx0070
tags: [crm, automation, sales, productivity, operations, hygiene]
capabilities: []
---

# CRM Maintenance

## When to use
Use this as a routine (daily or weekly) to keep the CRM honest without manual data entry. It reads recent email and calendar activity and proposes the updates that keep records accurate.

**Not for:** a one-time deep clean of duplicates and stale deals (use smb-crm-cleanup) or contacting customers. This maintains records only — it never sends anything.

## Method
1. Review recent email threads and calendar events since the last run.
2. Detect new people worth adding as contacts, and existing contacts or deals that changed (meetings held, replies received, stage movement).
3. Draft the updates: new contacts, deal field changes, and short activity notes. Decision point: ground every note only in what the source shows — no inferred intent ("seems eager to buy") unless the message says so.
4. Flag deals that have gone quiet and may need owner attention.
5. Present all proposed changes for approval before writing to the CRM. Do not send any email or contact a customer; this skill only maintains records.

## Example
Since last run: a new sender, Priya Nair (Acme Co.), emailed a pricing question → propose new contact. The "Westside remodel" deal had a site visit on the calendar Tuesday → propose stage move Qualified → Proposal, plus a note: "Site visit held Tue; discussed timeline." The "Harbor account" deal has had no activity in 21 days → flag as stale. Awaiting approval before syncing.

## Pitfalls
- **Inferring beyond the source.** Log what happened, not what you assume the customer feels.
- **Creating duplicate contacts.** Check for an existing record by email before proposing a new one.
- **Silent stage jumps.** Propose stage changes with the evidence, don't just move them.
- **Writing before approval.** Every CRM write waits for the owner's yes.

## Output format
```
New contacts:
  - <name>, <company> — source: <email/event>
Deal updates:
  - <deal> — <field change> — source: <...>
Notes to log:
  - <deal/contact> — "<note>" — source: <...>
Stale flags:
  - <deal> — quiet <n> days
"Approve these updates and I'll sync them to the CRM."
[after approval] Synced: <concise confirmation>
```

## Reference

### Pipeline stages and exit criteria
Stage changes should be evidence-based, not vibes. Propose a move only when the exit criterion is met by something in the source:

| Stage | Definition | Exit criterion (evidence to advance) |
|---|---|---|
| New / Lead | Made contact, unqualified | Confirmed a real need/interest |
| Qualified | Fit + need + rough budget confirmed | Agreed to a next step (call/demo/site visit) |
| Proposal / Quote | Quote or proposal sent | Prospect acknowledged/reviewed it |
| Negotiation | Discussing terms/price/scope | Verbal agreement or open points narrowed |
| Won | Signed / paid | Contract signed or deposit received |
| Lost | Declined or gone cold | Explicit no, or past stale threshold with no response |

When email/calendar shows the exit criterion (e.g., "site visit held" → agreed next step done), propose the advance *with the evidence quoted*. Never skip stages silently.

### Activity-note taxonomy
Log activities in consistent types so history is searchable and reports work. Each note: type + date + one factual line + source.
- **Call** — "Call 6/12: discussed 12-mo plan; wants pricing by Fri." 
- **Email** — "Email 6/12: replied asking about install timeline."
- **Meeting** — "Site visit 6/12: measured space, confirmed scope."
- **Task/next step** — "Follow-up due 6/15: send revised quote."
- **Note** — factual context only.
Record what happened and what was said — not inferred feelings. "Asked about pricing" is a fact; "seems ready to buy" is a guess (only log it if the message literally says so).

### New-contact dedupe check (before proposing)
Never propose a contact that already exists. Before adding, check by: exact email match first, then phone, then name+company. If a probable match exists, propose an **update to the existing record** instead of a new contact. Capture on creation: name, email, phone, company, source, and the linked deal if any.

### Stale thresholds by stage (flag, don't act)
Flag deals with no activity past these windows so the owner can re-engage:
- New/Lead: 7 days • Qualified: 14 days • Proposal: 10 days • Negotiation: 14 days.
A stale flag is a prompt for owner attention, not an auto-status-change — that's smb-crm-cleanup's job with approval.

### Suggested cadence
Run daily for an active sales team (catch same-day meetings and replies while fresh), or weekly (e.g., Monday morning) for a lighter pipeline. Each run covers only activity since the last run to avoid re-proposing the same updates. Keeping the CRM current daily is what makes the pipeline forecast, the call list, and the business pulse trustworthy downstream.

### Data-quality guardrails
- One source of truth per field — don't create parallel notes when a field exists (use the Stage field, not a note that says "now in proposal").
- Every proposed change carries its **source** (which email/event) so the owner can verify.
- Keep notes short and factual; long editorializing rots.

### Owner-approval gate
This skill drafts and proposes only. Nothing writes to the CRM until the owner approves, and it never emails, messages, or contacts a customer under any circumstance. After approval, sync only the approved items and return a concise confirmation of what was written.
