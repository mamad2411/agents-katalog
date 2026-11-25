---
name: agentic-workflow-patterns
description: Use when designing, reviewing, or structuring multi-step agentic workflows — covering prompt chaining, parallelization, orchestrator-subagent handoffs, evaluator-optimizer loops, and artifact-first agent-usable delivery design.
---

# Agentic Workflow Patterns

## Specialization

Design and validate multi-step agentic workflows so agents can execute delivery, engineering, and review work deterministically without relying on implicit human coordination.

This skill translates agentic execution research into practical workflow construction rules. It applies across every skill family in the workspace — delivery, engineering, testing, UX — wherever a task must be decomposed, parallelized, or handed off between agent components.

## Objective

Produce an agentic workflow design that is explicit, deterministic, and auditable: inputs and outputs are defined per step, agents cannot silently skip or expand scope, and every handoff has an explicit entry condition and exit gate.

## Trigger Conditions

- A task spans multiple steps, skills, or agents and execution order matters.
- A skill, plan, or delivery artifact needs to be validated before it can serve as an agent input.
- A multi-agent system (orchestrator + specialists) needs explicit routing and handoff rules.
- A task involves parallel workstreams that must be synchronized before downstream steps proceed.
- Agent outputs are inconsistent or non-deterministic and the workflow needs hardening.

## Scope Boundaries

In scope:

- Agentic workflow pattern selection and composition.
- Step-level input and output contracts.
- Parallelization analysis and synchronization rules.
- Orchestrator-subagent routing and handoff design.
- Evaluator-optimizer loop design for iterative refinement.
- Artifact-first design: all agent inputs and outputs are durable, inspectable artifacts.
- Tool use boundaries and fallback rules.

Out of scope:

- Application implementation code.
- Agent `.agent.md` file authoring (use `agent-authoring`).
- Skill or instruction file creation (use `skills-authoring` or `instructions-authoring`).
- Model selection or inference budget optimization.
- Platform-specific API configuration.

## Inputs

- Task or workflow description: what must be accomplished end to end.
- Known constraints: ordering dependencies, approval gates, tool availability, scope limits.
- Participating agent types or skill families: orchestrator, specialists, reviewers.
- Any existing artifact contracts or skill outputs that feed into the workflow.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Workflow pattern selection with rationale: which pattern fits the task and why.
- Step map: ordered steps with named inputs, outputs, and handoff conditions.
- Parallelization analysis: which steps are independent and can run concurrently.
- Handoff contract: entry condition, exit gate, and escalation rule per boundary.
- Evaluator gate design (when iteration is required): pass criteria, fail action, and loop stop rule.
- Anti-pattern flags: list of workflow smells detected and their remediation.

## Workflow Patterns

### Prompt Chaining

Use when a task decomposes into a fixed, sequential pipeline where each step's output is the next step's input.

Rules:
- Each step must have exactly one named output artifact.
- A step must not proceed if the previous step's output fails its exit gate.
- Do not chain more than necessary — merge steps that share the same agent context without meaningful intermediate artifact value.

### Parallelization

Use when independent subtasks can be executed concurrently and their results merged before a synchronization step.

Rules:
- Subtasks are independent if they share no mutable state and produce non-conflicting outputs.
- Define the synchronization point explicitly: what artifact or signal triggers merging.
- Merging must have an explicit conflict resolution rule when outputs can disagree.

### Orchestrator-Subagent

Use when a coordinating agent routes tasks to specialist agents based on task type and skill domain.

Rules:
- The orchestrator MUST classify scope before routing. No direct specialist execution without intake.
- Each routing decision must include: target specialist, task boundary, required input artifact, and expected output artifact.
- The orchestrator is responsible for final output assembly; specialists are responsible for their task scope only.
- If a specialist's output fails its quality gate, the orchestrator routes to remediation, not silent retry.

### Evaluator-Optimizer

Use when a task requires iterative refinement until a quality threshold is met.

Rules:
- Define the evaluator criteria before the first optimizer run. Do not evaluate against vague standards.
- The loop must have an explicit maximum iteration count and a hard stop rule.
- On each loop: the optimizer receives the evaluator's failure signal as a structured input, not raw prose.
- When the stop rule triggers without passing evaluation, escalate rather than deliver a failing artifact.

### Routing Gate

Use when a task needs a classification or decision step before execution branches.

Rules:
- The gate must produce an explicit routing decision with rationale.
- Each branch must have a defined input contract.
- Unknown or ambiguous inputs must route to a clarification step, not to a default branch.

## Deterministic Workflow

1. Identify the task type and whether it is sequential, parallel, iterative, or routed.
2. Select one or more patterns. Prefer the simplest composition that satisfies the task.
3. Define each step: name, input artifact, output artifact, entry condition, exit gate.
4. Mark independent steps as parallelizable and define the synchronization contract.
5. For orchestrator-subagent designs: define routing rules, specialist boundaries, and output assembly.
6. For evaluator-optimizer designs: define evaluator criteria, loop stop rule, and escalation path.
7. Check each handoff for implicit contracts — if the next step cannot start without human interpretation of the previous output, the contract is not explicit enough.
8. Flag anti-patterns and record remediation.
9. Publish the workflow design as a durable artifact before execution begins.

## Anti-Patterns

- **Invisible handoffs**: the next step assumes context that was never output by the previous step.
- **Scope creep by default**: an agent expands task scope without an explicit gate approving the expansion.
- **Silent retry**: an evaluator failure causes the optimizer to silently re-run without a structured failure signal.
- **Monolithic orchestrator**: the orchestrator handles task-level work instead of routing; specialist boundaries collapse.
- **Missing stop rule**: an evaluator-optimizer loop has no maximum iteration count and can run indefinitely.
- **Prose-only contracts**: step outputs are free-form prose with no defined minimum fields, making them unreliable as downstream inputs.
- **Parallel without synchronization**: independent subtasks run concurrently but the merge step has no defined conflict resolution.

## Artifact Contract

| Artifact | Minimum Fields |
|---|---|
| Workflow design | Task description, pattern selected, step count, parallelization note |
| Step map | Step name, input artifact, output artifact, entry condition, exit gate |
| Handoff contract | Boundary ID, entry condition, exit gate, escalation rule |
| Evaluator gate | Criteria, pass signal, fail action, max iterations, hard stop rule |
| Anti-pattern log | Pattern name, location in workflow, remediation |

## Done Criteria

- Workflow pattern is selected with rationale.
- Step map is complete with explicit input/output artifacts.
- All handoff contracts are written.
- Evaluator gates are defined where iteration exists.
- Anti-pattern log is present and empty or remediated.
- Source catalog entries are current for this evaluation cycle.

## Workflow

1. Capture inputs and constraints.
2. Execute this skill's deterministic steps.
3. Publish outputs with status and next actions.

## Execution Context
### Input Context

- Request objective and scope boundary.
- Applicable constraints and required outputs.

### Process Context

- Follow this skill's deterministic workflow from intake to closure.
- Record ownership and decisions for required outputs.

### Output Context

- Deliverables with explicit completion status.
- Residual risks and next actions.
## References Assets

- [Reference assets](./references/README.md)
