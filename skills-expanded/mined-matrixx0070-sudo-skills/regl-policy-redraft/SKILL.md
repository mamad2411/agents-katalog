---
name: regl-policy-redraft
version: 1.0.0
description: Redraft an internal policy to close identified gaps and align it with a new rule — precise, traceable edits with rationale, not a wholesale rewrite.
author: matrixx0070
tags: [regulatory, legal, policy-drafting, remediation, compliance, redline]
capabilities: []
---

## When to use

Use this after a diff or gap analysis has identified specific deltas and you need to update the governing policy text to meet the new obligation. Reach for it to turn findings into concrete, reviewable redline edits with a rationale trail.

**Not for:** finding what changed (use regl-policy-diff) or what is unmet (use regl-gap-surfacer), tracking deadlines (use regl-gaps), or filing a public comment (use regl-comments). Policy language that creates legal obligations or waivers must be attorney-reviewed and approved before it takes effect — you draft, counsel signs off.

## Method

1. Start from the finding, not a blank page: list the exact deltas or gaps this redraft must close, each tied to its source rule provision.
2. Locate the precise policy section for each delta. Edit surgically — change only what the finding requires so review stays focused and the change history stays clean.
3. Draft each edit as a redline (old → new) with a one-line rationale citing the driving provision (RIN/section). Traceability is what lets counsel and auditors approve fast.
4. Preserve internal consistency: check that the edit does not contradict adjacent clauses, defined terms, or linked procedures.
5. **Decision point:** distinguish a plain conformance edit (procedural, low-risk) from language that shifts legal posture, creates a waiver, or alters liability — the latter must go to attorney review before adoption.
6. Set the effective date to align with the rule's compliance date, and note any transition/phase-in language.
7. Route the redline for approval and record who signed off.

## Example

> Finding: Delta 1 (TIGHTENED) retention 7y→5y; Delta 2 (NEW) annual deletion attestation. Redraft: §3.2 "retain up to seven (7) years" → "up to five (5) years" (rationale: RIN 3170-AB00 §12(a)). Add §3.5 requiring annual deletion attestation by Records Owner (rationale: §12(c)). Effective 2027-01-01. Attorney-reviewed (retention change touches litigation-hold policy). Approved: GC, 2026-11-03.

## Pitfalls

- Rewriting the whole policy when three clauses needed changing — bloats review and hides the real change.
- Editing without citing the driving provision, leaving no rationale trail for audit.
- Breaking a defined term or contradicting a linked procedure elsewhere in the policy.
- Shipping liability-shifting language without attorney sign-off.

## Output format

```
POLICY REDRAFT — <policy name/version> | driving rule: <RIN/section>
Redline:
  §<x>: "<old text>" → "<new text>"  (rationale: <provision>)
  +§<y>: "<new clause>"  (rationale: <provision>)
Consistency check: <defined terms / linked procedures verified>
Effective date: <date> | Transition: <phase-in note>
Attorney reviewed: <yes/no> | Approved by: <name, date>
```

## Reference

**Rulemaking lifecycle:** only redraft against final rules — text at NPRM stage may change, and redrafting to a proposal risks re-work. Align the policy effective date to the rule's compliance/phase-in date, not the publication date.

**Comment-period mechanics:** if the driving rule is still in its comment window, the correct action is to comment (regl-comments), not to redraft; hold redrafting until the rule is final.

**Policy-diff method:** every edit maps one-to-one to a classified delta (NEW/TIGHTENED/RELAXED) with the provision cited — the redline is the diff, resolved. Attorney-escalation gate: conformance edits proceed on your draft; liability-, waiver-, or posture-shifting language requires counsel approval before it becomes effective policy.
