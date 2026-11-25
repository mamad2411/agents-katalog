---
name: sow-review
description: Review a Statement of Work for scope risks, ambiguous language, missing protections, and negotiation points. Use before signing or whenever a client sends a new or revised SOW. Usage - /sow-review path/to/sow.md
---

# SOW Review

Review a Statement of Work for scope risks, ambiguous language, missing protections, and
negotiation opportunities. Best run before signatures, not after.

## Input

`$ARGUMENTS` is the path to the SOW (`.md`, `.txt`, `.docx`, or `.pdf`), optionally followed by
context after `--`, for example:

```
/sow-review my-projects/client/sow.md -- fixed-price, client wants to start in 3 weeks
```

If no path was given, ask for one. Do not review from memory of an earlier conversation.

## Steps

Read the full document first. Then assess it across the dimensions below and produce the
structured output. Quote the document's own words wherever you flag a risk, with the section
number, so the reader can find it.

## Output

**Overall Risk Rating:** [🔴 High / 🟡 Medium / 🟢 Low]: one-sentence summary

**Scope Risks:**
- Ambiguous deliverables, undefined acceptance criteria, or scope that could "expand by interpretation"
- Quote the specific language and explain the risk

**Commercial Risks:**
- Pricing assumptions that may not hold, payment terms, penalty clauses, IP ownership, limitation of liability gaps

**Timeline Risks:**
- Aggressive milestones, dependencies on client actions not contractually required, holidays or blackout periods unaccounted for

**Assumptions & Exclusions:**
- List any assumptions that shift risk to the client. Are they explicit and strong enough?
- Flag any missing exclusions that should be there

**Change Control:**
- Is there a defined change control process? What triggers it? Who approves?

**Recommended Negotiation Points:**
- Top 3 to 5 specific changes to request before signing, with suggested replacement language

**What I did not check:** one or two lines naming anything the review could not assess from the
document alone (for example, whether the rate card matches the firm's standard).

Use direct, practical language. This review is for the delivery lead, not the client. The
negotiation is the lead's to run; this review is the preparation.

## Example Output

**Overall Risk Rating:** 🔴 High. Acceptance criteria are undefined and the change control section is absent.

**Scope Risks:**
- "The team will deliver a fully functional data warehouse" (Section 2.1). "Fully functional" is undefined. Recommend replacing with a specific list of deliverables and a signed acceptance checklist.

**Recommended Negotiation Points:**
1. Add an Acceptance Criteria section specifying test pass rates and sign-off process
2. Insert a Change Control clause (the `/change-request` skill has a template)
3. Clarify client responsibilities for data access and SME availability (currently missing)
