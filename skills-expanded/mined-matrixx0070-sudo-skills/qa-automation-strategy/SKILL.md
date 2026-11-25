---
name: qa-automation-strategy
version: 1.0.0
description: Decide what to automate versus test manually and shape the test-pyramid mix for a fast, trustworthy automated suite.
author: matrixx0070
tags: [qa, automation, test-pyramid, roi, ci]
capabilities: []
---

## When to use

When deciding where to invest automation effort — which checks to automate, at which layer, and what to leave manual. Automation is an investment with maintenance cost, not a default good. Use this before building a suite, or when an existing suite is slow, flaky, or top-heavy.

**Not for:** authoring one specific automated test (just write it), choosing a tool/framework vendor (that's tooling, downstream of strategy), or deciding overall test coverage for a feature (see qa-test-plan). This is the automate-or-not and which-layer call.

## Method

1. **Filter candidates by automation ROI.** Automate what is repetitive, stable, high-value, and deterministic. Decision point: if a check runs rarely, changes constantly, or needs human judgment (visual polish, UX feel), keep it manual — automating it costs more than it saves.
2. **Place each check at the lowest viable layer** of the pyramid: unit (logic, edge cases — many, fast), integration/API (seams, contracts, real dependencies — moderate), UI/e2e (critical journeys only — few, slow). If a bug can be caught by a unit test, don't write an e2e for it.
3. **Guard the pyramid shape.** Decision point: if e2e count is climbing, it's a smell — push cases down. An inverted pyramid (many slow UI tests) is the top cause of flaky, distrusted suites.
4. **Design for determinism** — control clock, network, randomness, and test data. A flaky test is a defect; quarantine and fix, never paper over with retries.
5. **Set the CI gate:** fast unit + integration block every merge; slow e2e run pre-release or nightly.
6. **Plan maintenance:** who owns failures, how flakes are triaged, when tests get deleted.

## Example

```
Feature: invoice generation.
Automate: tax math, rounding, currency formatting (unit — 30 cases);
          invoice API + real DB (integration — 6); "create + download PDF" (e2e — 1).
Manual: PDF visual layout, print rendering (human judgment).
Pyramid: 30 / 6 / 1. Gate: unit+integration on merge, e2e nightly.
Determinism: freeze clock for due-date tests; seed fixed invoice IDs.
```

## Pitfalls

- **Automate everything** — including one-off checks and UX feel, drowning in maintenance.
- **Inverted pyramid** — slow flaky UI tests doing work a unit test should own.
- **Ignoring flake** — retry-looping green instead of treating flakes as defects, eroding trust.
- **No owner for failures** — a red suite everyone ignores is worse than no suite.

## Output format

```
Automate vs. manual: <what's automated | what stays manual + why>
Pyramid mix: unit / integration / e2e — rough counts + rationale
ROI notes: <why each automated area earns its maintenance cost>
Determinism plan: <clock/network/random/data control>
CI gate: <blocking suites vs. nightly/pre-release>
Maintenance: <failure owner, flake triage, deletion policy>
```
