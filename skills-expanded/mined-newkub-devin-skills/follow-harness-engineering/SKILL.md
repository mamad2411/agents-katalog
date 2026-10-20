---
name: follow-harness-engineering
description: Build and improve AI agent harnesses for reliability and verifiable execution
argument-hint: "[scope]"
related:
  - follow-context-engineering
  - deep-review-codebase
  - deep-validate
  - run-test
---

## Goal

Build and improve AI agent harnesses (the runtime infrastructure layer) for reliability, verifiable execution, and auditable agent workflows

## Scope

Use for projects with AI agent infrastructure such as MCP servers, agent runtimes, tool interfaces, or coding agent systems that need harness-level engineering

See also: /deep-review-codebase

## Execute

### 1. Assess Harness Components

> Goal: Assess Harness Components

Assess harness components against the ETCLOVG taxonomy

1. Check the Execution environment: sandbox, runtime, resource limits, isolation
2. Check the Tool interface: tool definitions, input/output schemas, error handling, token efficiency
3. Check Context management: context selection, compaction, memory — run `/follow-context-engineering`
4. Check Lifecycle/Orchestration: agent loop, state management, retry logic, recovery
5. Check Observability: logging, tracing, metrics, execution traces — run `/deep-review-codebase`
6. Check Verification: test harness, requirement checks, output validation — run `/deep-validate`
7. Check Governance: permissions, access control, audit trail, intervention recording

### 2. Optimize Tool Interface

> Goal: Optimize Tool Interface

Improve tool interfaces for efficiency

1. Check that tools have clear input/output schemas; use `Zod` for validation
2. Check that tools have no overlapping functionality
3. Check that tool descriptions are clear, unambiguous, and sufficient for the model to select them correctly
4. Check that tools return concise data without bloated output
5. Check tool error handling: structured error responses, no system-wide crashes
6. For an MCP server, follow the `mcp-builder` skill

### 3. Strengthen Lifecycle And Orchestration

> Goal: Strengthen Lifecycle And Orchestration

Improve the agent lifecycle and orchestration

1. Check the agent loop: clear termination conditions, no infinite loops
2. Check state management: state is persisted and restored correctly
3. Check retry logic: exponential backoff for transient failures
4. Check recovery: graceful degradation when a service is down
5. For multi-agent orchestration: check coordination, message passing, and error propagation

### 4. Improve Observability

> Goal: Improve Observability

Add observability for auditable execution

1. Record execution traces: action, tool call, context, verification, failure attribution
2. Use structured logging for every tool call and agent decision
3. Record interventions: when a human intervenes, log the context and reason
4. Check entropy: log unrelated changes the agent made beyond what was needed
5. Run `/deep-review-codebase` for comprehensive observability improvements

### 5. Implement Verification

> Goal: Implement Verification

Build a verification layer for verifiable execution

1. Define requirement checks for every task: what must pass
2. Build deterministic checks: test suite, type check, lint, build
3. Build behavioral checks: output format validation, schema compliance
4. Save verification results as structured reports
5. Run `/run-test` and `/deep-validate` for comprehensive verification

### 6. Apply Harness Ladder

> Goal: Apply Harness Ladder

Assess and improve the harness level along the H0-H3 ladder

1. H0 (Raw model): the model works alone with no runtime support — identify which level the project is at
2. H1 (Tool harness): the model has tools and file access — check tool quality
3. H2 (Context-memory harness): the model has context management and persistent memory — run `/follow-context-engineering`
4. H3 (Full harness): the model has verification, observability, governance — check every layer
5. Plan how to raise the current level to a higher one

### 7. Evaluate Harness Quality

> Goal: Evaluate Harness Quality

Evaluate harness quality through trace-based evaluation

1. Run the agent on a controlled task and record the execution trace
2. Analyze the trace: check actions, tool usage, context selection, verification
3. Identify execution-alignment failures: reasoning that does not match tool feedback or workspace state
4. Assess: completion rate, process quality, efficiency, failure behavior
5. Build an episode package: final artifact, execution trace, usage stats, validator output

## Rules

### 1. ETCLOVG Coverage

The harness must cover all 7 layers

- Execution environment: sandbox, runtime, isolation
- Tool interface: schemas, validation, token efficiency
- Context management: selection, compaction, memory
- Lifecycle/Orchestration: loop, state, retry, recovery
- Observability: logging, tracing, metrics
- Verification: requirement checks, output validation
- Governance: permissions, audit, intervention

### 2. Verifiable Execution

Every agent action must be verifiable

- Record an execution trace for every agent run
- Have deterministic checks for every task
- Record failure attribution when the agent fails
- Record interventions when a human steps in
- Build an episode package for audit

### 3. Tool Quality

Tools must be high quality

- Have `Zod` schemas for input/output validation
- No overlapping functionality
- Clear descriptions, sufficient for the model to select correctly
- Return concise data, no bloat
- Structured error handling, no system-wide crashes

### 4. Model-Harness Separation

Separate model capability from harness capability

- Evaluate performance at the model-harness configuration level, not the model alone
- Harness-only gains often have more impact than model gains
- Improve the harness before switching models
- Record the harness configuration for reproducibility

### 5. Safety And Governance

The harness must have safety measures

- Have permissions for every tool action
- Record an audit trail for every action
- Have a kill switch to stop the agent
- Limit resource usage (tokens, time, file access)
- Have human-in-the-loop for high-risk actions

## Expected Outcome

- The harness fully covers all 7 ETCLOVG layers
- Tool interfaces are high quality, non-redundant, and validated
- Execution traces are recorded for audit
- Verification is complete: deterministic + behavioral checks
- The harness level is assessed and upgraded
- Agent reliability improves from harness improvements, not the model alone
