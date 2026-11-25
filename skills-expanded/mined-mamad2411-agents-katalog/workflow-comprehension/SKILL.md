---
name: workflow-comprehension
description: >-
  Optional local comprehension interview after AI review. Dev checks out the
  work branch, tests and previews the PR, then runs this skill in a local
  Claude Code session — no routine, no GitHub label changes. Skip by merging
  the PR and closing the issue. Use when the user runs /workflow-comprehension
  or wants to verify understanding of an issue's changes before merge.
disable-model-invocation: true
metadata:
  internal: true
---

# Workflow: Comprehension (local, optional)

Verify the **developer** understands what was built — behavior, code structure, and how to maintain it — **before merging the PR**.

**Optional.** No routine fires this skill. If the dev does not want a comprehension session, they **merge the PR and close the issue** — workflow complete.

## When to use

| Path | Action |
|------|--------|
| **Comprehension** | Issue has `workflow:human-review` → checkout `work_branch` locally → test/preview → run **`/workflow-comprehension`** (optionally with issue number) |
| **Skip** | Merge PR on GitHub → close issue → done |

Adapted from ai-workflow **workflow-comprehension** — local session only (no handoff commits, no labels).

## Preconditions

1. Issue has label **`workflow:human-review`** (AI review finished).
2. Branch **`workflow/issue-{n}`** with `workflow/issues/{n}/` containing requirements, implement-handoff, review-report, and `work_branch` / `base_branch` in `state.json`.
3. Dev has **`work_branch` checked out locally** (or checks out as first step).
4. Dev has run tests and previewed the change locally (recommended before starting).

If preconditions fail, explain what's missing and stop. Do not change labels or handoff files on the branch.

## Start sequence

1. **Resolve issue** — from user message (`issue #42`, URL) or ask.
2. **Fetch handoff** — checkout `workflow/issue-{n}`; read `workflow/issues/{n}/` per [handoff-format.md](../workflow-routines/handoff-format.md).
3. **Confirm branch** — `work_branch` and `base_branch` from `state.json`.
4. **Local verification** — encourage dev to have already run PROJECT.md test commands and previewed the feature; offer to run tests now if not done.
5. **Read context** — handoff files, `workflow/PROJECT.md`, gotchas, `git diff`, key changed files.
6. Enter **start** mode (interview below).

**No GitHub writes** — no session comment, no label swap, no handoff commits.

## Interview style

Ask **one question at a time** — free text or multiple choice (`A`/`B`/`C`/`D`). Like clarify, but you **grade each answer** before asking the next.

**Cover these dimensions** across the interview (adapt to the diff):

| Dimension | What to probe |
|-----------|---------------|
| **Functionality** | What changed for users/systems, edge cases, error behavior |
| **Code** | Where the change lives, how data/control flows, key design choices |
| **Maintenance** | Where to extend or fix later, what tests guard this, what to watch for |

**Question count is not fixed.** A small fix may need 3–4 questions; a multi-module feature may need 8+. Stop when all three dimensions are adequately demonstrated — not after a quota.

Use what the dev saw during local test/preview to ask grounded questions (e.g. "You ran X — what happens if Y?").

## What NOT to ask

- Trivia: port numbers, exact env var names, line numbers, memorized identifiers
- Facts irrelevant to understanding the change
- Trick questions or framework minutiae unless central to the diff

## Modes

| Situation | Mode |
|-----------|------|
| First entry, or `ready` / `retake` after fail | **start** |
| User answers the pending question (not `skip-comprehension`, `ready`, `retake`, `done`) | **continue** |
| User says `skip-comprehension` (alias: `take the shame`) | **shame** |
| Pass or skip recorded; user says `done` / `merge` | **close** |

## Mode: start

1. Track attempt number in **session memory** (increment on `ready` / `retake`).
2. Read diff and artifacts. Identify probe areas for functionality, code, maintenance.
3. Keep in-session **`comprehension-test.md`** log (template below) — **not** written to repo or GitHub.
4. Ask **question 1** only — free text or multiple choice.

**Stop.** Wait for the answer.

## Mode: continue

1. Read the user's answer to the **last pending question**.
2. Grade: **correct**, **partial**, or **incorrect** with brief rationale. Append to in-session log.
3. Decide next action:

### More probing needed

- Ask the **next question** (one only). Prefer weak areas or dimensions not yet demonstrated.

**Stop.** Wait for the answer.

### Sufficient understanding demonstrated

- Record: `PASS — demonstrated understanding of {areas}`.
- Summarize what they demonstrated well.
- Tell dev: comprehension complete — **`gh pr ready`** when inviting reviewers, then merge and close the issue.
- Offer **`done`** to end the session.

**Stop.**

### Critical gaps remain

Only fail after fair assessment across all three dimensions:

- Record: `FAIL — gaps: {list with file pointers}`.
- Offer:
  - **`ready`** / **`retake`** — new attempt after reviewing the code locally
  - **`skip-comprehension`** — proceed without passing (waives this optional gate)
  - Review the branch / re-run tests before retake

**Stop.** Do not ask a new question in the same turn as declaring FAIL.

## Mode: shame

Triggered by **`skip-comprehension`** (alias: `take the shame`).

1. Append `**SKIPPED — continued without passing**` to in-session log.
2. Brief, playful acknowledgment (1–2 emojis max).
3. Tell dev: optional gate waived — **`gh pr ready`** when inviting reviewers, then merge and close the issue.

**Stop.**

## Mode: close

User sends **`done`**, **`merge`**, or confirms they are finished.

1. Present one-line summary (PASS / SKIP / attempt count).
2. Remind: mark PR ready when inviting reviewers (`gh pr ready`), merge PR on GitHub, close linked issue.
3. **Stop** — no further workflow phases in this repo.

## comprehension-test.md template (session memory only)

```markdown
# Comprehension Test: issue-{n}

**Branch:** {work_branch} · **Style:** one question at a time

## Attempt {n} — {ISO date}

### Probe plan
- Functionality: ...
- Code: ...
- Maintenance: ...

### Q1 — {free text | multiple choice} [{dimension}]
{question}

**Answer:** (pending | ...)
**Grade:** (pending | correct | partial | incorrect)
**Rationale:** ...
```

## Writable locations

| Location | When |
|----------|------|
| Session memory | Interview log, grades, pass/skip state |
| `work_branch` | **Never** — comprehension does not change code |
| GitHub | **Never** |

## Hard rules

- **Never** modify application source code.
- **Never** commit handoff files or change workflow labels.
- **Never** ask trivia (ports, line numbers, exact variable names).
- **Never** dump all questions at once — **one question per turn**.
- **Never** reuse the same questions across attempts.
- Be fair but rigorous — partial credit for directionally right answers; follow up when vague.
- Comprehension is **optional** — never block merge; skipping is always valid.
