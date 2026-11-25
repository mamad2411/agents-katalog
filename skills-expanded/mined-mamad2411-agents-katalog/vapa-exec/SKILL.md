---
name: vapa-exec
description: Use when handed a VAPA issue link and asked to implement, plan, fix, or refine an approved proposal. Orchestrates artifact-driven execution using a project-local .vapa workspace, with multi-agent execution preferred, a decomposition protocol for large tasks, architecture rigor gates before coding, and visual verification requirements for frontend work.
---

# VAPA Issue Execution

## Overview

`vapa-exec` turns an approved VAPA proposal into a traceable implementation. It is an execution orchestrator, not merely a coding shortcut.

The skill must preserve the reasoning trail in a project-local workspace:

```text
.vapa/vapa-exec-<issue-id>/workspace/
```

This workspace is intended to be committed with the implementation when it contains no secrets or private data. It lets the team inspect how the Agent understood the proposal, planned the work, executed it, tested it, and prepared it for audit.

## When to Use

- A user pastes a VAPA issue URL and asks to implement, plan, fix, or refine it.
- The issue body or comments include proposal context, design notes, implementation constraints, screenshots, or acceptance criteria.
- The user asks for Agent execution after a proposal has been approved or explicitly authorizes execution.

If the user asks only to create or improve a proposal, use `vapa-proposal` instead. If implementation is complete and the user asks whether it is ready for PR or validation, use `vapa-audit`.

## Core Principle

Agent execution should be multi-agent by default, artifact-driven always, and single-session only as a fallback for small tasks.

```text
approved
  -> readiness-check
  -> context-ready
  -> plan-ready
  -> implemented
  -> tested
  -> audited
  -> ready-for-pr | needs-revision | blocked-for-human
```

The current state must always be recoverable from the workspace alone. Any session — including a fresh one after an interruption — must be able to read `state.json` and the artifacts, and continue from the recorded phase without re-deriving context from memory.

## Required Workspace

Ensure a workspace exists at:

```text
.vapa/vapa-exec-<issue-id>/workspace/
```

Create it if missing. If `vapa-design` ran first, the workspace already exists
with a `design/` archive of the confirmed design comments — reuse it and never
wipe or restart it.

Use the GitHub issue number as `<issue-id>` when available. If the source is not GitHub, use a stable slug such as `<host>-<project>-<id>`.

Required structure:

```text
.vapa/vapa-exec-<issue-id>/workspace/
  state.json            # machine-readable phase tracker (see below)
  issue.json            # raw issue snapshot
  comments/             # one file per comment, chronological
  images/               # referenced screenshots and design assets
  issue-brief.md
  source-map.md
  readiness-report.md
  codebase-survey.md    # architecture baseline before planning
  VAPA_EXEC_PLAN.md
  VAPA_EXEC_LOG.md
  TEST_REPORT.md
  evidence/             # screenshots, recordings, command output captures
  PR_DRAFT.md
```

Conditional artifacts:

- `ui-spec.md` — required whenever the change touches user-facing UI (see Frontend Execution Requirements).
- `decomposition.md` — required whenever the task is executed as decomposed sub-issues (see Decomposition Protocol).
- `design/` — present when `vapa-design` ran before execution: the archived bodies of the confirmed design comments. The issue comments remain the canonical record; treat this directory as read-only input for the brief and plan.

`VAPA_AUDIT.md` is produced by `vapa-audit` after implementation and tests are complete.

### state.json

Keep a small machine-readable tracker so execution can be resumed and orchestrated:

```json
{
  "issue": "42",
  "size": "S",
  "domain": "frontend | backend | mixed | docs",
  "phase": "readiness-check | context-ready | plan-ready | implemented | tested | audited",
  "branch": "vapa/42-batch-export",
  "revision_count": 0,
  "updated_at": "YYYY-MM-DDTHH:mm:ssZ"
}
```

Update `state.json` at every phase transition. If a session starts and `state.json` already exists, resume from the recorded phase instead of restarting; verify the recorded branch and the latest artifacts before continuing. If the workspace exists but has no `state.json` — typically because `vapa-design` created it to archive confirmed designs — start a fresh execution and treat the existing `design/` archive as input, not as prior execution state.

For decomposed tasks (see Decomposition Protocol), the parent workspace extends the schema:

```json
{
  "issue": "42",
  "mode": "decomposed",
  "sub_issues": {
    "43": {"workspace": ".vapa/vapa-exec-43/", "phase": "audited", "audit": "READY_TO_INTEGRATE", "depends_on": ["41"]},
    "44": {"workspace": ".vapa/vapa-exec-44/", "phase": "implemented", "audit": null, "depends_on": []}
  },
  "integration_phase": "pending | integrating | tested",
  "defect_fix_rounds": 0
}
```

A sub-issue workspace adds `"parent": "42"` to its own `state.json`.

State reconciliation: when `vapa-exec` starts on a parent issue, rebuild the aggregate view from the tracker linkage and each sub-workspace's `state.json` rather than trusting the parent's copy — sub-issues may have been executed individually since the parent state was last written. If they disagree, the sub-workspace records win; correct the parent `state.json` and record the reconciliation in `VAPA_EXEC_LOG.md`.

## Execution Flow

### Step 0: Classify the Task

Before anything else, classify along three axes and record the result in `state.json`:

- **Size**: from the issue's `Size` field, or estimate if absent. This selects the execution mode (see Decomposition Protocol).
- **Domain**: frontend, backend, mixed, or docs. Frontend or mixed tasks trigger the Frontend Execution Requirements.
- **Risk**: does the change touch data models, public APIs, auth, payments, or shared infrastructure? High-risk changes require the extended design section in the plan.

### Step 1: Fetch the Source of Truth

1. Fetch the raw issue with metadata, labels, body, comments, and author information.
   - Prefer `gh issue view --json` for GitHub issues.
   - Preserve a raw snapshot as `issue.json`.
2. Save each comment separately under `comments/`, numbered in chronological order.
3. Download referenced images into `images/` when permitted.
4. Record every source in `source-map.md`, including issue body, comments, images, linked documents, and important code references.

Do not rely on memory or remote-only context after this step.

### Step 2: Run the Readiness Gate

Before implementation, write `readiness-report.md` and decide whether execution may proceed.

Required checks:

- Issue is `status: approved`, or it is a sub-issue listed in the `decomposition.md` of an approved parent issue (the parent's approval covers it), or the user explicitly authorizes execution.
- Defect-fix round: when re-entering an issue whose execution previously concluded because of new defect comments (see Defect Handling), enumerate the defect comments added since the last run and get the human's confirmation of the fix list before implementation.
- Agent execution readiness checklist exists in the issue body or comments, or the user explicitly accepts the missing checklist.
- Acceptance criteria are concrete enough to test or manually verify.
- Boundaries are stated: what must not change, compatibility requirements, and out-of-scope work.
- Required context is available: relevant code, APIs, data structures, designs, or linked documents.
- For UI work: design references (screenshots, mockups, or an explicit "follow existing design system" instruction) exist, or the gap is recorded as a human decision point.
- `Size: M` or larger proposals are split into `Size: S` sub-issues, or the reason for continuing is explicitly documented.
- No new information invalidates the proposal's core assumptions.
- Design comments: if the task has a non-trivial design surface but no `vapa-design` confirmed design comments exist on the issue, recommend running `vapa-design` first. This is advisory, not blocking.
- The working tree is clean and based on the latest default branch, or the divergence is recorded.

If any blocking item fails, stop implementation. Produce `readiness-report.md` with `Verdict: BLOCKED` and ask for the missing human decision.

### Step 3: Synthesize the Brief

Write `issue-brief.md` with these sections:

- Background and problem
- Approved scope
- Explicit non-goals
- Acceptance criteria
- Design requirements
- Implementation requirements
- Open questions
- Human decisions already made

Every non-obvious claim should point back to `source-map.md`.

Verbatim rule: acceptance criteria, boundary constraints, and "this is not" exclusions must be quoted word-for-word from the issue or comments, each with its source reference. Paraphrasing these three categories is forbidden — the brief may add interpretation next to a quote, but never replace it. These quotes are the contract that planning, implementation, testing, and audit all trace back to.

Confirmed design comments (`<!-- vapa-design: ... status=confirmed -->` markers) are part of that contract: they belong in "Human decisions already made", are quoted verbatim like acceptance criteria, and the plan may not contradict them. When several versions of the same design item exist, the highest `v=` wins.

Coverage self-check: the brief is a lossy summary of `issue.json` and `comments/`, so after writing it, re-read the raw sources and verify the reverse direction — every substantive requirement, constraint, and later-comment amendment either appears in the brief or is explicitly listed in a "Deliberately excluded" note with the reason. `source-map.md` guarantees that brief claims are traceable to sources; this check guarantees that sources are not silently dropped from the brief.

### Step 4: Survey the Codebase

Before planning, write `codebase-survey.md`. Planning without this survey produces plans that fight the existing architecture.

Required content:

- **Impact area**: modules, packages, and files the change will plausibly touch, and their current responsibilities.
- **Existing patterns**: how the codebase already solves similar problems — naming conventions, layering, error handling style, state management, test structure. New code must follow the closest existing analog unless the plan explicitly justifies deviating.
- **Reusable assets**: existing components, utilities, services, or design tokens the implementation should reuse instead of recreating.
- **Contracts at the boundary**: public APIs, database schemas, events, or shared types the change touches, and who else depends on them.
- **Constraints discovered**: build tooling, lint rules, minimum runtime versions, CI checks that the implementation must pass.

For frontend work, additionally inventory the design system: component library, theme/token files, and the closest existing screens to imitate.

### Step 5: Plan

Write `VAPA_EXEC_PLAN.md` before editing code.

Before planning, spot-check the brief against the raw sources: re-read `issue.json` and at least the most recent comments in `comments/`. The brief is the working input, not the source of truth — if it conflicts with or omits something in the raw issue, the raw issue wins; fix the brief (append a dated correction, per the no-rewrite rule) before writing the plan. This matters most when the Planner is a different agent or session than the one that wrote the brief.

Required sections:

- Objective
- Non-goals
- Acceptance criteria mapping
- Design
  - Interfaces and contracts: function/API signatures, component props, events, or schema changes, defined before implementation.
  - Data: model changes, migrations, and backward compatibility for existing data.
  - Error handling and edge cases at system boundaries.
  - Key decisions: for each non-obvious choice, the selected option, at least one rejected alternative, and why. High-risk tasks (per Step 0) must also cover security, performance, and rollout implications.
  - New dependencies: any new library or service requires explicit justification and is a human decision point unless the proposal already approved it.
- Files and modules likely to change
- Implementation steps, ordered so the code builds and tests pass after each step
- Test strategy and commands
- Risks and rollback plan
- Human decision points

For UI work, the plan must reference `ui-spec.md` (see Frontend Execution Requirements) and map acceptance criteria to concrete screens and states.

For `Size: S`, a single session may plan and implement inline. For `Size: M`, prefer separate Planner, Implementation, and Audit roles. For `Size: L` or `XL`, follow the Decomposition Protocol.

### Step 6: Implement

Implement according to the plan. Keep changes scoped to the approved proposal.

Git discipline:

- One issue, one branch: work on a dedicated branch named `vapa/<issue-id>-<slug>` unless the repository has its own convention. Sub-issues of a decomposed task do not get their own branches — their work lands on the parent's branch (see Decomposition Protocol).
- Parallel sub-issue work happens in separate worktrees; the orchestrator merges a sub-issue's work back into the parent branch with commits referencing the sub-issue number, and only after the sub-issue's audit returns `READY_TO_INTEGRATE`. Sub-agents never write to the parent branch directly.
- Commit in coherent, buildable increments that follow the plan's implementation steps. Reference the issue number in commit messages.
- Commit workspace artifact updates together with the implementation steps they describe.

Maintain `VAPA_EXEC_LOG.md` with:

- Files changed
- Steps completed, with commit references
- Deviations from plan and why
- Key Agent-made judgments
- Human confirmations or blockers
- Follow-up items deferred out of scope

Handle deviations by severity:

1. **In-plan judgment** (naming, minor structure): decide, log it.
2. **Plan deviation within scope** (different file layout, extra step discovered): log it, append a dated revision note to `VAPA_EXEC_PLAN.md`, continue.
3. **Broken assumption** (the proposal's premise is wrong, the approved approach cannot work, scope must grow): stop, set the log entry, and request a human decision. Never silently change direction or expand scope.

For long-running work, checkpoint at least at every completed implementation step: update `state.json`, `VAPA_EXEC_LOG.md`, and commit, so an interrupted session loses at most one step.

### Step 7: Test

Run the relevant checks and write `TEST_REPORT.md`.

Include:

- Commands run, with actual output captured in `evidence/`
- Pass/fail results
- Manual verification performed
- Acceptance criteria coverage — every criterion must map to a test, a manual check, or an explicitly recorded gap
- Regression check: existing test suite and lint/build for the impacted area still pass
- Known gaps or tests not run, with reasons

For UI work, testing additionally requires visual evidence — see Frontend Execution Requirements.

If tests fail because of the implementation, return to Step 6. If tests fail because the proposal needs a decision, stop and record the blocker.

### Step 8: Prepare PR Draft

Write `PR_DRAFT.md` with:

- Suggested PR title (`[#<issue>] verb + object`)
- Linked issue
- Implementation summary
- Acceptance criteria mapping
- Test evidence, including visual evidence for UI changes
- Known limitations
- VAPA workspace path
- Suggested contribution records

For decomposed tasks, organize the implementation summary and acceptance criteria mapping by sub-issue, so human reviewers can review the PR segment by segment.

Do not claim the work is ready for PR until `vapa-audit` returns `READY_FOR_PR`.

## Decomposition Protocol

Size selects the execution mode:

| Size | Mode |
|---|---|
| S | Single session allowed; all artifacts still required |
| M | Multi-agent roles preferred; decomposition into S sub-issues strongly preferred |
| L | Must be decomposed into `Size: S` sub-issues before implementation |
| XL | Must return to the Proposal/Review layer for re-scoping; never execute directly |

### Decomposition rules

1. **Single level only.** Decomposition depth is 1. If a sub-issue turns out to be too large during execution, stop and report `BLOCKED_FOR_HUMAN_DECISION`. Never decompose a sub-issue further on your own.
2. **Human confirmation before issue creation.** Write `decomposition.md` in the parent workspace (template: `${CLAUDE_SKILL_DIR}/references/decomposition.md`) — the sub-issue list with dependency edges, what each delivers, and the integration criteria that define "the parent issue is done" — and present the split to the human for approval before creating tracker sub-issues. Record the approval and the creation in `VAPA_EXEC_LOG.md`.
3. **Tracker linkage.** On GitHub, create sub-issues with the native sub-issue feature so the tracker records the parent-child relationship automatically. On other platforms, fall back to a task list in the parent issue body plus a first-line parent reference in each sub-issue body. Record the linkage method in `decomposition.md`. The workspace remains the source of truth for execution; tracker linkage is the visibility layer.
4. **Approval coverage, with a guardrail.** The parent issue's approval covers the sub-issues listed in `decomposition.md`. Discovering a need for a sub-issue outside that list is a scope change and requires a human decision.
5. **One branch per parent issue.** All sub-issue work lands on the parent's branch `vapa/<parent-id>-<slug>`. Sub-issues that run in parallel work in separate worktrees; the orchestrator merges a sub-issue's work back into the parent branch only after its audit returns `READY_TO_INTEGRATE`. Sub-agents never write to the parent branch directly.
6. **Dual entry.** `vapa-exec` accepts either a parent issue URL — orchestration mode: reconcile state, schedule sub-issues by DAG waves, integrate, prepare for the parent audit — or a sub-issue URL — single mode: execute only that sub-issue, but first read the parent workspace's `decomposition.md` and the parent plan's cross-cutting contracts. If the parent workspace is missing locally in single mode, direct the user to run `vapa-exec` on the parent first.
7. **Single writer for parent artifacts.** Only the orchestrator writes the parent `state.json` and the parent issue's roll-up comments. Sub-agents write only their own workspace and their own issue's comments.

### DAG scheduling

Record dependencies explicitly in `decomposition.md`, per sub-issue:

```markdown
### Sub-issue #43: <title>
- delivers: <what it delivers>
- depends_on: [#41]        # logical dependency: #41's output is #43's input
- conflicts_with: [#44]    # optional physical conflict: touches the same files; serialize
```

- Validate the graph is acyclic when the human confirms `decomposition.md`.
- Schedule in topological waves: sub-issues with no unmet dependencies form the current wave and may run in parallel, one worktree each. When the whole wave is merged back, the next wave unlocks. A sub-issue with multiple dependencies waits for all of them.
- Wave N+1 worktrees are created from the parent branch only after wave N has been fully merged back, so dependencies are physically present in the code the next wave builds on.
- Distinguish `depends_on` (logical; fixed order) from `conflicts_with` (file overlap; serialized, but any order). Most file overlaps should already be dissolved by defining cross-cutting contracts in the parent plan; `conflicts_with` is the fallback.
- Blocked propagation follows the edges: when a sub-issue is blocked, its downstream sub-issues pause; its siblings continue. The parent roll-up comment states what is affected.
- The DAG lives only in the workspace (`decomposition.md` and `state.json`). Tracker sub-issue features do not express dependencies. Keep the machinery simple: a `depends_on` list, topological waves, and the environment's concurrency limit — not a general-purpose scheduler.

### Integration

1. Each sub-issue gets its own `vapa-exec` run with its own workspace (`.vapa/vapa-exec-<sub-id>/workspace/`), linking back to the parent in its `issue-brief.md` and recording `"parent"` in its `state.json`.
2. Cross-cutting contracts (shared interfaces, schemas, design tokens) are defined in the parent plan **before** sub-issue implementation starts, so parallel work does not diverge.
3. After all sub-issues reach `READY_TO_INTEGRATE` and are merged back, run an integration pass in the parent workspace: verify the sub-implementations compose, run the full test suite, and record the result in the parent `TEST_REPORT.md` before handing to audit.

Revision budget: if `vapa-audit` returns `NEEDS_REVISION` twice for the same underlying finding, or `revision_count` in `state.json` reaches 3, stop and escalate to a human instead of iterating further. In decomposed mode, each sub-workspace counts its own audit rounds and the parent workspace counts only integration-audit rounds. Repeated failed revisions are evidence of a broken assumption, not a coding problem.

## Frontend Execution Requirements

These requirements apply whenever `domain` is frontend or mixed. Backend-only tasks may skip this section.

### ui-spec.md

Before implementation, translate all design inputs (screenshots in `images/`, mockups, textual descriptions) into `ui-spec.md`:

- **Screens and components affected**, each mapped to its closest existing component or screen in the codebase (from `codebase-survey.md`). Prefer extending existing components over creating bespoke ones.
- **Layout and visual intent**: spacing, hierarchy, and alignment expectations; which design tokens (colors, typography, spacing scale) apply. Never hardcode values that exist as tokens.
- **Interaction states** for every interactive element: default, hover, focus, active, disabled, loading, empty, and error. Ambiguous states are open questions, not silent guesses — record them and either resolve from the design system's conventions or raise them as human decision points.
- **Responsive behavior**: which breakpoints are in scope and how the layout adapts. If the proposal is silent, follow the repository's existing breakpoint conventions and record that judgment.
- **Accessibility baseline**: keyboard operability and focus order, accessible names/roles for new controls, and color contrast for new visual elements.
- **Motion**: transitions or animations if specified; otherwise follow existing patterns.

### Visual verification

`TEST_REPORT.md` for UI work must include, stored under `evidence/`:

- Screenshots of every affected screen or component in its primary state, at least at one desktop and one mobile viewport when responsive behavior is in scope.
- Screenshots or notes covering the non-default interaction states that the change introduces (loading, empty, error, disabled).
- A side-by-side or explicit comparison against the design reference when one exists, noting any intentional deviations and why.
- Confirmation of keyboard navigation through new interactive flows.

Use a browser tool to capture real rendered output whenever the environment allows; if rendering is impossible in the environment, record that as an explicit verification gap for the human validator rather than skipping silently.

## Multi-Agent Roles

Use separate agents or separate sessions when the environment supports it:

| Role | Responsibility | Output |
|---|---|---|
| Orchestrator | Gatekeeping, workspace setup, phase transitions, state tracking | `readiness-report.md`, `state.json`, `decomposition.md` |
| Context Agent | Issue/comment/image/repo context capture, codebase survey | `issue-brief.md`, `source-map.md`, `codebase-survey.md` |
| Planner Agent | Design, plan, and test strategy | `VAPA_EXEC_PLAN.md`, `ui-spec.md` |
| Implementation Agent | Code changes and execution log | code, `VAPA_EXEC_LOG.md` |
| Test Agent | Verification, including visual evidence | `TEST_REPORT.md`, `evidence/` |
| PR Agent | PR draft | `PR_DRAFT.md` |

When true multi-agent execution is unavailable, simulate these roles sequentially in one session and keep the same artifacts.

## Issue Status Sync and Progress Reporting

VAPA replaces reporting with transparency; the issue must reflect execution reality:

- When implementation starts, set `status: in-progress` on the issue (or ask the user to, if the Agent lacks permission).
- Post a progress comment on the issue at meaningful transitions: execution started (with workspace path and branch), blocked (with the specific decision needed), and tested/audit-ready (with a summary and evidence pointers).
- When blocked, the issue comment is the canonical record of the blocker — not just the workspace log.
- After audit returns `READY_FOR_PR`, the issue moves toward `status: in-validation` as part of PR submission.

For decomposed tasks, sync runs in both directions:

- Every phase transition of a sub-issue produces a detailed comment on the sub-issue and a condensed roll-up comment on the parent issue, posted by the orchestrator: sub-issue id, transition outcome, and a link to the detailed comment. Reference, never copy — the sub-issue's comment is the canonical record.
- Blocked sub-issues propagate: mark the sub-issue blocked in the parent `state.json`, pause scheduling of its downstream sub-issues (per the DAG), and state the needed human decision in the parent roll-up comment.
- Defect fixes post a receipt: reply to the defect comment with the fixing commit and verification evidence, plus a roll-up comment on the parent issue (see Defect Handling).
- When all sub-issues are integrated and the parent audit concludes, post a final summary comment on the parent issue: the sub-issue verdict list, integration test results, the parent audit verdict, and the workspace path.

## Defect Handling

Defects found after an execution has concluded take different channels depending on merge state:

| Timing | Channel | Handling |
|---|---|---|
| Before the issue's PR merges (validation) | A defect comment on the issue | Re-run `vapa-exec` on the issue to start a defect-fix round: enumerate new defect comments since the last run, present the fix list for human confirmation, fix on the same branch, reply to each defect comment with the fixing commit and verification evidence, then run a delta re-audit (see Handoff to Audit) |
| After the issue's PR merges | A standalone issue using the lightweight defect template | Standard `vapa-exec` pipeline with its own branch, workspace, audit, and PR. Reference the source issue and comment in the body; tracker linkage (e.g. a GitHub sub-issue relationship) is optional and serves visibility only |

Boundaries:

- Problems found by `vapa-exec`'s own testing are fixed in place (the Step 7 → Step 6 loop); they do not use either defect channel.
- `NEEDS_REVISION` findings from an audit stay in the normal revision loop; they are not promoted to defect channels.
- `defect_fix_rounds` in `state.json` counts defect-fix rounds. If new defects still appear after 3 rounds, escalate to a human — recurring defects indicate a systemic problem in the implementation or the acceptance criteria, not something more fixing can solve.
- Defect issues use the lightweight template at `${CLAUDE_SKILL_DIR}/references/defect-report.md`: symptom, expected behavior, reproduction steps, and source (the validated issue plus comment link). Approval still requires a human; the acceptance criterion is "symptom eliminated without regression".

## Safety and Traceability

- The `.vapa` workspace is commit-worthy by default, but never commit secrets, private user data, production exports, or unreleasable third-party material.
- If sensitive information appears in an issue, summarize it and record the redaction in `source-map.md`.
- Do not delete or rewrite workspace artifacts to hide mistakes. Append corrections or add a new section explaining the revision.
- Do not expand scope just because implementation is easy. Scope changes require human approval or a proposal update.
- If the default branch moves significantly during execution, rebase or merge deliberately, re-run the impacted tests, and record the event in `VAPA_EXEC_LOG.md`.

## Handoff to Audit

After implementation and tests, invoke or recommend `vapa-audit` with the workspace path.

The handoff is ready only when these files exist:

- `state.json` (phase: `tested`)
- `issue-brief.md`
- `source-map.md`
- `readiness-report.md`
- `codebase-survey.md`
- `VAPA_EXEC_PLAN.md`
- `VAPA_EXEC_LOG.md`
- `TEST_REPORT.md`
- `PR_DRAFT.md`
- `ui-spec.md` and `evidence/` when the task touches UI
- `decomposition.md` when the task was decomposed

Expected audit verdicts:

- `READY_FOR_PR`: move toward human validation and PR submission.
- `READY_TO_INTEGRATE`: sub-level verdict for decomposed tasks; authorizes the orchestrator to merge the sub-issue's work back into the parent branch. Never treated as PR readiness.
- `NEEDS_REVISION`: return to implementation or test; increment `revision_count` and respect the revision budget.
- `BLOCKED_FOR_HUMAN_DECISION`: stop and ask the human to decide.

Two-level audit for decomposed tasks:

- Each sub-issue is audited in its own workspace and must reach `READY_TO_INTEGRATE` before the orchestrator merges its work back.
- The parent audit covers the integrated whole. Its precondition is that every sub-issue has reached `READY_TO_INTEGRATE` and been merged back; otherwise the audit returns a not-ready list instead of a verdict (see `vapa-audit`).

Post-audit changes: any code change after an audit verdict — including defect-fix rounds — invalidates that verdict. Run a delta re-audit covering the changed surface plus regression evidence, and issue a revised `VAPA_AUDIT.md`. Delta re-audits do not increment `revision_count`; defect-fix rounds are tracked separately by `defect_fix_rounds`.

## Common Mistakes / Red Flags

- Starting code edits before `readiness-report.md`, `codebase-survey.md`, and `VAPA_EXEC_PLAN.md` exist.
- Treating comments or design screenshots as optional context.
- Paraphrasing acceptance criteria or boundary constraints in the brief instead of quoting them verbatim.
- Planning and implementing from `issue-brief.md` alone, treating the summary as the source of truth and never spot-checking `issue.json`.
- Planning file changes without surveying existing patterns, then fighting the architecture mid-implementation.
- Inventing new components, styles, or utilities when the codebase already has an equivalent.
- Implementing only the happy-path UI state and ignoring loading, empty, error, and disabled states.
- Claiming a UI acceptance criterion passes without rendered visual evidence.
- Using `/tmp` as the only execution record, or losing resumability because `state.json` was never updated.
- Losing track of acceptance criteria during implementation.
- Executing an L/XL task in one session because decomposition felt like overhead.
- Decomposing a sub-issue recursively instead of stopping and escalating.
- Creating tracker sub-issues before the human has confirmed `decomposition.md`.
- Adding sub-issues beyond `decomposition.md` under the cover of the parent's approval.
- Executing a sub-issue standalone without reading the parent plan's cross-cutting contracts.
- Sub-agents writing to the parent branch or the parent `state.json` directly.
- Scheduling a sub-issue before its `depends_on` dependencies have been merged back into the parent branch.
- Summarizing or submitting the parent PR before every sub-issue has reached `READY_TO_INTEGRATE` and been merged back.
- Skipping the delta re-audit after defect fixes.
- Letting the tracker linkage drift from `decomposition.md` without correcting it.
- Iterating on `NEEDS_REVISION` indefinitely instead of escalating a broken assumption.
- Leaving the issue silent for the whole execution — no status label, no progress comments.
- Auditing your own work without writing a separate audit artifact.
- Preparing a PR that lacks traceability back to the proposal.
