---
name: refine-ideas
description: Use when capturing raw ideas and iteratively refining them through structured challenge loops and targeted topic learning before committing to implementation.
---

# Refine Ideas

## Specialization

Turn an early idea into a refined, decision-ready concept by combining structured idea capture, topic learning, and disciplined challenge rounds.

## Supporting Activities

- Run assumption pressure tests, trade-off challenges, and decision-quality checks.
- Perform depth-calibrated topic learning with source-backed context.
- Validate high-impact claims with external evidence before final recommendation.

## Trigger Conditions

- You have a rough concept and need to shape it before planning or implementation.
- You want explicit back-and-forth traceability for how the idea evolved.
- You need to learn the domain while stress-testing the idea.
- You want a stop rule for when the idea is "good enough" to proceed.

## Output Contract

Always produce:
- Idea seed and success intent.
- Topic learning map summary (or links to existing map output).
- Challenge log with each round's question, response, tension, and revision.
- Refined idea statement and non-goals.
- Confidence score and unresolved risks.
- Clear next recommendation: proceed, research more, or discard.

Use `./references/idea-refinement-session-template.md` for the session artifact.

## Portability And Reuse

- Keep this skill project-agnostic; do not assume a specific repository structure.
- Store the session artifact where the host project keeps planning or discovery records.
- If the host project has governance lanes, map outputs to its canonical planning/research location.
- Reuse the same challenge loop and decision criteria even when output paths differ.

## Workflow

1. Capture the raw idea in one paragraph plus constraints and desired outcome.
2. Select learning depth (`L1` to `L4`) and build domain grounding from authoritative sources.
3. Run iterative challenge rounds one focused question at a time.
4. After each round, update the challenge log with:
   - challenge question
   - current answer
   - exposed risk or contradiction
   - idea revision
   - confidence delta
5. Repeat until one of these stop conditions is met:
   - no high-severity contradictions remain
   - top risks have concrete mitigations or explicit assumptions
   - additional rounds are producing low-value churn
6. Produce the refined idea package with go/no-go recommendation.

## Challenge Dimensions

Use these dimensions each cycle (rotate as needed):
- Problem clarity: Is the problem real, costly, and frequent enough?
- User value: Who benefits, and how measurable is the benefit?
- Feasibility: Can this be delivered with available skills, time, and constraints?
- Differentiation: Why this approach over simpler alternatives?
- Risks: What could fail technically, operationally, or adoption-wise?
- Evidence: What assumptions are still unverified?

## Done Criteria

This skill is complete when the user has a refined idea with a traceable reasoning log, explicit assumptions, and a clear next-step decision.

## Inputs

- User request context and target scope for this skill invocation.

## Required Outputs

- A concrete, project-applicable result aligned with this skill purpose.
