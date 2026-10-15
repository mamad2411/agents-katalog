---
name: fast-end-to-end-development
description: "Run a lightweight, artifact-backed development workflow for an ordinary single-repository change: agent planning, implementation, one independent review, one revision pass, and pull-request creation, with an optional self-contained HTML explainer. Use when the user wants a quicker end-to-end coding flow and does not require durable orchestration, high-risk approval, multi-repository integration, or resumability."
---

# Fast End-to-End Development

Use this skill for a small or medium change that should move from request to pull request in one bounded pass:

`plan → implement → review once → revise once → create PR → [optional HTML explainer]`

The current agent owns the run. Keep the process fast by removing Herdr worker orchestration, multi-profile policy selection, mandatory plan-approval pauses, integration workers, and retry loops. Keep the safety that matters: preserve pre-existing work, inspect repository instructions, record evidence, use a fresh reviewer, cap remediation at one batch, and stop on material ambiguity or high-risk scope.

Resolve `SKILL_DIR` to this skill's directory. Set `RUN_DIR` to the run directory created below and pass absolute paths to the renderer.

## Agent runtime

Use `gpt-5.6-luna` with effort proportional to the work: `high` for planning, implementation, review, and revision; `medium` for delivery or artifact rendering. Mechanical Git, forge, and renderer commands do not need a delegated model session. When launching an agent explicitly, pass the corresponding Codex `reasoning_effort` or Pi `--thinking` value.

## Herdr pane lifecycle

When this workflow creates an agent pane through Herdr, record the returned `pane_id` separately from any `terminal_id`. As soon as that agent settles and its required result has been captured, close the workflow-created pane with `herdr pane close <pane_id>` and verify the command succeeds. Do this after planning, review, delivery, or any other delegated stage rather than leaving completed panes visible until the final handoff.

Before reporting completion, account for every Herdr pane created by this run and close any remaining settled pane. Never close the coordinator pane, a pre-existing user pane, or a pane that is still working, blocked, or needed to diagnose a timeout. If a completed pane cannot be closed, report pane cleanup as a blocker instead of making the user infer which pane is still active.

## Scope gate

Use the fast path for one repository and ordinary application changes. Before editing:

- Escalate to `end-to-end-development` for multiple repositories or changes involving authorization, security-sensitive code, database migrations or backfills, destructive data operations, concurrency/distributed behavior, background processing, new storage, public contracts, or another high-cost mechanism.
- Ask the user only when a material product decision or repository identity cannot be established. Do not pause merely for plan approval.
- Read repository-local instructions (`AGENTS.md`, `CONTRIBUTING.md`, `README`, package/build configuration, and relevant nested instructions) before planning.
- Verify Git and the repository forge are available when the request includes a PR. Prefer the connected GitHub capability or `gh` for GitHub; use the repository's established forge CLI otherwise.

## Durable run record

Create a run directory outside the repository before changing code:

```text
${XDG_STATE_HOME:-$HOME/.local/state}/codex/fast-end-to-end-development/<UTC-timestamp>-<request-slug>/
```

Keep concise evidence there; keep full command output in a `logs/` child directory. Write these files as stages complete:

| File | Required contents |
| --- | --- |
| `request.md` | User request verbatim and the resolved repository/branch scope |
| `plan.md` | Acceptance criteria, implementation slices, checks, risks, and non-goals |
| `implementation.md` | What changed, changed-file inventory, and pre-review checks |
| `review.md` | Exactly one independent review, findings, severity, and evidence |
| `revision.md` | Finding dispositions, any fixes, and post-revision checks |
| `delivery.md` | Commit, branch, PR URL, and forge/check status |
| `pr-explainer.json` | When requested: sanitized structured input for the HTML renderer |
| `pr-explainer.html` | When requested: self-contained human-readable PR explainer |

Do not put secrets, environment values, full diffs, or unbounded terminal transcripts in these artifacts. Record commands, exit codes, short conclusions, hashes, and paths instead.

## Invariants

- Capture `git status --short` and the baseline commit before editing. Preserve unrelated user changes; never use `reset --hard`, `clean`, broad checkout, or an overwrite to make the tree convenient.
- Use a task branch unless the user explicitly supplied a task branch. If unrelated uncommitted changes make branch isolation unsafe, use a dedicated worktree or stop and explain the boundary.
- Keep one project-file writer. Do not let a reviewer or delivery step edit source files.
- Close every workflow-created Herdr pane immediately after its agent settles and its result is captured; retain only working, blocked, or timed-out panes that still need attention.
- Treat the plan as the implementation contract. A simpler equivalent change or focused test is allowed; a new high-cost mechanism, public contract, migration, or unrelated refactor requires escalation.
- Perform at most one review and one revision batch. A no-op revision is valid when the review has no `must-fix` findings. Never start a second review or revision batch.
- Do not create the PR until the revision gate and required local checks pass. If a post-PR CI failure needs code changes after the one revision is spent, report the blocker and recommend the full workflow.
- Keep the HTML explainer derived from accepted artifacts, not from memory or raw transcripts.

## Workflow

### 1. Plan by the agent

Inspect the repository, current branch, working-tree status, recent conventions, relevant implementation files, tests, and delivery configuration. Establish:

- the exact baseline commit and task branch;
- observable acceptance criteria mapped to files/modules;
- the smallest implementation slices and their order;
- focused and broad validation commands;
- risks, non-goals, and any required user decision.

Write `plan.md` before implementation. Keep it outcome-oriented rather than a list of speculative line edits. If the tree is dirty, identify which changes predate the run and carry that inventory into `implementation.md` and `delivery.md`.

### 2. Implement

Implement the approved-by-the-agent plan in the task branch. Follow existing patterns, keep the diff narrow, and add or update focused tests with the behavior. Do not introduce an undeclared mechanism merely to avoid asking a question.

Run `git diff --check`, focused tests, and the relevant broader checks in one validation pass. Record each command, exit code, and a concise result in `implementation.md`. Stop on a failing environment or dependency check rather than hiding it as a code result.

### 3. Review once

Run one fresh, independent review against the baseline-to-current diff. Give the reviewer `plan.md`, the acceptance criteria, repository instructions, changed-file inventory, and the diff; do not give it the implementer's conclusions. The reviewer checks:

- requirement and acceptance-criteria coverage;
- correctness, edge cases, and error handling;
- security and data-safety implications appropriate to the scope;
- compatibility with repository conventions;
- tests and missing validation;
- accidental scope expansion or undeclared mechanisms.

Do not fix files during review. Write `review.md` with a stable finding ID, severity (`must-fix` or `advisory`), evidence path/hunk, and disposition. A review with no findings must say so explicitly and record the reviewed baseline and head.

### 4. Revise once

Resolve all compatible `must-fix` findings in one bounded batch. Keep advisory findings visible without creating another worker or review cycle. If a finding requires changing the product decision, plan, public interface, migration strategy, or risk profile, stop and escalate instead of stretching the fast path.

Run the affected tests plus the relevant broad checks once after the batch. Write `revision.md` mapping every finding ID to `resolved`, `accepted-as-advisory`, or `blocked`, with changed files and command results. If no revision is needed, record a no-op revision and retain the passing checks.

### 5. Create the PR

Before delivery, verify the diff contains only task changes, no secrets, and no unexplained generated files. Confirm the final checks and branch tip, then:

1. Commit only the task changes with a focused message.
2. Push the task branch with its upstream configured.
3. Create the PR against the recorded base branch.
4. Use a concise PR body containing the problem, solution, tests, review/revision status, and risks. Add the HTML explainer reference after rendering when the forge supports a comment or attachment.
5. Record the commit SHA, PR URL/number, base/head, and initial check state in `delivery.md`.

Use the forge's normal authentication and PR tooling. Do not amend or force-push unrelated history. If the forge rejects delivery for authentication, permission, or infrastructure reasons, preserve the artifacts and report the exact next action.

### 6. Optionally render the PR explainer in HTML

Run this step only when the user requested an HTML report/explainer. After the PR exists, write a sanitized `pr-explainer.json` from the plan, implementation, review, revision, and delivery artifacts. Render a self-contained HTML file:

```bash
python3 "$SKILL_DIR/scripts/render_pr_explainer.py" \
  --input "$RUN_DIR/pr-explainer.json" \
  --output "$RUN_DIR/pr-explainer.html"
```

The explainer must include the request, outcome, plan, changed files, validation commands/results, the single review and finding dispositions, revision status, PR link, risks, and remaining notes. It must not embed secrets, raw logs, or a full diff. Link or mention the generated artifact in the final handoff; if the forge supports a comment or attachment workflow, add the artifact reference after rendering without modifying project files.

The renderer requires non-empty `title`, `summary`, `repository`, and `pr_url` fields. Also provide `branch`, `base`, `acceptance_criteria`, `plan`, `implementation`, `validation`, `review`, `revision`, `delivery`, `risks`, and `remaining_notes` so the explainer is useful rather than a placeholder.

## Completion handoff

Finish only when the PR exists, any requested `pr-explainer.html` validates as a readable file, and every completed Herdr pane created by the workflow has been closed. Report, briefly:

- status and PR URL;
- final commit and check state;
- run directory and HTML artifact path when requested;
- unresolved advisory findings or blockers, if any.

If any gate fails, do not claim completion. Leave the durable artifacts in place and state the exact resume action or escalation to the full `end-to-end-development` skill. Absence of an unrequested HTML explainer is not a failed gate.

## Bundled resource

`[scripts/render_pr_explainer.py](scripts/render_pr_explainer.py)` renders the final explainer without third-party dependencies. It accepts JSON on disk or stdin and HTML-escapes all user/repository-controlled values.
