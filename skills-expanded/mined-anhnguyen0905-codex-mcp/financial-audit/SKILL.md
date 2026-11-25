---
name: financial-audit
description: Financial and internal audit method — audit planning, risk assessment, materiality thresholds, sampling, internal control walkthroughs and control testing, substantive procedures, audit evidence standards, workpapers, findings and management letters, fraud red flags, segregation of duties. Use for auditing financial statements, internal controls, expense compliance checks, or preparing for an external audit. Not for code/security audits.
---

# Financial Audit (risk, controls, evidence, findings)

## The method is risk-first, not checklist-first

1. **Plan**: understand the entity, set materiality, identify where the statements are most likely
   to be materially wrong (risk assessment by account and assertion).
2. **Test controls** where you intend to rely on them; otherwise go straight to substantive work.
3. **Substantive procedures** sized to residual risk: more risk → more evidence.
4. **Conclude and report**: findings with condition/criteria/cause/effect, a management letter,
   and workpapers that let a stranger re-perform the audit.

Effort follows risk. Auditing every account equally means over-auditing petty cash and
under-auditing revenue.

## Materiality

```
overall materiality      ≈ benchmark × rule-of-thumb %
common rules of thumb:     5% of pre-tax profit, 0.5–1% of revenue, 1–2% of total assets
performance materiality  ≈ 50–75% of overall (working threshold, leaves room for aggregation)
trivial threshold        ≈ 3–5% of overall (below this, don't accumulate)
```

These percentages are convention, not law — pick the benchmark users of the statements care about
and document why. Materiality is also qualitative: a small misstatement that flips a covenant,
turns a loss into a profit, or involves management override is material regardless of size.

## Assertions — what you're actually testing

Every balance is tested against assertions: **existence/occurrence** (it's real), **completeness**
(nothing missing), **accuracy/valuation**, **cutoff** (right period), **rights and obligations**,
**presentation**. Direction matters: existence testing samples from the ledger to source documents;
completeness samples from source documents (or the world) back to the ledger. Testing the wrong
direction finds nothing — you cannot prove completeness by vouching ledger entries.

## Controls: walkthrough, then test

- **Walkthrough**: trace one transaction end-to-end to confirm the process is as described. It
  proves design, not operation.
- **Control testing**: sample the control's operation across the period (common convention:
  25–40 items for a frequent manual control, 1 for an automated control plus IT general controls).
  A deviation triggers evaluation — root cause, possible sample extension, and deficiency assessment — never a silent waiver as "isolated".
- **Segregation of duties**: no one person should initiate, approve, record, AND hold the asset.
  In small entities where this is impossible, compensating review by the owner is the fallback —
  test that the review actually happens (evidence of it, not assertion of it).

## Sampling and substantive work

State population, method (random/monetary-unit/haphazard — never "judgmental picks of clean
items"), sample size rationale, and how errors extrapolate to the population. Substantive staples:
external confirmations (bank, AR, legal), cutoff testing either side of period end, analytical
procedures with an **expectation formed before** looking at the actual, recalculation, and
physical inspection. An analytical procedure without a pre-formed expectation is a narrative,
not evidence.

## Evidence and workpapers

Evidence hierarchy (strongest first): auditor-generated → external third-party → internal but
externally validated → internal → inquiry alone. Inquiry is never sufficient by itself. Each
workpaper: purpose, source, work performed, result, conclusion, preparer/reviewer and dates —
the re-performance standard: a competent stranger can redo it from the paper alone.

## Fraud red flags

Revenue spikes at period end reversed after; round-number or just-below-approval-threshold
payments; vendors sharing addresses/bank accounts with employees; dormant accounts reactivated;
management override of controls; missing originals with "copies available"; one person who never
takes vacation and won't hand over their process. Red flags demand extended procedures, not
comfort from management explanation.

## Findings and reporting

Every finding carries: **condition** (what is), **criteria** (what should be), **cause**,
**effect/exposure**, and **recommendation** — rated by severity. Management's response is attached,
not merged into the finding. The management letter covers control improvements below the reporting
threshold; it is not a dumping ground for hedged non-findings.

## Failure modes

- Materiality set after fieldwork to make known misstatements immaterial.
- Testing existence and claiming completeness (direction error).
- Sample of the easiest/cleanest items, deviations waived as "isolated" without extension.
- Reliance on controls that failed testing, with no increase in substantive work.
- Evidence = management said so, documented as "discussed with CFO, no issues noted".
- Findings softened until condition and criteria are indistinguishable.
- Workpapers that reference conclusions with no trail of what was actually done.

## Reviewer checklist

- [ ] Materiality benchmark, %, and rationale documented before fieldwork
- [ ] Risk assessment maps to the procedures actually performed (effort follows risk)
- [ ] Each test names its assertion and samples in the correct direction
- [ ] Sampling method and error extrapolation documented; deviations extended, not excused
- [ ] No conclusion rests on inquiry alone
- [ ] Findings have condition/criteria/cause/effect and a severity rating
- [ ] Workpapers pass the re-performance standard

## Provenance

Distilled from standard audit methodology (ISA/GAAS-style). Materiality percentages and sample
sizes are rules of thumb, not requirements — firm methodology and applicable standards govern on
a real engagement. This is method guidance, not an audit opinion.
