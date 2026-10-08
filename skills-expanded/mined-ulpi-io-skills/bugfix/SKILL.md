---
name: bugfix
version: 4.0.0
description: |
  Fix a CONFIRMED bug at its root cause, smallest correct change only — reproduce before you touch code:
  write a failing reproducer, diagnose the first broken assumption in the data flow, load the matching
  framework reference and category playbook, apply the minimal fix, then verify the reproducer goes green
  and run the regression scope. Never writes fix code without a reproducer (or a documented reason one is
  impossible), never patches the symptom while the root cause stands, and never weakens a test to pass.
  Use when the user says "fix this bug", "fix the findings", "/bugfix", or asks to repair a confirmed defect.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
argument-hint: "[bug description or finding selector]"
arguments:
  - request
when_to_use: |
  Use when the task is to fix a confirmed defect, failing test, runtime error, or verified finding.
  Examples: "fix this bug", "fix finding #3", "fix the critical bugs", "repair the checkout crash",
  "make this failing test pass without regressions". Do NOT use to discover bugs (that's find-bugs),
  for behavior-neutral cleanup (that's code-simplify), or for feature work and speculative refactors —
  bugfix changes only what a confirmed root cause requires.
---

<EXTREMELY-IMPORTANT>
Every bugfix must follow a reproduce-diagnose-fix-verify loop.

Non-negotiable rules:
1. Do not write fix code before you have a reproducer or a clearly documented reason reproduction is impossible.
2. Fix the root cause, not the symptom.
3. Keep the change minimal and scoped to the bug.
4. Load the relevant framework reference before patching.
5. Load `references/bug-playbooks.md` after classifying the bug category.
6. Never weaken tests to make a fix pass.
</EXTREMELY-IMPORTANT>

# Bugfix

## Inputs

- `$request`: Optional bug description, failing scenario, or finding selector

## Goal

Resolve confirmed defects with the smallest correct change, backed by reproduction, diagnosis, targeted implementation, and regression checks.

## Step 0: Detect framework and load references

Before diagnosing the bug, identify the language and framework from the buggy file's imports, the project's dependency files, and the file extension:

| Signal                                      | Framework          | Reference File                    |
| ------------------------------------------- | ------------------ | --------------------------------- |
| `package.json` has `express`                | Express.js         | `references/expressjs.md`         |
| `package.json` has `react` + JSX/TSX files  | React              | `references/react.md`             |
| `package.json` has `react-native` or `expo` | React Native       | `references/react-native.md`      |
| `package.json` has `next`                   | Next.js            | `references/nextjs.md`            |
| `package.json` has `fastify`                | Fastify            | `references/fastify.md`           |
| `package.json` has `hono`                   | Hono               | `references/hono.md`              |
| `package.json` has `@remix-run/react`       | Remix              | `references/remix.md`             |
| `bun.lockb` or `bunfig.toml` present        | Bun                | `references/bun.md`               |
| `composer.json` has `laravel/framework`     | Laravel            | `references/laravel.md`           |
| `go.mod` present                            | Go                 | `references/golang.md`            |
| `go.mod` has `github.com/gin-gonic/gin`     | Go + Gin           | `references/go-gin.md`            |
| `go.mod` has `github.com/labstack/echo`     | Go + Echo          | `references/go-echo.md`           |
| `go.mod` has `github.com/gofiber/fiber`     | Go + Fiber         | `references/go-fiber.md`          |
| `.swift` files, `Package.swift`             | Swift              | `references/swift.md`             |
| `Cargo.toml` present, `.rs` files           | Rust               | `references/rust.md`              |
| `Cargo.toml` has `axum`                     | Rust + Axum        | `references/rust-axum.md`         |
| `Cargo.toml` has `actix-web`                | Rust + Actix Web   | `references/rust-actix.md`        |
| `Cargo.toml` has `rocket`                   | Rust + Rocket      | `references/rust-rocket.md`       |
| `.ts`/`.js` files (no specific framework)   | Node.js/TypeScript | `references/nodejs-typescript.md` |

Reference loading rules:

1. Always load the base language reference (e.g., `nodejs-typescript.md` for Node.js, `golang.md` for Go, `rust.md` for Rust).
2. Layer the framework-specific reference on top (e.g., read both `nodejs-typescript.md` and `expressjs.md` for Express; both `rust.md` and `rust-axum.md` for Axum).
3. React Native includes React -- read both `react.md` and `react-native.md`.
4. Next.js and Remix include React -- read both `react.md` and the framework file.
5. Go frameworks layer on Go -- read both `golang.md` and the framework file.
6. Rust frameworks layer on Rust -- read both `rust.md` and the framework file.
7. If the framework is unclear, fall back to the language-level reference.

**Success criteria**: The relevant language and framework references are loaded before diagnosis begins.

## Step 1: Parse and select the bug

Accept any of these inputs:

- verified `/find-bugs` findings
- user bug reports
- failing tests
- runtime crashes or build failures encountered during work

Extract:

- symptom
- trigger
- expected behavior
- likely file or subsystem
- severity if provided
- whether the task is a single bug or a batch

For `/find-bugs` output:

- extract only the findings the user asked to fix
- sort by severity and dependency
- group findings that touch the same file or function

If the request does not describe a confirmed bug, stop and clarify instead of patching blindly.

**Success criteria**: The bug scope is explicit enough to reproduce and fix.

## Step 2: Reproduce the bug first

Create or locate the smallest relevant test close to the affected code.

Required loop:

1. write a failing test for the exact bug scenario
2. run only that reproducer
3. confirm it fails for the expected reason
4. add closely related edge-case tests only if they directly protect the fix

If you cannot reproduce:

- check environment assumptions
- check exact triggering input
- check whether the code has already changed since the report
- check whether the bug is intermittent or concurrency-related
- if it still cannot be reproduced, stop and report what you tried

**Success criteria**: You have a failing reproducer, or a precise explanation of why reproduction is blocked.

## Step 3: Diagnose the root cause

Read the full local context:

- the affected function or module
- direct callers
- direct dependencies
- nearby tests
- relevant type definitions or contracts

Then:

1. trace data flow from entry point to failure point
2. identify the first broken assumption in the chain
3. map the blast radius:
   - callers
   - importers
   - dependent tests
   - public APIs or contracts affected
4. classify the bug category

Bug categories:

- Injection
- XSS
- Auth/AuthZ
- Null safety
- Race condition
- Boundary / off-by-one
- Async / Promise
- Type safety
- Resource leak
- Logic / business rule

After classification, read `references/bug-playbooks.md` and use the matching section.

**Success criteria**: You can state the root cause in one sentence and name the correct fix playbook.

## Step 4: Plan the minimal fix

Design the smallest change that fixes the root cause.

Check before editing:

- which files must change
- which callers or dependents are affected
- whether a public API or type changes
- whether the fix needs defense-in-depth
- whether the fix should be split by dependency order in a batch

For significant fixes, present a short plan before patching:

- bug
- root cause
- category / playbook
- blast radius
- reproducer
- intended files to change

**Success criteria**: The planned change is clearly smaller than a refactor and directly tied to the root cause.

## Step 5: Implement the fix

Implementation rules:

- patch the smallest surface that resolves the bug
- follow the category playbook from `references/bug-playbooks.md`
- follow the loaded framework reference
- do not mix in cleanup, style fixes, or feature work
- do not blindly copy the `/find-bugs` suggestion without checking the code

After each logical edit:

1. run the reproducer
2. confirm movement toward green
3. finish the dependency chain if the fix changes callers or contracts

**Success criteria**: The reproducer turns from failing to passing for the right reason.

## Step 6: Verify against regressions

After the reproducer is green:

1. run the affected test scope
2. run broader tests if the blast radius crosses module or package boundaries
3. run type checking or equivalent static verification
4. run the category-specific verification checklist from `references/bug-playbooks.md`
5. check for debug artifacts and accidental cleanup changes

If the fix causes unrelated failures, stop and re-diagnose before expanding scope.

**Success criteria**: The fix is green locally, category-specific checks pass, and no obvious regressions were introduced.

## Step 7: Handle multi-bug batches carefully

For multiple findings:

- group by file, function, and dependency
- fix dependent findings in order
- fix independent findings by severity
- run verification after each group, not only at the end
- if one fix resolves another finding, say so explicitly instead of pretending both required separate patches

**Success criteria**: Batch work remains reviewable and regressions are caught early.

## Step 8: Report the result

For each bug fixed, report:

- root cause
- category / playbook used
- files changed
- reproducer test
- verification completed
- any remaining risk or deferred follow-up

Include a summary with:

- bugs fixed
- tests added or updated
- files modified
- whether broader verification passed

If a bug was not fixed, say exactly why:

- could not reproduce
- insufficient information
- root cause is upstream
- fix requires architectural change beyond bugfix scope

**Success criteria**: Another engineer can understand what was fixed, why it was fixed that way, and how it was verified.

## Guardrails

- Do not fix without a reproducer unless you explicitly document why reproduction is impossible.
- Do not fix the symptom if the root cause is still present.
- Do not weaken or skip tests.
- Do not mix refactors with bugfixes.
- Do not convert bugfix work into feature work.
- Do not leave broad TODOs instead of finishing the actual fix.

## When To Load References

- Framework references:
  load the relevant language and framework docs in Step 0.
- `references/bug-playbooks.md`:
  load after classifying the bug in Step 3.

## Output Contract

Keep the response focused on execution and proof:

1. what bug is being fixed
2. what reproduced it
3. what root cause was found
4. what changed
5. how the fix was verified
