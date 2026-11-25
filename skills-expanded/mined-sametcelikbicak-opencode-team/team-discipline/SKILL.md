---
name: team-discipline
description: >-
  Use on every coding task to apply the team's default engineering discipline:
  understand before changing, YAGNI, the smallest complete change, test-first,
  evidence before claims, and a short report. This is default behavior, not an
  optional mode.
---

# Engineering Discipline

Default behavior for every agent that writes or reviews code. The goal is the smallest change that fully solves the task, not the most code.

The best code is the code never written. But lazy means efficient, not careless: a small change in the wrong place is a second bug.

## When to use

- Any task that writes, fixes, refactors, reviews or chooses a dependency.
- Any build, QA, security or docs stage that touches source code.
- Not only when the user says "simple", "minimal" or "YAGNI". This is the baseline.

The stage playbook (`team-build`) wins on TDD mechanics. This skill sets the default standard every role applies.

## 1. Understand before changing

Read the task and the code it touches. Trace the real flow end to end before choosing an approach.

List the blast radius:

- callers of every function you change;
- tests, fixtures and snapshots that depend on the behavior;
- config, exports, types and public interfaces;
- data the change could destroy or expose;
- callers that would stop working.

That list is the scope. Extra features are not scope.

If the request is ambiguous in a way that changes the design, ask one short question. Do not guess and rewrite later.

## 2. The ladder

Stop at the first rung that holds:

1. Does this need to exist at all? Skip features, options and flexibility nobody asked for.
2. Does it already exist in this codebase? Reuse the helper, util, component or pattern.
3. Does the standard library already do this? Use it.
4. Does a native platform feature cover it? Use it.
5. Does an already-installed dependency solve it? Use it.
6. Can it be one clear line? Make it one line.
7. Only then: write the minimum code that works.

The ladder runs after you understand the problem, not instead of it.

## 3. The smallest complete change

- No abstraction, wrapper, type conversion, option, config or "for later" code nobody asked for.
- No new dependency if it can be avoided.
- No boilerplate nobody asked for.
- Deletion beats addition. Boring beats clever. Fewest files possible.
- Keep the structure the codebase already has: its layers, interfaces and conventions.
- Keep values in the form the platform already gives you.
- Comment only the *why* the code cannot show, in one line.

A change is complete only when every part the task needs is done: callers, tests, fixtures, config and docs your change breaks or requires.

### Bug fixes

A report names a symptom. Find the root cause, grep every caller of the function you touch, and fix the shared function once. One guard there is smaller than one guard per caller, and patching only the named path leaves a sibling caller broken.

### Preserve what protects users

Code you move, merge or rewrite keeps its input validation, error handling and access checks.

## 4. Test-first

For new behavior:

1. Write the smallest test that fails for the right reason.
2. Run it and confirm it fails.
3. Write the minimum code to pass.
4. Run it and confirm it passes.
5. Refactor with the test green.

Non-trivial logic leaves one runnable check behind: the smallest thing that fails if the logic breaks. That can be a small test file, an assert-based self-check or a demo script. No framework, fixtures or test pyramid is required for a small change.

Trivial one-liners need no test.

Test the behavior at the boundary, not the implementation detail. Keep tests deterministic. Mock only what you do not own (network, clock, filesystem, third-party service).

## 5. Evidence before claims

- Run the command before saying it passes.
- Quote the real output, not a paraphrase.
- If it was not run, write "not run". Never invent command output, metrics or test results.
- A claim of "fixed" needs the failing case to pass now.
- Do not claim a stage is complete while a requested specialist is missing, failed or cancelled.

## 6. Design gate

For a large or risky change, state the plan before editing:

- the files you will touch;
- the approach and the alternative you rejected;
- how you will verify it;
- the rollback path if it changes data or deployment.

Ask for approval when the change is destructive, crosses a trust boundary, or the request has real ambiguity. Otherwise proceed and report.

## 7. Report

End with a short report a busy human can read once:

- what changed and why;
- what now works, concretely;
- the evidence (command and result);
- known gaps, shortcuts and risks;
- one concrete next action when something remains.

One or two lines for what you skipped or did not check, and any risk the user must know.

## Not lazy about

Never cut these to save code:

- input validation at trust boundaries;
- error handling that prevents data loss;
- security and authorization;
- accessibility;
- calibration that real hardware needs;
- anything the user explicitly requested.

## Deliberate shortcuts

A shortcut with a known ceiling gets a code comment in this form:

```text
shortcut: <the limit>, <when to upgrade>
```

Example: `shortcut: global lock, replace with per-key locks when writes exceed ~100/s`.

An unmarked shortcut is a hidden bug.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Patching the reported caller only | Grep every caller and fix the shared function. |
| Building a config option nobody asked for | Delete it; add it when a real caller needs it. |
| Adding a dependency for a few lines | Use the standard library or an installed package. |
| Writing code before tracing the flow | Read the callers and tests first. |
| Claiming tests pass without running them | Run them and quote the output, or write "not run". |
| A test that passes before the fix | Make it fail for the right reason first. |
| Hiding a known limit | Mark it with `shortcut:` and name the upgrade path. |
| Rewriting unrelated code in the same change | Keep the diff to the task. |

## Relationship to other skills

- `team-build` — red-green-refactor, seams and the test pyramid for the build stage.
- `team-memory` — record durable decisions and lessons, not transcripts.
- Stage playbooks — the role's methodology; this skill is the default standard on top of it.
