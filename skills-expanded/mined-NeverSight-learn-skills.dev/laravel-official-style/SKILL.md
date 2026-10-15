---
name: laravel-official-style
description: Make Laravel code simpler, more idiomatic, and closer to official Laravel conventions while preserving behavior.
---

# Laravel Official Style Skill

Use this skill when simplifying, reviewing, or refactoring Laravel code.

## Goal

Make the code feel like idiomatic Laravel:

- Simple.
- Readable.
- Convention-driven.
- Easy to test.
- Not over-engineered.

## Refactoring rules

- Preserve behavior unless asked otherwise.
- Prefer built-in Laravel features.
- Remove unnecessary abstraction.
- Keep naming clear and domain-specific.
- Prefer expressive Eloquent relationships.
- Prefer Collection methods when they improve readability.
- Avoid introducing repositories, managers, traits, or base classes unless the project already uses them and they provide clear value.

## Common improvements

- Move validation from controllers to FormRequest when validation is large or reused.
- Move authorization to Policies.
- Replace duplicated query logic with local scopes when reused.
- Replace repeated transformation logic with API Resources when the project uses Resources.
- Use route model binding where appropriate.
- Use config values instead of hard-coded environment reads outside config files.
- Use Laravel helpers only when consistent with the project.

## Code smell checklist

- Fat controller.
- Repeated validation arrays.
- Manual authorization checks scattered across controllers.
- N+1 query risk.
- Raw SQL with interpolated variables.
- Large service method doing unrelated work.
- Duplicated magic strings.
- Feature test missing for changed HTTP behavior.

## Output expectations

When completing a task:

- Mention which Laravel conventions were applied.
- Mention whether behavior changed.
- Mention tests or checks run.
- Mention any follow-up migration, queue, cache, or config concern.
