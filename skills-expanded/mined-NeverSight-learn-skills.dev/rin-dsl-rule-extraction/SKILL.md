---
name: rin-dsl-rule-extraction
description: Explores a Swift project and extracts project-specific Rin (Rinter) DSL rule candidates verifiable by current AST predicates. Use only when the user explicitly invokes /rin-dsl-rule-extraction or asks for Rin rule extraction from a PROJECT_ROOT.
disable-model-invocation: true
---

# Rin DSL Rule Extraction

> DSL reference and semantics moved to `rin-dsl-rinfile`. Install both skills for extraction.

Extract **project-specific** rules expressible by the current Rin DSL. Prefer conventions found in the target codebase. Do not invent predicates that do not exist.

Invoke only via `/rin-dsl-rule-extraction` or `@rin-dsl-rule-extraction`.

Contributor constraints: [AGENTS.md](https://github.com/novr/Rin/blob/main/AGENTS.md).

## Prerequisites (required)

1. **Apply `rin-dsl-rinfile` semantics** at start (`@rin-dsl-rinfile` or read [rin-dsl-rinfile/SKILL.md](https://github.com/novr/Rin/blob/main/skills/rin-dsl-rinfile/SKILL.md)).
2. If not installed, recommend both (one command per skill):

```bash
npx skills add novr/Rin -s rin-dsl-rinfile -g -a cursor -y
npx skills add novr/Rin -s rin-dsl-rule-extraction -g -a cursor -y
```

3. Map conventions using the **pattern catalog** in `rin-dsl-rinfile`.

## Extraction defaults

Follow [rin-dsl-rinfile authoring defaults](https://github.com/novr/Rin/blob/main/skills/rin-dsl-rinfile/SKILL.md#authoring-defaults). Additionally:

4. Each candidate needs path + line or function name; prefer 2+ files or a doc citation.
5. Tune after `rinter_validation`.

Put rules that need receiver refactors (e.g. `deps.analytics.foo()` instead of `Analytics.foo()`) in `needs_code_convention_change`, not `applicable_rules`. See [rin-dsl-rinfile evaluation model](https://github.com/novr/Rin/blob/main/skills/rin-dsl-rinfile/SKILL.md#evaluation-model).

## Workflow

```
Task Progress:
- [ ] Apply rin-dsl-rinfile semantics
- [ ] Resolve PROJECT_ROOT
- [ ] Omnidirectional survey (layout, naming, entry points, catch handling, existing Rinfile.swift)
- [ ] Map conventions → Rule.scope (files) + onPath (units) via rin-dsl-rinfile catalog
- [ ] Emit draft_rinfile with project-specific identifiers
- [ ] Run rinter validation (mandatory)
- [ ] Report tuning (scope, ifEmpty, rule splits)
```

## Project-path prompt

Replace `<<<PROJECT_ROOT>>>`.

````markdown
# Rin DSL rule extraction (project path)

Survey the project and extract **project-specific** rule candidates verifiable by the **current Rin (Rinter) DSL**.

Apply [rin-dsl-rinfile](https://github.com/novr/Rin/blob/main/skills/rin-dsl-rinfile/SKILL.md) semantics before mapping.

## Target project

- PROJECT_ROOT: `<<<PROJECT_ROOT>>>`
- Depth: `quick` | `standard` (default) | `thorough`

## Scope split (required)

- **Files** → `Rule.scope` / `Target`
- **Functions / catch inside files** → `onPath` on predicate
- `matchingFunctions` matches **function names**, not file names

## Predicates (summary)

`MustCall`, `MustCallAnyOf`, `WhenCalls` (+ `mustAlsoCall` / `mustAlsoCallAnyOf`), `MustHandleError`, `MustDeclare`, `MustThrow`, `WhenCalls(name:)`. Details: rin-dsl-rinfile.

## Extraction defaults

Follow rin-dsl-rinfile authoring defaults. Prefer `namedFunctions` / `matchingFunctions` with `ifEmpty: .skip` over bare `everyFunction`.

## Evidence rules

- Each candidate needs **evidence**: path + line or function name (prefer 2+ files or doc citation).
- Use project-specific identifiers in `dsl_body`, not placeholders.

## Output

`project_summary`, `applicable_rules` (with `verification_sample` OK/NG), `needs_code_convention_change` (receiver/call-site refactors per rin-dsl-rinfile), `out_of_scope`, `draft_rinfile`, `rinter_validation`.

**Not supported (`out_of_scope`):** import rules, access control, SwiftUI-specific, cross-file resolution, type inference / `typealias`, return/parameter type signatures, call order / 1:1 pairing, helper delegation. `MustThrow` skips plain `throws`, no `throws`, and `throws(any Error)` (literal typed-throws only).

## Self-check

- [ ] `Rule.scope` vs `onPath` correct
- [ ] Narrow `onPath` preferred
- [ ] `mustAlsoCallAnyOf` for OR pairs
- [ ] `rinter_validation` completed
````

## Manual-input prompt

Accept convention descriptions from the user. Map `onPath` using [rin-dsl-rinfile convention table](https://github.com/novr/Rin/blob/main/skills/rin-dsl-rinfile/SKILL.md#convention--onpath).

Same output sections as project-path mode.

## rinter_validation (mandatory)

```bash
cd PROJECT_ROOT
rinter --config Rinfile.swift --check-config
rinter --config Rinfile.swift --all-files
```

If `rinter` is missing, state the blocker and how to install (Homebrew / release binary / `swift build`).

Report: `exit_code`, `violation_count`, `runtime_errors`, `false_positive_candidates`, `missing_coverage`, `recommended_tuning`.

Exit codes: `0` pass, `1` violations, `2` errors. Do not finish without validation or a stated blocker.

## Quality checklist

- [ ] `rin-dsl-rinfile` semantics applied
- [ ] `Rule.scope` vs `onPath` correct
- [ ] Narrow `onPath` preferred
- [ ] Evidence on every candidate
- [ ] `mustAlsoCallAnyOf` for OR pairs
- [ ] `rinter_validation` with tuning notes
