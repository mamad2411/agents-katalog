---
name: component-composition
description: Architect scalable UI components using compound components, Radix-style asChild slot delegation, headless hook separation, and anti-boolean prop sprawl patterns. Use when designing reusable component libraries, refactoring prop-heavy components, or decoupling interaction state from presentation.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, run_dev_server, execute_command]
---

# Component Composition

Use this skill to design, refactor, and review modular frontend components using compound component architectures, headless state hooks, slot delegation (`asChild`), and explicit variant patterns.

## When to Use

- refactoring components suffering from boolean prop explosion (>2 boolean customizer flags)
- designing reusable UI design system primitives (Dialogs, Dropdowns, Cards, Drawers, Comboboxes)
- decoupling interaction state machines and accessibility logic from visual markup
- enabling polymorphic trigger elements via Radix-style `asChild` / `Slot` delegation
- lifting UI state into dedicated provider components for decoupled sibling and action access
- transitioning legacy React component code (`forwardRef`, `useContext`) to modern React 19 idioms (`ref` prop, `use()`)
- **React 19 idioms mandatory migration**
- **shadcn v4 form architecture migration**

## Core Rules

- **Enforce Anti-Boolean Prop Sprawl**: strictly ban components that use boolean flags to toggle internal layout structures (e.g. `isThread`, `hasBadge`, `isHeader`, `withIcon`, `isLoadingModal`); replace with compound components or explicit variants; **max 2 booleans for purely stylistic states**
- **Mandate Compound Component Architecture**: complex components with multiple visual sub-regions must expose subcomponents sharing a typed context interface (`Component.Root`, `Component.Trigger`, `Component.Content`, `Component.Close`)
- **Modernize Form Layouts (`FieldGroup` + `Field`)**: replace legacy v3 nested `FormItem`/`FormControl` boilerplate with shadcn v4 `FieldGroup` and `Field`; use React 19 `useId()` for deterministic label, description, and error linking compatible with Server Actions
- **Compound Inputs (`InputGroup`)**: wrap inputs with prefix/suffix addons, action buttons, or dropdowns using `InputGroup`; eliminate absolute positioning padding hacks in favor of unified flex containers with container `:focus-within` rings
- **Base UI `render` Prop vs Radix `asChild`**: use Base UI `render` prop (`render={(props, state) => ...}`) when children require internal headless state injection or polymorphic tags; use Radix `asChild` (`Slot`) for single-child prop delegation without state projection
- **Decouple State Implementation from UI**: UI compound components must consume a generic context interface (`{ state, actions, meta }`); never hardcode global stores directly inside leaf UI subcomponents; inject state through provider boundaries
- **Decompose Headless Hooks**: extract complex interactive state (focus traps, keyboard navigation, open/close state, ARIA contracts) into reusable headless hooks (`useDialog`, `useDropdown`) returning `{ state, actions, triggerProps, contentProps }`
- **Prefer Children Over Render Props**: compose static and semi-static layouts using nested `children`; reserve render props strictly for dynamic data projection callbacks (`renderItem={({ item, index }) => ...}`)
- **Enforce React 19 Idioms**: do not use `forwardRef` in React 19 codebases (pass `ref` as a standard prop); use `use(Context)` instead of `useContext()`; use `<Context value={...}>` instead of `<Context.Provider>`
- detailed architecture guide and templates: [`references/composition-architecture-and-headless-specs.md`](references/composition-architecture-and-headless-specs.md) and [`../ui-ux-designer-anti-slop-standards.md`](../ui-ux-designer-anti-slop-standards.md)

## Suggested Process

### 1. Audit Prop Surface & Identify Pathologies

Scan the component interface. Count boolean customization props (`is*`, `has*`, `show*`, `with*`). If more than 2 boolean flags alter layout or render branches, declare boolean prop explosion and plan a compound refactor.

### 2. Define Context & Injected Contract

Create the component's context interface with three distinct facets:

- `state`: read-only data values required by subcomponents
- `actions`: callbacks and mutation functions
- `meta`: references (DOM refs, unique IDs, active indices)

### 3. Extract Headless State Machine Hook

Author the headless hook managing state transitions, keyboard bindings (Escape, Enter, Arrows), and ARIA attributes (`aria-expanded`, `aria-controls`, `aria-labelledby`).

### 4. Implement Compound Primitives & Slot Delegation

Author the compound subcomponents. Ensure triggers support `asChild` using the `Slot` primitive, cleanly merging consumer class names, refs, and event listeners.

### 5. Compose Explicit Variants

Author pre-composed, ergonomic variants for frequent use cases (`ThreadComposer`, `ChannelComposer`). Consumers with standard requirements use the variant; consumers with novel layouts compose the primitives directly.

### 6. Verify via Behavioral UI Tests

Use skill: `frontend-testing`. Assert subcomponents render correctly across arbitrary compositions, `asChild` delegates props to custom tags, keyboard accessibility functions, and external action buttons can trigger provider actions.

## Checklist

- [ ] component avoids boolean prop proliferation; maximum <= 2 booleans for purely stylistic states
- [ ] complex multi-region layout structured as compound component (`Root`, `Trigger`, `Content`, etc.)
- [ ] state management decoupled from UI via context provider interface (`state`, `actions`, `meta`)
- [ ] interactive triggers support `asChild` slot delegation without generating illegal DOM wrapper nesting
- [ ] event handlers and refs merged safely via `composeEventHandlers` and `composeRefs`
- [ ] keyboard navigation and WAI-ARIA roles handled deterministically via headless hook or primitive
- [ ] **React 19 idioms used**: direct `ref` prop, `use(Context)` hook, `<Context value={...}>`, `useId()` for forms
- [ ] shadcn v4 `FieldGroup` + `Field` with `useId()` for form layouts
- [ ] `InputGroup` for compound inputs with `:focus-within` rings
- [ ] Base UI `render` prop used for state injection/polymorphic tags; Radix `asChild` for single-child delegation
- [ ] headless hooks extracted: `useDialog`, `useDropdown` returning `{ state, actions, triggerProps, contentProps }`
- [ ] explicit pre-composed variants provided for common high-frequency use cases
- [ ] behavioral interaction tests verify compound composition and accessibility contracts
- [ ] `ui-component-spec.json` and `implementation-result.json` emitted and validated

## Failure Modes

- **Boolean Sprawl Regression**: an engineer adds `isSecondaryHeader` or `withActionButton` to an existing component instead of a compound slot. Mitigation: code review gate rejects PRs adding layout-altering booleans; requires compound refactor.
- **Event Handler Collision in Slot**: child `onClick` overwrites trigger `onClick`. Mitigation: always use `composeEventHandlers` to ensure both internal logic and consumer callbacks execute.
- **Broken Ref Forwarding**: custom child passed to `asChild` loses ref binding. Mitigation: merge refs using `composeRefs` supporting both callback refs and object refs.
- **Context Null Pointer Exception**: subcomponent rendered outside Provider crashes. Mitigation: context consumer hook throws helpful diagnostic error (`useComposerContext must be used within Composer.Provider`).
- **React 19 Migration Incomplete**: `forwardRef` or `useContext()` remains in codebase. Mitigation: codemod for `forwardRef` removal; lint rule for `use(Context)` vs `useContext()`.
- **shadcn v3 Form Legacy**: `FormItem`/`FormControl` boilerplate persists. Mitigation: codemod for `FieldGroup`/`Field` migration; lint rule banning legacy form components.
- **Base UI/Radix Misuse**: `render` prop used for simple delegation; `asChild` used when state injection needed. Mitigation: decision tree in code review; documented pattern examples.
- **Headless Hook State Leakage**: internal state exposed in hook return. Mitigation: strict return type `{ state, actions, triggerProps, contentProps }`; no internal state exposure.
- **Ref Forwarding Broken in `asChild`**: custom child loses ref binding. Mitigation: `composeRefs` supporting callback and object refs; test with `forwardRef` components.

## Output Contracts

When this skill is invoked as part of a coordinated frontend slice, emit:

- **`contracts/schemas/ui-component-spec.json`** — Declares compound component hierarchy, subcomponent contracts, prop interfaces, and slot capabilities.
- **`contracts/schemas/implementation-result.json`** — Records files modified, components created/refactored, test coverage, and public prop surface changes.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: ensure consumer-provided action callbacks cannot override core permission guards inside the component provider.
- **ASI04 Supply Chain**: avoid unvetted heavy component utility bundles; implement lightweight `Slot` and composition primitives locally under `src/components/ui/` or vetted packages (`@radix-ui/react-slot`).
- **ASI05 RCE Guard**: never render dynamic component types from untrusted user input; validate variant names against compile-time string literal unions.
- **ASI07 Inter-Agent Communication**: emit structured `ui-component-spec.json` documenting the compound component hierarchy for downstream UI and QA agents.

## Related Skills

- **add-ui-component**: Author and style the presentation elements of the composed component
- **frontend-testing**: Author behavioral interaction and accessibility test suites
- **setup-design-system**: Align compound component tokens and styling with design system rules
- **review-code**: Audit components for boolean prop sprawl and composition anti-patterns
- **implement-view-transitions**: Animate layout state changes and morphs across composed elements
- Companion example: `examples/headless-combobox-compound-component.tsx`

Last updated: 2026-11-08