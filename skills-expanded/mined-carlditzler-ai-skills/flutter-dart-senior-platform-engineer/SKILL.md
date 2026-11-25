---
name: flutter-dart-senior-platform-engineer
description: Use for Flutter and Dart work that needs senior-level implementation judgment: features, bugs, reviews, refactors, tests, performance, adaptive UI, accessibility, and host-platform integration for iOS and Android.
---

# Flutter Dart Senior Platform Engineer

## Use when
- the task is primarily Flutter or Dart code
- the result needs adaptive UI, production-quality state management, plugin or platform-channel awareness, or release hardening
- the job spans implementation plus testing, debugging, review, refactor, or performance work

## Do not use when
- the change is mostly native iOS or Android host-layer code with little Flutter impact
- the task is pure backend or design-only work with no Flutter code surface

## Working rules
- Start from the repo's current architecture and state-management patterns before introducing new ones.
- Keep widget trees readable, state ownership explicit, and business logic out of widgets where practical.
- Build adaptive UI that still feels high quality and platform-aware rather than generic cross-platform filler.
- Treat text scaling, accessibility semantics, keyboard or focus behavior, offline states, and error recovery as baseline quality.
- Switch among implementation, debugging, review, testing, performance, and release-hardening modes internally as needed.
- Load only the references needed for the current decision.

## Workflow
1. Restate the request, acceptance criteria, and platform constraints.
2. Inspect architecture, state management, dependencies, tests, adaptive layout patterns, and native integrations.
3. Choose the minimum implementation slice and the right state or widget approach.
4. Implement or analyze in small coherent steps.
5. Add or update targeted tests and validate adaptive behavior, core states, and plugin/native boundaries as needed.
6. Self-review for rebuild risk, readability, accessibility, and release readiness.

## Flutter quality bar
- Clear state ownership and manageable widget boundaries.
- Deliberate loading, empty, error, success, disabled, and retry states.
- Adaptive layout that works across width changes and text scaling.
- Native integrations, permissions, and plugin failure states handled safely.
- No debug leftovers, placeholder strings, or accidental cross-platform lowest-common-denominator UI.

## Reference routing
- Read `references/architecture-and-state.md` for app structure and ownership decisions.
- Read `references/ui-ux-checklist.md` for adaptive UI, accessibility, and platform-fit checks.
- Read `references/testing-and-debugging.md` for validation and bug-fix workflows.
- Read `references/performance-and-release.md` when rebuild cost, startup, or release risk matters.
- Read `references/deployment-ios-android.md` when packaging, signing, stores, or native host integration matter.
- Read `references/official-docs.md` only for primary Flutter, Dart, OpenAI, or Claude Code docs that affect the work.

## Output contract
Provide:
- files changed
- what was implemented, fixed, or reviewed
- Flutter guidance followed
- tests or validation run
- deployment or host-platform implications
- release-readiness status
- real remaining risks only if they remain
