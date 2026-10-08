---
name: guidance-promoter
description: Use when user corrections, repeated AI failures, or session-state conclusions should be promoted into stable AI development guidance.
source: agent-feed
trust: core
---

# Guidance Promoter

Use this skill to turn user corrections and repeated AI development failures into stable project guidance.

## Required Use

Use this skill when:

1. The user corrects how the AI should work in this repository.
2. The user says a rule, workflow, or conclusion should be remembered.
3. A repeated failure appears across multiple turns.
4. Session-state carry-forwards become stable enough to promote.
5. The user asks to improve `.agents`, AGENTS, rules, skills, or development protocol docs.

## Workflow

1. Identify what the user corrected, requested to remember, or showed through repeated failure.
2. State the AI failure, missing source-of-truth, unclear trigger, or workflow gap it reveals.
3. Decide whether the conclusion is durable guidance or only session-local state.
4. Check existing rules, project/domain indexes, skills, README, and session-state before creating a new asset.
5. Choose the owning asset:
   - `.agents/rules/`: reusable invariant, gate, or protocol constraint.
   - `.agents/project/`: repository-specific engineering constraint, source layout, verification, release, security, dependency, or delivery boundary.
   - `.agents/domain/`: stable project concepts, contracts, business rules, source-of-truth ownership, or durable domain facts.
   - `.agents/skills/`: repeatable task method with clear triggers and workflow steps.
   - `.agents/session-state/<session_id>.json`: active handoff fact that is useful now but not stable enough to promote.
   - `README.md` or `docs/`: user-facing capability, setup, command, or protocol explanation.
6. Propose the target asset and exact change. Ask for confirmation when `.agents/rules/decision-gates.md` says the change affects future development results, source-of-truth ownership, public behavior, protocol rules, verification, release, or product scope.
7. If the target is `.agents/skills/`, use `.agents/skills/skill-maintainer/SKILL.md`.
8. If the target is `.agents/project/` or `.agents/domain/`, update the corresponding README recall index with owned boundary, read trigger, and evidence expectation.
9. If the change is still session-local, update `.agents/session-state/<session_id>.json` instead of stable docs.
10. Run the relevant design review and verification gates before final handoff.

## Guardrails

1. Do not promote a one-off preference into reusable rules.
2. Do not put project-specific facts into generic Agent Feed rules.
3. Do not put reusable AI workflow gates into `.agents/project/` or `.agents/domain/`.
4. Do not silently write durable guidance when the user only asked for read-only analysis.
5. Do not preserve a user correction as transcript text; extract the repeatable rule, trigger, or source-of-truth boundary.
6. When the correction reveals an external/custom skill gap, route through `.agents/skills/specialist-router/SKILL.md` or `.agents/skills/skill-maintainer/SKILL.md` instead of making the external skill authoritative.

## Output

When proposing or applying a promotion, report:

1. User feedback or repeated failure.
2. Stable conclusion.
3. Target asset.
4. Why that asset owns it.
5. Index or mirror updates required.
6. Verification command.
