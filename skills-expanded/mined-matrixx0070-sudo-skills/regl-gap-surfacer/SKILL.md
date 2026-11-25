---
name: regl-gap-surfacer
version: 1.0.0
description: Proactively hunt for latent compliance gaps — obligations you already carry but do not yet meet — before a regulator or auditor finds them.
author: matrixx0070
tags: [regulatory, legal, gap-analysis, compliance, audit, risk]
capabilities: []
---

## When to use

Use this to audit your current state against obligations already in force, independent of any new rule. Reach for it before an exam, when entering a new jurisdiction or product line, after an acquisition, or on a periodic control review — anywhere unmet obligations may be hiding.

**Not for:** measuring the delta from a single new rule (use regl-policy-diff), rewriting policy text (use regl-policy-redraft), or the weekly rollup (use regl-gaps). Any surfaced gap that carries live legal exposure goes to an attorney to scope liability before remediation is promised externally.

## Method

1. Build the obligation inventory: enumerate every rule, standard, and contractual commitment currently binding on the scoped business, keyed to jurisdiction and effective date. Missing obligations cannot be gapped.
2. For each obligation, locate the evidence that you meet it — a control, policy, log, or attestation. No evidence is itself a gap.
3. Classify each: MET (evidenced), PARTIAL (some coverage), UNMET (no control), or UNKNOWN (owner can't confirm). Treat UNKNOWN as a finding, not a pass.
4. **Decision point:** rank gaps by exposure (penalty severity × likelihood of exam) not by ease of fix — remediate the dangerous ones first.
5. Assign each gap an owner and a realistic remediation path; distinguish a quick control fix from a structural change.
6. Flag any gap with active legal exposure or reporting/self-disclosure implications for attorney review before it is documented as a known deficiency.

## Example

> Scope: EU data processing. Inventory: 14 obligations. Findings: UNMET — no DPIA for the new analytics pipeline (high exposure, owner Privacy); PARTIAL — breach-notification runbook exists but untested (medium, owner Security); UNKNOWN — sub-processor list currency unconfirmed → treat as gap. Self-disclosure question on the DPIA gap → attorney review before any regulator contact.

## Pitfalls

- Auditing controls you have instead of obligations you owe — you only find gaps in things you thought to check.
- Scoring UNKNOWN as compliant, so blind spots never get remediated.
- Prioritizing by fix effort, leaving the highest-penalty gap for last.
- Documenting a known deficiency in writing before counsel weighs in on disclosure duties.

## Output format

```
GAP SURFACE — <scope/jurisdiction> | as of <date>
Obligation | Source | Status (MET|PARTIAL|UNMET|UNKNOWN) | Evidence | Exposure | Owner
---
Prioritized gaps (by exposure):
  1. <gap> — <remediation path> — owner — <attorney review?>
Attorney review needed: <gaps with disclosure/liability implications>
```

## Reference

**Rulemaking lifecycle:** gaps arise not only from new rules but from final rules that already reached their effective date while your controls lagged — this skill catches the accumulated backlog the diff pipeline missed.

**Comment-period mechanics:** if a gap traces to an obligation still at NPRM stage, it is premature — do not remediate against unfinalized text; route it to regl-comments instead.

**Policy-diff method:** the inventory-and-evidence approach is a diff against reality — obligation (expected) vs control (actual), set-differenced. Attorney-escalation gate: gaps with penalty, disclosure, or self-reporting implications are legal determinations; counsel scopes exposure before any written admission or external commitment.
