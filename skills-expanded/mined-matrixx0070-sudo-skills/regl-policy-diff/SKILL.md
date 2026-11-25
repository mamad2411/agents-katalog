---
name: regl-policy-diff
version: 1.0.0
description: Diff a new or proposed rule against your current internal policy to surface exactly what changed, what it obligates, and where you are now out of step.
author: matrixx0070
tags: [regulatory, legal, policy-diff, gap-analysis, compliance, rulemaking]
capabilities: []
---

## When to use

Use this when a rule, guidance document, or amendment lands and you must know how it differs from the obligations you already meet. Reach for it after regl-reg-feed-watcher flags a hit, or whenever someone asks "does this actually change anything for us?"

**Not for:** discovering unmet obligations with no triggering rule (use regl-gap-surfacer), rewriting the policy text itself (use regl-policy-redraft), or tracking the comment clock (use regl-comments). Any diff that changes legal exposure is analysis, not advice — route the conclusion to an attorney before acting.

## Method

1. Pin both sides precisely: the incoming instrument (docket/RIN, stage, effective date) and the exact current policy version/section it maps to. Diffing against a stale policy invents phantom gaps.
2. Extract obligations, not prose. Reduce each side to atomic requirements: who must do what, by when, evidenced how. Compare requirement-to-requirement.
3. Classify each delta: NEW (obligation you don't meet), TIGHTENED (stricter than today), RELAXED (you may simplify), UNCHANGED (already compliant), or AMBIGUOUS (text unclear).
4. **Decision point:** for proposed rules (NPRM), mark deltas as provisional — the final rule may move. For final rules, mark them binding with the effective/phase dates.
5. Rate each delta's impact (effort × exposure) and note the internal owner who must respond.
6. Flag every AMBIGUOUS or exposure-changing delta for attorney review; do not resolve legal ambiguity yourself.

## Example

> Incoming: Final rule, RIN 3170-AB00, effective 2027-01-01. Current: Data-Retention Policy v4, §3. Delta 1 (TIGHTENED): retention max cut 7y→5y — impact high, owner Records. Delta 2 (NEW): annual deletion attestation — impact medium, owner Compliance. Delta 3 (AMBIGUOUS): "affiliated entities" scope unclear → attorney review.

## Pitfalls

- Diffing narrative against narrative instead of obligation against obligation.
- Comparing to an outdated policy version, producing false NEW deltas.
- Treating NPRM deltas as final and re-tooling before the rule settles.
- Silently resolving ambiguous scope language that only counsel should interpret.

## Output format

```
POLICY DIFF — <rule docket/RIN, stage> vs <policy name/version §>
Effective: <date or provisional>
Delta | Type (NEW|TIGHTENED|RELAXED|UNCHANGED|AMBIGUOUS) | Impact | Owner
---
Attorney review needed: <deltas flagged>
Recommended next step: <redraft | comment | monitor>
```

## Reference

**Rulemaking lifecycle:** ANPRM → NPRM → comments → final rule → effective (often phased). Only final rules create binding obligations; NPRM text routinely changes before finalization, so provisional-tag NPRM deltas.

**Comment-period mechanics:** if the diff finds costly or unworkable proposed deltas, that is exactly the material for a comment during the open window — hand it to regl-comments rather than absorbing the cost silently.

**Policy-diff method:** normalize both sides to atomic obligations (actor / action / trigger / deadline / evidence), then set-difference them. Classify by direction and certainty. Attorney-escalation gate: ambiguous or exposure-shifting deltas are legal calls, not operational edits.
