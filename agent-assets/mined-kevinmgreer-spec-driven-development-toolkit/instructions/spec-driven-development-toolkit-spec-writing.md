---
description: "Use when writing Gherkin feature files, technical specs, acceptance criteria, or user stories. Covers how to write clear, testable, behavior-focused specifications. Trigger phrases: write spec, feature file, acceptance criteria, user story, specification, Gherkin, BDD, scenarios, Given When Then."
---

# Spec Writing Guidelines

## Core Principle: Behavior, Not Implementation

Good specs describe **what** the system does from the outside, not **how** it does it internally.

| ❌ Implementation-focused                                        | ✅ Behavior-focused                   |
| ---------------------------------------------------------------- | ------------------------------------- |
| `Given the UserService validates the password hash using bcrypt` | `Given I enter an incorrect password` |
| `Then the database record should have status=1`                  | `Then my account should be locked`    |
| `When the MessageBroker publishes to the order.created topic`    | `When I place an order`               |

---

## Gherkin Feature Files

### Structure

```gherkin
Feature: <Short imperative noun phrase, e.g. "User Login">
  As a <role>
  I want to <goal>
  So that <benefit>

  Background:
    Given <shared precondition for ALL scenarios>

  @smoke @happy-path
  Scenario: <Most critical success path>
    Given <initial state>
    When <action taken>
    Then <observable outcome>
    And <additional outcome>

  @edge-case
  Scenario Outline: <Data-driven variation>
    Given <state with <variable>>
    When <action>
    Then <outcome matches <expected>>
    Examples:
      | variable | expected |
      | ...      | ...      |
```

### Step Writing Rules

**Given** — establishes preconditions / context (state, not action)

- ✅ `Given I am logged in as an admin`
- ✅ `Given the cart contains 3 items`
- ❌ `Given I click the login button` (that's a When)

**When** — the action or event being tested (present tense, active voice)

- ✅ `When I submit the registration form`
- ✅ `When the payment processor is unavailable`
- ❌ `When the system processes the request` (implementation detail)

**Then** — the observable outcome from the user's or caller's perspective

- ✅ `Then I should see "Account created successfully"`
- ✅ `Then the order total should be $15.99`
- ❌ `Then the EmailService.send() method should be called once` (internal detail)

### What Makes a Good Scenario

- **Single behavior**: Each scenario tests exactly one thing
- **Independent**: Each scenario can run in any order without depending on others
- **Readable**: A non-technical stakeholder can understand it
- **Specific**: Uses concrete values (`$15.99`, not `the price`)
- **Testable**: Can be automated without ambiguity

### Scenario Coverage Checklist

- [ ] `@smoke` scenario (single most critical happy path)
- [ ] `@happy-path` scenarios (all primary success variations)
- [ ] Boundary values (empty inputs, max length, exactly-at-limit)
- [ ] Invalid formats (wrong type, malformed data)
- [ ] Required-field missing
- [ ] Unauthorized access (not logged in, wrong role)
- [ ] System/dependency failure (graceful degradation)

---

## Technical Spec (Markdown)

Technical specs complement Gherkin by documenting details that don't belong in scenarios:

- **Business rules** — detailed logic with edge cases and examples
- **API contracts** — request/response shapes, status codes, headers
- **Data constraints** — field types, max lengths, required vs optional
- **Out-of-scope** — explicit exclusions to prevent scope creep
- **Dependencies** — external services, infrastructure requirements

See [tech-spec.template.md](../skills/atdd/assets/tech-spec.template.md) for the full template.

---

## Naming Conventions

| Artifact             | Convention                       | Example                                               |
| -------------------- | -------------------------------- | ----------------------------------------------------- |
| Feature file         | `kebab-case.feature`             | `user-registration.feature`                           |
| Technical spec       | `kebab-case-spec.md`             | `user-registration-spec.md`                           |
| Feature name in file | Title case imperative            | `Feature: User Registration`                          |
| Scenario names       | Sentence case, describes outcome | `Scenario: Account is locked after 5 failed attempts` |
