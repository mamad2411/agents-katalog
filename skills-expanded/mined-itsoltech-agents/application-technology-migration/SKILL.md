---
name: application-technology-migration
description: "Migrate applications or toolchains with parity, staged rollout, rollback, and decommissioning."
---

# Application Technology Migration

Treat a rewrite as a product, technical, and operational migration. Do not start from code generation. First prove why migration is the right option, identify the smallest safe slice, preserve current behavior with characterization and contract tests, and plan rollout and rollback before implementation.

## Process

1. Clarify the migration driver: business problem, current technology, target technology, users, data, integrations, operational constraints, and why refactor or upgrade is insufficient.
2. Apply a scope gate. If the request says "rewrite the app" or spans unrelated modules, propose a smaller first migration slice and defer the rest into later plans.
3. Load `itsol-current-tech-context` to verify current and target technology versions, official migration guides, SDK/runtime/package choices, latest stable defaults for new target components, and support windows unless the user explicitly pins versions.
4. Inventory the current system: features, data, integrations, infrastructure, security, support workarounds, hidden jobs, reports, exports/imports, and production behavior.
5. Map current behavior with characterization tests and contract tests before proposing replacement behavior.
6. Choose a migration strategy: refactor, upgrade, Strangler Fig, Branch by Abstraction, parallel run, or big bang only when risk is low and rollback is proven.
7. Write or update a migration plan file in the repo, including current tech context, feature parity, slice plan, data plan, rollout, rollback, observability, security, risks, success criteria, stop criteria, and decommissioning.
8. Self-review the migration plan for hidden scope, missing contracts, missing data strategy, weak rollback, missing current tech context, missing skills, untested behavior, and unresolved operational risk.
9. For implementation, route each approved slice through `itsol-functional-planning` or `itsol-bug-debugging` as appropriate, proportionate verification, focused domain skills, review skills, and `itsol-subagent-workflow` when subagent-driven. Add `itsol-tdd-workflow` only on explicit user request.

If the task is only a small feature or bug in an existing migration, route to the narrower skill after checking migration constraints.

## Focused References

- [01-decision-and-inventory.md](./references/01-decision-and-inventory.md) - Decision And Inventory
- [02-strategy-architecture-data.md](./references/02-strategy-architecture-data.md) - Strategy Architecture And Data
- [03-implementation-testing-rollout.md](./references/03-implementation-testing-rollout.md) - Implementation Testing And Rollout
- [04-security-docs-decommissioning.md](./references/04-security-docs-decommissioning.md) - Security Documentation And Decommissioning
- [05-planning-templates-and-review.md](./references/05-planning-templates-and-review.md) - Planning Templates And Review
