---
name: decompose-agentic-system
description: Architect recursive system and task decomposition for large-scale multi-agent architectures (100+ files, 50K+ tokens), DAG dependency trees, disk-backed persistent planning (planning-with-files), anti-context-rot mechanisms, NHI autonomy-tier classification, and policy-as-code fitness functions. Use when scoping complex multi-agent workflows, establishing durable markdown planning, isolating agent blast radiuses, or preventing LLM context rot.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_tests]
version: "1.0.0"
---

# Decompose Agentic System

Architect recursive system and task decomposition for large-scale multi-agent architectures (100+ files, 50K+ tokens), DAG dependency trees, disk-backed persistent planning, and policy-as-code fitness functions.

## Core Rules

- **Recursive Work Breakdown**: Decompose massive workloads (100+ files, 50K+ tokens) hierarchically into bounded sub-agent scopes; prohibit monolithic single-agent execution on massive codebases.
- **Hierarchical DAG Dependency Trees**: Structure execution as Directed Acyclic Graphs (DAGs); establish topological sorting and strictly prohibit unconstrained cyclic agent loops.
- **Invariant Gating**: Enforce automated pre-condition and post-condition assertions at every phase boundary; halt execution immediately on invariant failure (`AGENTIC-DECOMPOSITION LOCK`).
- **Disk-Backed Persistent Planning (`planning-with-files`)**: Maintain execution plans, task manifests, and progress logs in durable markdown files on disk (`plan.md`, `task.md`, `progress.md`, `BRIEFING.md`); never store long-horizon state in ephemeral context (`CONTEXT-ROT-RESISTANCE LOCK`).
- **Deterministic Completion Verification**: Require empirical verification evidence (test outputs, compiler exit code 0, schema validation) before task closure; reject LLM self-declaration of completion.
- **Anti-Context-Rot Discipline**: Enforce periodic liveness updates (`Last visited: [ISO-8601]`), smart zone prompt budgeting, and compact briefings (< 100 lines) surviving context compaction and session resets (`/clear`).
- **Non-Human Identity (NHI) Autonomy Tiers**: Classify sub-agent tasks into Tier 1 (Supervised / HITL), Tier 2 (Semi-Autonomous / Guardrailed), or Tier 3 (Fully Autonomous / Sandboxed).
- **Blast-Radius Perimeter Isolation**: Confine sub-agent filesystem access, network egress, and token capabilities to designated module directories and sandboxes (`BLAST-RADIUS LOCK`).
- **Policy-as-Code Architectural Fitness Functions**: Codify architectural constraints into automated CI fitness functions using Cedar (agent trust boundaries), OPA/Rego (module boundaries), or calibrated LLM-as-judge (`FITNESS-FUNCTION LOCK`).

## When to Use

- Structuring massive multi-agent software engineering initiatives spanning 100+ files or 50K+ tokens
- Designing hierarchical DAG execution graphs with topological sequencing and invariant checks
- Establishing disk-backed durable planning (`planning-with-files`) resilient to context rot and `/clear`
- Defining Non-Human Identity (NHI) autonomy tiers, blast-radius perimeters, and sandbox policies
- Formulating policy-as-code architectural fitness functions (Cedar, OPA/Rego, calibrated LLM-as-judge)
- Eliminating agent loops, attention degradation, and premature self-declared task completions

## Suggested Process

1. **Analyze System Scope & Complexity**: Quantify token envelope, file surface, and subsystem boundaries; determine if workload requires recursive DAG breakdown.
2. **Construct Hierarchical DAG Dependency Tree**: Map milestones, epics, and atomic implementation slices into a DAG; declare hard blockers, parallel streams, and invariant checkpoints.
3. **Establish Persistent Planning Workspace**: Configure disk-backed durable planning artifacts (`task.md`, `plan.md`, `progress.md`, `BRIEFING.md`) and compaction recovery routines.
4. **Classify NHI Autonomy Tiers & Approvals**: Map execution phases to Tier 1, Tier 2, or Tier 3; define human-in-the-loop (HITL) escalation gates for irreversible actions.
5. **Enforce Blast-Radius & Sandboxing Perimeters**: Define directory boundaries, ephemeral scoped credentials, and network egress policies per sub-agent role.
6. **Implement Policy-as-Code Fitness Functions**: Codify boundary rules and delegation limits into Cedar policies or OPA/Rego tests; calibrate LLM judges against historical PRs.
7. **Specify Completion Predicates & Emit Contracts**: Define deterministic verification commands, test assertions, and emit `adr-spec.json` and `architecture-options.json`.

## Checklist

- [ ] Workload decomposed into hierarchical DAG sub-agent scopes without cyclic loops.
- [ ] Invariant pre- and post-conditions defined for every DAG phase boundary.
- [ ] Persistent planning configured with durable disk markdown files (`planning-with-files`).
- [ ] Compaction recovery protocol established to resume state after `/clear` or context overflow.
- [ ] Deterministic completion gates require empirical proof (exit code 0, test results).
- [ ] NHI autonomy tiers (Tier 1-3) assigned with explicit HITL approval triggers.
- [ ] Blast-radius perimeters restrict sub-agent filesystem mutations and network egress.
- [ ] Policy-as-code fitness functions (Cedar / OPA) codify architectural invariants.
- [ ] Architecture decision record emitted conforming to `contracts/schemas/adr-spec.json`.

## Output Contracts

When decomposition and planning architecture is established:

- **`contracts/schemas/adr-spec.json`**: Primary architectural decision record specifying DAG topology, persistent planning protocols, NHI autonomy tiers, and fitness functions.
- **`contracts/schemas/architecture-options.json`**: Comparative analysis evaluating decomposition granularities, state persistence strategies, and sandbox isolation boundaries.

## Failure Modes

- **Monolithic Context Exhaustion**: Assigning 100+ files to a single agent induces attention dilution, hallucinated imports, and silent file drops. Mitigation: Enforce recursive DAG sub-agent scoping.
- **Premature Self-Declaration ("Vibe Completion")**: Agents claim tasks are complete without running tests or builds. Mitigation: Enforce deterministic completion gates requiring empirical verification logs.
- **Context Rot on Long Horizons**: Agent loses early requirements after multi-turn tool calling or compaction. Mitigation: Decouple state into disk-backed durable files (`plan.md`, `task.md`).
- **Lateral Privilege Escalation**: A compromised or drifting sub-agent modifies critical infrastructure or adjacent modules. Mitigation: Enforce blast-radius perimeters and Cedar policy bounds.

## Security Guardrails (OWASP ASI)

- **ASI01 Prompt Injection via External Context**: Sanitize file contents and tool outputs before feeding into sub-agent planning contexts.
- **ASI02 Tool Misuse & Exploitation**: Restrict sub-agents to least-privilege tool allowlists; mandate HITL approval for schema drops, deployments, or credential access.
- **ASI03 Identity & Privilege Abuse**: Provision ephemeral, role-scoped NHI credentials; prohibit shared master credentials across sub-agents.
- **ASI07 Insecure Inter-Agent Communication**: Validate contract schemas and signatures on all inter-agent messages and handoff artifacts.
- **ASI08 Cascading Agent Failures**: Isolate sub-agent failure domains; halt DAG branch on invariant failure to prevent error propagation.
- **ASI09 Over-Reliance on Autonomous Logic**: Embed policy-as-code fitness functions and automated linters as objective arbiters of correctness.
- **ASI10 Rogue Agent Misbehavior**: Monitor token velocity and file mutation scope; trigger automatic kill-switches on out-of-boundary access.

## Related Skills

- **architect-mcp-server**: Architect MCP tool contracts and stateless transports used by decomposed sub-agents
- **system-design**: Design overall system architectures, data flows, and infrastructure capacity
- **agent-graph-orchestration**: Orchestrate dynamic runtime DAG execution graphs and agent state machines
- **agent-context-management**: Manage prompt token budgets, smart zone buffers, and sliding window memory
- **agent-delegation**: Execute runtime task handoffs between parent and worker agents
- **agent-panel-meeting**: Convene multi-agent expert panels to debate high-stakes architectural options
- **ai-risk-assessment**: Assess safety, compliance, and failure risks of autonomous agent systems
- **plan-technical-delivery**: Translate architectural DAGs into sprint implementation milestones
