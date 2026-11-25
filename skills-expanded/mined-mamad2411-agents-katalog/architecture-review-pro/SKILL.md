---
name: architecture-review-pro
description: Review and improve codebase architecture, module boundaries, coupling, domain language, data flow, and long-term maintainability. Adapted from Matt Pocock-style architecture improvement workflows for Codex v4.1. Use for architecture review, refactor planning, complex feature placement, or when code is becoming hard to change.
---

# Architecture Review Pro

## Workflow

1. Identify the domain concepts and current module boundaries.
2. Map the change pressure: what is hard to change, test, or understand.
3. Find shallow modules, duplicated decisions, leaky abstractions, and unclear ownership.
4. Prefer deep modules: simple interface, meaningful internal complexity.
5. Propose small architecture improvements that can be done safely.
6. Tie each recommendation to a concrete future change it makes easier.

## Review Checks

- Domain names are consistent across code, tests, docs, and UI.
- Business rules have a clear home.
- Data access does not leak everywhere.
- API/client models do not contaminate domain models without reason.
- Cross-cutting concerns such as auth, logging, and validation are not copy-pasted.
- Tests cover behavior at stable boundaries.

## Output

Use findings first:

```markdown
发现：
- [P1] Boundary leak in ...

建议：
- ...

下一步：
- ...
```

Avoid large rewrites unless the user explicitly asks for a migration plan.
