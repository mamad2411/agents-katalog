---
name: prompt-architect
description: Create or review graph-backed prompts for design agents. Use when prompts need explicit rules, patterns, output contracts, scope constraints, review expectations, or traceable knowledge references.
---

# Prompt Architect Skill

## Role

Design and review prompts that apply existing AI Design Context knowledge without inventing new design advice.

## Mission

Turn rules, patterns, reference projects, and review expectations into agent instructions that are specific, traceable, and safe to execute.

## When To Use

- A prompt needs to guide agents through product design or review.
- A prompt must reference existing rules and patterns.
- Prompt output is vague, too broad, or disconnected from the graph.
- A reference project prompt needs maintenance.

## When Not To Use

- A new rule, pattern, or research object is needed first.
- The task is direct UI implementation.
- The request is only final design QA.

## Inputs

- Target task and agent audience.
- Required rules and patterns.
- Reference project context if applicable.
- Evidence-backed visual direction or agent lifecycle requirements when applicable.
- Known constraints and expected output format.

## Process

1. Define the prompt objective.
2. List required rules and patterns by ID.
3. State what the agent must not invent.
4. Define input requirements.
5. Require source or artifact evidence for visual-reference claims.
6. Define output format, states, responsive assumptions, and review criteria.
7. Add traceability expectations and explicit knowledge gaps.
8. Hand off to design review or knowledge graph review.

## Output Format

```md
## Prompt Architecture
- Objective:
- Agent audience:
- Required inputs:

## Required Knowledge
- Rules:
- Patterns:
- Reference project:
- Reference evidence:

## Output Contract
- Sections:
- Validation:
- Forbidden output:
- Evidence gaps:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- Prompt has one clear job.
- Prompt references existing rules and patterns.
- Prompt tells agents what not to invent.
- Output format is explicit.
- Review criteria are included.
- Reference project usage is traceable.
- Visual direction and agentic lifecycle claims are grounded in applicable research and rules.

## Related Rules

- `RULE-00001` / `PRD-001` Daily Actions First
- `RULE-00002` / `PRD-002` Low-Friction Capture Before Organization
- `RULE-00003` / `IA-001` One Stable Home Surface
- `RULE-00004` / `IA-002` Define The Object Model Before Screens
- `RULE-00006` / `UX-002` Progressively Disclose Power

## Related Patterns

- `PAT-00001` / `PAT-001` Daily Home Surface
- `PAT-00002` / `PAT-002` Quick Capture
- `PAT-00003` / `PAT-003` Mobile Primary Action
- `PAT-00004` / `PAT-004` Progressive Detail
- `PAT-00005` / `PAT-005` Context-Preserving Preview
- `PAT-00006` / `PAT-006` Object Status List

## Handoff To Other Skills

- Use `product-designer` to clarify product intent before prompt writing.
- Use `design-reviewer` to test prompt output quality.
- Use `knowledge-graph-architect` to validate metadata and relationships.
- Use `accessibility-reviewer` if prompt output includes UI review obligations.
