---
name: parallelism-aware-skill-step-design
description: "Design skill steps with explicit execution topology, asking which parts run directly, in subagents, in teammate swarms, or in parallel."
metadata:
  author: ychampion
---

# SKILL: Parallelism-Aware Skill Step Design
**Domain:** multi-agent  
**Trigger:** Use when converting a workflow into a skill and some steps may run in parallel, through task agents, through teammate swarms, or require human checkpoints.
**Source Pattern:** Distilled from reviewed multi-agent coordination and child-runtime patterns.

## Core Method
Model each major step not just by what it does, but by how it executes. During the interview, ask whether steps are independent, whether they should run directly or via agents, and whether any human confirmation is required before advancing. Then encode those answers into the saved skill so later agents know where concurrency is safe, where isolation is useful, and where execution must pause for a person.

## Key Rules
- Ask explicitly whether sibling steps can run in parallel before assuming a sequential workflow.
- Distinguish direct execution, task-agent execution, teammate-swarm execution, and human-owned steps in the final step design.
- Capture the artifacts that parallel steps must hand back before downstream steps can continue.
- Mark irreversible or judgment-heavy transitions with a human checkpoint even if surrounding steps are automated.
- Keep the execution annotations tied to concrete workflow behavior, not to abstract enthusiasm for subagents.

## Example Application
If a launch skill needs one branch to post release notes and another to monitor CI, mark those steps as parallel and note the artifacts they return. If the next step merges a release branch, add a human checkpoint before that merge even though earlier monitoring ran through subagents.

## Anti-Patterns (What NOT to do)
- Do not flatten every workflow into a purely sequential script when some steps are independent and could safely overlap.
- Do not label steps as agent-driven without defining what result they must return or when a person needs to intervene.
