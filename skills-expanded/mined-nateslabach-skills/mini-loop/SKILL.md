---
name: mini-loop
description: Autonomous build-verify-fix loop that runs until an explicit Definition of Done passes. Use when named (mini-loop) or when the user says exactly "run a loop".
---

# mini-loop

Run any task to completion without mid-loop confirmation. Exit only when every Definition of Done item passes.

Pairs with **just-stop**: this skill keeps you looping until DoD passes; just-stop blocks optional polish after that.

## When to use

- User names this skill (`mini-loop`)
- User says exactly: `run a loop`
- Any use case with verifiable exit criteria: greenfield apps, features, refactors, docs, scripts, migrations

## Core principles

1. **DoD is the exit gate** — no "mostly done," no stopping on vibes
2. **Verify after every meaningful change** — don't batch unverified work
3. **Infer verification** — derive checks from the stack/repo; don't wait for the user to list commands
4. **Fast start, ask once** — if goal or DoD is missing/mushy, ask once for only what's missing, then lock and go. No mid-loop confirmation after that (except secrets, credentials, or irreversible destructive action)
5. **Fix forward** — errors and incomplete features re-enter the loop immediately

## Input Brief

Users should attach what they can. Minimum useful prompt:

```
Goal: [what to produce]
Scope: [in / out — optional]
Definition of Done:
- [observable check]
- [observable check]
Constraints: [stack, design, don't-touch — optional]
```

Verify commands are optional — the agent infers them.

## Process

### 0. Preflight (once)

From the prompt, check for:

- **Goal** — clear enough to build without guessing product intent
- **DoD** — explicit, observable checklist (or concrete enough to write one without inventing features)

If both are clear → lock immediately and start.

If either is missing or mushy → **ask once**, only for the gaps. Prefer a short checklist of questions over an interview. Do not ask for verify commands, stack preference, or polish details unless ambiguity would change the build.

After the user answers (or if they say "just go") → lock goal + DoD + scope/constraints as stated, then enter the loop. No further scope renegotiation mid-loop.

### 1. Lock the Definition of Done

Write the locked DoD as an explicit checklist. Every item must be observable (command succeeds, behavior works, artifact exists, UI state looks right). Prefer concrete checks over subjective ones.

Track it as a live checklist. Do not invent extra scope beyond what DoD requires.

### 2. Infer verification

From the repo/stack, pick the cheapest reliable checks that prove DoD items. Examples:

- App/package: install → build → start/dev (or test) as appropriate
- Library/script: typecheck/test/run the entrypoint
- Docs/content: file exists, links resolve, required sections present
- Refactor: existing tests/build still pass; targeted behavior still works

Prefer project-native commands (`package.json` scripts, Makefile, etc.) over ad-hoc ones. If multiple stacks are possible, choose what can be run and verified locally with the least friction.

### 3. Execute the loop

```
while any DoD item is unmet:
  1. Implement the next incomplete item
  2. Run inferred verification
  3. If fail → diagnose, fix, go to 2
  4. If pass → mark item done, continue
```

Rules inside the loop:

- Work autonomously. Do not ask for confirmation between steps.
- After each change that could break something, re-verify — don't accumulate debt.
- Incomplete features count as failures. Re-enter the loop.
- Stay on the critical path to DoD. No polish beyond what DoD demands unless polish *is* a DoD item.

### 4. Exit

Stop only when every DoD item passes verification.

Then give:

1. **Summary** — what shipped, what's verified
2. **How to run / use** — exact commands or next steps
3. **DoD checklist** — each item marked passed

## Anti-patterns

- Starting the loop with a mushy goal/DoD instead of asking once
- Turning preflight into a multi-round intake
- Stopping because "it should work" without running verification
- Asking "should I continue?" while DoD items remain open
- Expanding scope past DoD mid-loop
- Claiming done when build/dev/tests still fail
