---
name: superrun
description: Use when asked to execute the next ready implementation plan in a goal's plan tree from its root seed/master plan — finds the highest-priority written-but-unexecuted leaf plan, executes it, and closes it out.
license: MIT
related skills: supertraverse, superbuild, superfinish, superplan
---

# Superrun

The **execution** leg of the plan-tree lifecycle. The `super*` family covers the rest of the
arc — `supergoal` seeds the tree, `superplan` writes a step's implementation (leaf) plan and marks
its row `PLAN WRITTEN — ready to execute`, `superfinish` closes out an *already-executed* leaf.
superrun is the verb between "plan written" and "closed out": given a goal's **root** seed/master
plan, it finds the highest-priority written-but-unexecuted leaf plan, **executes it**, and hands it
to `superfinish`.

## Repo configuration (.superenv)

Resolve project context before any workflow action by sourcing `${CLAUDE_PLUGIN_ROOT}/scripts/_common.sh` under bash (it refuses zsh and other shells — wrap the call in `bash -c '…'` when your shell is not bash) and calling `superagent_load_context "$PWD" run` (lifecycle control commands first load the registered `SUPERAGENT_PROJECT_ROOT`). Use its exported physical `REPO` and validated `SUPER_GIT_MODE`. Resolution is process environment > nearest/explicit project `.superenv` > packaged default; missing mode means `github`. In `none`, never run git, gh, GitHub API, credential discovery, worktree, commit, push, PR, merge, sync, or CI-poll operations. An existing `.git` directory does not change this rule.

## Execution engine — `superagent:superbuild`

This skill executes implementation and code-changing discovery plans through this plugin's own
task loop, `superagent:superbuild` (a fresh implementer per task, a task review, a capped fix loop,
one whole-branch review). No other plugin is required. Never degrade code work to inline
execution. A verified evidence-only discovery takes its explicit earlier branch and does not run
the task loop.

A plan authored before 0.11.0 carries a header naming `superpowers:subagent-driven-development` as
its required sub-skill. Read that line as `superagent:superbuild`: execute the plan with the native
task loop and never look for, or wait on, the superpowers plugin.

**One leaf plan per invocation.** superrun finds the single highest-priority incomplete leaf,
executes it, closes it out, reports, and exits. To run the next plan, invoke superrun again on the
same root.

Unlike superplan/superfinish (which are docs-only), superrun **does** change source code — but
**only via the delegated skills**. Code implementation is owned by superbuild and closeout by superfinish.
The explicit evidence-only discovery branch below runs the stage's specified experiment and publishes
its evidence/decision docs through A7 without changing source; it is the sole non-superbuild execution path.

| Thought | Reality |
|---------|---------|
| "I'll just detect the target plan myself by reading the tree" | NO. Invoke `superagent:supertraverse` DESCENT in **execution mode** — it is the only place tree navigation is defined. |
| "I'll implement the plan's tasks directly / dispatch my own subagents" | NO. You **MUST** use `superagent:superbuild` to execute the plan. |
| "I'll write the findings/closeout report and update the tree myself" | NO. You **MUST** use `superagent:superfinish` for closeout. |
| "No worktree needed — I'll edit in the primary checkout" | In `github`, NO: enter a worktree. In `none`, the recorded project plus inherited writer lock is the required workspace; superbuild runs its `none` branch and no git stage. |
| "I'll pause before each CI push to confirm" | NO. Run fully autonomously — superbuild runs end-to-end and never checks in between tasks. |
| "The plan is ambiguous here — I'll ask the user" | NO. superbuild B5 routes it: a load-bearing conflict is a BLOCKED report, anything else is a ledgered ruling that reaches the Final Report. Never ask from inside the loop. |
| "I found the target, I'll execute the next one too while I'm here" | NO. One leaf per invocation. After closeout, report and exit. |
| "CI is red — declare BLOCKED and let the supervisor sort it out" | NO. Run **CI-failure triage** (Step 3a) first: read the failing step's log, classify it, name the best-supported cause and the cheapest fix. Apply an in-scope, unprotected fix yourself; only the rest is BLOCKED, with the triage record attached. |
| "The step's duration matches the timeout, but I never saw the kill — cause unproven" | NO. A duration that matches a configured limit is sufficient evidence of a timeout. A runner or `subprocess` timeout kills the child internally and leaves no separate kill record; do not demand one. |
| "A long CI push is queued — I'll wait for it to finish before pushing the next one" | NO. If `SUPER_CI_RUNNERS > 1`, queue every independent long push back-to-back (**CI scheduling**, Step 3) — the next free runner picks up the next job; serialize only across a named procedural gate. If `SUPER_CI_RUNNERS=1`, there is no runner contention to exploit, but a shardable batch's pushes still queue together and wait together. |
| "I'll wait for CI with `gh run watch` / a backgrounded sleep-poll loop" | NO. The wait is **monitor-parked** (Step 3a): standalone → arm one Monitor over all run ids and end the turn; under superagent → return a CI-PENDING report and stop. Poll loops burn context for nothing. | <!-- cc-only -->
<!-- cursor-only:start
| "I'll wait for CI with `gh run watch` / a backgrounded sleep-poll loop" | NO. The wait is **parked** (Step 3a): standalone → report the queued run ids and end the turn (resume later via **Resume entry — post-CI**); under superagent → return a CI-PENDING report and stop. Poll loops burn context for nothing. |
cursor-only:end -->
<!-- codex-only:start
| "I'll wait for CI with `gh run watch` / a backgrounded sleep-poll loop" | NO. The wait is **parked** (Step 3a): standalone → report the queued run ids and end the turn (resume later via **Resume entry — post-CI**); under superagent → return a CI-PENDING report and stop. Poll loops burn context for nothing. |
codex-only:end -->

## Input — `<PLAN.md>` (Gate 1)

superrun requires `<PLAN.md>` — the **root** seed/master plan of the goal whose tree it traverses.
If it was not provided, exit with:

    superrun needs the root plan file (<PLAN.md>) to traverse. Nothing was run. Exiting.

Do not guess a root from the working directory.

## Step 1 — Find the target (invoke `superagent:supertraverse`, execution mode)

Invoke the `superagent:supertraverse` skill (Skill tool) and run its **DESCENT in execution mode** on
`<PLAN.md>`. It returns one of:

- **`not-traversable`** — the root is not maintained as a progress-report tree (only orchestration
  tables / no step-tracking list). Report this and exit; there is nothing to execute.
- **BLOCKED** — report the row and reason; exit without execution.
- **`NEEDS-REFINEMENT`** — this is an upfront-v1 leaf with its exact root, stage ID/path, and
  receipt/revalidation evidence. Report `NEEDS-REFINEMENT` with those exact values and exit. Do not
  invoke superrefine, superplan, superbuild, or a child process under EXECUTOR; the controller must schedule
  PLAN_REFINER as a separate planning operation. Incremental and unmarked roots do not use this
  outcome and retain their existing manual execution behavior.
- **`REPLAN-REQUIRED`** — report the root, stage ID/path, and broken source/stage/predecessor/
  contract/finding assumption. When an acceptance case cannot be met as written, also report the case
  and superreplan's remedies 1–5 (*Prefer the smallest unblocking change*) with which appear to apply;
  the same applies to a REPLAN-REQUIRED that superbuild returns mid-execution. Exit without execution so the existing decision and REPLANNER path can
  adopt or reject the structural change. Never turn that evidence into an in-place execution ruling.
- **`none`** — no execution target exists; invoke **supertraverse C9 completion audit** before
  reporting. **complete**: report none with integration/disposition evidence. **incomplete**:
  report none with the planning/repair gap. **BLOCKED**: return a BLOCKED report naming the
  unresolved leaf/PR/evidence, even though traversal returned none. An open-PR closeout is not
  completion. Do not run superfinish on a fabricated target.
- **a target leaf plan file path** — the highest-priority written-but-unexecuted leaf. Proceed.

For an upfront-v1 target, immediately before Step 2 re-read synchronized source, code, predecessor
delivery, contract, finding, root-generation, and stage evidence and apply superstage S1/S2/S5. This
is a fresh execution-entry check, not a recursive traversal call. A current valid PREPARED receipt
and S3-satisfied prerequisites permit Step 2. A missing receipt or an unrelated-baseline advance that
needs focused compatible revalidation returns `NEEDS-REFINEMENT` with the exact root/stage ID; leave
the leaf untouched. A relevant changed assumption returns `REPLAN-REQUIRED`; missing or contradictory
evidence is BLOCKED. Do not prepare a stage while running as EXECUTOR.

Before implementation, capture one **execution-entry snapshot** from that verified state: root path and
Plan generation; active stage path, Stage ID and Stage revision; Preparation report path and its
prepared-plan digest; the authoritative vault commit containing that stage and receipt; reviewed code
revision; source agreement/revision; and every consumed contract revision/provider delivery receipt.
The existing tracked prepared plan plus receipt are the durable snapshot; do not create a second
database or a pre-code docs publication. Carry this exact identity into the code PR description (or
direct-integration evidence), any CI-PENDING packet, and superfinish. If recovery must reconstruct it,
use only the tracked receipt, the exact historical vault blob/commit, and verified branch/PR history;
missing or conflicting identity is BLOCKED. Never derive a past execution identity from the current
plan after closeout or replanning has edited it.

Before invoking superbuild, reconcile evidence that the selected identity already ran. A verified merged
PR/direct integration with no complete closeout means **closeout recovery**: do not implement again;
invoke superfinish with the execution snapshot and actual integration evidence. A verified already
published delivery receipt is also handed to superfinish for idempotent reconciliation rather than
creating another report. An open/CI-pending attempt resumes its recorded branch/worktree path. If an
active successor replaced this identity, preserve the old attempt as history and follow C8; never
execute or close the successor by inference.

## Evidence-only discovery branch — before Steps 2–3

Read `Stage kind` before entering the code-worktree path. If the selected upfront stage is
`discovery` and its approved task outline requires no tracked code change, execute this branch and
**skip Steps 2, 3 and 3a**:

1. Run the stage's specified experiment exactly as approved, using its distinguishing inputs and
   evidence method. Temporary experiment output stays outside tracked source unless the stage names a
   vault evidence artifact. Do not create a code branch, code worktree, code PR, or superbuild task loop.
2. Review the observed result in a separate pass against the stage's evidence requirements, decision
   criteria, acceptance IDs, assumptions it may invalidate, and produced discovery contracts. Missing,
   ambiguous or contradictory evidence is BLOCKED; do not invent a decision.
3. Before delivery publication, synchronize code and vault state and re-run the current-authority gate:
   validate S1/S2, root generation and Active replan, active stage path/ID/revision, execution snapshot,
   and any C8 disposition. If unchanged with no barrier, continue. If a request is pending, do not
   publish obsolete delivery: retain the reviewed experiment as a scratch checkpoint/history bound to
   its snapshot, ensure C8 inventories that checkpoint/evidence before replanning, and return to the C8
   path with execution paused. After a batch publishes, deliver from this attempt only when its explicit
   disposition retains the same active stage/execution identity and validates the evidence against that
   stage. A replacement/successor must execute its own prepared discovery contract; the old experiment
   remains historical input, not its delivery.
4. Draft the evidence artifact and documented decision outside the vault, including the execution-entry
   snapshot, source/code revisions examined, contract/assumption IDs, result, decision criteria and
   delivered discovery-contract revisions. Publish them as one authoritative docs unit using
   superauthor A7: protected internal vault → merged docs PR; direct internal mode → configured direct
   commit; external vault → vault commit. Verify the actual A7 PR/commit and tracked artifacts. This is
   the discovery delivery identity; an ignored loop file or scratch result is insufficient.
5. Invoke superfinish with the stage, execution snapshot, and verified evidence/decision publication.
   Its closeout is a separate idempotent bookkeeping A7 unit. Then report and exit; Step 5 has no code
   worktree to remove.

If a discovery stage's approved experiment actually requires tracked code changes, use the ordinary
Steps 2–3a code path and its PR/direct-integration rules. Discovery is not a blanket exemption from
code review or integration when code changed.

## Repair successor context

For a C8 successor, read its Repair record and integration disposition before Step 2. If it
reuses a PR/worktree, verify their current branch/head and use that isolated worktree; do not
create a conflicting second checkout or blindly recreate the PR. Execute the successor's
remaining/corrective tasks and all required review/test gates, then close out the **successor**.
For a replacement, follow the plan's explicit predecessor PR disposition. Missing or conflicting
integration instructions are BLOCKED. Supersession alone authorizes neither merge nor deletion.

## Step 2 — Isolate the workspace (enter a worktree)

If `SUPER_GIT_MODE=none`, do not invoke EnterWorktree or any git fallback. Work in the recorded
physical `REPO` under the inherited project/vault workspace ownership. Validate the token and live
owner, then capture the pre-task manifest with `workspace-state.py snapshot`. Continue to Step 3.

If `SUPER_GIT_MODE=github`, use the worktree procedure below unchanged.

Before any code work, enter a git worktree via the native `EnterWorktree` tool. This is a
precondition of the task loop, required regardless of any host-repo policy on the
question. Keep multi-batch execution isolated from the primary checkout. The native tool can be
unavailable in subagent/headless contexts (a pinned cwd it cannot change) — when it is, fall back to
plain `git worktree add <path> <branch>` with absolute-path operations from there on, which
preserves the same isolation in substance.

## Step 3 — Execute the plan (invoke `superagent:superbuild`)

**For an implementation stage or code-changing discovery, you MUST use
`superagent:superbuild` to execute the target leaf plan. Do not execute code work any
other way.** Invoke it via the Skill tool and follow it exactly, supplying the
**execution profile** below.

In `SUPER_GIT_MODE=none`, this binding local-mode override governs the controller and every
implementer, reviewer, fix, and final-review prompt (superbuild B3 carries it into each dispatch):

> Git mode: none. Work in the recorded project under inherited workspace ownership. Do not invoke
> worktree, commit, PR, merge, or finishing-branch operations. Use before/after manifests and file
> content diffs for review context. Retain task reviews, final review, local tests, and acceptance
> verification. Publish local closeout only after those gates pass.

> **You must be the top-level agent of your process.** superbuild's task loop dispatches subagents and
> foreground-waits on each one; a subagent cannot foreground-wait on its own children (superloop
> L7's depth-1 constraint), so if superrun itself were a subagent, every task-loop child would background
> and yield instead of returning, and the loop would decay into `SendMessage` nudges and a
> two-writer worktree race (issue #25). A `superagent` loop therefore runs superrun in its own
> headless CLI process (`role-bridge.sh --tools executor`); a human runs it as the session's task.
> If you find you are an Agent-tool subagent anyway, stop before Step 3 and report BLOCKED:
> "superrun was dispatched as a subagent; it must run as a top-level process — see superagent
> **Subagent dispatch**." Never nudge backgrounded children along by hand.

<!-- pi-only:start
> **On Pi, the task loop's subagents are the `pi-subagents` `subagent` tool.**
> Dispatch every superbuild child with `async: false` — one child per call,
> foreground, the tool result is the child's final output. Before executing any plan task,
> verify `pi-subagents` ≥ 0.58.0 (the init prerequisite), that `SUPER_PI_SUBAGENTS` resolves to
> `required`, and that this session exposes the `subagent` tool. Normalize legacy `recommended`
> to `required` for this run and report the deprecated alias, without changing the user's
> configuration; `off` or any other value is a hard error. If any check fails, STOP with the missing
> prerequisite and `pi install npm:pi-subagents` / re-run `superagent:init` guidance.
> The task loop requires subagents; do not execute tasks in-context as a fallback.
> Never launch background, parallel, chain, or workflow runs.
pi-only:end -->

- **Read the target leaf plan yourself** for its task list and scene-setting context. superbuild
  hands each implementer its **full task text** as a brief file (the subagent never reads the plan
  file); you provide the context about where each task fits.
- Run the plan **end-to-end, fully autonomously** — do **not** pause for confirmation between tasks
  or before CI pushes.
- Honor the review plan (superbuild B2a): every task classified `task` gets its spec + quality
  review, and the whole-branch review always runs; never skip a planned review or proceed with
  unfixed issues.
- superbuild returns **complete** — with its exhaustive list of rulings and the deferred and
  parked items — **BLOCKED** (B5: a load-bearing conflict, with a cap summary when a cap ended it),
  or **CHECKPOINT** (B4.6: the dispatch deadline is near). On BLOCKED, do not integrate: go to
  the Final Report's blocked path. On CHECKPOINT, return a **CHECKPOINT report** (below) and stop.
  Carry every ruling into the Final Report.

#### CHECKPOINT — yield before the wall-clock limit

A `superagent` dispatch runs under `SUPER_EXECUTOR_TIMEOUT_MIN`; `role-bridge.sh` exports its
deadline as `SUPER_EXECUTOR_DEADLINE_EPOCH`. superbuild checks it at every task boundary (B4.6); the
same check applies before you start Step 3a's triage fix, the approved-change fix or a targeted
round; a CHECKPOINT taken there also carries the CI-PENDING fields and the triage record path, and
names the Step 3a step as **Next**. Below the margin,
return this as your final message instead of being killed mid-task. Nothing is lost: the worktree,
its commits and the ledger stay in place, and the next dispatch resumes through **Resume entry —
checkpoint**. A CHECKPOINT report is a valid yield, not a failure and not your Final Report.

    ## Superrun CHECKPOINT
    **Leaf plan:** <full path to the target leaf plan>
    **Root:** <full path to <PLAN.md>>
    **Worktree:** <absolute path — left in place>   (local mode: the project root)
    **Branch:** <branch name>   (or N/A in local mode)
    **Ledger:** <path to progress.md>
    **Done:** <tasks complete>/<tasks total>; <final review state>
    **Next:** <the next ledger step>
    **Longest command:** <command — minutes, from the ledger's Long command lines, or none>
    **Execution snapshot:** <as in CI-PENDING>
- When the tasks are done, superrun integrates the code PR **itself**, autonomously, per **Step 3a**
  below. Capture the resulting **code PR** URL for the Final Report.

### Verify delivery against the approved acceptance agreement

For each implementer and spec reviewer, provide the relevant approved checklist rows verbatim,
source revision, binding notes and resolvable full-agreement path from the plan. The final
whole-branch reviewer receives the complete agreement as context, plus the current leaf/PR's
assigned AC IDs and any explicit division of a shared item across leaves. If the plan omitted these, recover them
from its named authoritative source before dispatch; report BLOCKED if required context cannot
be resolved. Do not run a contract-only inventory stage or invoke `supercoverage` here.

Implementers report, by approved AC ID: test/subtest identifier, distinguishing input, assertion
location and meaning, and execution evidence tied to the reviewed revision (local or CI per
profile). Use concrete file evidence for non-test obligations. Parameterized tests may satisfy
multiple rows. Reviewers inspect actual evidence; mappings, test counts and green commands
alone do not establish the required assertions. Missing or ineffective evidence for an approved
item is a spec-review finding and follows the existing fix/review path. Check all assigned items
at task review and all items assigned to this leaf/PR at whole-branch review. Items explicitly
assigned to later leaves are not failures of this PR; record their ownership without marking
them delivered. If ownership is missing or conflicting, report BLOCKED for plan clarification.
Project-wide acceptance belongs to `supereval`; a leaf review cannot claim project completion.

Additional test ideas are advisory unless needed to meet an existing explicit requirement.
Ambiguity or conflict between checklist and PRD is BLOCKED for author resolution through the
existing escalation path; never silently expand or weaken acceptance scope. Ordinary bug and
code-quality review still applies. Legacy plans without a checklist retain their explicit written
requirements: verify those directly, do not invent an approval or impose a new checklist gate.

### Execution profile — this repo's `.superenv` settings for the task loop

This block is the single, consolidated statement of how this repo's `.superenv` configures
superbuild. Carry it into every dispatch the task loop makes:

1. **Test evidence is keyed by `SUPER_TEST_EVIDENCE`.** If `SUPER_TEST_EVIDENCE=ci`: implementers
   never run tests or builds locally — no test runners, no build scripts. A task's test
   evidence is the CI push its plan step specifies: the run id and conclusion. The local
   RED/GREEN output contract does not apply; reviewers judge the code plus the reported CI
   results and never execute anything themselves. If `SUPER_TEST_EVIDENCE=local` (the shipped
   default): superbuild's local RED/GREEN contract applies (B3).
2. **Conflict routing is split by consequence** (superbuild B5). A **load-bearing** conflict — a
   later task or stage builds on it, it would change acceptance, constraints, contracts or scope,
   those commitments contradict each other, or it cannot be classified — is a **BLOCKED** report carrying the finding and the plan
   text it collides with; the caller (a `superagent` loop's escalation ladder, or a human running
   superrun directly) decides. A plan **body** that fails the plan's own commitments is not
   load-bearing: it is fixed in-loop under a ruling. Anything else is ruled on, ledgered, and
   listed in the Final Report.
   Never call `AskUserQuestion` from the controller.
3. **Model policy**: dispatch each task-loop role on its
   `.superenv` model key — implementer: `SUPER_MODEL_IMPLEMENTER`, fix-applier:
   `SUPER_MODEL_FIX_APPLIER`, task reviewer: `SUPER_MODEL_TASK_REVIEWER`, re-reviewer:
   `SUPER_MODEL_RE_REVIEWER`, final whole-branch reviewer: `SUPER_MODEL_BRANCH_REVIEWER`, fix rounds
   4–5 fix-planner: `SUPER_MODEL_FIX_PLANNER` (then hand the mechanical edit to a
   `SUPER_MODEL_FIX_APPLIER` fix-applier). A value of `inherit` means omit the model override. A tier
   name (`sonnet` | `opus` | `haiku` | `fable`) is passed as the Task call's `model:` parameter. A
   **full model ID** (matches `^claude-`, e.g. `claude-fable-5`) cannot go through `model:` — the
   parameter is tier-enum-only — so dispatch that role with `subagent_type: super-<role>` (e.g.
   `super-implementer`, `super-task-reviewer`), the per-role agent definition `superagent:init`
   generates in `.claude/agents/`, and omit `model:`. A missing definition for a full-ID key, or any
   other unrecognized value, is a hard error — fail the dispatch loudly (for the missing-definition
   case, instruct a `superagent:init` re-run); never silently substitute a cheaper tier.
   **Bridged roles:** a value naming a harness other than `SUPER_HARNESS` (explicit
   `codex:`/`pi:`/`cursor:`/`claude:` prefix, or inferred — `gpt-*`→codex, `<provider>/<model>`→pi,
   tier names and `claude-*`→claude, which is bridged only when `SUPER_HARNESS` ≠ claude)
   is dispatched with `subagent_type: super-<role>` and no `model:`, exactly like a full-ID pin;
   the definition `superagent:init` generated is a relay that runs the foreign CLI and returns its
   result verbatim. A reply beginning `BRIDGE-FAILED` is a failed subagent: treat it as you would an
   implementer/reviewer that crashed (retry once, then BLOCKED), and quote the
   `log=` path in the BLOCKED report. Missing definition = hard error (re-run `superagent:init`).
   **Effort policy:** each role also has a `SUPER_EFFORT_<ROLE>` key (same names as the
   model keys). `inherit` = no override.
<!-- cc-only:start -->
   A non-`inherit` effort can only ride the
   generated per-role agent definition (the Task tool has no effort parameter) — dispatch
   that role with `subagent_type: super-<role>` and omit `model:` (the definition carries
   both pins). A missing definition for a non-`inherit` effort key is the same hard error
   as the full-ID case: fail loudly and instruct a `superagent:init` re-run.
<!-- cc-only:end -->
<!-- cursor-only:start
   Effort is not supported in this build: a non-`inherit` `SUPER_EFFORT_<ROLE>` value →
   WARN, treat it as `inherit`, and dispatch the role normally — never a hard error and
   never a definition requirement.
cursor-only:end -->
<!-- codex-only:start
   In this build the effort pin dispatches at spawn time: pass the role's resolved value
   as the spawn call's `reasoning_effort` parameter (`inherit` = omit it), alongside the
   role's model key as `model`. There are no per-role definition files on Codex and
   nothing for `superagent:init` to generate — a bad effort value fails in the spawn
   call itself. A **bridged** role (harness ≠ codex) is spawned as a relay: `model` =
   `SUPER_BRIDGE_RELAY_MODEL` (omit when `inherit`), message =
   `${SUPER_PLUGIN_ROOT}/templates/relay-preamble.md` rendered for the role + the full
   task prompt; a `BRIDGE-FAILED` reply is a failed subagent.
codex-only:end -->
<!-- pi-only:start
   In this build a role's pins ride the `pi-subagents` agent definition `superagent:init`
   generated at `.pi/agents/super-<role>.md`: dispatch the role with `agent: super-<role>` and
   no model/thinking override on the call (native definition = model/thinking pins; bridged
   definition = a relay that runs the foreign CLI and returns its result verbatim — a reply
   beginning `BRIDGE-FAILED` is a crashed child: retry once, then BLOCKED,
   quoting the `log=` path). A role with both keys `inherit` still has a named definition,
   with no model/thinking fields: always pass `agent: super-<role>`. A missing definition
   for any task-loop role is a hard error (re-run
   `superagent:init`). An unavailable `subagent` tool is also a hard error under the
   prerequisite above; never execute the role without its required dispatch.
pi-only:end -->
4. **Reviewer labels — keyed by `SUPER_REVIEW_CONFIDENCE_FILTER` (shipped default `controller`,
   the only supported value).** Reviewers report **every** finding with a severity **and a
   confidence label**; the controller filters to high-confidence findings before acting on or
   surfacing them. Never instruct a reviewer to report only high-confidence issues — Claude
   5-family reviewers apply that filter silently and drop real findings.
   **Review depth is keyed by `SUPER_REVIEW_DEPTH`** (superbuild B2a). `risk` (the shipped
   default): the controller — on `SUPER_MODEL_EXECUTOR` — classifies each task before execution;
   risky tasks get their own review, mechanical isolated ones are reviewed only in the whole-branch
   review. `full`: every task gets its own review. The whole-branch review always runs.
5. **Integration is owned by Step 3a**, for attended and unattended callers alike — there is no
   interactive completion menu. (`SUPER_SKIP_FINISHING_HANDOFF` is retired: the key is accepted and
   ignored.)
6. **Repo notes.** If `SUPER_REPO_NOTES` is set, read that file before starting the task loop and
   treat it as standing repo policy.
7. **Protected surfaces — keyed by `SUPER_PROTECTED_PATHS`** (empty by default). A path matching
   one of its globs (`superagent_protected_match` in `scripts/_common.sh`; source it under bash),
   an approved acceptance row, or a value the project's own instructions pin is a protected
   surface. No executor ruling, fix round, final fix wave or CI-triage fix may change one
   (superbuild B5). When the fix needs one, the outcome is BLOCKED with the exact change named
   (file, old value, new value, evidence), so the supervisor can ask the owner a yes/no
   protected-change question (superloop L7). An owner approval recorded under the loop's
   `## Decisions` and passed to you as guidance authorizes exactly that change and nothing wider.

### CI scheduling — queue all shards (keyed by `SUPER_CI_RUNNERS`)

If `SUPER_CI_RUNNERS > 1`, this repo's CI shares one job queue across that many identical runners —
the next free runner picks up the next queued run. When the leaf plan's tasks trigger **more than
one independent long CI push** (>10 min each — e.g. a shardable stress lane split into per-shard
pushes, or two unrelated long lanes), **queue them all back-to-back, then wait on all of them
together**:

1. Push every shard/lane now — each as its own commit + push. If `SUPER_CI_FLAG_TEMPLATE` is set
   (e.g. `[test:%s]`), stamp each push with it — when `SUPER_CI_ONE_FLAG_PER_PUSH=true` (the shipped
   default), **exactly one** flag per push; sharding is *more pushes queued at once*, never more
   flags per push. If `SUPER_CI_FLAG_TEMPLATE` is empty, the repo has no commit-flag system — push
   normally.
2. Record **every** resulting run id; the CI-green gate (Step 3a) waits on **all** of them in a
   single monitor-parked wait.
3. Serialize two pushes **only** across a genuine procedural gate the plan names — worked example
   from the originating repo: a smoke lane that must be green before its expensive baseline, like
   `multi_motif_smoke` → `multi_motif`. Runner contention is never a reason to serialize — the queue
   handles it.

If `SUPER_CI_RUNNERS=1` (the shipped default), there is no runner contention to exploit: push and
wait for CI runs in the order the leaf plan specifies. A plan that names a shardable batch still
queues every shard's push together and waits on all run ids in one monitor-parked wait (Step 3a) —
it just gets no benefit from parallel pickup. If the plan text stages pushes serially with no named
procedural gate under `SUPER_CI_RUNNERS > 1` (a leftover of single-runner-era authoring), queue them
concurrently anyway and note the deviation in the Final Report.

## Step 3a — Autonomous code-PR integration

If `SUPER_GIT_MODE=none`, suppress this entire integration stage. Capture the resulting snapshot, compare it to the
pre-task manifest, rerun final workspace acceptance checks, and retain the exact command results,
review outcomes, and evidence paths for Step 4. Do not reinterpret CI-only acceptance; the resolver
has already rejected `SUPER_TEST_EVIDENCE=ci`. Continue directly to Step 4.

Step 3a owns integration end-to-end, whoever the caller is. Integrate the code PR with **no interactive prompt**,
merging only when the CI-green gate below — or its review-green fallback — is satisfied. This
integration step is itself keyed by `SUPER_PROTECTED_MAIN` — the CI-gate keying in item 2 below still
governs whether to wait for CI **first**, in both branches; only the merge mechanism at the end (item
3) differs. Both key states need the primary checkout's absolute path below — derive it once, before
item 1, so it is defined for every use in either branch:

```bash
primary_root="$REPO"
```

1. The leaf plan's own task steps already pushed to CI with the flag `SUPER_CI_FLAG_TEMPLATE`
   specifies, if any (see Step 3). Ensure the feature branch is pushed — if `SUPER_BRANCH_STYLE=flat`
   (the shipped default), use a flat branch name with no slashes (a slashed name can miss CI's branch
   glob); if `SUPER_BRANCH_STYLE` is anything else, follow that style instead. If
   `SUPER_PROTECTED_MAIN=true` (the shipped default), also open the code PR with `gh pr create`. If
   `SUPER_PROTECTED_MAIN=false`, skip `gh pr create` — there is no PR in this branch, only the pushed
   feature branch (still pushed so CI, if any, has something to run against). Record the execution-entry
   snapshot in the PR description when there is a PR, or in the verified direct-integration evidence
   handed to superfinish when there is not; this makes a lost response recoverable from actual delivery
   history.
2. **CI-green gate — monitor-parked, never polled — keyed by `SUPER_TEST_EVIDENCE` three ways:**
   - **`SUPER_TEST_EVIDENCE=ci`:** collect the run id of **every** CI run this leaf queued (`gh run
     list --branch <branch>` — one run per push; a sharded batch has several, see **CI scheduling**
     in Step 3), then wait for all of them (wait mechanics below). If the plan expected a run and
     `gh run list` finds none, that is **BLOCKED** — do not merge.
   - **`SUPER_TEST_EVIDENCE=local`** (the shipped default) **and `gh run list --branch <branch>`
     returns runs** — the repo has CI wired even though evidence is local: wait for those runs to be
     green before merging (same wait mechanics as the `ci` branch).
   - **`SUPER_TEST_EVIDENCE=local` and no runs exist:** CI evidence is not expected for this repo.
     Skip the wait entirely and merge on review-green alone — the task reviews and final
     whole-branch review already completed in Step 3 are the evidence. State this explicitly in the
     Final Report (e.g. "no CI configured for this repo; merged on review-green").

   When a wait is needed (either of the first two branches above), never wait with `gh run watch`,
   foreground sleeps, or backgrounded re-poll loops — every poll iteration re-enters your context and
   a long lane (60–120 min) burns it for nothing. Instead:
<!-- cc-only:start -->
   - **Standalone (superrun is the top-level session's task):** arm **one `Monitor`**
     (`persistent: true`) whose check `curl`s
     `https://api.github.com/repos/<owner>/<repo>/actions/runs/<id>` for **each** pending run id
     (auth: `TOK=$(gh auth token)` captured before arming). Prefer `curl` for polling inside a
     Monitor — on hosts where `SUPER_GH_DISABLE_SANDBOX=true`, `gh` cannot run *inside* the Monitor
     at all (it needs keychain access), so `curl` to `api.github.com` is the only option there; where
     `SUPER_GH_DISABLE_SANDBOX=false`, `curl` is still preferred for consistency. Fire the Monitor the
     first time **every** run reports `status: completed`, emitting each run's `id: conclusion` pair.
     It MUST emit on **any** terminal state — success, failure, cancelled, timed_out — never only on
     success (a success-only filter is silent through a crash, and silence is indistinguishable from
     "still running"). Then **end the turn**; the harness re-invokes you when the Monitor fires.
<!-- cc-only:end -->
<!-- cursor-only:start
   - **Standalone (superrun is the top-level session's task):** there is no Monitor tool in this
     build, so do not wait in-session at all. Report the queued run ids, the worktree/branch/PR
     packet, and how to check the runs (`gh run list --branch <branch>`), then **end the turn**.
     Once every run is terminal, re-invoke superrun via its **Resume entry — post-CI** with that
     packet and the conclusions to finish the leaf.
cursor-only:end -->
<!-- codex-only:start
   - **Standalone (superrun is the top-level session's task):** there is no Monitor tool in this
     build, so do not wait in-session at all. Report the queued run ids, the worktree/branch/PR
     packet, and how to check the runs (`gh run list --branch <branch>`), then **end the turn**.
     Once every run is terminal, re-invoke superrun via its **Resume entry — post-CI** with that
     packet and the conclusions to finish the leaf.
codex-only:end -->
   - **Dispatched by a `superagent` loop (a headless process the supervisor is blocking on):** do
     NOT arm the wait yourself (a Monitor cannot outlive your process) and do NOT emit interim
     "still waiting" notifications. Return a **CI-PENDING report** (format below) as your final
     message and stop — your process ends with it. The supervisor owns the wait and later starts a
     fresh superrun process with this packet plus the terminal conclusions (see **Resume entry —
     post-CI**). A CI-PENDING report is a valid yield, not a failure and not your Final Report.

         ## Superrun CI-PENDING
         **Leaf plan:** <full path to the target leaf plan>
         **Root:** <full path to <PLAN.md>>
         **Worktree:** <absolute path — left in place>
         **Branch:** <branch name>
         **Code PR:** <url> (open — awaiting CI) — or `N/A (SUPER_PROTECTED_MAIN=false)` if there is no PR
         **CI runs:** <every queued run id, comma-separated>
         **Execution snapshot:** generation <N>; stage <ID> revision <N>; preparation <path> digest <sha256>;
         vault commit <sha>; reviewed code <sha>; source <revision>; consumed deliveries <IDs/receipts>
         **Remaining:** CI-green gate verdict (Step 3a) → superfinish closeout (Step 4) → worktree exit (Step 5)

   On the terminal state (Monitor fired, or the supervisor resumed you) — or immediately, when no
   wait was needed (`SUPER_TEST_EVIDENCE=local` with no runs found), run this **integration-authority
   gate before either merge mechanism**:

   - synchronize authoritative code and vault state; re-read S1/S2, the active Plan link, root
     generation/Active replan, current stage identity, and any C8 record/disposition;
   - match the branch, PR/head or direct-integration candidate, and execution-entry snapshot. For an
     unchanged active stage with no barrier, continue. A pending batch is a whole-goal barrier even
     when CI is green. Preserve the old PR/branch/worktree/run evidence in that record and do not merge
     while its stage disposition is unresolved;
   - when a batch published after execution began, never merge from the queued packet alone. Direct
     post-CI completion is allowed only when the record explicitly retains the **same execution
     identity**: same active stage path/ID/revision, prepared plan/receipt and execution attempt, with
     focused new-generation validation and an integration disposition that preserves it. A mapped
     successor is different even when it says `resume-existing`: route that active prepared successor
     through normal Steps 1–3 on the reused branch/worktree, capture its own execution snapshot, execute
     remaining/corrective tasks, and rerun required reviews/tests. Old CI remains historical evidence
     and cannot merge or close either identity. `replace`, retirement, changed or unmapped identity,
     unresolved disposition, missing record, or contradictory publication likewise blocks direct merge
     and preserves the old integration history for reconciliation.

   This gate applies identically to ordinary completion and post-CI resume. A barrier/identity failure
   returns BLOCKED or REPLAN-REQUIRED with the root, Decision ID, stage, PR and snapshot; it never closes
   or merges the old PR and never treats green CI as authority. Once the gate passes:

   - **ALL runs GREEN, or no CI wait was needed** → (`SUPER_PROTECTED_MAIN=true`, the shipped
     default) merge per `SUPER_MERGE_METHOD` (default `squash`) — e.g.
     `gh pr merge --squash --delete-branch` (plain merge — **not** `--admin` unless
     `SUPER_ADMIN_MERGE=true` permits it; see item 3) — then
     `git -C "$primary_root" pull --ff-only`. When `SUPER_PROTECTED_MAIN=false`,
     integrate via item 3's direct-merge recipe instead — no PR, no `gh`.
   - **ANY run RED / cancelled / timed_out** → **do NOT merge.** Leave the PR open, capture the
     failing run URL(s), and run **CI-failure triage** (below) before anything else. If triage's
     cheapest fix is in scope and touches no protected surface, apply it and push again within this
     dispatch; otherwise declare the step **BLOCKED** in the Final Report with the triage record.
   - **`SUPER_TEST_EVIDENCE=ci` expected a run and found none** → **do NOT merge.** Declare the step
     **BLOCKED** in the Final Report; there is no run to triage.

   (When a `superagent` loop drives superrun, its escalation ladder decides what happens after
   BLOCKED; a human caller sees the blocker plainly.)
3. **If `SUPER_PROTECTED_MAIN=true` (the shipped default): merge per `SUPER_MERGE_METHOD` (default
   `squash`). Pass `gh pr merge --admin` only if `SUPER_ADMIN_MERGE=true` — otherwise never.**
   Reaching for `--admin` when the key is unset or `false` buys nothing on a repo whose branch
   protection doesn't require it, and reliably **trips the harness security classifier**, which reads
   merge-over-red as a privileged override and denies it. If the plain merge is actually refused,
   escalate to `--admin` only when `SUPER_ADMIN_MERGE=true` permits it, and report why. Full rationale
   in `superauthor` clause **A7**. Note that `--delete-branch` can exit 1 with `fatal: '<branch>' is
   already used by worktree` **after a successful merge** — that is the local delete step, not a
   rejection; confirm with `gh pr view <n> --json state,mergedAt` and drop the remote ref via
   `gh api -X DELETE repos/<owner>/<repo>/git/refs/heads/<branch>` rather than re-running the merge.

   **If `SUPER_PROTECTED_MAIN=false`: no PR, no `gh` — merge the worktree branch into the default
   branch directly and locally, from the primary checkout** (the worktree stays on its feature
   branch throughout — `git checkout <default-branch>` is invalid there, since Step 2's linked
   worktree already has the default branch checked out at the primary), once the CI-gate above
   (item 2) is satisfied:

   ```bash
   git -C "$primary_root" merge --no-ff <branch>   # or per SUPER_MERGE_METHOD, e.g. --squash — but
                                                    # --squash stages without committing, so follow it with:
                                                    # git -C "$primary_root" commit -m "<leaf-plan title>"
   git -C "$primary_root" push   # only if a remote exists — a repo with no remote simply keeps the merge local
   ```

   Put the complete execution snapshot in the merge/squash commit message body so direct integration
   has the same recoverable identity as a PR description. Verify that commit on authoritative main
   before invoking superfinish.
4. If `SUPER_GH_DISABLE_SANDBOX=true` (macOS hosts where `gh` needs keychain access to verify the
   TLS cert), all `gh` commands need `dangerouslyDisableSandbox: true`. If `false` (the shipped
   default), run `gh` normally. Do **not** add Anthropic/Claude attribution or `Co-Authored-By`
   trailers (repo policy).

### CI-failure triage — before BLOCKED

A red run is not yet a blocker. A timeout, a failing test and a broken runner need different fixes,
and only the executor holds the worktree, the logs and the plan context at once. Spend a few
minutes on ordinary triage before you report anything, and write the result to the superbuild
ledger as `CI triage <n>: <run id> — <class> — <cause> — <fix>`, with the full record in
`<dir>/ci-triage-<n>.md`.

1. **Where it failed.** The failing job and step, and the step's duration (`gh run view <id>
   --json jobs`).
2. **Class:** `timeout`, `test-failure`, `setup/infra`, or `unknown`.
3. **For `test-failure`:** the failing test IDs and the assertion line, from the job log
   (`gh run view <id> --log-failed`) or the run's junit/test-report output.
4. **For `timeout`:** the limit that was hit and where it is configured (file and line), plus the
   same step's duration on the last green run of the default branch (`gh run list --branch
   <default> --workflow <workflow> --status success -L 1`). When several runs are at hand, note the
   spread of durations.
5. **For `setup/infra`:** what never became ready and why, from the job log and any container or
   service exit state the standard job output shows (an import error at startup, a missing file in
   an image, a dependency that failed to install).
6. **Ownership.** Whether each failing test is in a file this branch added or changed.
7. **The best-supported cause**, in one sentence, with the two or three facts that support it and
   what you did not check. Then the **cheapest fix**: the files it touches, whether it is in this
   stage's scope, and whether it touches a protected surface (Execution profile item 7 — run
   `superagent_protected_match` over its file list, and check value pins the project's instructions
   name).

**The evidence bar is the best-supported explanation, not proof.** A step whose duration matches a
configured limit — within a few seconds, or with the limit quoted in the log — timed out; that is
sufficient evidence. Do not require a directly observed kill record: a runner or `subprocess`
timeout kills the child internally and leaves none. Classify `unknown` only after reading the
failing step's log, and say in the record what you read. Read the ordinary CI job log and
junit output by default; honour any project rule that excludes a specific sensitive source, such as
privileged service logs, and name what that left unread.

**Act on it.**

- **In scope and unprotected** — a failing test or code the branch added, an image or workflow line
  the stage owns, a test this branch made slow: apply the fix through superbuild's fix mechanics —
  one FIX_APPLIER with the triage record as its finding, then one RE_REVIEWER over the fix range
  (superbuild B4.4 *Every round*) — ledger `CI fix <n>/2 (<base7>..<head7>)`, push, and return to
  the CI-green gate above (under `superagent`, that is a fresh CI-PENDING report). At most **two**
  triage fixes per leaf for the same failing step; a third red run on that step is BLOCKED with every
  triage record and a cap summary in `<dir>/cap-summary-ci.md` (superbuild B5's four fields, one
  entry per triage record).
- **A `[planner]` constraint in the way** — a plan restriction tagged `[planner]` (a diagnostic budget,
  a ban on rerunning a job after a fix) may be relaxed under a superbuild B5 ruling when triage shows
  the fix needs it; ledger the ruling and proceed as above. `[source]` and `[owner]` restrictions
  never are.
- **Out of scope, or touching a protected surface** — BLOCKED, with the triage record and the exact
  change the fix needs (file, old value, new value) in the Final Report. Do not work around a
  protected limit inside the stage, and do not build observation tooling to strengthen a cause the
  evidence already supports. When a genuinely unexplained failure needs instrumentation, it stays in
  scratch or on a throwaway branch (superbuild: *Keep investigation out of the delivery*); push the
  throwaway branch for a diagnostic CI run, never the stage's PR.
- **`unknown` after reading the log** — BLOCKED with the triage record, naming what was read and the
  cheapest further read-only check.

Triage never replaces the rules around it: red CI still never merges, and rerunning the same commit
unchanged is not a fix. Act on the best-supported cause; do not retry until green.

### Resume entry — post-CI (superagent-driven)

When superrun is invoked with a **CI-terminal
resume packet** — the CI-PENDING fields (leaf plan, root, worktree, branch, PR url, run ids) plus each
run's terminal conclusion — first require its complete execution snapshot. Enter the recorded worktree
(it was left in place), verify the actual branch/PR head and each conclusion with one `gh run view <id>`
per run (trust but verify — the packet may be stale), then run Step 3a's integration-authority gate
against the current authoritative root, C8 record, and disposition. A packet queued before a batch
request is recovery evidence, never merge authority. Re-read the superbuild ledger left in the
worktree (`superbuild.sh workspace <leaf plan>` → `progress.md`) for the rulings, deferred items,
and earlier `CI triage` / `CI fix` lines the Final Report must carry; the queuing process's memory
is gone. If any conclusion is not `success`, this resume process runs **CI-failure triage** (Step
3a) — it holds the worktree — and counts the ledger's earlier `CI fix` lines toward the cap.

Only when the active identity is unchanged (including an explicitly retained same-identity stage
validated in the new generation) may this terminal handler avoid re-running Steps 1–3, merge after both
CI and current authority pass, and continue with Steps 4–5. If C8 maps the packet to a successor, the
old terminal packet is a redirect rather than execution evidence for that successor: re-enter normal
target/receipt validation, use the successor's authorized reused branch/worktree, capture its new
execution snapshot, and run its remaining/corrective tasks, reviews, and tests through Steps 2–3 before
any merge or closeout.

### Resume entry — checkpoint (superagent-driven)

When superrun is invoked with a **CHECKPOINT packet**, first require its execution snapshot. Enter the
recorded worktree (local mode: the recorded project under the inherited lock), verify the branch head
against the ledger's last range, and re-run the Step 1 execution-entry checks for the recorded identity
— a changed active identity or a pending barrier is handled as there. Then re-invoke superbuild on the
same leaf: it resumes from the ledger (B1) and runs to completion, BLOCKED or the next CHECKPOINT. When
**Next** names a Step 3a step (a CI fix, an approved change, a targeted round), resume at that step
with the packet's CI fields and triage record instead of re-invoking superbuild. Continue with Step 3a
once superbuild returns complete.

**Single-step guidance** (from the supervisor after repeated timeouts) may accompany this entry or
an ordinary dispatch. Pass it to superbuild in Step 3 either way: superbuild then runs exactly one
ledger step before yielding CHECKPOINT (B4.6).

### Resume entry — targeted round (superagent-driven)

When superrun is invoked with a **targeted round** — the blocked attempt's packet (leaf plan, root,
worktree, branch, PR url, execution snapshot), the cap summary's path, and the one change the panel
chose from it (with its Decision ID) — do not re-run Steps 1–3. Enter and verify the worktree and run
the integration-authority gate as in **Resume entry — approved protected change** step 1. Dispatch
one FIX_APPLIER with exactly that change as its finding, then one RE_REVIEWER over the fix range,
and ledger `Targeted round: <finding> (<Decision ID>) (<base7>..<head7>)`. If the re-review closes
the finding, push and return to Step 3a's CI-green gate; if not, return BLOCKED with the updated cap
summary. One targeted round per finding: a second request for the same finding is BLOCKED.

### Resume entry — approved protected change (superagent-driven)

When superrun is invoked with an **approved protected change** — the blocked attempt's packet (leaf
plan, root, worktree, branch, PR url, execution snapshot) plus the change exactly as recorded under
the loop's `## Decisions` (files, old value → approved value, Decision ID) — do not re-run Steps 1–3
and do not apply anything wider than that change:

1. Enter the recorded worktree, verify the branch and that the PR is open at the recorded head, and
   run Step 3a's integration-authority gate against the current root, C8 record and disposition. A
   failed check is BLOCKED with what did not match.
2. Apply exactly the approved change through superbuild's fix mechanics: one FIX_APPLIER whose
   Context names the change as approved, with the Decision ID, then one RE_REVIEWER over the fix
   range. Ledger `Approved change: <file> <old> → <new> (<Decision ID>) (<base7>..<head7>)`. The
   approval covers that change only; any other edit it turns out to need is BLOCKED with a new
   triage record.
3. Push and return to the CI-green gate (Step 3a) — under `superagent`, a fresh CI-PENDING report.
   A later red run on the same step is triaged as usual, and the ledger's `CI fix` lines still count
   toward the cap.
4. Once merged, Step 4 runs superfinish, which reconciles the earlier partial closeout into the
   delivered one; Step 5 follows.

## Step 4 — Close out the plan (invoke `superagent:superfinish`)

Once execution is complete, invoke the `superagent:superfinish` skill (Skill tool), **passing the
target leaf `<PLAN.md>`, its execution-entry snapshot, and actual delivery evidence** (superfinish's
Gate-1 resolution precedence #2 — "passed by a calling
skill"). It captures findings, writes the closeout report, annotates the leaf plan, runs
`supertraverse` **completion-mode ascent** (C7) to advance the parent seed's progress-report table,
and merges its docs-only **closeout PR**. Capture that PR URL too.

The evidence-only discovery branch reaches Step 4 through its earlier A7 publication without a code
PR. A discovery stage that changed tracked code reaches Step 4 through the ordinary integration path.
In both cases pass the evidence, documented decision, and delivered discovery-contract revisions to
superfinish. Absence of source-code work is not a waiver of the stage's evidence contract.

## Step 5 — Worktree lifecycle

In `SUPER_GIT_MODE=none`, there is no worktree lifecycle. Reopen the completed-local receipt and
reported artifacts, remove this leaf's superbuild scratch directory
(`<REPO>/.superagent-runtime/build/<plan-slug>/`) once its rulings are in the Final Report, then
return the Final Report without git cleanup.

After `superfinish` reports the work merged, exit the worktree via `ExitWorktree`
(worktree is kept only while a PR stays open). When that tool is unavailable (a headless process
whose allowlist lacks it — the `superagent` dispatch path), do the equivalent by hand from the
primary checkout: `git worktree remove <path>` (the branch is already merged and deleted remotely).
Before removing the worktree, delete this leaf's superbuild scratch directory inside it
(`<worktree>/.superagent-runtime/`) — its rulings must already be in the Final Report.
If the **code PR** was left open in Step 3a (CI red /
BLOCKED, not merged), leave the worktree in place and note that in the Final Report.

## Final Report — then exit

Give the user a single report and exit. **Ground every line in evidence from this session** — a tool
result, PR URL, or CI conclusion you actually observed. If something is not yet verified (e.g. a merge
you did not confirm landed), say so explicitly rather than reporting it done:

    ## Superrun complete

    **Executed plan:** <full path to the target leaf plan>
    **Root:** <full path to <PLAN.md>>
    **Worktree:** <path> (exited / left in place — code PR open)

    **Code PR:** <url> (merged)               ← or (open — BLOCKED: <reason>, CI run <url>)
    **Discovery evidence:** <A7 PR url or external-vault commit> (verified)  ← evidence-only discovery; Code PR is N/A
    **Closeout PR:** <url> (merged)            ← from superfinish

    **Findings:** <summary>                    (or: none — superfinish recorded none)
    **Rulings:** <every superbuild ruling, in order: decision — why — cost if wrong>   (or: none)
    **Review depth:** <N> task-reviewed, <M> branch-only (<SUPER_REVIEW_DEPTH>); upgrades: <list or none>
    **Cap summary:** <per open finding at a cap: tried — why it did not land — smallest closing change (in scope?; protected?)>   (or: none)
    **CI triage:** <per red run: class — best-supported cause (facts; not checked) — cheapest fix (files; in scope?; protected?) — applied / not applied>   (or: none)

    ⚠️ **Critical:** <only when a finding or blocked task needs attention>

If execution was **blocked** (superbuild returned BLOCKED — a load-bearing conflict, a plan that is
wrong, a task too large, missing context — or the Step 3a CI-green gate was red), do **not** fabricate
completion and **do not merge** the code PR: report the blocker plainly, note what was and wasn't done,
and still run `superagent:superfinish` so the partial outcome is recorded honestly. A CI-red blocker
always carries its **CI triage** record. A blocker whose fix needs a protected surface names the exact
change — file, old value, new value, and the evidence in two or three lines — so the caller can ask
for exactly that change. A blocker issued at a cap (fix rounds, final fix waves, CI-triage fixes)
carries the **cap summary**: for each open finding, what was tried, why it did not land, the smallest
change that would close it, and whether that change is in scope and touches a protected surface.

After printing the report, the skill is done: take no further action and ask no follow-up question.
