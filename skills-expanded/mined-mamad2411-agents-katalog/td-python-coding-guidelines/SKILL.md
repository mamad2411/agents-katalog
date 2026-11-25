---
name: td-python-coding-guidelines
description: "Use when writing or reviewing Python code, fixing lint/docstring/import/naming/exception/type annotation issues, unifying team style, or migrating `.py` files toward Google style."
---

# Google Python Coding Guidelines (Google PyGuide)

Aligned with the official document: <https://google.github.io/styleguide/pyguide.html>.

Coverage: section 2 language rules (2.1-2.21) and section 3 style rules (3.1-3.19).

## Reference Files

| File | Scope | When To Load |
| --- | --- | --- |
| `references/language-rules.md` | Section 2.1-2.21 language-level rules: lint, imports, exceptions, default values, truthiness, decorators, threading, `__future__`, general type-annotation rules, and related topics. | Before writing or refactoring code. |
| `references/style-rules.md` | Section 3.1-3.18 style-level rules: semicolons, line length, whitespace, comments, docstrings, strings, logging, TODOs, import formatting, naming table, main, and function length. | When writing, formatting, or standardizing style. |
| `references/exceptions.md` | Deep dive for section 2.4: `assert` boundaries, custom exceptions, the two catch-all exceptions, exception chaining, `Raises:` constraints, and anti-patterns. | When handling exceptions or reviewing error paths. |
| `references/type-annotations.md` | Section 2.21 and 3.19.1-3.19.16 type annotation details: NoneType, TypeAlias, TypeVar, generics, `TYPE_CHECKING`, and related topics. | When annotating public APIs, refactoring types, or migrating typing usage. |
| `references/review-checklist.md` | A-N review checklist with an output template. | During code review. |

## Workflow

1. **Identify the task type**
   - Writing or refactoring code: read `style-rules.md` and `language-rules.md`.
   - Exception handling: read `exceptions.md`.
   - Type annotations or typing migration: read `type-annotations.md`.
   - Code review: use `review-checklist.md`.
   - Bulk style migration: handle imports, naming, and docstrings first; then exceptions and type annotations; then run lint and tests.

2. **Load references on demand**
   - Do not load everything at once. Choose the one or two files most relevant to the task.

3. **Implement changes or provide review comments**
   - Provide executable fixes, not just descriptions of problems.
   - If existing repository conventions conflict with PyGuide, follow the target repository convention and explicitly mention the difference.
   - In change or PR descriptions, tag each change with its topic, such as imports, naming, docstring, exceptions, typing, and so on.

4. **Keep output traceable**
   - Classify review comments as `Critical`, `Major`, or `Minor` by using the output template at the end of `review-checklist.md`.
   - In change summaries, state whether behavior changed. The default expectation is no behavior change.

## Constraints

- Prefer small, low-risk changes. Avoid unrelated refactors.
- Keep import, naming, docstring, exception, and type annotation styles consistent.
- When suppressing lint, explain why and keep the suppression as narrow as possible, such as a line-level or block-level `# pylint: disable=xxx`.
- Test modules may be lighter than production modules for docstrings and overridden method descriptions, but empty or uninformative comments are still forbidden.
- Public APIs must have type annotations. Nullable types must be explicit, such as `X | None`. Prefer `collections.abc.*` abstract containers.
- `Raises:` should list only exceptions that are part of the API contract. Do not list exceptions caused by API misuse.

## Quick Entry Points

- **Writing or changing code:** read `references/style-rules.md`, then `references/language-rules.md`.
- **Handling exceptions or reviewing error paths:** read `references/exceptions.md`.
- **Adding type annotations or migrating typing:** read `references/type-annotations.md`.
- **Code review:** use the A-N checklist in `references/review-checklist.md` and follow its output template.
- **Bulk style migration:** imports / naming / docstrings -> exceptions -> type annotations -> lint / tests.
