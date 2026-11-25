---
name: architecture-proposal
description: Produces the formal architecture proposal before implementation: executive summary, requirements mapping, system, application, database, API, frontend, security and DevOps architecture, sized to the project and written as the technical contract. Run after technology selection, before the validation gate.
license: MIT
metadata:
  category: delivery-skills
  version: 1.0.0
  depends_on: [engineering-core, requirements-analysis, architecture-design, technology-selection]
  outputs: [architecture-document, requirements-mapping, risk-register, proposal-summary]
---

# Architecture Proposal

Writes the document the user approves and the implementation obeys. After the
validation gate, this document is the technical contract; departing from it
requires change control, not a decision.

`architecture-design` decides boundaries for one subsystem. This skill
produces the whole picture for a project, and makes it reviewable by someone
who will not read the code.

## 1. Sizing

The proposal is proportional. A one page proposal that gets read beats a forty
page document that gets approved unread.

| Project | Proposal |
|---|---|
| small | one page, sections 1, 3, 5, 9 only, others marked not applicable |
| medium | three to five pages, all nine sections, short |
| large | one document per section, in `docs/architecture/` |

Every section that does not apply says so with a reason. Silence is not a
size.

## 2. The nine sections

### 1. Executive summary

What will be built, how, in a paragraph a non engineer can read. The stack in
one line. The one or two decisions that shape everything else.

### 2. Requirements mapping

Every major requirement mapped to the component that satisfies it.

```
| Requirement | Component | Notes |
|---|---|---|
| R4 trainee receives an attestation | certificate service, PDF generation | R4 depends on U3, resolved as generated PDF |
```

This table is what makes the proposal reviewable. A requirement with no
component is not covered. A component serving no requirement is not needed.

### 3. System architecture

Only the pieces the project actually has. Naming a queue, a cache and a worker
that the project does not need makes the proposal look serious and the system
worse.

```
Frontend           what runs in the browser, how it is served
Backend            what runs on a server, in how many pieces
Database           engine, one or several, why
Authentication     mechanism and where identity lives
Storage            files, where, public or private
External services  each one, what it does, what happens when it is down
Queues, workers    only if a real need is stated
Caching            only after a measurement or a stated volume
Infrastructure     where this runs
Monitoring         how a failure becomes visible
```

Each line that is absent from the project is written as `none, and why`.

### 4. Application architecture

Modules, responsibilities, boundaries, data flow, dependency direction. One
diagram in ASCII, no more.

The important content is the ownership table: which module owns which
behaviour and which data. See `architecture-design` section 3.

### 5. Database architecture

Entities, relationships, keys, indexes, constraints, transactions, data
lifecycle, migration strategy.

Data lifecycle is the field most often omitted and most expensive to add
later: what is created, what is soft deleted, what is purged, what is
retained and for how long, what happens to related rows when an account
closes.

### 6. API architecture

Endpoints or operations, request and response shapes, authentication,
authorization model, validation, error contract, pagination, filtering,
sorting, idempotency where money or resource creation is involved.

The authorization model is stated as a rule, not per endpoint: how the system
decides whether this caller may touch this object.

### 7. Frontend architecture

Routing, component architecture, state placement policy, data fetching,
forms, validation, the five states, responsive strategy, accessibility target.

The accessibility target is a level and a measurement method, not an
intention.

### 8. Security architecture

Authentication, session or token model with lifetimes, authorization
enforcement point, input validation strategy, rate limiting, secret handling,
security headers, data protection, and the threat model in three lines: who
would attack this, for what, and what stops them.

### 9. DevOps architecture

Environments, local development, CI, CD, deployment mechanism, secret
delivery, migration execution, backups, monitoring, logging, rollback.

Rollback is stated concretely, including what a rollback does not restore.

## 3. Risk register

Every proposal carries one. A proposal with no risks was not thought about.

```
| Risk | Likelihood | Impact | Mitigation | Trigger to revisit |
|---|---|---|---|---|
```

Include at minimum: the assumptions that would be expensive to reverse, the
external dependencies, the parts of the schema that are hard to change, and
anything the timeline makes tight.

## 4. What the proposal must not contain

- Components the requirements do not justify.
- A microservice split for a team that deploys one artefact.
- A queue, a cache or a search engine introduced without a stated need.
- Technology chosen for its popularity, with no alternatives considered.
- Diagrams that repeat the text.
- Estimates presented as certainties.
- Any statement that the design is secure, scalable or future proof.
- Requirements that were not in the specification.

## 5. Document location

Follow the project. When it has none:

```
docs/
  architecture/
    architecture.md          sections 1, 3, 4
    technology-decisions.md  from technology-selection
    database.md              section 5
    api.md                   section 6
    security.md              section 8
    deployment.md            section 9
```

Small projects use one file. Creating six files for a one page proposal is the
same error as omitting sections from a large one.

## 6. Protocol

1. Take the specification, the assumptions and the stack decisions.
2. Size the proposal, section 1.
3. Write the requirements mapping first. It exposes gaps before effort is
   spent on prose.
4. Write sections 3 to 9, marking the inapplicable ones with a reason.
5. Delegate each subsystem boundary decision to `architecture-design`.
6. Build the risk register.
7. Restate every surviving assumption, visibly, at the end.
8. Check against section 4.
9. Write the proposal summary for `validation-gate`.

## 7. Auto-critique

Score from 0 to 5: proportionate size, every requirement mapped to a
component, no component without a requirement, data lifecycle present,
authorization stated as a rule, failure paths per external dependency, risk
register honest, assumptions restated, nothing invented.

Threshold: no axis below 3, average at least 4. A requirement with no
component, or a component with no requirement, is an automatic failure.

## 8. Interfaces

- Upstream: `requirements-analysis`, `clarification-gate`,
  `technology-selection`.
- Delegates to: `architecture-design` for boundary decisions,
  `devops-core` for section 9.
- Downstream: `validation-gate`, then `delivery-planning`.
- Maintained by: `scope-and-change-control` once approved.
