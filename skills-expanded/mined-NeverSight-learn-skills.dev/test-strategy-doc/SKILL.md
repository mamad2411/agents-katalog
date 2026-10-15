---
name: test-strategy-doc
description: >-
  Generate an ISTQB- and ISO/IEC 25010:2023-aligned test strategy document from a
  PRD, feature spec, or codebase. Includes a mandatory quality-characteristics
  priority assessment covering all nine ISO 25010:2023 characteristics, test
  levels/types, entry/exit criteria, and risk-based scope. Use when: "test strategy,"
  "テスト戦略," "QA plan," "testing approach," "what's our overall testing approach,"
  or any request for test planning documentation. Not for: prioritizing/sequencing
  test effort under time pressure — use risk-based-testing; or designing individual
  test cases — use the test-design skills. Related: risk-based-testing, boundary-value-analysis.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §5.1"
  iso25010: [functional-suitability, performance-efficiency, compatibility, interaction-capability, reliability, security, maintainability, flexibility, safety]
  mode: [design]
---

# Test Strategy Document

Produce an actionable, standards-traceable test strategy — a document that drives
testing decisions, with every scope choice justified by a quality characteristic and
a risk level.

## Objective

A strategy document where (a) all ISO/IEC 25010:2023 quality characteristics have been
explicitly prioritized — including the ones deprioritized, with reasons — and (b) test
levels, types, and exit criteria trace to those priorities. The failure mode this
prevents: strategies that only cover functional testing because nobody asked "what
about flexibility?"

## Context Discovery

Gather before writing. Read the PRD/spec/codebase first; ask only for gaps:

- Product type, users, business-critical flows
- Release cadence and compliance requirements (PCI-DSS, GDPR, 医療機器 etc. — these
  force certain characteristics to Critical)
- Current test assets and team composition
- Deployment targets (single cloud? on-prem? multi-platform? — this decides whether
  flexibility/compatibility are relevant or safely deprioritized)

## Instructions

1. **Assess all quality characteristics — no skipping**: Fill the ISO 25010:2023
   priority table below for every characteristic. "Low priority, because X" is a valid
   entry; a missing row is not. This forces the conversation that ad-hoc strategies skip.

2. **Derive test types from priorities**: Each characteristic rated High/Critical must
   map to at least one concrete test type with an owner and a tool. A Critical rating
   with no corresponding test type is a contradiction — flag it.

3. **Define test levels**: Unit/integration/E2E split with target ratios and run
   frequency (ISTQB §2.1). Justify deviations from the standard pyramid.

4. **Set entry/exit criteria per level** (ISTQB §5.1.3): measurable, e.g. "exit system
   test: 0 open critical defects, requirement coverage ≥ 95%, flaky rate < 2%."

5. **Scope by risk**: In/out of scope with reasons. Out-of-scope items name the risk
   owner who accepted the gap.

6. **Add traceability appendix**: table mapping each strategy section → ISO 25010:2023
   characteristic / ISTQB syllabus section, for audit use.

## Output Format

ALWAYS include these sections, in order:

```
# Test Strategy: {Product/Feature}
## 1. Scope & Objectives
## 2. ISO/IEC 25010:2023 Quality Characteristics Priority Assessment
   | Characteristic | Priority (Critical/High/Med/Low) | Rationale | Test Types |
   (one row per characteristic — Functional Suitability, Performance Efficiency,
    Compatibility, Interaction Capability, Reliability, Security, Maintainability,
    Flexibility, Safety*)
## 3. Test Levels & Types (owner, framework, target volume, frequency)
## 4. Entry / Exit Criteria per Level
## 5. Risk-Based Scope (in/out, accepted risks, risk owners)
## 6. Environments & Data
## 7. Quality Gates & Metrics
## 8. Traceability Appendix (section → ISO 25010:2023 / ISTQB reference)
```

*State the edition used in section 2. This skill defaults to ISO/IEC 25010:2023 (nine
characteristics). If a client mandates the 2011 model, map Interaction Capability →
Usability and Flexibility → Portability, and drop the Safety row.

## Anti-Patterns

- **Silent deprioritization** — omitting a characteristic instead of rating it Low
  with a reason. **Guard:** the priority table must have all rows; empty = incomplete.
- **Critical rating, no test** — declaring Security "Critical" while section 3 has no
  security test type. **Guard:** cross-check section 2 vs 3 before finalizing.
- **Shelf-document bloat** — 50 pages of boilerplate nobody reads. **Guard:** cap at
  what the team size warrants; every section must contain a decision, not a definition.
- **Unmeasurable exit criteria** — "quality is sufficient." **Guard:** every criterion
  has a number and a measurement source.

## Related Skills

- `risk-based-testing` — produces the risk matrix consumed by section 5.
- `boundary-value-analysis` and other test-design skills — execute section 3.

## References

- ISTQB CTFL v4.0 Syllabus §5.1 (Test Planning), §2.1 (Test Levels)
- ISO/IEC 25010:2023 (product quality model — nine characteristics)
- ISO/IEC/IEEE 29119-3 (test documentation structure)
