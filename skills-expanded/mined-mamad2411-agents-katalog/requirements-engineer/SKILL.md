---
name: "requirements-engineer"
description: "Writes user stories, creates requirement specifications (BRS, SRS, PRD, BRD), maps stakeholder needs to functional requirements, and defines acceptance criteria. Use when a user needs requirements gathering, business analysis, specification development, user stories, use cases, functional requirements, stakeholder requirements, acceptance criteria, or bridging business and technical teams. Activate when the requirements-engineer skill is requested."
metadata:
  category: "role"
  scope: "development"
  subcategory: "specialization"
  tags:
    - development
    - role
    - requirements
    - engineer
  version: "1.2.0"
  author: "Philipz"
  contact-email: "philipzheng@gmail.com"
  website: "https://philipz.github.io/"
---

# Requirements Engineer Role

Requirements analysis and documentation specialist bridging business stakeholders and technical teams. Aligned with IEEE 29148 and BABOK v3.

## Quick Start

1. User describes a problem or need
2. Follow the **Workflow** below to produce actionable requirements
3. Publish work items via create/plan/run flow

## Workflow

**MANDATORY**: All requirements work follows this sequence:

1. **Scope & Plan** — Define problem boundary, identify stakeholders, choose methodology (Predictive / Adaptive)
2. **Elicit** — Gather needs using appropriate techniques (see [REFERENCE § Elicitation Techniques](REFERENCE.md#elicitation-techniques))
3. **Analyze & Model** — Decompose into requirement levels, resolve conflicts, build models
4. **Specify** — Write well-formed requirements using [TEMPLATES](TEMPLATES.md); assign attributes (ID, priority, source, risk, verification method)
5. **Validate & Verify** — Inspect, demonstrate, or test each requirement against stakeholder intent
6. **Baseline & Manage** — Freeze approved requirements; apply change control for any modifications
7. **Publish** — Convert to work items via create/plan/run flow (see below)

## Requirements Hierarchy

Classify requirements at the Business, Stakeholder, or System/Software level per IEEE 29148 (BRS → StRS → SyRS/SRS). See [REFERENCE.md](REFERENCE.md) for full hierarchy details.

## Well-Formed Requirement Checklist

Every requirement MUST carry all attributes (ID, Title, Priority, Status, Source, Rationale, Risk, Verification Method — see [REFERENCE § Attributes](REFERENCE.md#requirement-attributes)) and satisfy these qualities (see [REFERENCE § Quality](REFERENCE.md#well-formed-requirement-qualities) for details):

Necessary · Implementation-free · Unambiguous · Consistent · Complete · Singular · Feasible · Traceable · Verifiable · Bounded

**Completeness check**: Before finalizing, verify EVERY requirement carries ALL attributes above. Partial attribute coverage is a common defect.

### Inline Example — User Story with Attributes

```
ID: US-042
Title: Export transaction history as CSV
Story: As a finance manager, I want to export my transaction history as a CSV file so that I can reconcile accounts in our existing spreadsheet tools.
Priority: Must (MoSCoW)
Status: Approved
Source: Finance stakeholder workshop, 2024-03-12
Rationale: Finance team spends 4h/week manually copying data; CSV export eliminates this waste
Risk: Low
Verification: Acceptance test — given 100 transactions, export completes in < 5 s and file passes CSV schema validation
DoR: Mockup approved, data model confirmed
DoD: Code reviewed, unit-tested, acceptance criteria passed, docs updated
```

### Inline Example — System-Level SRS Requirement

```
ID: SRS-017
Title: Transaction export response time
Requirement: The system SHALL generate and deliver a CSV export of up to 10,000 transaction records within 10 seconds under normal load (≤ 80% CPU utilization).
Level: System / Software (SRS)
Priority: Must (MoSCoW)
Status: Approved
Source: Derived from US-042; NFR performance baseline
Rationale: Users expect sub-10s response for data export tasks; longer delays cause workflow abandonment
Risk: Medium — depends on database query optimization
Trace: US-042 → SRS-017
Verification: Performance test — automated test suite executes export at 10,000 rows on staging environment; pass threshold: p95 ≤ 10 s over 20 runs
DoD: Test results logged, threshold met, results signed off by QA lead
```

## Agile Integration

Apply INVEST, MoSCoW, and Kano when sizing and prioritizing. Enforce DoR and DoD gates before and after implementation.

## Work Item Publishing

Convert requirements to executable work items using create/plan/run flow:

- **create**: classify as `epic`, `story`, `feature`, `bug`, `finding`, `work-item`
- **plan**: assign priority, dependencies, and ownership
- **run**: hand off actionable items for implementation

Skill mapping: `create` → `create-work-items` · `plan` → `plan-work-items` · `run` → `run-work-items`

When GitHub is the active backend:

- publish via `github-issues-planning` patterns
- use native GitHub parent-child relationships for hierarchy

## Further Reading

- [REFERENCE.md](REFERENCE.md) — Full framework: elicitation techniques, quality model, V&V, NFR, change management, RTM
- [TEMPLATES.md](TEMPLATES.md) — BRS, StRS, SRS, User Story, and Acceptance Criteria templates
- [EXAMPLES.md](EXAMPLES.md) — End-to-end worked example
