---
name: gherkin-specs
description: Use when writing or editing OpenSpec specs — guides Gherkin-style GIVEN/WHEN/THEN scenarios in the domain's business language.
license: MIT
---

# Gherkin Specs

## Overview

Write domain specifications using Gherkin-style scenarios. Each scenario describes one behavior from the
user's perspective, using the domain's business language.

## When to Use

- During the **propose** phase, when writing `specs/`
- Editing existing specs in `openspec/specs/<capability>/spec.md`
- Adding scenarios for edge cases or new requirements

Do NOT use for implementation details, technical design, or test code. Specs describe **WHAT** the
system does, not **HOW**.

## Format

```markdown
### Requirement: <name>
<Business description in domain language>

#### Scenario: <name>
- **GIVEN** <precondition / initial state>
- **WHEN** <action / trigger>
- **THEN** <expected outcome>
- **AND** <additional outcomes> (optional)
```

## Conventions

- **Domain language**: use the business terms defined in `AGENTS.md`; do not introduce synonyms.
- **No implementation terms**: avoid class names, layers, endpoints or data structures.
- **One behavior per scenario**: do not test several variants in the same scenario.
- **GIVEN is mandatory**: every scenario needs an explicit initial state.
- **Independence**: scenarios do not depend on each other; each sets its own GIVEN.
- **Business, not UI**: describe intent, not clicks or screens.

## Examples

> The identifiers in angle brackets are **placeholders**. Replace them with the project's domain terms.

### Requirement: Register `<entity>` with a unique identifier

The system allows registering an `<entity>` with a unique identifier.

#### Scenario: Successful registration

- **GIVEN** a valid identifier that does not exist in the system
- **WHEN** an `<entity>` is registered with its mandatory data
- **THEN** the `<entity>` is created with the provided data
- **AND** the corresponding domain event is published

#### Scenario: Duplicate identifier rejected

- **GIVEN** an existing `<entity>` with identifier X
- **WHEN** another `<entity>` is registered with the same identifier X
- **THEN** the system rejects the operation with a duplicate error

### Requirement: Register `<lifecycle event>`

The system allows recording a `<lifecycle event>` for an existing `<entity>`.

#### Scenario: Successful lifecycle transition

- **GIVEN** an `<entity>` in a state that allows the transition
- **WHEN** the `<lifecycle event>` is registered with its data
- **THEN** the `<entity>` moves to the new state
- **AND** the state change is visible in subsequent queries

#### Scenario: Invalid transition rejected

- **GIVEN** an `<entity>` in a state that does not allow the transition
- **WHEN** the `<lifecycle event>` is registered
- **THEN** the system rejects the operation with an invalid-state error
