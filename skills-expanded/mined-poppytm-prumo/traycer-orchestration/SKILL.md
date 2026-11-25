# Traycer Build-Tracer Orchestration

## Purpose
Orchestrate AI-assisted build execution with Traycer treated strictly as a replaceable execution adapter: repository Goals and acceptance criteria stay canonical, work decomposes into a traced plan graph, every step emits replayable artifacts, checkpoints allow resume after interruption, and verification gates decide completion — never the adapter's internal status.

## Use when
- A Goal requires multi-step build, migration, or refactor execution where progress must survive interruptions and be auditable afterward.
- Decomposing a locked Goal into ordered plan steps with explicit inputs, outputs, and per-step verification.
- Replaying a previous execution trace to audit decisions or resume from the last green checkpoint.
- Swapping or upgrading the execution adapter without rewriting Goals, plans, or evidence.

## Do not use when
- The task is a single atomic edit with no sequencing, checkpoint, or replay value; direct implementation is cheaper.
- Repository Goals or acceptance criteria are still undefined; orchestration cannot substitute for missing objectives.
- The workflow needs hard real-time guarantees or kernel-level scheduling that a build-tracer adapter cannot provide.

## Required context
- Locked Goal with measurable acceptance criteria and the frozen plan-graph version under execution.
- Adapter interface version, for example Traycer adapter v2.4 with plan, dispatch, trace, checkpoint, and replay operations.
- Checkpoint policy: checkpoint after every green verification gate, retain the last 20 checkpoints per plan.
- Budgets: maximum 25 plan steps, maximum 3 retries per step, step timeout 20 minutes.

## Procedure
1. **Freeze the plan graph**: decompose the Goal into at most 25 ordered steps, each declaring inputs, expected artifacts, and its verification gate. Record the plan hash; any mid-run plan edit creates a new plan version and re-baselines downstream checkpoints.
2. **Dispatch through the adapter boundary**: send each step to Traycer with repository paths and acceptance text only. The adapter never receives authority to reinterpret the Goal; outputs that contradict acceptance criteria are rejected at the boundary regardless of adapter-reported success.
3. **Trace every step**: append plan-step id, adapter operation, artifact hashes, start and end timestamps, and gate verdicts to the append-only step ledger at `.prumo/tracer/ledger.jsonl`. A step without a ledger entry is treated as not executed.
4. **Gate and checkpoint**: run the step verification gate immediately after execution; on pass, write a checkpoint containing the artifact snapshot plus ledger offset, keeping the last 20. On gate failure, retry up to 3 times with the failure log attached, then mark the step blocked and halt the plan.
5. **Resume and replay**: after any interruption, resume from the latest checkpoint by replaying the ledger forward; never re-execute green steps. Produce replay reports pairing each artifact with the ledger entry that created it for audit.
6. **Verify the orchestration**: run `scripts/verify.sh`, confirm trace completeness at 100% of executed steps, step success rate above 90%, and a clean resume drill from checkpoint on the sample plan before closing the Goal.

## Decision rules
- **Goals are canonical**: on any conflict between adapter output and repository acceptance criteria, the criteria win and the step fails.
- **No ledger entry, no execution**: untraced work is rework; credit is granted only to ledger-recorded steps with gate verdicts.
- **Checkpoints gate retries**: a step exhausts its 3 retries only from checkpointed state, never by mutating uncommitted leftovers.
- **Adapter is replaceable**: no plan, ledger, or checkpoint may depend on Traycer-internal identifiers; migration to another adapter must replay existing ledgers.
- **Blocked halts the plan**: a step that fails 3 gates stops downstream dispatch until a human re-plans; optimistic continuation is forbidden.

## Evidence required
- Orchestration specification following `templates/traycer-orchestration-spec.md` with plan graph, budgets, and adapter version.
- Append-only step ledger with per-step gate verdicts and artifact hashes.
- Checkpoint inventory plus a resume-drill report proving green steps are not re-executed.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Executed plan with per-step artifacts, gate verdicts, and trace completeness report.
- Checkpoint set enabling resume from the last green state.
- Replayable audit trail mapping every artifact to its creating ledger entry.

## Stop conditions
- All plan steps green with trace completeness at 100% and Goal acceptance criteria satisfied.
- A step blocks after 3 failed gates and the plan halts for human re-planning.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to the Goal owner when the adapter repeatedly produces outputs that contradict acceptance criteria, so the plan or the adapter selection can be revised.
- Escalate to the lead architect if checkpoint resume diverges from fresh execution, indicating nondeterminism that tracing cannot paper over.
