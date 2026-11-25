---
name: tech-code-refactoring-team
description: End-to-end code refactoring workflow. Use when the user wants a complete refactoring package covering code structure analysis, git-history technical debt signals, Clean Code/SOLID/Clean Architecture review, refactoring pattern selection, target architecture design, behavior-preserving simplification, migration planning, and verification. Coordinates code-analyzer, agent-git-oracle, uncle-bob, code-refactoring, system-architect, and simplify.
metadata:
  short-description: Complete code refactoring workflow
---

# Tech Code Refactoring

Use this skill as the workflow entry point for a complete code refactoring package. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Use `code-analyzer` to understand code structure, module responsibilities, execution flow, data flow, DDD boundaries, complexity, and duplicated logic.
2. Use `agent-git-oracle` to inspect git history for hotspot files, repeated churn, debt accumulation, architectural drift, and refactoring priority.
3. Use `uncle-bob` to evaluate Clean Code, SOLID, Clean Architecture, naming, cohesion, coupling, and dependency direction.
4. Use `code-refactoring` to match problems to safe refactoring patterns and produce staged, behavior-preserving operations.
5. Use `system-architect` when the refactor needs new module boundaries, target architecture, interface contracts, or migration paths.
6. Use `simplify` to execute or propose focused simplifications that preserve external behavior and match the surrounding codebase.

## Routing

- If the user asks to understand a large codebase before changing it, start with `code-analyzer`.
- If the user asks where technical debt is concentrated, use `agent-git-oracle` with git history and churn evidence.
- If the user mentions SOLID, clean code, Uncle Bob, architecture boundaries, or code smells, use `uncle-bob`.
- If the user asks how to refactor safely, use `code-refactoring` to produce a staged plan.
- If the user asks for module decomposition or architecture redesign, use `system-architect`.
- If the user asks to simplify code directly, use `simplify` and keep behavior unchanged.

## Project-First Rules

When working in a local codebase:

1. Inspect tests, public interfaces, dependency boundaries, and current git state before editing.
2. Preserve external behavior unless the user explicitly asks for a behavior change.
3. Prefer small, independently verifiable refactoring steps over broad rewrites.
4. Keep the repository's existing patterns unless they are the source of the refactoring problem.
5. Validate with the narrowest relevant tests first, then broaden when the changed surface warrants it.

## Output Package

For a full code refactoring package, produce:

1. Code structure analysis: responsibilities, complexity hotspots, dependency risks, and duplicated logic.
2. Technical debt assessment: git-history hotspots, risk ranking, and refactoring priority.
3. Clean Code/SOLID report: principle violations and better boundaries.
4. Refactoring plan: staged operations, pattern matches, risks, rollback points, and verification steps.
5. Target architecture: module boundaries, interfaces, dependency direction, and migration path.
6. Refactored code or patch summary: behavior-preserving changes and verification evidence.

## Operating Notes

- Refactor to make the next change easier, not to showcase clever abstractions.
- Do not mix behavior changes with refactoring unless the user explicitly asks.
- Treat missing tests as a risk that shapes the refactoring plan.
- If a safe automated refactor is not possible, deliver a staged plan with verification gates.
