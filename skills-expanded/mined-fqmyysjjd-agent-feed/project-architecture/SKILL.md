---
name: project-architecture
description: Use at the start of every project session, after context compression, and before architecture, module, runtime, or requirement decisions.
source: agent-feed
trust: core
---

# Project Architecture Skill

## Required Use

Use this skill for **understanding** decisions: what the project is, why it exists, how modules connect, or where a responsibility belongs. It is a read-only orientation skill — its output is a written explanation, not edited code.

For tasks that *write or modify code* (implementation, refactor, fix, tests, project-structure edits), use `.agents/skills/project-development/SKILL.md` instead. That workflow already calls `engineering-architecture.md` and `engineering-planning` for ownership and placement decisions, so you do not need this skill before editing.

Use this skill when:

1. The user asks "what does this project do" / "how does X module work" / "where does Y belong" without asking for an edit.
2. A new architecture, module, runtime, or requirement decision is being proposed and needs orientation before going to `decision-gates.md`.
3. The session just started or context was compressed and the AI must rebuild a project model before routing to other skills.

## Required Reading

1. `.agents/rules/outcome-boundary.md`
2. `.agents/domain/README.md`
3. `.agents/domain/concepts.md`
4. `.agents/domain/contracts.md`
5. `.agents/domain/source-of-truth.md`
6. `.agents/project/architecture-boundaries.md`
7. `.agents/project/project-structure.md`

## Expected Outcome

After using this skill, you should be able to explain the project target, owner module, relevant contract source, and whether a proposed change is architecture, domain, implementation detail, or out of scope.
