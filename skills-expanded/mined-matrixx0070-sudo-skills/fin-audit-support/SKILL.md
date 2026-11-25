---
name: fin-audit-support
version: 1.0.0
description: Support ICFR audits by scoping a key control, selecting a defensible sample, and producing workpapers an auditor can re-perform unaided.
author: matrixx0070
tags: [finance, audit, sox-404, icfr, internal-controls, workpapers, compliance]
---

# Audit Support

## When to use
Use this when you support an internal or external audit of internal control over financial reporting (ICFR), test a SOX 404 key control, or prepare workpapers an auditor can re-perform without asking you a single question.

**Not for:** initial control *design* documentation (use fin-sox-testing for D&I), account-level tie-outs (fin-reconciliation), or financial-statement preparation (fin-financial-statements). This assumes the control already exists and needs testing evidence.

## Method
1. **Scope the control.** Record control ID, the assertion it addresses (existence, completeness, accuracy, valuation, cutoff), the risk it mitigates, and whether it is preventive or detective.
2. **Pick the testing approach.** Choose inquiry, observation, inspection, or re-performance. Decision point: re-performance is strongest — use it for high-risk controls; inquiry alone is *never* sufficient for a conclusion.
3. **Set sample size by frequency.** Daily ~25, weekly ~5, monthly ~2, quarterly ~2, annual 1. Decision point: if the control is high-risk, was changed mid-period, or relies on an automated step that could have broken, increase the sample and split it before/after the change.
4. **Select the sample.** Use random or systematic (interval) selection from the *full* population. Document population source, total count, and method so it is reproducible.
5. **Execute.** For each item capture the attribute tested, the evidence inspected, and pass/fail with a specific reason.
6. **Evaluate exceptions.** Decision point: classify each as deficiency, significant deficiency, or material weakness, and judge isolated vs systemic — one exception in a control-change window is systemic, not isolated.
7. **Conclude.** State operating effectiveness and note any compensating controls.

## Example
Control APR-07: two-signature approval on wires over $50k, preventive, addresses *authorization*. It fires ~daily, so you pull 25 of 312 wires by interval selection (every 12th, seed documented). Attributes: (a) both signatures present, (b) signer within authority matrix, (c) approval dated before release. Item 14 shows one signature only — a control deficiency. It is isolated (1/25), no dollar impact (wire was valid), compensating detective bank-recon caught nothing amiss. Conclusion: operating effectively with one noted deficiency, remediation logged.

## Pitfalls
- **Sampling from an incomplete population.** If you cannot tie the population to a system total, your sample proves nothing — completeness first.
- **Treating inquiry as evidence.** "They told me they check it" is not a test result. Inspect artifacts.
- **Auto-classifying one exception as isolated.** Frequency and root cause decide severity, not the count.
- **Non-reproducible selection.** No seed, no interval, no source = the auditor re-derives a different sample and rejects yours.

## Output format
```
Control: <ID> | Assertion: <...> | Risk: <...> | Type: prev/det | Freq: <...>
Approach: <inquiry/obs/insp/re-perf> — rationale: <...>
Population: source <...> | total <n> | tied to <system total>
Sample: size <n> | method <random/interval, seed> | reproducible: yes
Test of detail:
  | item | attribute | evidence | result | note |
Exceptions: | desc | severity | isolated/systemic | root cause |
Conclusion: effective / deficient | compensating controls: <...>
Open items: <...>
```

## Reference

### Financial-statement assertions (what a control must cover)
Every key control maps to one or more assertions. Name the assertion when scoping so the test targets the right risk.

| Assertion | Question it answers | Typical control |
|---|---|---|
| **Existence / occurrence** | Did the recorded item really happen / exist? | Approval, three-way match, physical count |
| **Completeness** | Is everything that happened recorded? | Sequence checks, cutoff, GRNI review |
| **Accuracy / valuation** | Is the amount right and properly valued? | Recalculation, reconciliation, reserve review |
| **Cutoff** | Is it in the correct period? | Period-end cutoff testing |
| **Rights & obligations** | Do we own the asset / owe the liability? | Title/contract review, confirmations |
| **Presentation & disclosure** | Correctly classified and disclosed? | Disclosure checklist, financial-statement review |

### Testing approaches and when to use them
| Approach | Strength | Use when |
|---|---|---|
| **Inquiry** | Weakest — corroborating only | Never alone; always paired with another |
| **Observation** | Point-in-time only | Confirming a process is performed |
| **Inspection** | Strong for documented controls | Approvals, sign-offs, reconciliations |
| **Re-performance** | Strongest | High-risk key controls; independent recompute |

Inquiry alone can never support a conclusion. For a system-generated report used in a control, test the **IPE (information produced by the entity)** — completeness and accuracy of that report — before relying on it.

### Sample size by frequency (attribute testing)
| Frequency | Population | Sample |
|---|---|---|
| Many times daily | thousands | 25–40 |
| Daily | ~250 | 25 |
| Weekly | ~52 | 5 |
| Monthly | 12 | 2 |
| Quarterly | 4 | 2 |
| Annual | 1 | 1 |
| Automated | one config | 1 (+ GITCs) |

Increase and split the sample for high-risk controls, prior-year exceptions, or a mid-period control change (test before and after separately).

### Workpaper standard (auditor can re-perform unaided)
A defensible workpaper states: control ID and description; assertion and risk; population source, total count, and completeness tie-out to a system total; selection method, seed/interval, and the exact items pulled; attributes defined *before* selection; per-item evidence inspected and pass/fail with a specific reason; exceptions with severity and root cause; conclusion on operating effectiveness; and any compensating controls. Tickmarks and cross-references must let a reviewer trace every number back to source. The test: an auditor re-derives your sample and your conclusion without asking you a single question.

### Exception evaluation
Classify each exception as **deficiency / significant deficiency / material weakness** by likelihood × magnitude and by root cause — not by count. Judge **isolated vs. systemic**: one exception inside a control-change window, or one tied to a process gap, is systemic. Quantify dollar impact where relevant, but note that a control can be deficient even with no dollar misstatement (the control failed to operate). Look for a **compensating control** that mitigates before concluding, and log remediation with an owner and date.

### GITCs (IT general controls) — the foundation
Automated-control reliance depends on effective GITCs: **access to programs and data** (provisioning, periodic access reviews, segregation of duties), **program changes** (change management, testing, approval), **program development**, and **computer operations** (job scheduling, backup, incident management). If GITCs are ineffective, automated application controls cannot be relied upon and must be tested manually or supplemented with substantive procedures.
