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

## Required Reading

1. `.agents/rules/outcome-boundary.md`
2. `.agents/project/README.md`
3. `.agents/project/project-structure.md`
4. `.agents/project/architecture-boundaries.md`
5. `.agents/domain/contracts.md`
6. The nearest existing module, helper, adapter, command, test, or document that already owns related behavior.

## Workflow

Before editing:

1. Recover the current Task Brief and stop condition.
2. Identify the owning layer: rule, skill, project constraint, domain knowledge, source module, script, adapter, test, or documentation.
3. Search existing code, tests, helpers, templates, scripts, and docs for reusable behavior before creating anything new.
4. Decide whether the change should extend an existing owner, create a small new owner, or avoid code changes entirely.
5. Check whether the placement preserves project structure, source-of-truth ownership, public contracts, configuration boundaries, and generated-template boundaries.
6. Choose the smallest write set that can satisfy the result without scattering related behavior.
7. Decide the verification evidence before editing.

## Engineering Planning Card

For non-trivial implementation or fix work, keep this compact card in working notes or the user-facing plan:

```md
| Item | Decision |
| --- | --- |
| Owner | Existing module/file/layer that should own the change |
| Reuse | Existing code, helper, pattern, test, or doc to reuse |
| Placement | Where the change belongs and why |
| Write set | Files/directories expected to change |
| Boundary | Public contract, config, template, adapter, security, or project boundary to preserve |
| Verification | Tests/checks that prove the result |
```

Skip the visible card only for tiny local edits where owner, reuse, placement, and verification are obvious.

## Guardrails

1. Do not create a new file until checking whether an existing owner should be extended.
2. Do not put reusable protocol behavior into project-specific docs.
3. Do not put project-specific constraints into reusable Agent Feed rules or skills.
4. Do not duplicate adapter-specific behavior when a canonical source can generate it.
5. Do not introduce a helper, abstraction, dependency, or directory only to make the current patch look organized.
6. If placement or ownership is unclear and the decision affects future maintenance, apply `.agents/rules/decision-gates.md` before editing.

## Output

After using this skill, the AI should be able to state:

1. Where the work belongs.
2. What existing behavior is reused.
3. Why the write set is maintainable.
4. What verification proves the integration.
