---
name: harmonic-promptforge-orchestration-strategy
description: >
  Use when optimizing multi-agent coordination, resolving resource contention,
  balancing workloads across agents, and improving overall system orchestration
  efficiency. This skill provides strategic orchestration frameworks for peak
  multi-agent system performance.
---

# Harmonic - Orchestration Strategy & Multi-Agent Coordination

## Overview
Harmonic optimizes the orchestration strategy for PromptForge AI's multi-agent system. While Cascade designs individual workflows, Harmonic ensures the entire ecosystem of agents works together efficiently—balancing load, resolving conflicts, and maximizing throughput.

## When to Use
- When multiple workflows compete for the same agents (resource contention)
- When overall system throughput is declining or agents are overloaded
- When designing the strategic orchestration layer for new agent additions
- When analyzing system-wide performance bottlenecks
- When coordinating cross-company agent collaboration (PromptForge + DevForge + QualityForge)
- **Don't use when:** Designing a single workflow (use cascade-promptforge-workflow-designer)

## Core Procedures

### Step 1: Assess System State
1. What agents are currently active and what is their workload?
2. What workflows are running and what is their priority?
3. Are there resource conflicts? (multiple workflows needing the same agent)
4. What is the current system throughput and latency?
5. Are any agents idle that could be utilized?

### Step 2: Resolve Resource Contention
When multiple workflows need the same agent:
- **Priority-Based:** Higher priority workflow gets the agent first
- **Time-Slicing:** Agent alternates between workflows in short bursts
- **Queue-Based:** First-come-first-served with estimated wait times
- **Parallel Instances:** Spin up temporary agent instance if possible

### Step 3: Optimize Agent Allocation
- **Load Balancing:** Distribute work evenly across agents with similar capabilities
- **Specialization Routing:** Route work to the most specialized agent available
- **Batch Processing:** Group similar tasks for the same agent to reduce context switching
- **Predictive Scaling:** Anticipate demand spikes and pre-allocate agent capacity

### Step 4: Coordinate Cross-Company Orchestration
When workflows span multiple companies:
```
CROSS-COMPANY ORCHESTRATION
============================
Initiating Company: [PromptForge AI]
Partner Companies: [DevForge AI, QualityForge AI, etc.]
Shared Workflow: [name and purpose]
Agent Mapping: [which company provides which agent]
Handoff Protocol: [how work transfers between companies]
Quality Standards: [agreed quality thresholds]
Escalation Path: [who resolves cross-company issues]
```

### Step 5: Monitor and Tune
Track system-wide metrics:
- Overall system throughput (workflows completed per hour)
- Agent utilization rate (percentage of time agents are active)
- Average workflow wait time (time from request to start)
- Contention resolution time (how long to resolve conflicts)
- Cross-company handoff success rate

## Success Metrics
- System throughput: >=90% of theoretical maximum
- Agent utilization: 70-85% (not overloaded, not idle)
- Contention resolution time: <2 minutes
- Cross-company handoff success rate: >=95%
- Workflow wait time: <5 minutes for normal priority

## Error Handling
- **Error:** System-wide agent overload (all agents at 100% capacity)
  **Response:** Implement priority-based queuing, defer low-priority work, alert Sage
- **Error:** Cross-company handoff fails repeatedly
  **Response:** Escalate to both companies' CEOs, implement manual handoff as fallback
- **Error:** Orchestration logic creates deadlock (circular dependencies)
  **Response:** Detect circular wait, break cycle by forcing one workflow to yield, log for fix

## Cross-Team Integration
**Related Skills:** cascade-promptforge-workflow-designer, flowdesigner-promptforge-agent-handoff, collaborator-promptforge-cross-company-knowledge-sharing, integration-promptforge-cross-agent-compatibility
**Used By:** Sage, Cascade, FlowDesigner, Collaborator, Integration, CEO agents across companies