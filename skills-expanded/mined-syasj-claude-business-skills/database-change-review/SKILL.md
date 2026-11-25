---
name: database-change-review
description: "Review a schema or data change for safety, rollback, and lock risk before it reaches production. Use when the user mentions schema review, migration review, database change, backfill review, or asks for a database change review. Engineering skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: engineering
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'database-change-review' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# Database Change Review

Review a schema or data change for safety, rollback, and lock risk before it reaches production.

## When to use this skill

Use this skill when the user:

- schema review
- migration review
- database change
- backfill review

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Prefer the repository's existing patterns. Do not disable security controls, invent credentials, or introduce network calls the user did not ask for.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The change
- Table size and traffic if known
- Rollback idea
- Data correctness risk

## Workflow


### 1. Intent

What user or reporting problem the change serves.
### 2. Safety

Locks, rewrites, and nullability. If size is unknown, say the risk is unknown rather than approving.
### 3. Backfill

How existing rows become valid. A constraint added before a backfill is a finding.
### 4. Rollback

How to get back, or an explicit statement that the change is forward-only and who accepts that.
### 5. Observability

What to watch during the migration.
### 6. Secrets

No production connection strings in the review notes. Ask for redacted plans.

## Output

Deliver a **database change review**.

- Purpose of this database change review, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Aisha Rahman, engineering lead at Fieldnote in Edmonton, needs a database change review by 30 September 2026. A migration adds a NOT NULL column with a default on a table of unknown size and has no rollback.

### Example data

```text
From: Aisha Rahman, engineering lead
Organization: Fieldnote, Edmonton
Date: 14 September 2026
Needed by: 30 September 2026

A migration adds a NOT NULL column with a default on a table of unknown size and has no rollback.

The change: requested 14 September 2026. Not yet approved
Table size and traffic if known: 65 in the last period. No prior period attached, so no trend
Rollback idea: A migration adds a NOT NULL column with a default on a table of unknown size and has no rollback. Stated once, in the ask. Not written down anywhere else
Data correctness risk: Checkout service is open. No score in the file
```

### Example outcome

**Database change review**
To: Aisha Rahman, engineering lead, Fieldnote
Date: 14 September 2026 · Needed by: 30 September 2026

**Decision**
Marks risk unknown, requires a batched plan, and rejects credential pasting.

**What the file supports**

| Input | Value | Status |
| --- | --- | --- |
| The change | requested 14 September 2026. Not yet approved | Needs confirmation |
| Table size and traffic if known | 65 in the last period. No prior period attached, so no trend | Carried into the draft |
| Rollback idea | A migration adds a NOT NULL column with a default on a table of unknown size and has no rollback. Stated once, in the ask. Not written down anywhere else | Carried into the draft |
| Data correctness risk | Checkout service is open. No score in the file | Needs confirmation |

**How this draft was built**

**1. Intent**  
What user or reporting problem the change serves.

**2. Safety**  
Locks, rewrites, and nullability. If size is unknown, say the risk is unknown rather than approving.

**3. Backfill**  
How existing rows become valid. A constraint added before a backfill is a finding.

**4. Rollback**  
How to get back, or an explicit statement that the change is forward-only and who accepts that.

**5. Observability**  
What to watch during the migration.

**Deliberately not done**
- Approving a lock-heavy migration with unknown table size.
- A constraint before the backfill.
- Pasting production credentials into the plan.

**Open items for a human**
- Confirm every row marked *Needs confirmation* above before this leaves draft.
- Anything absent from the file stayed absent. No figure, date, or name was supplied from outside it.

Next: Aisha Rahman by 30 September 2026. This is a draft, not a sign-off.

## Anti-patterns

- Approving a lock-heavy migration with unknown table size.
- A constraint before the backfill.
- Pasting production credentials into the plan.

## Related skills

- `data-migration-plan`
- `release-checklist`
