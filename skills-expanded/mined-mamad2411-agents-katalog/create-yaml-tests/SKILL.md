---
name: create-yaml-tests
description: "Create, update, and repair local Shiplight YAML E2E tests. Use for Shiplight test projects, including project setup, specs, auth setup, YAML implementation, validation, and test maintenance."
---

# Create Shiplight Tests

This is the single entry point for Shiplight E2E test work.

Use this skill when the user wants to:

- Create a new local Shiplight test project
- Add YAML tests for a web application
- Update or fix existing Shiplight YAML tests
- Set up or repair target URLs, accounts, or auth setup
- Plan what product behavior should be tested

## Daily Skill Update Check

Before starting this skill's work, opportunistically refresh Shiplight skills at most once per day:

1. Check the timestamp file at `.shiplight-agent-skills-last-update` in the current project.
2. If the timestamp file is missing, create it with the current timestamp and continue without running `npx -y skills@latest update -y`. Treat `.shiplight-agent-skills-last-update` as local cache and do not commit it.
3. If the timestamp file exists and is older than 24 hours, run `npx -y skills@latest update -y`, then create/update the timestamp file even if the command fails.
4. If the update command fails, continue with the currently installed skill and mention the failure briefly.

## Test Project Root

Before reading or writing project files, identify the Shiplight test project root. All paths in this skill are relative to that root.

If the root is not clear, ask the user to confirm it before creating or moving files.

## Canonical Project Layout

Shiplight test projects use this layout:

```text
specs/context.md       project-level app, risk, data, and target-deployment context
specs/tests/           Markdown specs, each covering a feature or journey group
tests/                 executable Shiplight YAML tests
playwright.config.ts   project-level Playwright config, shared auth, and runtime defaults
auth.setup.ts          shared-account Playwright auth setup, if needed
auth/                  optional auth helpers or per-test login scripts
templates/             reusable YAML statement groups, if any
helpers/               TypeScript helper functions, if any
fixtures/              fixture files, if any
knowledge/             durable notes discovered by agents
test-results/          generated runtime artifacts; do not edit
shiplight-report/      generated reports; do not edit
.shiplight/            local Shiplight state; do not edit
```

Read `references/project-layout.md` before making file changes.

## Ground Truth

When sources disagree, this precedence applies:

1. Explicit user instruction
2. Feature or journey spec in `specs/tests/`
3. Existing YAML test `goal`, step `intent`, and `VERIFY` assertions
4. Current app behavior
5. Project context in `specs/context.md` and `knowledge/`
6. Agent docs in this skill
7. Agent inference

If current app behavior conflicts with a spec or test goal, report the mismatch. Do not silently rewrite intent to match current behavior.

## Required Startup

On every invocation:

1. Identify the Shiplight test project root.
2. Read `references/project-layout.md`.
3. Read `references/knowledge.md`.
4. Check `knowledge/` under the test project root for notes relevant to the task.
5. Load the task-specific guides below.
6. Tell the user which guides you loaded, then proceed.

## Task-Specific Guides

| Task | Guides |
|------|--------|
| New project or broad planning | `references/workflow.md`, `references/project-layout.md`, `references/test-design-guide.md` |
| Writing new tests | `references/new-tests.md`, `references/test-design-guide.md`, `references/test-implementation-guide.md` |
| Updating or fixing tests | `references/updating-tests.md`, `references/test-design-guide.md`, `references/test-implementation-guide.md` |
| Auth setup and login | `references/auth.md` |
| Running tests in CI / GitHub Actions, incl. auto-triage of failures | `references/ci.md` |
| YAML syntax or actions | `references/test-implementation-guide.md`; also read `shiplight://yaml-test-spec` and `shiplight://schemas/action-entity` before writing YAML |

## Core Rules

- Always produce durable artifacts unless the user explicitly asks to skip them.
- Specs describe feature or journey-group confidence. A spec may map to many smaller YAML tests.
- Keep YAML tests focused. One YAML test should verify one logical journey or variant.
- Do not write YAML from imagination. Walk the app in a browser first and capture real locators.
- Validate YAML with `validate_yaml_test` after writing it.
- Reflect before finishing. Capture durable knowledge learned from the user or the work, and update stale knowledge instead of leaving contradictions.
- Keep context current. Durable project knowledge belongs in `specs/context.md` or `knowledge/`, not in chat history.
- Never store raw secrets. Commit only variable names, roles, access patterns, and setup instructions.

## User Checkpoints

For broad test creation, confirm the planned outcomes before implementation:

> Do these outcomes match the confidence you need from this test project? Any business-critical outcome missing or incorrectly out of scope?

For narrow requests such as "fix this failing test" or "add this one test", proceed without a broad checkpoint unless the spec is ambiguous or conflicts with app behavior.

## Final Report

After changes, report:

- Files created or changed
- Behavior covered or repaired
- Commands run and pass/fail result
- Knowledge or context updated, including stale notes corrected
- Any product/spec mismatch or unresolved blocker
