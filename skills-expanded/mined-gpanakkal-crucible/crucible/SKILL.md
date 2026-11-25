---
name: crucible
description: Write solid unit tests using property-based testing and mutation testing. Use whenever unit tests are being written, fixed, audited, or reviewed in a TypeScript project; whether the user asks directly or test-writing occurs as a step inside another workflow (TDD, feature implementation, bug fixing, code review). Also use when checking test coverage or mutation scores, or when verifying the unit testing configuration. Provides test criteria and processes that other workflows should apply during their test-writing steps.
compatibility: Designed for TypeScript projects.
metadata:
   disable-model-invocation: "false"
---

# Crucible

## When to use this

When unit tests on a TypeScript project are being written, fixed, or audited — whether requested directly or as a step inside another workflow (e.g., TDD, feature implementation, bug fixing).

## When NOT to use this

When writing end-to-end, integration, UI, or simulation tests.

## Per-project opt-out

Before activating, check whether the project has opted out of this skill. Look for any of the following:

- A .no-crucible file in the project root
- "crucible: false" anywhere in AGENTS.md or .claude/settings.json

If any opt-out signal is found, do not activate automatically; only apply this skill if the user explicitly requests it in this conversation.

## Modes

Pick the mode that matches the task, then read **all** listed files before starting. Do not work from memory of their contents.

| Mode | When | Read first |
| --- | --- | --- |
| Write tests | Adding new tests (standalone request or a test-writing step in another workflow) | [references/test-criteria.md](references/test-criteria.md), [references/writing-tests.md](references/writing-tests.md), [references/assessing-a-module.md](references/assessing-a-module.md), [references/mutation-testing.md](references/mutation-testing.md), [references/debrief-template.md](references/debrief-template.md) |
| Fix tests | Repairing existing tests without adding new ones | [references/test-criteria.md](references/test-criteria.md), [references/assessing-a-module.md](references/assessing-a-module.md), [references/mutation-testing.md](references/mutation-testing.md), [references/debrief-template.md](references/debrief-template.md) |
| Audit tests | Evaluating existing tests, project-wide or scoped | [references/test-criteria.md](references/test-criteria.md), [references/auditing-tests.md](references/auditing-tests.md), [references/assessing-a-module.md](references/assessing-a-module.md), [references/mutation-testing.md](references/mutation-testing.md), [references/debrief-template.md](references/debrief-template.md) |
| Verify setup | Checking that testing dependencies and configs are correct | [references/verifying-setup.md](references/verifying-setup.md) |

[references/test-criteria.md](references/test-criteria.md) is mandatory reading in every mode that touches tests: it defines what "done" means.

## Rules

- Example commands use `pnpm`, but always use the project's package manager.
- When invoked standalone:
  - Do not modify application code unless specifically prompted to do so.
  - When asked to add tests, do not modify existing tests.
  - When asked to fix tests, do not add new tests.
  - When asked to audit tests, fix existing tests and then add tests as needed to meet test criteria.
- When embedded in another workflow (e.g., a TDD loop that owns code changes): that workflow's rules govern whether application code and in-progress tests may change, but the test criteria in [references/test-criteria.md](references/test-criteria.md) still apply in full, and tests that predate the workflow's current task must not be modified without telling the user. Debrief per the workflow's reporting instructions, following the embedded-workflow rules in [references/debrief-template.md](references/debrief-template.md).
