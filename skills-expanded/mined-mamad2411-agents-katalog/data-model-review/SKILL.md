---
name: data-model-review
description: Reviews and redesigns data models from first principles using Go's type system. Use when the user wants to review a data model, redesign types, improve a domain model, fix stringly-typed code, add type safety, use Go generics, composition, or interfaces, or says "data model", "review types", "redesign schema", "type system", "make impossible states unrepresentable", "branded types", "domain model", "entity design", "data architecture", "type safety review", "refactor data layer", "model redesign", "Go data model", "Go types", "Go generics", "Go structs", "Go interfaces", "Go composition". Triggers for any language but produces Go as the primary design language. Also fires when the user asks about validation layers, schema design, or converting implicit models to explicit typed ones.
metadata:
  tags: data-model, types, go, golang, generics, composition, interfaces, review, architecture, domain-design, schema, validation, branded-types, first-principles, embedding, iota, type-safety
allowed-tools: bash view edit write ls grep
---

# Data Model Review

A first-principles review and redesign skill for data models. Reviews what exists, catalogs every problem, then uses Go's type system to design a model where invalid states are unrepresentable.

## Why This Matters

Most data models grow organically. They start as a few structs, accumulate pointer fields, sprout string-typed enums, and eventually become a minefield of nil-pointer dereferences and runtime validation masquerading as type-safe code. This skill stops that rot and replaces it with intentional design.

The output is not just a list of problems. It is a complete redesign — using branded types, interface-based unions, generics, composition via embedding and interfaces, and zero-value discipline — delivered as a self-contained HTML presentation that the team can read, bookmark, and reference.

## Process

READ, UNDERSTAND, RESEARCH, REFLECT before each action.

### Step 1: Discovery — Understand the Current Model

1. **Find all type definitions** in the target scope:
   - Structs, interfaces, type aliases, enums (iota)
   - Database schemas, ORM models, DTOs, API request/response types
   - Config types, state types, domain entity definitions
2. **Read every file** that defines data structures. Do not skip any.
3. **Map the relationships** — which types reference which? Draw a mental (or actual) graph.
4. **Identify the primary language** — this skill produces Go as the design language, but adapts concepts to the target language.
5. **Catalog implicit assumptions** — fields that are "always set except when...", types that are strings but should be branded, pointer fields that are never nil, etc.

### Step 2: Problem Catalog — Brutal Honesty

For every type, field, and relationship, ask these questions and record every problem found.

Grade each problem by **severity** (critical/high/medium/low) and **systemicity** (how many types it affects).

| #   | Problem                          | Severity | Key Question                                               |
| --- | -------------------------------- | -------- | ---------------------------------------------------------- |
| P1  | Stringly-Typed Everything        | Critical | Are identifiers/raw `string` instead of branded types?     |
| P2  | Pointer Fields as State Encoding | Critical | Is `*time.Time` used to mean "not yet" instead of a union? |
| P3  | No Validation at Type Level      | High     | Can a struct be constructed invalid and still compile?     |
| P4  | Primitive Obsession              | High     | Are domain concepts (`Email`, `UserID`) raw primitives?    |
| P5  | Missing Interface-Based Unions   | High     | Are polymorphic types `Type string` + optional pointers?   |
| P6  | No Composition, Only Embedding   | High     | Are base structs embedded blindly, creating deep coupling? |
| P7  | Implicit Relationships           | Medium   | Are foreign keys raw `int` with no type link to parent?    |
| P8  | No Versioning or Lifecycle       | Medium   | No `CreatedAt`, `UpdatedAt`, `Version` fields?             |
| P9  | Duplicated Logic Across Types    | High     | Same validation copied into multiple structs?              |
| P10 | Weak Collection Types            | Medium   | Slices where maps/sets matter? Nil vs empty confusion?     |
| P11 | No Generic Parameterization      | Medium   | `UserPage` / `OrderPage` defined separately?               |
| P12 | Missing Error Models             | Medium   | Errors as untyped `error` with string matching?            |

For detailed fixes for each problem, load [./references/go-patterns.md](references/go-patterns.md).

### Step 3: Reflection — Step Back

STOP. Do not start designing yet.

1. **Re-read the problem catalog.** Are there problems you missed? Problems you graded wrong?
2. **Identify the root causes.** Are the symptoms 12 separate issues or 3 systemic ones?
3. **Ask "what is this model trying to achieve?"** — not "what does it currently do."
4. **Identify the core entities** — the 3-5 concepts that everything else revolves around.
5. **Identify the invariants** — what must ALWAYS be true? (e.g., "an Order must have at least one LineItem")
6. **Think about Go's full type power:**
   - Can branded types prevent accidental substitution?
   - Can interface-based unions replace pointer-field state machines?
   - Can generics eliminate duplicated collection/pagination types?
   - Can struct embedding compose behavior without inheritance?
   - Can unexported methods create closed unions?
   - Can constructor functions enforce invariants at creation time?
   - Can `iota` typed constants replace string enums?

### Step 4: Design the Improved Model

Design a new model from first principles. Every design decision must have a rationale.

For the complete pattern catalog with code examples, load [./references/go-patterns.md](references/go-patterns.md).

For decision trees on when to use which pattern, load [./references/decision-trees.md](references/decision-trees.md).

Key patterns:

- **Branded types** — `type UserID string` for compile-time distinction; struct wrapper for runtime validation
- **Interface-based unions** — `type Order interface { order() }` with private method tag for closed unions
- **Generics** — `type Page[T any] struct { Items []T }` for reusable pagination
- **Composition** — struct embedding (`Timestamped`) and interface composition
- **Constructor functions** — `NewLineItem(...)` enforcing invariants at creation time
- **Iota enums** — typed constants with `String()` method for uniform-state enums
- **Custom errors** — structured error types with `errors.As` for handling

### Step 5: Create the HTML Presentation

Write a self-contained, zero-dependency HTML file at `docs/brainstorming/YYYY-MM-DD_<slug>.html`.

Use the **shared design system** from the `html-report-kit` skill:

- Design spec: [./assets/html-report-kit/references/html-output-guide.md](./assets/html-report-kit/references/html-output-guide.md)
- Template: [./assets/html-report-kit/assets/report-template.html](./assets/html-report-kit/assets/report-template.html)

For data-model-specific output guidance (section structure, Go syntax highlighting
examples), also load [./references/output-guide.md](references/output-guide.md).

Required sections:

1. **Hero** — Title, subtitle, architecture deep-dive badge
2. **Table of Contents** — sticky nav
3. **Current State** — stat cards (type count, problem count, severity breakdown)
4. **Problem Catalog** — `.card-problem` cards with severity badges and Go fixes
5. **The Vision** — what perfection looks like
6. **Go Data Model** — type definitions with `.tok-*` syntax highlighting
7. **Composition in Action** — side-by-side before/after (`.compare-*` components)
8. **Validation Layer** — how invalid states become unrepresentable
9. **Decision Log** — why each choice was made, with rejected alternatives
10. **Anti-Patterns** — traps to avoid when adopting the new model
11. **Migration Roadmap** — numbered-step components (`.migration-step`)
12. **Conclusion** — summary quote

### Step 6: Cross-Skill References

After the redesign is complete, consider which related skills should be activated next:

- For Go library decisions, domain types, and architecture patterns — load the `how-to-golang` skill
- For naming quality of the new types and functions — load the `naming-review` skill
- For a full codebase review of the implementation — load the `full-code-review` skill

### Step 7: Git Workflow

Before finishing:

1. Run `git status` to verify what changed.
2. Stage the new HTML file specifically with `git add <file>`.
3. Commit with a VERY DETAILED commit message describing:
   - What was reviewed
   - Problems identified (list them)
   - Go type system features used in the redesign
   - Files added
   - Design decisions
4. Push with `git push`.

## Execution

READ, UNDERSTAND, RESEARCH, REFLECT.
Break this down into multiple actionable steps. Think about them again.
Execute and Verify them one step at the time.
Repeat until done. Keep going until everything works and you think you did a great job!
