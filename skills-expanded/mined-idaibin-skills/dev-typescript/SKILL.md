---
name: dev-typescript
description: "Implement non-browser TypeScript or JavaScript changes for Node.js, Bun, or Deno."
---

# TypeScript Implementation

## Entry Gate

Implement the smallest authorized non-browser source slice in the repository's actual runtime and package-manager contract. Read effective guidance, identify the owning root and current basis, and stop if a decisive contract cannot be resolved.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Any source change | [checklist](references/checklist.md) | Scoped implementation and credible validation |
| Node, Bun, Deno, ESM/CJS, package or runtime choice applies | [runtime profiles](references/runtime-profiles.md) | Runtime-compatible change |
| Public seam/testable behavior applies | [behavior first](references/behavior-first.md) | Bounded behavior evidence |
| Module/API design or quality risk applies | [codebase design](references/codebase-design.md) and/or [code quality](references/code-quality.md) | Reuse and maintainability decision |
| Cross-boundary signals apply | [project grounding](references/project-grounding.md) | Qualified boundary evidence |

## Invariants

- Preserve existing user-facing copy and feedback type/timing unless the current request or an accepted Product/UI decision authorizes the change. A technical change alone is not that authority; an agent-written spec or test cannot supply it. Apply an explicit user copy choice without asking again; when choosing authorized wording, reuse accepted project terms and claim only observable states. Propose unsupported changes and continue unaffected work.
- Within the authorized change, apply [unused-code evidence](references/code-quality.md#unused-and-dead-code) to code it makes obsolete; retain uncertain consumers and avoid broader cleanup. If a demonstrated instruction gap causes omission or rework, report the exact rule and a minimal candidate to its owner; do not rewrite governing instructions implicitly.
- Before touching another business module, apply the [cross-module business gate](references/codebase-design.md#cross-module-business-gate); an implementation request alone does not authorize changing its existing behavior or code.

- Preserve existing runtime, package manager, module, source, and test owners; do not add a parallel stack.
- For CLI changes, exercise the actual command entry point and representative flags
  when safe and available; keep build, installed-command and runtime evidence distinct.
  Select build checks by changed risk and the project's required delivery gates.
- If an entrypoint or launcher guard changes, also exercise an existing supported noncanonical invocation such as its symlink or alias; do not invent another form. Do not substitute a build for CLI execution.
- Keep source, static, build, runtime, artifact, and deployment claims separate.
- Do not implement browser UI, review, stage/commit/push, or infer unresolved behavior.

## Output Map

Report scope, authoritative inputs, runtime/profile, reuse decision, changed files, focused validation, Worktree drift, exclusions, and `Not verified` gaps.

## Reference Map

- Read [checklist](references/checklist.md) for the baseline workflow and stop conditions.
- Read [runtime profiles](references/runtime-profiles.md) only for runtime/package concerns.
- Read [behavior first](references/behavior-first.md), [codebase design](references/codebase-design.md), [code quality](references/code-quality.md), and [project grounding](references/project-grounding.md) only when their condition applies.
- Read [usage](references/usage.md) for triggers and nearest boundaries.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
