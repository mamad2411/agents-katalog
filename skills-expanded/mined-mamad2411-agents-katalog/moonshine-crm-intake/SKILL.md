---
name: moonshine-crm-intake
description: Process Moonshine Capital funding, affiliate, or partner intake from Gmail into HubSpot, Notion, and the Master CRM Sheet with evidence-backed enrichment, reconciliation, and follow-up. Use for Moonshine operations, not generic CRM work or standalone copywriting.
metadata:
  version: 2.1.0
---

# Moonshine CRM Intake

Classify new Gmail items as funding applicant, affiliate or partner, existing-record update, or irrelevant. Preserve submitted facts exactly and label every added fact as `supplied`, `existing source`, `publicly sourced`, `inferred`, or `unverified research clue`.

## Workflow

1. Scan relevant inbox and sent-thread activity first; capture source, thread, timestamps, and intent.
2. Before any write, inspect live HubSpot schema and search HubSpot, Notion, and the Master CRM Sheet for identity matches.
3. Create or update contacts, companies, notes, and tasks when identity and intent are clear. Create deals only for qualified commercial opportunities; create tickets only for support or implementation work.
4. Write the normalized internal note using [the note template](templates/normalized-note.md). Keep material funding claims, ambiguous routing, provider terms, and applicant decisions for human review.
5. When a sent email or reply changes state, preserve the Gmail thread ID and update last touch, fulfilled task, current status, and the next follow-up.
6. Report writes, evidence, missing information, exceptions, and one recommended next action per active record.

## Required controls

- Do a live-schema preflight before using uncertain properties, pipeline IDs, stages, lifecycle values, lead statuses, owners, or enum values. Prefer an existing standard property; use a note when no clean field exists.
- State coverage as `complete`, `sampled`, or `partial/paginated`. Never call a limited search a complete audit.
- Apply duplicate evidence in this order: exact email; exact phone; company domain or website; same name plus company; then supporting social/context clues. Never merge on a fuzzy name alone.
- Automate administration, assist analysis, human-review the money talk, and leave an audit trail.

Read [the operating contract](references/operating-contract.md) for the evidence, risk, and pipeline rules that govern this skill.

## Guardrails

- Never fabricate profiles, financial performance, approval status, commitments, lender terms, or outreach.
- Never commit or expose private applicant data, bank data, credit files, credentials, or secrets.
- Draft recurring outreach as a reply in the original Gmail thread when one exists.

