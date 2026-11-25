---
name: kmp-refactor
description: Refactors Kotlin Multiplatform code across commonMain, androidMain, iosMain, and tests. Use when moving platform APIs out of shared code, introducing interfaces or expect/actual declarations, or changing architecture boundaries.
---

# KMP Refactor

## Agents

- Lead Agent
- KMP Architect Agent
- Android Agent
- iOS Agent
- Test Agent
- Review Agent

## Use When

- Platform APIs leaked into `commonMain`.
- Shared API needs platform-specific implementation.
- Code must move between `commonMain`, `androidMain`, and `iosMain`.
- `expect/actual` signatures, packages, or missing actuals fail compilation.
- Architecture boundaries between presentation, domain, data, and platform layers are unclear.

## Inputs

- Affected files and source sets.
- Current compile error or review finding.
- Supported targets.
- Existing platform adapter patterns.
- `.cursor/docs/project-structure.md`, `.cursor/docs/info/agent/module-map.md`.

## Workflow

1. Lead Agent identifies affected source sets and delegates specialists.
2. KMP Architect Agent decides interface + injection vs `expect/actual`.
3. Android Agent implements Android actuals or platform adapters when needed.
4. iOS Agent implements iOS actuals or platform adapters when needed.
5. Test Agent updates shared tests or reports gaps.
6. Review Agent checks boundaries and behavior risks.
7. Lead Agent runs final verification.

## Rules

- Prefer interface + constructor injection for replaceable behavior.
- Use `expect/actual` only for small stable platform contracts.
- Keep actual declarations in the same package and with matching signatures.
- Do not split refactored code into micro-files with fewer than 10 meaningful lines unless the file is an architectural unit or enum.
- Preserve compact Kotlin formatting: no blank lines between data class fields, sealed class entries, or enum entries of the same kind.
- Do not change unrelated UI, DI, navigation, or business behavior.

## Outputs

- Boundary decision and rationale.
- Files moved or changed by source set.
- Android/iOS parity notes.
- Tests updated or gap explained.
- Compile/verification command and result.

## Failure Handling

- If one platform cannot support the same behavior, stop and report the product/architecture decision needed.
- If actual declarations cannot match common signatures, route back to KMP Architect Agent.
- If refactor expands into unrelated DI/navigation changes, pause and ask Lead Agent to confirm scope.

## References

- [expect-actual-guide.md](references/expect-actual-guide.md)
