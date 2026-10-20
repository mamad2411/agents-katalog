---
name: to-specs
description: Turn requirements or conversation context into a structured spec. Use when asked to create, update, or refine a spec document.
---

# To Specs

Framework for writing and maintaining a spec. Each requirement section clarifies a focused set of dimensions, with deep-module design awareness and test-seam planning.

## Process

### 1. Explore

Explore the repo to understand the current state of the codebase. Use the project's domain glossary vocabulary throughout, and respect any ADRs in the area you're touching.

### 2. Sketch test seams

Sketch the seams at which you'll test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point — the fewer seams across the codebase, the better. The ideal number is one.

Check with the user that these seams match their expectations.

### 3. Write the spec

Write the spec using the section template below. Clarify these dimensions per requirement:

1. **User / Stakeholder** — who benefits from this requirement?
2. **Problem statement** — what specific problem does this solve?
3. **Solution** — what solution, from the user's perspective?
4. **User stories** — "As a [persona], I want [goal] so that [reason]"
5. **Acceptance criteria** — concrete, testable conditions for done
6. **Implementation decisions** — modules to build/modify, interfaces, schema changes, API contracts, architectural decisions
7. **Module sketch & deep module design** — major modules needed; look for deep module opportunities
8. **Testing decisions** — test seams (from step 2), what makes a good test here, modules to test, prior art in the codebase
9. **Non-functional requirements** — performance, reliability, security, scalability
10. **Edge cases** — boundaries: empty, error, default, concurrent, restart, reconnect, no data, rate limits
11. **Out of scope** — explicitly what is NOT covered
12. **Priority** — Must-have, Should-have, Nice-to-have
13. **Dependencies** — what other requirements or external things must exist first?
14. **Open questions** — what is still unknown or undecided?
15. **Further notes** — anything else

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet encoding a decision more precisely than prose (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts.

## Deep Module Design

Actively look for opportunities to extract **deep modules** — modules that encapsulate significant complexity behind a simple, stable, testable interface (few exported symbols, minimal API surface). The goal is strong encapsulation: callers depend on a simple interface, not the internal complexity.

Distinguish between:
- **Deep modules** — packages hiding significant complexity behind a narrow interface (e.g. `internal/exchange/`, `internal/lua/`, `internal/db/`)
- **Shallow modules** — straightforward packages with minimal hidden complexity (e.g. `internal/config/`, `internal/symbol/`)
- **Thin binaries** — `cmd/*` packages that compose deep modules rather than containing significant logic

## Spec Section Template

Each requirement section follows this structure:

```
### <Title>

**User / Stakeholder:** <who>

**Problem statement:** <what problem>

**Solution:** <what solution, from user perspective>

**User stories:**
- As a <persona>, I want <goal> so that <reason>

**Acceptance criteria:**
- [ ] <condition>
- [ ] <condition>

**Implementation decisions:**
- <modules, interfaces, schema changes, API contracts, architectural decisions>

**Module sketch & deep module design:** <description, calling out deep vs shallow>

**Testing decisions:** <test seams, what makes a good test here, modules to test, prior art>

**Non-functional requirements:** <performance, reliability, etc.>

**Edge cases:** <boundary conditions>

**Out of scope:** <what is NOT covered>

**Priority:** <Must-have / Should-have / Nice-to-have>

**Dependencies:** <what must come first>

**Open questions:** <what is still unknown>

**Further notes:** <anything else>
```

## Interview Guidance

When interviewing the user about requirements:

- Ask questions **one at a time**. Do not batch questions.
- Start with the most foundational / high-impact questions first (new sections, then cross-cutting implied changes) before drilling into specifics.
- For impacted existing sections, interview only about the specific dimensions that need updating — do not re-interview the entire section.
- If a question can be answered by exploring the codebase, explore instead.
- For each question, provide your recommended answer.