---
name: smb-crm-cleanup
version: 1.0.0
description: Scan the CRM for stale deals, duplicate contacts, and missing fields, propose fixes, and apply only what the owner approves.
author: matrixx0070
tags: [crm, data-quality, operations, cleanup, sales, dedupe]
capabilities: []
---

# CRM Cleanup

## When to use
Use this when the CRM has drifted — old deals lingering in the pipeline, the same contact entered twice, records missing emails or owners. It produces a cleanup plan and executes only the changes the owner signs off on.

**Not for:** routine ongoing upkeep from email/calendar (use smb-crm-maintenance) or building a daily call list (use smb-call-list). This is a periodic deep clean, not a daily sync.

## Method
1. Scan all contacts and deals. Detect duplicates (matching name, email, or phone), stale deals (no activity past a threshold you state), and records missing key fields (email, owner, stage, value).
2. Group findings by type and estimate cleanup impact (how many records, what it unblocks).
3. For duplicates, propose which record to keep and which to merge. Decision point: keep the record with the most complete history and recent activity; show exactly what data survives.
4. For stale deals, propose a status change (close-lost, revive, or nurture) with reasoning — never auto-close.
5. Present the full plan. Apply only approved changes, then confirm what was updated. Deletions and merges always require explicit approval.

## Example
Findings: 6 duplicate contacts, 11 stale deals (>60 days no activity), 9 records missing an owner. Duplicate example: "J. Smith" (2 records) → keep the one with 4 logged calls and the recent email, merge in the other's phone number. Stale example: $3k deal, last touch 74 days ago → propose close-lost. Nothing changes until the owner replies with which items to apply.

## Pitfalls
- **Auto-merging on a name match.** Two different people share names; require email or phone corroboration before merging.
- **Auto-closing stale deals.** A quiet deal may be mid-negotiation offline — propose, don't close.
- **Losing data in a merge.** Always show which fields survive so nothing important is silently dropped.
- **Bulk-applying without a change log.** After execution, return exactly what changed so it's auditable.

## Output format
```
Findings: <n> duplicates | <n> stale | <n> missing fields
Duplicates:
  - keep <record A> / merge <record B> — survives: <fields>
Stale deals:
  - <deal> — last activity <date> — propose <close-lost/revive/nurture>
Missing fields:
  - <record> — missing <field>
"Reply with the items to apply (or 'all')."
[after approval] Change log: <exactly what was modified>
```

## Reference

### Duplicate-match confidence tiers
Not all matches are equal. Grade each candidate pair and act only per its tier:

| Confidence | Signal | Action |
|---|---|---|
| **Exact** | Same email address (normalized) OR same phone (E.164) | Safe to propose auto-merge |
| **Strong** | Same company + same normalized name; or same name + same phone | Propose merge, show evidence |
| **Possible** | Same name only; or similar name + same company | Flag for human review — do NOT auto-merge |
| **Weak** | Fuzzy name similarity, no corroborating field | List, but default to "leave separate" |

**Normalize before comparing:** lowercase and trim emails (and strip `+tags` and dots in gmail addresses); reduce phones to digits/E.164; standardize company suffixes (Inc/LLC/Ltd/Co) and drop punctuation; treat nicknames (Bob/Robert, Liz/Elizabeth) as name-only (Possible) matches, never Exact.

### Merge survivorship rules (which record wins)
Pick the surviving ("master") record, then pull missing data from the loser so nothing is lost:
1. **Master = most complete + most recently active** record (most filled fields, most logged activity, most recent touch).
2. **Field-level rule:** for each field, keep the master's value if present; otherwise fill from the duplicate. Never overwrite a good value with a blank.
3. **Never lose:** merge — don't discard — all emails, phones, notes, activity history, tasks, and deal associations from the loser onto the master.
4. **Conflicts** (two different phone numbers, two owners): keep both where the field allows multiples; otherwise surface the conflict for the owner to pick.
5. **Show the before/after** of the surviving record so the owner sees exactly what data carries over.

### Stale-deal thresholds by stage
"Stale" depends on where the deal sits and your sales-cycle length. Default no-activity thresholds:

| Stage | Stale after | Default proposal |
|---|---|---|
| New / Lead | 14 days | Nurture or disqualify |
| Qualified | 30 days | Re-engage, else nurture |
| Proposal / Quote sent | 21 days | Follow up; if silent 45d → close-lost |
| Negotiation | 30 days | Owner attention |
| Verbal / Commit | 14 days | Confirm or slip date |

Adjust to your cycle: a 6-month-sales-cycle business should roughly double these. Always propose the status change with the last-activity date and a reason — never auto-close.

### Field-completeness standard
Define "complete" so missing-field scans are consistent. Minimum viable record:
- **Contact:** name, valid email OR phone, company, owner, lifecycle stage, source.
- **Deal:** name, linked contact/company, stage, value, expected close date, owner.
Flag any record missing a required field; group by field so the owner can fix in bulk (e.g., "9 deals missing an owner — assign all to [rep]?").

### Cleanup impact framing
Quantify why the cleanup matters so the owner prioritizes: "11 stale deals inflate pipeline by $27k — closing the dead ones makes the forecast real"; "6 duplicates mean some customers got double-emailed"; "9 ownerless records mean nobody's following up." Impact turns a chore into a decision.

### Owner-approval gate
This is a proposal engine. Merges, deletions, and status changes are irreversible or customer-affecting and require explicit owner approval — item by item or a blanket "all." After applying only the approved items, return a precise change log (what merged into what, which deals closed, which fields filled) so every change is auditable and reversible if wrong.
