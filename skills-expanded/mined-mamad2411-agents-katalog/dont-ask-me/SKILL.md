---
name: dont-ask-me
description: No-ask session mode — replace every /ask-me with /follow-your-suggestion
argument-hint: "[scope]"
related:
  - ask-me
  - continue
  - follow-your-suggestion
  - ask-project-requirement
  - suggest-next-action
  - loop-until-complete
  - ship

---

## Goal

Enable a "no-ask" mode from invocation until the end of the session — never use `/ask-me`, `ask_user_question`, or any selection-style prompts, even when `global_rules.md` or other skills instruct `/ask-me`. Replace them with `/follow-your-suggestion` and work incrementally and safely without skipping steps, until the job is fully complete via `/loop-until-complete`

## Scope

- Use when the user says `dont-ask-me`, `dont ask me`, `do not ask`, `no need to ask`, `proceed`, or `no ask`, or when a workflow such as `/ship` enables this mode in `dont-ask-me` mode
- Works as a session mode: once enabled it applies to every instruction in the same session, including `global_rules.md` and any skills that reference `/ask-me`
- Not a store of requirements or preferences — if a prompt contains a question that must be answered before starting, answer it with a safe default via `/follow-your-suggestion` instead of asking

## Execute

### 1. Activate Session Mode

> Goal: turn on no-ask mode for the rest of the session

1. Record that this session is in `dont-ask-me` mode from now until the session ends
2. Set a temporary rule: everywhere `global_rules.md`, a skill, or a workflow says to run `/ask-me` or `ask_user_question` → replace it immediately with `/follow-your-suggestion`
3. If a prompt has an outstanding question → answer it with a safe default and record the decision; do not ask back

### 2. Evaluate Context

> Goal: confirm it is safe to proceed

1. Read context, memory, project conventions, and `AGENTS.md`
2. Check that the choice has a clear and safe outcome
3. If still unclear → pick a safe default via `/follow-your-suggestion` instead of `/ask-me` or `/ask-project-requirement`

### 3. Pick Safe Default

> Goal: choose the simplest and safest option

1. Pick the option with the lowest risk that is reversible
2. Ground the choice in best practices and project conventions
3. If several options are equal, take the simplest and most reversible one

### 4. Proceed Step By Step

> Goal: work incrementally and safely without skipping steps

1. Proceed one step at a time in order; never skip a step the workflow defines
2. Change one small point at a time and check the result before continuing — never bundle several risky changes in one round
3. Do not use `ask_user_question`, do not show selection prompts, do not call `/ask-me` or `/ask-again`
4. Use `/follow-your-suggestion` to apply the suggestion instead of asking for confirmation
5. Record every decision in the report so it stays traceable

### 5. Loop Until Complete

> Goal: repeat until the work is fully complete

1. Run `/loop-until-complete` to re-check until the criteria pass or a good-enough point is reached
2. If a problem appears along the way → fix it point by point with `/resolve-errors` and keep looping; do not stop mid-way to ask
3. Stop only when fully complete, when hitting max iterations, or when a genuinely dangerous action is found

### 6. Report

> Goal: report results and next steps

1. Summarize what was done, why nothing was asked, and which defaults were chosen
2. State that `dont-ask-me` mode is still active for the next tasks in the session
3. Run `/suggest-next-action` to recommend the next step without asking

## Rules

### 1. Session Override

- While `dont-ask-me` is active → override every `/ask-me` and `ask_user_question` in `global_rules.md` and all skills until the session ends
- `/ask-me`, `/ask-again`, `/ask-project-requirement`, and `pick-bestest` calls made by other workflows → run `/follow-your-suggestion` with a safe default instead
- The user can always cancel the mode with an explicit command such as "start asking again" or "cancel dont-ask-me"

### 2. No Prompt Discipline

- Never use `ask_user_question` while in `dont-ask-me` mode
- Never show prompts offering choices
- Never call `/follow-your-suggestion` to ask for confirmation — use it only to apply suggestions
- `/continue` and `/loop-until-complete` may be used immediately as normal

### 3. Safe Stepwise Execution

- Work incrementally, one step at a time in workflow order — never skip steps
- Fix incrementally, point by point, and verify before continuing
- Never take dangerous or irreversible actions — pick the safest path and report instead of asking

### 4. Uncertainty Handling

- If doubt arises mid-work → stop that step, report the status, then choose a safe default to continue with other parts
- If no safe option exists at all → stop and report without asking

## Expected Outcome

- No `/ask-me` or user-facing prompts at all until the session ends
- Every point that once required a question is decided via `/follow-your-suggestion` with a traceable safe default
- Work proceeds safely step by step, never skipping steps, and loops until complete via `/loop-until-complete`
- Fewer unnecessary questions without added risk, and the user never has to answer repeated questions
