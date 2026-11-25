---
name: engineer-architecture
description: Design the implementation for a work item, written to architecture.md
---

# Architecture Design

This skill designs the implementation approach for the work described in `context.md`, and writes it to `architecture.md`. It's the second of two steps — run `engineer-context` first if you haven't.

The user's request should name the work item as `<type>/<slug>` (e.g. `feat/csv-order-export`), matching the work item created by `engineer-context`. If they didn't state it clearly, ask before proceeding rather than guessing.

Work item folder: `.codex/work/<type>/<slug>/`, e.g. `.codex/work/feat/csv-order-export/`.

## Preparation

- Read `.codex/work/<type>/<slug>/context.md`. If it doesn't exist, stop and tell the human to run `engineer-context` for `<type>/<slug>` first — don't try to reconstruct it from scratch.
- If `.codex/work/<type>/<slug>/architecture.md` already exists, confirm with the human whether you're revising it before overwriting.

## Architecture

Given the understanding captured in `context.md`, design the implementation's architecture. The architecture artifact should map out what's being built: the modules, dependencies, conventions, technologies, constraints, assumptions, trade-offs, alternatives, and consequences.

This is where you bring your deepest thinking to bear on the best path to build this, while respecting the project's conventions and best practices.

Go through the relevant source code, understand its organization and purpose, and design an architecture that aligns with the project's conventions and best practices.

Guidance:
- Use file search/grep tools to locate specific files based on `context.md`, and read through relevant code in batches.
- Dig deep into similar features and conventions.
- Examine specific implementation details.
- Review the project's technical master docs to make sure this aligns with the technical vision.
- Use web search for best practices or library documentation when needed. Don't guess how a library works — look it up.

Your architecture artifact should cover:
- A high-level view of the system (before and after the change)
- Impacted components, their relationships and dependencies
- Conventions and best practices that will be kept or introduced
- External dependencies that will be used or need to be added
- Constraints and assumptions
- Trade-offs and alternatives
- Negative consequences (if any) of this design
- A list of the main files to be modified/created

Build a Mermaid diagram if it helps clarity.

### Domain model (DDD — only where the domain warrants it)

Include this only if the project already has an explicit domain model, or this feature touches business logic complex enough that naming things precisely actually prevents bugs. Skip it entirely for straightforward CRUD or infrastructure work — forcing it where the domain is simple just adds noise.

When it applies, cover:
- **Bounded context**: which part of the domain this belongs to, and where its boundaries are.
- **Ubiquitous language**: domain terms that could otherwise be ambiguous, with their precise meaning here.
- **Entities / aggregates / value objects**: what has identity and a lifecycle (entities, aggregates) versus what's just a described value (value objects).
- **Domain events** (if relevant): state changes this produces that other parts of the system might need to react to.

If at any point you have doubts or find something that contradicts `context.md`, ask the human for clarification.

Once you have a solid understanding, save it to `.codex/work/<type>/<slug>/architecture.md`.

---

## Cross-consistency check (mandatory)

**After creating `architecture.md`, run this check before asking the human for final approval.**

### Why this phase exists

Common problems this check prevents:
- `context.md` says "modify component X" but `architecture.md` says "delete component X"
- A business value is mentioned in one document but missing from the other
- Fields or flows differ between the two documents
- The technical approach violates the project's documented standards

### Consistency checklist

**1. Consistency between documents** — compare `context.md` and `architecture.md`:

| Item | Check |
|---|---|
| Core problem | Described the same way in both? |
| Files to modify | Identical or compatible lists? |
| Technical approach | Strategy, patterns, libraries aligned? |
| Business values | Any number, deadline, or rule consistent across both? |

**2. Compliance with the business spec** (if one exists for this feature):
- [ ] Every field/input mentioned in the spec appears in `architecture.md`
- [ ] Every flow/scenario in the spec is covered
- [ ] Numeric values (deadlines, limits, etc.) match the spec
- [ ] UI/feedback messages match the spec
- [ ] Validations and business rules match the spec

**3. Compliance with project standards** (if ADRs/conventions are documented):
- [ ] Naming follows the documented conventions?
- [ ] Architecture/folder structure follows the project's pattern?
- [ ] Types/schemas follow the project's pattern (shared vs. local)?
- [ ] Code patterns follow the documented conventions?

### Fixing inconsistencies

1. **Minor** (e.g. a value missing from one doc): fix the incomplete document, no need for user approval.
2. **Approach conflicts** (e.g. different strategies): determine which is correct based on the project's standards, update both documents to align, and tell the user what was corrected.
3. **Conflict with the business spec**: the business spec always wins — fix the technical documents to match it, and document any divergence found.

### Recording the check

Append to the end of `architecture.md`:

```markdown
---

## ✅ Consistency Check

**Date**: [YYYY-MM-DD]
**Status**: ✅ Approved / ⚠️ Corrected

### Checklist
- [x] context.md and architecture.md are consistent
- [x] Matches the business spec (if applicable)
- [x] Matches project standards/conventions (if documented)
- [x] Business values and rules verified

### Corrections applied (if any)
- [Describe what was fixed]

### Notes
[Any relevant observation]
```

---

Once `architecture.md` is finalized and the cross-consistency check has passed, ask the human to review it.

If the human agrees, tell them `engineer-plan` is the next step — provide the same `<type>/<slug>` again. Otherwise, keep iterating together until you get explicit approval to proceed.

⛔ **Don't proceed automatically. Wait for the human's explicit approval and for them to invoke `engineer-plan` manually. Don't run planning or implementation on your own.**
