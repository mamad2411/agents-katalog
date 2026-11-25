---
name: pr
description: Spec-driven change flow for a task given to an agent. Pulls in the tracker issue (Linear or GitHub, per `living-architecture.yaml`) that the current git branch belongs to, and combines it with whatever the user typed when invoking the skill. Rehydrates context, detects the current stage, and dispatches to the stage skills la:pr-plan → la:pr-tests → la:pr-implement → la:pr-review.
---

**Preflight:** run `la-doctor --plugin <this skill's base directory> --require-config --require-plan-store` once per session before using any `la-*` or `dr-*` command; it also covers the stage skill this session dispatches. If it reports the missing-config finding (the one naming `/la:init`), run the fast path of the `la:init` skill; if it reports a format finding naming `la-arch-migrate` (a missing or older format): when `git status --porcelain` prints anything, stop and show the user those paths; otherwise run `la-arch-migrate` without asking and commit the paths it prints at once, without a push of their own. Then re-run this preflight; stop and show the user its output on anything it still reports, or on any other failure.

I want a detailed spec-driven flow. The brief is the union of:
1. The tracker issue tied to the current branch (see "Rehydrate" below), AND
2. Whatever I just typed when invoking this skill.

## The four stages

The flow runs as four stage skills in this fixed order, and I reset the
session (`/clear`) between stages. Each stage ends at a hard stop; everything
a fresh session needs is on disk or in the tracker, so any stage can resume from
just the branch name:

1. **`pr-plan`** — interview me, Codex-review the plan (when
   `reviewers.codex` is on), emit the
   OpenSpec change (OpenSpec repos only), make the plan durable.
   Ends at 🛑 reset point 1 (before tests).
2. **`pr-tests`** — write the full failing test suite for the plan,
   Codex-review the tests against the plan (when `reviewers.codex` is on).
   Ends at 🛑 reset point 2 (before implementation).
3. **`pr-implement`** — implement until every test passes, then commit and
   push, and (with my go-ahead) open the PR.
   Ends at 🛑 reset point 3 (just after the PR is created).
4. **`pr-review`** — run `/la:process-reviews` until converged, then
   archive the OpenSpec change (OpenSpec repos only), then keep sweeping the
   gates on the archived HEAD until they converge again, so I can merge.

This skill does NO stage work itself. It only: rehydrates context (below),
detects which stage we're at, and invokes that stage's skill (`la:<stage>`) via
the Skill tool. Run exactly ONE stage per session — when its hard stop is reached, STOP;
never chain into the next stage, even if it looks quick.

## Stopping policy

Each stage skill ends with its own **hard stop** so I can reset your context.
At a hard stop: say which reset point we're at, then STOP and wait — do not
start the next stage. I'll `/clear` and re-invoke `/la:pr` (possibly with
"continue on branch `<BRANCH>`"); rehydration + stage detection below take it
from there.

**Within a stage, run autonomously — do NOT stop or ask permission to
proceed.** The only other permitted pauses are:
- the **`pr-plan` interview** (its whole point is questioning me);
- a **nontrivial design decision** — a real fork with more than one reasonable
  option — raised with explicit PROS/CONS + RECOMMENDATION (per the interview
  rule in `pr-plan`, offering only genuine options as its "Genuine options
  only" rule defines them). A choice with an obvious default is NOT this:
  take the default and move on;
- the standing **go-ahead gate before opening a PR** (`pr-implement`): never
  open a PR without my explicit go-ahead; pushing this change's own branch needs none;
- a **suspected unrelated gap** — a failure, restriction, or missing capability
  that looks pre-existing or outside this change's scope (a bind-level refusal, an
  allowlist, a fixture that cannot express a scenario, …). Whether it is unrelated
  and what to do about it is MY call, never yours: STOP and ask, presenting what
  you found, the existing tracker issues you searched for (search first, cite ids
  and titles), and the options (treat as in-scope / xfail against an EXISTING issue
  / narrow the scenario) with a recommendation. NEVER create a tracker issue, mark a
  scenario xfail, or narrow a scenario on your own to route around it — even when a
  tasks.md line or an earlier plan says "file its own issue".
- an **existing test that contradicts the plan** — it pins a shape or behaviour the
  plan changes: ask ONLY for my approval to align that test with the plan, naming
  each file and what changes in it. This is an approval request, not a choice:
  NEVER pose alternatives beside it (a workaround the plan rejected, keeping the
  old shape to spare the test, …).

Never stop just to report progress, to confirm an obvious next step, or to ask
something you can determine yourself.

**Ask every question before acting on any answer, one question per message.**
Every pause above is a question: a design choice, an approval to align a test, an
approval of a plan, spec, harness or skill edit. When questions are pending —
including ones that surface mid-stage — stop working, queue them all, and ask
them back to back, exactly ONE per message, each self-contained. An answer is
NEVER a go signal while another question is still queued: reply to it with the
next question and nothing else. Act on the answers only after the LAST one; if
acting raises new questions, stop and queue them the same way.

## The plan is frozen once pr-plan ends

The plan — the OpenSpec change folder (proposal, design, tasks, delta specs) or,
without OpenSpec, the finalized-plan comment on the tracker issue — is MINE once
`pr-plan` reaches its hard stop. In EVERY later stage, NEVER change it without
my explicit confirmation of the exact edit: no added or amended decisions, no
rewritten or added scenarios, no "corrections" after a probe, no re-scoping, no
notes folded into tasks. If a stage finds the plan wrong, incomplete, or
contradicted by an axiom or a probe, STOP, present the exact proposed diff with
the reason, and wait. The one self-serve edit is flipping a task's `[ ]` to `[x]`
when it was completed exactly as written.

## Nothing the next stage needs lives in chat

Sessions `/clear` between stages, so the stop message reaches no future stage.
Anything the next stage must know therefore has to be **persisted where that
stage will discover it naturally** during its own rehydration and work — NEVER a
turn-final "heads-up", "note for next time", "FYI for pr-implement", or a
caveat tacked onto the stop message. Such text is gone the instant I `/clear`, so
it only masquerades as a hand-off. If you catch yourself about to write one,
STOP and put it in one of these instead:

- **tasks.md** — an open sub-task, a gotcha, or a calibration note on a step
  (the next stage works through this file);
- **design.md / proposal.md / the spec delta** — a decision, rationale, or a
  constraint on how something must be built;
- **the tracker issue** — the spec in the body, resume state and probe outcomes
  in a handoff comment;
- **the code itself** — a test's assertions plus a terse comment, or a
  pointer to a FUTURE issue that will change it (the only issue reference
  allowed in code) — for anything about how the code must behave.

A hard stop then states only which reset point we're at: everything the next
stage needs is already on disk or in the tracker, by construction.

## Commit at the end of every stage

At each stage's hard stop — after the stage's work is done, just before you
STOP — commit the files that stage created or changed, **without asking**. This
overrides any standing "don't commit, I'll commit" / "ask me each time"
preference, and it supersedes any "do NOT commit" wording in the stage
skills. What still holds:

- Stage ONLY **specific named file paths**. Name every file explicitly, and put
  them all in ONE command (`git add <path1> <path2> ...`), not one command per
  file. NEVER use `git add -A`, `git add .`, a glob, or a whole directory.
- **Commit only** — opening the PR still needs my explicit go-ahead
  (`pr-implement` Step 3 / the stopping policy above)

## Local test scope

Locally, run only the tests this change can affect; the full suite is CI's job.
The scope is:

- the files `la-affected-tests --base <base-branch>` prints (the PR's base
  branch once a PR exists, else the default branch): the tests this change
  added or changed, and every test whose imports reach a changed file;
- whatever else you judge this change reaches: goldens, conformance cases and
  snapshots pinning changed output, tests reading changed data or config files,
  everything under a changed fixture or conftest;
- every test CI reported failing on this PR.

Run them with the repo's test runner (the one behind `la-config get
commands.test`, keeping its usual options) narrowed to those files or test
ids, leaving out printed files the runner does not collect as tests (helpers,
fixtures). Never run the whole suite locally "to be safe"; a test missed here
is caught by CI.

## Normative harnesses (living-architecture repos)

In a repo whose `living-architecture.yaml` sets `architecture: true`, load the
`la:living-architecture` skill at EVERY stage of the flow and follow its
"Working under the architecture" rules; "the user" there is me. One addition
for this flow: wording quoted verbatim in the plan's decisions log as
`(user, approved wording)` is the per-change OK for that edit. Apply it
verbatim, and ask again only if it has to change.

## Rehydrate — pull in the tracker issue for the current branch

Read the repo's decisions from its config: `TRACKER=$(la-config get tracker)`
(`linear`, `github` or `none`) and `la-config get openspec`. Capture
`BRANCH=$(git rev-parse --abbrev-ref HEAD)`.

**`TRACKER=linear`.** Look up the Linear issue whose `gitBranchName` equals
`BRANCH` **exactly**. I create branches by clicking "Copy git branch name" in
the Linear issue UI and `git checkout -b`-ing them, so the local branch name is
byte-equal to the issue's `gitBranchName`. That equality is the join key.

1. Try the cheap path first: Linear's auto-generated branch name is
   `<user>/<lowercased-key>-<title-slug>` (e.g.
   `alice/abc-123-add-storage-layer`). Pull out the `<key>` chunk
   (`abc-123`), uppercase it (`ABC-123`), and call
   `mcp__linear__get_issue(id="ABC-123")`.
2. If that returns an issue **and** the returned issue's `gitBranchName`
   equals `BRANCH` exactly, use it. Otherwise fall back to
   `mcp__linear__list_issues(team="<KEY-PREFIX>", query="<key-or-slug>",
   includeArchived=false)` (`<KEY-PREFIX>` = the key's team part, e.g. `ABC`)
   and walk the results, comparing each issue's
   `gitBranchName` to `BRANCH`. Pick the unique exact match.
3. Once a match is confirmed, read the issue body in full
   (`mcp__linear__get_issue` already returns it) plus any comments via
   `mcp__linear__list_comments`.

**`TRACKER=github`.** GitHub's "Create a branch" names the branch
`<N>-<title-slug>`, so take the leading `<N>-` of `BRANCH` (after any
`<user>/` segment). The issue is `#<N>` iff `gh issue develop --list <N>` lists
`BRANCH` among its linked branches; GitHub has no reverse lookup, so this is
the only join. Read the issue with `gh issue view <N> --comments`.

**`TRACKER=none`.** There is no issue: the brief is my typed input alone.

If no issue maps to the branch (Linear: 0 exact matches; GitHub: no leading
number, or the branch is not linked to that issue), tell me so and ask whether
to proceed with only my typed input as the brief. If Linear gives >1 exact
matches, list them and ask which one.

**Set the change-id and OpenSpec.** `CHANGE_ID` = `$BRANCH` with any leading
`<user>/` segment stripped (`alice/abc-123-add-storage-layer` gives
`CHANGE_ID=abc-123-add-storage-layer`; OpenSpec change ids forbid underscores,
so replace any with `-`). This keeps issue ↔ git branch ↔ OpenSpec change
1:1:1. `OPENSPEC=1` iff `la-config get openspec` prints `true` (the preflight
already checked that `openspec/` agrees); otherwise `OPENSPEC=0`, and skip
everything marked *"OpenSpec repos only"* in the stage skills.

## Detect the stage

Work out which stage this session should run — first match wins:

1. **Open PR for `BRANCH`?** Check with `gh pr view --json state,url`.
   If an open PR exists → **`pr-review`**.
2. **No durable plan yet?** The plan is durable iff:
   - `OPENSPEC=1`: `openspec/changes/<CHANGE_ID>/` exists and
     `openspec validate <CHANGE_ID> --strict` passes; or
   - `OPENSPEC=0`: the tracker issue has a comment containing the finalized
     plan (Linear: `mcp__linear__list_comments`; GitHub: `gh issue view <N>
     --comments`).
   If not durable → **`pr-plan`**.
3. **No tests for this change yet?** Look for test files added/changed for
   this change: the working tree (`git status`) plus commits since the
   merge-base with the default branch
   (`git diff --name-only $(git merge-base HEAD <default-branch>)..HEAD`).
   If none → **`pr-tests`**.
4. **Otherwise** → **`pr-implement`** (plan and tests exist, no PR yet;
   this stage also covers the "all tests already pass, awaiting my
   PR go-ahead" case).

If the evidence is ambiguous (e.g. test files changed but they don't obviously
belong to this change), say what you found and ask me which stage to run.

## Dispatch

Tell me in one line which stage was detected and why, then invoke that stage's
skill (`la:pr-plan` / `la:pr-tests` / `la:pr-implement` / `la:pr-review`)
via the Skill tool and follow it to its hard stop. If I explicitly named a stage
when invoking `/la:pr`, that overrides detection.
