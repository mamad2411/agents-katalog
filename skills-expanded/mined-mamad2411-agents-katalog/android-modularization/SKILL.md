---
name: "android-modularization"
description: "Design Android repositories with feature, core, and build-logic modules that scale without cyclic dependencies."
metadata:
  version: "0.1.0"
  category: "foundations"
  tags: ["android", "modules", "gradle", "repository-design"]
  triggers:
    include: ["android module split", "feature modularization in android", "break cyclic module dependency", "android app into modules", "core ui data domain modules", "android module graph", "api vs implementation dependency android", "android-modularization skill", "feature module boundary android"]
    exclude: ["compose focus management", "room query tuning", "notification delivery only", "slow gradle build", "configuration cache problem", "version catalog for android repo", "agp build logic change"]
  owners: ["@android-agent-skills/maintainers"]
  test_targets: ["examples/orbittasks-compose", "examples/orbittasks-xml", "benchmarks/triggers.jsonl"]
---
# Android Modularization

## When To Use
- Use this skill when the request is about: android module split, feature modularization in android, break cyclic module dependency.
- Primary outcome: Design Android repositories with feature, core, and build-logic modules that scale without cyclic dependencies.
- Reach for this skill when the problem is dependency direction, API ownership, or feature/data/core boundaries, not task-level build speed tuning.
- Handoff skills when the scope expands:
- `android-gradle-build-logic`
- `android-architecture-clean`

## Workflow
1. Map the current module graph first: app, feature, data, core, build-logic, and any dynamic-feature or test-only modules.
2. Identify which direction is wrong: feature-to-feature coupling, framework leakage into domain/data, API surface too wide, or duplicated shared code with unclear ownership.
3. Split by ownership and change rate, not by abstract theory; create the smallest module boundary that removes the current coupling problem.
4. Keep `api` vs `implementation`, public surface area, and test fixture ownership explicit so the new boundary stays stable.
5. Hand off build-speed or plugin-architecture issues only after the module graph itself is coherent.

## Guardrails
- Prefer official Android and Kotlin guidance over custom local conventions when they conflict.
- Keep public APIs boring and explicit; avoid clever abstractions that hide Android lifecycle costs.
- Do not mix architectural cleanup with product behavior changes unless the request explicitly needs both.
- Document any compatibility constraints that will affect old modules or generated code.
- Avoid over-modularizing a small codebase when the real need is a single clearer ownership boundary.

## Anti-Patterns
- Sprinkling helpers across modules without a clear ownership boundary.
- Introducing framework-specific code into pure domain or data layers.
- Refactoring every adjacent file when only one contract needed to change.
- Leaving migration notes implied instead of writing them down.
- Treating module count as the goal instead of build isolation and dependency clarity.

## Examples
### Happy path
- Scenario: Review the fixture apps as app modules and map the next split into feature/core layers.
- Command: `cd examples/orbittasks-compose && ./gradlew :app:projects`

### Edge case
- Scenario: Keep shared XML resources and manifest placeholders from leaking across modules.
- Command: `cd examples/orbittasks-xml && ./gradlew :app:dependencies`

### Failure recovery
- Scenario: Differentiate modularization requests from architecture-clean and build-logic prompts.
- Command: `python3 scripts/eval_triggers.py --skill android-modularization`

## Done Checklist
- The implementation path is explicit, minimal, and tied to the right Android surface.
- Relevant example commands and benchmark prompts have been exercised or updated.
- Handoffs to adjacent skills are documented when the request crosses boundaries.
- Official references cover the chosen pattern and the main migration or troubleshooting path.

## Official References
- [https://developer.android.com/topic/modularization](https://developer.android.com/topic/modularization)
- [https://docs.gradle.org/current/userguide/multi_project_builds.html](https://docs.gradle.org/current/userguide/multi_project_builds.html)
- [https://developer.android.com/build/extend-agp](https://developer.android.com/build/extend-agp)
- [https://developer.android.com/build/migrate-to-kotlin-dsl](https://developer.android.com/build/migrate-to-kotlin-dsl)
