---
name: data-access
description: Implement the data access layer including contracts, repositories, and BLoC/Cubit for business logic. Use when adding Flutter CQRS data access.
argument-hint: "<feature-or-use-case>"
---

# Implement Data Access Layer

Implement the data access layer including contracts, repositories, and BLoC/Cubit for business logic.

## Relevant knowledge

- For details about CQRS and contracts, see `../flutter-cqrs-usage/references/cqrs-data-access.md`.
- For command/query/operation naming, base classes, the `cqrs.run`/`cqrs.get` API, repository boundaries, and contract generation, see `reference.md` (alongside this skill).
- For base-cubit recipes, use `flutter-cubit-utils`.

## Steps

1. Find the required contracts in `contracts.dart`. Match them against the user prompt.
2. If contracts are missing, ask the user to run the contracts generator or run it manually.
3. For simple API calls, use contracts directly in the BLoC/Cubit.
4. For complex logic (caching, multiple sources, mapping), implement a repository.
5. Implement the BLoC or Cubit to handle the feature's business logic.
6. Do not create operations unless explicitly requested.

## Success criteria

- Code follows `../flutter-cqrs-usage/references/cqrs-data-access.md` and other relevant plugin rules.
- Missing contracts are reported if still absent after generation.
- All uncertainties are clarified with the user rather than assumed.
