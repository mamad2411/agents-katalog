---
name: writing-tests
description: Use when test quality decisions are needed for new, changed, brittle, missing, or review-requested unit or component tests, including tests-first work, assertion choice, mock boundaries, lifecycle scenarios, or independent test-session handoff.
---

# Writing Tests

Write tests from the caller's perspective using Vladimir Khorikov's standards. Tests protect desired behaviour, not current implementation.

This is a progressive-discovery skill: load only the reference needed for the current step.

## First Gate

If this same conversation session already implemented the production code under test, stop before mode detection. Do not enter mode detection or any workflow.

A session means one conversation window. Invoking this skill in the same conversation that wrote the code still shares the same context and blind spots. Knowing the code well is the liability: the builder will tend to write tests that confirm what the code does, including its bugs.

The builder must not write its own post-feature tests. Use a fresh test session with the requirement and finished code.

Exception: valid tests-first TDD before production code exists. Use `superpowers:test-driven-development` when available; otherwise state the fallback and follow RED-GREEN-REFACTOR locally.

Details: `references/agent-workflow.md`.

## Mode Detection

Declare one mode before reading implementation files:

| Signal | Mode |
|---|---|
| Tests before production code | TDD |
| Implementation is in progress | While-building |
| Feature is finished | Post-feature |
| Existing tests need fixing | Update |
| User asks for quality review | Review |
| Unclear | Ask one mode question, then stop |

Vague prompts always require the clarifying question. Examples: "write tests for X", "add tests for the Y part", and "test this feature" do not declare a mode. Ask one mode question only; do not ask mode and scope together, run discovery, inspect files, or infer a mode.

## Start Checklist

For every clear mode, post a visible checklist/plan before workflow work:

```text
- [ ] Step 1: Read source file (or TDD requirement/spec) + classify
- [ ] Step 2: Audit existing tests, if any
- [ ] Step 3: Recommend behaviours to protect -> user approves
- [ ] Step 4: Write tests
- [ ] Step 5: Run + report
```

Before Step 1, also post the confirmed file list. In TDD mode, read the user-provided requirement/spec first and post the planned public test target instead of a source file list. Do not read implementation files in TDD.

Zero exceptions: not for small files, obvious tests, time pressure, or a specific file named in the prompt. If you skipped the checklist, mode declaration, file list or TDD target, stop and restart at the gate.

Detailed gate rules and report format: `references/workflow.md`.

## Workflow

1. **Discover target.** Non-TDD: use branch diff, issue context, explicit user target, then search. TDD: use requirement/spec. Confirm the file list or TDD target with the user.
2. **Classify.** Domain -> unit tests, Controller -> unit-test any pure logic you extract; its cross-module orchestration belongs to the repo's flow / end-to-end layer, never an integration test authored here, Trivial -> skip, Overcomplicated -> Humble Object refactor recommendation, LLM-boundary -> deterministic unit tests + mocked API. Load `references/classification.md`.
3. **Audit existing tests.** Always check colocated tests before proposing new ones. Load `references/audit.md`.
4. **Recommend behaviours.** Lead with your recommendation and post the exact header `## Approved behaviours`. Do not use variations. Wait for user approval before writing.
5. **Write tests.** Discover the runner first. Assertion order: output > state > communication. Mock only unmanaged external dependencies. Load `references/assertions.md` and `references/mocking.md`.
6. **Run and report.** Outside TDD, leave desired-behaviour failures red and do not fix source. In TDD, the RED companion phase ends after the expected failing test; hand control to `superpowers:test-driven-development` for GREEN when available, or state that the local fallback will continue with GREEN/REFACTOR as a separate TDD step.

For stateful code, add lifecycle scenarios from `lifecycle-checklists.md`.
For skills, slash commands, and agent prompts, test behaviour with evals. Load `references/agent-artifact-evals.md`.

## Test scope — unit and component only

Authors unit and component tests only, each covering just the intended behaviour of the unit. No integration tests:

- **Never create `*.integration.test.*` files** — not a valid test type here.
- **No hidden integration in a unit file** — a `*.test.ts(x)` must not boot the full app/router, hit a real DB/HTTP/filesystem/external service, or wire several real modules together. That's a flow / end-to-end test, owned by the repo's higher layer, not here.
- Real ≠ integration: using one real **managed** dep a unit owns (its store, an in-process DB) and mocking only **unmanaged** deps is correct unit practice (`references/mocking.md`). Integration = cross-module / full-app wiring, not "a real dependency".

## Mode Notes

- **TDD:** `writing-tests` is the RED-phase quality companion. It writes and verifies the failing test; the TDD workflow owns later production-code GREEN/REFACTOR work. The unit/component-only scope (no integration tests) holds across the cycle — carry it into the `superpowers:test-driven-development` handoff.
- **While-building:** test each implementation slice immediately and report slice status.
- **Post-feature:** run discovery, then workflow per file in Domain -> Controller order.
- **Update:** identify tests covering the changed files, then audit and improve them in place after approval.
- **Review:** report quality findings first. For deep review, use `engineering-skills:adversarial-review`.

## Cross-Skill Handoffs

| Need | Handoff |
|---|---|
| Code too complex to classify | `engineering-skills:explaining-code` |
| TDD workflow | `superpowers:test-driven-development` if available; otherwise local RED-GREEN-REFACTOR |
| Skill, slash-command, or agent-prompt authoring quality | `superpowers:writing-skills` |
| Unexpected failure with unclear root cause | `superpowers:systematic-debugging` if available; otherwise debug systematically before reporting |
| Claiming all tests pass or merge readiness | `superpowers:verification-before-completion` if available; otherwise verify commands and outputs directly |
| Ready for PR | `engineering-skills:raising-linear-pr` |

## Reference Index

- `references/workflow.md` — gates, discovery, framework detection, report format
- `references/agent-workflow.md` — separate-session rule and TDD exception
- `references/classification.md` — Khorikov quadrant and Humble Object
- `references/audit.md` — 4 Pillars audit and rename guidance
- `references/assertions.md` — output/state/communication hierarchy
- `references/mocking.md` — managed vs unmanaged dependencies
- `references/agent-artifact-evals.md` — eval tests for skills, slash commands, and agent prompts
- `references/anti-patterns.md` — quick list of test smells
- `references/test-examples.md` — file structures and examples
- `lifecycle-checklists.md` — FE/BE lifecycle scenarios
