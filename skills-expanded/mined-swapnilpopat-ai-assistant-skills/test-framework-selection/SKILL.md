---
name: test-framework-selection
description: Choose a test framework using a weighted decision matrix across stack fit, parallelism, debugging, ecosystem, CI, and team skills. Use when starting a new project or replacing an aging framework.
source: self
date_added: 2026-05-01
---

# Test Framework Selection

Frameworks are 5-year decisions. This skill drives a defensible, criteria-based choice — not a vibes-based one — across unit, component, API, UI, mobile, and performance layers.

## Stack Baseline (2026)

| Layer | Strong defaults | Notable alternatives |
| --- | --- | --- |
| JS/TS unit | **Vitest 3** | Jest 30, Bun test, Node `--test` |
| Java unit | **JUnit 5.11** | TestNG 7.10, Spock 2 (Groovy/Kotlin) |
| Python unit | **pytest 8** | unittest, nose2 |
| .NET unit | **xUnit.net 3** | NUnit 4, MSTest v3 |
| Go test | **stdlib + testify** | Ginkgo 2, gocheck |
| Component (web) | **Vitest browser mode + RTL**, Storybook test | Cypress component, Playwright CT |
| API E2E | **Playwright APIRequest** / **Bruno** / **RestAssured 5** | Karate 1.5, Postman/Newman, hurl |
| Contract | **Pact 4.x**, **Schemathesis 4** | Spring Cloud Contract, Dredd |
| UI E2E | **Playwright 1.50** | Cypress 14, WebdriverIO 9, Selenium 4 |
| Mobile | **Maestro 2** (smoke), **Appium 2** (deep), XCUITest, Espresso | Detox |
| Perf | **k6 0.55** | Gatling 3.13, Locust 3, JMeter 5.6 |
| BDD | **Cucumber 7** + Playwright/Karate | Behave, SpecFlow → Reqnroll |
| Visual | **Chromatic**, Percy, Playwright snapshots | Argos |
| Property-based | jqwik (Java), fast-check (TS), Hypothesis (Py), proptest (Rust) | — |

## When to Use

- Greenfield project / repo split.
- Migration off a legacy framework (Protractor, EOL JUnit 4, Selenium IDE).
- Polyglot platform standardization.
- Costly flake / parallelism / IDE-debug pain.

## Decision Matrix Template

Score each candidate 1–5 against weighted criteria; total wins.

| Criterion | Weight | Why it matters |
| --- | ---: | --- |
| Stack fit (lang, build, framework) | 5 | Friction kills adoption |
| Speed & parallelism | 5 | Sub-10-min CI feedback target |
| Debug experience (IDE, traces) | 4 | TTR on flake / fail |
| Auto-wait / determinism | 4 | Flake budget |
| Ecosystem & plugins | 3 | a11y, visual, OTel, BDD |
| Reporting (HTML, Allure, GH) | 3 | Stakeholder trust |
| Cloud grid support | 3 | BrowserStack/Sauce/AWS |
| Team skills & community | 3 | Hiring + Stack Overflow depth |
| Maintenance trajectory | 4 | Active releases, vendor health |
| Cost / license | 2 | OSS preferred |

## Worked Example — Web E2E in 2026

| Criterion | Wt | Playwright | Cypress 14 | WdIO 9 |
| --- | ---: | ---: | ---: | ---: |
| Stack fit (TS, monorepo) | 5 | 5 | 5 | 4 |
| Speed & parallelism | 5 | 5 | 4 (parallel cloud or community) | 4 |
| Debug (trace viewer, codegen) | 4 | 5 | 5 | 4 |
| Auto-wait | 4 | 5 | 5 | 4 |
| Ecosystem | 3 | 5 | 4 | 5 |
| Cross-browser (WebKit, FF) | 3 | 5 | 3 | 5 |
| Mobile emulation | 2 | 5 | 3 | 5 |
| Cloud grids | 3 | 4 | 4 | 5 |
| Reporting | 3 | 5 | 4 | 4 |
| Cost | 2 | 5 (OSS) | 4 (OSS, paid cloud) | 5 |
| **Total (×wt)** | | **156** | **140** | **143** |

→ **Playwright** wins; Cypress is reasonable for teams with Cypress muscle memory; WdIO if you need Selenium grid + cross-mobile.

## Process

1. **Define needs**: stack(s), browsers/devices, CI minutes budget, parallelism, BDD requirement, compliance/reporting needs.
2. **Long-list 3–4 candidates** per layer.
3. **Score with the matrix**; document weights up-front (no retro-fitting).
4. **Spike top 2** for 2 days each: same realistic flow (login + form + table + dialog), measure wall-clock, flake count, debug TTR.
5. **Decide & ADR.** Commit to one per layer; document escape hatch criteria.
6. **Re-evaluate yearly** — frameworks evolve fast.

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Choosing on Twitter sentiment | Run a spike on your real flow + score |
| Mixing two UI E2E frameworks "to compare" forever | Pick one; deprecate the other within a quarter |
| Ignoring WebKit / mobile in 2026 | Real users browse on Safari/iOS; Cypress lacks WebKit-on-CI |
| Picking BDD for engineering convenience | BDD only if PM/QA actually author scenarios |
| Cloud grid lock-in | Keep tests runnable locally; grid is a deploy target, not a dependency |
| "Modern = better" | Maturity, ecosystem, debug tools beat novelty |

## Output Format (ADR-lite)

```
Decision: Playwright 1.50 for web E2E
Date: 2026-05-01  Owners: QA Guild + Web Platform
Context: Replacing Cypress 12; need WebKit + iOS Safari in CI
Options scored: Playwright 156, WdIO 143, Cypress 140 (matrix attached)
Spike outcome: Playwright = 4m20s parallel × 4 shards, 0 flakes / 100 runs
Consequences:
  + WebKit + iOS in CI; built-in trace viewer; faster
  − Re-train 6 engineers (1 sprint); rewrite 80 specs
Escape: re-evaluate if WebKit support degrades or Microsoft archives the project
```

## References

- ThoughtWorks Tech Radar (test): <https://www.thoughtworks.com/radar>
- State of JS — Testing: <https://stateofjs.com/>
- Playwright vs Cypress comparisons (Sauce Labs / BrowserStack)
- ISTQB Test Automation Engineer syllabus
