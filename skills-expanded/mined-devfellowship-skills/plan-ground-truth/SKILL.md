---
name: plan-ground-truth
description: "Use at the very start of a large plan, before any drafting — put every primary source on disk, confirm scope, resolve unknown terms, audit the code with path:line, screenshot the current product, and probe live state (branch protection, CI time, release gates, tools, credentials). Also use for every revision (v2, v3), which re-reads the sources and not the previous version. Skip for a plan whose only source is one short message you can quote whole."
author: SamuelStefano
tags: [planning, research, requirements, audit]
---

# Ground truth before the first line of the plan

**Core principle:** draft only from files you can re-read. Your memory, your
summary and your previous version are not sources.

Every plan that went wrong in the source cases went wrong here: a chat summary
that dropped requirements, a term nobody looked up (it was the whole publishing
layer), a request read too broadly, a repo rule nobody opened.

## Step 1 — Sources on disk → `sources/`

- Raw transcripts, threads, voice notes, verbatim.
- `sources/CONTEXT.md`: a **sectioned** distillation — requirements, rejections,
  open doubts, names/terms, deadlines. Planners read this file, not your chat summary.
- Design exports / prototypes: extract the **source** (HTML/CSS/JSON), not only
  images, and list which viewport bands the design covers. Missing bands go to
  the matrix as questions. *(17 frames, zero tablet or narrow desktop → that band shipped broken.)*
- If the conversation was compacted, re-read from disk.

## Step 2 — Confirm scope before spending

- List the surfaces the request could mean (e.g. Home, Editor, Export) **and the
  delivery form** (responsive tree / PWA / native app). Ask which, offering
  "decide for me" and "I'll describe it".
- "Study and decide a better UI" is not licence for a redesign of everything.
  *(A 6-agent study redesigned the editor; the requester only wanted the projects page.)*
- Show **one example** (see `complex-plan`) before any fan-out.
- Stamp superseded decision records `DISCARDED` at the top.
- When reconciling with an earlier decision, copy **every clause** ("remove the
  cap" AND "replace it with a container-relative cap"). Dropping one half is a
  new decision and needs its owner. *(The dropped half became an overflow bug.)*

## Step 3 — `COVERAGE.md`

Template: `complex-plan/templates/COVERAGE.md`. Every source item → plan section,
or `dropped because`. Re-checked in readiness.

## Step 4 — Resolve every unknown term

Search code, docs, web; then ask. No block is written around an unresolved term.
Check **integrate or buy** before listing any "build X" item.

## Step 5 — Quote deciders with their strength

"Could be a path" ≠ "do not evaluate". Copy the exact phrase when a decision rests on it.

## Step 6 — Audit the code and look at the product

- Parallel read-only audits by area → `sources/audit-<area>.md`, every claim `path:line`.
  Cross-check contradicting audits yourself.
- Record **what already exists** ("already built — reuse, do not replan").
- Every "keep X" / "X already works" cites the `path:line` that powers it.
  No citation = it is a build item. *(A "kept" AI button had no backend.)*
- Write down the **commit of every repo you read** and put it in the plan header:
  line numbers are only true at that commit. *(A PR merged while the plan was
  being drafted added a new reader of the very tables the plan changes; the line
  numbers of the plan's most-cited file had shifted.)*
- Find one **real pending change** of the kind the plan must survive (a held
  content update, a queued migration, a half-done refactor) and hand it to the
  planners as the test case. *(The brief did not name a ready, on-hold content
  package that inserts items mid-list; combined with one draft's edit rule it would
  have rewritten published content.)*
- UI plans: screenshots of the current UI at the bands in `complex-plan/templates/MATRIX.md`
  → `sources/screenshots/<band>-<screen>.png`. Pipelines: screenshot the
  consumer's actual view (board, channel) as they see it.

## Step 7 — Probe live state → `sources/PROBES.md`

One row per probe: `probe | result | command/source | date`.

| Probe | Why it bit |
|---|---|
| Branch protection, required reviews, code owners | Merges stalled 2h40 at the end; then "skip CI" removed the only e2e gate |
| Repo rule files (`CLAUDE.md`, `AGENTS.md`, ADRs, specs) for release gates — **in every repo a PR row will touch**, not only the main one | A rule required physical-device proof before the new tree became default; nobody read it, so no device gate was scheduled and the flag never flipped. A secondary repo's UI-language and routing rules surfaced only in the third review |
| CI duration of the suites the plan extends | Mobile e2e grew to 45–50 min/PR and was ignored |
| Tools, MCPs, credentials the plan needs, and who owns them | A diagram tool was disconnected; a DNS token lived in a personal vault |
| Test accounts and CI secrets: **list them through the API**, and read the last run of the suite the plan extends — how many tests ran, how many skipped | A plan scheduled "create the test secrets"; they had existed for two months. The workflow never declared them, so every spec that needed a login skipped (20 skips in the last run) and nobody had read the count |
| Every database or service the plan must measure: can you reach it **with a validated target** today? | The planner's token did not reach the project; the database measurements moved to Phase 0 with an owner instead of being guessed |
| Deploy topology: which branch deploys, restart behavior, caches | A merged feature did not appear: the server restarts only when idle |
| Protections the design relies on (row-level security, rulesets) — via API | Twice assumed on, twice found off |
| Existing plans and ADRs on the topic | Avoids a third vocabulary; lets the author refute wrong review claims |
| Where each human consumer actually looks (view, filter, sort, channel) — ask them | A working pipeline delivered into a board and channel the consumer never opened |

Repeat the last probe before **each review** and before publishing:
`git log <commit you read>..origin/main -- <paths the plan touches>`. A new reader
or writer of the data you are changing is a missing PR row.

## Step 8 — `sources/NOT-READ.md`

`Not read: <board X — no access>, <repo Y — not cloned>`. Copied into the PLAN.md
header. A named gap gets filled; a guessed gap becomes a bug.

## Revisions (v2, v3…)

Re-run steps 3 and 7 against the **sources**, including earlier answered
questions, and add a table `decided in vN → still valid today?`. List "changed
since vN". Re-read live state right before publishing — PRs merge while you plan.
