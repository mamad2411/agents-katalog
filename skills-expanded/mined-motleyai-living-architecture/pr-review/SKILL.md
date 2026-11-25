---
name: pr-review
description: Stage 4 of 4 of the /la:pr flow — run /la:process-reviews in a loop until every source is green, then (OpenSpec repos only) archive the change, push, and keep looping on the archived HEAD until every source is green again so the PR can merge. Normally dispatched by /la:pr; if the /la:pr context (BRANCH, CHANGE_ID, OPENSPEC, tracker issue) is not already loaded in this session, invoke the la:pr skill instead.
---

**Stage 4 of 4 of the `/la:pr` flow.** Prerequisite: `/la:pr` has run in this
session, preflight included, and established `BRANCH`, `CHANGE_ID`, `OPENSPEC`, and the full tracker
issue (body + comments, if there is one), and the PR for `BRANCH` exists. If any of that is
missing, invoke the `la:pr` skill instead — it rehydrates and dispatches back
here. The `/la:pr` stopping policy applies throughout this stage.

**Review sources.** `la:process-reviews` owns everything per source: which bots
are on this PR (`la-pr-reviewers`), waiting for them, fetching, validating, and
handling invalid findings. Every step below that names CodeRabbit or Sonar
applies only when that bot is on the PR. Codex follows `reviewers.codex`: when
`la-config get reviewers.codex` prints `false` there is no Codex gate; when it
is on and the Codex MCP server (`mcp__codex__codex`) is missing, STOP and tell
me — never skip it silently.

## Step 1 — Review loop (batch local fixes; push only once per batch)

Do NOT re-run every gate after every micro-fix. Re-triggering the slow and
quota-limited flows (CI, CodeRabbit, the Sonar PR gate) costs a full push
each time. Batch fixes and verify them locally, then push once per batch.

**Run this loop autonomously — fix findings and push fix batches without asking.
The ONLY pauses are (a) a nontrivial design choice — a real fork with more than
one reasonable option, raised with PROS/CONS + a recommendation per the
symptom-vs-structural rule below — and (b) the Step 2 archive gate. A flagged
gate item is NEVER dismissed as "pre-existing": if a gate (Sonar, CI,
conventions, the type baseline, …) flags something on this PR — even on an old
line, an untouched file, or an issue with a months-old creation date — it is in
scope. Fix it, or, only for a genuine false positive, suppress it through that
gate's sanctioned channel with a written reason. "It predates my change" / "the
gate is still green overall" is NEVER a reason to skip a flagged item.**

Never ask before pushing to this PR's own branch: push as soon as a batch is
ready. Only opening a PR needs my approval.

Split the gates into two tiers:

- **Local gates** — fast, deterministic, need no push and no network trigger;
  run against the working tree / local diff:
  - the tests in the `/la:pr` local test scope (which includes every test CI
    reported failing) and the linter (`la-config get commands.lint`, else the
    repo's usual linter);
  - conventions gate (`la-check-conventions <PR>`), handled as the
    `la:process-reviews` conventions gate section describes;
  - type check (`dr-typecheck`), under the ratchet rule described at the
    type-check gate of the `la:pr-implement` skill;
  - Codex on the local diff (`mcp__codex__codex`, read-only; when
    `reviewers.codex` is on) — it analyses the working tree, so it needs no push;
  - (Sonar on the PR) local Sonar pre-check: `mcp__sonarqube__analyze_code_snippet`
    on each changed source file (single-file only — no cross-file, coverage, or
    duplication analysis; a fast pre-filter, NOT a substitute for the pushed
    Sonar gate);
  - `openspec validate <CHANGE_ID> --strict` (OpenSpec repos);
  - **living-architecture repos** (`architecture: true`): the
    `la:living-architecture` skill's "Working under the architecture" rules
    apply to every fix in this loop. Then `la-arch-check` (the one import law, model-truth at every
    declared granularity) and LikeC4 model validation (see the
    `la:living-architecture` skill).
- **Remote gates** — slow and/or quota-limited; only a push produces them:
  CI (GitHub Actions), CodeRabbit, and the Sonar PR-decorated quality gate
  + new-issues count (the bots only when on the PR).

The loop:

1. **Initial full sweep.** Run `/la:process-reviews` on the current pushed HEAD. Fix each valid item in the working tree as soon as it is triaged, while the watch keeps running; push nothing. Run every local gate. When the watch exits, the failing set is complete.
2. **Local fix sub-loop — NO push.** Fix the failures, then re-run (a) the
   specific gates that failed AND (b) every local gate above — INCLUDING a
   fresh full-PR Codex pass over the fixed working tree (Codex is a local
   gate: it reads the working tree, so a pre-push run costs no CI cycle;
   include uncommitted changes via `git diff origin/<base>`). Do NOT push and
   do NOT re-trigger CI / CodeRabbit / Sonar in this sub-loop. Repeat
   until ALL local gates converge on the same tree state — tests, linter,
   conventions, type check, Sonar pre-check, openspec/architecture checks green
   AND Codex returning no new valid findings. NEVER push a fix Codex has not reviewed —
   a gap in the fix itself otherwise ships and costs a full extra CI round.
   Run the local gates on these fixes as you go; the full convergence, Codex included, runs once the watch has exited.
3. **Push once.** Only after step 2 has fully converged (Codex included),
   commit and push — this re-triggers the remote gates a single time for the
   whole batch. Never push while a question to me is pending (or about to be
   asked) — ask first, push after I answer, even if the batch excludes the
   disputed change.
4. **Full remote sweep.** Run `/la:process-reviews` again on the new HEAD (it also re-runs Codex), fixing each valid item as it is triaged, without pushing, until its watch exits. Any new failure sends you back to step 2, then step 3. Repeat until one full push cycle returns every source green with nothing left to fix.

**"Green" for CI means an actually-COMPLETE, PASSING run — every check finished
with a pass conclusion.** "No *failed* checks" is NOT green while any check is
still QUEUED / IN_PROGRESS, and `la-wait-for-reviews` exiting 0 only
means the checks it saw were terminal at that poll — it can fire before slow
jobs (the full test matrix, integration/example jobs) even start or finish.
Before treating CI as green, confirm EVERY check shows `pass` (e.g.
`gh pr checks <PR>`). NEVER declare convergence on an incomplete or
still-running CI run.

Use `/la:process-reviews` for the remote sweeps (steps 1 and 4) — it owns the
watch + fetch of CI/CodeRabbit/Sonar and the Codex pass. Run the local
sub-loop (step 2) directly against the working tree; do not invoke
`/la:process-reviews` there (its watch is about remote state you have not
re-triggered yet).

**Symptom vs. structural cause — decide before you patch.** For EACH valid
finding, before writing the fix, ask whether it is merely a *symptom* of a
deeper structural issue and whether a *structural* fix would be more correct
than a local band-aid — judged against the principles/axioms in the
`architecture/*.arc42.md` files (a band-aid that leaves an axiom-violating
shape standing, a bug that recurs because two code paths must agree by hand, a
missed-normalization that a single canonical representation would obviate, etc.
are all tells). When a structural fix appears warranted, STOP and present the
case to me — the symptom, the structural cause, the band-aid vs. structural
options with PROS/CONS, the arc42 grounding, and your RECOMMENDATION — then wait
for my call (this is the design-decision pause permitted by the `/la:pr` stopping
policy). If the finding is genuinely local with no structural cause, just fix
it. Never silently ship a band-aid over a structural problem, and never
undertake a large structural refactor without my go-ahead.

**Convergence also requires zero dangling CodeRabbit threads** (CodeRabbit on
the PR): every thread `la:process-reviews` says needs a reply has one. "All
sources green" alone is not enough.

## Step 2 — Archive the OpenSpec change, then I merge (OpenSpec repos only)

Skip unless `OPENSPEC=1`. **Archiving is the ONE action that ALWAYS needs my
fresh, explicit say-so. It is NEVER covered by any "keep going until clean" /
"don't ask unless there's a design choice" autonomy I grant — that autonomy is
for the fix loop (fixing findings, pushing fix batches) and STOPS at the archive.
Do NOT archive on your own judgment, ever, even when every gate is green.** Once
the Step 1 loop has CONVERGED — every source ACTUALLY green (CI a complete
passing run per the definition above, Sonar, CodeRabbit, Codex, conventions,
type check) — do
NOT archive: STOP, tell me the loop is clean, and ASK my permission to archive.

**Before offering to archive, the branch MUST include the PR's base.** If
`git merge-base --is-ancestor origin/<base> HEAD` is false, merge it in
(`git merge origin/<base>`, never rebase), re-run the Step 1 loop on the merged
tree, and push. This is autonomous — do it without asking. Archiving a stale
branch bakes an out-of-date corpus into the merge.

**Before you offer to archive, verify `openspec/changes/<CHANGE_ID>/tasks.md`
has no unchecked `- [ ]` items.** `openspec archive` only *warns* on incomplete
tasks and continues under `--yes`, so a silent gap would ship. For each
unchecked task: tick it if the work is already done (a gate/verification task
you ran during the loop but never ticked is a common cross-session miss — tick
it), do it if it is real remaining work, or — if it was deliberately deferred —
strike it with a one-line pointer to the issue it moved to. Do NOT offer to
archive while a genuinely-incomplete task remains: surface the list to me and
resolve it first, and when you do offer, report which unchecked tasks you ticked
as already-done.

Only on my explicit go-ahead run:

```
openspec archive <CHANGE_ID> --yes
```

and commit + push the result on the PR branch. Archiving pre-merge (NOT
post-merge) lands the corpus update atomically with the code in the same PR.

**The archive push re-triggers every remote gate. Keep reviewing until
convergence.** The archive commit is docs-only, but CodeRabbit still reviews it
(the new `openspec/specs/**` file is fresh text to it), and CI reruns. So after
the push, go back into the Step 1 loop on the archived HEAD: run
`/la:process-reviews` for a full remote sweep, fix or answer every finding, push
each fix batch, and sweep again. Repeat until one full push cycle is green on
every source, with zero dangling CodeRabbit threads. This applies equally to any
later push before the merge. Only then tell me the PR is ready to merge. NEVER
report "ready to merge" right after the archive push.

The archive does not reopen the plan. A finding that would change the archived
change folder or `openspec/specs/**` beyond a pure typo is a plan edit. Present
the exact diff and wait for my OK, as the `/la:pr` frozen-plan rule requires.
Fixes to code and tests stay autonomous.

This merges the delta into `openspec/specs/` (ADDED appended, MODIFIED replaced,
REMOVED deleted) and moves the change to
`openspec/changes/archive/YYYY-MM-DD-<CHANGE_ID>/`. Commit the result with one
`git add` that names every changed `openspec/specs/` file and every moved file
by explicit path, including the removed source paths under
`openspec/changes/<CHANGE_ID>/`. This
is the one step that keeps the behaviour corpus current — everything upstream is
best-effort authoring; `validate` (in `pr-plan`) and `archive` here are
the deterministic guarantees.
