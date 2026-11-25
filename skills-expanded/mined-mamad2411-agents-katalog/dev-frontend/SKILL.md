---
name: dev-frontend
description: "Use when a frontend change must be implemented or refactored across UI, state, data, styling, build/tooling, accessibility, performance, or desktop integration, including mapped two-pass visual closure for an accepted selected source; owns source edits and validation, not audit-only, browser-only, UI-spec, or Git delivery."
---

# Frontend Implementation

## Overview

Implement frontend changes with existing-stack alignment, minimal DOM/CSS, clear layout ownership, and explicit verification. Detect the actual framework before applying framework-specific rules. Use `ops-browser` for web runtime evidence and `ops-client` for real desktop-window proof.

## Workflow

1. Read effective repository guidance first, including `AGENTS.md`, `CLAUDE.md`, and host-provided instructions when present.
2. Identify the frontend project class, app boundary, package manager, runtime pin, script contract, directory/naming standard, and documented exceptions.
3. Identify the target page, route, screen, component, framework, UI type, visual source, and required states before editing. When usable authorities apply, load the minimum chain in this order: effective instructions, product requirements or product Feature Spec, selected-source UI Feature Spec, root `DESIGN.md`, existing `repo-map` (navigation only), then live source/config before editing. Load `references/specification-authorities.md`, resolve authorities by meaning rather than filename, and read only the target-slice facts needed for this change. Missing optional artifacts do not create ceremony, but separately report each missing authority as `Not verified` when it affects behavior or acceptance. A missing map never blocks bounded live discovery. For selected-source visual work, also read the selected-source evidence and [references/frontend-visual-evidence.md](references/frontend-visual-evidence.md).
4. Confirm acceptance criteria, non-goals, affected contracts/files, and validation seams from usable approved requirements. Consume existing contracts directly; hand unresolved product decisions to `product-spec` or required selected-source/shared visual decisions to `ui-spec` without treating either Skill as a file detector. When an applicable UI Feature Spec declares a viewport acceptance matrix, consume it without copying its schema: exercise required entries, select optional entries only when useful and in scope, and treat excluded entries only as outside the current acceptance scope, never as proof of unsupported behavior. A newer explicit user viewport constraint overrides a stale artifact. For complex work without a usable specification, use the host's built-in planning and effective repository instructions before editing.
5. Use an existing `repo-map` only to navigate, then verify routes, UI, state, services, tests, analogous implementations, and live theme/adapters in source and config. For API callers, follow the repository's existing client/type authority. Load the protocol-contract profile only when an OpenAPI/generated-client chain already exists or the task explicitly introduces one.
6. Treat root `DESIGN.md` as the shared visual-semantic authority when adopted. Tailwind, Ant Design, shadcn/ui, and local theme/config are implementation adapters and current execution facts, not competing semantic authorities. Verify their actual binding in live source/config; do not claim DESIGN.md automatically synchronizes implementation. Decide `reuse`, `extend`, `wrap`, or justified `new`, and record insufficient candidates or unresolved drift as `Not verified`.
7. For selected-source work, require a valid `spec-ready` artifact and stop before editing when the source is unavailable, the slice is `Partial`/`Not Ready`, target viewport/state is unresolved, or a P1 asset lacks an accepted owner and per-item fallback. Map every applicable acceptance ID to owner file/component, `reuse`/`extend`/`wrap`/justified `new`, asset/data owner, and static/runtime verification method; validate the artifact at `mapped` before editing. Keep source targets separate from current computed runtime values.
8. Inspect only the selected target and reference files needed for the requested change.
9. Classify the existing UI system and layout model: product surface, framework, component library, state/data stack, styling system, shell/content/page boundaries, panels, and scroll regions. When layout geometry, spacing, sizing, overflow, scrolling, layering, or responsive behavior is material, load `references/frontend-layout-governance.md` and identify the affected owners and task-completion seam.
10. Select exactly one framework profile per edited boundary: **React**, **Vue Composition**, **Vue Options**, or **Repository-native Other**. Select only styling profiles actually present, such as **Tailwind**, **CSS Modules**, **Sass/Less**, **CSS-in-JS**, **Ant Design**, or **shadcn/ui**.
11. Preserve typography, spacing, density, already-correct structure, routing, state, API contracts, accessibility, and shared visual ownership unless the task explicitly changes them. Close P1 structure, real assets, font inheritance, contrast, and cross-section alignment before P2 polish; do not rewrite the whole page or change shared `DESIGN.md` tokens for a page-local delta. Do not duplicate a DTO or endpoint already owned by the repository's client/type authority.
12. When behavior is stable and a durable public seam exists, confirm that seam, then work one external behavior at a time: run one red-capable check, make the minimum green change, and continue as a vertical tracer bullet. Load `references/behavior-first.md`; do not force it onto exploratory visuals, generated code, or behavior without an honest seam.
13. Implement with the smallest component, DOM, CSS, and ownership surface that matches existing patterns. When the change materially involves duplication, dead/unused code, abstraction, coupling, or maintainability, load `references/code-quality.md` with implementation semantics and remove only code made obsolete by this task.
14. Update manifests, scripts, routes, tests, docs, indexes, generated route files, and stale references when adding, reusing, moving, renaming, or deleting structural frontend code.
15. Remove stale wrappers, duplicate declarations, late overrides, and temporary layout patches made obsolete by the change.
16. Run focused checks after each slice, then matching project-defined gates; use `ops-browser` or `ops-client` when runtime UI evidence is required. For selected-source work, use `ops-browser` to complete two same-viewport/state comparisons: validate `pass-1` after the first capture/computed review, fix confirmed findings, then recapture and reinspect before validating `final`. Exercise the desktop target and every key breakpoint named by the spec; otherwise report `Partial` or `Not Ready`, never visual completion. Record Worktree state before validation that may generate or rewrite files, compare it afterward, and classify every new diff as requested source, expected task-owned generated output, validation side effect, or unrelated/user-owned work before continuing.

## Modes

- **Targeted implementation:** make a requested frontend change without broad layout or stack changes.
- **Structure and style simplification:** reduce wrapper DOM, repeated utilities, duplicated CSS, unclear layout ownership, and competing scroll/overflow rules.
- **Implementation self-check:** verify the edited frontend surface for component-system, import, style, layout, ownership, route, and framework-native state drift.
- **Stack alignment:** decide how to use React, Vue, Next.js, Vite, TanStack Router, Vue Router, Tailwind, Ant Design, shadcn/ui, desktop webviews, or local components based on the existing app.

## Do Not Use For

- First-pass repository discovery, real commands, or entry points; use `repo-map`.
- Planning-only requests without authorized frontend source changes; use the host's built-in planning.
- Shared cross-functional business language/rule or lifecycle conflicts; use `domain-modeling`. Route feature-local behavior, states, and acceptance to `product-spec`.
- UI specification, selected-source translation, shared visual contracts, task briefs, tokens, mappings, or acceptance rules without source edits; use `ui-spec`.
- Dirty-tree ownership, mixed-hunk review, staging plans, or commit readiness; use `repo-review`.
- Actual staging, commit creation, rebase/squash, push, or delivery; use `repo-delivery` after review.
- Systematic frontend architecture, reuse, state/data, accessibility, performance, or Tauri-boundary audit without requested edits; use `audit-frontend`.
- Browser operation, screenshots, console, network, downloads, uploads, or runtime evidence collection; use `ops-browser`.
- Desktop-client launch review, CGWindowID proof, real-window screenshots, or native runtime operation; use `ops-client`.
- Diagnosis-only requests without authorized frontend source changes; use the host's built-in diagnosis under effective instructions.

## Hard Rules

- Verify the actual stack before using Tailwind, Ant Design, shadcn/ui, React Router, Vue Router, Pinia, Zustand, Redux, React Query, Vue Query, form libraries, icon libraries, or routing helpers.
- Follow repository-pinned Node/package-manager versions, lockfile, dependency policy, script names, directory names, and file naming. Do not upgrade or normalize them during unrelated UI work.
- Keep framework-native structure: use the repository's React Router `routes`, Next.js `app`, Astro `pages`, Vue Router/views or feature convention, or documented equivalent. Preserve existing naming until alignment is explicit.
- Do not introduce a parallel UI kit, CSS system, routing pattern, state layer, API helper, icon library, or form library when an existing one covers the need.
- Do not create a page, component, hook, composable, helper, service, store, wrapper, or shared abstraction before checking any available `repo-map` navigation and performing a targeted live file/symbol search.
- Do not elevate Tailwind, Ant Design, shadcn/ui, local theme/config, or current source into a second visual-semantic authority. They prove only their current implementation binding; report design-to-adapter drift or unexercised behavior as `Not verified` until evidenced.
- Create a new implementation only when reuse or adaptation would violate ownership or behavior. State the reason and place it in the existing directory and naming convention.
- Preserve existing user-visible behavior and repository-owned route, state, data,
  accessibility, and visual contracts unless the task explicitly changes them.
- Load and apply only the selected framework, styling, build/tooling, protocol,
  behavior-first, conditional code-quality, or codebase-design references. Do
  not cross-apply another stack profile.
- Prefer non-mutating `lint`, `typecheck`, `test`, `check`, build, and formatting validation. A command name or documented intent is not proof that the checkout stayed unchanged: compare pre/post Worktree state when the tool may generate or rewrite files, disclose unexpected drift, and never absorb it into the task silently. Run known write-mode generators in an isolated copy when practical. Restore a task-owned validation side effect only when its exact prior content is known and the complete current diff is attributable to that validation with no concurrent or mixed ownership; otherwise preserve the diff, stop, and route ownership reconciliation to `repo-review`.
- Mark unchecked visual, responsive, console, network, runtime, or accessibility behavior as `Not verified`.
- Do not claim selected-source visual completion from build/lint/typecheck, SCSS inspection, or one screenshot pass. Require the two-pass runtime gate and applicable computed geometry/style evidence.
- Do not replace all product logos or content assets with one generic fallback. Keep fallback behavior isolated to an approved missing/failed item.
- Report OpenAPI gates only when that profile applies; otherwise mark them `Not
  applicable`, not `Not verified`.
- Do not add speculative shared layers, default memoization, export-style
  rewrites, or bundler migrations as incidental cleanup. Do not delete
  apparently unused frontend code until route, dynamic import, framework
  registration, build, test, and external-consumer reachability is resolved.

## Output Contract

Report the branch, detected project class/stack and selected profiles, selected-source readiness and acceptance-to-owner implementation mapping when applicable, existing implementations checked, reuse or new-surface decision, changed files and ownership/contracts, both visual review passes and evidence artifacts when applicable, validation status, validation-created drift and its disposition, and intentionally excluded changes. Mark lint/runtime behavior as `Not verified` unless executed in scope; add detailed layout, state, protocol, desktop, or lifecycle evidence only when that profile materially affected the task. If the user explicitly requests independent external review/research, hand one fixed basis/question to `ask-chatgpt`; never send implicitly.

## References

- See [references/usage.md](references/usage.md) for trigger guidance and examples.
- See [references/checklist.md](references/checklist.md) for implementation and review checks.
- See [references/specification-authorities.md](references/specification-authorities.md)
  when resolving product requirements, root `DESIGN.md`, slice UI contracts, and
  owner handoffs before implementation.
- See [references/frontend-layout-governance.md](references/frontend-layout-governance.md)
  when geometry, spacing, sizing, overflow, scrolling, layering, or responsive
  behavior is material to the change.
- Read [references/frontend-visual-evidence.md](references/frontend-visual-evidence.md) for staged selected-source mapping and the two-pass visual gate; validate each stage offline with `python3 scripts/validate-frontend-visual-evidence.py <artifact.json>` and [assets/frontend-visual-evidence.schema.json](assets/frontend-visual-evidence.schema.json). See [references/frontend-visual-gate-example.md](references/frontend-visual-gate-example.md) for a sanitized synthetic example.
- See [references/protocol-contracts.md](references/protocol-contracts.md) only for an existing or explicitly requested OpenAPI/generated-client chain.
- See [references/behavior-first.md](references/behavior-first.md) when a stable public seam supports vertical red-green slices.
- See [references/codebase-design.md](references/codebase-design.md) only when the change materially affects a public module/interface, seam, cross-caller abstraction, or testability.
- See [references/framework-profiles.md](references/framework-profiles.md) for React, Vue Composition, Vue Options, and repository-native framework rules.
- See [references/styling-systems.md](references/styling-systems.md) for Tailwind, CSS Modules, Sass/Less, CSS-in-JS, Ant Design, shadcn/ui, and mixed-stack rules.
- See [references/stack-guidelines.md](references/stack-guidelines.md) for toolchain, routing, layout, and desktop-webview boundaries.
- See [references/code-quality.md](references/code-quality.md) when the requested
  change materially involves duplication, dead/unused code, abstraction
  quality, hidden coupling, or maintainability.
- See [references/eval-cases.md](references/eval-cases.md) for trigger and quality evals.
