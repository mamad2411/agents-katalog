---
name: clean-code-standards
description: Apply pragmatic clean-code standards — DRY, YAGNI, KISS, separation of concerns, naming, small functions, low complexity. Use when writing or reviewing code to keep it readable and maintainable. Cited by the implementer, QA, and code reviewer as a shared rubric.
---

# Clean Code Standards

- **DRY** — remove duplicated knowledge; extract a single source of truth. But don't over-abstract incidental similarity.
- **YAGNI** — build what the requirement needs now, not speculative generality. Delete unused options/flags.
- **KISS** — prefer the simplest design that works; complexity must earn its place.
- **Separation of concerns** — I/O, business logic, and presentation in distinct units.
- **Naming** — intention-revealing; no abbreviations that need a decoder; verbs for functions, nouns for values.
- **Functions** — small, one level of abstraction, few parameters; prefer pure where possible.
- **Complexity** — guard against deep nesting; early-return; cap cyclomatic complexity.
- **Comments** — explain *why*, not *what*; delete commented-out code.

## Review heuristics
Flag duplicated knowledge, speculative generality, names that mislead, functions doing >1 thing, nesting >3 deep. Cite file:line and the standard. Prefer concrete refactors over vague "make it cleaner".
