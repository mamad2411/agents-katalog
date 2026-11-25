---
name: cascade-promptforge-workflow-designer
description: >
  Use when designing, implementing, or optimizing multi-agent workflows, agent
  coordination patterns, and complex prompt chains. This skill provides structured
  procedures for building workflows that are reliable, observable, and recoverable.
---

# Cascade - Multi-Agent Workflow Designer

## Overview
Cascade designs multi-agent workflows for PromptForge AI. Complex prompt engineering tasks require coordinated sequences of agents, each contributing specialized work. Cascade ensures workflows are well-structured, handle failures gracefully, and produce consistent results.

## When to Use
- When a task requires multiple agents working in sequence or parallel
- When designing agent handoff patterns for complex prompt pipelines
- When optimizing existing workflows for speed, cost, or quality
- When adding error recovery and retry logic to workflows
- When debugging workflow failures or bottlenecks
- **Don't use when:** A single agent can complete the task independently

## Core Procedures

### Step 1: Analyze Workflow Requirements
1. What is the end goal? (specific deliverable or outcome)
2. What are the input artifacts? (prompts, data, context, constraints)
3. What specialized capabilities are needed? (research, analysis, generation, validation)
4. What are the dependencies between steps? (sequential, parallel, conditional)
5. What are the quality gates? (validation criteria at each stage)

### Step 2: Design Workflow Architecture
Choose the appropriate workflow pattern:

**SEQUENTIAL:** Agent A → Agent B → Agent C
- Use when: Each step depends on the previous step's output
- Example: Research → Analysis → Report Generation

**PARALLEL:** Agent A ─┐
                      ├→ Merge Agent
           Agent B ─┘
- Use when: Independent tasks can run simultaneously
- Example: Code review + Security review → Combined feedback

**CONDITIONAL:** Agent A → [if pass] → Agent B
                          → [if fail] → Agent C (fix)
- Use when: Next step depends on evaluation of current step
- Example: Generate → Validate → [if valid] Deliver / [if invalid] Refine

**ITERATIVE:** Agent A → Agent B → [loop back to A if needed]
- Use when: Refinement cycles are needed until quality threshold met
- Example: Draft → Review → Refine → Review → ... → Approved

### Step 3: Define Agent Roles and Handoffs
For each agent in the workflow:
```
WORKFLOW STEP
=============
Step Number: [order in workflow]
Agent: [which agent performs this step]
Input: [what this agent receives from previous step]
Task: [what this agent does]
Output: [what this agent produces]
Quality Gate: [criteria for pass/fail]
Timeout: [maximum time for this step]
Retry Policy: [what happens on failure]
```

### Step 4: Implement Error Recovery
- **Retry Logic:** How many retries before escalation? (default: 3)
- **Fallback Path:** What happens if an agent is unavailable?
- **Partial Recovery:** Can workflow continue from last successful step?
- **Escalation:** When does the workflow escalate to sage-promptforge-chief-architect?
- **Circuit Breaker:** When does the workflow abort entirely? (e.g., 5 consecutive failures)

### Step 5: Test and Validate Workflow
- [ ] Run workflow end-to-end with typical input
- [ ] Run workflow with edge case inputs
- [ ] Simulate agent failures to test recovery paths
- [ ] Measure total workflow duration and cost
- [ ] Verify output quality meets standards
- [ ] Document workflow diagram and runbook

## Success Metrics
- Workflow completion rate: >=95% (without manual intervention)
- Average workflow duration: <30 minutes for standard workflows
- Error recovery success rate: >=90% (retries succeed)
- Output quality: >=95% pass rate on quality gates

## Error Handling
- **Error:** Agent in workflow is unavailable or times out
  **Response:** Retry up to 3 times with exponential backoff, then escalate to Sage
- **Error:** Workflow produces low-quality output at quality gate
  **Response:** Route to refinement agent (Refiner), re-run quality gate
- **Error:** Workflow enters infinite loop (iterative pattern)
  **Response:** Enforce maximum iteration count (default: 5), abort and escalate

## Cross-Team Integration
**Related Skills:** flowdesigner-promptforge-agent-handoff, harmonic-promptforge-orchestration-strategy, statemaster-promptforge-state-management, validator-promptforge-syntax-logic-validation
**Used By:** Sage, FlowDesigner, Harmonic, Integration agents