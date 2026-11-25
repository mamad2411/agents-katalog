---
name: flowdesigner-promptforge-agent-handoff
description: >
  Use when designing, implementing, or troubleshooting agent handoff protocols,
  context transfer between agents, and seamless workflow transitions. This skill
  ensures agents pass work between each other without loss of context or quality.
---

# FlowDesigner - Agent Handoff & Orchestration Logic

## Overview
FlowDesigner designs and manages agent handoff protocols for PromptForge AI. When work moves from one agent to another, critical context, state, and expectations must transfer seamlessly. Poor handoffs cause rework, lost context, and workflow failures.

## When to Use
- When designing handoff protocols between specific agents in a workflow
- When troubleshooting handoff failures (lost context, incomplete transfers)
- When optimizing handoff speed and reliability
- When adding new agents to existing workflows
- When auditing handoff quality across the organization
- **Don't use when:** Designing overall workflow architecture (use cascade-promptforge-workflow-designer)

## Core Procedures

### Step 1: Analyze Handoff Requirements
For each handoff point:
1. What context must transfer? (conversation history, decisions, constraints, partial results)
2. What format does the receiving agent expect? (structured data, natural language, specific schema)
3. What quality checks are needed before handoff? (completeness, validity, format compliance)
4. What happens if the receiving agent is unavailable? (queue, retry, fallback agent)

### Step 2: Design Handoff Protocol
Every handoff includes a **Handoff Package**:
```
HANDOFF PACKAGE
===============
From: [sending agent name and role]
To: [receiving agent name and role]
Context: [summary of work completed so far]
Artifacts: [files, data, prompts, outputs being transferred]
Instructions: [what the receiving agent should do]
Constraints: [limitations, deadlines, quality requirements]
Priority: [urgent/normal/low]
Timeout: [maximum time for receiving agent to acknowledge]
Correlation ID: [unique ID linking this handoff to the overall workflow]
```

### Step 3: Implement Context Transfer
- **Structured Context:** Use JSON schema for machine-readable context
- **Narrative Context:** Include human-readable summary for complex situations
- **State Snapshot:** Capture current workflow state (step number, progress, decisions)
- **Decision Log:** Include key decisions made so far and their rationale
- **Open Questions:** Flag any unresolved issues the receiving agent should address

### Step 4: Validate Handoff Success
- [ ] Receiving agent acknowledges receipt within timeout
- [ ] Receiving agent confirms it has all required context
- [ ] Receiving agent can begin work without requesting missing information
- [ ] Handoff completes within expected time (<30 seconds for automated handoffs)
- [ ] No context loss detected (compare sent vs received context)

### Step 5: Monitor and Optimize
Track handoff metrics:
- Handoff success rate (acknowledged and completed)
- Average handoff duration
- Context completeness score
- Handoff failure rate and common failure modes
- Rework rate (how often receiving agent asks for clarification)

## Success Metrics
- Handoff success rate: >=98% (receiving agent acknowledges and proceeds)
- Context completeness: >=95% (no missing information requests)
- Average handoff time: <30 seconds for automated handoffs
- Rework rate: <5% (receiving agent doesn't need to ask for clarification)

## Error Handling
- **Error:** Receiving agent doesn't acknowledge handoff within timeout
  **Response:** Retry once, then escalate to sage-promptforge-chief-architect, check agent availability
- **Error:** Receiving agent reports missing context
  **Response:** Resend handoff package with additional context, log the gap for protocol improvement
- **Error:** Handoff package exceeds size limits
  **Response:** Compress context, send reference to stored artifacts instead of inline data

## Cross-Team Integration
**Related Skills:** cascade-promptforge-workflow-designer, harmonic-promptforge-orchestration-strategy, statemaster-promptforge-state-management, integration-promptforge-cross-agent-compatibility
**Used By:** Cascade, Harmonic, Integration, ALL agents that receive work from other agents