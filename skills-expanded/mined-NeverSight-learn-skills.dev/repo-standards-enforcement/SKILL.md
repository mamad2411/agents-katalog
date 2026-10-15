---
name: repo-standards-enforcement
description: Use this skill to enforce repository-wide standards for toolchain compliance, package-manager purity, type safety, testing, maintainability, and architecture. When a more specific skill exists for a concern such as final linting or formatting remediation, that more specific skill takes precedence over this skill's generalized guidance.
license: Apache-2.0
metadata:
   author: Mike Willbanks
   repository: https://github.com/mwillbanks/agent-skills
   homepage: https://github.com/mwillbanks/agent-skills
   bugs: https://github.com/mwillbanks/agent-skills/issues
---

# Repository Standards Enforcement

Use this skill whenever work must comply with repository-native standards, tooling, package-manager rules, TypeScript safety, maintainability rules, design system constraints, testing expectations, and infrastructure conventions.

This skill enforces repo detection, toolchain compliance, maintainability-first implementation, validation discipline, and rejection of one-off or low-quality engineering shortcuts.

## Concern ownership

This skill is a **repository-wide policy skill**.

When another skill exists that is more specific to a concern covered here, that more specific skill owns execution for that concern.

Priority order:

1. Narrow concern-specific skill
2. Stack-specific skill
3. Repository-wide standards skill

Examples:

- `biome-enforcement` owns Biome execution, remediation flow, config and ignore-path decisions, and post-Biome validation
- a MUI or design-system implementation skill owns component and design-system execution details
- a Pulumi-specific infrastructure skill owns infrastructure execution details

This skill continues to govern all remaining repository-standard concerns that are not owned by a more specific skill.

The agent must not run duplicate or conflicting workflows across overlapping skills.

---

## When to use

Invoke this skill whenever the task involves modifying code, tests, infrastructure, tooling, build scripts, workspace configuration, shared components, APIs, or any other repository artifact that must conform to local engineering standards.

Use it together with `agent-execution-mode` for implementation tasks, and defer to any more specific skill that governs a subset of the repository rules enforced here.

---

## Core enforcement goals

- honor the repository’s actual toolchain and conventions
- enforce package-manager purity
- enforce TypeScript correctness
- enforce linting and formatting correctness through deferred bulk remediation unless a more specific linting or formatting skill supersedes this guidance
- enforce maintainability over one-off implementations
- enforce design-system-first thinking
- enforce test discipline
- enforce infrastructure standards when Pulumi is present
- explicitly hand off to stack-specific skills when detectable
- defer concern ownership to more specific skills when available
- enforce deterministic validation sequencing and idempotent remediation workflows

---

## Repo detection matrix

### Affected scope determination

The agent must determine the minimal correct scope for validation and remediation.

Rules:

- prefer affected files or packages when boundaries are clear
- expand to repo-wide scope when tooling, configs, or cross-cutting concerns require it
- include transitive dependents when changes impact shared modules or contracts
- avoid unnecessarily broad repo-wide operations when a narrower scope is safe and correct

### Command resolution

When executing build, test, linting, or formatting steps, command selection must be deterministic and repository-native.

Rules:

- prefer repository-defined scripts in package manifests, workspace tooling, task runners, or documented developer workflows
- if multiple candidate commands exist, select the command aligned with repository conventions, docs, or existing automation
- if no repository-defined command exists, fall back to the standard toolchain command implied by detected tooling
- do not invent non-standard commands when a repository-defined command exists
- use the same command family consistently across validation phases unless a more specific skill requires otherwise
- resolve commands before execution begins so validation phases do not switch entrypoints mid-workflow

### Linting and formatting tooling

Detect if any linting or formatting tooling is configured, for example:

- biome configuration files
- eslint configuration files
- prettier configuration files
- other repository-defined linting or formatting tools

If detected:

- linting and formatting are mandatory unless a more specific linting or formatting skill supersedes this section
- linting and formatting remediation must be deferred until after core build validation and initial test execution
- when a more specific linting or formatting skill exists, that skill owns execution timing, command structure, remediation workflow, and post-validation behavior
- otherwise, use repository-native linting and formatting workflows against the affected scope in a single bulk remediation sequence

Rules:

- always respect the repository's linting and formatting configuration
- always check affected files or affected scopes at minimum
- run at the appropriate root based on repo structure
- do not bypass configured tooling with ad hoc formatting
- do not run repetitive per-file lint or format fix cycles
- do not duplicate or conflict with a more specific linting or formatting skill when one is available

### Bun

Detect if any of these exist:

- `bun.lock`
- `bun.lockb`
- workspace config indicating Bun usage
- scripts or docs clearly using Bun

If detected:

- Bun is the default package manager, runtime, and test entry path unless the repo clearly requires something else
- in Bun workspaces, prefer both repo root and affected package when scripts differ
- do not introduce npm, yarn, or pnpm commands or lockfiles unless the repo already uses them

### TypeScript

Detect if TypeScript is present through `tsconfig.json`, package manifests, or source layout.

TypeScript validation order:

1. project-specific typecheck script if present
2. `bunx tsc --noEmit`
3. `tsc --noEmit` only if already wired in the repo

Rules:

- touched scopes must have zero TypeScript warnings and errors unless a more specific validation skill defines a stricter or more specialized workflow
- run repo-wide checks when cheap and already stable
- do not suppress type errors to force progress unless explicitly justified and safe
- prototype mode still may not break type safety

### Test runner detection

Detect existing test runner conventions first.

Rules:

- follow existing repo conventions first
- prefer `bun test` when Bun-native and no different repo convention exists
- use `vitest` only when the repo already uses it or clearly expects it
- do not introduce a new testing framework without explicit need

### MUI and design-system detection

Detect shared design system or MUI dependencies from package manifests, component structure, or docs.

If detected:

- explicitly hand off to stack-specific skills such as MUI/design-system skills when available
- enforce design-system-first implementation
- enforce composition, extension, shared primitives, and reusable boundaries
- reject one-off visual hacks unless clearly justified

### Pulumi

Detect if any of these exist:

- `Pulumi.yaml`
- Pulumi stack files
- Pulumi TypeScript modules

If detected, Pulumi rules are mandatory.

---

## Maintainability enforcement

Reject these patterns unless explicitly justified and documented:

- page-local one-off components where shared or reusable boundaries clearly apply
- duplicated data mapping logic
- duplicated validation rules
- ad hoc fetch or mutation handling that bypasses shared patterns
- hardcoded design values when shared design tokens or design system mechanisms exist
- bypassing shared primitives or repository-standard abstractions
- shortcut architecture that increases long-term maintenance cost without explicit user approval

Principles:

- maintainability over quick one-off fixes
- composition and extension over copy-paste specialization
- repo-native patterns over convenience hacks
- shared abstractions over duplicated behavior
- consistent developer experience over isolated local optimizations

---

## Linting and formatting policy

Linting and formatting remediation is a deferred validation phase.

Definitions:

- build validation: execution of the repository's compile, build, or typecheck steps to ensure the codebase is in a valid state
- tests: execution of the repository's configured test suites according to existing conventions
- affected scope: the minimal set of files, packages, or modules impacted by the change, expanded when required for correctness

Validation phases:

- implementation phase: make the required changes without prematurely running deferred linting or formatting remediation
- core validation phase: run build validation and required pre-remediation tests
- remediation phase: run deferred bulk linting and formatting remediation until clean
- post-remediation validation phase: if remediation modified files, re-run build validation and tests
- completion phase: declare completion only after all applicable validations pass or limitations are documented honestly

Required sequence:

1. Complete implementation
2. Run build validation
3. Run tests
4. Run linting / formatting remediation loop
5. If linting / formatting modified files:
   * re-run build
   * re-run tests
6. Declare task complete

When linting or formatting tooling is configured:

- if a more specific linting or formatting skill is available, use that skill for execution behavior
- otherwise, use the repository-native linting or formatting command for the affected scope

Remediation loop:

1. Parse the linting / formatting output, for example Biome JSON
2. Convert diagnostics into a remediation task list
3. Resolve issues in bulk across the affected scope without introducing new violations
4. Run the linting / formatting command again

Repeat until **linting / formatting reports zero errors**.

Exit criteria:

- linting and formatting report zero errors
- no new issues are introduced in previously clean areas
- the remediation loop converges without oscillation

Rules:

- run linting and formatting in bulk across the affected scope
- do not run linting or formatting per file in repeated small cycles
- run broader scopes when practical
- do not claim completion if linting or formatting issues remain in touched code
- do not hand-format around the configured formatter
- do not create a conflicting linting or formatting workflow when a more specific skill exists
- if linting or formatting modified files, re-run build validation and tests before declaring completion
- remediation must be idempotent when re-run on a clean state
- avoid oscillating fixes between rules or files
- prefer repository-provided commands or scripts over constructing ad hoc commands


State requirements:

- each validation phase must have a stable command set before execution starts
- the workflow must progress forward through phases without skipping required validation
- phase transitions triggered by remediation changes must return to post-remediation validation rather than restarting ad hoc earlier steps
- completion is only valid from a clean post-remediation state

---

## TypeScript policy

Type safety is mandatory.

Rules:

- no TypeScript warnings or errors in touched scopes
- repo-wide type validation should be run when cheap and stable
- no unsafe type escapes without explicit rationale
- no knowingly broken types left for follow-up unless the user explicitly permits non-production work and blockers are documented
- do not confuse “compiles enough” with “type-safe enough”

Preferred validation order:

```text
1. existing typecheck script
2. bunx tsc --noEmit
3. tsc --noEmit if already repo-native
```

Additional rules:

- type validation must be run against the affected scope and expanded when required for correctness
- do not rely on partial compilation success when full type safety is required by the repo

---

## Test enforcement policy

Default expectations:

- run targeted tests for affected scope
- run targeted or repository-defined pre-remediation tests before deferred linting or formatting remediation
- if linting or formatting remediation modifies files, re-run build validation and tests
- run the full test suite before declaring completion unless a more specific validation skill defines a different completion sequence
- follow existing repo test conventions first

Rules:

- do not skip tests when behavior changed
- do not claim completion when targeted tests fail
- do not skip full-suite validation before completion unless impossible or the repo is already known unstable, and if so, document that honestly
- if a changed area lacks tests where tests are appropriate, add or update them

For Pulumi repositories:

- require 100% unit test coverage as reported from `bun test --coverage`

---

## Package-manager purity policy

The configured or clearly detectable package manager is mandatory.

Rules:

- if the repo uses Bun, use Bun
- do not introduce npm, yarn, or pnpm lockfiles or commands into a Bun repo unless the repo already intentionally uses them
- do not mix package-manager workflows casually
- follow workspace-aware installation and execution patterns

---

## Bun workspace behavior

In Bun workspaces:

- prefer repo root and affected package execution when scripts differ
- validate both the local package and relevant root-level workflows
- do not assume package-local success implies workspace-level correctness
- respect workspace dependency boundaries and shared packages

---

## Design system policy

All projects must use a design-system-first approach.

Rules:

- prefer component composition and extension over one-off components
- prefer reusable boundaries over page-local fragments
- prefer tokens, shared primitives, and centrally managed patterns over hardcoded styling or isolated implementations
- when stack-specific design-system skills are available, use them explicitly
- do not bypass the design system because implementing correctly is more work

---

## Pulumi policy

When Pulumi is present, the following are non-negotiable:

- no hardcoded environment values where config-driven stacks should be used
- config-driven stack behavior
- typed inputs and outputs
- reusable component resources when reuse is warranted
- preview-safe changes
- infrastructure documentation updates for infra changes
- 100% unit test coverage from `bun test --coverage`

Additional rules:

- do not make infra changes that are operationally ambiguous without documenting the behavior
- do not scatter infra conventions inconsistently across stacks
- do not bypass typed abstractions when shared Pulumi component patterns are appropriate

---

## Validation checklist

Before claiming completion, validate all applicable items:

- repo tooling was detected correctly
- command resolution was determined correctly and kept consistent across validation phases
- configured package manager was respected
- linting and formatting requirements were satisfied when configured, using a more specific skill when available
- concern ownership was resolved correctly before execution began
- no generalized workflow here conflicted with a more specific skill
- touched TypeScript scopes have zero warnings/errors
- targeted tests passed
- deferred linting and formatting remediation was run in bulk at the correct phase
- remediation loop converged without oscillation or repeated conflicting fixes
- validation phases were executed in order and completion was reached from a clean post-remediation state
- full suite was run before completion or any limitation was documented honestly
- design-system and maintainability rules were followed
- Pulumi-specific rules were satisfied when Pulumi exists
- no one-off hacks were introduced without explicit justification

---

## Output behavior

When responding after using this skill, summarize:

- tooling detected
- standards enforced
- commands run
- validation phases executed
- affected scope determination and rationale
- validation outcomes
- any repo constraints that shaped the implementation
- any honest blockers or known repo instability
- any more specific skills that took precedence over generalized rules in this skill
- whether deferred bulk linting and formatting remediation modified files and triggered re-validation

Do not claim standards compliance without validating it. Do not use vague phrases instead of actual command and result summaries.
Always include the specific commands executed (e.g., `bunx tsc --noEmit`, `bun test --coverage`) and their outcomes when reporting on standards enforcement. If any step could not be completed, document the reason honestly and indicate any potential impact on compliance.

---

## Specific-over-general rule

When this skill and a more specific skill both apply:

- the more specific skill owns execution details for its concern area
- this skill continues to govern all remaining repository-standard concerns
- the agent must avoid running conflicting duplicate workflows
- deferred linting and formatting remediation must follow the timing and loop owned by the more specific skill when one exists

This skill defines repository-wide standards.
It should not override a more specific skill that exists specifically to execute a narrower concern more correctly.
