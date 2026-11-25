---
name: code-craft
description: Apply Jess's engineering conventions to architecture, boundary typing, error handling, and abstraction decisions.
user-invocable: true
argument-hint: "[rust|typescript|go|python] [target]"
---

# Code craft

Use the repository's current instructions and established conventions. Apply
these defaults where the requested change needs a design decision; they do not
authorize unrelated restructuring or new tooling.

Read the reference for the decision in scope:

| Decision | Reference |
| --- | --- |
| Represent states and domain identities | [Illegal states](principles/illegal-states.md) |
| Decode external input into useful types | [Parse, don't validate](principles/parse-dont-validate.md) |
| Model recoverable errors and required gates | [Errors as values](principles/errors-as-values.md) |
| Choose an abstraction or investigate performance | [Simplicity](principles/simplicity.md) |
| Maintain module boundaries and their documentation | [Architecture docs](principles/architecture-docs.md) |

Read a language reference only when its idioms, concurrency, or tooling details
matter: [TypeScript](languages/typescript.md), [Rust](languages/rust.md),
[Go](languages/go.md), or [Python](languages/python.md).

Use [testing-craft](../testing-craft/SKILL.md) for test-design decisions.
Repository setup belongs to [project-bootstrap](../project-bootstrap/SKILL.md)
when that setup is requested. Follow the project's required verification;
reviews do not automatically require a full test suite.

Adapted from `leonardomso/rust-skills` (MIT), Matklad's Rust100k series, and
Alexis King's writing on parsing and type safety.
