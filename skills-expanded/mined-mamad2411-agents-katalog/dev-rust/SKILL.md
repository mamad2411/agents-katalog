---
name: dev-rust
description: "Use when a Rust source change must be implemented, ported, or refactored across APIs, crates, services, CLIs, async, persistence, unsafe or FFI boundaries, tests, or docs; owns source edits and validation, not audit-only, review-only, or Git-delivery work."
---

# Rust Implementation

## Overview

Implement Rust changes against the repository's real toolchain, project class, crate boundaries, error model, and validation contract. Select validation by risk rather than applying native/FFI-level gates to every routine change.

## Workflow

1. Read effective repository guidance, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present, then run `git status --short` before edits.
2. Identify the Rust project class: library workspace, application workspace, HTTP service, CLI, Tauri/native backend, or compact single package.
3. Read the approved requirement/specification when one exists. Confirm requested behavior, acceptance criteria, non-goals, affected crates/modules/files, compatibility, and validation seams; for complex work without a usable specification, use the host's built-in planning and effective repository instructions before editing.
4. Inspect the relevant `Cargo.toml`, lockfile, toolchain, formatter, lint, command source, modules, tests, architecture docs, and API/interface docs.
5. Consume a current `repo-map` inventory or perform the same targeted search across route registration, handlers, services, repositories, traits/impls, types/DTOs, errors, migrations, callers, tests, and analogous features.
6. Start with the **Baseline** validation contract, then select every applicable risk overlay. Overlays are composable, not severity levels:
   - **Protocol automation:** an existing OpenAPI/generated-client pipeline or an explicitly requested contract migration. Ordinary HTTP/API changes keep the repository-native route/DTO/client/test boundary under Baseline.
   - **Concurrency/runtime:** Tokio tasks, channels, locks, cancellation, blocking work, overload, or shutdown.
   - **Persistence/SQLite:** migrations, transactions, schema/query changes, durable compatibility, backup, or recovery.
   - **Unsafe/FFI:** unsafe, ABI/layout, raw pointers, callbacks, allocators, native handles, or cross-language resource ownership.
   - **Porting/parity:** language port or large rewrite that must preserve observable behavior and release semantics.
   - **Target/platform:** `cfg`, target-specific APIs, packaging, native linkage, or supported-platform behavior.
   A routine change uses Baseline with no overlays. A mixed FFI plus SQLite change selects both overlays; a target-only change selects Target/platform without inheriting unrelated heavy tools.
7. Decide in order: directly reuse, extend an existing contract, adapt the nearest reference, or create new. Record why existing interfaces are insufficient before adding an endpoint, trait, type family, or module.
8. Trace ownership, dependency direction, and the complete interface chain before adding or moving code. If Protocol automation applies, identify one code-first or contract-first authority; otherwise preserve the repository-native API authority without introducing OpenAPI.
9. When behavior is stable and a durable public seam exists, confirm that seam, then work one external behavior at a time: run one red-capable check, make the minimum green change, and continue as a vertical tracer bullet. Load `references/behavior-first.md`; do not force it onto exploratory work, generated code, or behavior without an honest seam.
10. Implement the smallest idiomatic change that follows local ownership, borrowing, module, error, async, persistence, FFI, configuration, logging, documentation, and test patterns. When the task materially involves duplication, dead/unused code, abstraction, coupling, or maintainability, load `references/code-quality.md` with implementation semantics and remove only declarations made obsolete by the authorized change after resolving Rust reachability.
11. Update manifests, module exports, tests, commands, docs, CI/deploy paths, migrations, generated files, and indexes when the structural or public boundary changes.
12. Run focused checks after each slice, then the repository's baseline gates and every selected overlay. Use Miri, sanitizers, fuzzing, stress, or repeated-operation tools only when both supported by the target repository/environment and relevant to the changed invariant.

## Modes

- **Targeted implementation:** add or fix Rust behavior without broad architecture or toolchain changes.
- **Structure alignment:** align modules, crates, manifests, commands, and docs to an explicit repository standard.
- **Contract migration:** change an API, DTO, feature, persistence, or consumer boundary with compatibility and rollout evidence.
- **Native/porting implementation:** preserve observable behavior, ABI/resource semantics, supported targets, and release behavior before idiomatic cleanup.
- **Implementation self-check:** verify the edited Rust surface for ownership, errors, async behavior, safety, tests, dependencies, and structural drift before `repo-review` assesses commit readiness.

## Do Not Use For

- First-pass repository discovery; use `repo-map`.
- Planning-only requests without authorized Rust source changes; use the host's built-in planning.
- Shared cross-functional business language/rule or lifecycle conflicts; use `domain-modeling`. Route feature-local behavior, states, and acceptance to `product-spec`.
- Diagnosis-only requests without authorized Rust source changes; use the host's built-in diagnosis under effective instructions.
- Dirty-tree ownership, staging plans, or commit grouping; use `repo-review`. Use `repo-delivery` for actual staging or commits after review.
- Systematic Rust architecture, performance, memory, concurrency, SQLite, unsafe, or FFI audit without requested edits; use `audit-rust`.
- Review of a fixed Rust change basis, including authorization or token risks; use `repo-review`.
- Frontend or webview UI changes; use `dev-frontend`.

## Hard Rules

- Follow repository-pinned Rust, edition, resolver, formatter, lint, dependency, and command contracts. Do not upgrade them during unrelated feature work.
- Keep directories consistent with the identified project class. Do not copy a Web/Rust, Tauri, CLI, library, or multi-process layout into another class without an explicit migration requirement.
- Do not create an endpoint, handler, service, repository, trait, DTO/type family, error model, or shared module before reading relevant docs and checking the existing interface chain. Reuse or extend first; follow the nearest feature's placement and naming when a new contract is justified.
- Do not introduce OpenAPI or a generated client solely because a REST endpoint changes. When Protocol automation applies, discover the real toolchain, preserve one code-first or contract-first authority, and keep generated artifacts derived.
- Preserve dependency direction. Entry modules stay thin; workflows belong in the established service/engine owner; deterministic domain logic avoids IO; persistence stays behind repository or storage boundaries when the project defines them.
- Prefer typed errors and `Result` propagation. Do not add runtime `unwrap`, `expect`, `panic!`, silent error swallowing, or fallback behavior unless the contract explicitly requires it.
- Load and apply only references for the selected protocol, concurrency, persistence,
  unsafe/FFI, porting, target/platform, behavior-first, conditional code-quality,
  or codebase-design overlays. Do not inherit heavy gates from an unselected
  overlay.
- Treat new warnings in the touched surface as defects. Do not broaden scope to clean unrelated legacy warnings; report them separately. Prefer a local justified `#[expect(...)]` over weakening workspace lints.
- Keep product-specific behavior in the product repository. Move code to a shared crate only after real reuse, stable API, named ownership, and consumer validation are established.
- When adding, reusing, moving, renaming, or deleting a crate, module, feature, binary, migration, or shared surface, update every owning manifest, export, command, test, doc, CI/deploy path, generated output, and index in the same task.
- Preserve unrelated local changes and generated files not owned by the task.
- Do not add speculative traits, generic layers, managers, repositories, or
  configuration switches for hypothetical consumers. Do not delete apparently
  unused items until public API, features, targets, `cfg`, macros, derives,
  build scripts, examples/benches, FFI exports, and downstream use are resolved.

## Validation Model

- **Baseline:** repository-defined format/check plus focused behavior tests; Clippy only when it is part of the repository baseline.
- **Selected overlays:** add only the contract, concurrency/runtime, persistence/SQLite, unsafe/FFI, porting/parity, and target/platform evidence required by the changed surface. Combine overlays when risks interact; do not let one overlay erase another.
- **Protocol-automation overlay:** only when selected, validate/rebuild the OpenAPI artifact, check clean idempotence and compatibility, regenerate owned clients, and run applicable backend conformance. Otherwise use repository-native API tests.
- **Optional heavy tools:** Miri, sanitizers, fuzzing, stress, leak, and repeated-operation gates are never inherited merely from a target-specific change. Run them only when supported and relevant, or record why they were excluded.

Do not claim Baseline or an overlay passed when a required tool, target, runtime, dataset, or external dependency was unavailable; mark the exact gap `Not verified`.

## Output Contract

Report project class, Baseline evidence, selected risk overlays, toolchain and command sources, existing docs/interfaces checked, reuse/extension/reference decision, new-interface justification, changed ownership and contract chain, manifests/docs updated, validation mapped to each selected overlay, failures, excluded optional checks with reasons, and `Not found` or `Not verified` gaps. If the user explicitly requests independent external review/research, hand one fixed basis/question to `ask-chatgpt`; never send implicitly.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for implementation and review checks.
- See [references/protocol-contracts.md](references/protocol-contracts.md) only when Protocol automation is selected.
- See [references/behavior-first.md](references/behavior-first.md) when a stable public seam supports vertical red-green slices.
- See [references/codebase-design.md](references/codebase-design.md) only when the change materially affects a public module/interface, seam, cross-caller abstraction, or testability.
- See [references/best-practices.md](references/best-practices.md) for idiomatic Rust API, ownership, error, test, docs, performance, dispatch, and concurrency rules.
- See [references/code-quality.md](references/code-quality.md) when the requested
  change materially involves duplication, dead/unused code, abstraction
  quality, hidden coupling, or maintainability.
- See [references/bun-production-patterns.md](references/bun-production-patterns.md) for source-backed migration, FFI, unsafe, resource-lifetime, lint, and validation patterns derived from Bun's production Rust rewrite.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
