---
name: code-patterns
description: The bar for any code you write, edit, or review. Read these rules whenever you are writing or reading any code
---

**NON-NEGOTIABLE RULES**

- Favour clarity over cleverness; if a line needs a comment to be understood, rewrite it.
- Make the smallest change that fully solves the task — keep diffs focused and reviewable.
- No dead code: no commented-out blocks, unused or unreachable code, or stray debug/console statements.
- Don't repeat yourself — extract a reusable abstraction so a fix happens in one place, but don't over-abstract.
- Use guard clauses and early returns to flatten nesting and keep the happy path obvious.
- Fully implement what was asked: no TODOs, placeholders, or missing pieces, and verify it works before reporting it done.
- If the request conflicts with project conventions, flag it and propose the conformant alternative instead of silently breaking them.
- Give variables, functions, and types intention-revealing names; avoid generic ones like a, b, tmp, data.
- Keep functions small and focused — one thing, at one level of abstraction.
- Keep it simple (KISS/YAGNI): the simplest thing that works, built for the need the task actually has.
- **Default to ZERO comments**: write self-documenting code (intention-revealing names, small functions) so it needs no narration. Never add a comment that restates _what_ the code does. Add one ONLY for a non-obvious _why_ the code itself cannot carry — a workaround, a deliberate tradeoff, an edge-case reference - The code **SHOULD SPEAK** for itself.
- **Never transcribe requirements, specs, or docs into code comments.** Pasting functional requirements, acceptance criteria, ticket/spec prose, or a summary of a doc section into the source is _not_ a legitimate _why_ — it is the most expensive kind of stale comment. The spec and the project docs are the source of truth for _what_ was asked and _why it was asked_; code carries _how_. An inline copy of that prose silently rots the moment the spec changes, moves, or is deleted, and then actively misleads the next reader. If a line genuinely needs traceability, point to the spec with a short stable id (the change/ticket slug), never a paragraph of restated requirement. A non-obvious _why the code is shaped this way_ still earns its one short comment; a requirement narration never does.
- Leave each file cleaner than you found it, and write testable code backed by automated tests so it can be refactored without fear.

Apply SOLID with judgment, especially in OO designs: single responsibility (one reason to change), open/closed (extend with new code rather than editing working code — but prefer reusing or extending an existing shared component/module over building a fresh one; "new code" means a new extension point, not a duplicate of something the project already ships), Liskov substitution (subtypes substitute cleanly), interface segregation (small focused interfaces), dependency inversion (depend on abstractions, inject dependencies).
