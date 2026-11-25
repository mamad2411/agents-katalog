---
name: flow-compilation
description: >
  Business flow slice compilation pipeline. Defines how Flow Mapper output
  (FLOW-*.md files) gets compiled by the Threat Modeler into tasks.
  One flow → N tasks, prioritized by economic risk score and invariant criticality.
trigger: When Threat Modeler reads specs/flows/ to generate tasks.
agents: [threat-modeler, flow-mapper]
---

# Flow Compilation Skill

## From Flow to Tasks

A business flow is NOT a task. A flow describes HOW the protocol works.
A task describes WHAT specific property to prove or disprove.

The compilation step converts flow slices into focused proof obligations.

## Flow → Task Compilation Rules

### Rule 1: One Flow Can Generate Multiple Tasks

For each flow, generate tasks targeting DIFFERENT potential failure modes:

```
FLOW-001-withdraw can generate:
  TASK-001: withdraw() — reentrancy via external token callback
  TASK-002: withdraw() — share price stale at time of calculation
  TASK-003: withdraw() — totalAssets desync from actual balance via donation
  TASK-004: withdraw() — rounding error accumulation over many withdrawals
```

Generate tasks for each failure mode where a violation is PLAUSIBLE given the flow's:
- External calls (reentrancy surface)
- Oracle reads (staleness/manipulation)
- Share price calculations (inflation)
- Rounding operations (precision loss)

### Rule 2: Every Task Must Link to Its Flow

The `flow_id` field in every task must reference the flow that generated it:
```yaml
flow_id: FLOW-001-withdraw
```

This enables flow coverage tracking: the Gap Analyzer can identify which flows
have no resolved tasks.

### Rule 3: Prioritize by Flow's economic_risk_score

```
flow.economic_risk_score >= 0.8 → Tasks from this flow: Critical or High priority
flow.economic_risk_score 0.5-0.8 → Tasks: High or Medium priority
flow.economic_risk_score < 0.5 → Tasks: Medium or Low priority
```

### Rule 4: Inherit Flow Context Into Tasks

Copy relevant context from the flow slice into each task:

```yaml
# From the flow:
execution_path:        inherit the flow's key_contracts → key_functions chain
relevant_state:        inherit the flow's state_changes list
attacker_capabilities: derive from flow's initiator + external_callers
assets_at_risk:        inherit from flow's assets_at_risk list
```

This prevents the Reasoner from having to re-derive context that Flow Mapper already compiled.

### Rule 5: Flow Cross-References = Cross-Contract Tasks

If a flow touches 3+ contracts in sequence, generate at least one cross-contract task:
```
TASK-N: Cross-contract: {FlowName} — state consistency across {Contract A} and {Contract B}
```

## Compilation Template

For each flow file `specs/flows/FLOW-{N}-{name}.md`, the Threat Modeler should:

```
1. Read the flow's key_contracts, key_functions, assets_at_risk, invariants
2. Check negative memory for each potential failure mode
3. For each plausible failure mode:
   a. Determine which of the 10 testing phases applies
   b. Write the task with all 19 fields, linking flow_id
4. Add all tasks from this flow to specs/tasks/INDEX.md
5. Mark the flow as "compiled" in specs/flows/FLOW-INDEX.md
```

## Flow Coverage Tracking

The Orchestrator's gap-cycle engine uses this tracking to detect uncovered flows:

```markdown
# specs/flows/FLOW-INDEX.md (updated by Threat Modeler after compilation)

| Flow ID | Type | Risk Score | Tasks Generated | Tasks Resolved | Coverage |
|---------|------|-----------|----------------|----------------|---------|
| FLOW-001 | withdraw | 0.95 | 4 | 3 | 75% |
| FLOW-002 | deposit | 0.70 | 2 | 2 | 100% |
| FLOW-003 | liquidation | 0.88 | 0 | 0 | ❌ NOT STARTED |
```

A flow with 0 tasks is the highest-value gap (especially if economic_risk_score > 0.7).

## Output Directory Structure

```
specs/
  flows/
    FLOW-001-withdraw.md         ← Flow Mapper output
    FLOW-002-deposit.md
    FLOW-INDEX.md                ← Index with coverage tracking
  tasks/
    TASK-001-withdraw-reentrancy.md     ← Compiled from FLOW-001
    TASK-002-withdraw-share-price.md    ← Compiled from FLOW-001
    TASK-003-deposit-share-inflation.md ← Compiled from FLOW-002
    INDEX.md
```
