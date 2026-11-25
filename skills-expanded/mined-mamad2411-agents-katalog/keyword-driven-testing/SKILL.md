---
name: keyword-driven-testing
description: Use keyword-driven and BDD-style frameworks (Robot Framework 7, Cucumber 7, Gauge) so non-technical stakeholders can author or read tests, while engineers maintain the keyword library. Use when business readability is the binding constraint, not when developers own all tests.
source: self
date_added: 2026-04-30
---

# Keyword-Driven Testing

Keyword-driven testing separates *test logic* (data tables / Gherkin) from *implementation* (keywords/step definitions). Powerful for BAs and SMEs; expensive to maintain if misused.

## Stack Baseline (2026)

| Tool | Notes |
| --- | --- |
| Robot Framework 7 | Tabular keywords, huge library ecosystem (Browser/Playwright, SeleniumLibrary, RequestsLibrary) |
| Cucumber 7 (JVM/JS/.NET) | Gherkin syntax (`Given/When/Then`), step defs in code |
| SpecFlow / Reqnroll | .NET Gherkin |
| Gauge | Markdown specs, polyglot |
| Karate | DSL combining Gherkin + powerful API/UI engine |

## When It Pays Off

- Domain experts must read or write scenarios (insurance, finance, healthcare).
- Acceptance tests double as living documentation.
- Many similar test cases vary only by data (parameter tables).

## When It Hurts

- Pure dev-driven testing: BDD adds ceremony with no readers.
- Highly technical flows (perf, security, infra) where Gherkin is awkward.
- Small teams: maintenance of glue code outweighs benefits.

## Layered Architecture

1. **Specifications** — Gherkin `.feature` or Robot `.robot` files; one scenario per behavior.
2. **Keywords / step defs** — reusable, business-language verbs (`Place an order for {qty} of {sku}`).
3. **Page/Service objects** — implementation detail (selectors, HTTP calls).
4. **Helpers** — data builders, fixtures, hooks.

Keep keywords business-level; never write `Click on #btn-submit` as a keyword.

## Robot Framework Snippet

```robot
*** Settings ***
Library    Browser

*** Test Cases ***
User places an order
    Given a logged-in customer    alice@example.com
    When they add 2 of    SKU-42    to the cart
    And they check out
    Then the order is confirmed with status    PAID

*** Keywords ***
a logged-in customer
    [Arguments]    ${email}
    Open Browser To Login
    Login As    ${email}
```

## Cucumber Snippet

```gherkin
Feature: Checkout
  Scenario Outline: discount applied
    Given a cart total of <total>
    When promo code <code> is applied
    Then the new total is <expected>
    Examples:
      | total | code     | expected |
      | 100   | SAVE10   | 90       |
      | 200   | SAVE10   | 180      |
```

## Governance

- Step defs/keywords in a shared library with semantic versioning.
- Linter (gherkin-lint, robotframework-lint) on PR.
- Reuse audit: ban one-off step defs that wrap a single API call.
- Avoid "imperative Gherkin" (`Given I click ...`) — keep declarative.

## Common Pitfalls

- **Imperative Gherkin** — reads like a script, not a specification.
- **Step explosion** — hundreds of near-duplicate steps. Refactor into parameters.
- **Glue code becomes the system** — hidden complexity worse than in code.
- **BDD without business** — all the cost, none of the benefit.
- **Tests in PowerPoint, not VCS** — specs must live in repo.

## References

- Robot Framework — https://robotframework.org/
- Cucumber docs — https://cucumber.io/docs/
- _BDD in Action_ — John Ferguson Smart
- _Specification by Example_ — Gojko Adzic
