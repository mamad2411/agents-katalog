---
name: pr-implement
description: Stage 3 of 4 of the /la:pr flow — implement until every test from the pr-tests stage passes, then commit, push and, with the user's explicit go-ahead, open the PR. Normally dispatched by /la:pr; if the /la:pr context (BRANCH, CHANGE_ID, OPENSPEC, tracker issue) is not already loaded in this session, invoke the la:pr skill instead.
---

**Stage 3 of 4 of the `/la:pr` flow.** Prerequisite: `/la:pr` has run in this
session, preflight included, and established `BRANCH`, `CHANGE_ID`, `OPENSPEC`, and the full tracker
issue (body + comments), if there is one. If any of that is missing, invoke the `la:pr` skill
instead — it rehydrates and dispatches back here. The `/la:pr` stopping policy
applies throughout this stage.

Before writing anything, recover the durable plan (the
`openspec/changes/<CHANGE_ID>/` folder when `OPENSPEC=1`, else the plan
comment on the tracker issue) and the failing tests already on disk from
`pr-tests`.

## Step 1 — Implement until tests pass

Implement the plan. After changes, run the tests in the `/la:pr` local test scope and fix any failures. Do not
declare done until every test from the `pr-tests` stage passes.
An existing test that breaks because it pins what the plan changes is not a
design fork: ask only for approval to align it with the plan (the `/la:pr`
stopping policy), never with alternative options.

**Symptom vs. structural cause — decide before you patch.** The plan already
chose between a band-aid and a structural fix; implement the structural shape
it chose, and do not quietly degrade it into instance patches to get tests
green faster. If, while implementing, a test failure or the code itself
reveals that the planned fix is a band-aid after all — the same change must be
repeated in N places, two code paths have to agree by hand, a missed
normalization that a single canonical representation would obviate, an
axiom-violating shape left standing (judged against the principles/axioms in
the `architecture/*.arc42.md` files) — STOP and present the case to me: the
symptom, the structural cause, the band-aid vs. structural options with
PROS/CONS, the arc42 grounding, and your RECOMMENDATION (leaning structural —
a bigger diff is an acceptable cost). Wait for my call (this is the
design-decision pause permitted by the `/la:pr` stopping policy). If the
failure is genuinely local with no structural cause, just fix it. Never
silently ship a band-aid over a structural problem, and never undertake a
large structural refactor the plan did not include without my go-ahead.

Intermediate local commits during implementation are fine within reason — e.g.
to merge origin/main before editing, or to checkpoint a coherent working state.
Keep them tidy (specific `git add`, never `git add -A`); they can be reorganized
before the push. The go-ahead gate in Step 3 governs **opening the PR** only.

If `OPENSPEC=1`, tick off `openspec/changes/<CHANGE_ID>/tasks.md` as you complete
each task (the same checklist authored in `pr-plan` — this is the
`apply` phase, driven by TDD here instead of `/opsx:apply`).

When writing code, follow the `la:concise-comments` skill: no design essays,
ticket-ID-on-every-line, or code-restating comments; docstrings to a line.
Rationale belongs in the spec / PR description / the tracker issue — not in
code — so verbose comments never get written in the first place.

## Step 2 — Local gates (before commit)

Once the tests in scope are green, run the SAME deterministic gates `pr-review` uses, so
the review bots don't have to redo them and the first push is already clean.
Both are HARD GATES: do not proceed to Step 3 while either is RED.

**Conventions.** There is no PR yet at this stage, so diff against the default
branch with `--base`:

```
la-check-conventions --base <default-branch>
```

What it checks and how to fix each finding is described once, in the
`la:process-reviews` skill (its conventions gate section); follow it. An
`import-not-top` waiver must be confirmed with me BEFORE landing it. Re-run
until green.

**Type check.** Run `dr-typecheck`. It checks each applicable language against
its committed baseline, and exit 1 means this change added errors outside it.
The baseline is a ratchet:
- never re-record it (`--write-baseline` exists only to adopt the gate once);
- fix every new error at its root, never by loosening types or adding a
  suppression; a per-line suppression with a reason
  (`la-config get lang.<language>.suppression`) is a solve only when the checker is wrong (a false
  positive) or the wrongness is deliberate (e.g. an invalid-input test);
- it only shrinks: when a file you touch carries baselined errors that
  root-fix without much churn, fix those too, and commit the baseline
  `dr-typecheck` shrinks.

`dr-typecheck` printing "nothing to check" means no language applies, which is
not a failure. Re-run until green.

## Step 3 — Push, then ask me to open the PR

Once every test in scope passes AND both local gates are green, push the branch,
then stop and ask me whether to open a PR (folding in any final commit of the
implementation). Intermediate local commits along the way were fine (Step 1);
push the branch when ready, but **opening the PR** needs my explicit go-ahead —
never do it on your own.
Then follow the standard commit/PR workflow (specific `git add` for each new
file, never `git add -A`).

If `OPENSPEC=1`, the whole `openspec/changes/<CHANGE_ID>/` folder is part of the
change — `git add` it explicitly alongside the code (proposal, design, tasks,
delta specs). Do NOT archive yet — that happens once the review loop has
converged, just before I merge (`pr-review`).

**Always merge the PR's destination branch before creating the PR.** After
committing and before the push, bring the PR's envisioned base branch (the branch
the PR will target — usually `main`) into `BRANCH`, so the PR opens against, and
CI runs on, the current destination rather than a stale base: `git fetch origin
<base>` then `git merge origin/<base>`. Commit any local changes first, then
merge — NEVER stash, NEVER rebase; the merge message's
first line must name the merged ref in single quotes, e.g. `Merge branch
'origin/main' into <BRANCH>`. Resolve any conflicts, re-run the local gates
(the local test scope plus the tests covering every file the merge conflicted on,
conventions and type check) on the merged tree, and only then
push and `gh pr create`. If the base has not advanced since your last merge the
merge is a no-op — proceed straight to the push.

**Write the PR description for a human reader**, not as a spec dump. Concise but
complete prose: what the change does and why, the user-facing behaviour it adds
or changes, and — where it makes the change concrete — a short runnable example
or two (a query plus what it now returns, or a before/after). Cover anything a
reviewer needs to understand and evaluate the change; skip what they don't.
Do NOT paste `openspec show --diff`, the raw delta specs, or the tasks
checklist — the change folder is committed in this PR, so whoever wants the full
spec surface reads it there. Link the tracker issue (GitHub: `Closes #<N>`).

## Step 4 — Hard stop

> **🛑 HARD STOP (reset point 3 of 3) — just after the PR is created.** Code,
> tests (green, local gates clean), and the change folder are committed and
> the PR exists. Say we're at reset point 3 and STOP — do not start the review
> loop. I'll `/clear` and re-invoke `/la:pr`, which will detect and run
> `pr-review`.
