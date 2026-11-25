# Multi-Agent Orchestration

## Purpose
Execute multi-agent work as a dependency DAG with isolated workspaces, capped retries and delegation depth, diversified reviewers, and evidence-gated completion so CI and recorded evidence, not agent self-report, decide when a Goal is done.

## Use when
- Running a live multi-agent Goal that fans out across implementers, test runners, and reviewers.
- Planning task order as a dependency DAG with critical-path scheduling and parallel dispatch.
- Enforcing isolation between agents (separate worktrees, no shared mutable state) and caps on retries and delegation.
- Certifying completion: every leaf task carries test, lint, or review evidence before the Goal closes.

## Do not use when
- Designing the recipe, roles, and handoff contracts up front (use `agentic-workflow-design`).
- Running a single-agent task with no delegation or parallelism.
- Assigning human incident-command roles or on-call rotations.

## Required context
- Approved workflow recipe (from `agentic-workflow-design`) with stages, owners, and handoff schemas.
- Dependency DAG: nodes with inputs, edges for depends-on, and the computed critical path.
- Isolation mechanism: git worktrees per agent (e.g. /tmp/prumo-wt/T-342-coder) with merge-back protocol.
- Caps ledger: retries used per node (cap 2), delegation depth used (cap 3), reviewer diversity record.

## Procedure
1. **Materialize the DAG**: expand the recipe into executable nodes with explicit depends-on edges using `prumo plan --dag`; compute the critical path and dispatch ready nodes in parallel up to the pool limit of 4 concurrent agents.
2. **Isolate every worker**: give each implementer its own git worktree and task-scoped file allowlist (e.g. auth/refresh.go, auth/refresh_test.go); workers never write outside their allowlist or into another worktree.
3. **Enforce caps at runtime**: track retries per node and delegation depth per chain in the caps ledger; a node exhausting 2 retries or a chain reaching depth 3 is parked and escalated, never silently retried again.
4. **Diversify review**: assign reviewers with no authorship on the diff (author != reviewer enforced by user id check); security-sensitive diffs require 2 reviewers, one with security scope.
5. **Gate completion on evidence**: a node closes only with attached evidence (test log, lint log, or review approval id); CI re-runs the suite on merge-back and its verdict overrides any agent claim of done.
6. **Record the run and execute `scripts/verify.sh`**: archive the DAG, caps ledger, reviewer record, and CI verdicts under evidence/<goal-id>/ for audit.

## Decision rules
- **DAG before dispatch**: no agent starts until its node, dependencies, and allowlist are recorded in the DAG.
- **Isolation is structural**: separate worktrees and allowlists, never policy-by-prompt ("please don't touch other files").
- **Caps are hard stops**: retry 3 or depth 4 does not happen; the node parks and a human decides.
- **Evidence over assertion**: "done" without attached test, lint, or review evidence is rejected by the orchestrator.
- **CI is the final arbiter**: conflicting agent claims resolve in favor of the CI verdict on the merged result.

## Evidence required
- Executed DAG with per-node status, retry counts, and depth records.
- Reviewer diversity record proving author != reviewer on every diff.
- CI verdicts on every merge-back plus the archived run bundle.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Merged, CI-green result for the Goal with full evidence traceability.
- Archived run bundle (DAG, caps ledger, reviews, CI logs) under evidence/<goal-id>/.
- Post-run report naming cap hits, escalations, and reviewer coverage.

## Stop conditions
- All DAG nodes closed with evidence and CI green on merge-back.
- Caps exhausted on a node; parked and escalated with a written record.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the Goal owner when the critical path slips past the committed date or a node parks on exhausted caps.
- Escalate to a human immediately if isolation is breached (cross-worktree writes) or reviewer independence cannot be staffed.
