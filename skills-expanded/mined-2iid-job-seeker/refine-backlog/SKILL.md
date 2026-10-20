---
name: refine-backlog
description: Groom the backlog and roll the next sprint(s) from it — re-validate, re-atomize, and re-prioritize the unplanned items, split any that grew into an epic, merge/close stale duplicates, then slice the next demoable sprint and set each issue's Sprint field on the board. This is what keeps continuous-flow actually continuous — when the pre-planned sprints run out with backlog left, it refills them. Use at every sprint boundary while backlog remains, when new items arrive (from /adopt, /growth-review, bug reports), or when work stalls with stories left unplanned. Trigger words — refine backlog, backlog refinement, groom, grooming, re-plan, replan, plan next sprint, remaining stories, replenish sprint, refill the backlog, no sprint.
---
# /refine-backlog — keep the sprint engine fed

**Use when:** a sprint just closed and unplanned backlog remains; new items arrived (from `/adopt`, `/growth-review`,
bugs); or the loop stalled because leftover stories were never planned into a sprint. **Owners:** `sprint-planner`
(+ `product-strategist` for priority calls). Planned sprints are finite; the backlog usually isn't — this is the
ritual that turns the reliquat into the next sprints so `/next` never runs dry.

## Procedure
1. **Gather the unplanned backlog.** Every issue **not** in a done or ACTIVE sprint — from the board (via `gh`) or
   `scripts/kanban/issues.csv`. Explicitly include carry-overs **and anything with no `Sprint` value** (the
   "No Sprint" limbo — those are invisible to a sprint-driven flow and are the usual cause of a stall).
2. **Refine each item** (the grooming):
   - **Still valid & needed?** Close/drop obsolete or superseded ones — with a one-line reason, never silently.
   - **Still atomic?** If it grew, or was always an epic, run `decompose-feature` to split it into agent-ready issues.
   - **De-dupe / merge** overlapping items.
   - Re-confirm a rough **size**, and give every item the **three fields that make the downstream gates
     mechanical** — an issue missing any of them is not groomed:
     1. **Acceptance criteria** — the user-visible outcome, phrased so `scripts/verify.sh --observe` can state
        expected vs observed and `/sprint-review` can check it without interpretation.
     2. **Security flag** — does the change touch anything in `vantry.yml` **`sensitive_paths`**? If yes, the
        issue owes a committed `.vantry/reviews/<branch-slug>.security.json` with `verdict: "pass"` before it
        can close (RLS allow/deny where relevant).
     3. **Declared `paths`** — the globs the change will write. This is what lets `/next` co-dispatch safely;
        an issue with no declared `paths` can only ever run **alone**.
3. **Re-prioritize** by value / risk / dependencies — **stabilize-first** carries (security + shaky foundations
   before new features). Order so `/next` can never pick a blocked issue.
4. **Slice the next sprint(s).** Pull the top of the refined backlog into the next **demoable** sprint
   (continuous-flow, **no timebox** — size by a coherent demoable outcome, not a calendar). Write it to
   `docs/planning/sprint-plan.md` (new sprint: goal + issue list) and **set each issue's `Sprint` field on the
   board** so nothing is left in "No Sprint".
5. **Report + hand off.** The new sprint's goal + issues, what was dropped / split / merged (with reasons), and how
   many items remain in the groomed backlog. End with `/next`.

## Guardrails
- **Never invent scope.** Refinement re-shapes what already exists (+ work that genuinely arrived); it does not
  fabricate features.
- **Every planned issue is atomic, dependency-ordered, and board-synced.** An item with no `Sprint` value is a bug —
  it vanishes from the flow.
- **Acceptance criteria, security flag and `paths` are not optional.** They are the inputs the verification and
  review gates consume; an issue without them cannot be judged done and cannot be parallelized.
- Keep every sprint **demoable** — it should end with something a stakeholder understands.
- Dropped/merged items are recorded with a reason, never quietly deleted.

## New stories are not on the board until you put them there
This is the step that was missing, and its absence is quiet: refinement takes a sprint from 11 stories to 20,
`issues.csv` says 20, and **the board still shows 11**. Everything downstream then reads the old number —
`/next` cannot hand out an issue that does not exist, `/standup` counts 11, `/sprint-review` closes a sprint on
a scope nobody agreed.

The cause: setting a `Sprint` field only moves an issue that **already exists**. A row you just wrote has no
issue behind it. So after grooming, in this order:

```bash
bash scripts/kanban/lint-kanban.sh                       # the rows are well-formed first
DRY_RUN=1 bash scripts/kanban/import-kanban.sh --project <n>   # read the preview
bash scripts/kanban/import-kanban.sh --project <n>       # creates the NEW ones, syncs the rest
bash scripts/kanban/import-kanban.sh --check             # must print: every backlog row exists on the board
```

The importer is idempotent — it back-fills labels on issues that exist and creates only what is missing, so
re-running it is safe and is the normal way to finish a refinement.

If a **new sprint number** appears (S4 when the board only knew S1–S3), the importer amends the Sprint field's
options for you. If it cannot, it says so and names the option to add by hand; do that before assigning.

## Done when
- **`bash scripts/kanban/import-kanban.sh --check` exits 0** — every row in `issues.csv` has an issue on the
  board. This is the clause that was missing: without it, refinement could report done while half the sprint
  existed only in a CSV.
- `bash scripts/kanban/lint-kanban.sh` exits 0.

The unplanned backlog is groomed, the **next sprint is planned and ACTIVE on the board**, and **every issue carries a
`Sprint` value** — scheduled work in `S1…SN`, everything else in an explicit **`Backlog`**, **never empty**. (An empty
Sprint field is exactly what creates a "No Sprint" column — there must be none; the board's columns are `S1 … SN · Backlog`.)
`sprint-plan.md` agrees, `/next` has a real first issue — **or** the backlog is genuinely empty (say so, and point to
`/refine-idea` or `/growth-review` to source new work).
