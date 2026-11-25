---
name: superauthor
description: Shared plan-authoring core — the no-execution rule, the plan-authoring standard, no-placeholders, generic self-review, standing authorization, findings capture, commit-and-merge-via-PR, and Final Report format. Invoked by plan-producing skills (supergoal, superplan) to avoid duplicate planning logic.
license: MIT
---

# Superauthor

The single source of truth for the mechanics shared by plan-producing skills: how to **author a
planning artifact to the shared standard, self-review it, capture findings, commit and merge it via
a PR, and report** — without ever executing the planned work.

This is the authoring analogue of `supertraverse` (which owns plan-*tree navigation*). Like
`supertraverse`, superauthor is a **clause library**: the calling skill (e.g. `supergoal`) invokes it
via the Skill tool and carries out the clauses A1–A8 inline with its own file / Bash / Skill tools.
**Superauthor itself reads nothing, writes nothing, runs nothing, and commits nothing** — the **caller**
owns every read, write, and commit. The clauses define *how* the shared steps are performed; the caller
supplies the artifact-specific specifics:

- **(a)** the **goal folder** all output is written under;
- **(b)** the **artifact(s)** to author and where they route (which subfolder);
- **(c)** for A7 — the **branch prefix**, the **commit subject**, and the explicit **`git add` file list**;
- **(d)** for A8 — the **report lines** specific to what the caller produced.

Anything tree-specific (descent, a parent-seed reference, updating a parent's progress-report row,
ascending the tree) is **not** part of superauthor — a calling skill that participates in a plan tree
layers those on top of A1–A8 itself.

---

## A1 — The deliverable is the plan, and ONLY the plan

**The calling skill produces a planning artifact and a report, then stops. DO NOT execute, implement, or
begin any of the planned work.** Not one "trivial" step. Not "just scaffolding it." Not even in
auto-accept / `bypassPermissions` mode. Not even if the user seems eager or the work looks small.

A superauthor-driven skill **never** writes or edits source code, **never** runs tests or builds,
**never** creates worktrees, and **never** begins the planned work. Executing the plan is a separate,
later action the user invokes explicitly (e.g. `superrun`) —
it is **not** part of the authoring skill.

The one thing the skill *does* commit is **the planning artifacts themselves** (the plan documents and
any structural/`findings/` docs it wrote). Once written to the vault, the skill commits **only those
artifacts** and merges them to `main` via a pull request as its final action — **automatically, under
the user's standing authorization, without pausing to ask** (see A7). That is the sole commit — never
source code, never execution output.

| Thought | Reality |
|---------|---------|
| "Auto mode is on, so I'm cleared to start coding" | NO. Auto mode governs tool permissions, not scope. The deliverable is the plan. |
| "The first task is trivial, I'll just knock it out" | NO. Zero implementation steps. Ship the artifact and stop. |
| "I'll set up the worktree / branch for the planned work" | NO worktree and no branch for the *planned work*, and no source-code commits. (The artifacts are committed and merged via PR as the final step — that is the only commit.) |
| "The user will obviously want this run, I'll get a head start" | NO. Produce and commit the artifact, report, exit. Wait to be asked before executing. |

## Repo configuration (.superenv)

Resolve project context before any workflow action by sourcing `${CLAUDE_PLUGIN_ROOT}/scripts/_common.sh` under bash (it refuses zsh and other shells — wrap the call in `bash -c '…'` when your shell is not bash) and calling `superagent_load_context "$PWD" run` (lifecycle control commands first load the registered `SUPERAGENT_PROJECT_ROOT`). Use its exported physical `REPO` and validated `SUPER_GIT_MODE`. Resolution is process environment > nearest/explicit project `.superenv` > packaged default; missing mode means `github`. In `none`, never run git, gh, GitHub API, credential discovery, worktree, commit, push, PR, merge, sync, or CI-poll operations. An existing `.git` directory does not change this rule.

## Vault root

Resolve `SUPER_GOAL_ROOT` (above). If it starts with `/` or `~`, the vault is **external**:
`<vault_root>` is that path (`~` expanded to `$HOME`, one trailing `/` stripped), resolved physically
(`cd "<path>" && pwd -P`) so it matches the paths `launch.sh` stores, and the vault is its own git
repository outside the checkout. Otherwise `<vault_root>` is `<primary_root>/<SUPER_GOAL_ROOT>`
(`primary_root` = the physical `REPO` exported by `superagent_load_context`). Every goal
folder, project folder, loop-status file and lock derives from `<vault_root>`; **never join
`SUPER_GOAL_ROOT` onto the checkout root by hand.** The same rule is `vault_root` /
`vault_is_external` in `scripts/_common.sh`.

## A2 — Authoring standard (REQUIRED)

**Author the plan yourself, directly, to the standard below.** This standard is self-contained:
no other plugin's planning skill is invoked to produce the plan document. Whether
the produced plan's own verification steps follow the local test-first cycle or specify CI
pushes instead is governed by `SUPER_TEST_EVIDENCE` (see the **Verification-steps mode** bullet below).

Write for a skilled engineer with **zero context for this codebase**. First classify the artifact's
planning maturity; the required detail follows that observable state:

- An **upfront stage contract** (`upfront-v1`, not yet prepared) follows superstage S2. It commits to
  goal and scope, acceptance ownership, a chosen architecture/approach, dependency ownership,
  versioned cross-stage behavior, distinguishing verification scenarios, and a concrete task outline.
  Include known paths, mandated signatures/algorithms, and observed predecessor facts. Bounded
  predecessor-dependent filenames, helper names, exact future line numbers, and complete test bodies
  may remain unresolved only with evidence, bounds, a resolution method, and invalidation triggers.
  Do not fabricate code or paths merely to make a future stage look executable.
- A **prepared stage** must add actionable task, file, code/signature where useful, and test detail
  grounded in the current repository and predecessor evidence. It must be executable without another
  architecture or requirements decision and must satisfy the preparation receipt in superstage S5.
- An **incremental or unmarked legacy implementation plan** keeps the established full-detail
  standard: name the exact files each task touches, show the actual code, and state how the work is
  verified. Existing full-detail plans need no rewrite.

All maturities are DRY and YAGNI. Bounded implementation uncertainty is allowed only in an upfront
stage contract; vague or missing scope, architecture, acceptance, contracts, or verification remains
a plan failure at every maturity.

- **File structure first.** For prepared and legacy plans, map the exact files that will be created or
  modified and what each owns before defining tasks. For an upfront stage contract, map relevant
  components and every currently known path, then identify each bounded path/detail that preparation
  must resolve. Prefer small, focused responsibilities and established repository patterns rather
  than restructuring beyond the task's scope.
- **Task right-sizing.** A task is the smallest unit that carries its own verification and is worth
  a fresh reviewer's gate. Fold setup, configuration, scaffolding, and documentation steps into the
  task whose deliverable needs them; split only where a reviewer could meaningfully reject one task
  while approving its neighbor. Each task ends with an independently verifiable deliverable.
- **Plan header.** Every implementation plan starts with:

  ```markdown
  # [Feature Name] Implementation Plan

  > **For agentic workers:** REQUIRED: execute this plan with `superagent:superrun` (its
  > `superagent:superbuild` task loop implements it task-by-task). Steps use
  > checkbox (`- [ ]`) syntax for tracking.

  **Goal:** [one sentence describing what this builds]
  **Architecture:** [2–3 sentences about approach]
  **Tech Stack:** [key technologies/libraries]

  ## Global Constraints

  [The source material's project-wide requirements — version floors, naming rules, exact values
  copied verbatim, one line each. Every task's requirements implicitly include this section.]
  ```

- **Task structure.** In prepared and legacy plans, each task carries a **Files** block with exact
  paths (`Create:` / `Modify: path:lines` / `Test:`); an **Interfaces** block — *Consumes:* what this
  task uses from earlier tasks (exact signatures), *Produces:* the names, parameter and return types
  later tasks rely on; and checkbox (`- [ ]`) steps whose code steps contain real code blocks. In an
  upfront stage contract, use superstage's stable `Consumes` / `Produces` contract IDs and behavioral
  revisions, list known files/components, and give a task outline plus verification scenarios.
  Preparation converts that outline into the executable task shape once the missing evidence exists.
- **Verification-steps mode is keyed by `SUPER_TEST_EVIDENCE`.** If `SUPER_TEST_EVIDENCE=ci`: authored
  plan steps specify CI pushes as the test evidence — the commit flag (if any), the lane it routes to,
  and the run id + conclusion as the pass criterion — following the CI-scheduling rules the caller
  supplies (queue-all batches, monitor-parked waits); never write `pytest` / `./run.sh` / build
  commands to execute on the host, and never instruct poll-loop CI waits in plan text. If
  `SUPER_TEST_EVIDENCE=local` (the shipped default): plan steps use the local test-first cycle —
  for each behavior, a step that writes the failing test (real test code), a step that runs it with
  the exact command and the expected failure, a step with the minimal implementation, a step that
  re-runs the command with the expected pass, then a commit step.
- **A mechanical gate belongs in a committed test, never in an unrun shell block.** If a plan step
  says "verify X before proceeding" and X is checkable by code, the plan's deliverable is **the test
  that checks X**, cited by name — not a snippet the executor is told to run and trust. A committed
  test is executed, reviewed, and maintained; a code block in plan prose is **none of those and is
  trusted anyway**, because plan text reads as authoritative. This applies with most force to a
  **STOP gate**: a wrong gate does not merely fail to catch a defect, it **halts a correct run**.
  Worked example — a T2.2.4 Task-0 STOP gate asserted `src.count('pool="train"') == 41` against a
  file where the string also appears in a docstring and a comment, so the true count is **43**. An
  executor obeying the plan literally would have halted a run that was entirely correct. If a gate
  genuinely cannot be a test (it inspects CI output, a PR state, or the host), write the exact
  command **and** the failure mode that makes it wrong, so the executor can tell a real trip from a
  broken probe.
- **Never size a test fixture as a multiple of the parameter under test.** A fixture whose dimensions
  are commensurate with the parameter lets a wholly wrong implementation satisfy every assertion.
  Worked example — a plan-mandated stratification test used two synthetic strata of **6** against
  `stride=3`; because 6 is a multiple of 3, an implementation that ignored stratification entirely
  passed all seven assertions. Unequal, non-commensurate sizes (4 and 6) fail it immediately. State
  the fixture's dimensions in the plan **with the reason they were chosen**, so an implementer does
  not "tidy" them back into round numbers. The general form: **a fixture must be able to distinguish
  the property under test from its most plausible wrong implementation** — write down what that wrong
  implementation is, and check the fixture separates them.

  > Both rules above exist because this class of defect is **self-concealing**: it produces green,
  > confident output. In one authoring-plus-review session it recurred **four times** — twice in the
  > plan text and twice in the reviewer's own throwaway verification regexes (one required a unit
  > word, one rejected sentence-final periods; each published a wrong count that had to be retracted).
  > Treat any ad-hoc regex or one-off count written to *check* a claim as unreviewed code on the
  > critical path: cross-check it against a second, differently-shaped extraction before quoting the
  > result.

**Author the draft to a scratch path OUTSIDE the goal folder** (e.g. `$TMPDIR/` or `.claude/scratch/`),
not into the goal folder. **Nothing is written under the goal folder (no plan file, no structural doc,
no `findings/` doc) until self-review (A4) passes** — at which point the scratch draft is written into
the vault automatically.

An upfront initial-tree caller keeps all root, sub-master, stage, directives, and tree-review drafts
in one scratch set until its whole-tree S2/A4 review and caller-specific confirmation gate succeed.
The scratch set is never execution authority or a partial publication: its caller records source
identity, intended vault destinations, stable IDs, review progress, and the remaining gate in a draft
index so it can resume without inventing a second tree.

> The A2 standard applies to authoring a **plan**. Purely *structural* documents a caller may also
> write (e.g. a `goal-directives.md` layout guide) are not plans and are exempt from the plan-shaped
> parts of the standard. The caller states which of its outputs are plans.

## A3 — No placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write
them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" without actual test code in a prepared/legacy plan, or without
  distinguishing inputs, expected observations, and evidence method in an upfront stage contract
- "Similar to Task N" (repeat the code — the engineer may read tasks out of order)
- Prepared/legacy code steps that describe what to do without showing how (code steps require code blocks)
- References to types, functions, or methods that the plan relies on but neither defines nor records
  as a bounded predecessor-dependent detail

For an upfront stage contract, a dedicated bounded-unknown entry is not a placeholder when it names
the current evidence, the finite detail still unknown, why predecessor delivery controls it, the
method and evidence that will resolve it during preparation, and its invalidation trigger. It still
must preserve the stage's chosen approach and behavioral commitments. "Choose the architecture later,"
"determine requirements during implementation," or an unbounded design task fails A3. Prepared and
legacy plans retain the full prohibitions above, including actual test/code detail where applicable.

## A4 — Generic self-review

**Review the written plan yourself, inline — not via a subagent dispatch.** The caller authored the
plan directly (A2), so nothing has pre-checked it — run the full checklist with fresh eyes:

1. **Spec coverage against the caller's source material** — skim each section/requirement of the topic.
   Point to a task that implements it; add a task for any gap. When the source includes an approved
   acceptance checklist, carry its relevant IDs, source revision, full conditions and expected
   results through root, sub-master and leaf plans. Link the complete agreement so a fresh agent
   can resolve it. Check task coverage against that agreement; do not re-author the test inventory.
   Conflicting or ambiguous acceptance inputs are findings for the author, not new conditions
   for the implementer. This does not restrict implementation choices or ordinary code review.
2. **Maturity and placeholder scan** — identify upfront-contract versus prepared/legacy maturity,
   apply its A2/A3 detail standard, and fix every prohibited placeholder. For an upfront stage, apply
   superstage S2: bounded details may remain, but missing scope, architecture, acceptance, contract,
   scenario, or resolution commitments fail review. For a prepared stage, validate its S5 identity.
3. **Type/term consistency** — do the types, signatures, contract IDs/revisions, and names used in later tasks match what
   earlier tasks defined? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in
   Task 7 is a bug.

An initial upfront-tree caller applies this checklist across the complete candidate, then also checks
S2 active-scope coverage, intended-vault-path-to-scratch-path resolution, cross-stage contract
compatibility and dependency order, unique stable IDs, and the durable review's acceptance-to-stage
map. It cannot publish a tree with an unlinked active row or replace that gap with incremental planning.

If you find issues, fix them inline — no need to re-review the whole plan.

**Tree-specific self-review items are NOT part of A4.** Confirming a parent-seed reference, an updated
immediate-parent progress-report row, or an ancestor ascent applies only to a skill that inserts the new
plan into an existing plan tree — that skill adds those checks itself, after A4. A root-creating caller
(no parent, no tree above it) has none of them and runs A4 alone.

## A5 — Standing authorization: proceed without pausing

The user has granted **standing authorization** for a superauthor-driven skill to write its docs to the
vault and merge the artifact PR. **Do NOT pause to ask for approval, and do NOT present the draft and
wait for a "go" before writing.** After self-review, proceed directly — capture findings (A6), write the
docs into the goal folder, commit, and merge the PR (A7) — then report (A8). This is not waived or
re-enabled by auto-accept / `bypassPermissions` mode; it is the default behavior.

Do not print the full draft to chat up front. The user's single checkpoint is the **Final Report** (A8),
which clearly enumerates every file written this run.

In `SUPER_GIT_MODE=none`, the same standing authorization covers durable local publication under
the inherited workspace lock. It does not authorize git/GitHub operations; proceed through A6 and
the local A7 branch without pausing.

## A6 — Capture findings

After self-review, identify any **findings** or new insights uncovered during the authoring phase —
e.g. a constraint discovered, a contradiction in the source material, a mechanism that does not work as
assumed, or a non-obvious fact a future planner would need.

Review the existing docs in the goal folder's **`findings/`** subfolder to decide whether each finding is:

- an **addition** — write it to a new doc in `findings/`, named `YYYY-MM-DD-hh_mm-<topic>.md` (today's date and the current UTC hour and minute), or
- a **revision** — update the relevant existing doc in `findings/`.

(These writes happen as part of the automatic write-out — after self-review, alongside the plan file. No
user confirmation is awaited.)

**Be extra certain of each finding.** If you are unsure whether a finding is correct, **do not include
it** — false findings are harmful to the goal. Only record what you have verified. If there are no
findings, record none.

## A7 — Commit and merge via PR (caller-parameterized)

**Local persistence (`SUPER_GIT_MODE=none`) overrides every commit recipe in this skill and every
caller.** Write only the caller's explicit artifact list, reopen each file and verify its expected
identity/content, and report the physical paths. Do not inspect tracking state or run git, gh,
credential, branch, worktree, commit, push, PR, merge, sync, or CI operations. For completion work,
also write and verify the `completed-local` receipt defined by superloop L6. Persistence is the
durable file plus its verified receipt; A7 then returns directly to A8. This override applies equally
to internal and external vaults and to duplicated commit sections in superplan, superfinish,
supergoal, superprd, and supermeta.

After the artifact(s) and any `findings/` docs are written into the goal folder, commit those planning
artifacts. **Never pause before writing, committing, or merging** — the user has granted standing
authorization (A5).

**Target repo — resolve first (see Vault root).** In **internal** mode the target is the code repo
and the rest of this clause applies as written. In **external** mode the target is the **vault repo
at `<vault_root>`**.

**Precondition (external mode only) — verify before the first git command:** `git -C "<vault_root>" rev-parse
--show-toplevel` must succeed and its output, resolved physically (`cd … && pwd -P`), must equal
`<vault_root>` resolved physically. If it does not — `<vault_root>` is not a repository, it sits
inside another repository's tree (git would silently commit into *that* repo and, if it has a
remote, push there), or it resolves inside `<primary_root>` — **STOP**: write nothing further,
commit nothing, and report "external vault at `<vault_root>` is not initialised — run `superagent:init`".
Never `git init` here; init owns vault creation.

In **external** mode the **direct-commit variant** (bottom of this clause) **always applies**,
regardless of `SUPER_PROTECTED_MAIN` — that key describes the code repo, not the vault: run every
git command as `git -C "<vault_root>" …`, express the caller's `git add` paths **relative to
`<vault_root>`**, keep the caller's commit subject, push **only if** `git -C "<vault_root>" remote
get-url origin` succeeds (otherwise the commit stays local — not an error), and open **no branch,
no PR, no `gh` call**. Record the short SHA for A8 (`git -C "<vault_root>" rev-parse --short HEAD`).
The remaining paragraphs describe the internal target.

**Merge the PR without asking the user for confirmation** (internal mode).

If `SUPER_PROTECTED_MAIN=true` (the shipped default), the default branch is a **protected branch**
(direct pushes are rejected), so this MUST go through a feature branch and a PR — merged per
`SUPER_MERGE_METHOD` (default `squash`) — even though it is docs-only. If `SUPER_PROTECTED_MAIN=false`,
a direct commit to the default branch is permitted instead.

**Scope of the commit: only the planning artifacts this run produced.** Add each with an explicit
`git add <path>`; **never `git add -A`** (the working tree may hold unrelated changes that are not yours
to commit). These are docs-only changes, so tag the commit subject `[skip ci]` to avoid firing CI on the
merge.

**The caller supplies three parameters:** the branch prefix, the commit subject, and the explicit
`git add` file list. Substitute them into this skeleton:

```bash
# from the repo root, with the artifact/findings files already written
BRANCH="<caller-branch-prefix>-$(date +%Y-%m-%d)"
git checkout -b "$BRANCH"
git add <file> [<file> ...]                       # caller-supplied explicit paths only — never git add -A
git commit -m "<caller-commit-subject> [skip ci]"
git push -u origin "$BRANCH"
gh pr create --title "<caller-pr-title>" \
  --body "<caller-pr-body>"
gh pr merge --squash --delete-branch          # plain --squash is the DEFAULT — do NOT reach for --admin
git checkout main && git pull --ff-only
```

Notes:
- `--squash --delete-branch` keeps history clean and removes the feature branch after merge.
- **Merge per `SUPER_MERGE_METHOD` (default `squash`). Pass `gh pr merge --admin` only if
  `SUPER_ADMIN_MERGE=true` — otherwise never.** Reaching for `--admin` when the key is unset or `false`
  buys nothing on a repo whose branch protection doesn't require it, and reliably **trips the harness
  security classifier**, which reads merge-over-red as a privileged override and denies it. If the plain
  merge is actually refused, escalate to `--admin` only when `SUPER_ADMIN_MERGE=true` permits it, and
  say in your report **why** it was refused.
- **`--delete-branch` can exit 1 with `fatal: '<branch>' is already used by worktree` — the PR still
  merged.** That failure is the *local* branch-delete step, not a permission rejection. Confirm with
  `gh pr view <n> --json state,mergedAt`; if it merged, delete the remote ref directly with
  `gh api -X DELETE repos/<owner>/<repo>/git/refs/heads/<branch>` rather than re-running the merge.
- Capture the resulting **PR URL** (from `gh pr create` / `gh pr view --json url`) — report it in A8.
- Do **not** commit Anthropic/Claude attribution or `Co-Authored-By` trailers (repo policy).
- If `SUPER_GH_DISABLE_SANDBOX=true` (macOS hosts where `gh` needs keychain access to verify the
  TLS cert), all `gh` commands need `dangerouslyDisableSandbox: true`. If `false` (the shipped
  default), run `gh` normally.

**Direct-commit variant — `SUPER_PROTECTED_MAIN=false`, or any external vault.** The skeleton
above is the internal-mode `SUPER_PROTECTED_MAIN=true` (shipped-default) path. When
`SUPER_PROTECTED_MAIN=false`, or whenever the target is an external vault (then prefix each
command with `-C "<vault_root>"` and make the paths vault-relative), skip the branch/PR machinery
entirely and commit straight to the target repo's current branch (internal mode: the default
branch, as today; external vault: whichever branch the vault repo has checked out) — no `gh` calls
at all:

```bash
# internal mode: from the code repo root; external vault: every command carries -C "<vault_root>" — files already written
git add <file> [<file> ...]                       # caller-supplied explicit paths only — never git add -A
git commit -m "<caller-commit-subject> [skip ci]"
git push                                           # only if a remote exists
```

A repo with no remote simply keeps the commit local — `git push` has nothing to push to and that is
not an error; skip it rather than forcing a remote into existence.

## A8 — Final Report, then exit (caller-parameterized)

After the artifact is written, self-review is done, findings are captured, and the PR is merged (A7),
give the user a **single report** and then **exit the skill**. **Do not ask whether to execute the plan
and do not offer execution options** — a superauthor-driven skill never offers execution.

**This report is the user's single window into what the skill wrote — every file path created or
modified this run MUST appear here.** Include the merged **PR URL**, and call out any **CRITICAL finding**
(a contradiction in the source, a mechanism that does not work as assumed, a blocking constraint) under
its own bold ⚠️ line so it cannot be missed.

Generic shape — the caller fills in its artifact-specific lines (and may rename the heading to its own
skill):

```
## <skill> complete

**<primary artifact>:** <full path>      ← the most important line; always include it
**PR:** <url> (merged)
**Commit:** <short-sha> in <vault_root>   (external vault — print this line INSTEAD of the PR line, verbatim form)
**Persistence:** local files verified (SUPER_GIT_MODE=none)  (local mode — print this line instead)

**Other files created/modified:**
- <path> — <what changed>     (or: none)

**Findings:**
- <finding summary>           (or: none)

⚠️ **Critical:** <only present when a finding needs attention>
```

In external vault mode there is no PR: print `**Commit:** <short-sha> in <vault_root>` on that
line instead. Every caller's instantiation applies the same substitution.

After printing the report, the skill is done: take no further action and ask no follow-up question.
