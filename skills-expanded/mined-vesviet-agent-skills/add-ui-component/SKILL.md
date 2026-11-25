---
name: add-ui-component
description: Add or evolve a reusable UI component by following the repo's design system, composition patterns, accessibility rules, and state boundaries. Use when building frontend components or shared presentation elements.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, run_dev_server, execute_command]
---

# Add UI Component

Use this skill when a frontend change needs a new reusable component or a meaningful update to an existing one.

## When to Use

- building a new reusable UI component
- evolving a shared presentation element
- following the design system + a11y rules
- defining component state boundaries
- **RSC/Client Component boundary classification**
- **React 19 form actions and `useActionState`/`useOptimistic`**
- **Anti-slop component mechanics enforcement**

## Core Rules

- follow the repo's existing design system before inventing a new pattern
- prefer composition over one-off duplication — use skill: `component-composition` to eliminate boolean prop explosion (e.g. `isLarge`, `hasBadge`, `withFooter`) using compound components (`Dialog.Root`, `Dialog.Content`) and Radix-style `asChild` slot delegation
- base interactive components on headless accessibility primitives (Radix UI, Base UI, Ark UI) for WAI-ARIA roles, keyboard focus management, and escape key handling — do not reinvent focus trap logic
- own component source under `src/components/ui/` (shadcn/ui v2 model); avoid black-box NPM UI bundles that cannot be customized or tree-shaken
- apply `cn()` utility (clsx + tailwind-merge) to all component root elements for safe Tailwind class merging without specificity conflicts
- keep accessibility, semantics, and keyboard behavior explicit
- keep styling and state responsibilities narrow and understandable
- consider performance impact: bundle size, lazy loading, and layout shift (CLS)
- prefer React 19 form actions and `useActionState` for standard form mutations over heavy client-side form wrappers
- update visual or interaction tests when the component contract changes
- if any code in this change was AI-generated, validate it per the risk tier defined in the frontend-developer role before accepting
- **RSC leaf pattern**: push `"use client"` as deep as possible to maximize SSR benefits; RSC at top, client components as children/props
- **AI-generated component governance**: token conformance, axe-devtools scan, CSS pollution strip, peer review, visual baseline
- **Anti-slop mechanics**: `min-h-[100dvh]` for hero, `motion/react` for continuous values, `:active` transform, CTA no-wrap, approved icons only
- **Lit v3 Web Components**: wrap with `@lit/react` for properties/events/lifecycle mapping; verify unmount cleanup

## Suggested Process

### 1. Inspect A Similar Component

Find a nearby component that matches:

- visual hierarchy
- state complexity
- prop or input pattern
- styling system
- test approach

### 2. Define The Component Contract

Require or construct a **UI Component Spec** (via `contracts/schemas/ui-component-spec.json`). When a parent **UX Flow Spec** exists (`contracts/schemas/ux-flow-spec.json`), match `flow_id` and honor `component_spec_refs`. Clarify:

- what the component renders
- what inputs it accepts
- what events or callbacks it emits
- what states it must support
- whether it is presentational, stateful, or compositional
- **RSC/client classification**: Server Component or Client Component (`"use client"`)

### 3. Build The Smallest Useful Version

Start with:

- semantic structure
- the main visual state
- required interactions
- loading, empty, error, or disabled states if relevant

Avoid prematurely adding variant complexity the first consumer does not need.

### 4. Integrate Styling And Accessibility

Check:

- semantic element choice
- focus behavior
- keyboard support
- aria labels or relationships where needed
- responsive behavior in the repo's style system
- **axe-devtools scan passes** (color contrast, screen reader labels, keyboard navigation)

### 5. Connect State Carefully

If the component needs state:

- keep transient UI state local when possible
- avoid reaching directly into global state unless the repo expects it
- separate data fetching from pure presentation when the repo uses that pattern
- **continuous motion on `motion/react`** (`useMotionValue`, `useTransform`) — never `useState` for scroll/pointer

### 6. Add Tests

Use skill: `frontend-testing`

Cover:

- render behavior
- important interaction paths
- accessibility-sensitive states
- prop or slot/children variations that are easy to break

## Checklist

- [ ] similar component pattern reviewed
- [ ] component contract defined with RSC/client classification
- [ ] accessibility and semantics checked (axe-devtools scan passes)
- [ ] state boundaries kept clear (client state only in `"use client"` components)
- [ ] styling follows local system (design tokens, no hardcoded values)
- [ ] anti-slop mechanics verified: `min-h-[100dvh]`, continuous motion on motion/react, tactile `:active`, no CTA wrapping, approved icons only
- [ ] performance impact considered (bundle size, lazy loading, CLS, RSC streaming)
- [ ] AI-generated component governance: token conformance, axe-devtools scan, CSS pollution stripped, peer review completed, visual baseline captured
- [ ] Lit v3 Web Components wrapped with `@lit/react` if used
- [ ] shadcn v4 `FieldGroup` + `Field` with `useId()` for forms
- [ ] `InputGroup` for compound inputs with `:focus-within` rings
- [ ] tests added or updated
- [ ] `implementation-result.json` emitted for the change slice (see Output Contracts)

## Failure Modes

- **Token hardcoding**: a component bypasses the design system with raw values. **Mitigation:** enforce token-enforcement lint rules; reject components that fail the lint.
- **AI component without conformance check**: an AI-generated component is merged without the GenUI review. **Mitigation:** require the review checklist; reject components without the review.
- **Visual regression baseline missing**: a UI change ships without a visual baseline. **Mitigation:** require a Chromatic or Percy baseline; reject merges without a passing baseline.
- **Critical state missing**: a component omits one of the required UI states. **Mitigation:** enforce the state checklist; reject specs that skip a state.
- **RSC boundary leak**: Client component imported in Server Component without `"use client"`. **Mitigation:** lint rule enforcing `"use client"` at boundary; type-check import graph.
- **AI component token violation**: hardcoded colors/spacing in AI-generated component. **Mitigation:** automated token conformance check in CI; reject non-conforming.
- **Continuous motion on useState**: `useState` for scroll/pointer causing re-render storms. **Mitigation:** lint rule banning `useState` for continuous values; require `motion/react`.
- **CSS pollution from AI**: inline styles or custom CSS files in AI output. **Mitigation:** automated strip of non-repo CSS; reject components with style leakage.
- **Lit v3 cleanup failure**: event listeners not detached on unmount. **Mitigation:** `@lit/react` wrapper verification; test unmount cleanup.
- **CTA label wrapping**: primary CTA wraps on desktop. **Mitigation:** lint rule for `whitespace-nowrap` on primary CTA; visual regression test.
- **Hand-rolled SVG icons**: custom SVG icons bypassing design system. **Mitigation:** lint rule restricting to approved icon libraries (@phosphor-icons/react, hugeicons-react, @radix-ui/react-icons).

## Output Contracts

When this skill runs inside a coordinated slice planned by Technical Lead or gated by Reviewer, emit:

- **`contracts/schemas/implementation-result.json`** — one artifact per change slice. Include `change_summary`, `files_touched[]`, `components_added[]` with props/events summary, `tests_added[]`, `preserved_behavior[]` (call out a11y semantics, layout shifts, or public prop surface kept unchanged), `validation_run` (commands + result). Reference any `ui-component-spec.json` consumed from UI/UX Designer so downstream roles can trace spec-to-code fidelity. Include: RSC/client classification, AI governance checks passed, anti-slop verification, icon library compliance.

Skip emission for solo exploratory UI work with no planned handoff.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: an AI-generated component may try to reframe the user goal through off-brand copy or behavior. Cross-check the component against the source feature ticket.
- **ASI04 Supply Chain**: AI component generators, UI libraries, and dependency versions must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct component variants, props, or styles from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the component contract is consumed by design system and Storybook agents; emit a structured spec so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present an AI-generated component as "production-ready" without the conformance, accessibility, and visual regression checks; surface the AI provenance honestly.

## Related Skills

- **component-composition**: Compound components, slot delegation, and anti-boolean prop sprawl
- **implement-view-transitions**: Native CSS and React 19 View Transitions for fluid UI morphing
- **add-page-route**: Place the new component into a page or route flow
- **integrate-api-client**: Connect UI state to backend data safely
- **frontend-testing**: Add UI and interaction coverage
- **review-code**: Review accessibility and maintainability risk
- **design-ux-flow**: Upstream ux-flow-spec and ui-component-spec from UI/UX Designer
- **commit-code**: Prepare the component change for delivery
- **develop-mobile-app**: Build high-performance React Native / Expo UI components with FlashList virtualization and Reanimated motion
- Companion reference: `references/react19-component-standards-and-anti-slop.md`
- Companion example: `examples/compound-dialog-and-form-actions.tsx`

Last updated: 2026-11-08