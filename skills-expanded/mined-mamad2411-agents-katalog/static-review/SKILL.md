---
name: static-review
description: >-
  Plan and run work-product reviews (requirements, design, code, test bases) per ISTQB
  CTFL v4.0 §3 and the ISO/IEC 20246 review process — static testing that finds defects
  before any code runs. Use when: "static testing," "review," "静的テスト," "レビュー,"
  "requirements/design review," "inspection," "walkthrough," "review meeting,"
  "レビュー会の進め方," or catching defects early in a work product. Produces a review
  plan, roles, and an anomaly log/report (design mode). Not for: assessing code
  testability / test-suite effectiveness — use maintainability-review; or running the
  software. Related: maintainability-review, defect-report.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §3 (§3.1–3.2)"
  iso25010: [functional-suitability, performance-efficiency, compatibility, interaction-capability, reliability, security, maintainability, flexibility, safety]
  mode: [design]
---

# Static Review

Find defects by examining a work product — not by executing it — using the right review
type and the ISO/IEC 20246 process, so requirements/design defects are caught before
they become expensive code defects.

## Objective

A review that fits its work product's risk: the right review type, defined roles, the
ISO/IEC 20246 activities, and an anomaly log that feeds fixes. Per CTFL v4.0 §3.1.2,
static testing catches defects in the earliest SDLC phases and finds defects dynamic
testing cannot (e.g. unreachable code), usually at far lower overall cost. The failure
mode this prevents: a requirements ambiguity discovered in system test, when it costs
10× to fix.

## Organization-specific inputs (fill these in)

- **What gets reviewed** and at which review type — map work products (requirements,
  design, code, test cases, contracts) to informal / walkthrough / technical review /
  inspection based on risk.
- **Roles & who fills them**: moderator/facilitator, scribe, reviewers, review leader.
- **Checklists / reference bases** per product type; the entry condition to start a
  review and the exit condition to end it.
- **Tooling** (review in the PR tool, a dedicated review tool, or documents).

## Context Discovery

- What work product, how risky/critical, and how stable? (drives review formality)
- Are there existing review checklists or a definition-of-done for the product type?
- Who are the qualified reviewers and stakeholders?

## Instructions

1. **Choose the review type** (§3.2.4) by needed formality and objective:
   - **Informal** — no defined process, no formal output; goal: detect anomalies fast.
   - **Walkthrough** — led by the author; evaluate quality, build consensus, educate,
     detect anomalies.
   - **Technical review** — technically qualified reviewers led by a moderator; reach
     decisions on a technical problem and detect anomalies.
   - **Inspection** — most formal; follows the full process, collects metrics; the
     author cannot be review leader or scribe. Goal: maximum anomalies found.

2. **Assign roles** (§3.2.3): manager (allocates resources), author (creates/fixes),
   moderator/facilitator, scribe/recorder, reviewer(s), review leader.

3. **Run the ISO/IEC 20246 process activities** (§3.2.2): planning → review initiation
   → individual review → communication and analysis → fixing and reporting.

4. **Log anomalies, don't fix in the meeting**: the review detects; the author fixes
   afterward. Record each anomaly with location and severity.

5. **Apply success factors** (§3.2.5): right reviewers, defects welcomed neutrally and
   blamelessly, review chunks kept small enough to stay effective.

## Output Format

### design mode

```
# Review Plan: {work product}
## Type & rationale (informal/walkthrough/technical review/inspection)
## Roles (moderator, scribe, reviewers, review leader, author, manager)
## Entry / exit conditions · reference base / checklist
## Anomaly log
   | ID | Location | Description | Severity | Raised by | Status |
## Report (metrics for inspections: anomalies found, effort, coverage of product)
```

## Anti-Patterns

- **Fixing in the review meeting** — derails detection into debugging. **Guard:** log
  anomalies; the author fixes afterward (fixing & reporting is a later activity).
- **Blame culture** — reviewers attack the author, defects get hidden. **Guard:**
  defects are welcomed neutrally; review the product, not the person (§3.2.5).
- **Reviewing too much at once** — effectiveness drops on oversized chunks. **Guard:**
  bound the review size; split large products.
- **No defined type or roles** — an ad-hoc meeting with no moderator/scribe. **Guard:**
  pick a review type and assign roles before starting.
- **Skipping individual preparation** — reviewers reading it cold in the meeting.
  **Guard:** individual review precedes communication & analysis.

## Related Skills

- `maintainability-review` — assesses code testability and test-suite effectiveness
  (mutation/complexity); this skill is the human review process for any work product.
- `defect-report` — anomalies confirmed as defects become defect reports.

## References

- ISTQB CTFL v4.0 Syllabus §3 (Static Testing): §3.1 basics/value, §3.2 review process,
  types (§3.2.4), roles (§3.2.3), activities (§3.2.2)
- ISO/IEC 20246 — Work product reviews (the generic review process CTFL references)
