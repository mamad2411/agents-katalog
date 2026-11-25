---
name: legal-signature-request
version: 1.0.0
description: Prepare and route a finalized document for e-signature with a pre-send checklist, correct signer order, and post-signature follow-through.
author: matrixx0070
tags: [legal, e-signature, workflow, routing, execution]
capabilities: []
---

## When to use
Use this once a document is final and ready to execute — a contract, NDA, SOW, offer letter, or consent form — to send it for e-signature cleanly on the first try. It prevents the common failures: wrong version, missing signer, bad signing order, unfilled fields.

**Not for:** documents still under negotiation or review (finalize first via `legal-review-contract`), deciding whether terms are acceptable, or anything where required approvals aren't yet recorded. Do not send until it is truly final.

## Method
1. **Confirm it is truly final.** Version matches the approved redline; all internal approvals recorded; no open comments or tracked changes. *Decision point:* any open comment or missing approval → stop, do not send.
2. **Run the pre-send checklist.** Correct legal entity names, dates, dollar amounts, exhibits/attachments included, all placeholders resolved.
3. **Identify every signer and role.** Full name, title, entity, email, and authority to sign. *Decision point:* if a signer lacks signing authority, correct the routing before sending.
4. **Set signing order.** Sequential vs. parallel; note witness or notary requirements. Add CC recipients who need the executed copy.
5. **Place fields.** Signature, date, initials, and any required data fields per signer.
6. **Configure reminders and expiry.** Reminder cadence and a completion deadline.
7. **Plan post-signature steps.** Where the executed copy is stored, who is notified, and any calendared obligations (renewal, milestone).

## Example
Document: mutual NDA v4 (final, matches approved redline). Checklist: entity names correct, effective date blank → set to send date, no placeholders, no tracked changes → pass. Signers: their GC (signs first), our VP Legal (signs second). CC: deal owner. Order: sequential. Reminders: every 3 days, expiry 14 days. Post-signature: store in contract repository under vendor folder, notify deal owner, no calendared obligation (perpetual NDA).

## Pitfalls
- **Sending a near-final draft.** One unresolved tracked change means re-signing the whole thing.
- **Wrong signer authority.** A signature from someone without authority can void the agreement.
- **Parallel order when sequence matters.** Counterparty-then-internal routing gets scrambled.
- **No storage/notification plan.** The executed copy lands in an inbox and is never filed or calendared.

## Output format
```
Document / version / parties:
Pre-send checklist:
  | Item | Pass/Fail |
Signer list:
  | Name | Title | Entity | Email | Order |
CC / storage location / notifications:
Reminders & expiry:
Post-execution actions:
  | Action | Owner | Date |
```

## Pre-send checklist reference
Run every row before the document leaves your hands. Any "Fail" is a hard stop — do not send a document you have to re-sign.

| Check | What good looks like | Fail = stop |
|-------|---------------------|-------------|
| Version match | Matches the final approved redline exactly | Any tracked changes or open comments remain |
| Approvals recorded | All internal sign-offs logged and traceable | A required approver has not signed off |
| Entity names | Exact legal names + entity type (e.g. "Acme, Inc.", a Delaware corporation) | Wrong, informal, or inconsistent entity names |
| Dates | Effective date set, or intentionally left blank to complete on execution | Placeholder or accidentally wrong date |
| Dollar amounts & numbers | Every figure matches the body and all exhibits | Any mismatch between clauses, exhibits, or schedules |
| Exhibits / schedules / attachments | All present, attached, and referenced correctly | A referenced exhibit is missing or misnumbered |
| Placeholders resolved | No [BRACKETS], TBDs, or highlight markers | Any unresolved placeholder anywhere in the doc |
| Defined terms | Consistent capitalization and usage throughout | A defined term used before/outside its definition |
| Signature blocks | Correct name, title, entity, and authority per signer | Wrong signatory, title, or missing block |
| Counterpart / e-sign clause | Present and permits electronic execution | No counterpart or e-signature authorization |

## Signer & routing reference
- **Authority to sign.** Confirm each signer can actually bind the entity — an officer, someone with delegated signing authority, or, where the deal or bylaws require it, a board resolution. A signature from someone without authority can void the agreement.
- **Signing order.** Use **sequential** order when routing is counterparty-first or gated by an approval step (each signer waits for the prior). Use **parallel** only when the signatures are genuinely independent of each other.
- **Witness / notary requirements.** Some instruments need more than a signature: deeds, certain real-estate and IP assignments, and documents in some jurisdictions may require witnessing, notarization, or an apostille for cross-border use. Confirm before sending.
- **CC recipients.** Identify who should receive the executed copy (deal owner, finance, contract repository) and add them so distribution is automatic.

## E-signature workflow reference
| Setting | Recommended default |
|---------|--------------------|
| Reminder cadence | Every 2-3 days |
| Expiry | 7-14 days |
| Field placement | Signature, date, initials, and title placed per signer |
| Authentication level | Email for routine docs; SMS or KBA (knowledge-based) for high-value or high-risk |
| Audit trail / certificate | Retained with the executed copy in the system of record |

## Post-execution
Once every party has signed, close the loop:

- [ ] Store the executed copy in the system of record (contract repository / CLM), not an inbox
- [ ] Distribute the fully executed copy to all parties
- [ ] Extract key dates into a calendar or CLM — effective date, term end, renewal-notice deadline, milestones
- [ ] Notify the obligation owners who must act on those dates
- [ ] Confirm the audit trail / signature certificate is filed with the document

**E-signature legal validity:** in the US, ESIGN and UETA make electronic signatures valid for most commercial documents; in the EU, eIDAS governs (with tiers of e-signature). Some documents — wills, certain family-law or court filings, some statutory notices, and specific real-estate instruments — may require wet-ink signatures or notarization. Confirm with counsel for any exception before relying on e-signature.
