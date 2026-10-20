---
name: refactoring-safely
description: Restructures existing code without changing behavior using small, test-protected steps and named refactorings (extract, inline, move, rename, replace conditional with polymorphism). Use when cleaning up code, reducing duplication or complexity, paying down tech debt, or preparing code for a new feature.
metadata:
  role: senior-developer
  version: "1.0"
---

# Refactoring safely

Refactoring changes structure, never behavior. If behavior changes, it is a feature or a fix — do it in a separate commit.

## Preconditions

1. **Tests exist and pass** for the code being changed. If not, first write *characterization tests* that pin current behavior (including current bugs) through the public interface.
2. **Clean working tree.** Commit or stash unrelated changes.
3. **A reason.** State the goal: "make room for feature X", "remove duplication between A and B", "reduce function from 200 to <50 lines". No goal → no refactor.

## The loop

1. Pick one named refactoring (below).
2. Apply it in the smallest possible step. Prefer IDE/LSP automated refactorings for renames and moves.
3. Run tests. Green → commit with message `refactor: <what>`. Red → revert, take a smaller step.
4. Repeat until the goal is met. Stop there.

## Smell → refactoring

| Smell | Refactoring |
|-------|-------------|
| Long function | Extract Function; Replace Temp with Query |
| Duplicated code | Extract Function / Pull Up Method; then delete copies |
| Long parameter list | Introduce Parameter Object; Preserve Whole Object |
| Feature envy (uses another object's data) | Move Function |
| Switch on type repeated in many places | Replace Conditional with Polymorphism |
| Primitive obsession (strings for money, ids) | Replace Primitive with Value Object |
| Deep nesting | Replace Nested Conditional with Guard Clauses |
| Shotgun surgery (one change touches many files) | Move Function/Field to consolidate |
| Large class | Extract Class |
| Dead code | Delete it (git remembers) |

## Large-scale refactoring

For changes too big for one PR:
- **Parallel change (expand → migrate → contract):** add the new path, move callers one by one, remove the old path.
- **Branch by abstraction:** introduce an interface in front of the old implementation, build the new one behind it, switch, delete the old.
- Keep every intermediate state shippable. Never hold a long-lived refactoring branch.

## Rules

- Do not mix refactoring and behavior changes in one commit.
- Do not refactor code you are not otherwise touching unless that is the task.
- Preserve public APIs, or deprecate them with a migration path.
- Report: goal, steps taken (commit list), tests run, and anything deliberately left for later.
