---
name: workflow-clarify
description: >-
  Clarification phase for GitHub-issue workflows. Creates the work branch first,
  persists ephemeral handoff files on branch, grills requirements one question at
  a time, posts short human issue comments, and sets workflow:implement. Use when
  a routine fires on workflow:start or for issue $0.
disable-model-invocation: true
metadata:
  internal: true
---

# Workflow: Clarify

Grill the plan before implementation. **No application code changes. No test runs.**

**First repo action after label swap:** create branch `workflow/issue-{n}` and init `workflow/issues/{n}/`. Commit handoff files on each Q&A turn. Issue comments are **short and human-only**.

On **`approve requirements`**, final handoff commit, post **approved requirements on the issue**, swap to `workflow:implement`, stop.

See [handoff-format.md](../workflow-routines/handoff-format.md), [state-schema.md](../workflow-routines/state-schema.md), [label-rules.md](../workflow-routines/label-rules.md).

## Read-only before branch exists

| File | Use |
|------|-----|
| `workflow/PROJECT.md` | Read from `base_branch` |
| `workflow/learnings/gotchas.md` | Skim |
| Application code | Read-only |

After branch exists, **only write** under `workflow/issues/{n}/` during clarify.

## Handoff files (on branch)

| File | Path |
|------|------|
| `state.json` | `workflow/issues/{n}/state.json` |
| `task.md` | `workflow/issues/{n}/task.md` |
| `language.md` | `workflow/issues/{n}/language.md` |
| `requirements.md` | `workflow/issues/{n}/requirements.md` |
| `adrs.md` | `workflow/issues/{n}/adrs.md` (optional) |

Branch is **source of truth** — commit after every update.

## Trigger modes

### A — Routine start (`workflow:start`)

Start sequence → grilling loop.

### B — Session continuation (`workflow:clarify`, same session)

Checkout branch, read `workflow/issues/{n}/`, continue.

### C — Manual (`/workflow-clarify {issue_number}`)

Same as A/B.

## Start sequence (mode A)

1. **Swap labels first** — `workflow:clarify`. Nothing else on GitHub before this.
2. **Read issue** — number, title, body, labels, URL.
3. **Verify init** — `workflow/PROJECT.md` on base branch; else stop → `/workflow-init`.
4. **Create work branch + initial handoff commit** (see handoff-format):
   - Branch `workflow/issue-{n}` from `base_branch` (default `main`)
   - Write `state.json` per [fixture](../workflow-routines/fixtures/state-example-clarify-start.json)
   - Write initial `task.md`, `language.md`, `requirements.md`
   - Commit + push
5. **Post session comment** — pick a **fresh phrasing** from handoff-format example bank (or invent one). **Must link** session + branch. Reference the issue topic when natural.

   Do **not** reuse the same clarify-start comment across issues.
6. Ask **first question**.

## Grilling loop

One question at a time with recommended answer. Explore codebase before asking.

## Domain modeling (`language.md`)

Update on branch when terms resolve — same format as `PROJECT.md` `## Language`. Implement merges to PROJECT.md later.

## Resume

Checkout `workflow/issue-{n}`, read handoff files, or use session comment link.

## On human answers

1. Update `requirements.md`, `language.md`, `state.json` on branch.
2. Commit + push.
3. Ask next question or ask for `approve requirements`.

## On `approve requirements`

1. Verify `requirements.md` complete.
2. Finalize `state.json` — `requirements_approved: true`, `status: done`, history.
3. Check approval in `requirements.md`.
4. Commit + push.
5. **Post approval comment** on the issue:
   - **Varied header** (see handoff-format approve example bank — not always "Requirements approved")
   - `---`
   - **Full approved `requirements.md`**
   ```bash
   gh issue comment {n} --body-file /tmp/requirements-comment.md
   ```
6. **Swap labels last** — `workflow:implement`. **Stop.**

## requirements.md template

```markdown
# Requirements: issue-{number}

## Original ask
{from task.md}

## Clarifications
| # | Question | Answer | Recommended |
|---|----------|--------|-------------|

## Acceptance criteria
- [ ] ...

## Approved by human
- [ ] Pending — reply `approve requirements` when ready
```

## GitHub writes (clarify)

| When | Git | Issue |
|------|-----|-------|
| Start | CREATE branch + init commit | Session comment with **session + branch links** |
| Q&A turn | COMMIT + push handoff | None |
| Approve | COMMIT + push | Header + **full requirements.md** → label swap last |

## Hard rules

- Never write application source code.
- **Only write** `workflow/issues/{n}/` during clarify.
- **Create branch at start** — before session comment and Q1.
- **Issue comments:** varied, engaging — see handoff-format example bank. Never repeat the same comment verbatim across issues.
- **Commit handoff after every Q&A turn** and at approve.
- **Never put `state.json` or other machine handoff in issue comments** — publish **approved `requirements.md` only** at clarify approve.
- If push fails, short issue comment and **stop**; do not swap to `workflow:implement`.
- **Label swap first** at start; **last** at approve.
