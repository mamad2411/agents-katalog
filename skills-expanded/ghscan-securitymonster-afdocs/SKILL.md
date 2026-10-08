---
name: afcs
description: "AI-Friendly Compliance Standard. Use when mapping security controls to compliance frameworks (OWASP, NIS2, ISO 27001, etc.), creating risk assessments, checklists, or compliance scorecards."
user-invocable: true
---

# AFCS — AI-Friendly Compliance Standard

Use this skill to map AFSS security controls to external compliance frameworks, create risk assessments, and generate compliance scorecards.

## When to Use

- Mapping controls to OWASP Top 10, NIS2, ISO 27001, SOC 2, or any framework
- Creating compliance checklists for audits
- Performing risk assessments (likelihood x impact)
- Generating compliance scorecards with coverage percentages
- Identifying compliance gaps and remediation plans

## Key Deliverables

```
docs/
  compliance/
    frameworks.yaml                    ← framework registry (required)
    mappings/
      owasp-web-2021.md               ← one mapping per framework
      nis2-article-21.md
    checklists/
      owasp-web-2021-checklist.md      ← one checklist per framework
    risk-assessments/
      system-risk-assessment.md
    scorecards/
      compliance-scorecard.md
    scorecards.yaml                    ← scorecard registry (optional)
```

## Artifact Types

| Type | Description |
|------|-------------|
| `compliance-framework` | Registers a framework the system tracks |
| `compliance-mapping` | Maps framework requirements → AFSS controls/policies |
| `compliance-checklist` | Actionable verification checklist for a framework |
| `risk-assessment` | Likelihood x impact analysis |
| `compliance-scorecard` | Quantitative coverage and maturity scoring |

## Framework Registry (frameworks.yaml)

```yaml
frameworks:
  - framework_id: owasp-web-2021
    name: OWASP Top 10 Web Application Security Risks (2021)
    version: "2021"
    type: industry-standard         # regulation | industry-standard | internal
    url: https://owasp.org/Top10/
    requirements_count: 10
    mapping_path: docs/compliance/mappings/owasp-web-2021.md
    checklist_path: docs/compliance/checklists/owasp-web-2021-checklist.md
    status: active                  # active | planned | deprecated
    last_reviewed: 2026-02-10
```

## Compliance Mapping Metadata

```yaml
---
mapping_id: owasp-web-2021
name: OWASP Top 10 (2021) Compliance Mapping
type: compliance-mapping
framework_id: owasp-web-2021
scope: system
status: active
owner: security-team
last_reviewed: 2026-02-10
coverage_summary:
  total_requirements: 10
  fully_covered: 7
  partially_covered: 2
  not_covered: 1
  not_applicable: 0
  coverage_percent: 80
---
```

## Mapping Body Structure

```markdown
## Framework Overview
Brief description, official URL, why it applies.

## Requirement Mapping Table

| Req ID | Requirement | AFSS Controls | AFSS Policies | Coverage | Notes |
|--------|-------------|---------------|---------------|----------|-------|
| A01:2021 | Broken Access Control | auth-rls-user-profiles | authorization | full | |
| A08:2021 | Software Integrity | — | — | none | No CI/CD integrity |

Coverage values: `full` | `partial` | `none` | `not-applicable`

## Gap Analysis
For each `partial` or `none` entry:
- What is missing
- Recommended AFSS control to create
- Impact on compliance posture

## Remediation Plan

| Priority | Req ID | Gap | Remediation | Target Date | Owner |
|----------|--------|-----|-------------|-------------|-------|
| 1 | A08 | No integrity checks | Create control | 2026-Q2 | platform |
```

## Risk Assessment Schema

```yaml
---
assessment_id: system-risk-2026-q1
name: System Risk Assessment — 2026 Q1
type: risk-assessment
scope: system
methodology: likelihood-impact-5x5
status: current
owner: security-team
assessment_date: 2026-02-10
next_assessment: 2026-05-10
---
```

### Risk Scoring

Likelihood (1-5) x Impact (1-5) = Score (1-25)

| Score | Category |
|-------|----------|
| 1-4 | Low |
| 5-9 | Medium |
| 10-16 | High |
| 17-25 | Critical |

### Risk Register

| Risk ID | Threat ID | Description | L | I | Score | Treatment | Control IDs | Owner |
|---------|-----------|-------------|---|---|-------|-----------|-------------|-------|
| RISK-001 | threat-disclosure-data-leak | User data exposure | 2 | 5 | 10 | mitigate | auth-rls-user-profiles | platform |

Treatment: `mitigate` | `accept` | `transfer` | `avoid`

## Compliance Scorecard

```markdown
## Summary
Overall compliance: 80% (8/10 frameworks fully mapped)

## Per-Framework Scores

| Framework | Coverage | Maturity | Trend |
|-----------|----------|----------|-------|
| OWASP Web 2021 | 80% | Managed | ↑ |
| NIS2 Article 21 | 60% | Defined | → |

## Maturity Assessment
Initial → Defined → Managed → Measured → Optimized

## Trend
Quarterly comparison.

## Action Items
Top-priority remediation items.
```

## Core Principles

- **Compliance is mapped, not duplicated** — map to AFSS controls, don't re-document them
- **Framework requirements are canonical** — use official IDs and text, don't paraphrase
- **Coverage is quantifiable** — every requirement has full/partial/none/not-applicable
- **Risk is scored** — numeric scoring enables prioritization and trending
- **AI agents can assess posture** — read mappings, identify gaps, estimate impact

## Cross-References

- All `control_id` references MUST match AFSS `controls.yaml`
- All `policy_id` references MUST match AFSS `policies.yaml`
- Risk assessment `Threat ID` references MUST match AFSS threat model
- Operational requirements may reference AFOPS `procedure_id`
- Compliance gaps SHOULD have corresponding AFRS security roadmap items

## Full Standard

https://github.com/securitymonster/afdocs/blob/main/AFCS.md
