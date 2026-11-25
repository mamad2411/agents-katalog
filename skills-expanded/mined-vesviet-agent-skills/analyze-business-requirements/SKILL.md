---
name: analyze-business-requirements
description: Analyze and write business requirements by making actors, business rules, state transitions, exceptions, preserved behavior, and downstream process impact explicit. Use when a feature, policy change, or bug fix needs implementation-ready requirements and testable acceptance criteria.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Analyze Business Requirements

Use this skill when business needs, bug behavior, or process expectations must be turned into clear, testable, implementation-ready requirements.

## When to Use

- a feature, workflow, or policy change needs structured requirements
- making actors, business rules, and state transitions explicit
- defining testable behavioral acceptance criteria (BDD / Gherkin)
- capturing preserved behavior versus changed behavior
- specifying probabilistic acceptance criteria and HITL escalation triggers for AI/LLM features
- defining autonomy boundaries, MCP tool permissions, and kill-switches for agentic systems
- preparing structured machine handoffs via `contracts/schemas/feature-ticket.json`

## Core Rules

- **Observable Behavior Over Implementation**: write requirements as observable system behavior and business outcomes; ban internal implementation guesses and GUI micro-actions
- **The Layered Requirements Pipeline**: structure requirements refinement through 4 progressive stages:
  1. *Impact Mapping* (Why/Who): map strategic goals to actors and measurable KPI metrics
  2. *Event Storming* (What/Flow): model timeline-ordered Domain Events (past tense), Commands (imperative), and Aggregates
  3. *Story Mapping* (How/Slices): slice releases vertically into Walking Skeletons spanning all architectural tiers
  4. *Executable BDD*: specify Given/When/Then scenarios with stateful invariants and failure guarantees
- **Enforce BDD Syntactic Precision**:
  - *Single-Action Invariant*: the `When` step contains exactly ONE discrete action verb; chained actions are prohibited
  - *Stateful Conservation Invariants*: postconditions (`Then`) assert system invariants (e.g. $\sum \text{Debits} \equiv \sum \text{Credits}$)
  - *Explicit Failure Guarantees*: negative scenarios define system state when an exception occurs
- **Boundary Value Analysis (BVA)**: partition input domains into valid/invalid equivalence classes; embed combinatorial pairwise decision tables
- **AI Probabilistic Acceptance Criteria**: replace binary pass/fail with statistical confidence thresholds over sample windows ($N$ samples); define evaluation harnesses (LLM-as-Judge, golden benchmarks) and production degradation alerts
- **HITL Escalation Matrix**: mandate trigger conditions, operational SLAs, responsible roles, and immutable audit logs for high-stakes AI decisions
- **Agentic MCP Governance**: declare autonomy level (L1–L5, L3 ceiling), attenuated per-invocation tool permissions, forbidden zones, and emergency kill-switches
- **Canonical Machine Handoff**: emit `contracts/schemas/feature-ticket.json` (Draft 2020-12) containing all domain blocks
- Detailed patterns, math, and templates: [`references/layered-requirements-pipeline-and-bdd-standards.md`](references/layered-requirements-pipeline-and-bdd-standards.md)

## Suggested Process

### 1. Frame Business Problem & Actors
Identify the business opportunity, customer pain, target actors, and intended measurable outcome. Clarify preserved behavior versus changed behavior.

### 2. Map Domain Events & Aggregates (Event Storming)
Model the business timeline using past-tense Domain Events (`OrderPlaced`, `PaymentSettled`), imperative Commands, and Aggregate invariant boundaries.

### 3. Decompose into Vertical Slices (Walking Skeleton)
Apply Elephant Carpentry patterns to carve out the thinnest viable end-to-end slice spanning UI, API, and persistence. Audit against INVEST criteria.

### 4. Author Behavioral Acceptance Criteria (BDD / Gherkin)
Write Given/When/Then scenarios enforcing the Single-Action Invariant, stateful conservation checks, and explicit failure guarantees. Embed BVA decision matrices.

### 5. Formulate AI & Agentic Governance Envelopes
If AI/LLM is in scope, specify probabilistic AC, evaluation judge, degradation triggers, and HITL escalation protocols. For agentic systems, catalog MCP tool permissions and kill-switches.

### 6. Delegate Dependencies Before Lock
- Unknown domain/policy: issue `research_request` $\to$ consume `research-report.json`
- Numeric baselines: issue `analytics_request` $\to$ consume `data-analysis-report.json`
- Search/content goals: issue `seo_content_request` $\to$ consume `seo-content-brief.json`

### 7. Package Machine Handoff
Serialize requirements into `contracts/schemas/feature-ticket.json` adhering to Draft 2020-12.

## Output Format

```markdown
# <Feature Title> - Business Analysis Brief

## Business Context & Outcome
- Problem: - Actors: - Outcome: - Preserved behavior: - Changed behavior:

## Domain Context (Event Storming)
- Bounded Context: - Aggregate Root: - Domain Events: - Commands:

## Vertical Slice Decomposition
- Slice Pattern: [workflow_step | rule_variation | data_channel | crud]
- Walking Skeleton: [Yes | No] - INVEST Audit: [Verified]

## Business Rules & Invariants
- [BR-01]: [Declarative business rule and mathematical invariant]

## Behavioral Acceptance Criteria (BDD)
```gherkin
@core @smoke
Scenario: [Happy path scenario]
  Given [Precondition state]
  When [Single discrete action]
  Then [Expected observable outcome]
  And [Stateful conservation invariant]
```

## AI & Agentic Specs (when in scope)
- Behavioral Boundary: - Probabilistic AC: - HITL Trigger: - Autonomy Level: - Kill-Switch:

## Non-Functional Requirements & Governance
- Performance SLA: - GDPR Legal Basis: - Deletion Propagation SLA:
```

## Checklist

- [ ] problem, actors, and observable business outcome defined
- [ ] preserved behavior versus changed behavior explicitly stated
- [ ] Event Storming timeline modeled with past-tense Domain Events and Aggregates
- [ ] feature decomposed into thin vertical slices (Walking Skeleton verified)
- [ ] BDD scenarios enforce Single-Action Invariant and stateful system invariants
- [ ] boundary value analysis (BVA) and combinatorial decision tables included
- [ ] AI features specify probabilistic AC, evaluation judge, and degradation alert
- [ ] high-stakes AI decisions have complete HITL escalation matrices (SLA, role, audit log)
- [ ] agentic features declare autonomy level (L1–L5), MCP permissions, and kill-switch
- [ ] personal data processing specifies GDPR Article 6 legal basis and erasure cascade
- [ ] living assumption register scored ($\text{Impact} \times (6 - \text{Confidence})$)
- [ ] handoff contract emitted conforming to `contracts/schemas/feature-ticket.json`

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: cross-check refined requirements against original stakeholder intent.
- **ASI02 Tool Misuse & Exploitation**: restrict agentic features to least-privilege MCP tool allowlists and mandatory kill-switches.
- **ASI07 Inter-Agent Communication**: hand off requirements strictly via validated `feature-ticket.json` schemas.
- **ASI09 Human Oversight**: enforce mandatory human sign-off on AI-assisted requirements before sprint lock.

## Output Contracts

- `contracts/schemas/feature-ticket.json`

## Failure Modes

- **Chained When steps**: a Gherkin `When` contains two actions ("submits and confirms"), hiding a real state transition and making the scenario untestable. Mitigation: enforce the Single-Action Invariant; split chained actions into separate scenarios with intermediate `Given` states.
- **Preserved behavior omitted**: the brief specifies the change but never states what must keep working, so regressions ship unnoticed. Mitigation: record preserved-vs-changed behavior explicitly and derive regression acceptance criteria from the preserved set.
- **Implementation leak**: acceptance criteria name tables, classes, or GUI micro-actions instead of observable outcomes. Mitigation: rewrite each criterion as observable system behavior; ban internal implementation guesses per the Core Rules.
- **Probabilistic AC without harness**: an AI feature gets "≥95% accuracy" with no sample size, judge, or degradation alert, making it unenforceable at test time. Mitigation: every probabilistic AC must define the N-sample window, the evaluation judge (LLM-as-Judge or golden benchmark), and a production degradation trigger.
- **Toothless HITL escalation**: the escalation matrix names a role but no trigger or SLA, so high-stakes AI failures never escalate. Mitigation: require trigger condition, operational SLA, responsible role, and immutable audit log for every HITL entry.
- **Autonomy over ceiling**: an agentic feature ships with L4/L5 autonomy or broad MCP tool permissions and no kill-switch. Mitigation: cap autonomy at the L3 ceiling, attenuate per-invocation tool permissions, and declare forbidden zones plus an emergency kill-switch.
- **Exception state unspecified**: negative scenarios stop at "an error is shown" without asserting system state, so failed transactions leave locks held or ledgers unbalanced. Mitigation: every negative scenario defines explicit failure guarantees and stateful conservation invariants.
- **Invalid machine handoff**: the `feature-ticket.json` emitted at lock time fails Draft 2020-12 validation, breaking downstream Technical Architect and Technical Lead consumption. Mitigation: validate the serialized ticket against the schema before lock; fix the domain blocks, never the schema.

## Related Skills

- **elicit-requirements**: structured stakeholder interviewing and BABOK v3 quality audits
- **write-use-cases**: detailed 13-field Use Case specifications and Cockburn scoping
- **trace-requirements-impact**: RTM maintenance and BFS change request blast radius analysis
- **build-story-map**: 2D story mapping, walking skeletons, and CPM dependency scheduling
- **ai-risk-assessment**: NIST AI RMF governance and EU AI Act risk tiering
- **plan-technical-delivery**: technical milestone breakdown from feature tickets

Last updated: 2026-10-05