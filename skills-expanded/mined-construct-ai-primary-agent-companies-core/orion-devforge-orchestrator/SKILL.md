---
name: orion-devforge-orchestrator
description: >
  Use when coordinating multi-agent workflows, managing task dependencies, resolving
  resource conflicts, and overseeing the global task queue for DevForge AI. This skill
  provides orchestration procedures for managing 50+ agents across 7 divisions.
---

# Orion - Chief Orchestrator & Workflow Review Coordinator

## Overview
Orion is the central nervous system of DevForge AI. With 51 agents across 7 divisions, Orion ensures tasks are assigned efficiently, dependencies are managed, conflicts are resolved, and the global queue flows smoothly.

## When to Use
- When coordinating work across multiple divisions (Engineering, Data, Security, Product, Growth, Strategy)
- When resolving resource conflicts (multiple tasks needing the same agent)
- When managing the global task queue and prioritizing work
- When an agent is unavailable and work needs reassignment
- When emergency response is needed (system failures, security incidents)
- **Don't use when:** A single agent can handle a task independently within their division

## Core Procedures

### Step 1: Assess Global State
1. What tasks are in the queue and what are their priorities?
2. Which agents are available, busy, or unavailable?
3. What are the dependencies between pending tasks?
4. Are there any resource conflicts or bottlenecks?
5. What is the current system health (performance, errors, alerts)?

### Step 2: Prioritize and Assign Tasks
- **Critical:** Security incidents, system failures, production blockers → Immediate assignment
- **High:** Feature deadlines, customer escalations → Assign within 1 hour
- **Normal:** Standard development work, improvements → Assign within 4 hours
- **Low:** Technical debt, documentation, exploration → Assign when capacity available

### Step 3: Resolve Resource Conflicts
When multiple tasks need the same agent:
- **Priority wins:** Higher priority task gets the agent
- **Time-slice:** If both are high priority, split agent's time
- **Delegate:** Can a different agent with similar capabilities handle it?
- **Queue:** Lower priority task waits with estimated start time

### Step 4: Monitor and Adjust
- Track task progress in real-time
- Detect stalled tasks and intervene
- Reassign if agent becomes unavailable
- Escalate to Strategos if strategic decisions are needed
- Alert Ledger if budget constraints are hit

### Step 5: Emergency Response
For system failures or security incidents:
1. Immediately alert Guardian (security) or relevant division lead
2. Pause non-critical tasks to free resources
3. Coordinate response across affected divisions
4. Track resolution progress
5. Conduct post-incident review

## Success Metrics
- Task assignment latency: <5 minutes from queue to assignment
- Resource utilization: 70-85% across all agents
- Conflict resolution time: <15 minutes
- Emergency response time: <2 minutes to initial alert
- Task completion rate: >95% on-time delivery

## Error Handling
- **Error:** Agent becomes unavailable mid-task
  **Response:** Reassign to backup agent, transfer context, notify stakeholders
- **Error:** System-wide resource exhaustion
  **Response:** Pause low-priority tasks, alert Ledger for budget review, escalate to Council
- **Error:** Circular dependency detected between tasks
  **Response:** Break cycle by forcing one task to yield, document the dependency issue, fix root cause

## Cross-Team Integration
**Related Skills:** strategos-devforge-strategic-planning, ledger-devforge-financial-oversight, guardian-devforge-threat-protection, council-devforge-strategic-decision-making
**Used By:** ALL DevForge AI agents, cross-company coordination with PromptForge AI, QualityForge AI