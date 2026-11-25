---
name: adhd-divergent-brainstorm
description: Spawn isolated parallel cognitive frames to prevent linear anchoring, bypass mental blocks, and prune low-value ideas.
category: productivity
aliases:
- divergent-thinking
- tree-of-thought
- non-linear-brainstorm
- parallel-ideation
triggers:
- divergent brainstorm
- tree of thought ideation
- bypass my mental block
- explore non-linear ideas
- ADHD brainstorming session
keywords:
- divergent
- brainstorm
- adhd
- tree-of-thought
- cognitive
- ideation
- mental-block
- parallel
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
lifecycle: enabled
capabilities:
- divergent-brainstorming
- tree-of-thought-exploration
- block-bypassing
inputs:
- problem
- domain
- constraints
outputs:
- divergent_branches
- pruned_options
- high_leverage_ideas
permissions:
  filesystem: none
  network: none
  shell: none
  secrets: none
author: Mr-Nobody-Anonymous
tags:
- adhd
- brainstorm
- divergent
- productivity
- tree-of-thought
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# ADHD Divergent Brainstorm

## Purpose
Fosters divergent thinking and Tree-of-Thought exploration by spawning multiple isolated, parallel cognitive frames. Bypasses linear anchoring and cognitive fixation while systematically pruning low-value branches.

## When to Use
- User feels stuck in an ideological rut or cannot see alternative solutions.
- Creative ideation phase of a new software feature, product, or architecture.
- When traditional linear brainstorming generates repetitive, conventional concepts.
- ADHD users seeking rapid novelty without getting lost in tangents.

## When NOT to Use
- During convergent execution where decisions are already finalized and implementation is underway.
- When an emergency bugfix requires an immediate, proven hotfix rather than novel experimentation.

## Capabilities
- **Parallel Framing**: Generate 3–5 radically distinct angles (e.g., minimalist, contrarian, brute-force, asynchronous).
- **Cognitive Decoupling**: Isolate each branch from early constraints to prevent premature filtering.
- **Automatic Pruning**: Score branches by novelty vs. feasibility and eliminate dead ends early.
- **Synthesis & Anchor Points**: Extract high-leverage insights into a structured decision matrix.

## Inputs
- `problem` (required) — Core question, goal, or creative challenge.
- `constraints` (optional) — Explicit technical, budget, or timeline limitations.
- `perspectives` (optional) — Custom lens or archetype to consider.

## Workflow
1. Frame the central problem in one neutral statement.
2. Spawn 3 divergent cognitive frames representing mutually distinct paradigms.
3. Explore 2–3 concrete implications under each isolated frame without cross-contamination.
4. Apply feasibility pruning to drop high-friction, low-payoff concepts.
5. Synthesize the top 2 highest-leverage ideas into actionable next steps.

## Tools
- Standard model reasoning capabilities; optional canvas or diagram tools when visualizing tree branches.

## Examples
- "I'm having a mental block on how to design this auth system; run a divergent brainstorm."
- "Give me non-linear ideas for reducing customer onboarding friction."
- "Bypass my mental block on this refactor with tree-of-thought ideation."

## Safety
- Keep ideation bounded to the stated domain.
- Do not propose solutions that compromise security, user privacy, or operational safety.

## Source
Custom skill maintained in this library adhering to cognitive workflow patterns.

## Notes
Can be chained with `productivity.adhd-task-breakdown` or `development.brainstorming` for turning divergent concepts into actionable development roadmaps.
