---
name: repo-delivery
description: "Use when authorized Git mutation must preserve a large task through semantic milestone, targeted fixup, or exceptional checkpoint commits, normalize task-branch history, or deliver reviewed changes through commit, push, integration, cleanup, or ref proof; stops before pull-request creation."
---

# Repository Delivery

## Overview

Own two separately authorized Git lifecycles: **Execution Durability** preserves large-task progress on a task branch through semantic milestones, targeted fixups, and exceptional safety checkpoints; **Final Delivery** normalizes the completed branch when requested, fixes the final review basis, and performs reviewed commits, pushes, integration, or cleanup. Execution commits preserve work but never imply final review, merge readiness, or remote durability. Verify branch policy, sharing/rewrite safety, permissions, commit grouping, and staged content before mutation; never open a pull request.

## Workflow

1. Read effective repository guidance first, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
2. Run `git status --short --branch` and identify branch, upstream, staged files, dirty files, and unrelated local work.
3. Select **Execution Durability** or **Final Delivery** from the requested outcome. Implementation-only wording never authorizes either lifecycle.
4. Inspect existing local refs. Fetch or otherwise refresh remote state only for an explicitly authorized push, sync, branch-integration, history-rewrite assessment, or remote-refresh target; a local-commit-only request leaves remote state `Not verified`.
5. Confirm each target through either exact per-action authorization or a bounded task-level execution-durability plan. A standing plan records the task branch, owned scope, allowed milestone/fixup/checkpoint types, event triggers, validation floor, message policy, and push policy; matching commits may proceed without asking again. Scope expansion, a new commit type, failed safety gates, rewrite, push, integration, or cleanup requires fresh authority.
6. Confirm branch policy and permissions: task/default/protected status, upstream and known sharing/review state, force-push restrictions, required checks, branch naming, and every unknown that changes safety.
7. For **Execution Durability**, require exact per-action authority or a still-valid bounded task plan plus an exact separable scope. Classify it as a completed semantic milestone, a correction owned by one reachable milestone, or an exceptional checkpoint permitted by the plan before a concrete loss/recovery risk. Reuse implementation evidence, run focused validation when possible, stage only exact paths/hunks, inspect the complete cached diff, commit, then report remaining and unrelated Worktree content. Continue under the same plan only while its branch, scope, triggers, and safety gates still match; push remains separately authorized.
8. For ordinary reviewed local commits, ensure the accepted review basis and ownership are clear, then classify every approved path or hunk by semantic intent and dependency order. Default to one commit per independent category. Use one commit only when explicitly requested or the complete scope is one indivisible intent. Inspect cached stat, name-status, and full diff before each commit.
9. For **Final History Normalization**, require completed implementation, exact rewrite authorization, and either a clean task worktree or an isolated worktree with every remaining staged/unstaged/untracked item fingerprinted outside the rewrite basis. Record the source range, before HEAD/tree, and recoverable pre-rewrite SHA; do not rewrite a default, protected, shared, or active-review branch when safe ownership is not proven. After normalization, require the expected tree and scope to match, freeze the new immutable basis, and obtain final fixed-basis review evidence. Any later history or tree change invalidates that evidence.
10. For branch integration, fix the source range and target tip before choosing the history shape. Preserve coherent, reviewed, meaningful commits when their order and boundaries remain useful; squash noisy, fixup-heavy, checkpoint-bearing, or single-outcome history when policy or explicit intent calls for one commit. Selecting only some source commits requires explicit partial-integration scope and proof that omitted content is intentional.
11. For push, sync, cleanup, or conflict resolution, execute only that target's authorized mutations. Conflict authorization separately covers file resolution, staging, merge/rebase continuation or commit, and push; an omitted action remains forbidden.
12. Verify the requested final local and remote state with branch, status, log, tree, remaining Worktree content, and remote ref evidence. A local-only durability commit reports remote protection as absent, not implied.

## Modes

- **Categorized local commits:** classify reviewed changes and create one commit per independent intent without pushing.
- **Explicit single commit:** create exactly one commit only when requested or when the reviewed scope has one indivisible intent.
- **Semantic milestone:** preserve one completed, separable, focused-validated task slice on a non-default task branch; mark it `slice-validated`, not final-reviewed.
- **Targeted fixup:** commit a correction that belongs to exactly one reachable milestone and mark its normalization target; use a normal semantic correction when that ownership is not singular or rewrite is not planned.
- **Safety checkpoint (exceptional):** preserve incomplete task-owned work only before a concrete loss/recovery risk; record why it exists and require split, absorption, or removal before final integration.
- **Final history normalization:** with exact rewrite authorization, normalize completed task-branch history while preserving the expected tree, then freeze a new final review basis.
- **Current-branch push:** push the already reviewed current branch after upstream/divergence checks; do not stage or commit unless separately authorized.
- **Review publication:** after local review and validation, create and/or push the explicitly authorized fixed commit on a GitHub-backed non-default, non-protected branch so an external reviewer can use repository URL, branch, and SHA. Stop before PR creation or target-branch integration.
- **Branch sync:** pull, fetch, rebase, merge, or fast-forward only according to repo guidance, current divergence, and the user's requested target.
- **Branch integration:** integrate a fixed reviewed source range into the target by preserving coherent semantic commits or squashing noisy/single-outcome history according to explicit intent, repository policy, and evidence.
- **Squash-to-main:** a conditional branch-integration strategy that moves reviewed branch work into `main` as exactly one final commit only when repo guidance and explicit user intent permit direct `main` updates.
- **Cleanup:** delete local or remote temporary branches only after final target state is verified and cleanup is requested or required by repo guidance.
- **Conflict resolution (conditional):** resolve an authorized in-progress merge/rebase hunk by hunk from both sides' primary intent. Treat resolution writes, staging, continuation/commit, and push as separate permissions.

## Do Not Use For

- First-pass repository discovery, real commands, or docs alignment; use `repo-map`.
- Future implementation planning or subagent task splitting; use the host's built-in planning.
- Implementation or validation requests that do not explicitly authorize a local commit or other Git mutation; use the implementation owner and leave Git unchanged.
- Existing local diff review, ownership classification, mixed-hunk analysis, or commit grouping before delivery scope is clear; use `repo-review`.
- Review-only requests that do not authorize Git mutation; use `repo-review`.
- Review of a fixed change basis, including authorization or token risks; use `repo-review`.
- Browser or desktop-client runtime evidence; use `ops-browser` or `ops-client`.
- Branch publishing that explicitly includes creating a draft or ready pull request; use the available GitHub publishing workflow.

## Hard Rules

- Do not make ordinary task changes directly on protected or default branches when repo guidance forbids it.
- Do not infer staging or commit authorization from a review-only request.
- Do not infer milestone, fixup, or checkpoint authorization merely from a large, long-running, or risky implementation request. Git preservation may use exact per-action authority or one explicit bounded task-level plan; do not ask again for commits already covered by that plan.
- Do not infer push, sync, branch-integration, cleanup, conflict-resolution, or branch-deletion authorization from a local commit request.
- Do not infer that `main` is writable merely because local checkout permits a commit.
- Review publication requires explicit commit and push authorization, a verified GitHub remote, a non-default and non-protected current branch, a fixed locally reviewed basis, and remote-ref proof. If any condition is absent, return the necessary files or review package to the caller instead of publishing.
- Do not stage unrelated local changes.
- Do not use `git add .`, `git add -A`, directory-wide adds, or wildcard adds unless the user explicitly approves that exact scope.
- Do not commit when unrelated staged files are present.
- Do not collapse multiple independent categories into one commit unless the user explicitly requests one commit.
- Do not split one indivisible contract change merely to increase commit count.
- Do not rewrite, force-push, squash, delete branches, change remotes, or alter upstream tracking unless the user requested it or repo guidance requires it for the delivery target.
- Never treat a milestone, fixup, or checkpoint as final review, merge readiness, release evidence, or remote backup.
- Do not create time-based or automatic WIP commits. Prefer a semantic milestone; use a checkpoint only for a named loss/recovery risk and never on a default or protected branch.
- A standing execution-durability plan is authorization, not automation: trigger only on verified semantic events inside its branch and owned scope. Stop and refresh authority when scope, branch, commit type, validation floor, or risk materially changes.
- Every checkpoint must identify incomplete scope and a final disposition of split, absorb, or drop. Do not carry checkpoint-only history into final integration by accident.
- Do not bind one fixup to multiple independent milestones or use fixup syntax when no later normalization is intended.
- Before history normalization, require a clean task worktree or isolate and fingerprint all remaining content. A tree SHA does not cover untracked or unrelated dirty files.
- Record before and after tree SHAs and compare the complete expected task scope after normalization. Stop on any unexplained mismatch.
- Do not rewrite a default, protected, shared, remotely consumed, or active-review branch unless exact ownership, rewrite, and remote-update authority are proven. Prefer merge-time squash or a clean integration branch when sharing is unknown.
- Final review evidence applies only to the normalized immutable basis. Any later history or tree change requires a new fixed basis and review.
- Never use review publication to update `main`, another default/protected branch, create a pull request, force-push, or imply external reviewer approval.
- Never use force push as an automatic response to non-fast-forward rejection. Re-read remote state and report the divergence first.
- Do not rebase or merge over a dirty worktree without an explicit safe plan for local changes.
- Preserve user-provided commit text verbatim.
- Prefer exact path or hunk staging; verify the staged diff before every commit.
- Keep one commit to one logical intent; do not mix a second category merely because it is already modified.
- Do not choose squash merely because it is convenient. Record why preserved commits or a squash best represents the reviewed source range.
- Do not preserve WIP, fixup, conflict-only, or validation-repair commits as important history when they can be safely folded into their owning intent.
- Do not cherry-pick a subset of another branch unless partial integration is explicit and every omitted commit is accounted for.
- Verify remote success from the updated ref or commit SHA, not only from a successful command exit.
- If remote state changed after review or validation, stop and reassess before pushing or updating a target branch.
- Say `Not verified` when validation, branch protection, permissions, remote refs, CI, deployed state, or branch cleanup were not checked.
- Do not create or update pull requests; this workflow stops after the requested Git ref and cleanup state are verified.

## Output Contract

Return a compact Delivery Report with `Completed`, `Changed Files`, `Verification`, `Known Issues`, `Next Steps`, and `Git Status`. Include lifecycle and mode, per-action or bounded-plan authorization basis, delivery target, branch/upstream, branch policy, ahead/behind/diverged state, dirty-tree risks, semantic categories and dependency order, each staged scope and commit hash, validation and review state, local-only versus pushed durability, remaining uncommitted content, required checkpoint/fixup disposition, before/after tree proof for normalization, branch-integration strategy and rationale, authorized Git actions, final local and remote ref evidence, rejected unsafe operations, and every `Not verified` item. Reference existing artifacts instead of duplicating them; redact secrets and unrelated personal data.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and mode examples.
- See [references/execution-durability.md](references/execution-durability.md) for milestone, fixup, and exceptional checkpoint gates.
- See [references/history-normalization.md](references/history-normalization.md) for rewrite safety, tree proof, and final-basis review.
- See [references/checklist.md](references/checklist.md) for delivery and verification details.
- See [references/delivery-report.md](references/delivery-report.md) for the compact handoff/report template.
- See [references/resolving-merge-conflicts.md](references/resolving-merge-conflicts.md) only for an authorized in-progress merge/rebase conflict.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
