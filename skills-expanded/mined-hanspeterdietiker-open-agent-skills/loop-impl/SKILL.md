---
name: loop-impl
description: Use when the user asks to implement a whole project, epic or multi-ticket plan across resumable sessions, set up or resume an implementation loop, continue "the loop", or delegate tickets to workers — implementar projeto ticket a ticket, loop de implementação, retomar ciclo, épico com vários tickets.
license: MIT
metadata:
  author: hanspeterdietiker
  sub-skills: clean-code (required), orchestration (optional, external), harness-loop (optional background)
---

# Implementation Loop

## Overview

A multi-ticket project runs as a **resumable loop** recorded in a control note. Each cycle implements ONE ticket, proves the result with evidence, and **stops at the gate**. Whoever resumes (you tomorrow, another agent, a worker) needs only the note and git.

**Principle:** the loop finishes tickets, not sessions. A ticket closes only with evidence + an approved gate; without both it is not done, however done it looks.

Optional conceptual background: the `harness-loop` skill (Loop × Harness separation). This skill is the execution template.

## When to Use

- "Implement project/epic X", "do the tickets in the plan", "resume the loop".
- Work that won't fit in one session or will be continued by another agent/worker.

**Don't use** for an isolated single-ticket change — just implement it.

## Step 0 — User decisions (before any code)

Ask in a single message, showing the suggested default for each item, and record the answers in the note under "User decisions — <date>". The project may already answer some of them in CLAUDE.md/AGENTS.md, memories, or a previous loop note: if so, present that answer for confirmation. No answer, no code. "Go with the defaults" is an answer: record the defaults.

| Decision | Suggested default |
| --- | --- |
| **Gate** per ticket | Coordinator review of the full diff; alternative: external review brought by the user |
| **Branches** | One per ticket, stacked on the previous one; one PR per ticket into the project's integration branch |
| **Commits** | Only with user authorization (asked per ticket, unless a standing authorization is recorded here) |
| **Execution** | Inline, or workers via `/orchestration`; record who implements and who reviews |
| **Pace** | Stop at the end of each ticket |
| **Extra records** | Deploy checklist, sprint report — as the project requires |

## Step 1 — Control note

Create the note from `template.md` (in this folder). Location: the project's convention (e.g. a `loops/` folder in the docs/Obsidian vault mentioned in CLAUDE.md); with no convention, `docs/loops/Implementation <project>.md`. Write the note in the project's documentation language. Fill the verification table with the project's REAL commands (read CLAUDE.md, package.json, pyproject, etc.) and the "Project rules in the cycle" section with the per-ticket obligations from the project's instructions (final builds, deploy checklist, report, comment language...).

**Resuming without a note** (missing or inconsistent with git): rebuild the state from git and the plan in a "Reconstruction cycle", show it to the user, and only then proceed.

## The cycle (one ticket at a time)

1. **Context:** reread the project instructions, the plan, and the note. Check `git status`/`git log` against the last recorded cycle; on divergence the code wins — fix the note.
2. **Selection:** the first pending ticket whose dependencies have an approved gate. Extract tasks, DoD, and tests; state which go into this increment.
3. **Branch** per the recorded decision (when resuming, use the existing one).
4. **Implement** the increment, with tests for the changed behavior, applying `clean-code` (see "With /clean-code"). Scope is locked: nothing beyond the ticket without user confirmation.
5. **Verify:** run the table. Record command, directory, result, and exit code. A command not run, a missing tool, or an environmental failure is **pending**, never a success.
6. **Self-review the full diff** before asking to commit: security, data isolation, business rules, duplication, conventions, and the `clean-code` checklist. Fix and re-verify whatever was affected. This is NOT the gate: the gate is the formal decision in step 8, with a recorded verdict.
7. **Commit** (with authorization) and record the full hash in the note.
8. **Close:** assemble the gate package (commits, commands and results, evidence for each DoD criterion, limitations). **STOP** and hand it to the user.
9. **Record:** update the note at the end of EVERY cycle, including interrupted ones, ending with the **exact next step**.

## Stop rules

| Situation | Action |
| --- | --- |
| Ticket ready for the gate | Stop. Do not start the next ticket. |
| Same verification still failing after 3 fix attempts (switching approach does not reset the count) | Stop; record error, attempts, and hypothesis; state `blocked`; tell the user. Never weaken or skip the test. |
| Business rule missing or ambiguous | Ask. Don't invent. |
| Context running out | Close at a clean point with the note updated. |
| Gate rejected | New fix cycle on the SAME ticket. |

## With /orchestration

If the decision is to use workers: **REQUIRED SUB-SKILL:** use `orchestration` to dispatch, wait for, and read each delivery. You are the coordinator: write the ticket spec (record its path in the note) with the `clean-code` requirement in its Constraints, review the worker's diff as in step 6, and decide the gate. A worker never marks a ticket done; only the coordinator does, after review. Record run/task/dispatch IDs in the note.

Parallelism: tickets with no dependency on each other may go to different workers at the same time, each with its own cycle and gate. A ticket is dispatched only when all its dependencies have an approved gate.

## With /clean-code

Every implementation: **REQUIRED SUB-SKILL:** use `clean-code` while writing the code (step 4) and when self-reviewing the diff (step 6), whether the implementer is you or a worker. When the execution is via `/orchestration`, the ticket spec carries the `clean-code` checklist under Constraints and the coordinator checks it in the worker's diff before the gate. Record in the gate package the checklist result and any justified exception.

Scope and precedence: `clean-code` is a set of design heuristics, not a license to refactor beyond the ticket or change behavior. The project's instructions (CLAUDE.md/AGENTS.md) win on conflict — e.g., when the project requires comments explaining the *why*, keep them and remove only redundant or noise comments. Apply it to the code the ticket touches, without reformatting unrelated code.

Checklist (in the diff of each ticket):

- [ ] **Size & responsibility:** each new or changed function does one thing at one level of abstraction; long functions (≈ 20+ lines) are split or justified.
- [ ] **Naming:** intention-revealing, searchable names (nouns for classes, verbs for methods); no disinformation.
- [ ] **Comments:** no redundant or noise comments; the *why* comments required by the project stay.
- [ ] **Arguments:** 0–2 per function; 3+ only with justification (prefer a parameter object).
- [ ] **Error handling:** domain exceptions/errors per the project, not return codes; no returning or passing `null` where the language/project offers a better alternative.
- [ ] **Tests:** a focused test that fails without the change exists for each changed behavior (F.I.R.S.T.).
- [ ] **No smells:** no duplication, needless complexity, hidden side effects, or Law of Demeter chains introduced by the diff.

## Rationalizations vs. reality

| Thought | Reality |
| --- | --- |
| "The user is in a hurry, I'll do everything on one branch and commit at the end" | Hurry doesn't change the gate. Offer the Step 0 options; record what the user decides. |
| "Tests pass, I'll move on to the next ticket" | Tests ≠ gate. Stop and hand over the package. |
| "They asked for a commit, so everything is authorized" | Only what's recorded in Step 0 counts. An ambiguous request ("commit at the end") authorizes only that; ask once about its scope and record it. Push and PR are never implied. |
| "The build failed because of the environment, I'll call it OK" | Pending. Record it as such. |
| "This extra requirement is obvious, I'll include it" | Scope is locked. Ask. |
| "It works, clean-code is optional for this ticket" | `clean-code` is required in every implementation. Run the checklist on the diff and record the result. |
| "While I'm here I'll clean up the whole file" | `clean-code` applies to what the ticket touches. Refactoring outside the scope needs user confirmation. |

## Red flags — stop

- Starting ticket N+1 without ticket N's gate.
- Writing "done" without the verification table filled in.
- Handing over the gate package without the `clean-code` checklist result.
- Control note out of date relative to git.

## Créditos / Credits

- **Autor / Author:** [hanspeterdietiker](https://github.com/hanspeterdietiker) — skill e [`template.md`](template.md).

Sub-skills referenciadas / Referenced sub-skills:

| Sub-skill | Uso no loop / Role | Autor / Author | Onde obter / Where to get it |
| --- | --- | --- | --- |
| `clean-code` | Obrigatória nos passos 4 e 6 / Required in steps 4 and 6 | [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills/tree/main/skills/clean-code) (MIT), originalmente de [jackjin1997/ClawForge](https://github.com/jackjin1997/ClawForge) | [`../clean-code`](../clean-code/SKILL.md) neste repositório / in this repository |
| `orchestration` | Opcional, quando a execução é por workers / Optional, worker execution | [stablyai/orca](https://github.com/stablyai/orca) (MIT) | Externa; requer o app Orca / External; requires the Orca app: [`skills/orchestration`](https://github.com/stablyai/orca/tree/main/skills/orchestration) |
| `harness-loop` | Base conceitual opcional / Optional conceptual background | [hanspeterdietiker](https://github.com/hanspeterdietiker) | [`../harness-loop`](../harness-loop/SKILL.md) neste repositório / in this repository |
