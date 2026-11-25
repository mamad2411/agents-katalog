---
name: engineering-planning
description: Use before implementation, fix, refactor, tests, file creation, or project-structure changes to decide placement, reuse, ownership, and maintainable integration before editing.
source: agent-feed
trust: core
---

# Engineering Planning

## Required Use

Use this skill before any task that writes code, creates files, changes tests, moves project structure, introduces dependencies, or changes implementation behavior.

This skill exists to prevent "just add a file" work. The output must explain where the change belongs, what can be reused, and how the implementation will remain maintainable.

## Position In The Stack

This skill is the *pre-edit decision routine*. It sits between the
`.agents/rules/engineering-architecture.md` invariants (stable rule layer) and
the `.agents/skills/project-development/SKILL.md` task workflow (full
implementation flow). The Engineering Planning Card below is the per-task
working artefact; do not re-explain the rule layer's invariants inside it.

## Required Reading

1. `.agents/rules/outcome-boundary.md`
2. `.agents/rules/engineering-architecture.md`
3. `.agents/project/README.md`
4. `.agents/project/project-structure.md`
5. `.agents/project/architecture-boundaries.md`
6. `.agents/domain/contracts.md`
7. The nearest existing project unit that already owns related behavior, as evidenced by code, tests, docs, config, or generated assets.

## Workflow

Before editing:

1. Recover the current Task Brief and stop condition.
2. Use `.agents/rules/engineering-architecture.md` to infer the existing owner from repository evidence, not from fixed template categories.
3. Search existing code, tests, helpers, templates, scripts, docs, config, and generated assets for reusable behavior before creating anything new.
4. Decide whether the change should extend an existing owner, create a small new owner, or avoid code changes entirely.
5. Check whether the placement preserves project structure, source-of-truth ownership, public contracts, dependency direction, configuration boundaries, and generated-template boundaries.
6. Choose the smallest write set that can satisfy the result without scattering related behavior.
7. Decide the verification evidence before editing.

## Engineering Planning Card

For non-trivial implementation or fix work, keep this compact card in working notes or the user-facing plan:

```md
| Item | Decision |
| --- | --- |
| Owner | Smallest existing project unit that should own the change |
| Evidence | Files, calls, tests, docs, config, or generated assets proving the owner |
| Placement | Where the change belongs and why |
| Reuse | Existing code, helper, pattern, dependency, test, or doc to reuse |
| Dependency direction | Existing direction preserved or decision required |
| Abstraction level | Local code / helper / shared utility / public contract |
| Write set | Files/directories expected to change |
| Boundary | Public contract, config, template, adapter, security, or project boundary to preserve |
| Verification | Tests/checks that prove the result |
```

Skip the visible card only for tiny local edits where owner, reuse, placement, and verification are obvious.

## Guardrails

1. Do not create a new file until checking whether an existing owner should be extended.
2. Do not put reusable protocol behavior into project-specific docs.
3. Do not put project-specific constraints into reusable Agent Feed rules or skills.
4. Do not duplicate boundary-conversion behavior when a canonical source can generate or own it.
5. Do not introduce a helper, abstraction, dependency, or directory only to make the current patch look organized.
6. Do not assume a project architecture shape from this template; infer it from the repository being changed.
7. If placement, ownership, dependency direction, or abstraction level is unclear and the decision affects future maintenance, apply `.agents/rules/decision-gates.md` before editing.

## Output

After using this skill, the AI should be able to state:

1. Where the work belongs.
2. What existing behavior is reused.
3. Why the write set is maintainable.
4. What verification proves the integration.
