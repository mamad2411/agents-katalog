---
name: react-component-scaffolder
audience: team
description: >
  Scaffolds a single React / TypeScript component or route with a typed props interface, a
  co-located React Testing Library test, an accessibility baseline, and an optional Storybook
  story. React analog of fastapi-scaffolder — the component/route is the front-end "unit". Use
  when creating a new React component, adding a route/page, generating a typed presentational or
  container component, or standing up a component with its test and story.
---

# React Component Scaffolder

> "A component is a contract. Make its props explicit, its output accessible, its behavior tested."
> -- Adapted from API design practice

> "Accessibility by default means the inaccessible path requires more work than the accessible one."
> -- Adapted from OWASP Secure Design Principles

## Core Philosophy

A React component is the front-end unit the way an endpoint is the back-end unit. Like an endpoint, it
has a contract (its props), an output that must be safe and well-formed (accessible, escaped JSX), and a
test that proves it behaves. A component shipped without a typed props interface, a test, and an
accessibility baseline is a black box that future changes will break silently.

Accessibility by default means semantic HTML and keyboard support are the scaffold, not a follow-up
ticket. The inaccessible `<div onClick>` must be the path that requires extra justification.

> **Grounding note:** the KB has no React corpus. Use `collection="javascript"` for TS, `collection="ui_ux"`
> for WCAG/ARIA, and cite **react.dev** for component/hook patterns. Never invent a `react` collection.

**Non-Negotiable Constraints:**
1. **Typed props** — every component has an explicit `Props` type/interface; no implicit `any`
2. **Test co-located** — a `*.test.tsx` is created with the component, not after
3. **Accessible by default** — semantic elements, labels, keyboard reachability; `eslint-plugin-jsx-a11y` clean
4. **Presentational by default** — a new component takes data + callbacks via props; data fetching is opt-in and explicit
5. **No business logic in JSX** — branching/logic goes in a hook or a prop callback

**What this skill is NOT:**
- It is NOT a feature-architecture tool — use `react-feature-slice` to organize many components
- It is NOT an app bootstrapper — use `react-app-scaffolder` to create the project skeleton
- It is NOT a styling system — bring your own (CSS Modules, Tailwind, etc.)

The 10 domain principles, KB lookup queries, AI discipline rules, anti-patterns, and error-recovery
procedures live in `references/conventions.md`.

## Workflow

### Phase 1: DETECT

```bash
# React + TS + test runner + storybook
grep -E '"(react|typescript|vitest|jest|@testing-library/react|@storybook)"' package.json

# Where components live and the existing convention
find src -type d -name components | head
ls src/features 2>/dev/null

# Test + story file conventions already in use
find src -name "*.test.tsx" | head -3
find src -name "*.stories.tsx" | head -3
```

Record: React version, test runner (Vitest/Jest), whether Storybook is present, naming/location convention.

### Phase 2: SCAFFOLD

**Objective:** Create the component with its typed props, test, and (optional) story.

See `references/component-template.md` for full skeletons (presentational, container, form).

```
src/<location>/<Name>/
  <Name>.tsx              # the component (presentational by default)
  <Name>.test.tsx          # RTL test (co-located, required)
  <Name>.stories.tsx       # Storybook story (optional)
  index.ts                 # re-export
```

### Phase 3: ACCESSIBILITY

**Objective:** Meet the a11y baseline. See `references/accessibility-baseline.md`.

```bash
npx eslint src/<location>/<Name> --plugin jsx-a11y
```

### Phase 4: VERIFY

```bash
npx tsc --noEmit
npx eslint src/<location>/<Name>
npx vitest run src/<location>/<Name>
# Story renders (if Storybook present):
npx --no-install storybook build --quiet >/dev/null 2>&1 && echo "stories build OK"
```

## State Block

```xml
<react-component-scaffold-state>
  phase: DETECT | SCAFFOLD | ACCESSIBILITY | VERIFY | COMPLETE
  component_name: [name]
  kind: presentational | container | form | route
  test_runner: vitest | jest
  storybook_present: true | false
  props_typed: true | false
  test_created: true | false
  a11y_clean: true | false | not_run
  last_action: [description]
  next_action: [description]
</react-component-scaffold-state>
```

## Output Template

The scaffold checklist (Contract / Accessibility / Tests / Story / Verification) lives in
`references/conventions.md` under "Output: Scaffold Checklist". Emit it filled-in at COMPLETE.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `react-feature-slice` | Provides the feature structure; this skill generates the individual components inside a slice. |
| `react-app-scaffolder` | Stands up the project (Vite + TS + Vitest + Storybook) this skill scaffolds components into. |
| `react-security-review` | After scaffolding, audit link/URL handling and any raw-HTML usage in the component. |
| `react-architecture-checklist` | Quality gate for hooks discipline and render performance across components. |
| `tdd-loop` | Drive the component test-first (RED → GREEN → REFACTOR) instead of scaffolding code ahead of the test. |
