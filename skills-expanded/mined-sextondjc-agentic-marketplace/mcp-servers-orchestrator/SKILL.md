---
name: mcp-servers-orchestrator
description: Use when an MCP request spans writing, refining, and improving servers and needs deterministic phase ownership with official-source and SDK-scope controls.
---

# MCP Servers Orchestrator

## Specialization

Coordinate multi-phase MCP server work from one intake while enforcing two hard constraints:

- Official MCP sources only.
- SDK implementation decisions limited to C# and TypeScript.

## Trigger Conditions

- A request spans server creation, refinement, and quality improvement.
- The work needs one intake and explicit ownership across multiple phases.
- A cross-project compendium asset must be reusable without repo-specific assumptions.

## Scope Boundaries

In scope:

- Deterministic MCP work intake and phase ownership.
- Phase-output mapping for write, refine, and quality gate flows.
- Official-source and SDK-scope policy enforcement.

Out of scope:

- Language paths outside C# and TypeScript.
- Community source routing and aggregator-driven recommendations.

## Inputs

- Objective and required outputs.
- In-scope server domain and runtime constraints.
- Risk level and release target.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Intake contract with objective, boundaries, and required outputs.
- Phase-output ownership matrix.
- Unified execution recommendation with explicit mode.
- Rejected-candidate table with deterministic reason codes.

## Capability Phases

- Write phase: baseline server implementation contract.
- Refine phase: ergonomics, robustness, and maintenance improvements.
- Quality gate phase: security, reliability, protocol compliance, and release readiness.

## Deterministic Workflow

1. Lock intake objective, constraints, and required outputs.
2. Select phase set from Write, Refine, and Quality Gate.
3. Map every required output to exactly one owning phase.
4. Reject the plan if any required output is unowned or multiply owned.
5. Enforce source and SDK policies before execution.
6. Produce one recommendation: `narrow-execution`, `phased-execution`, or `stop-pending-blockers`.
7. Publish closure status with unresolved blockers.

## Phase Ownership Matrix Template

| Required Output | Owning Phase | Evidence Expectation |
|---|---|---|
| Initial server contract | Write | Tool/resource/prompt design with transport selection |
| Incremental hardening set | Refine | Delta list with behavior and compatibility notes |
| Final go or no-go | Quality Gate | Severity-ranked findings and gate disposition |

## Policy Locks

- Official sources only. See [source-catalog.md](./references/source-catalog.md).
- C# and TypeScript are the only SDK tracks allowed in this workflow.

## Reason Codes

- `R1`: Outside MCP server scope.
- `R2`: Violates official-source-only policy.
- `R3`: Violates C#/TypeScript-only SDK policy.
- `R4`: Missing required evidence for owned outputs.
- `R5`: Adds phase overlap without new coverage.

## Done Criteria

- Required outputs have exactly one owner each.
- Execution mode is explicit.
- Policy locks are satisfied.
- Residual risks and blockers are documented.


