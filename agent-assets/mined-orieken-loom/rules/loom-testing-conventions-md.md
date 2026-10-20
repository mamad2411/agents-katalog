# Testing Rules

Cross-language testing principles and the Saturday/Sunday framework conventions. Language-specific
tooling (unit test framework, fake-data/factory libraries, per-language Playwright bindings, reporting)
lives in each language's own `shared/rules/<language>-conventions.md` — this file covers what's shared
across all of them.

For the *why* behind the categories and disciplines below (FIRST principles, the Three Laws of TDD, when
role separation preserves TDD's design pressure and when it doesn't), see
`docs/patterns/testing-pyramid.md`. This file is the
enforceable "always/never" side; that one is the philosophy.

## Test Categories

Every test belongs to exactly one level. The level determines the writing agent, the framework, and the
principles that apply. Full detail in `docs/patterns/testing-pyramid.md`; this table is the enforcement
map.

| Level | Written by | Framework | Speed budget | Principles |
|---|---|---|---|---|
| Unit | `developer`, with the code it changes (ADR-009), or `unit-tester` (backfill/characterization) | project's language convention (Vitest/pytest/JUnit/xUnit/`testing`) | fractions of a second | FIRST |
| Integration | `qa-engineer` (or `developer` when the integration IS the feature) | same as unit | seconds, not minutes | FIRST |
| API Contract | `api-test-generator` (from OpenAPI) or `qa-engineer` (hand-written) | Sunday (`BaseApiClient` + `IHttpAdapter` + Fluent Matchers + Zod + Resilience Primitives) | seconds | Sunday's Declarative API Client Pattern |
| Acceptance | `qa-engineer` inside `deliver-atdd` or `deliver-feature` | Gherkin (Cucumber.js / Reqnroll / pytest-bdd / Cucumber-JVM per language) | tens of seconds per scenario | scenario IS the AC, business language |
| E2E / UI | `qa-engineer` following Saturday conventions | Saturday (Cucumber.js + Playwright, Site-Centric pattern) | minutes total for the suite | Saturday's Site-Centric Pattern |

## Saturday Framework (E2E / UI Testing)
ALWAYS use the Site-Centric pattern: `BaseSite`, `BasePage`, `BaseElement`, `BaseFlow`.
NEVER use traditional Page Object Model (POM).
ALWAYS use Playwright driven by Cucumber.js for UI automation.
ALWAYS include OpenTelemetry instrumentation for every BDD scenario.

## Sunday Framework (API Testing)
ALWAYS use Vitest for unit tests and Playwright for integration/E2E API tests.
ALWAYS use the custom api fixture (`api`) and fluent matchers (`toHaveStatus`, `toBeSuccessful`, `toRespondWithin`).
ALWAYS extend `BaseApiClient` for domain-specific API clients.
ALWAYS validate schemas with Zod (`validateSchema()`).
NEVER use custom retry loops — use `CircuitBreaker` or `ExponentialBackoffStrategy`.

## Test Quality
CRITICAL: Lines a change adds or modifies MUST be >= 85% covered (ADR-008).
CRITICAL: Cyclomatic complexity per function MUST be < 7.
ALWAYS prove a new test can fail: no test without a path to a failure; mutants on changed lines die.
Test-first is a technique, not a rule (ADR-009) — write the test before or after, then show it fails.
NEVER write feature code without tests.
ALWAYS keep tests "moist," not fully dry — DRY the setup noise (via Flows, Factories, fixtures) but
keep the critical assertion path visible in the test itself. A test verifying search results should
show "user searched for X" prominently in the test body; how they clicked into the search input should
not. Over-DRYing by hiding the interesting user action inside a flow makes the test read like a magic
incantation and defeats the point. This is the same idea as DAMP (Descriptive And Meaningful Phrases),
a well-known counterpoint to blanket DRY in tests.

## Reporting Pipeline
Cucumber JSON summaries feed the Friday dashboard (see `shared/rules/approval-gates.md` gate #1 —
posting to Friday requires explicit human approval, same as any other external-facing action). Every
language's port of Saturday should be able to produce Cucumber-JSON-compatible output, or a bridge to
it, so results from any language funnel through the same reporting/approval pipeline rather than each
language inventing its own.

## Test Annotation Convention

Every test carries traceability back to two things: **(1)** the issue that motivated it, and
**(2)** the specific acceptance criterion (or fine-grained behavior derived from one) it verifies.
Report-time mapping is a snapshot — rename or move the test and it evaporates — so the annotation
lives with the test itself.

- **Issue reference**: free-form (`PROJ-123`, `#789`, a URL). Teams pick what matches their tracker.
- **AC reference**: a short excerpt of the AC text, or a numbered reference (`AC1: ...`).
- **Use the language's own mechanism**, never a homegrown comment convention: JSDoc `@issue`/`@ac`,
  a pytest docstring, JUnit `@Tag`/`@DisplayName`, xUnit `[Trait]`, a Go comment, a Gherkin tag.
- **Gherkin needs no AC annotation** — the scenario name IS the acceptance criterion.
- **Granularity**: one AC often spawns 3-5 unit tests; each carries the same issue-ref and a
  narrower AC-ref (`AC1 - empty email`). Acceptance and E2E need only the issue tag.

The syntax for each language, the exemplar-test marking, and why this is documented convention
rather than a CI check, are in `docs/patterns/test-annotation.md` — kept out of every stage's
prompt, since a test is written in one language at a time (roadmap L3.19).
