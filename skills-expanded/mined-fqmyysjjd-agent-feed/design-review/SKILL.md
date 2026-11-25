---
name: design-review
description: Use when reviewing design documents, architecture plans, implementation routes, gap analyses, README, AGENTS, rules, domain docs, or skills.
source: agent-feed
trust: core
---

# Design Review Skill

## Required Use

Use this skill after drafting or updating any design, protocol, planning, README, AGENTS, skill, rule, domain, or handoff-document change.

## Required Reading

1. `.agents/rules/outcome-boundary.md`
2. `.agents/domain/README.md`
3. `.agents/rules/context-loading.md`
4. `.agents/project/architecture-boundaries.md`
5. `.agents/rules/development-workflow.md`
6. `.agents/rules/review-gates.md`
7. `.agents/rules/evidence-gates.md` if external research is used.
8. The document being reviewed.

## Core Rule

Do not silently complete unresolved design gaps.

The review's highest-priority question is:

Can the next development step proceed from this design without inventing missing decisions?

Before judging readiness, verify result fit:

1. The document addresses the user's stated or clearly inferred goal, not just the visible artifact format.
2. The document explains the real problem, outcome, or workflow it claims to support.
3. Any missing decision, evidence, boundary, or user assumption that could change the result is called out as a gap.
4. The document does not hide weak support behind polished wording, broad framing, or generic best practices.
5. The proposed next action would actually move the user toward the intended result.

If yes, state that the design is ready for the next development step and stop.

If no, identify the blocking gaps. Close a gap directly only when all of these are true:

1. The answer is already supported by existing source-of-truth files.
2. The change stays inside the current Task Brief.
3. The change does not alter public behavior, CLI/API contracts, architecture ownership, adapter behavior, verification gates, source-of-truth boundaries, persistence, security, release scope, or product positioning.

When any condition is false, do not fill the gap yourself. Apply `.agents/rules/decision-gates.md` and ask for the required decision.

## Output

Return readiness judgment, current task boundary, findings or gaps, decision points requiring confirmation, safe next step, documents that should be updated, and whether the document can drive implementation.
