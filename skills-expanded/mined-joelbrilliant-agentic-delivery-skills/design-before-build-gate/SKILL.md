---
name: design-before-build-gate
description: Enforces a design/spec approval gate before production implementation. Use when UI, UX, product flows, architecture, API shape, prototypes, visual direction, or user-facing behaviour need signoff before builders write production code.
---

# Design Before Build Gate

## Overview

Use this skill when design, product direction, or interface shape matters before implementation.

Prototype and spec work is not production build work. The gate exists to stop agents from turning half-approved ideas into shipped code.

## When to Use

- UI or product surface changes.
- New user flow or information architecture.
- API or module interface is uncertain.
- Multiple design directions should be compared.
- A prototype exists and needs approval before build.
- The user changes design after signoff.

## Roles

- **Designer/spec agent**: explores options, prototypes, and tradeoffs. Does not implement the production slice by default.
- **Owner/user**: signs off direction.
- **Builder**: implements only the approved direction.
- **Orchestrator**: enforces the gate and resolves scope drift.

## Gate Workflow

### 1. Define design question

State what must be decided:

- layout;
- interaction;
- content hierarchy;
- API contract;
- data model shape;
- user behaviour.

### 2. Produce options

Prefer 2 to 3 distinct options when uncertainty is real.

For each option, include:

- intent;
- tradeoffs;
- implementation complexity;
- risks;
- what would make it fail.

### 3. Get explicit signoff

Before production build, capture:

```text
Approved direction:
Rejected alternatives:
Required changes:
Non-goals:
Evidence/reference:
```

No ambiguous "looks good" if material decisions remain.

### 4. Build only approved scope

Builder must not reinterpret design. If implementation reveals a design flaw, stop and request re-approval.

### 5. Re-approval triggers

Re-approval is required when:

- visual hierarchy changes materially;
- interaction changes;
- API contract changes;
- design tokens or brand direction change;
- data shown to users changes;
- implementation chooses a rejected alternative.

## Verification

Final signoff should compare:

- approved design/spec;
- production implementation;
- screenshots or runtime surface;
- accessibility/usability basics;
- responsive states if relevant;
- data states: empty, loading, error, populated.

## Anti-patterns

- Designer writes production code by default.
- Builder chooses a different design because it is easier.
- User-facing UI is verified only with unit tests.
- Design changes after signoff are treated as implementation details.
- Prototype polish is mistaken for production readiness.
