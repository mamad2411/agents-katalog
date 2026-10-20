---
description: "Use when reading, writing, or modifying Gherkin .feature files. Covers syntax, formatting, step writing, Background, Scenario Outline, and tag conventions. Auto-applied to all .feature files."
applyTo: "**/*.feature"
---

# Gherkin Conventions

## File Location & Naming

- `specs/capabilities/<domain>/behavior.feature` — current truth. Never carries delta tags
- `specs/changes/<name>/delta.feature` — one change's additions, edits, removals. Always tagged
- Domains and change names use `kebab-case`

## Delta Tags (in `delta.feature` only)

| Tag                     | Meaning                                |
| ----------------------- | -------------------------------------- |
| `@added`                | New scenario, appended on merge        |
| `@modified:"<name>"`    | Replaces the named capability scenario |
| `@removed:"<name>"`     | Deletes the named capability scenario  |
| `@renamed:"<old name>"` | Retitles the named capability scenario |

Every delta scenario carries exactly one. Quoted names must match the capability exactly. A
`@modified:` must keep every `Then` the capability already has — dropping one is a removal, and
needs confirmation. Full reference: `docs/atdd/gherkin.md` § Delta Tags.

## Feature Block

```gherkin
Feature: <Title — imperative noun phrase, e.g. "Password Reset">
  As a <actor: user / admin / system / API client>
  I want <goal: what the actor is trying to do>
  So that <benefit: the business or user value>
```

## Background

Use `Background:` for preconditions shared by **ALL** scenarios in the file:

```gherkin
Background:
  Given the application is running
  And the database is seeded with test data
```

Do NOT use Background if a precondition applies to only some scenarios — put it in those scenarios
directly.

## Tags

Apply tags on the line immediately before `Scenario:` or `Scenario Outline:`:

```gherkin
@smoke @happy-path
Scenario: Successful password reset
```

| Tag           | Meaning                                              | Count           |
| ------------- | ---------------------------------------------------- | --------------- |
| `@smoke`      | Single most critical path — run on every build       | 1 per feature   |
| `@happy-path` | Primary success flows                                | 1–2 per feature |
| `@edge-case`  | Boundary conditions, unusual-but-valid inputs        | 2–4 per feature |
| `@error`      | Invalid inputs, unauthorized access, system failures | 2–3 per feature |
| `@wip`        | Not yet implemented — will fail intentionally        | Temporary       |
| `@regression` | Added to catch a previously found bug                | As needed       |

## Scenario Outline

Use for data-driven tests (same behavior, multiple input sets):

```gherkin
@edge-case
Scenario Outline: Login fails with various invalid credentials
  Given I am on the login page
  When I enter email "<email>" and password "<password>"
  Then I should see the error "<error_message>"

  Examples:
    | email              | password | error_message              |
    | not-an-email       | pass123  | "Invalid email format"     |
    | user@example.com   |          | "Password is required"     |
    |                    | pass123  | "Email is required"        |
```

## Formatting Rules

- 2-space indent for scenario content
- Blank line between scenarios
- Use `And` / `But` for additional steps of the same keyword (not repeated `Given`/`When`/`Then`)
- Keep step text concise — under 100 characters
- Use double quotes for string values: `"expected value"`
- Use angle brackets for Scenario Outline variables: `<variable_name>`

## Step Reuse

Reuse steps across scenarios by using **identical** step text. Even minor wording differences
create incompatible step definitions. Establish a consistent step vocabulary early.

## Anti-Patterns

| Anti-pattern                                 | Problem                            | Fix                                         |
| -------------------------------------------- | ---------------------------------- | ------------------------------------------- |
| Multiple `When` steps                        | Scenario tests multiple behaviors  | Split into separate scenarios               |
| `Then` asserts DB values / internal state    | Tests implementation, not behavior | Assert via the same interface the user uses |
| Scenario depends on another scenario's state | Order-dependent, fragile           | Use Background or explicit Given steps      |
| Vague `Then`: "Then it should work"          | Not testable                       | Specify the exact observable outcome        |
| Huge Background with 10+ steps               | Hard to understand any scenario    | Extract a step that encapsulates the setup  |
