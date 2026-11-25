---
name: frontend-clean-architecture
description: >
  Plan, implement, or review frontend UI code with clean architecture guardrails
  and a default single-purpose file architecture. Use for React, TypeScript, UI
  components, custom hooks, client-side services, API integration views,
  design-system components, frontend feature setup, frontend refactors, and code
  review where separation of presentation, state/use-case logic, data access,
  accessibility, loading/error/empty states, or test seams matter. Do not use as
  a replacement for repo route cards, enterprise gates, product-design visual
  work, live proof, browser proof, or local project conventions.
---

# Frontend Clean Architecture

## Purpose

Use this skill to keep frontend changes structured, testable, accessible, and
compatible with the existing app. For new feature work, default to a
single-purpose, feature-local file map. Treat exceptions as explicit design
choices, not as the default.

## First Gate

Before proposing or editing UI code:

1. Read the repo route/worktree rules and existing UI conventions.
2. Find the nearest existing component, hook, route, API client, style system,
   and test pattern before inventing a new folder shape.
3. If the work is Helpdesk or another governed repo, keep existing enterprise,
   blast-radius, browser-proof, canary, PR, and live-schema gates in charge.
4. If this is visual exploration or prototype design, use the Product Design
   workflow first; return here only for production code structure.

Stop if current source truth, owner module, or proof surface is unknown.

## Plan Shape

For new or refactored frontend work, write the smallest plan that names:

- User workflow and acceptance behavior.
- Existing owner surface and files likely to change.
- Proposed single-purpose files, including feature-local files that have only
  one current caller.
- Data flow: source -> transform/state -> UI -> action/side effect.
- UI state: loading, error, empty, disabled, optimistic, stale, and success.
- Accessibility path: keyboard, labels, focus, ARIA only where appropriate.
- Test/proof: unit/integration tests plus browser proof for rendered workflows.
- Non-goals and forbidden scope.

Use a table when the change crosses layers:

| Layer | Owns | Prefer | Avoid |
|---|---|---|---|
| Types/contracts | Runtime DTOs and UI view models | Exact response and prop shapes | Vague `any`, copied backend guesses |
| Service/client | HTTP or external data access | Existing API client and error contract | `fetch`/SDK calls in components |
| Hook/use case | State, orchestration, derived UI behavior | Injectable seams when they improve tests | Hidden singleton side effects |
| Component | Rendering and local interaction state | Props, accessible controls, stable layout | Business rules and network calls |
| Page/composition | Wiring owner components together | Thin composition and route integration | Reimplementing child behavior |

## Architectural Default

For new frontend feature setup, start from separate single-purpose files even
when each file is initially single-use. Do not wait for reuse before separating
responsibilities.

Default feature-local map:

- `*.types.ts` or existing contract file: DTOs, prop types, view models, and
  discriminated UI state.
- `*Service.ts`, existing API client, or route loader module: data access,
  response parsing, and side-effect error contract.
- `use*.ts` or use-case module: orchestration, pending/error/success state,
  derived behavior, and test seams.
- `*.tsx` component: rendering, semantic controls, layout, and local interaction
  state.
- `*.test.ts(x)` or nearest existing test file: contract, state transition,
  accessibility, and interaction proof.

Collapse files only when the change is genuinely tiny, visual-only, or the local
repo has a clear co-location pattern. When collapsing, state the reason and the
future extraction seam in the plan.

## Implementation Guardrails

- Follow local architecture before generic kit structure.
- Keep each file purpose explainable in one sentence. A file with "and" in its
  purpose is a split candidate unless local convention says otherwise.
- Prefer feature-local single-purpose files over large multi-concern files, even
  if a file is not reused yet. Architecture is for ownership and proof, not only
  reuse.
- Do not create a service interface for every service by default. Create one when
  callers need a stable contract, tests need a seam, or multiple implementations
  exist.
- Inject dependencies where the seam matters. Avoid awkward prop-drilling or
  parameter injection that makes the production call path harder to understand.
- Local UI state in components is fine for interaction state such as open,
  focused, expanded, pending, or transient success. Move orchestration, data
  fetching, business decisions, and derived workflow state out of components.
- Use TypeScript precisely. Avoid `any`; prefer narrowing, discriminated unions,
  parsed DTOs, and explicit nullish/falsy handling.
- Preserve valid falsy values such as `0`, `false`, and empty string when they are
  meaningful. Do not use `value || fallback` for domain values.
- Keep effects stable: avoid stale closures, unstable dependency objects, and
  render loops from freshly-created action bags.
- Keep error behavior honest: do not return fake success data from failed service
  calls unless the product contract explicitly wants degraded placeholder state.
- Do not call code production-ready from mock-only tests or unchecked examples.

For more detailed patterns, read `references/frontend-patterns.md`.

## Review Checklist

Lead with findings before summaries:

- Source truth: existing owner, component hierarchy, API contract, and style/test
  conventions were read.
- Layering: network/data access stays out of render components unless local
  framework convention explicitly owns it there.
- Contracts: response shapes, prop types, and nullable/falsy values are explicit.
- State: loading, disabled, retry, error, empty, optimistic, stale, and success
  behavior is coherent.
- Accessibility: keyboard path, focus behavior, labels, semantic controls, and
  live regions are covered where relevant.
- Runtime proof: UI/rendered-output changes have browser or equivalent headless
  proof; mock-only tests are marked as limited.
- SRP: any touched mixed-responsibility file has `fix_now`, `follow_up`, or
  `not_applicable` classification.
- Blast radius: sibling components/hooks, route consumers, shared clients, and
  tests are named.

## Output

For planning:

```markdown
**Frontend Architecture Verdict:** <READY | REVISE | BLOCKED>
**Existing patterns read:** <files/symbols>
**Layer map:** <types/service/hook/component/page>
**State and accessibility coverage:** <summary>
**Proof plan:** <commands/browser actions>
**Stop rules:** <bullets>
```

For code review:

```markdown
**Findings**
- [severity] <file:line> <issue and why it matters>

**Proof Gaps**
- <mock-only/runtime/browser/accessibility/schema gap>

**Safe Reuse**
- <existing patterns/components/hooks/services reused>
```
