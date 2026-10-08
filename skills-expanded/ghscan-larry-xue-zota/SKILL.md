---
name: tenets-lesson-plan
description: Defines design tenets for generating lesson plans in zota across setup and practice continuity. Use when creating or revising lesson plans that must align with target scenes, dynamic session language, and measurable progression.
advisors: []
---

# Tenets Lesson Plan

## Inputs expected
- learner setup outputs (portrait, plan, scenarios, topics)
- current progress and pending review state
- target scene requirements and timeline constraints
- teaching language for the current planning context

## Procedure
1. Anchor every lesson unit to one target scene outcome and one measurable success signal.
2. Sequence units from comprehension to production to pressure simulation.
3. Integrate retrieval and recycle loops using pending review signals.
4. Keep lesson objectives narrow enough for single-session completion.
5. Encode adaptive branches for confidence dips, repeated errors, and time constraints.
6. Validate that each unit supports self-correction behaviors before direct correction fallback.
7. Output a plan structure that downstream agents can execute without reinterpretation.

## Tool Policy
- Use setup artifacts as planning baseline and update with live progress evidence.
- Use tenets-practice to keep coaching behavior aligned with plan intent.
- Avoid external speculative tools unless core inputs are missing.

## Decision Gates
- If objective cannot be measured in-session, rewrite objective before planning.
- If timeline is short, prioritize mission-critical units tied to immediate scene performance.
- If progress data conflicts with setup assumptions, rebase difficulty and sequence.
- If self-correction path is missing in a unit, revise unit before finalizing plan.

## Guardrails
- Do not generate generic weekly templates detached from user context.
- Do not overpack units with multiple unrelated objectives.
- Do not hardcode one fixed language trajectory for all sessions.
- Do not rely on direct correction as the default learning mechanism.
- Do not publish plans with unclear execution handoff to setup or practice agents.
