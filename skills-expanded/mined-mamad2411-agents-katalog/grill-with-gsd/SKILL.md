---
name: grill-with-gsd
description: "Use when inserting grill-me before a GSD plan phase to clarify requirements or design, then persist final grill decisions into the phase CONTEXT.md and a structured GRILL.md evidence file before automatically committing and pushing the result."
---

# Grill With GSD

Use this skill as a thin adapter between GSD phase planning and the `grill-me` skill. It does not create a new questioning framework and does not modify GSD itself.

## Scope

- Supports only GSD phase `CONTEXT.md` files under `.planning/phases/`.
- Runs before `$gsd-plan-phase <phase>` when the phase context needs hard clarification.
- Calls `grill-me` as the questioning engine.
- Writes final conclusions back to `CONTEXT.md`, so later GSD sessions and agents can consume them normally.
- Writes a structured `<phase>-GRILL.md` evidence file for traceability.
- Automatically commits and pushes the `CONTEXT.md` and `<phase>-GRILL.md` updates after the run.
- Does not sync installed copies or automatically run `$gsd-plan-phase`.

## Target Resolution

Supported invocations:

```text
$grill-with-gsd
$grill-with-gsd phase 09
$grill-with-gsd .planning/phases/09-theme/09-CONTEXT.md
```

First resolve the target context with the bundled helper:

```bash
python3 <skill_root>/run.py locate-context --repo <repo> [target...] --format json
```

Use the current working directory as `<repo>` unless the user provides another repo. If the helper is unavailable, fall back to a manual search under `.planning/phases/`. If the target cannot be resolved to exactly one GSD `CONTEXT.md`, fail loud and show candidates; do not guess.

Before editing, run `git status --porcelain` in the repo. Dirty unrelated files do not block the skill. If the target `CONTEXT.md` or target `<phase>-GRILL.md` is already dirty before the run, stop before grilling and explain that automatic delivery cannot safely isolate this run from pre-existing edits.

## Grill-Me Handoff

Load the `grill-me` skill and use it directly. If `grill-me` is unavailable, stop and report that this adapter cannot run.

Do not invent a fixed questionnaire. Prepare the source material for `grill-me` from the phase directory:

- target `CONTEXT.md`
- matching `DISCUSSION-LOG.md`
- matching `RESEARCH.md`
- matching `VALIDATION.md`
- existing `UI-SPEC.md` or `PLAN.md` files if present
- current GSD state files if they are cheap to read

Tell `grill-me` the plan/design to interrogate and add these hard constraints:

- Ask one question at a time.
- Provide a recommended answer for each question.
- If an answer can be found by exploring local files, explore instead of asking.
- Do not write files during the questioning phase.
- Finish by producing `Final Grill Decisions` and `Question Trail` blocks in the formats below.

## Autonomous Finalization

Do not ask for final confirmation after `grill-me` finishes. Treat the user's answers during the grilling phase as the approval source for the final decision block.

After `grill-me` produces the required `Final Grill Decisions` and `Question Trail` blocks, write `CONTEXT.md` and `<phase>-GRILL.md` immediately. If the final blocks are incomplete or internally inconsistent, continue grilling or stop without writing.

## Context Write Format

Append a new run to `CONTEXT.md`; do not overwrite or rewrite old grill decisions.

```md
## Grill-Me Clarifications

### Run YYYY-MM-DD HH:mm

Status: passed | partial | blocked
Evidence: <phase>-GRILL.md

#### Decisions
- D-GRILL-YYYYMMDD-01: ...

#### Scope Cuts
- OUT-GRILL-YYYYMMDD-01: ...

#### Assumptions
- A-GRILL-YYYYMMDD-01: ...

#### Acceptance Updates
- AC-GRILL-YYYYMMDD-01: ...

#### Remaining Open Questions
- none

#### Plan Blockers
- none
```

If a new decision supersedes an older one, append a new item that explicitly says `Supersedes D-GRILL-...`; do not delete the older item.

## Evidence File Format

Write or append to `<phase>-GRILL.md` in the same phase directory. Use structured summary, not a verbatim transcript.

```md
# Grill-Me Review

## Run YYYY-MM-DD HH:mm

Status: passed | partial | blocked
Context file: <phase>-CONTEXT.md
Trigger: plan-before-clarification

## Question Trail

### Q1: ...
Recommended answer: ...
User answer: ...
Decision: ...
Impact on CONTEXT.md: D-GRILL-YYYYMMDD-01

## Final Grill Decisions
...
```

## Status Semantics

- `passed`: no plan-blocking ambiguity remains; suggest `$gsd-plan-phase <phase>` as the next step.
- `partial`: no blocker remains, but open questions exist; write them under `Remaining Open Questions` and tell the user the planner must include validation or checkpoints for them.
- `blocked`: blocker remains; write `Plan Blockers`, write evidence, commit and push the blocker record, and do not recommend running `$gsd-plan-phase`.

## Automatic Git Delivery

After writing files, deliver the run without asking for another confirmation:

- Run `git diff --check -- <context-file> <grill-file>` before staging.
- Stage only the target `CONTEXT.md` and `<phase>-GRILL.md`; do not stage unrelated dirty files.
- If those files have no diff after writing, skip commit and push, then report that there was nothing to deliver.
- Commit with a concise message that follows the target repo's language and style conventions. If there is no local convention, use `docs(gsd): record grill decisions for phase <phase>`.
- Push the current branch after the commit. Use the existing upstream when present. If no upstream exists but `origin` and a branch name are available, use `git push -u origin HEAD`; otherwise fail loud and report the missing push target.
- Do not create or switch branches as part of this skill.

## Failure Rules

Fail loud and do not claim success when:

- no unique target `CONTEXT.md` can be resolved
- the target file is not a GSD phase context
- `grill-me` cannot be loaded
- `grill-me` does not produce complete final decision and question trail blocks
- writing `CONTEXT.md` or `<phase>-GRILL.md` fails
- `git diff --check`, `git commit`, or `git push` fails after files are written

For `blocked`, file writes and Git delivery are still required so the blocker is preserved, but the final response must say not to proceed to plan.

## Final Response

Keep the close-out short:

- status: `passed`, `partial`, or `blocked`
- updated files
- commit hash and pushed branch, or why delivery was skipped or failed
- whether `$gsd-plan-phase <phase>` is recommended
- any open questions or blockers that affect planning
