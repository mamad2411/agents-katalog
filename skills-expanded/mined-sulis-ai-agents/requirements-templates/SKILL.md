---
name: requirements-templates
description: "Templates used by the requirements analyst, not run directly."
user-invocable: false
---

# SRD Artifact Templates

These templates define the structure for all artifacts produced during requirements
facilitation. Use them as the skeleton when generating artifacts in Phase 4 (Artifact
Generation). Replace `{placeholders}` with content from the facilitation session.

---

## SRD Template

# Software Requirements Document: {Project Name}

**Version:** {version}
**Date:** {date}
**Status:** Draft | Review | Approved
**Author:** {author} (facilitated by Requirements Analyst)

---

### 1. Introduction

#### 1.1 Purpose
{Why this document exists. What system, feature, or integration it specifies.}

#### 1.2 Scope
{What is in scope and what is explicitly out of scope.}

#### 1.3 Intended Audience
{Who will read this document and what they need from it.}

#### 1.4 Definitions and Acronyms
See [GLOSSARY.md](GLOSSARY.md) for the full domain glossary.

#### 1.5 References
{Related documents, existing specifications, external standards.}

---

### 2. Overall Description

#### 2.1 Product Perspective
{How this system fits into the larger context. Existing systems, integrations, users.}

#### 2.2 Product Functions (Summary)
{High-level summary of major functions. Detail is in Section 4.}

| Function | Description |
|----------|-------------|
| {F-01} | {Brief description} |

#### 2.3 User Classes and Characteristics

| Actor | Description | Frequency of Use | Technical Proficiency |
|-------|-------------|-------------------|----------------------|
| {Actor 1} | {Description} | {Daily/Weekly/etc.} | {High/Medium/Low} |

#### 2.4 Operating Environment
{Platforms, browsers, devices, infrastructure constraints.}

#### 2.5 Design and Implementation Constraints
{Technology constraints, regulatory requirements, standards compliance.}

#### 2.6 Assumptions and Dependencies
{What must be true for these requirements to be valid.}

---

### 3. External Interface Requirements

#### 3.1 User Interfaces
{UI requirements, accessibility requirements, responsive design constraints.}

#### 3.2 Hardware Interfaces
{If applicable.}

#### 3.3 Software Interfaces
{APIs consumed, databases, external services. Detail in diagrams/sequence-diagrams.md.}

#### 3.4 Communications Interfaces
{Protocols, data formats, sync/async patterns.}

---

### 4. System Features

#### 4.1 {Feature Name} [F-01]

**Priority:** {High | Medium | Low}

##### 4.1.1 Description
{What this feature does and why it exists.}

##### 4.1.2 Use Cases
See [diagrams/use-cases.md](diagrams/use-cases.md) — {UC-01, UC-02}.

##### 4.1.3 Functional Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-{01} | {Requirement} | {H/M/L} | {Measurable criterion} |

---

### 5. Non-Functional Requirements

See [NFR.md](NFR.md) for full non-functional requirements specification.

| Category | Summary |
|----------|---------|
| Performance | {Key performance targets} |
| Scalability | {Scaling requirements} |
| Security | {Security requirements} |
| Availability | {Uptime targets} |
| Data | {Data requirements} |

---

### 6. Diagrams

All diagrams use Mermaid notation for portability and version control.

| Diagram Type | File | Purpose |
|-------------|------|---------|
| Use Case | [diagrams/use-cases.md](diagrams/use-cases.md) | Actor-goal relationships |
| Process Flow | [diagrams/process-flows.md](diagrams/process-flows.md) | Activity/workflow diagrams |
| Sequence | [diagrams/sequence-diagrams.md](diagrams/sequence-diagrams.md) | Integration and interaction sequences |
| State | [diagrams/state-diagrams.md](diagrams/state-diagrams.md) | Entity lifecycle state machines |
| Data Flow | [diagrams/data-flows.md](diagrams/data-flows.md) | Data movement between components |

---

### 7. Traceability Matrix

| Goal | Use Cases | Diagrams | NFRs | Features |
|------|-----------|----------|------|----------|
| {G-01} | {UC-01, UC-02} | {use-cases, sequence} | {NFR-01} | {F-01} |

---

### 8. Appendices

#### 8.1 Exploration Journal
See [EXPLORATION_JOURNAL.md](EXPLORATION_JOURNAL.md) for the facilitation record.

#### 8.2 Completeness Report
See [COMPLETENESS_REPORT.md](COMPLETENESS_REPORT.md) for the verification assessment.

#### 8.3 Handover Brief
See [HANDOVER.md](HANDOVER.md) for the execution agent handover.

---

## Comprehensive DESIGN.md Target-Structure Template

This is the **always-comprehensive** design-document template (FR-01/FR-11,
ADR-002). The design artifact carries this full Target Structure for **every**
behavioural change, regardless of depth — depth sizes only the interview, never
which sections exist (FR-02). Section names and ordering follow the canonical
`features/entity-crud/DESIGN.md` (C-01); the `## Verification Plan` heading is
fixed verbatim (C-02 / ADR-001) so the P-VER section-presence check anchors on
it.

**The invariants this template encodes:**

- Every mandatory section is present. A section a change cannot populate carries
  an explicit `n/a — <justification>`, **never** a bare omission (SC-03,
  NFR-R01 — "degrade detail, not existence").
- The Non-Functional Requirements section is **always on** and states a
  **measurable** target per category — Performance, Security, Reliability — not
  an adjective like "fast" (SC-05, FR-06).
- The §7 Solution Design carries an **always-on STRIDE threat model** (FR-15),
  an **architecture-at-levels (C4)** sub-section with three distinct levels —
  context, container, component (FR-16) — and an **Interface Contract** section
  filled to the full CF-10 founder-reviewable dimensions (Schema +
  three-category errors per CF-03 + Auth/permissions + Audience + User guide +
  Error fixes). A contract operation missing any CF-10 dimension is incomplete
  (the design stage does not complete, MUC-07). The contract is present even
  when a change exposes no tool surface (marked `n/a — <reason>`), so a
  tool-walk always has a target and contract-first ordering holds (ADR-007).

The deterministic emitter that produces this structure from a depth-sized
intake is `plugins/sulis/scripts/_drive_specify.py` (the methodology adapter the
SC-01/02/03/05 scenarios drive); the WP-003 inspectors
(`_assert_doc_sections`, `_assert_same_section_set`, `_assert_section_na`,
`_assert_measurable_nfr`) verify the produced document against these invariants.

```markdown
# Design — {change slug}

## 1. Executive Summary

{1–3 paragraphs: what changes, why now, the load-bearing decisions. Depth
sizes how much detail; the section is always present.}

## 2. Problem Discovery

{Problem statement, current behaviour, desired behaviour, why-now, impact of
not doing. `n/a — <reason>` only for a pure-mechanical change with no problem
to discover.}

## 3. Stakeholders / Personas

{The actors and their interests. `n/a — <reason>` if the change has no distinct
stakeholders beyond the implementing agent.}

## 4. Requirements

### Functional Requirements

{The functional requirements — recap by phase or table. `n/a — <reason>` if none.}

### Non-Functional Requirements

Always-on, measurable targets per category (FR-06). Structure is invariant
across depth; detail is interview-sized. **Each category MUST state a number /
threshold, not an adjective.**

#### Performance

{A measurable target — e.g. `< 5 ms`, `≤ 1.6×`, `1000 calls < 5 s`.}

#### Security

{A measurable target — e.g. `100%` of inputs validated, `0` unauthenticated
paths.}

#### Reliability

{A measurable target — e.g. `≥ 99.9%` availability, `0` silent section drops.}

### Threat Model

{**Always-on STRIDE threat model (FR-15).** Name all six STRIDE categories in a
matrix — a category that does not apply to this change carries an explicit
`n/a — <reason>` rather than being dropped (NFR-R01). Add trust boundaries and
the attack surface where the change has them.

| Category | Threat | Applicable? | Mitigation |
|----------|--------|-------------|------------|
| **S**poofing | {threat or `n/a — <reason>`} | {Yes/No} | {mitigation} |
| **T**ampering | {…} | {…} | {…} |
| **R**epudiation | {…} | {…} | {…} |
| **I**nformation disclosure | {…} | {…} | {…} |
| **D**enial of service | {…} | {…} | {…} |
| **E**levation of privilege | {…} | {…} | {…} |
}

### Constraints

{Hard constraints — standards to match, headings fixed verbatim, purity
requirements. `n/a — <reason>` if none.}

### Assumptions

{What must be true for the design to hold. `n/a — <reason>` if none.}

### Dependencies

{Internal / external dependencies and their classification. `n/a — <reason>`
when the change declares no dependencies (SC-03).}

## 5. Scope

{In scope / out of scope / MVP-vs-future.}

## 6. Use Cases

{Use cases with main / alternate / exception flows. `n/a — <reason>` if the
change has no user-facing or machine-facing use case.}

## 7. Solution Design

### Solution Overview

{The composition narrative — what is built / reused / extended, and the
load-bearing decisions.}

### Architecture-at-Levels (C4)

{**Always-on, three distinct C4 levels (FR-16).** Each level is its own
sub-heading — a two-level section (e.g. context + container, no component) is
incomplete. A thin change still states each level (a one-line `n/a — <reason>`
where it has nothing to add), never drops one.}

#### Level 1 — System Context

{The change in its environment: the actors and the systems it talks to. A
mermaid `graph` is ideal; prose is acceptable.}

#### Level 2 — Container

{The deployable / maintainable units the change spans.}

#### Level 3 — Component

{The load-bearing internals of the newest / most-changed container.}

### Interface Contract

{**MANDATORY for a tool surface; filled to the full CF-10 dimensions (FR-18).**
When the change exposes no tool surface: `n/a — <reason>`, with the skeleton
standing ready. Per FR-19 the tool-walk's operations must be a subset of this
contract. Render one block per operation carrying the schema, the CF-03
three-category errors, AND the four CF-10 founder-reviewable dimensions — a
missing dimension makes the contract incomplete (the design stage does not
complete, MUC-07):

#### Operation: `<name>`

| Dimension | Value |
|-----------|-------|
| **Schema** | in: `<input types>`; out: `<output types>` |
| **Errors** | Protocol: `<transport failure>`. Expected: `<deterministic failure>`. Internal: `<unexpected crash>`. (CF-03) |
| **Auth / permissions** | {does it require sign-in / a permission?} |
| **Audience** | {operator / agent vs founder / end-user} |
| **User guide** | {one plain-language sentence: what it does + when to use it} |
| **Error fixes** | {per error: the cause + the user-fix and/or developer-fix} |
}

## 8. ADRs + BDRs

{Technical decisions (ADR) and business decisions (BDR), recorded with distinct
shapes (FR-17). `n/a — <reason>` if none recorded.

An **ADR** records a *technical* decision — Context / Decision / Options
considered / Consequences — answering "how do we build it?".

A **BDR** records a *business* decision — a scope cut, a sequencing call, a
cost/benefit trade — answering "what do we choose to do, and why is that worth
it?". Same skeleton (Context / Decision / Options / Consequences) but the
options and consequences are framed in business terms (cost, risk, founder
value), and it carries `kind: bdr` so it is distinguishable from a technical
ADR.

| ID | Title | Kind |
|----|-------|------|
| ADR-001 | {technical decision} | technical |
| BDR-001 | {business decision} | business |
}

## 9. Migration / Rollback / Security / Performance

{How the change is migrated, rolled back, and the security + performance posture
recap (targets stated in §4 Non-Functional Requirements).}

## Verification Plan

{The verbatim `## Verification Plan` heading (C-02 / ADR-001). Populated per the
Verification Plan section template below.}
```

**No reordering, no omissions.** Inapplicable sections carry `n/a —
<justification>`; the structure is invariant (ADR-002). The numbered §1..§10
spine matches the canonical; the always-on NFR / Threat Model / Constraints /
Assumptions / Dependencies sub-sections and the Interface Contract skeleton are
named sub-headings beneath the spine that the document inspectors anchor on.

---

## Verification Plan section template

This block is the skeleton for the SRD's `## Verification Plan` section
— the design-time commitment to how the work will be verified, captured
when the spec is written rather than bolted on at the end. The
requirements-analyst populates each subsection from the canonical
20-question set; the P-VER rubric phase (in
[`decompose-validation-rubric.md`](../../references/decompose-validation-rubric.md)
§Phase 9) reads this section's shape to verdict it.

**Canonical source.** The questions referenced below (Q1..Q20) live in
[`plugins/sulis/references/standards/VERIFICATION_QUESTIONS.md`](../../references/standards/VERIFICATION_QUESTIONS.md)
v1.0.0. **Do not inline the question text into the SRD.** The agent
reads the canonical at runtime; the SRD's Verification Plan section
contains the *answers* and references the questions by ID. ADR-001
fixes the section heading literal (`## Verification Plan`, exact
casing — the P-VER section-presence regex anchors on it). ADR-007
fixes the seven-row kind→adapter table that the fifth subsection
below (the per-kind adapter row) draws from. The placeholder
instructions below tell the agent which canonical question maps to
each subsection.

```markdown
## Verification Plan

<!-- VERIFICATION_QUESTIONS source: plugins/sulis/references/standards/VERIFICATION_QUESTIONS.md v1.0.0 -->

### What user-observable behaviour are we verifying?

{agent populates with answer to Q1, ≥ 30 substantive characters — the
concrete observable, plain English: a new screen, a faster response,
an email that arrives. P-VER's MUC-001 placeholder-scan rejects
shorter / `TBD` / "to be defined" content.}

### Verification environment(s)

{agent populates with answer to Q2 — one or more of: local,
staging, ephemeral, production-shadow, production-canary. Each named
environment carries one line of why it's appropriate.}

### Bootstrap-from-zero case

{agent populates with answer to Q3 — what verification looks like
when no data, no users, no upstream artifacts exist yet. The anchor
failure mode for the release-train + discovery dogfood incidents
that motivated this section; do not skip even if "obvious".}

### Per-integration verification strategy

{agent populates with answers to Q5-Q13 per touched integration.
For each integration, the table row carries: integration name + the
classification (`existing` with resolvable path / `deferred` with
canonical identifier / `out-of-scope` with one-line justification) +
real-vs-recorded-vs-simulated verdict + the test that exercises it.
P-VER's MUC-002 defence rejects any integration without one of the
three classifications.}

| Integration | Classification | Real / Recorded / Simulated | Test |
|---|---|---|---|
| {name} | `existing` / `deferred` / `out-of-scope` | {verdict} | {path} |

### Per-kind verification adapter

**Adapter (from VERIFICATION_QUESTIONS.md row for `kind: <K>`):**
{one-liner copied from the seven-row table per ADR-007 — verbatim
from the canonical}

{agent populates with answers to Q14-Q20 — the per-kind concretion:
which specific test classes the adapter resolves to in this codebase,
which fixtures, which CI lane. The adapter row from the canonical is
the *shape*; this subsection is the *binding* to the specific project.}

### Infrastructure needs surfaced (deferred)

{agent populates with deferred entries per the canonical's deferred-
need identifier recipe. Each entry: stable identifier + one-line
description + why-deferred + the change this would become if
auto-drafted by ADR-005's slice-end trigger. Empty list is acceptable
if no deferred needs surfaced — the section heading + an explicit
`*(none)*` line is required by P-VER's section-presence check.}
```

**No invented subsections, no reordering, no omissions.** The rubric's
P-VER section-shape check (rubric §9.01) asserts the six subsections
appear in the order above. The order is anchored by the canonical's
question grouping (foundational → environment → bootstrap →
per-integration → per-kind → deferred).

---

## Use Case Template

### UC-{ID}: {Use Case Name}

**Actor:** {Primary actor}
**Goal:** {What the actor is trying to achieve}
**Priority:** {High | Medium | Low}
**Preconditions:**
- {What must be true before this use case can begin}

**Postconditions (success):**
- {What is true when the use case completes successfully}

**Postconditions (failure):**
- {What is true when the use case fails}

#### Basic Flow

| Step | Actor | System |
|------|-------|--------|
| 1 | {Actor action} | |
| 2 | | {System response} |
| 3 | {Actor action} | |
| 4 | | {System response} |

#### Alternate Flows

**{AF-01}: {Alternate flow name}**
- Branches from: Step {N}
- Condition: {When this alternate flow triggers}

| Step | Actor | System |
|------|-------|--------|
| {N}.1 | {Action} | |
| {N}.2 | | {Response} |

- Rejoins: Step {M} | Ends

#### Exception Flows

**{EF-01}: {Exception name}**
- Branches from: Step {N}
- Condition: {Error condition}

| Step | Actor | System |
|------|-------|--------|
| {N}.1 | | {Error handling} |
| {N}.2 | | {User notification} |

- Result: {Outcome — retry, abort, degrade}

#### Business Rules

| ID | Rule | Applies To |
|----|------|------------|
| BR-{01} | {Business rule description} | Step {N} |

#### Negative Requirements

What this use case MUST NOT do, MUST refuse, or MUST detect. Populated from Phase 3.6
Adversarial Sweep; cross-references the relevant misuse cases.

| ID | Negative Requirement | Source Misuse Case | Trigger |
|----|---------------------|--------------------|---------| 
| NR-{01} | {System MUST refuse / detect / log ...} | MUC-{ID} | Step {N} / Always |

#### Use Case Diagram (Mermaid)

```mermaid
graph LR
    Actor1["{Actor 1}"]
    subgraph System["{System Name}"]
        UC01("{UC-01: Use Case Name}")
    end
    Actor1 --> UC01
```

---

## Sequence Diagram Template

### {SD-ID}: {Sequence Name}

**Related Use Case:** {UC-ID}
**Participants:** {List of systems/components involved}
**Trigger:** {What initiates this sequence}

```mermaid
sequenceDiagram
    participant U as {User/Actor}
    participant A as {Component A}
    participant B as {Component B}
    participant C as {External System}

    U->>A: {Request}
    activate A
    A->>B: {Internal call}
    activate B
    B->>C: {External call}
    activate C
    C-->>B: {Response}
    deactivate C
    B-->>A: {Result}
    deactivate B
    A-->>U: {Response}
    deactivate A

    alt {Error condition}
        C-->>B: {Error response}
        B-->>A: {Error handling}
        A-->>U: {Error message}
    end
```

#### Interaction Notes

| Step | From | To | Data | Notes |
|------|------|----|------|-------|
| 1 | {From} | {To} | {Payload description} | {Protocol, auth, format} |

#### Error Handling

| Error Condition | Handler | User Impact | Recovery |
|----------------|---------|-------------|----------|
| {Condition} | {Component} | {What user sees} | {Auto-retry / manual / abort} |

#### Performance Expectations

| Interaction | Expected Latency | Timeout | Retry Policy |
|-------------|-----------------|---------|--------------|
| {Call} | {Target} | {Timeout} | {Retry count and backoff} |

---

## Process Flow Template

### {PF-ID}: {Process Name}

**Related Use Case:** {UC-ID}
**Trigger:** {What starts this process}
**End State:** {What constitutes process completion}

```mermaid
flowchart TD
    Start([Start: {Trigger}])
    Step1[{Step 1 description}]
    Decision1{"{Decision question}"}
    Step2[{Step 2a description}]
    Step3[{Step 2b description}]
    Step4[{Step 3 description}]
    End([End: {End state}])

    Start --> Step1
    Step1 --> Decision1
    Decision1 -->|Yes| Step2
    Decision1 -->|No| Step3
    Step2 --> Step4
    Step3 --> Step4
    Step4 --> End
```

#### Process Steps

| Step | Description | Actor/System | Inputs | Outputs | Business Rules |
|------|-------------|-------------|--------|---------|----------------|
| 1 | {Description} | {Who/what} | {Required inputs} | {Produced outputs} | {BR-IDs} |

#### Decision Points

| Decision | Criteria | Yes Path | No Path |
|----------|----------|----------|---------|
| {Decision} | {How the decision is made} | {Path} | {Path} |

---

## State Diagram Template

### {ST-ID}: {Entity Name} Lifecycle

**Entity:** {Entity name}
**Related Use Cases:** {UC-IDs}
**Purpose:** {Why this entity has state — what decisions depend on its current state}

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Active: activate
    Active --> Suspended: suspend
    Suspended --> Active: reactivate
    Active --> Completed: complete
    Suspended --> Cancelled: cancel
    Active --> Cancelled: cancel
    Completed --> [*]
    Cancelled --> [*]
```

#### States

| State | Description | Entry Conditions | Allowed Actions |
|-------|-------------|-----------------|-----------------|
| {Created} | {Description} | {How entity enters this state} | {What can happen in this state} |

#### Transitions

| From | To | Trigger | Guard Conditions | Side Effects |
|------|----|---------|-----------------|--------------|
| {State A} | {State B} | {What causes transition} | {Conditions that must be true} | {What else happens} |

#### Invalid Transitions

| From | To | Why Invalid |
|------|----|------------|
| {State A} | {State B} | {Why this transition is not allowed} |

---

## Data Flow Template

### {DF-ID}: {Data Flow Name}

**Scope:** {System-level | Feature-level | Integration-level}
**Related Use Cases:** {UC-IDs}

```mermaid
flowchart LR
    subgraph External
        ES1[("{External Source 1}")]
        ES2[("{External Sink 1}")]
    end

    subgraph System["{System Name}"]
        P1["{Process 1}"]
        P2["{Process 2}"]
        DS1[("{Data Store 1}")]
    end

    ES1 -->|"{data description}"| P1
    P1 -->|"{transformed data}"| DS1
    DS1 -->|"{query results}"| P2
    P2 -->|"{output data}"| ES2
```

#### Data Stores

| ID | Name | Type | Contents | Access Pattern |
|----|------|------|----------|----------------|
| DS-{01} | {Name} | {Database/Cache/File/Queue} | {What data is stored} | {Read-heavy/Write-heavy/Both} |

#### Data Flows

| ID | From | To | Data | Format | Volume | Frequency |
|----|------|----|------|--------|--------|-----------|
| {Flow-01} | {Source} | {Destination} | {Description} | {JSON/CSV/Binary/etc.} | {Expected volume} | {Real-time/Batch/On-demand} |

#### Privacy and Sensitivity

| Data Element | Classification | Handling Requirements |
|-------------|---------------|----------------------|
| {Element} | {PII/Sensitive/Public} | {Encryption/Masking/Retention} |

---

## NFR Template

### Performance

| ID | Requirement | Metric | Target | Measurement Method |
|----|-------------|--------|--------|-------------------|
| NFR-P01 | {Requirement} | {Metric name} | {Specific threshold} | {How measured} |

### Scalability

| ID | Requirement | Metric | Target | Measurement Method |
|----|-------------|--------|--------|-------------------|
| NFR-S01 | {Requirement} | {Metric name} | {Specific threshold} | {How measured} |

### Security

| ID | Requirement | Category | Implementation | Verification |
|----|-------------|----------|----------------|-------------|
| NFR-SEC01 | {Requirement} | {Auth/Encryption/Access/Audit} | {How implemented} | {How verified} |

### Availability

| ID | Requirement | Metric | Target | Measurement Method |
|----|-------------|--------|--------|-------------------|
| NFR-A01 | {Requirement} | {Metric name} | {Specific threshold} | {How measured} |

### Data

| ID | Requirement | Category | Implementation | Verification |
|----|-------------|----------|----------------|-------------|
| NFR-D01 | {Requirement} | {Retention/Backup/Recovery/Privacy} | {How implemented} | {How verified} |

**NFR Quality Criteria:** Every NFR MUST be measurable (specific threshold), testable
(pass/fail against threshold), traceable (linked to business goal), and achievable.

---

## PRIMITIVE_TREE.jsonld Template

```json
{
  "@context": {
    "@vocab": "https://sulis.co/ontology/primitive-tree/",
    "schema": "http://schema.org/",
    "prim": "https://sulis.co/ontology/primitive-tree/",
    "name": "schema:name",
    "description": "schema:description"
  },
  "@id": "prim:tree-{project-name}",
  "@type": "prim:PrimitiveTree",
  "name": "{Project Name} — Primitive Tree",
  "synthesised_at": "{ISO-8601 timestamp}",
  "synthesis_path": "{brownfield | greenfield}",
  "source_index": "{CODEBASE_INDEX.json | null}",
  "@graph": [
    {
      "@id": "{node-id}",
      "@type": "prim:{node-type}",
      "name": "{Human-readable name}",
      "definition": "{What this node represents in the target domain}",
      "success_criterion": "{Measurable condition confirming correct specification}",
      "health_status": "{untested | testing | validated | failed | accepted-as-risk}",
      "phase": "{discover | define | connect | constrain | verify}",
      "artifactAffinity": ["{use-case | process-flow | sequence-diagram | state-diagram | data-flow | business-rule | nfr}"],
      "source": "{codebase | inferred | user}",
      "parent": "{parent-node-id | null}",
      "dependencies": [
        {"target": "{target-node-id}", "type": "{depends-on | enables | conflicts-with}"}
      ]
    }
  ]
}
```

**Example nodes by type:**

```json
// domain-entity
{"@id": "node-user", "@type": "prim:domain-entity", "name": "User", "definition": "A person who has registered an account", "success_criterion": "All user attributes and relationships specified", "health_status": "untested", "phase": "define", "artifactAffinity": ["use-case", "data-flow"], "source": "codebase", "parent": "root", "attributes": ["id", "email", "role"], "relationships": ["has-many Orders"]}

// action
{"@id": "node-place-order", "@type": "prim:action", "name": "Place Order", "definition": "User submits a new order for processing", "success_criterion": "Complete flow specified including validation, payment, and confirmation", "health_status": "untested", "phase": "define", "artifactAffinity": ["use-case", "process-flow"], "source": "inferred", "parent": "root", "actor": "Customer"}

// integration
{"@id": "node-stripe", "@type": "prim:integration", "name": "Stripe Payment Gateway", "definition": "External payment processing service", "success_criterion": "Protocol, auth, error handling, and data contract specified", "health_status": "untested", "phase": "connect", "artifactAffinity": ["sequence-diagram", "data-flow"], "source": "codebase", "parent": "root", "external_system": "Stripe", "direction": "outbound"}

// data-store
{"@id": "node-postgres", "@type": "prim:data-store", "name": "Primary Database", "definition": "PostgreSQL database storing all domain entities", "success_criterion": "Retention, backup, and access patterns specified", "health_status": "untested", "phase": "connect", "artifactAffinity": ["data-flow"], "source": "codebase", "parent": "root", "store_type": "relational", "entities": ["User", "Order"]}

// state-machine
{"@id": "node-order-lifecycle", "@type": "prim:state-machine", "name": "Order Lifecycle", "definition": "States an order passes through from creation to completion", "success_criterion": "All states, transitions, triggers, and guards specified", "health_status": "untested", "phase": "define", "artifactAffinity": ["state-diagram"], "source": "inferred", "parent": "root", "entity": "Order", "states": ["draft", "submitted", "processing", "completed", "cancelled"]}

// policy
{"@id": "node-auth-policy", "@type": "prim:policy", "name": "Authentication Policy", "definition": "All API endpoints require authenticated access", "success_criterion": "Auth method, token lifecycle, and violation handling specified", "health_status": "untested", "phase": "define", "artifactAffinity": ["business-rule", "nfr"], "source": "inferred", "parent": "root", "policy_type": "authorization"}

// event
{"@id": "node-order-placed", "@type": "prim:event", "name": "Order Placed Event", "definition": "Published when a new order is successfully submitted", "success_criterion": "Trigger, payload, consumers, and delivery guarantees specified", "health_status": "untested", "phase": "connect", "artifactAffinity": ["sequence-diagram", "data-flow"], "source": "inferred", "parent": "root", "trigger": "Order transitions to submitted state", "consumers": ["Inventory Service", "Notification Service"]}
```

---

## HANDOVER.md Tree Section Template

Include this section in HANDOVER.md when a PRIMITIVE_TREE.jsonld exists:

### Structural Inventory (Primitive Tree)

**File:** [PRIMITIVE_TREE.jsonld](PRIMITIVE_TREE.jsonld)

The primitive tree provides a structural decomposition of the system's architectural
building blocks — the components, integrations, policies, and data stores that make up
the system. It complements the SRD's behavioural specification (use cases, flows, rules)
with a structural inventory.

#### New vs. Existing Components

| Category | Count | Description |
|----------|-------|-------------|
| Existing (source: codebase) | {n} | Components identified from the existing codebase |
| New — user specified (source: user) | {n} | Components specified during facilitation |
| New — inferred (source: inferred) | {n} | Components inferred by the analyst, confirmed during facilitation |

#### Implementation Sequencing

The tree's `depends-on` edges indicate implementation ordering. Build upstream
dependencies before downstream dependants:

1. {First tier — nodes with no upstream dependencies}
2. {Second tier — nodes that depend only on tier 1}
3. {Third tier — nodes that depend on tier 1 or 2}
...

Nodes connected by `conflicts-with` edges represent architectural alternatives —
resolve these decisions before implementing either option.

#### Reading the Tree

- **For human consumption:** Read the exec summary above for a plain-language overview.
- **For programmatic use:** Parse PRIMITIVE_TREE.jsonld. Each node in `@graph` has typed
  properties, health status, and dependency edges. Use `artifactAffinity` to locate the
  relevant SRD artifacts for each component.

---

## RECONCILIATION_MAP.md Template

Generated by the SRD analyst's **Two-Model OODA Reconciliation** rule (continuously during
Phases 2-3; one final sweep at Phase 3.5). One row per OODA cycle. Append-only across
sessions — read existing rows before appending new ones.

**Cycle ID format.** Dotted-decimal addresses scoped by ISO date.
`2026-05-15.1.3.2` = second child of third child of first cycle on 2026-05-15. New
top-level cycles in subsequent sessions continue from `2026-05-16.1`, never re-use the
same date prefix's number space.

**Category values.** `match` (domain need + code present, aligned), `gap` (domain need,
no code), `orphan` (code, no domain need). Resolution values: `spec UC-NN`, `reference
{module|spec}`, `out-of-scope`, `external-system`, `genesis-bootstrap`,
`primitive-component`, `external-spec`, `existing-impl`, `unresolved` (Phase 5 gate
fails on this).

**Source values.** `user-tNN` (user statement at turn NN), `prior-art-grep`,
`recurse from UC-NN`, `INDEX.md/{source-id}`, `CP-01/{entry}`, `WebFetch/{url}`,
`probe-1.2/{capability-id}`.

```markdown
# Reconciliation Map — {project-slug}

> Two-Model OODA Reconciliation record. Domain Model = what the real world needs.
> Code Model = what the codebase implements. One row per OODA cycle. Append-only.

| Cycle | Claim or Capability | Source | Domain need? | Code reality | Category | Resolution | Tree node | Journal |
|------:|---------------------|--------|--------------|--------------|----------|------------|-----------|---------|
| {YYYY-MM-DD.N} | {one-line claim or capability path} | {source-id} | {yes/no/admin-plane} | {none/partial/match-summary} | match\|gap\|orphan | {resolution} | {node-id or "leaf"} | t{NN} |

## Open frames

(Frames from `EXPLORATION_JOURNAL.md` § Reconciliation Cycle Stack with `status: open`.
Phase 5 gate fails until this list is empty.)

## Out-of-scope dispositions

(Orphan rows resolved to `out-of-scope` — kept here for audit; the original code
remains in the repo unspecified.)
```

---

## EXPLORATION_JOURNAL.md Triage Trace section (AAF-07)

Every question emitted to the user MUST first be logged here per AAF-07 in
`plugins/sulis/references/audience-adapted-framing-standard.md`. The trace is the
gate, not the documentation — questions without a trace row are not emitted.

```markdown
## Triage Trace

| Turn | Pending question (verbatim) | Step 1 | Step 2 | Step 3 | Emitted? |
|------|------------------------------|--------|--------|--------|----------|
| t{NN} | "{question text exactly as it will appear to the user}" | pass | pass | ask | yes |
| t{NN} | "{question that died at step 1}" | fail | — | — | no — silent |
```

One row per pending question. Step 1/2/3 values: `pass` / `fail` / `ask` /
`silent` / `announce`. "Emitted?" is yes only if all three steps pass to step 3
ask. A one-sentence rationale follows each row as a bullet beneath, citing the
specific clause of AAF-01 that fired.

---

## COMPLETENESS_REPORT.md Auto-Resolved section (AAF-06)

When Phase 5 validation runs, every gap from every perspective passes through
AAF-01 triage. Gaps that fire at step 1 or step 2 are fixed inline and listed
here — they never become user questions.

```markdown
## Auto-Resolved (step-1-silent and step-2-silent gaps fixed inline)

- [Perspective N] {flag} {gap description} — fixed by {action}; AAF-01 step {1|2} fired because {one-line rationale}
- ...
```

Sibling section `## Done with announcement` captures step-3-silent gaps where
the user's stated principles supplied the answer:

```markdown
## Done with announcement (convention applied; user can audit and override)

- [Perspective N] {flag} {gap} — applied {convention from CP-01..CP-05}; rationale: {one line}
```

The third list, `## User Input Required`, contains only step-3 survivors in
plain English — each entry must have a corresponding row in the Triage Trace.

---

## Glossary Template

| Term | Definition | Context | First Appeared |
|------|-----------|---------|----------------|
| {Term} | {Precise definition as used in this domain} | {Where/how this term is used} | {Phase/turn where it was introduced} |

### Synonyms and Disambiguation

| Preferred Term | Also Known As | NOT the Same As |
|---------------|---------------|-----------------|
| {Preferred} | {Synonyms used during exploration} | {Terms that sound similar but mean different things} |

---

## MISUSE_CASES.md Template

Generated by Phase 3.6 (Adversarial Sweep). Captures abuse cases, misuse flows, and the
negative requirements they imply. Each misuse case cross-references the use cases it
attacks and the NFRs that encode its system response.

# Misuse Cases: {Project Name}

**Version:** {version}
**Date:** {date}
**Status:** Draft | Review | Approved

---

## Summary

| MUC-ID | Misuse Case | Targets | System Response (Required) | Source |
|--------|-------------|---------|---------------------------|--------|
| MUC-01 | {Negative-phrased name} | UC-{ID}, ... | {Refuse / Detect / Rate-limit / ...} | {abuse-case / STRIDE / pre-mortem} |

---

## MUC-{ID}: {Misuse Case Name}

**Abusive Actor:** {Who would do this — fraudulent user, compromised account, hostile insider, automated abuse, competitor scraper, etc.}
**Targets:** {UC-IDs the attack is aimed at, or system assets — PII store, payment flow, etc.}
**Source:** {Abuse case (Stage 1) / STRIDE-{category} (Stage 2) / Pre-mortem (Stage 3)}
**Likelihood:** {High | Medium | Low}
**Impact if successful:** {What the attacker gains; what the system loses}

### Misuse Flow

| Step | Attacker | System (no response) | System (with required response) |
|------|----------|---------------------|--------------------------------| 
| 1 | {Attack action} | {What would happen if unprotected} | {What the system MUST do instead} |

### System Response (REQUIRED)

The negative requirement(s) that defend against this misuse case. These are added to the
affected use case's `Negative Requirements` section in SRD.md and to NFR.md where they
imply measurable targets.

| NR-ID | Requirement | Type | Lives in |
|-------|-------------|------|----------|
| NR-{01} | System MUST {refuse / detect / log / rate-limit / ...} | Functional | SRD.md UC-{ID} |
| NFR-{01} | System MUST {measurable target — rate ceiling, retention period, integrity guarantee} | Non-functional | NFR.md |

### Related Misuse Cases

{Cross-references to other MUCs that share the same abusive actor or attack pattern.}

---

## Pre-mortem Record

The pre-mortem question was: "Assume this system has been live for 6 months and has
failed badly. What are the top 3 most likely reasons?"

| # | Failure Scenario | User-Stated | Specified As |
|---|------------------|-------------|--------------|
| 1 | {Scenario} | turn {N} | MUC-{ID} / NFR-{ID} / Risk note in HANDOVER.md |
| 2 | ... | ... | ... |
| 3 | ... | ... | ... |

---

## STRIDE Coverage Matrix

Per security-sensitive primitive: which STRIDE categories were considered, which applied,
which were N/A and why.

| Primitive | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | Elevation |
|-----------|----------|-----------|-------------|-----------------|-----|-----------|
| {Auth flow / integration / data-store} | {MUC-{ID} / N/A: reason} | ... | ... | ... | ... | ... |
