---
name: keiko-epic
description: Drive a multi-issue GitHub epic end-to-end — plan and order child issues, run them on an epic integration branch, and deliver one green epic PR to dev under target authority and explicit run review choices. Use when the operator selects an epic to work on. Composes keiko-issue per child. Takes an epic number.
---

# keiko-epic

Canonical, parameterized epic workflow for both harnesses. Replaces the old
`codex-epic-prompt.md` / `claude-epic-prompt.md` run-cards. **Defers to**
`docs/workflow-contract.md` for the model and **composes** `keiko-issue` (per
child) and `keiko-issue-audit`. Do not restate contract rules.

**Argument:** the epic issue number `#E`.

## Role

You are the lead session — the sole orchestrator. Never spawn a sub-coordinator.
Compose `keiko-issue` for every child. Execute a small child directly or delegate
it under that skill’s proportional routing; preserve its independent audit.

## 0. Select the product profile (before planning)

Select against the target checkout using [profile selection](../../../profiles/README.md).
State the profile on the first output line; explicit operator selection wins.
Load only the selected profile and its task-relevant authority docs, including the
target's `AGENTS.md` and `CONTEXT.md` when present. Take readiness, verification,
templates, evidence, exclusions, and merge authority from it; ambiguity requires
clarification. The accepted target contract governs product requirements.

Target `AGENTS.md`, scoped instructions, ADRs, and explicit user choices override
generic workflow defaults. For Keiko, ADR-0135 authorizes accepted, checked
`dev` delivery through native auto-merge; ADR-0145 retires `agent:pre-pr`.
An explicit final epic human-review hold overrides target-authorized final auto-merge
for that run and adds no per-child approval. Preserve it until the human explicitly
authorizes final delivery; a green PR or an approval from another agent does not
lift it. Otherwise retain the generic final human-review default where the target
and user have not authorized another path.

Record the run's delivery choice once during intake, using the user's existing
instruction. “Autonomous until the final green epic PR, then human review” means
children integrate autonomously and the final epic PR remains unmerged for human
review. It authorizes implementation, local verification, child delivery and final
PR maintenance without another routine approval round. Ask only if a required
choice is missing or contradictory; never re-ask a choice already supplied.
Record this choice in the existing epic issue milestone comment at the start and
carry it into the final PR body or milestone comment. On resume, read that durable
run state before delivery; preserve the hold in evidence after every final push.
Use GitHub’s existing record, not a local receipt or another state store. A final
held PR must have auto-merge unarmed throughout CI/review maintenance; green checks
do not change the recorded choice.

Child-loop examples below use web branches and Playwright. Native uses its frozen
delivery target, runner-managed source branches, dedicated automation identity, and
Acceptance Journey harness; never assume a browser host or private-source access.

## 1. Read & plan

Fetch `#E`: body, comments, labels, child issues (sub-issues + linked), linked
PRs, board state. Build the execution plan:

- list every child with state, labels, area, likely file ownership, dependencies, verification, **and current GitHub assignee**;
- classify readiness using the selected profile. **keiko-web:** accepted children in
  `New` or `Triaged` are executable when acceptance criteria and verification are
  complete; those states alone do not block intake. Resume `In Progress`/`PR Open`
  work only within its accepted scope. Actual `Blocked` or `Waiting for User`
  states remain non-executable until the blocker is resolved or the requested
  decision arrives. **keiko-native:** follow the target's validated lifecycle
  (`profiles/keiko-native.md` → Issue lifecycle); `new`/`triaged` remain
  non-executable, and a current accepted readiness record does not bypass state
  action limits. Treat `done` as completed, and a child assigned to someone other
  than the operator as **owned — skip it**;
- respect the epic's required order; detect safe parallelism **only** when children have disjoint file ownership, independent acceptance criteria, and no ordering dependency.
  If the epic has no executable children and scope isn't clear enough to create them, stop and report.

Each `keiko-issue` child run assigns the operator (`--add-assignee @me`) as it
claims, and skips any child that's already assigned to someone else.

## 2. Epic branch

**Dev-baseline preflight (before committing to a long Web epic).** Check the
applicable integration run at the current `dev` HEAD against the target's current
contract. Under ADR-0178, the canonical resolver may reuse complete successful
pull-request evidence for the exact merged PR's byte-identical tree. Record the
integration run and its proven-tree evidence identity; sanctioned reused jobs do
not need duplicate check runs on the squash SHA. The coverage chain and SonarCloud
branch analysis still run on every `dev` push. A failed executed check remains red;
missing, pending, or unproven evidence is not green. Resolve or wait before starting.
This integration-only reuse never permits missing, skipped, or stale required
checks on a child or final epic PR: every PR needs the full exact-head matrix.
Native uses its frozen accepted delivery target and current activation contract.

Create one long-lived `epic/<name>` or `codex/epic-<name>` off the latest `dev`.
Record it on the board and an epic comment before implementation starts. Child
branches `issue/<id>-<short>` or `codex/issue-<id>-<short>` are cut **off the epic
branch**, not off `dev`. Run applicable local checks before pushing scoped
implementation. Native retains its frozen Execution Authority and delivery contract.

**Web integration-branch CI wiring (before any child integration).** Inspect the
target's current workflow contract and register a new long-lived epic branch
where required. Keiko requires it in `ci.yml`'s `push` and `pull_request` trigger
lists and protected-branch-gate allowlist, CodeQL's two trigger lists, and
Dependency Review's pull-request list. Run the target's workflow-consumer inventory
before editing, the applicable workflow checks, and `check:workflow-branch-parity`.
Make these scoped setup changes under the accepted epic authority, then prove
child PRs actually receive the full exact-head target matrix. A branch absent
from a trigger/allowlist is not ready for child integration. Missing checks never
qualify as green. Follow current target rules if these consumers change; do not
weaken protections or require optional branch protection merely to register CI.

Keep Web setup changes in a setup/child PR to the epic branch, with that candidate
carrying the required registration. Qualify its actual full target matrix before
integration. Do not open a bootstrap PR to `dev`: the single epic PR is opened
last, after all accepted work, base synchronization, integrated verification and
independent audit are complete (§4). If the target cannot run the full setup
matrix without a prior `dev` change, report that concrete delivery blocker; do
not create an early `dev` PR or accept missing checks.

## 3. Child loop (per executable child)

**Children run AFK (no human-in-the-loop per child).** A child integrates into the
epic branch **autonomously** — there is no per-child human review or sign-off. The
final review hold, when requested, applies to the **epic → `dev`** PR (the full
feature). A child
either **auto-merges on green machine evidence**, or it **escalates as an exception**
(something went wrong); it never pauses to wait for a human to approve that one child.

1. Run **`keiko-issue` `#child`** on its branch off the epic branch (it runs
   applicable local checks + `keiko-issue-audit` as part of its flow).
2. The child PR targets the **epic branch**. Run applicable local checks and the
   independent issue audit; fix confirmed findings and re-audit, bounded to three
   materially distinct repair attempts. User-facing children execute the accepted
   journey: Web uses runnable Playwright steps that assert acceptance criteria,
   fidelity and accessibility; Native uses its target-owned Acceptance Journey.
   Report actual command, audit and UI results with the exact PR head in its body
   or a comment. Optional subjective follow-ups go into final epic evidence;
   required journey/platform evidence must run before child integration.
   Wait for the full successful target required-check matrix on that exact head
   and settled reviews. Arm authorized native auto-merge with
   `gh pr merge <N> --auto --squash --match-head-commit <exact-head-sha>`.
   Native's dedicated identity and accepted authority still govern its merges.
   Never bypass checks, force-push or push directly to `dev`. Missing evidence
   means repair or escalation, never a per-child human approval ceremony.

3. **Child closeout — mechanical checklist (all must hold before the next child):**
   - [ ] PR **base** is the epic branch (not `dev`/`main`/`release`).
   - [ ] **Merge** landed through the target-authorized path.
   - [ ] **Post-merge verification:** epic branch passes applicable target checks at the new epic HEAD.
   - [ ] **Close the child as done.** With the child PR **merged into the epic branch**
         and all accepted scope stages and their evidence complete, transition the
         child to the profile's **done** state and **close it**. **keiko-native:** close with reason `completed` carrying
         exactly **`status: done`** (other `status:*` removed), a projection of
         `docs/qa/issue-lifecycle.md` — read it at runtime and **fail closed** if
         labels/contract are missing/stale; never let the board grant the transition.
         **keiko-web:** close + `status: done`. Never close a child whose PR is not
         merged or whose accepted stages remain. Separately audited stages do not complete the whole issue.
   - [ ] **Closure evidence** recorded: child comment linking PR/commit + verification/audit evidence; board updated (a projection of the closed/`done` state).
         Any unchecked box → stop and resolve before moving on.
4. Synchronize `dev` into the epic branch regularly (especially before the final
   PR) through the target’s permitted history policy. Preserve published commits;
   never force-push or rewrite the shared epic branch. If the permitted path
   cannot reconcile it, report the concrete blocker.
   **Dependency-readiness trace (before starting any runtime/dependent child):** do
   not start a child on the strength of an upstream issue merely being "closed" —
   trace the dependency **end-to-end** and confirm it is _actually_ ready: the
   upstream runtime / contract / artifact it consumes exists on the epic branch,
   builds, and its interface contract holds. If the trace fails, the child stays
   `blocked`. Never start `blocked` work. Parallelize children only when section 1's
   safety conditions all hold.

## 4. Final epic PR (target authority and run review hold)

When all required children are integrated on the epic branch:

1. **Synchronize the latest `dev` under the target’s history policy FIRST** —
   resolve conflicts without dropping others' work or rewriting published history.
   Everything below runs against this integrated HEAD; if `dev` moves again,
   re-integrate through the permitted path and rerun affected verification/audit.
2. **Verify and independently audit the integrated epic.** Run all applicable
   target checks, fix confirmed findings and re-audit until clean, bounded to
   three materially distinct repair attempts. Execute required integrated UI
   journeys through the active profile's accepted harness.
3. **Open the epic PR `epic/<name> -> dev`.** Fill the target template with the
   child matrix, capability summary, exact-head command/audit/UI results, known
   limitations and follow-ups. Publish evidence in the body or a comment using
   ordinary `gh` commands from the deliberately chosen repository workdir.
4. **Drive CI and reviews green** as lead or with a delegated `pr-shepherd`.
   Reproduce failures locally and repair within the bounded loop. After changes, rerun affected checks,
   independent audit and journeys, push, and update the exact-head evidence.
5. **Only once the full current-head target matrix is green and reviews are
   settled**, honor the requested final epic review hold: set `Ready for Human
   Review`, return the green exact-head evidence for the human, and do not merge
   or arm final auto-merge until the human explicitly lifts that hold. When no hold
   applies, follow target-authorized delivery (Keiko ADR-0135 native auto-merge);
   otherwise retain the generic final human-review default.
6. **Closure evidence — capture the post-merge baseline.** After the authorized
   merge of the epic into `dev`, the epic is only truly closed out when `dev` is green **at the new
   HEAD** under the applicable integration contract (including canonical ADR-0178
   reuse, never a skipped PR matrix): record the **post-merge branch analysis**
   (e.g. the `dev` Sonar branch run and any other required post-merge check) as closure evidence on the epic. A merged
   epic whose post-merge `dev` run is red is **merged but not closed out** — track the
   failing check as follow-up, don't mark the epic done on a red post-merge baseline.

## Escalate (stop, report)

Escalate missing or contradictory acceptance criteria, unresolved product or
architecture decisions, authority conflicts, material scope expansion, overlapping
write ownership, prohibited sensitive artifacts, or exhaustion of 3 materially
distinct repair attempts. Accepted in-scope security, public-API, and migration work
proceeds with the target-required audits and Quality Plan; its category alone does
not require another approval. Confirmed unsafe findings block delivery until
repaired and re-audited; escalate when safe resolution needs a missing decision,
additional authority, or exceeds the bounded recovery attempts.

## Final report

Terminal state (`ready-for-human-review` / `completed` / `escalated`) · child matrix (issue,
status, branch, PR, merge commit, verification) · epic branch + final PR + base +
latest `dev` sync · parallelism used + why safe · files by area · verification ·
board state · residual risks/follow-ups.
