---
name: dev-rust
description: "Implement, port, or refactor Rust source, including native Rust UI, in the existing Cargo workspace."
---

# Rust Implementation

## Entry Gate

Implement a bounded Rust change in the repository's actual Cargo workspace, toolchain, crate boundaries, and interface contracts. Read guidance and current Worktree state; stop before edits if the target crate, build contract, or decisive interface is unknown.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Any Rust source change | [checklist](references/checklist.md) and [best practices](references/best-practices.md) | Scoped implementation/validation |
| Public seam/testable behavior applies | [behavior first](references/behavior-first.md) | Behavior evidence |
| Architecture or quality risk applies | [codebase design](references/codebase-design.md) and/or [code quality](references/code-quality.md) | Reuse/quality decision |
| Rust-rendered desktop UI, GPUI, or a GPUI-based component kit changes | [native UI](references/native-ui-profile.md) | Revision-grounded UI implementation and layered acceptance |
| Stateful agent workflow, typed agent protocol, async lifecycle/backpressure, durable recovery, approval/sandbox enforcement, or Tauri/local app-server IPC applies | [agent runtime](references/agent-runtime-profile.md) | Stateful runtime procedure |
| An applicable Unsafe/FFI or Porting/parity question benefits from a Bun-derived source challenge | [Bun patterns](references/bun-production-patterns.md) | Optional focused boundary challenge |
| Integration, persistence, packaging, compatibility, or cross-project signal applies | [project grounding](references/project-grounding.md) | Qualified evidence |
| Existing/adopted protocol automation applies | [protocol contracts](references/protocol-contracts.md) and [OpenAPI governance](references/openapi-contract-governance.md) | Native-authority protocol work |

## Invariants

- Preserve existing user-facing copy and feedback type/timing unless the current request or an accepted Product/UI decision authorizes the change. A technical change alone is not that authority; an agent-written spec or test cannot supply it. Apply an explicit user copy choice without asking again; when choosing authorized wording, reuse accepted project terms and claim only observable states. Propose unsupported changes and continue unaffected work.
- Within the authorized change, apply [unused-code evidence](references/code-quality.md#unused-and-dead-code) to code it makes obsolete; retain uncertain consumers and avoid broader cleanup. If a demonstrated instruction gap causes omission or rework, report the exact rule and a minimal candidate to its owner; do not rewrite governing instructions implicitly.
- Before touching another business module, apply the [cross-module business gate](references/codebase-design.md#cross-module-business-gate); reuse an existing explicit decision for the same plan and scope.

- Preserve real crate, ownership/error, async, unsafe/FFI, toolchain, and test conventions.
- Do not add a framework, generated client, or protocol pipeline without an existing/adopted owner.
- Keep source, lint/build, native/runtime, artifact, and deployment proof separate; do not mutate Git.

## Output Map

Report basis, crate/toolchain/profile, changed files/contracts, focused validation, exclusions, and `Not verified` gaps.

## Reference Map

- Read [checklist](references/checklist.md) and [best practices](references/best-practices.md) for the baseline.
- Read [behavior first](references/behavior-first.md), [codebase design](references/codebase-design.md), [code quality](references/code-quality.md), and [project grounding](references/project-grounding.md) only when applicable.
- Read [native UI](references/native-ui-profile.md) only for Rust-rendered desktop UI changes; technology comparison remains research/planning and native-window operations remain with `ops-client`.
- Read [agent runtime](references/agent-runtime-profile.md), [Bun patterns](references/bun-production-patterns.md), [protocol contracts](references/protocol-contracts.md), and [OpenAPI governance](references/openapi-contract-governance.md) only under their Route Map conditions.
- Read [usage](references/usage.md) for triggers and nearest boundaries.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
