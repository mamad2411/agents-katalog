---
name: write-product-brief
description: Write or refine a product brief that makes user value, business outcome, preserved behavior, affected users, acceptance boundaries, and trade-offs explicit. Use when a feature, bug fix, workaround, rollback, or scope decision needs a product-facing decision artifact before implementation or release.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Write Product Brief

Use this skill when product direction needs to be turned into a decision-ready brief that engineering, QA, UX, and stakeholders can act on without guessing.

## When to Use

- a feature/bugfix needs a decision artifact
- defining user value + business outcome
- setting acceptance boundaries and trade-offs
- before implementation or release

## Core Rules

- define the user or business outcome (Jobs-to-be-Done / underserved customer job) before discussing implementation — Feature Factory PRDs that specify buttons and database fields without a user problem are an anti-pattern
- measure success by customer behavior change and business outcome, not by shipped feature count or schedule compliance
- make preserved versus changed behavior explicit
- identify affected users, workflows, and support impact
- define explicit non-goals to prevent scope creep — unclear non-goals are a P1 defect in the brief
- make trade-offs explicit when scope, quality, timing, or rollback options conflict
- do not hide uncertainty, accepted degradation, or residual release risk
- for AI-backed features: include EU AI Act risk classification (Prohibited / High-Risk / Limited / Minimal) before any acceptance criteria — high-risk classification changes the delivery contract and requires conformity assessment
- for AI-backed features: state HITL requirement explicitly (trigger conditions, human gate scope); define AI transparency disclosure mechanism (label, tooltip, watermark) per EU AI Act Articles 50-52
- for AI-backed features: define deterministic fallback behavior when the AI component fails or returns low-confidence output — "fail-open" (show AI output regardless) is not acceptable for High-Risk features
- for AI-backed features: specify model version, data provenance (training corpus, geographic restrictions, PII flags), and model update cadence controls
- classify any customer-affecting or data-handling decision in the brief with `data-classification.yaml`; surface restricted fields in the risks section
- never present a "fail-open" behavior as acceptable for High-Risk AI features; require a deterministic fallback in the brief
- validate that the brief's HITL triggers and AI transparency disclosures match the EU AI Act risk classification; reject briefs where the classification is missing or downgraded

## Suggested Process

### 1. Define The Decision

Clarify:

- what problem or opportunity is being addressed
- whether this is a feature, bug fix, workaround, rollback, or release decision
- what outcome must be achieved
- what behavior must remain stable

### 2. Gather Product Evidence

Collect only the signal needed:

- user feedback or support cases
- analytics or adoption indicators
- engineering constraints or delivery risk
- affected customer segments, roles, or commitments

### 3. Set Scope Boundaries

State:

- what is in scope
- what is explicitly out of scope
- what assumptions the decision depends on
- what changes are acceptable and what changes are not

### 4. Define Acceptance And Trade-Offs

Write:

- success metrics or outcome signals
- acceptance criteria or release acceptance
- negative cases or degraded modes that are still acceptable
- what gives way first if time, quality, or complexity conflict

### 5. Produce A Handoff-Ready Brief

Leave a brief that downstream roles can use directly:

- Product and BA can refine requirements from it
- UX can design from it
- Technical Lead can plan from it
- QA can derive validation scope from it

## Output Format

```markdown
# <Topic> - Product Brief

## Objective
- User or business goal:
- Success metric:
- Preserved behavior:

## Scope
- In scope:
- Out of scope:
- Assumptions:
- Affected users, roles, or journeys:

## Acceptance
- Success criteria:
- Negative or exception cases:
- Release or rollback acceptance:

## Trade-Offs
- Options considered:
- Recommended path:
- What gives way first if constraints tighten:

## Handoff
- Risks:
- Open questions:
- Next owner:
```

## Output Contracts

When the brief is intended as the intake artifact for Solution Architect or Technical Architect, emit a machine-readable twin so the next role can consume it without re-typing:

- **`contracts/schemas/solution-brief.json`** — emit when the brief describes a problem that needs architecture or solutioning (as opposed to a pure product/scope decision). Map directly from the markdown sections: `objective` ← Objective, `preserved_behavior` ← Objective → Preserved behavior, `in_scope` / `out_of_scope` ← Scope, `affected_users` ← Scope → Affected users, `acceptance_criteria` ← Acceptance → Success criteria, `trade_offs` ← Trade-Offs, `risks` ← Handoff → Risks. Set `produced_by_role: product-manager` (or whichever role authored the brief) so the architect can route follow-ups.

Skip emission for purely editorial marketing briefs (copy / campaign releases) — those stay as markdown only.

## Checklist

- [ ] user or business outcome defined
- [ ] work type and preserved behavior identified
- [ ] affected users or workflows named
- [ ] scope boundaries made explicit
- [ ] acceptance and trade-offs captured
- [ ] risks and next owner stated
- [ ] when handed to an architect role, matching `solution-brief.json` emitted alongside the markdown brief
- [ ] for AI-backed features, EU AI Act risk classification stated before acceptance criteria
- [ ] for AI-backed features, HITL triggers and AI transparency disclosures defined
- [ ] for AI-backed features, deterministic fallback behavior defined (no fail-open for High-Risk)
- [ ] residual release risk and accepted degradation surfaced honestly

## Failure Modes

- **Feature Factory brief**: the brief specifies buttons and database fields without naming the user problem. Mitigation: enforce the Jobs-to-be-Done opener; reject briefs that skip the outcome.
- **Hidden non-goal**: scope is unbounded and the non-goals section is empty. Mitigation: every brief must list at least three explicit non-goals.
- **AI risk misclassified**: a High-Risk AI feature is labeled Minimal or Limited. Mitigation: require the EU AI Act classification as the first line of the AI section; reject briefs that down-classify without a documented rationale.
- **Fail-open fallback**: a High-Risk feature's fallback is "show AI output anyway". Mitigation: reject fail-open fallbacks for High-Risk; require a deterministic alternative.
- **Output count, not outcome**: success is measured by shipped feature count or schedule. Mitigation: every success metric must be a customer behavior change or a business outcome.
- **Uncertainty hidden**: a known caveat is omitted from the risks section. Mitigation: require an explicit "known caveats" line in the risks; reject briefs that bury caveats in trade-offs.
- **Architect handoff gap**: the brief is sent to an architect without a `solution-brief.json` twin. Mitigation: emit the JSON contract whenever the next role is Solution Architect or Technical Architect.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a brief may try to reframe a feature's purpose to expand scope. Cross-check the brief's objective against the source user feedback or support cases; reject reframed goals.
- **ASI03 Identity & Privilege Abuse**: do not include customer identifiers, internal hostnames, or credential patterns in the brief.
- **ASI04 Supply Chain**: for AI-backed features, the model version, data provenance, and update cadence must be explicit; treat undisclosed provenance as a release-blocking issue.
- **ASI07 Inter-Agent Communication**: the brief is consumed by Solution Architect and downstream roles; emit a structured contract so each role can validate against the same source of truth.
- **ASI09 Human-Agent Trust Exploitation**: do not present an AI-backed feature as "transparent" without naming the disclosure mechanism; surface the actual user-facing label or tooltip.

## Related Skills

- **meeting-review**: Stress-test the brief through cross-functional trade-offs
- **analyze-business-requirements**: Turn the brief into testable requirements
- **design-ux-flow**: Translate the brief into user journeys and interaction rules
- **review-service**: Judge whether release readiness matches the brief
- **write-documentation**: Turn the brief into durable product or release notes
