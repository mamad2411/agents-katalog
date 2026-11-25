---
name: investigator
description: Use this skill when the user asks to "analyze", "research", "how do I", or "what's the best way" to understand project context, impact of potential actions, and root causes of issues.
---

# Investigator Skill

## Overview
The Investigator skill is used to gather deep context and perform rigorous analysis before any action is taken. It ensures that the agent understands the current state of the project, the broader implications of any proposed changes, and the fundamental reasons for any issues.

## When to Use
You MUST use this skill when the user mentions:
- "analyze"
- "research"
- "how do I"
- "what's the best way"
- Any request requiring deep understanding of the project's current state or history.

## Instructions

This skill covers three distinct use cases. Identify which use case(s) apply to the current task and follow the corresponding parallel subagent workflow.

---

### Use Case 1: Context & History Analysis
Use when you need to understand the "What", "How", and "When" of the project environment.

#### Dispatch Parallel Investigation Subagents:
- **Subagent 1 (Structural Analysis)**: List files and analyze directory layout to identify the tech stack and organization.
- **Subagent 2 (Documentation Review)**: Read and summarize key files (`README.md`, `AGENT.md`, `CLAUDE.md`, etc.).
- **Subagent 3 (Temporal Context)**: Review recent activity (e.g., `git log -n 5`) to understand recent changes and project evolution.

#### Synthesize:
Combine the structural, documented, and historical findings into a unified context report.

---

### Use Case 2: Impact & Relationship Mapping
Use when you need to understand connections and predict the consequences of potential actions.

#### Dispatch Parallel Investigation Subagents:
- **Subagent 1 (Dependency Analysis)**: Map out how components (files, functions, data) are interconnected. Use search tools to find all references.
- **Subagent 2 (Constraint Mapping)**: Identify project rules, patterns, or architectural constraints that must be respected.
- **Subagent 3 (Downstream Prediction)**: Predict how a specific change might propagate through the system and affect unrelated parts.

#### Synthesize:
Provide a clear map of relationships and a "risk report" for any proposed actions.

---

### Use Case 3: Root Cause Investigation (Troubleshooting)
Use when an issue is reported and you need to find the "Why" behind the failure.

#### Dispatch Parallel Investigation Subagents:
- **Subagent 1 (Reproduction)**: Establish a consistent reproduction case (manual steps or a minimal failing test).
- **Subagent 2 (Trace Analysis)**: Examine logs, trace data flows, and analyze state transitions to locate the breakdown.
- **Subagent 3 (Interface Analysis)**: Investigate interactions between components and external systems to find boundary failures.

#### Synthesize:
Provide a definitive explanation of the root cause and the evidence supporting it. Do NOT make changes or propose fixes.

---

### Final Outcome
For any selected use case:
1. **Consolidate**: Combine all subagent reports into a cohesive analysis.
2. **Identify Gaps**: Highlight any missing information or contradictions.
3. **Report**: Deliver the findings as a purely analytical report. Do NOT modify the project or implement fixes.

## Examples

### Scenario: User asks "How do I add a new API endpoint?"
1. **Context:** Analyze `package.json` to see the framework (Express) and `README.md` for endpoint conventions.
2. **Mapping:** Search the codebase for existing endpoints to understand the routing structure and where middleware is applied.
3. **Report:** Present the current pattern and the files that would be impacted.

### Scenario: User says "Analyze why the build is failing"
1. **Selection**: Select **Use Case 3: Root Cause Investigation**.
2. **Investigation (Parallel)**:
   - **Subagent 1 (Log Capture)**: Reproduces the build failure and captures the error logs for later correlation.
   - **Subagent 2 (Regression Hunt)**: Simultaneously searches the git history and diffs for any changes to the build configuration or entry points in the last 24 hours.
   - **Subagent 3 (Environment Audit)**: Simultaneously checks local environment variables, Node.js/Python versions, and global dependencies against the project's requirements.
3. **Synthesis**: Correlates Subagent 1's crash log (pointing to a missing secret) with Subagent 3's finding that the local `.env` is out of sync with the new requirements identified by Subagent 2.
