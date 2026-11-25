---
name: brainstorming
description: For Heavy-tier tasks only — turn ideas into specs through one-question-at-a-time dialogue, present design in sections, write spec doc, hand off to planning skill
---

# brainstorming

## When to use

The router invokes this skill ONLY for Heavy-tier tasks (multi-component, unclear scope, new subsystem, or user explicitly requests design/plan/architecture).

For Standard or Quick tier, skip brainstorming entirely — go straight to `Skill(imlazy-planning)` in light mode or inline execution.

This skill's job: produce a spec doc that `Skill(imlazy-planning)` can turn into an implementation plan.

## Process

1. **Explore project context** — read existing files, check recent commits before asking any questions.
2. **Ask clarifying questions one at a time.** Prefer multiple-choice. One question per message. Focus on: purpose, constraints, success criteria.
3. **Assess scope first.** If the request describes multiple independent subsystems, flag this and help the user decompose into sub-projects before proceeding. Each sub-project gets its own spec → plan → implementation cycle.
4. **Propose 2-3 approaches** with tradeoffs and your recommendation. Lead with the recommended option.
5. **Present the design in sections.** Get user approval section by section. Cover: architecture, components, data flow, error handling, testing.
6. **Write the spec** to `docs/imlazy/specs/YYYY-MM-DD-<topic>-design.md`. Self-review for placeholders, contradictions, scope, and ambiguity. Fix inline.
7. **Ask the user to review the spec** before proceeding.
8. **Hand off** to `Skill(imlazy-planning)` in full mode. Do not invoke any other skill.

## Key principles

- One question at a time. Multiple-choice preferred over open-ended.
- YAGNI ruthlessly — cut unrequested features from the design.
- Always propose 2-3 approaches before settling.
- Explore the existing codebase before proposing changes. Follow existing patterns. Targeted improvements to broken code you are touching are fine; unrelated refactoring is not.
- Be flexible — go back and clarify when something does not make sense.

## Spec self-review checklist

Before asking the user to review, check:
1. Placeholder scan — any TBD/TODO/incomplete sections?
2. Internal consistency — do sections contradict each other?
3. Scope check — focused enough for one implementation plan?
4. Ambiguity check — can any requirement be interpreted two ways?

Fix issues inline. No need to re-review.

## Hand-off

After the user approves the spec, invoke `Skill(imlazy-planning)` in full mode. Do not invoke any other skill — `imlazy-planning` is the terminal state for this skill.
