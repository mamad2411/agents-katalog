---
name: wcag-review
description: "Audit page sets and workflows against selected WCAG 2.2 (default) or 2.1 A/AA/AAA requirements, with draft WCAG 3.0 research separate. Use for frontend accessibility reviews, PR audits and conformance gap analysis."
---

# Audit accessibility across a selected WCAG 2.x standard

## Scope

Resolve **version + conformance level** via `../wcag-diagnose/references/standard-selection.md` before selecting requirements. Default **WCAG 2.2 AA** (55 criteria); explicit legacy **WCAG 2.1 AA** (50 criteria). Record the source of selection, assessed routes/processes, user roles, browser/AT support, representative states and evidence boundaries.

## Procedure

1. For product-wide evaluations, read `../wcag-diagnose/references/evaluation-methodology-2.0.md` and document evaluation scope, exploration, representative sample rationale, accessibility support baseline, and reporting limits. This W3C Group Note is informative, not an additional WCAG requirement. Then read the selected criterion catalog (`2.2/criteria.json` or `2.1/criteria.json`), `standards.json` and corresponding `2.2/conformance.json` or `2.1/conformance.json` in `../wcag-diagnose/references/`. Do not use the taxonomy union as the evaluation set.
2. Cover complete pages and every step in complete processes, including login, recovery, error, loading, success, responsive, touch/keyboard and third-party states.
3. For **every** applicable-level criterion, record `pass`, `fail`, `not_applicable`, `not_tested` or `needs_manual_review`; document reason/evidence for N/A. Do not exclude criteria that scanners cannot test.
4. Combine automation and manual keyboard, screen reader, zoom/reflow, touch, visual, media and content equivalence checks; include actual browser/AT matrix. Read `references/evidence-matrix.md` and specialist playbooks on demand.
5. Assess normative criteria against the **selected version's** W3C source. WCAG 2.2 removes 4.1.1 and adds nine; do not mix criteria. At 2.2 AA, test 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8 as relevant, while AAA additions apply only to AAA.
6. Summarize findings, unresolved failures and manual gaps. WCAG 3.0 guidance, if requested, belongs in an **advisory appendix** with snapshot date and no conformance implication.

Severity is based on user impact and task obstruction, not merely SC level. Report scope, criterion coverage, evidence, repair owner, and exact re-test. Never call a partial sample or automated scan a conformance determination.
