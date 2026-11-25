---
name: team-1shot
description: >-
  Run the full delivery trilogy end-to-end — team-intake → team-qa → team-build
  — from a raw request to a verified green build. Use when the user invokes
  /team-1shot, wants a one-shot / full-pipeline / start-to-finish delivery run,
  or asks to roll through intake+QA+build without staging approvals. Optional
  --release appends team-release after a green build. Does not run team-status.
argument-hint: >-
  Path to intake base folder (request lives here). Optional flags: --release,
  --pause-before-build. Will ask for folder if omitted.
disable-model-invocation: true
---

# Team 1shot

Orchestrates the **delivery trilogy** in one run:

1. **`team-intake`** → `technical-plan.md` + `pm-plan.md`
2. **`team-qa`** → `qa-assessment.md` + `test-plan.md` (input = completed intake folder)
3. **`team-build`** → isolated worktree + `build-report.md` (needs both plans)

Optional 4th stage if the user passed **`--release`**:

4. **`team-release`** → client-facing `release-notes.md` (after green build)

You are the **pipeline lead**. Do **not** re-implement those teams. For each
stage: **read that skill’s `SKILL.md` and execute it fully**, then hand the
next stage the artifacts it requires.

## Out of scope (never auto-run)

| Skill | Why |
|-------|-----|
| `team-status` | Advisory recon — use after, not inside, a 1shot |

## Flags

| Flag | Effect |
|------|--------|
| *(none)* | Auto-continue intake → qa → build. Halt only on hard stop (below). |
| `--pause-before-build` | After QA, summarize plans and **wait for user approval** before build. |
| `--release` | After a green build-report, run `team-release` (ask for version label if missing). |

## Step 0 — Resolve intake base

- Use the path from the skill argument / user message (folder that holds the
  request). If they pointed at a file, use its parent folder.
- **If no folder given, STOP and ask** for the intake base folder.
- Do not invent a request or location.

Parse flags from the argument/`--*` tokens; strip them before passing the path
to child skills.

## Step 1 — Intake

1. Locate and **read** the `team-intake` skill (`SKILL.md`).
2. Run it end-to-end against the intake base folder.
3. Record the produced folder:
   `<intake-base>/intake/<YYYY-MM-DD>-<slug>/`
4. **Hard stop** if triage (or later intake) is **BLOCKED**, or
   `technical-plan.md` / `pm-plan.md` were not written. Surface blockers; do
   not start QA/build.

Pin product-fork defaults per intake’s `durable-authority-guardrails.md` when
present; do not leave `decisions.md` empty when those forks apply.

## Step 2 — QA

1. Locate and **read** the `team-qa` skill (`SKILL.md`).
2. Run it against the **completed intake folder** from Step 1 (the change
   input is that folder’s technical plan / request surface — follow team-qa’s
   own intake rules).
3. Confirm `qa-assessment.md` and `test-plan.md` exist under the intake
   item’s `qa/` (or wherever team-qa writes for this layout).
4. **Hard stop** if QA cannot produce a buildable `test-plan.md`.

## Step 3 — Optional pause

If `--pause-before-build`:

- Summarize: request type, technical approach (3 bullets), top QA risks, paths
  to `technical-plan.md` + `test-plan.md`.
- Ask: proceed to build? **Wait.** Do not start build until the user confirms.

Otherwise continue.

## Step 4 — Build

1. Locate and **read** the `team-build` skill (`SKILL.md`).
2. Run it against the same completed intake folder (must contain technical-plan
   **and** test-plan).
3. Confirm a green `build-report.md` (or equivalent verifier sign-off per that
   skill).
4. **Hard stop** on failed verify / incomplete build. Do not invent a green
   report. Do not run release.

## Step 5 — Optional release

Only if `--release` **and** Step 4 is green:

1. Locate and **read** the `team-release` skill (`SKILL.md`).
2. Ask for a version label if not provided; run release over the shipped
   build folder(s).

## Step 6 — Final report (chat)

Return a short pipeline summary:

| Stage | Status | Primary artifact |
|-------|--------|------------------|
| Intake | done / blocked | `…/technical-plan.md`, `…/pm-plan.md` |
| QA | done / skipped / blocked | `…/test-plan.md`, `…/qa-assessment.md` |
| Build | done / skipped / failed | `…/build-report.md` (+ worktree/branch if any) |
| Release | done / skipped | `…/release-notes.md` if run |

Plus: overall verdict (ship-ready / stopped-at / failed), and the absolute
paths a human needs to open.

## Progress checklist (copy and update as you go)

```
Team 1shot
- [ ] Step 0 intake base resolved
- [ ] Step 1 team-intake complete (technical-plan + pm-plan)
- [ ] Step 2 team-qa complete (test-plan + qa-assessment)
- [ ] Step 3 pause cleared (or N/A)
- [ ] Step 4 team-build green (build-report)
- [ ] Step 5 team-release (or skipped)
- [ ] Step 6 final report
```

## Rules

- **Read then run** each child skill — never shortcut agents or invent plans.
- **One pipeline, one intake item** per invocation (don’t batch unrelated asks).
- Prefer child-skill hard stops over “best effort” continuation.
- This skill does not commit, push, or open PRs unless a child skill (and the
  user) explicitly require it.
