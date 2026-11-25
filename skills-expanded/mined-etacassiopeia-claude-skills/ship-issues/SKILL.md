---
name: ship-issues
description: "Orchestrate the full per-issue pipeline over a set of GitHub issues — triage -> fix-issue -> commit-push-pr -> babysit-prs -> merge — in a resumable serial loop that fixes-on-fail until each issue is merged. Triage gates on desirability first: an issue judged rejected-by-design or carrying an open should-question is never implemented. Cheap phases run on Haiku subagents; fix-issue runs on the session model. Issues triage routes to a model the session can't cover (e.g. design-heavy -> Fable) are deferred with a relaunch command. Usage: /ship-issues [<issue-number>...] [--all] [--label <name>] [--no-merge] [--force-model] [--admin-merge]"
user_invocable: true
argument-hint: "[<issue-number>...] | --all | --label <name> [--no-merge] [--force-model] [--admin-merge]"
allowed-tools:
  - Bash(gh issue view:*)
  - Bash(gh issue list:*)
  - Bash(gh pr list:*)
  - Bash(gh pr view:*)
  - Bash(git remote get-url:*)
  - Bash(git branch:*)
  - Bash(git status:*)
  - Bash(git worktree list:*)
  - Bash(git ls-remote:*)
---

## Live Context (loaded at invocation)

- **Args**: `$ARGUMENTS` (issue numbers and/or flags; empty → treat as `--all`)
- **Repo remote**: !`git remote get-url origin 2>/dev/null`
- **Current branch**: !`git branch --show-current 2>/dev/null`
- **My login**: !`gh api user --jq .login 2>/dev/null`
- **Open issues**: !`gh issue list --state open --json number,title,labels --limit 100 2>/dev/null`
- **My open PRs**: !`gh pr list --author @me --state open --json number,title,headRefName,baseRefName 2>/dev/null`

(The body fetches per-issue detail, per-PR state, and milestone/base rules itself — keep the
Live Context free of shell expansions and jq templates the permission checker rejects at preload.)

---

# Ship Issues — Orchestrator Loop

**Goal:** drive each issue in the worklist all the way to **merged**, unattended — implement it,
open a PR, watch CI, and when CI is green **merge**; when CI is red, fix and repeat until it merges
or a hard cap is hit. Do this for every issue in the worklist, one at a time, resumably.

This skill is a *conductor*. It writes no product code and diagnoses no build itself — it invokes
`triage-issue`, `fix-issue`, `commit-push-pr`, and `babysit-prs`, each of which already runs its
own verifier-first / watch-fix self-correcting loop. The conductor's jobs are: pick and order the
worklist, run the pipeline per issue, route each phase to the right model, respect the base-branch
rules, isolate failures so one bad issue never blocks the rest, and produce an auditable report.

## Guiding principles

- **Merge is the goal, not the PR.** By default the loop does not stop at "PR opened" — it babysits
  each PR to green CI and merges it, fixing-on-fail in between. `--no-merge` stops at green-CI PR.
- **But shipping the wrong thing is worse than shipping nothing.** Every other gate in this pipeline
  is a *can* question — is it specified, does it compile, is it green. Only 1a's desirability verdict
  asks whether it *should* exist, and an issue can be accurate in every factual claim and still be
  wrong. When that verdict says stop, the run stops for that issue and asks a person; it does not
  reason its way past it.
- **Serial, not parallel.** One issue at a time. `fix-issue` isolates each in its own git worktree,
  but PRs land on shared base branches; serial keeps merges conflict-free and the run legible. Do
  **not** fan out issues to parallel subagents.
- **The user's checkout is never touched.** Every issue is implemented in its own worktree under
  `.claude/worktrees/`, cut from `origin/<base>`. The loop never runs `git switch`/`checkout`/
  `reset`/`merge` in the main working directory: it stays on whatever branch the user left it on,
  with their uncommitted work intact. `git fetch` is the only git write the main repo needs.
- **Every issue starts from a fresh base.** Before implementing an issue, `origin/<base>` is fetched
  and the worktree is cut **from that remote ref** (Phase 1c), so it includes every previously-merged
  PR — and so it does NOT inherit whatever the user's checkout happens to be on. Combined with
  serial + merge-before-next, each issue builds on the latest code and conflicts
  are avoided rather than fought.
- **Failure is isolated, never fatal to the batch.** If an issue's `fix-issue` exhausts its 3-cycle
  cap, or its PR can't be driven green by `babysit-prs`, record the blocker and **move to the next
  issue**. Never merge red work; never abandon the remaining worklist because one issue failed.
- **Stack only real dependencies.** GitHub stacked PRs (*Phase 0 step 8*) are used **only** for issues
  that already depend on each other — dashboard `blocked_by`/`unblocks` edges, umbrella tranches,
  "depends on #X". Never stack unrelated issues: every layer above a blocked one becomes unmergeable,
  which trades the isolation principle above for a batch-wide blocker you manufactured yourself.
- **The base branch is chosen, never defaulted.** Follow the repo's milestone → base-branch map
  (*Phase 1b*). Defaulting every PR to `master` is a bug.
- **Authorization.** Invoking this skill **is** authorization to push, open PRs, **and merge** the
  worklist issues (merge delegates to `babysit-prs`, whose own merge-method and mergeability rules
  apply). Pass `--no-merge` if you want to review before merging.
- **Resumable & idempotent.** Progress is re-derived from GitHub each iteration (open PRs, merged/
  closed issues) plus a durable run-log, so the loop survives context compaction and a re-invoke
  simply continues where it left off — it never re-implements an issue that already has a PR, and
  never re-merges a merged one.

---

## Model policy — READ FIRST, it dictates how you launch this skill

There is one hard mechanical constraint: **`fix-issue` runs its entire main loop on whatever
top-level model this session was launched on, and a skill cannot switch the session's top-level
model.** Everything this orchestrator invokes *inline* (via the Skill tool) therefore shares the
session model. So the split is:

| Phase | Model | Mechanism |
|-------|-------|-----------|
| Orchestrator glue (this loop) | **session model** | runs inline; cheap (tool calls + short reasoning) |
| `fix-issue` (implementation) | **session model** | invoked **inline** → must be the session model |
| `triage-issue` | **haiku** | `Agent(model: 'haiku')` subagent |
| `commit-push-pr` | **haiku** | `Agent(model: 'haiku')` subagent |
| `babysit-prs` (watch-fix-merge) | **haiku** | `Agent(model: 'haiku')` subagent |

**⇒ Launch this skill on Opus.** That puts `fix-issue` (the only expensive phase, and the one you
want on Opus) on Opus, while the three cheap phases are delegated to **Haiku subagents** so they
bill at Haiku regardless of the session model. The orchestrator glue also rides on Opus, but it is
light — the saving that matters (heavy implementation on a strong model, everything mechanical on a
cheap one) is preserved. `fix-issue`'s *own* internal subagents still drop to haiku/sonnet as it
designs; this policy does not change that.

### Model routing & deferral (what happens when triage wants a different model)

`fix-issue` runs on the session model and cannot be switched per issue, so triage's per-issue model
recommendation is handled by **routing**, not by switching:

- **Session model *covers* the recommendation → run inline now.** A stronger session model is a safe
  substitute for a cheaper pick: an Opus session covers Opus / Sonnet / Haiku-recommended issues, so
  those are implemented in this run. (Never defer a trivial issue just to save a little on a cheaper
  model — the capability is already there.)
- **Recommendation is a *peer* model the session can't stand in for → defer.** Triage recommends
  **Fable** for design-heavy issues as a deliberate capability preference, not a downgrade; an Opus
  session is not a substitute for that intent. Such an issue is **not implemented** in this run: set
  `status=deferred(<model>)`, record it, and `continue`. At the end, deferred issues are grouped by
  model with an exact relaunch command (e.g. run `/ship-issues 14 22` in a **Fable** session).

  Concretely: `session=opus` defers `fable` picks; `session=fable` defers `opus` picks; a session
  defers any recommendation it does not itself cover. You (the running model) know your own identity —
  compare triage's pick against it.

- **`--force-model` overrides deferral:** implement every issue on the session model regardless of
  triage's pick (one-shot, no second session). Use when you'd rather run a design-heavy issue on Opus
  than launch a separate Fable batch.

**Delegating a phase to a Haiku subagent:** spawn `Agent` with `model: 'haiku'` and a prompt that
tells it to **invoke the named skill** for the given issue/PR and report back the result (PR number,
merged y/n, blocker). If a subagent cannot invoke skills in this harness, instruct it in the same
prompt to instead perform the phase's concrete steps directly (for commit-push-pr: commit per
`CLAUDE.local.md`, push, `gh pr create` against the chosen base; for babysit: `gh pr checks` watch,
fix-on-fail on the PR's own head, merge with the method matching the branch shape). Either path
bills at Haiku. Have the subagent return a compact structured result, not a transcript.

---

## Phase 0 — Parse args & resolve the worklist

### 0·claim — Claim a run slot before touching any shared state

More than one `/ship-issues` session can be live in the same repo at once, and other sessions may be
creating or deleting worktrees for unrelated reasons. Every run therefore claims a slot **before** it
writes a run-log, creates a worktree, or prunes the candidate set.

1. **Read `.rift-ship/ACTIVE-RUNS.md`** if it exists — the coordination record, one row per run:

   | run | batch | run-log file | status | owns these branches |

2. **Pick your run id**: highest id present + 1 (the first run in a repo is `1`).
3. **Claim a run-log file.** `worklist.md` belongs to whichever run already claims it. Take it only if
   it is unclaimed and no other run is `LIVE`; otherwise take `.rift-ship/worklist-run<N>.md`.
   **Never write, archive, rename or overwrite another run's log** — it is that run's only resume
   record, and archiving a live one mid-flight is the failure this whole step exists to prevent.
4. **Register your row** (`status=LIVE`, your batch, your log file, the branch patterns you will own).
   Create ACTIVE-RUNS.md with the header and these rules if it is absent.
5. **Edit only your own row.** ACTIVE-RUNS.md is shared mutable state: update your row in place, never
   rewrite the file wholesale, never restate another run's status. If you must record a cross-batch
   interaction that another run should know about, add it as a note section below the table and say
   which run wrote it.
6. **Release the slot in Phase 2** — set your row to `status=DONE (<YYYY-MM-DD>)`. A file full of stale
   `LIVE` rows is worse than no file: the next run learns to ignore it.

This costs about two file operations in the single-run case, which is the common one. Do it anyway —
the cost of discovering a second run *after* both have claimed `worklist.md` is a destroyed run-log
and two sessions implementing the same issue.

1. **Flags** (parse from `$ARGUMENTS`):
   - `--all` — every open issue (the default when no issue numbers are given).
   - `--label <name>` — restrict to open issues carrying that label.
   - `--no-merge` — stop at green-CI PR instead of merging (merge is otherwise the default).
   - `--admin-merge` — legacy no-op, forwarded to `babysit-prs` (1e). Babysit now admin-overrides a
     required-*review*-only block by default whenever you're a ruleset bypass actor (repo admin),
     even with other collaborators, so this flag no longer changes anything. CI must still be green
     and the PR MERGEABLE; the override never bypasses a red required check.
   - `--force-model` — defer nothing; implement every issue on the session model (see routing above).
   - Bare integers — an explicit issue list (overrides `--all`).
2. **Build the candidate set** from the Live Context *Open issues* (or an explicit list), applying
   `--label` if present.
3. **Resolve the repo's issue-branch convention — once, before anything matches against it.** Read
   the target repo's `CLAUDE.local.md` / `CLAUDE.md` for the branch-naming rule and derive a match
   pattern from it (rift's is `<type>/rift-<issue>-<slug>`). If the repo states no rule, fall back to
   matching any head branch that contains the issue number as a delimited token
   (`(^|[/-])<issue>([-_.]|$)`). This is not cosmetic: step 4 uses the pattern to detect an issue that
   **already has a PR**, so a convention mismatch silently re-implements the issue and opens a
   **duplicate PR**. Record the resolved pattern in the run-log header.

   (`.rift-ship/` is this skill's own state directory. The name is historical and does not assert the
   repo is rift — the directory is created in whatever repo the skill runs in.)
4. **Prune already-in-flight / done issues:**
   - Skip an issue that already has an open PR that closes it. Run **both** matchers — head branches
     from *My open PRs* against the step-3 pattern, and `gh pr list --search "<issue> in:body"` — they
     fail in different ways and a hit from either is enough. If such a PR exists and merge is enabled,
     hand it straight to Phase 1e (babysit) — don't re-implement.
   - **Skip an issue owned by another `LIVE` run** (from `0·claim`). Set `status=owned-by-run<N>` and
     leave it out of the worklist. This is the one case the two matchers above **cannot** catch: an
     issue being implemented in another run's worktree has no PR and no pushed branch yet, so live
     GitHub state reports it as untouched. That invisibility is exactly how two runs end up building
     the same issue twice. Corroborate with `git ls-remote --heads origin` against the step-3 pattern —
     a remote branch for the issue with no PR is an in-flight claim. But a matching remote branch that
     **no `LIVE` run owns** is a stale leftover from an abandoned run, not a claim: note it in the
     run-log and proceed normally.
   - Skip issues labeled `blocked`, `wontfix`, `needs-design`, or `question` unless named explicitly.
   - Skip issues labeled `needs-triage` (this is the hold-for-triage label the auto-filer applies —
     agent-found findings are not implemented until a human promotes them by removing that label)
     unless the issue is named explicitly in the args.
5. **Expand umbrella / tracking / epic issues — never implement them directly.** An umbrella issue
   describes a *plan enacted by other issues*, not a unit of work; handing its body to `fix-issue`
   would produce a monster PR and blow the fix cap. Detect an umbrella by **any** of:
   - a label like `epic`, `umbrella`, `tracking`, or `meta`;
   - native GitHub sub-issues (`gh api repos/{owner}/{repo}/issues/{n}/sub_issues`);
   - a task-list of issue refs (`- [ ] #NNN`) in the body **or comments**;
   - prose signals: "umbrella", "series of (small/additive) PRs", "tranche", "will link each PR
     here", "one per item".

   Prose signals are the weakest of the four — require a second signal, or an actual enumerable
   child list, before treating a prose-only hit as an umbrella. Misclassifying a normal issue as an
   umbrella drops it from the run silently (`umbrella-manual`), which is worse than attempting it.
   In particular, **"follow-up to #X" is not an umbrella signal**: a follow-up is an ordinary
   single unit of work that happens to reference its predecessor (use it for *ordering* in step 7,
   not for classification).

   On a hit, **decompose instead of implement**:
   - Enumerate children = native sub-issues ∪ task-list `#NNN` refs. Keep only the **open** ones
     (closed children are already done). Preserve the umbrella's stated order/tranches (e.g.
     "#316/#317/#318 first"; "depends on #X" first).
   - **Enqueue the open children** into the worklist (each runs the normal per-issue pipeline), and
     set the parent's `status=umbrella-expanded` — it is not implemented; it closes when its
     children do. Do not enqueue issues that merely *reference* the umbrella but aren't in its
     child list (those are related follow-ups → treated as ordinary standalone issues).
   - If **all** children are already closed → set `status=umbrella-done` and note "dischargeable —
     consider closing"; build nothing.
   - If an umbrella has **no machine-enumerable children** (pure-prose plan) → set
     `status=umbrella-manual` and skip; it needs a human to split it into issues first.
6. **Consult the delivery dashboard, if one is configured.** Discover it exactly as *Phase 2.5* does
   (explicit `dashboard.path` in the repo's `CLAUDE.local.md`; else `.rift-ship/dashboard-path`; else
   a discoverable *Delivery Dashboard* note with a `db/` issue folder). **No dashboard → skip this
   step silently**; everything below is a no-op without one.

   Phase 2.5 already *writes* this graph — `blocked_by` / `unblocks` edges and `kind: release` /
   `kind: consume` gate nodes. Reading it back here is what makes it a dependency graph instead of a
   write-only log:
   - **Screen out issues blocked upstream.** An issue whose `blocked_by` names an issue that is still
     **open**, or an unclosed release/consume gate, is not workable in this run: set
     `status=blocked-upstream(<what>)`, record it, and leave it out of the worklist. Without this
     screen the issue is attempted anyway, burns a full `fix-issue` cycle, and fails for a reason the
     graph already knew — a merge is not a delivery, and an `awaiting-release` downstream cannot be
     implemented against a version that isn't published yet.
   - **Order by the edges.** Order the survivors so that an issue which `unblocks` others comes first.
     Prefer these edges over the prose-scraped "depends on #X" of step 7 — the graph is the maintained
     version of the same information; prose is the fallback for issues the graph doesn't cover.
   - **Distrust stale edges.** An edge naming an issue that GitHub reports **closed** is stale: ignore
     it rather than blocking on it, and note it for the Phase 2.5 refresh. The graph is an input, not
     an authority — live GitHub state wins every disagreement.
7. **Order** the worklist: explicit arg order if given; else the dashboard edge order from step 6;
   else ascending issue number. If an issue body says "depends on #X" (and step 6 produced no edge
   for it), put #X earlier. Keep expanded-umbrella children in their tranche order.
8. **Identify stackable groups (GitHub stacked PRs) — only where a dependency already exists.**
   A *stackable group* is an ordered run of **≥2** worklist issues where each depends on the one
   before it: consecutive children of an expanded umbrella sharing a tranche order (step 5), issues
   joined by dashboard `blocked_by`/`unblocks` edges (step 6), or a prose "depends on #X" (step 7).
   Everything else stays an ordinary independent PR cut from `origin/<base>`. **Do not stack
   unrelated issues** — see the guiding principle; a stack is a dependency you are asserting, and
   asserting a false one costs you the batch's failure isolation.

   **Probe the capability once, before planning any stack:**

   ```sh
   gh extension install github/gh-stack   # once per machine; no-op if already installed
   gh stack view --json                   # exit 9 = stacked PRs not enabled for this repository
   ```

   Exit `9`, an extension you cannot install, or any doubt → **no stacks this run**: every issue takes
   the ordinary path and nothing below changes. Record `stacks: off — <why>` in the run-log header.
   Stacked PRs are in public preview, so absence is a normal outcome, not a degraded one — never
   block a run on it.

   For each group you do form, assign a stack id (`S1`, `S2`, …) and number the layers **bottom-up**,
   and record `stack:S1 layer 2/3` in each member's run-log notes. The bottom layer behaves exactly
   like an unstacked issue; the layers above it differ in base (1b), worktree origin (1c), link (1d),
   verification (1d-verify) and merge order (1e), and nowhere else.
9. **Write the run-log** at the path you claimed in `0·claim` — `.rift-ship/worklist.md` when you own
   it, else `.rift-ship/worklist-run<N>.md` (create the dir): a header line recording the run's id,
   mode, the step-3 branch pattern and the step-8 `stacks:` outcome, then one row per issue with columns
   `issue | title | base | status | pr | attempts | gate | docs | downstream | notes`, all
   `status=pending` and `attempts=0`. Where each column is filled: `gate` at 1c, `docs` at 1c-docs,
   `downstream` at 1f-cross, `attempts` incremented on every `fix-issue` invocation at 1c. The escalation outcome is written
   **inside the `attempts` cell**, not in `notes`: a 1e→1c escalation reads `2 (esc:rescued)` or
   `2 (esc:failed)` once its outcome is known. This file is the
   durable source of truth for resume **and the only record the Phase 2 report can be built from** —
   update it after every phase transition.
10. **Announce the plan**: print the ordered worklist (noting any umbrella expansions, any
    `blocked-upstream` skips, and any stackable groups with their layer order) and the mode (merge vs
    `--no-merge`). Then begin the loop.

---

## Phase 1 — Per-issue pipeline (loop over the worklist, serial)

For each issue **N** with a non-terminal status, run steps a–g. On any hard failure, set the
issue's status, write the run-log, and `continue` to the next issue — never abort the whole loop.

**Re-read the run-log at every issue boundary — do not carry the plan in conversation memory.** A
long batch will cross one or more context compactions, and a compaction summarises the transcript:
the ordering, the `attempts` counters, and which issues are already terminal are exactly the details
a summary flattens. Re-reading is a few hundred tokens and makes the loop's behaviour identical
either side of a compaction, which is the property the run-log exists to provide. Concretely, at the
top of each iteration: re-read your run-log, take the first non-terminal row as N, and trust that file
over anything you remember. If the log and your recollection disagree, **the log is right** — and if
the log disagrees with live GitHub (a PR you don't remember opening), GitHub is right and the log
needs correcting. This is also what keeps a batch's later issues as carefully done as its first.

### 1·coord — Coordinator: pipeline the CI waits (repo-aware, decide ONCE up front)

Implementation is **always serial** — `fix-issue` runs inline on the session model, one issue at a
time. But the ~per-PR **CI wait** in step 1e is dead time in a strictly-serial loop: on a repo whose
CI takes 15+ min, blocking on each merge before starting the next issue wastes that window. The win
is to overlap it — implement issue N+1 *while* N's CI runs — but only when it actually pays off and
won't trigger a rebase cascade. So before the loop, the coordinator makes **one** decision:

**Measure two facts about the target repo:**
1. **CI duration** — recent successful run wall-clock: `gh run list --limit 10 --json name,conclusion,startedAt,updatedAt` (or observe the *first* PR you open this run). Call it long if the required checks take **≳ 8–10 min**, short if **≲ a few min**.
2. **Does merging require an up-to-date branch / required status checks?** Check both classic protection (`gh api repos/{o}/{r}/branches/{base}/protection` → `required_status_checks.strict`) and **rulesets** (`gh api repos/{o}/{r}/rulesets` then the ruleset detail → any `required_status_checks` rule with `strict_required_status_checks_policy`). "Strict/up-to-date required" means every merge invalidates the other open PRs' mergeability → forced rebase + CI re-run for each.

**Choose the mode:**
- **Strictly serial** (default; the safe choice) when CI is **short**, OR the repo **requires
  up-to-date branches / required status checks**. Run 1a–1e inline per issue, babysit each PR to
  merged **before** starting the next (as written below). Short CI ⇒ the coordination isn't worth
  the complexity; strict-branch ⇒ pipelining just moves the wait into a rebase cascade. Say so in
  the run-log (`pipeline: off — CI ~3m` / `pipeline: off — strict branches`).
- **Pipelined fan-out** when CI is **long** AND up-to-date is **not** required AND required status
  checks are absent/bypassable (you're an admin). Then:
  1. Run **1a–1d, including 1d-verify, serial and inline** per issue (triage → base → implement →
     commit-push-pr → verify the push). Opening the PR starts its CI. Do **not** run 1e yet — move
     straight to the next issue so the CIs stack up and run concurrently. 1d-verify stays with 1d and
     is never deferred to the merge sweep: it needs the issue's worktree, which is still current at
     this point, and its whole purpose is to stop a partial push before CI's green result makes it
     look finished.
  2. After the last issue's PR is open, do a **merge sweep**: merge the PRs one at a time in worklist
     order (1e per PR). Because up-to-date isn't required, merging one does **not** invalidate the
     others — no rebase cascade. The only cross-PR conflict is a **shared file**, almost always
     `CHANGELOG.md`: resolve it by rebasing that one PR onto the new base and keeping *both* entries
     (place each issue's entry under a distinct changelog subsection — `Fixed`/`Security`/`Changed` —
     so git 3-way usually auto-merges them and no rebase is even needed). Since CI isn't merge-
     required here, a CHANGELOG-only rebase can merge as soon as it's mergeable without re-waiting a
     full CI re-run (the code was already green pre-rebase). **Within a stacked group this conflict
     cannot arise** — layer *k+1* already contains layer *k*'s changelog entry, because it is based on
     it. The resolution above applies only between independent fanned-out PRs.
  3. Keep the merge sweep **serial** — never fan out concurrent background merges that rebase onto a
     moving base (they race). Record `pipeline: on — CI ~15m, fan-out N PRs, merge sweep`.
  4. Re-sync the knowledge graph **after each merge in the sweep** (1g), not once at the end. The
     later PRs in the sweep are the ones most likely to be queried against a graph that predates the
     earlier merges.

- **Stacked (per group; orthogonal to the two modes above).** For each stackable group from *Phase 0
  step 8*, run 1a–1d per layer back-to-back — serial and inline, as always — and merge the layers
  bottom-up in one sweep (1e). This is what makes fan-out available in the **strict-branch** case the
  first bullet otherwise excludes: a layer is up-to-date with respect to *its own* base by
  construction, so merging the layer beneath it does not invalidate it, and GitHub rebases and
  retargets the layers above automatically instead of you fighting a cascade. Record e.g.
  `pipeline: off — strict branches; stacks: S1 (3 layers) fanned out`.

  What this does **not** change: implementation stays serial, and each layer's PR is still babysat to
  green individually before the layer above it merges. Stacking removes the *rebase cascade*, not the
  per-PR green gate.

Never pipeline the *implementation* (fix-issue is inline/serial by construction), and never merge a
red or unmergeable PR. When in doubt, stay strictly serial — it is always correct, just slower.

### 1a — Triage & route (Haiku subagent)
Delegate `triage-issue` for N to a **Haiku subagent**. It returns **two** verdicts — desirability
first, then model. Use them to:

1. **Honour the desirability verdict — this gate comes first, and it is not overridable by
   `--force-model`** (that flag governs which *model* implements an issue, never whether it should
   exist).
   - `rejected-by-design` → set `status=rejected-by-design`, record the should-question and the
     recorded principle it cites, and `continue`. **Do not implement.** Surface it in the Phase 2
     report with the recommendation to close the issue as *not planned* — and note anything the repo
     is still advertising (a pending panel, a stub, a doc promise), because a capability that is
     never coming should stop being promised.
   - `question-design` → set `status=needs-design(should)`, record the one-sentence should-question
     verbatim, and `continue`. **Do not implement.** This is a question for a person, and the whole
     value is asking it *now*, while declining costs one comment rather than a merged PR.
   - `build` → proceed to (2).

   Neither counts as a failure for the circuit breakers — like `deferred`, they are correct skips.

   **Do not soften a desirability verdict because the issue looks well-written.** An issue can be
   precise, well-researched and factually correct in every claim and still be rejected: that is the
   exact shape of `achird-labs/rift-cluster` #365/#366, which cleared implementability triage and
   independent premise checks before a human refused them outright.

2. **Screen out non-implementable issues** — if triage says the issue needs human design or is a
   question/underspecified, set `status=needs-design` and `continue`.
3. **Route by model** per *Model routing & deferral* above: if the session model covers triage's
   recommendation (or `--force-model` is set), proceed on the session model. If triage recommends a
   peer model the session can't cover (e.g. **Fable** for a design-heavy issue on an Opus session),
   set `status=deferred(<model>)`, record it, and `continue` — do not implement it in this run.
4. **Note complexity** in the run-log.

### 1b — Choose the PR base branch
Determine the base **before** implementing, from the **target repo's** convention (this skill runs
in any repo, so don't hardcode rift's rules):
- Read the repo's `CLAUDE.local.md` / `CLAUDE.md` for a base-branch rule. Some repos map
  issue → milestone → base branch (e.g. rift: "PR base branch — do NOT default to master", with
  per-milestone epic branches). If such a rule exists, follow it.
- If the repo has **no** such rule, default to the repo's **default branch** (`main`/`master`, via
  `gh repo view --json defaultBranchRef`).
- Epic-branch targets (when the rule requires one): if the epic branch doesn't exist yet it must be
  created off the default branch and pushed first. If that setup can't be done safely unattended,
  record it as a blocker and `continue` rather than opening a PR against the wrong base.
- **A stacked layer bases on the layer below it, not on `<base>`** (*Phase 0 step 8*). Layer *k+1*'s
  PR targets layer *k*'s head branch; only the bottom layer targets the group's real base branch. An
  umbrella whose children form a stack often needs **no epic branch at all** — the stack is what the
  epic branch was hand-rolling, minus the create-and-push setup and minus the unreviewable
  epic→default mega-PR at the end.
- Record the chosen base in the run-log's `base` cell — for a layer, the **predecessor's branch name**
  (`fix/rift-331-…`), not `master`. That cell is what tells a resumed run this PR is a layer rather
  than a stray mis-targeted PR.

### 1c — Sync the base, then implement (Opus, inline)

**Fetch the remote tip so the new work is cut from the latest code — but never touch the user's
checkout.** Because the loop is serial and (by default) merges each PR before the next issue starts,
every previously-shipped PR is already on the remote base by now; branching from `origin/<base>` is
what picks it up, and it is also what keeps the user's working directory out of the blast radius:

- `git fetch origin` so `origin/<base>` is current (this is the remote tip that includes every
  merged PR). Fetch is read-only — it updates remote refs and nothing else.
- Ensure `fix-issue` cuts its **isolated worktree directly from `origin/<base>`**:
  `git worktree add <path> -b <branch> origin/<base>`. The explicit `origin/<base>` is mandatory —
  without it the worktree branches from whatever the user's checkout has checked out, so a leftover
  feature branch silently becomes the base and its commits ride along into the PR.
- **Never `git switch` / `git checkout` / `git reset` / `git merge` in the user's checkout.** It
  stays on whatever branch they left it on — the loop has no business moving it. Do not
  "fast-forward the local base for cleanliness": it is not needed (you branch from `origin/<base>`,
  never from the local base), it silently changes the branch under the user's editor, and it fails
  outright the moment their tree is dirty. A stale local base is harmless because nothing ever
  reads it.
- **For a stacked layer, cut from the predecessor's branch instead of the base:**
  `git worktree add <path> -b <branch> origin/<layer-k-branch>` (after the same `git fetch origin`).
  The predecessor's branch is already pushed by the time you get here — 1d runs for layer *k* before
  layer *k+1* starts — so the remote ref exists. Everything else about 1c is unchanged, including
  that each layer still gets its **own** worktree and that the user's checkout is never touched.
- The **only** writable working directories this loop has are the per-issue worktrees under
  `.claude/worktrees/`. If a step seems to require editing the user's checkout, that step is wrong.

> Freshness holds only when PRs actually merge before the next issue — i.e. the default merge mode.
> Under `--no-merge`, earlier PRs stay open, so a later issue's base won't include them; that's
> inherent to `--no-merge`, not a bug.
>
> A stacked layer is the deliberate exception: it inherits its predecessor's work through its **base
> branch** rather than through a merge, which is the entire point of the stack — and is why a stacked
> group is the one shape that stays coherent under `--no-merge`.

Then invoke the **`fix-issue`** skill for N **inline** (so it runs on the Opus session model). It
runs verifier-first in an isolated worktree with a hard cap of 3 fix cycles. Increment the issue's
`attempts` in the run-log as you invoke it — that counter is what the Phase 2 report and the caps
below both read, and it is only correct if it is written here, at the invocation.
- **Success** (verify gate green, no unresolved review blockers) → proceed to 1c-docs.
- **Failure** (cap exhausted / Remaining Blockers Report) → set `status=blocked`, copy the blockers
  summary into the run-log notes, and `continue`. Do **not** open a PR for broken work.

**Record the gate's shape in the `gate` cell**, from `fix-issue`'s ship report: the number of tests
added and the total (`+9/214`), plus a mutation result when the sub-skill produced one
(`+9/214 mut 6/7`), else just the counts. This costs one number copied out of a report you already
have, and it is the only thing in the run-log that describes the *quality* of what shipped rather
than the fact that it shipped. Without it, every merged issue reads identically whether its gate was
nine discriminating tests or one that asserts `true`, and questions about whether the loop's gate
discipline is actually working — or whether a cap should move — have no evidence behind them but
impressions. Blank it (`gate: —`) for issues that never reached 1c.

**1c-docs — Documentation is part of "done" (before you leave 1c).** A change that ships new or
changed behaviour is not complete until the docs a user or maintainer would consult are updated **in
the same worktree, so the docs land in the same PR** as the code. `fix-issue` often does this when
the issue's acceptance criteria name it, but its coverage is issue-dependent — so treat docs as an
explicit gate here, not an afterthought. In the worktree, before 1d:

- **Decide what's relevant.** Map the change to the docs that describe it: user-facing docs
  (`docs/`, `README`, guides, a DSL/API reference), the public API's own doc comments/Scaladoc, a
  `CHANGELOG`/release notes if the repo keeps one, `--help`/usage text for a CLI, and config/env
  references for new knobs or flags. Look at how *sibling* features are documented and match that
  home and depth (e.g. a new combinator gets an entry alongside the existing ones, a new env var
  joins the existing table) rather than inventing a new location.
- **Update or add it**, then re-run the verify pipeline (docs can break a docs-build/link-check or a
  fenced code sample that's compiled) so the docs change is covered by the same green gate as the
  code. Keep examples runnable and consistent with the shipped API.
- **Exempt** only genuinely doc-less changes — a pure-internal refactor, a test-only fix, a CI/build
  tweak with no user-facing surface. When you exempt, say so in the run-log (`docs: n/a — <why>`);
  don't skip silently.
- Record what you touched in the run-log (`docs: <files>`), and include the doc change in the 1d PR
  body so a reviewer sees the behaviour and its documentation together.
- **Design of record** (only when the repo has the design-sync practice — `scripts/design-check.py`
  exists or CLAUDE.md declares `design-check:`): run `python3 <design-check> --diff <worktree>`;
  every document under CODE → DESIGN marked `[NOT changed]` is either confirmed still accurate or
  amended in this worktree (a `D-n` in `docs/decisions/DECISIONS.md` + `> **Amended by D-n**`
  callout + code citation + test pin). Then `python3 <design-check> --strict` must exit 0. The
  1d PR body carries exactly one of `Design: unchanged — <docs>, confirmed` / `Design: amended —
  D-n` / `Design: n/a — <why>`; record the same in the run-log (`design: …`). A decision the
  user or a reviewer made during this issue that is not a `D-n` by 1d is a blocker, not a
  follow-up.

### 1d — Commit, push, open the PR (Haiku subagent)
Delegate **`commit-push-pr`** for N's worktree/branch to a **Haiku subagent**, targeting the base
from 1b. It must follow `CLAUDE.local.md`: branch name matching the convention resolved in Phase 0
step 3 (rift's is `<type>/rift-<issue>-<slug>`), conventional-commit message (no Claude attribution in
the body), PR title = issue title, body with `Closes #N` + milestone. Record the PR number/URL in the
run-log; set `status=pr-open`.

The branch it *creates* and the pattern a resume run *matches against* must come from that one
resolved rule. If they diverge, a resumed run fails to see the existing PR and re-implements the
issue.

**1d-link — Register the stack on GitHub (topmost layer of a stackable group only).** Once the
group's top PR is open, link the whole chain in a single call, bottom-to-top:

```sh
gh stack link --base <base> <pr-bottom> <pr-next> … <pr-top>
```

`gh stack link` registers the stack **without local tracking**, which is the only variant compatible
with this loop: each layer lives in its own worktree, whereas `gh stack add` / `gh stack submit`
assume one tracked checkout they would fight for. **Do not use those commands here**, and do not
introduce a shared stack worktree — the per-issue worktree is what gives `fix-issue` its isolation.

If the link fails (exit `4` API failure, or `9` if the step-8 probe went stale), the PRs are still
valid chained PRs and the run continues unchanged: record `stack:S1 link failed — exit <code>` in the
run-log and move on. The merge order in 1e does not depend on the link — only the stack map in the UI
and `gh stack` conveniences do. Retargeting on merge is a property of the chained bases, not of the
registration.

**1d-verify — Confirm the PR actually contains the work that was verified.** `fix-issue` verified the
change in the worktree on the session model; a *different*, cheaper agent then committed and pushed
it. Nothing up to this point has checked that what landed on the remote is what was verified — and a
**green CI on a commit that omitted half the change is a perfectly consistent outcome**, not a
contradiction. A green check and a merge commit are both compatible with the work not being there.
Close the gap before babysit ever sees the PR:

- In the worktree: `git rev-parse HEAD` and `git diff --stat origin/<base>...HEAD`.
- On the remote: `gh pr view <pr> --json headRefOid` and `gh pr diff <pr> --stat`.
- The head SHAs must be equal, and the two file lists must match (per-file line counts within
  rounding).

**Stacked-layer carve-out.** Run this check where it already sits — **immediately after the push, and
before any layer beneath it merges** — and it works unchanged, because nothing has rewritten the PR
yet. What you must **not** do is re-run the SHA-equality half of it on a stacked layer *later* in the
run: once the layer below merges, GitHub rebases and retargets this PR, so its remote head
legitimately differs from the local worktree HEAD with no push involved. A later re-check compares the
**diff** (`gh pr diff <pr> --stat`, against the new base) and never the SHA. Reading a post-retarget
SHA change as a partial push is the exact mirror of the error this step exists to prevent — and it
would block a PR that is fine.

A mismatch means the push was partial — unstaged files, a new file swallowed by `.gitignore`, a commit
that was never made, or a push that raced the PR creation. Do **not** hand it to babysit: return to the
worktree, commit and push what is missing, and re-check. If it still mismatches after one correction,
set `status=blocked`, put **both file lists** in the run-log notes, and `continue`. An unexplained
mismatch is precisely the case where proceeding yields a merged PR that does not contain the feature,
and the merge makes it look finished.

### 1e — Babysit to merged (Haiku subagent) — default
**In pipelined mode (1·coord), 1e is deferred:** don't babysit here — move to the next issue and run
all the 1e merges together in the end-of-run merge sweep. In strictly-serial mode, run 1e inline now.

Unless `--no-merge`, delegate **`babysit-prs`** for this PR to a **Haiku subagent** (forwarding
`--admin-merge` if it was passed). It watches CI, fixes-on-fail on the PR's own head up to its own
3-cycle cap, and merges when green using the merge method matching the branch shape. babysit reads
the branch's **ruleset** (not just legacy branch protection) to classify a `BLOCKED` PR, and —
whenever you are a ruleset **bypass actor** (repo admin), regardless of other collaborators —
admin-overrides a required *review* it can't self-satisfy (green CI is still required).
- Merged → `status=merged`.
- babysit hard-stops (still red after its cap, or unmergeable) → `status=pr-red`, note why, `continue`.

If a CI failure roots in an implementation defect the Haiku babysit can't fix, it must say so in its
structured result **and include the diagnosis it did reach**: the failing check, the distinguishing
error lines (not the whole log), the file or symbol it suspects, and what it already tried. The
orchestrator may then re-run `fix-issue` (1c) **inline on the session model** for that issue once more
before giving up (this counts against the issue's overall attempts — see caps below) — and when it
does, it **passes that diagnosis into the re-run's prompt** and writes the outcome into the run-log's
`attempts` cell as `2 (esc:rescued)` or `2 (esc:failed)`. That retry is the issue's last attempt;
spending it re-deriving a failure Haiku already characterized wastes the single escalation the loop
has, and a re-run that starts from zero often reproduces the same wrong hypothesis.

With `--no-merge`, skip 1e and leave the green-CI PR for review; `status` stays `pr-open`.

**Stacked groups merge bottom-up, one layer at a time.** Babysit layer 1 to merged, then layer 2, and
so on; each layer gets its own green-CI gate exactly as an unstacked PR does. Expect every surviving
layer's CI to **re-run after the layer below it merges** — GitHub rebases and retargets it, so that is
a genuinely new commit under test, not a flake, and the layer is not mergeable until the new run is
green. Budget for it: an *n*-layer stack costs *n* CI rounds on its top layer in the worst case.

**Do not use `gh stack merge` to land a group in one shot.** It merges a PR plus every unmerged layer
beneath it, which skips the per-PR green gate this loop is built on ("never merge red work"). It is a
fine convenience for a human eyeballing a finished stack; it is not the unattended path.

**A blocked layer blocks everything above it.** If layer *k* ends `blocked`/`pr-red`, set every layer
above it to `blocked-upstream(stack:S<id> layer <k>)` and leave their PRs open — they are correct
skips, not failures, and like every `blocked-upstream` they count toward neither circuit breaker.
Layer *k* itself still counts as the failure it is. Do **not** retarget the orphaned layers onto the
real base to rescue them: their diffs assume the layer below, so a retarget produces either a conflict
or, worse, a clean merge of an incoherent change.

### 1e·mem — Failure memory (consult before diagnosing, record after)

A CI diagnosis is expensive to produce and currently dies with the run. The next run re-derives "this
is the known-flaky chaos-tier suite" from scratch, and — worse — a genuine regression that *resembles*
a known flake gets waved through as one. Give the loop somewhere durable to put what it learned:

- **Before** babysit diagnoses a red check, hand it the known-failure list so it can match first:
  `graphify query "CI failure <check-name> <first error line>"` in repos that have a graph, else read
  `.rift-ship/failures.md`. A match is a *hypothesis to confirm*, never a verdict.
- **After** any diagnosis that reached a root cause, record one entry: the failure **signature**
  (check name plus the distinguishing error line), the **root cause**, the **fix**, and the **PR or
  issue** it came from. Append to `.rift-ship/failures.md`; in graphify repos also
  `graphify save-result --question "CI: <signature>" --answer "<cause> → <fix>" --outcome useful`.
- **Record the misses, not just the hits.** A signature that matched a past entry but turned out to
  have a different cause is the most valuable entry in the file — write it with `--outcome corrected`
  and state what was actually true. A memory that only hears about its successes teaches the next run
  to be confidently wrong.
- **Flake vs. regression is settled by evidence, not resemblance.** Before writing a failure off as a
  known flake, confirm the failing run's head SHA is the same commit as the green run you are
  comparing it against. Two runs minutes apart on different SHAs are not a re-run of the same test,
  and treating them as one is how a real regression gets merged. **On a stacked layer there is a third
  reading**: the head SHA can change without a push and without a flake, because a lower layer merged
  and GitHub rebased this one. Check for that retarget before concluding either "flake" or
  "regression" — the correct verdict there is "different commit, genuinely re-tested".

### 1f — Harvest & file findings (out-of-scope discoveries)
While implementing (1c) and diagnosing CI (1e), the sub-skills routinely surface **concrete,
out-of-scope defects or gaps** that are worth a fix but must not derail the issue in hand — the
racy FSM transition and the stuck-pending leak in #310 are exactly this kind of discovery. For each
such finding, delegate to the **`file-finding`** skill (a **Haiku subagent**), passing the finding,
its evidence, a proposed fix, and the source (this issue / the PR). It dedups against open issues,
files with `agent-found` + `needs-triage`, and returns `filed #<n>` / `duplicate of #<n>` /
`no finding worth filing`.

Findings are **held for triage**: they carry `needs-triage`, so Phase 0 excludes them from a later
`--all` run until you promote them. This prevents a runaway find→fix→find loop while still capturing
everything. Record filed/duplicate finding numbers in the run-log notes for this issue.

### 1f-cross — Downstream-consumer impact (only when the repo declares consumers)

An engine/library repo is rarely the last stop: SDKs, conformance suites, sample corpora and
example harnesses consume its wire schemas, ABI, config format and CLI. A change can be perfectly
green here and still leave those repos stale — or leave its own value unrealized. **Skip this step
entirely when the repo declares no downstream consumers** (see discovery below); do not invent them.

**Discovery.** Read the repo's `CLAUDE.local.md` / `CLAUDE.md` for a *Downstream consumers* section
listing consumer repos and the surfaces each one consumes. No section → skip, silently.

**Cheap gate first.** Most issues touch nothing a consumer sees. Compare the merged diff's files
against the declared surfaces; if none match, record `downstream: none — no consumed surface
touched` and move on. Only on a match do the deeper analysis below (delegate it to a **Haiku
subagent**: give it the diff, the declared consumer map, and these rules).

**The trap this exists to catch: "additive" is not "nothing to do".** A backward-compatible
addition breaks no consumer *and* is invisible to every one of them until they adopt it — so the
feature ships and nobody uses it. Judge each consumer on two separate questions:

- **Compatibility** — does anything there *break* or silently misbehave? (A schema gaining a field
  under `deny_unknown_fields` means a new-SDK-on-old-engine call is a hard error, so adoption must
  be version-gated. A new error code/status a consumer maps. A changed response body.)
- **Adoption** — where does this change's *value* actually land? If the point of the work is that a
  consumer can now delete a workaround, that deletion is the deliverable, and it lives over there.

For each real item, file an issue **in that repo** (`gh issue create --repo <owner>/<name>`), with
the same discipline as 1f: dedup first, state the engine version/PR that introduced it, say plainly
whether it is *required* (compat) or *optional* (adoption), and label it for human triage. Never
implement it in this run — different repo, different gate, different review.

Record one line per consumer in the run-log (`downstream: rift-java #12 (adoption), rift-go none`),
and surface it in the Phase 2 report.

### 1g — Checkpoint, and re-sync the knowledge graph if anything merged

Update **your run's** run-log (`0·claim`). This run-log + live GitHub state is enough to resume after
compaction: a re-invoke re-reads it, re-prunes against open PRs/merged issues, and picks up the
first non-terminal issue.

**Then, if this issue's PR merged, re-sync the repo's knowledge graph.** A PR merges on GitHub, so
nothing happens locally: the main checkout's HEAD never moves and no git hook ever fires. This is
the one point in the loop hooks genuinely cannot cover, so it is an explicit step — skip it and
every later issue in the batch (and every later session) queries a graph that predates the merge,
which is exactly when a stale answer is most likely to be believed.

In a repo with a `graphify-out/` directory:

```sh
~/.claude/graphify/bin/graph-sync.sh            # fetch + graphify update + label --missing-only
```

Two things to know about it:

- **It only fetches; it never moves the user's HEAD.** So if the main checkout is behind
  `origin/<base>` — which it will be, since the loop never advances it — `graphify update` re-extracts
  from a working tree that predates the merge and the sync achieves nothing. Check first
  (`git -C <main> rev-list --count HEAD..origin/<base>`). When the checkout is **clean, on the base
  branch, and 0 commits ahead**, a `git merge --ff-only origin/<base>` is safe and is what makes the
  sync meaningful — it is a fast-forward to work the user just merged, not a rewrite. If the tree is
  **dirty**, or the branch is **ahead**, or it is **not on the base branch**, do NOT touch it: run
  the sync anyway, and say in the run-log that the graph is only as fresh as the checkout.
- Run it **once per merge**, not once per run. In pipelined mode that means inside the merge sweep,
  after each PR merges — not only after the last one.

No `graphify-out/` → skip silently; this is a no-op in repos without a graph.

---

## Phase 2 — Final report

When every issue is in a terminal status (`merged` / `pr-open` / `deferred(<model>)` /
`rejected-by-design` / `needs-design(should)` / `needs-design` / `blocked` / `pr-red` /
`blocked-upstream(<what>)` / `owned-by-run<N>` / `umbrella-expanded` / `umbrella-done` /
`umbrella-manual`), print a summary table:

| Issue | Title | Base | Status | PR | Attempts | Gate | Docs | Downstream | Notes |
|-------|-------|------|--------|----|----------|------|------|------------|-------|

The **Gate** column carries each implemented issue's tests-added/total (and mutation result where
one exists) from 1c. Read down it: a batch whose merged issues all show one or two added tests is
telling you the gate is tracking the issue's bullet list rather than the change's real surface, and
that is visible here and nowhere else.

The **Docs** column records the doc outcome from 1c-docs for each implemented issue — the files
touched, or `n/a — <why>` when genuinely exempt. It makes the "docs are part of done" gate auditable
at a glance; a merged issue with a blank Docs cell is a smell to flag, not to hide.

The **Downstream** column does the same for 1f-cross: the consumer issues filed (`rift-java #12`),
`none — no consumed surface touched`, or `n/a` in a repo that declares no consumers. Same reasoning:
a merged issue that changed a consumed schema and shows a blank cell is a smell.

State the **stacks** outcome in one line (*Phase 0 step 8* / 1d-link): the groups formed, their layer
order, whether `gh stack link` succeeded, and how many layers merged — `stacks: S1 = #331→#332→#333,
linked, 3/3 merged` — or why none were formed (`stacks: off — gh-stack not enabled (exit 9)`;
`stacks: none — no dependent groups in worklist`). Without this line, a run whose stacks all merged
and a run that silently formed none read identically.

State the **graph sync** outcome in one line too (1g): whether the knowledge graph was re-synced
after the merges and what it rebuilt to (`graph: synced — 2915 nodes / 119 communities @ <sha>`), or
why it was not (`graph: stale — main checkout dirty, not fast-forwarded`; `graph: n/a — no
graphify-out/`). A run that merged work and left the graph pointing at the pre-merge tree should say
so, because the next session's first query will silently answer from it.

Then, grouped for action:
- **Merged**: PR links.
- **PR open, CI green** (`--no-merge`): PR links to review & merge (or `/babysit-prs <n>`).
- **Deferred (wrong model)**: grouped by recommended model, with one exact relaunch command per
  group — e.g. "design-heavy → Fable: run `/ship-issues 14 22` in a Fable session".
- **Umbrellas**: `umbrella-expanded` (list the child issues enqueued), `umbrella-done`
  (dischargeable — suggest closing), `umbrella-manual` (needs a human to split into issues).
- **rejected-by-design**: issues triage judged should not be built, each with the should-question and
  the recorded principle it contradicts. Recommend closing as *not planned* — and name anything the
  repo still advertises for them (a pending panel, a stub, a doc promise), since a capability that is
  never coming should stop being promised. These are **not failures**; a run that refuses a bad issue
  did its job.
- **needs-design(should)**: issues where a *should*-question is open and unanswered. State the
  one-sentence question verbatim — the whole point is that a person can answer it in one reply.
  Distinguish these clearly from `needs-design` below: that one means "we do not know *how*", this
  one means "we have not established *whether*".
- **needs-design**: issues triage flagged as underspecified — need human input before implementing.
- **blocked / pr-red**: the one-line blocker per issue and the suggested next step.
- **blocked-upstream**: issues the dependency graph screened out (step 6), each with the open issue or
  unclosed release/consume gate it waits on — plus any stacked layers orphaned by a blocked layer
  beneath them (1e), named with their stack and blocking layer. These are **not failures** — they are
  correct skips, and they become workable as soon as the named gate closes or the layer below merges.
- **Findings filed** (`agent-found` + `needs-triage`): the new issue numbers filed during the run,
  noting they are held for your triage — promote (remove `needs-triage`) to make them eligible for a
  future `--all` run.
- **Downstream follow-ups filed** (1f-cross): grouped by consumer repo, each marked *required*
  (compat) or *optional* (adoption). Call out any *required* one explicitly — that is a consumer
  that is broken or version-gated until it lands, not a nice-to-have.

State counts plainly (e.g. "7 issues: 4 merged, 2 deferred (Fable), 1 needs-design; 3 findings
filed (#331-#333, held for triage)"). Never report an issue as merged that `babysit-prs` didn't
actually merge; never report `pr-open` as done. Report a `rejected-by-design` as its own outcome
rather than folding it into the skips — "1 rejected-by-design" is a result the run produced, and
burying it invites someone to re-file the same issue next month.

**Persist the report.** Write the same table and groupings to
`.rift-ship/reports/<YYYY-MM-DD>-<mode>.md` in addition to printing them — suffixed `-run<N>` whenever
another run has ever claimed a slot in this repo, because `<date>-<mode>` collides the moment two runs
share a day and a mode, and the loser is silently overwritten. **Then release your run slot**: set your
row in `.rift-ship/ACTIVE-RUNS.md` to `status=DONE (<YYYY-MM-DD>)`. A report that exists only in
the conversation is gone the moment the session is — which is both a problem for the human reading the
results of an unattended overnight run, and the reason questions like *does the 1e→1c retry ever
actually rescue an issue?* or *which caps bind in practice?* cannot be answered today. Along with the
table, carry over each issue's `attempts` and `gate` cells verbatim (including any `(esc:rescued)` /
`(esc:failed)` annotation) plus any failure signature written in 1e·mem. Cheap to write, and the only
evidence base for tuning the caps later — change them from measurements, not impressions.

---

## Phase 2.5 — Refresh the cross-repo delivery dashboard (if one is configured)

Some programs keep a **live cross-repo dependency dashboard** — a folder of one-note-per-issue
records plus a graph/board that answers *"what's next, and what's blocked by what."* When the run
touched such a program, refresh it so it never goes stale. **Skip this phase entirely if no dashboard
is configured** (no `dashboard.path` and no discoverable dashboard note) — do not invent one.

Discover the dashboard from, in order: an explicit `dashboard.path` in the repo's `CLAUDE.local.md`;
else a `.rift-ship/dashboard-path` file; else a note titled *"Delivery Dashboard"* / a `db/` issue
folder already linked from the repo. (For the Rift program the dashboard lives in the user's Obsidian
vault at `tasks/rift-enterprise/issues/` — `delivery-dashboard.md`, `cross-repo-issue-dependency-graph.md`,
and `db/*.md`, one note per issue with `status`/`priority`/`blocked_by`/`unblocks`/`kind` frontmatter.)

Delegate the refresh to a **Haiku subagent** (mechanical; give it the dashboard path + this run's
outcomes). It must:

1. **Add new findings.** For every issue filed in **1f** (`agent-found`), create/refresh its db note
   with `status: blocked|ready` and the `blocked_by`/`unblocks` edges you observed.
2. **Update statuses from this run.** Merged issue → remove its db note **iff** no *open* issue still
   references it in `blocked_by`/`unblocks` (a resolved leaf); if it's still referenced, keep it as
   `status: done` so the edge stays legible. `blocked`/`pr-red` → set `status: blocked` with the
   concrete blocker in `blocked_by`. New PR not yet merged → `status: in-flight`.
3. **Model release/consume gates — a merge is not a delivery.** Shipping an issue often does **not**
   unblock a downstream repo: the library must be **published** and the consumer must **bump its pin**
   (e.g. rift-conformance pins a `zio-bdd` version). Keep these as first-class gate nodes
   (`kind: release` for a publish, `kind: consume` for a pin-bump) between the code node and its
   downstream. When an issue merges but its downstream is still on the old published version, set the
   downstream to `status: awaiting-release` (**not** `ready`) and point its `blocked_by` at the gate.
   Close/remove a gate only when the publish/bump actually happened.
4. **Garbage-collect.** Drop db notes for issues that are closed **and** unreferenced by any open
   issue; leave everything still on someone's critical path.
5. **Stamp it.** Update the `Last updated:` footer (date + one line: e.g. "N merged, M findings, gates
   refreshed") in the dashboard note and the graph note. The Dataview/board views re-render from the
   db frontmatter automatically — only hand-curated mermaid needs a manual nudge if the *spine*
   changed (new cross-repo edge), which you note for the human rather than redrawing blindly.

Report the dashboard delta in the Phase 2 output (e.g. "dashboard: +2 findings, 3 leaves GC'd,
1 release gate opened"). If the dashboard path is unreachable (e.g. a headless run with no vault),
say so and skip — never fail the run over dashboard upkeep.

---

## Resuming after an interruption (token-out, crash, new session)

A session can die mid-run — token/rate-limit exhaustion, a crash, or you simply closing it. The
loop is built to make that a **pause, not a loss**:

- **Nothing merged or pushed is lost.** Merged PRs stay merged, open PRs stay open. Progress is
  re-derived from **live GitHub state** (open PRs, merged/closed issues) plus your run's run-log,
  which is checkpointed after every phase — not from conversation memory.
- **Find the right run-log first.** A fresh session defaults to `.rift-ship/worklist.md`, which may
  belong to a *different* run. Read `.rift-ship/ACTIVE-RUNS.md` (`0·claim`) and resume the row whose
  batch matches your arguments; adopt that run's id and log file rather than opening a new slot.
  Correctness does not hinge on this — Phase 0 re-derives from live GitHub and skips anything already
  PR'd — but reading the wrong log produces a wrong plan and a wrong report.
- **To resume:** re-invoke the *same* command (e.g. `/ship-issues --all`) in a fresh session once
  your tokens recharge. Phase 0 re-prunes against GitHub, re-reads the run-log, skips anything that
  already has a PR or is merged, and continues from the first non-terminal issue. Re-running is
  safe and idempotent — it never re-implements a PR'd issue or re-merges a merged one.
- **The only rework** is an issue whose `fix-issue` was interrupted *before* its PR was opened:
  it has no PR yet, so resume re-runs it from scratch. `fix-issue`'s own worktree and run-log
  persist on disk, so this is redo, never corruption.
- **A half-built stack resumes cleanly.** Phase 0 step 8 re-forms the groups from the same dependency
  edges each run, and step 4 prunes the layers that already have PRs, so a resume picks up at the
  first layer without one. Take that layer's base from the run-log `base` cell (the predecessor's
  branch), not from the group's real base — that cell exists for this. If the predecessor has since
  **merged**, GitHub already retargeted it, so cut the resumed layer from `origin/<base>` normally and
  note the stack as truncated.
- **To minimise blast radius** when token-outs are likely: run smaller explicit batches
  (`/ship-issues 316 317 318`) rather than `--all`, so an interruption lands on a clean boundary.
- **Unattended auto-resume:** because resume is idempotent, a scheduled routine that re-invokes
  `/ship-issues --all` every few hours will continue the batch on its own after a throttle window
  clears — and is a cheap no-op while everything is already merged.

## Hard caps & stop conditions

- Per-issue implementation and CI fixing inherit the sub-skills' **3-cycle caps**. The orchestrator
  allows at most **one** extra `fix-issue` re-run per issue when babysit traces a red CI to an
  implementation defect (1e → 1c). Beyond that, the issue is `pr-red`/`blocked` and skipped.
- **Circuit breakers — two of them, because one shape of systemic failure hides from the other:**
  - *Consecutive:* **3 issues in a row** end `blocked`/`pr-red` → stop. Catches a hard systemic
    problem (broken base branch, CI outage, bad environment) that per-issue retries won't fix.
  - *Rate:* once **at least 4 issues** have been attempted, stop if **more than half** of them ended
    `blocked`/`pr-red`. Catches the intermittent version of the same thing — a flaky required check
    that kills every *other* issue never trips a consecutive counter, but a run losing most of its
    worklist is not one to leave running unattended.
  - `deferred(<model>)`, `rejected-by-design`, `needs-design(should)`, `needs-design`,
    `blocked-upstream(...)`, `owned-by-run<N>` and the umbrella
    statuses are **not** failures and count toward neither breaker — they are correct skips, and a run made mostly of them
    is working as designed.
  - On either trip: report which breaker fired and why, list the remaining `pending` issues, and stop.
    Do not reset a breaker by retrying — that is the failure mode the breaker exists to prevent.
- Never force-push, never touch a branch that isn't an issue's own head, never merge a PR that isn't
  green and mergeable. In particular the stacking support is limited to `gh stack link` (registration
  only) and `gh stack view` (the probe): `gh stack push`/`submit`/`sync`/`rebase` force-with-lease
  across branches this loop does not own, and `gh stack merge` lands layers without their own green
  gate. None of them are the unattended path.
- **Never touch another run's things** (`0·claim`): do not write, archive or rename another run's
  run-log; do not merge a PR, push a branch, or `git worktree remove` a directory your run did not
  create. Worktree cleanup is especially easy to get wrong from outside a run — a directory whose
  issue is closed can still be a live run's working tree.
- Never move or dirty the user's checkout: no `git switch`/`checkout`/`reset`/`merge` outside a
  per-issue worktree, and no implementing an issue in the main working directory when its worktree
  cannot be created — stop and report instead.
