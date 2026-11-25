---
name: grimoire-implement
description: Implement code from a plan or conversation by applying structural design principles — lifecycle boundaries, composition, stable abstractions, and surgical changes. Requires a plan.
---

# Purpose

Implement production code from a plan. Every type boundary has a reason. Every change is surgical.

A plan is a prerequisite. Without a plan, there is nothing to implement.

# Scope

This skill writes code to the repository.

This skill requires a plan as input. Tickets and specs must be converted to a plan first (use grimoire-plan).

This skill does NOT:
- Write plans (use grimoire-plan)
- Write specs (use grimoire-spec)
- Decompose into tickets (use grimoire-slice)
- Record domain knowledge or ADRs (use grimoire-record)
- Clarify requirements (use grimoire-clarify)

Completion: All planned changes are implemented. Every type boundary has a justification. No unrelated code is modified.

---

# Workflow

## 1. Pre-flight

Determine the implementation source:

- Plan file (`.grimoire/plans/NNNN-title.html`) — use that plan.
- Conversation — the user's description of what to implement serves as the plan.
- Ticket or spec path — stop. Tell the user to run grimoire-plan first to generate a plan from the ticket/spec. Do not proceed.

Read the plan (file or conversation) and extract the concrete list of changes: which files to create, which to modify, which types are involved.

Completion: Plan is loaded. Change list extracted and written as a checklist.

---

## 2. Survey codebase

Explore the repository to understand what already exists:

- Read every file the change will touch. Understand current structure.
- Find existing patterns: error handling style, module layout, naming conventions. Follow them.
- Identify reusable logic: utility functions, base types, helper modules. Do not reinvent.
- Check language version and available features (Cargo.toml, tsconfig.json, pyproject.toml, etc.). Prefer the project's modern features over outdated patterns.

Completion: All files to be modified are read. Reusable logic is identified. Language feature level is known.

---

## 3. Design structure

Before writing code, apply every principle from [references/principles.md](./references/principles.md).

For each new or modified type, answer all eight questions:

| Principle | Decision question |
|-----------|-------------------|
| Lifecycle | When created? When destroyed? Group same-lifecycle things together. |
| Ownership | Who owns this? Dependency flows one way. No cycles. |
| Composition | What does it compose? Small focused types, not deep inheritance. |
| Abstraction | Is there a real second implementation today? If not, no interface/trait. |
| Responsibility | What one thing does this type manage? One concept per type. |
| Data vs logic | Are resources (handles, buffers, connections) separated from business logic? |
| State | Can fields represent an invalid state? Redesign to make it impossible. |
| Interface | Does the public API express capability, not implementation detail? Keep it small. |

Document each type: what it is, what it owns, what it depends on, and which principle justifies each boundary.

Completion: Every new or modified type has a design record with justified boundaries. No type owns more than one concept. No unnecessary abstractions planned.

---

## 4. Implement

Implement in dependency order. Foundational types (depended on by others) first.

For each change:

1. Write or modify only the code necessary to fulfill the design.
2. Reuse existing utilities when logic already exists in the codebase. Check step 2 findings before writing new helpers.
3. Use the project's modern language features. No outdated patterns from older language versions.
4. Keep functions single-purpose. Split only when a function becomes hard to understand at a glance — not by an arbitrary line count.
5. Do not touch unrelated code. No formatting changes, no drive-by refactors, no "while I'm here" improvements.
6. Verify the change compiles before moving to the next type.

After each type: confirm its public API matches the design record from step 3.

Completion: Every type is implemented and compiles. No unrelated files are modified. Functions are understandable.

---

## 5. Verify

Run through the final checklist:

- [ ] Every type boundary from step 3 is respected in the code.
- [ ] No cyclic dependencies exist — verify import/dependency graph.
- [ ] No interface/trait with a single implementation — abstract only when multiple implementations exist.
- [ ] No unrelated files were modified or reformatted.
- [ ] Functions are single-purpose and easy to understand. No function does too many things at once.
- [ ] Existing codebase patterns are followed, not replaced.
- [ ] Modern language features are used where applicable (not ancient syntax).

If any check fails, fix it before reporting completion.

Completion: All checks pass. Every deviation from the design in step 3 has a deliberate reason.

---

# Rules

- Dependencies flow one way. No cycles, no bidirectional references.
- One concept per type. Split types that manage unrelated things.
- One implementation = no abstraction. Interfaces/traits need at least two real implementors.
- Reuse before writing. Check the codebase for existing utilities before creating new ones.
- Surgical changes only. Don't reformat, restructure, or "improve" unrelated code.
- Modern syntax. Use the project's current language features, not decade-old patterns.
- Design principles live in [references/principles.md](./references/principles.md). SKILL.md controls workflow only.
