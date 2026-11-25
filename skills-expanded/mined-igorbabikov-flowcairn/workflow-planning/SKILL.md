---
name: workflow-planning
description: Plan coherent observable outcomes, interfaces and verification boundaries before brokered implementation.
---

# Dependency-aware work

- Preserve the original requirements and their IDs. Read the affected owner, consumers and existing verification before proposing changes. Separate facts, assumptions and material unknowns.
- Decompose by an observable outcome with a useful verification boundary. A cross-layer user scenario may be one work item. Do not split by arbitrary file counts, lines or duration. For a broad compatible migration, use expand, migrate, contract only when each boundary is independently checkable.
- Declare requirementIds, paths, needed readPaths and real needs. When one work produces an interface consumed by another, use produces/consumes with the exact same contract and explicit producer dependency. Do not use execution order as a substitute for that dependency.
- Review coverage, orphan work, cycles, conflicting interfaces and missing verifiers before source changes. A human acceptance or unavailable environment is an explicit remaining obligation, never an objective pass.
- A structural gate confirms only the structure it actually checks. Semantic assumptions need relevant source or provider review. Correction must retain intent, scope, criteria and permissions and use the Executor's bounded immutable replan mechanism.
