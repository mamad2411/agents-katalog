---
name: repo-audit
description: "Audit existing frontend, Java, or Rust surfaces read-only. Use repo-review for change-based reviews."
---

# Repository Audit

## Entry Gate

Audit declared existing path scope only. Require a language/profile and evidence basis;
do not turn broad exploration into a change-basis review, source fix, or runtime claim.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Any audit route | [rule priority](references/rule-priority.md) | Resolved evidence authority |
| Frontend baseline | [frontend profile](references/frontend-profile.md) and [frontend checklist](references/frontend-review-checklist.md) | Selected frontend concerns |
| Frontend architecture, state/data, or component ownership applies | [architecture](references/frontend-architecture-and-ownership.md), [state/data](references/frontend-state-data-and-forms.md), and/or [components](references/frontend-component-system.md) | Concern-specific findings |
| Frontend styling, CSS, layout, or design-system concern applies | [styling systems](references/frontend-styling-systems.md), [style/layout](references/frontend-styling-and-layout.md), [CSS](references/frontend-css-governance.md), and/or [layout governance](references/frontend-layout-governance.md) | Concern-specific findings |
| Frontend framework, build, accessibility/performance, desktop, or anti-pattern concern applies | [framework](references/frontend-framework-profiles.md), [build](references/frontend-build-tooling.md), [accessibility/performance](references/frontend-accessibility-and-performance.md), [desktop](references/frontend-desktop-tauri.md), and/or [anti-patterns](references/frontend-anti-patterns.md) | Concern-specific findings |
| Frontend selected-source, visual, or DESIGN authority applies | [visual evidence](references/frontend-visual-evidence.md), [DESIGN compliance](references/frontend-design-md-compliance.md), [visual direction](references/visual-direction-and-anti-slop.md), and/or [specification authorities](references/specification-authorities.md) | Qualified visual findings/gaps |
| Frontend protocol concern applies | [frontend protocol contracts](references/frontend-protocol-contracts.md) | Qualified contract findings |
| Java baseline or engineering concern applies | [Java profile](references/java-profile.md), [Java checklist](references/java-checklist.md), and [Java engineering](references/java-engineering.md) | Selected Java concerns |
| Java protocol concern applies | [Java protocol contracts](references/java-protocol-contracts.md) | Qualified contract findings |
| Rust baseline, architecture, ownership, API, async, or memory concern applies | [Rust profile](references/rust-profile.md), [Rust checklist](references/rust-review-checklist.md), [baseline/lifecycle](references/rust-project-baseline-and-lifecycle.md), [architecture](references/rust-architecture-and-modules.md), [ownership/resources](references/rust-ownership-and-resources.md), [errors/API](references/rust-errors-and-api-design.md), [async](references/rust-async-and-concurrency.md), and/or [memory](references/rust-memory.md) | Selected Rust concerns |
| Rust unsafe/security, web/desktop, SQLite, performance, testing, or anti-pattern concern applies | [unsafe/security](references/rust-unsafe-and-security.md), [web/desktop](references/rust-web-and-desktop-boundaries.md), [SQLite](references/rust-sqlite.md), [performance](references/rust-performance.md), [testing](references/rust-testing-and-quality.md), and/or [anti-patterns](references/rust-anti-patterns.md) | Concern-specific findings |
| Rust agent-runtime concern applies | [agent runtime](references/rust-agent-runtime-profile.md) | Runtime-boundary findings/gaps |
| Cross-profile quality, OpenAPI, grounding, or design concern applies | [codebase design](references/codebase-design.md), [code quality](references/code-quality.md), [OpenAPI governance](references/openapi-contract-governance.md), and/or [project grounding](references/project-grounding.md) | Cross-boundary findings/gaps |

## Invariants

- Audit only the declared profile/path scope; a miss or static signal is not absence/runtime proof.
- Findings need owner, reachability, concrete impact, and falsifiable validation.
- Do not edit source, mutate Git, replace `repo-review`, or claim browser/client/runtime coverage without that evidence.

## Output Map

Return profile, scope/basis, findings, evidence, checks, exclusions, and `Not verified` gaps.

Calibrate severity by demonstrated impact and urgency: P0 is catastrophic, active or readily reachable, and immediately blocking; P1 is high-impact risk that should block delivery; P2 is a meaningful scoped defect; P3 is a minor actionable improvement. State reachability or impact uncertainty instead of treating an unverified worst case as established.

## Reference Map

- Read [rule priority](references/rule-priority.md) for every audit route.
- Load only the concern-specific references in the selected Route Map row; do not load an entire language group by default.
- Maintainers/calibration only: read [eval cases](references/eval-cases.md), [frontend scenarios](references/frontend-eval-scenarios.md), [Java scenarios](references/java-eval-scenarios.md), [Rust scenarios](references/rust-eval-scenarios.md), [frontend corpus](references/frontend-reference-corpus.md), or [Rust corpus](references/rust-reference-corpus.md); do not load them during ordinary runtime.
