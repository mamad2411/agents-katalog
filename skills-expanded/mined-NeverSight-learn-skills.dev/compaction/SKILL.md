---
name: compaction
description: Compress phase outcomes into a dense, structured handoff brief that preserves decisions, risks, and next-step context without carrying the entire history forward.
---

# Compaction

Use this skill when a coordinator or support capability needs to condense a phase boundary into a smaller, structured brief for downstream phases or future iterations.

## Goals
- Preserve the concrete decisions and outcomes from a completed phase.
- Reduce context size without losing the important reasoning trail.
- Produce a compact handoff that downstream work can consume quickly.

## Required Inputs
- The completed phase artifact or artifacts
- The current workflow phase and next intended phase
- Relevant memory entries for the phase boundary
- Any open questions, risks, or unresolved constraints

## Required Outputs
- A dense structured brief for downstream use
- A list of preserved decisions and outcomes
- A list of remaining risks or follow-ups

## Procedure
1. Extract the concrete outcomes from the completed work.
2. Keep only the decisions, constraints, and evidence that matter for downstream work.
3. Separate verified facts from remaining uncertainty.
4. Record follow-up needs clearly and briefly.
5. Return a compact brief that can replace rereading the full history.

## Quality Bar
- The brief must be shorter than the source material.
- The brief must preserve the next-step context needed by downstream phases.
- The brief must not introduce new design or implementation decisions.
