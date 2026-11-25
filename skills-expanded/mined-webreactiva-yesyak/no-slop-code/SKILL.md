---
name: no-slop-code
description: Anti-slop convention for code, tests, docs and user-facing text. No comments that restate the code, no defensive checks out of place, no orphan or dead code, no speculative abstractions, no loose casts, no claims the code does not fulfil, no filler. Use it whenever you write or edit code, tests, templates or documentation, whenever you review generated code, and whenever the user mentions slop, redundant comments, unnecessary checks, clean code, over-engineering or "keep it lean".
---

# No slop code

If AGENTS.md sets a different convention for this topic, follow AGENTS.md.

## Code

| Slop | Do instead |
| --- | --- |
| A comment that repeats what the next line does | Delete it. Rename the variable or extract a function so the code says it. |
| A comment that explains *why*, when the project forbids comments | Put the reason in the name, in a test name or in an ADR. |
| A check for a case that cannot happen here (`if (!db) throw` right after creating `db`) | Delete it. Trust types and invariants. Validate only at boundaries: user input, files, network, environment. |
| A missing check at a real boundary (form body, query string, route params, env vars, a file or database that must exist) | Add a schema or a parser at the boundary, with a test for bad input. Fail fast when a required resource is missing; do not create an empty one in silence. |
| A function, dependency, export, template or table that nothing uses | Delete it, or add it in the same step as its first caller. |
| An abstraction for one caller "in case we need it later" | Inline it. Extract when the second caller appears. |
| A cast or a suppression (`as T`, `(T)x`, `@ts-ignore`, `# type: ignore`) to silence the checker | Narrow with a type guard, or fix the type at its source. |
| The same lookup or business rule copied into several handlers or layers | Extract one helper when you add the second copy. If two layers must both apply a rule, test it in both. |
| Catch-all error handling that hides the cause | Handle the errors you expect. Let the rest reach the error handler and the log. |

## Tests

- A test must fail when the behavior breaks. For each fix, check that the new test fails without the fix.
- Test helpers must behave like the real client. A helper that keeps stale state or skips a step can make tests pass for the wrong reason.
- Do not assert on incidental details (a hard-coded id that depends on seed size) when you can compute them.
- Security controls need at least one test that plays the attacker, not only the expected path.
- Check untrusted values (headers, form fields) against an allow-list. A deny-list lets every unexpected value through: casing, repeated headers, unknown values.

## Text

- User-facing messages must be true. Do not promise an effect (logged, sent, saved) that the code does not produce. Messages with a count must read well with 0, 1 and many ("1 orders" is a bug). Use a singular and a plural form, or a label such as `Deleted: 1`.
- Keep docs in sync in the same commit: README, AGENTS.md, spec, plan, environment variable tables.
- A spec or a plan that is longer than the code it describes is suspect. Cut repeated tables, restated decisions and text that a reader can get from the code or another document.

## Before you commit

Read the diff once with these questions:

1. Can I delete a line and lose nothing? Delete it.
2. Does every new symbol have a caller in this commit?
3. Is every check at a boundary, and every boundary checked?
4. Does any text promise something the code does not do?
