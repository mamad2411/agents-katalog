# Agentic Workflow Design

## Purpose
Design multi-agent recipes with explicit roles, state transitions, handoff contracts, coordination topologies, idempotency rules, and capped delegation depth so agent teams execute predictably instead of improvising coordination.

## Use when
- Defining a repeatable multi-agent recipe (triage loop, implement-review-merge pipeline, research-then-plan flow).
- Specifying handoff contracts between agents: required inputs, produced outputs, and evidence attached.
- Choosing a coordination topology (pipeline, fan-out/fan-in, supervisor, blackboard) for a Goal.
- Auditing an existing workflow for unbounded delegation, missing idempotency, or ambiguous ownership.

## Do not use when
- Executing a live multi-agent run with DAG scheduling and retry enforcement (use `orchestration-multi-agent`).
- Writing a single-agent system prompt (use `prompt-engineering`).
- Assigning human team responsibilities or sprint planning.

## Required context
- Goal statement with acceptance criteria and the evidence gates each stage must pass.
- Agent roster with capabilities (e.g. implementer with filesystem.write, reviewer read-only, test-runner with process.spawn).
- Shared state model: where handoff artifacts live (e.g. evidence/ directory, task ledger) and their schemas.
- Failure budget: max delegation depth (default 3), max retries per stage (default 2).

## Procedure
1. **Decompose into stages with owners**: split the Goal into stages (e.g. scout, implement, test, review), assign exactly one owning role per stage, and name the evidence each stage produces.
2. **Select the topology**: pipeline for linear flows, fan-out/fan-in for parallelizable shards with a merge stage, supervisor when dynamic routing is needed; document why the chosen topology fits the dependency structure.
3. **Write handoff contracts**: each handoff specifies required inputs (files, ids, prior evidence), produced outputs, and the schema version of exchanged artifacts (e.g. handoff v2 with fields task_id, files_changed, test_log).
4. **Define state transitions explicitly**: enumerate allowed transitions (pending -> running -> in_review -> done, running -> failed -> retrying) and forbid all others; retries increment a counter capped at 2 per stage.
5. **Enforce idempotency and depth caps**: every stage action must be safely re-runnable (same inputs, same result, no duplicate side effects); delegation chains halt at depth 3 and escalate instead of recursing.
6. **Simulate failure paths and run `scripts/verify.sh`**: walk through stage failure, reviewer rejection, and handoff schema mismatch; confirm each path terminates in done, escalated, or aborted, never in silent stall.

## Decision rules
- **One owner per stage**: shared ownership of a stage is prohibited; exactly one role answers for it.
- **Contracts before code**: no agent starts its stage until the handoff contract schema is written and versioned.
- **Bounded delegation**: delegation depth never exceeds 3; retries never exceed 2 per stage without escalation.
- **Idempotency mandatory**: any stage that cannot be safely retried must be redesigned before the recipe ships.
- **Explicit transitions only**: undocumented state transitions are treated as workflow defects.

## Evidence required
- Recipe document with stages, owners, topology rationale, and transition table.
- Versioned handoff contract schemas for every inter-stage boundary.
- Failure-path walkthrough showing termination for failure, rejection, and mismatch cases.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Shippable workflow recipe ready for the orchestrator to execute.
- Handoff schemas versioned and stored alongside the recipe.
- Failure analysis proving no silent-stall paths exist.

## Stop conditions
- Recipe covers all stages, contracts, transitions, and failure paths with evidence.
- Reviewer approves the recipe against the checklist.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the Goal owner if the decomposition reveals the Goal is too large for one recipe and must be split.
- Escalate to a human if failure analysis exposes a stall path that capping and contracts cannot close.
