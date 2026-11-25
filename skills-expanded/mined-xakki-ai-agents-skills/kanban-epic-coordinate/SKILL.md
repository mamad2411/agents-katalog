---
name: kanban-epic-coordinate
description: 'Plan, govern and deliver one approved Kanban epic: scoped execution, dependencies, pauses, review, integration and authorized handoff. Use for an existing multi-card epic or ready task group. RU: эпик, выполнить эпик.'
---

# Kanban epic coordination

Use for one approved Kanban epic or ready task group: planning, governance, scoped delegation, review, integration and authorized handoff. Delegation follows the superpowers `subagent-driven-development` skill.

## Epic lead

Coordinate one approved epic and its approved children. Resolve the active
board, its lifecycle and required project instructions before action; consult
[Kanban](../kanban-card-run/SKILL.md) and [Git workflow](../git-repo-run/SKILL.md). When the separate team-lead skill is needed, ask the user to invoke `kanban-queue-coordinate` manually. Their examples do not
supersede the user's scope, repository rules or runtime capabilities.

Record the epic identity, approved children, dependencies, acceptance criteria,
baseline and relevant risks. Do not start a later EPIC or expand scope without
authorization. Preserve unrelated changes and staged content; establish a clean
baseline only when the applicable project workflow requires one, without
resetting, stashing or discarding others' work.

For each finalization action, accept explicit user approval at hand-off,
recorded EPIC-scoped upfront autonomous authorization, other recorded upfront
task/workflow authorization, or recorded profile/agent authorization only if
applicable policy accepts it and it covers the exact target and action. Record
its source and scope. A grant for one action does not imply another, scope
expansion, or a tests/review bypass. Do not request another user confirmation
when a valid grant already applies. If the user or project requires explicit
confirmation for `done`, obtain it for that action.

### Prepare and execute

1. Resolve the actual project branch and board policy. Record the base identity;
   create or select an epic branch only when the task or project requires it.
   Do not assume a branch name, model, trailer or global clean worktree.
2. Map child dependencies, permitted paths, ownership, acceptance gates and
   integration boundaries. Parallelize only when authorized, dependencies allow
   it, and concurrent writes can be isolated or coordinated.
3. Delegate bounded work when the user, runtime and applicable policy require or
   support it. Use the available delegation interface and inherited defaults;
   select models or profiles only when explicitly required. If a required role
   is unavailable, report the blocker rather than silently substituting one.
   Otherwise, perform authorized implementation directly when appropriate.
4. Follow the actual lifecycle and QA requirements. Make or request independent
   read-only review when required or useful and available; report if a required
   review cannot be obtained. Repair confirmed in-scope findings with bounded
   retries and re-run affected evidence; stop if a required gate fails or a
   decision or scope change is needed.
5. Record concise results, relevant authorizations, review/gate evidence and
   verified commit identities where applicable. Keep prompts, credentials and
   secret-bearing output out of cards and logs. Follow project commit-message
   and trailer policy; never add evidence as Git trailers by default.

### Integrate and finalize

Integrate only the approved children and verify their real combined behavior,
including the full project quality gate when required by the applicable
workflow. A ready checkpoint does not itself authorize a final action. Perform
`done`, merge, push and deploy only with each action's valid authorization and
all applicable gates; where parent-before-child is required, preserve that
order. If a required grant, review or check is absent, retain the current state
and report the exact blocker.

Apply branch merge, archive or deletion only when the actual project policy and
the corresponding authorization permit it. Verify each authorized Git result
and preserve unrelated work. For an authorized push or deploy, read back the
exact target when the workflow requires it and report what was actually
observed. A local pass is not proof of publication or deployment. Hand off the
card states, changes, evidence, pending risks and any deferred actions.

## Epic planning and execution governance

Use for planning or delivering an existing multi-card epic. Establish the canonical parent and authorized project before broad discovery; a branch name alone does not prove epic identity.

Inventory every declared child against the actual board, including available untracked records. Distinguish parent and external dependencies from children, identify duplicate or historical cards, calculate stage counts, and distinguish lifecycle from acceptance. Compare old blockers with current source and recorded owner decisions; preserve accepted unchanged evidence without treating an unverified gate as passed.

Plan only the remaining executable scope. Split genuinely independent work at ownership and dependency boundaries, record security or live-data operations as controlled scope, and keep project-specific release rules in the project. Preserve canonical child IDs and historical provenance when regrouping; verify allocator and move behavior, including symlinks and previously allocated counters, before invoking them. Never advance grooming with unresolved questions or gates. A planning request does not authorize implementation, card moves, commits, or production actions.

During authorized execution, preserve the owner's decision sequence, selected roles, source revisions, and mandatory stage-entry gates. Avoid overlapping writers; include relevant untracked work in the complete candidate and obtain independent review where required. Reconcile a later owner decision with affected cards while preserving its narrower scope and historical rationale. A running process remains pending after an observation timeout: retain its handle and do not start a duplicate executor or gate. Distinguish runtime limits from explicit owner-limited operations, and continue authorized unfinished work without inventing a new quota. A native security refusal is a stop for the denied operation, never a reason to bypass it.

Before each stage move, reconcile its criteria, approval, existing status fields and evidence, then validate the actual card and checked count. If broad gates and review are explicitly deferred, keep each child at the last stage whose entry rules are satisfied, run required focused checks, and complete the deferred combined gates and review at the agreed point. Mark omitted checks NOT_RUN; an omission is not a pass or waiver. Do not start a reviewer while assigned source edits or mandatory gates remain incomplete. Qualify each executor's completed phase against its actual deliverable, not merely its exit or final wording.

Keep provider acceptance separate from downstream consumer integration and preserve genuinely independent prework as such. Classify review blockers as defects, missing evidence, scope ambiguity or a later Git/lifecycle predicate; fix or clarify the actual blocker, preserve earlier receipts, and rerun only affected required checks. Route out-of-scope findings to existing work with owner approval before changing another card. Distinguish commit, merge, push, deploy and data-operation authority. For `done`, honor the applicable policy and any valid authorization already recorded for that exact action.

Report every declared child, actual stage, ordered remaining work, prerequisite, checked versus unrun evidence, and parent-level acceptance. All children being `ready` does not itself prove parent completion, production readiness, or permission to perform `done` or release actions.

Use [interrupted child recovery](references/interrupted-child-recovery.md) when resuming incomplete execution, and [epic finalization](references/epic-finalization.md) only for an authorized coordinated completion.

For cross-repository handoffs, card transitions and evidence carried across
revisions, use [cross-repository evidence](references/cross-repository-evidence.md). For paused work,
workspace continuity and scoped evidence, use [continuity and evidence](references/continuity-and-evidence.md).

## Epic scope decisions, pauses and reductions

Use when an epic needs a durable scope decision, a dependency pause, or an authorized reduction in scope. Read the complete parent and affected children first; preserve existing history and unrelated work.

Record a concise current decision digest with the epic and ordered child IDs, pinned predecessors when relevant, acceptance gates, authorized actions and limits, current baseline, parked risks, and an explicit paused state when a dependency blocks execution. Verify actual repository or service state instead of treating card prose as proof. Mark superseded statements at their original location so the active plan is not contradictory.

When the owner approves reducing scope, distinguish remaining children from deferred standalone work; keep their criteria and dependencies. Reconcile the parent sequence and references, and use the supported board operations only for authorized card changes. A smaller scope does not accept an unfinished child or authorize parent closure.

Before moving excluded cards, verify standalone IDs are unique across the board, retain old epic IDs as historical provenance, and preserve their criteria and decisions. Update the parent's active child list, execution order, dependencies and completion criteria together. Do not start or move children while a blocking predecessor is unresolved.

Validate every changed record with the canonical board checker where available, inspect exact changes and any scoped review, and report unavailable checks. If a commit is authorized, stage only the explicit intended records, including both sides of a rename, and verify committed paths and post-commit status. Follow the task's Git and authorization policy rather than inventing a branch, trailer, commit, or publication requirement. Report the current scope, deferred children, gate results and precise remaining parent blocker.

See [pause digest](references/epic-pause-digest-session.md), [preparation staging](references/epic-preparation-staging.md), and [parent start verification](references/parent-start-verification.md) for supported steps.

## Autonomous epic delivery

Use for owner-authorized execution of an epic or ready task group. Establish the exact execution and lifecycle limits, including any user approval required for `done`, before starting.

1. Read the complete candidates, dependencies, existing epics, and current source contracts. Classify each as ready, blocked, or carrying a hidden risk; a `todo` stage alone is not readiness. Organizational, historical, and reference cards are not implementation nodes.
2. Give the owner a concise plan covering task areas, dependency order, exclusions, verification, and any Git actions. Create or modify board records only within the approval already granted.
3. Delegate only when authorized and the required role or profile is available. Partition work by ownership and avoid parallel edits to shared files or contracts. Preserve explicit sequencing, profile, review, and commit requirements from the task rather than inventing an agent name or trailer.
4. Run the applicable checks and required independent review of the complete diff and call sites. For shell, CLI, or build targets with user-controlled values, test argument boundaries with hostile synthetic inputs, ensure they are passed as data rather than interpolated shell source, and verify command failures propagate nonzero even through later formatting. Repair confirmed in-scope findings in a separate corrective change when the project requires it, rerun affected checks, and repeat independent review to confirm previous blockers are resolved.
5. Follow the actual board lifecycle and acceptance gates. Keep the epic active until its required children are ready. Do not treat a child handoff as parent completion, or static evidence as proof of a live effect. Move to `done` only with the authorization required by the applicable policy; merge, push, deploy, and destructive actions require their own applicable authorization. Keep independently owned implementation and lifecycle changes separate, and never include another actor's staged changes in a commit.
6. Report actual checks, known blockers, current active work, uncommitted changes, and the next actionable node. Map unrelated findings to existing work before suggesting a new card, and honor any requirement for owner approval before editing it.

See [readiness and review](references/readiness-and-review.md) for audit and verification details and [artifact audit](references/thin-client-artifact-audit.md) when reducing a client or provider capability.
