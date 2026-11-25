---
name: gap-analysis
description: Guides comparing current state against a target framework (ISO 27001, NIST CSF, SOC 2, etc.), scoring control maturity, and producing a prioritized gap list. Use when the user asks for a gap analysis, readiness assessment or maturity assessment, or wants to know how far they are from compliance with a standard.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Gap analysis workflow

Measure "where we are" vs "what <framework> requires", output a ranked remediation list.
Don't lecture on the framework; fetch its current control text and score against it.

## 1. Fix the target

- Confirm framework + version: ISO 27001:2022 Annex A, NIST CSF 2.0, SOC 2 TSC,
  CIS Controls v8.1, PCI DSS v4.0.1 (its future-dated requirements are mandatory since
  31 Mar 2025: score against those, not v3.2.1), etc. Versions move: `load_skill control-frameworks`
  and web-fetch the live control list; never score against memory.
- Confirm scope boundary (which systems/org units) before scoring, or gaps are noise.

## 2. Score each control's maturity

Per control, rate current state on a 0-5 implementation scale:

| Score | State                                                 |
| ----- | ----------------------------------------------------- |
| 0     | Nonexistent: not done, nobody owns it.                |
| 1     | Initial: ad hoc, undocumented, person-dependent.      |
| 2     | Repeatable: done consistently but no written process. |
| 3     | Defined: documented, communicated, followed.          |
| 4     | Managed: measured, metrics/KPIs, evidence retained.   |
| 5     | Optimised: reviewed and continuously improved.        |

- Target maturity is usually 3 (certification floor) unless the org sets higher.
- Gap = target - current. Only scores below target are gaps.
- Evidence-back every score: policy doc, config, ticket, `findings.md` entry. A
  proven pentest finding caps the related control's score (you can't claim
  "Managed" access control while an IDOR is open).

## 3. Prioritise

Rank gaps by: gap size x risk x (low) effort. Quick decision rule:

| Gap size | Linked risk   | Effort  | Priority    |
| -------- | ------------- | ------- | ----------- |
| >=2      | High/Critical | Any     | P1: now     |
| any      | High/Critical | Low     | P1: now     |
| >=2      | Medium        | Low/Med | P2: quarter |
| 1        | any           | any     | P3: backlog |

- Cluster gaps that share one fix (one IAM project may close 6 access controls);
  surface the shared root cause, not 6 line items.

## 4. Emit the gap list

`write_file /work/gap-analysis.md`:

| Control ID | Requirement (short) | Current | Target | Gap | Evidence/finding ref | Remediation | Owner | Priority |
| ---------- | ------------------- | ------- | ------ | --- | -------------------- | ----------- | ----- | -------- |

- Include a one-line coverage summary: X of Y controls at/above target (% compliant).
- Note explicitly-out-of-scope or not-applicable controls with a reason; silence reads as a miss.
- For the "Evidence/finding ref" column, map each finding to IEC 62443 / CRA / NIS2 obligations with `load_skill finding-control-crosswalk`.

## Anti-patterns

- Don't score "compliant/non-compliant" binary; maturity shows trajectory and effort.
- Don't accept a self-reported score with no artifact; mark it "unverified", treat as <=1.
