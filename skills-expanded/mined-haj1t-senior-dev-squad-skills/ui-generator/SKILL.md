---
name: ui-generator
description: "Generates production-ready UI components from specs, design system oriented, real code output. Use when building UI components from a design or specification."
---

# UI Generator — Converting Design to Code

## Overview

UI Generator takes a specification document and design system configuration to generate production-ready, framework-specific UI components. Inspired by the Open Design (nexu-io/open-design — 46K★) approach, it does not output wireframes or mockups; it produces directly executable code. It combines component tree extraction, design system primitive mapping, prop types, state management, accessibility, responsive guidelines, and form/data/navigation templates into a single pipeline.

**Core principle:** No UI component remains abstract — no code is generated for a piece without mapping it to a concrete primitive in the design system.

## The Iron Law

```
NEVER GENERATE CODE FOR A COMPONENT WITHOUT MAPPING IT TO A DESIGN SYSTEM PRIMITIVE.
A COMPONENT IS NOT CONSIDERED COMPLETE UNTIL EVERY STATE DESCRIBED IN THE SPECIFICATION (LOADING, EMPTY, ERROR, SUCCESS, DISABLED) IS ENTIRELY COVERED.
```

## When to Use

**Use this when:**
- A written specification (spec document) exists for a page or screen.
- A design system (e.g., ShadCN/Radix, Material UI, Chakra, Ant Design, custom) is defined for use.
- The component/screen type is clear (form, data table, modal, sidebar, page, etc.).
- Production-quality code is needed to integrate with the existing project structure.

**Use this ESPECIALLY when:**
- Manually coding the entire page would take hours and involves repetitive patterns.
- You plan to reuse the same design system components in multiple places.
- State management (loading, error, empty, success) and accessibility must be implemented uniformly.

**Don't skip when:**
- Developing a small form with only two inputs — proper state/validation/accessibility are still required.
- Under time pressure — UI Generator saves the most time in this exact scenario.

## Phase 1: Analyzing the Specification and Extracting the Component Tree

**BEFORE proceeding:**
Verify that the design system configuration (package name, import paths, existing primitives) is ready.

1. **Read the specification and extract the component hierarchy** — break down the page/screen into atomic parts. Define each part as a component.
2. **Determine component relationships** — establish parent/child, sibling, and containment relationships. Which component contains which?
3. **Label each component's type**: Layout (container, grid, stack), Data Display (table, list, card), Input (form field, button, select), Navigation (menu, tabs, breadcrumb), Feedback (modal, toast, alert), or Composite (a mixture of the above).

```yaml
# Example output — component tree in YAML format
components:
  - name: UserProfilePage
    type: page
    children:
      - name: ProfileHeader
        type: data-display
        children:
          - name: Avatar
          - name: UserName
          - name: EditButton
      - name: ProfileForm
        type: form
        children:
          - name: NameField
          - name: EmailField
          - name: SaveButton
```

## Phase 2: Performing Design System Mapping

**BEFORE proceeding:**
Is the design system config file (e.g., `design-system.config.json`) present? Has the list of available primitives been extracted?

1. **Map each component to the correct design system primitive** — e.g. `Avatar` → `Avatar` (ShadCN), `Table` → `Table, TableHeader, TableRow, TableCell` (MUI), `Card` → `Card, CardContent, CardMedia` (Chakra).
2. **If no mapping is found** — either flag it as a custom component and add inline style/requirement notes, or suggest an appropriate alternative primitive.
3. **Specify import paths correctly** — according to the framework (React: `import { Button } from "@/components/ui/button"`, Vue: `import Button from "@/components/ui/Button.vue"`).

```yaml
# Example mapping table
mappings:
  Avatar: { primitive: "Avatar", source: "@radix-ui/react-avatar", import: "import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'" }
  DataTable: { primitive: "Table", source: "@tanstack/react-table", import: "import { useReactTable, getCoreRowModel } from '@tanstack/react-table'" }
```

## Phase 3: Generating Props and States

**BEFORE proceeding:**
Are the component tree and design system mapping complete? Is it clear what data each component will accept from the user (props)?

1. **Define prop types** — required/optional props, TypeScript interfaces, and default values for each component.
2. **Identify variants** — design system-supported variants such as `size` (sm/md/lg), `variant` (primary/secondary/ghost/danger), `colorScheme`, etc.
3. **Cover states** — fully define the following states for each component:
   - **Loading** — skeleton/spinner display.
   - **Empty** — "No data found" message, empty state illustration.
   - **Error** — error message, retry button.
   - **Success** — feedback after a successful operation (toast, snackbar, confirmation text).
   - **Disabled** — button/input disabled state, visual cue.

```typescript
// Example — TypeScript interface
interface DataTableProps<T> {
  data: T[];
  columns: ColumnDef<T>[];
  isLoading?: boolean;
  isEmpty?: boolean;
  error?: Error | null;
  onRetry?: () => void;
  variant?: 'default' | 'striped' | 'bordered';
  size?: 'sm' | 'md' | 'lg';
}
```

## Phase 4: Adding Responsive and Accessibility Layers

**BEFORE proceeding:**
Are the design system's responsive utilities (breakpoints, grid system) and accessibility guidelines (ARIA, keyboard navigation) documented?

1. **Add responsive props** — use design system responsive helpers for mobile/tablet/desktop breakpoints:
   - Tailwind: `className="flex flex-col md:flex-row lg:grid lg:grid-cols-3"`
   - CSS Modules: CSS classes with media queries
   - styled-components: breakpoint templates using the `css` helper
2. **Perform an accessibility pass** — for each component ensure:
   - ARIA roles (`role="dialog"`, `role="tablist"`, `role="navigation"`)
   - ARIA labels (`aria-label`, `aria-describedby`, `aria-live`)
   - Keyboard navigation (`onKeyDown`, tabIndex, focus trap)
   - Focus management (bring focus inside when a modal opens, restore it when closed)
3. **Color contrast** — verify that the text/background contrast ratio complies with the WCAG AA (4.5:1) standard.

## Phase 5: Generating Component Code by Type

**BEFORE proceeding:**
Is the component type from the specification (form, data display, navigation, etc.) clear? Has the framework choice been finalized?

1. **Form generation:**
   - Map input fields to design system form components.
   - Add validation rules (required, minLength, pattern, custom validator).
   - Display error messages (below each input).
   - Submit handler, loading state (button disabled + spinner), success/error toast.
   - Form reset and initial values.

2. **Data display generation:**
   - Table: column definitions, sorting, filtering, pagination, row selection.
   - List: items, virtual scrolling (for large lists), empty state.
   - Card grid: responsive grid layout, card hover effects, loading skeleton.
   - All: loading skeleton, empty state, error state, retry mechanism.

3. **Navigation generation:**
   - Menu: highlight active item, nested menu, mobile hamburger.
   - Tab: active tab indicator, tab panel content, keyboard navigation.
   - Breadcrumb: automatic path-to-crumb mapping.
   - Sidebar: collapsible, active state, icon + label.
   - Modal/Drawer: open/close state, backdrop, close on ESC, focus trap.

```
# Framework-specific code output formats
# 1. React TSX: Component.tsx, Component.types.ts, Component.styles.ts
# 2. Vue SFC: Component.vue (template, script, style)
# 3. Svelte: Component.svelte
```

## Phase 6: Generating Style Output

**BEFORE proceeding:**
Which styling approach does the design system use? (Tailwind, CSS Modules, styled-components, Emotion, vanilla CSS, SCSS)

1. **Detect styling approach** — match the project's existing styling solution.
2. **Tailwind**: merge utility classes correctly, use conditional classes with a `cn()` helper (class-variance-authority, clsx/twMerge).
3. **CSS Modules**: write a dedicated `.module.css` file for each component, use CSS custom properties for theme support.
4. **styled-components**: write component-level styles using `styled.div`, `styled.button`, and breakpoints with the `css` helper.
5. **Design tokens**: use color, spacing, typography, and shadow tokens from the design system — DO NOT use magic numbers.

## Phase 7: Integration and Final Verification

**BEFORE proceeding:**
Is the project structure (folder hierarchy, import aliases, routing configuration) known?

1. **Adjust import paths to match project structure** — e.g. `@/components/ui/`, `@/lib/`, `@/types/`.
2. **Integrate the page/component file into the existing routing structure** — add lazy loading or route guards if required.
3. **Verify all components import each other correctly** — check for circular imports and missing exports.
4. **Add test coverage notes** — comments indicating which states need unit or integration testing.

**Final verification checklist:**

BEFORE checking off:

- [ ] Is every component mapped to a design system primitive?
- [ ] Are loading, empty, error, success, and disabled states implemented for each component?
- [ ] Are responsive breakpoints (mobile < tablet < desktop) applied?
- [ ] Accessibility: are ARIA roles, labels, keyboard navigation, and focus management included?
- [ ] Forms: are validation, error messages, and submit handling fully coded?
- [ ] Data display: are pagination, sorting, filtering, and empty states complete?
- [ ] Are import paths aligned with the project's existing alias and linting rules?
- [ ] Are style tokens (color, spacing, typography) taken directly from the design system without magic numbers?
- [ ] Is the framework-specific syntax (TSX/Vue SFC/Svelte) correct?
- [ ] Does the code compile and run? (lint + typecheck + build)

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I will write this component roughly and fix it later" — Every component must be mapped to the design system from the start.
- "I'll add the loading/empty state later" — If states are not added all at once, they will be forgotten.
- "This is a small component, ARIA is not needed" — Accessibility is built from the start, not tacked on later.
- "I'll use a magic number now and convert it to a token later" — It will never be converted, and will remain as technical debt.
- "Let's build only for desktop first, mobile responsiveness later" — Responsive design cannot be bolted on; it must be planned from the start.

**ALL of these mean: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Which design system component does this use?" — You skipped the design system mapping. Go back to Phase 2.
- "What if no data is returned?" — You skipped empty/error states. Go back to Phase 3.
- "How will this look on mobile?" — You skipped the responsive layer. Go back to Phase 4.
- "Can I switch between these tabs using a keyboard?" — You skipped accessibility. Go back to Phase 4.
- "Is this consistent with other components in the project?" — You set up styling tokens or import paths incorrectly. Go back to Phase 6-7.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll output a working version first, then add the states" | Adding states changes the component's structure; adding them from the start is faster. |
| "No need to look at the design system docs, I know it" | Every design system has subtle differences; not checking documentation leads to incorrect imports/props. |
| "A small input like this does not need responsiveness" | All components must be responsive; a form can become entirely unusable on mobile. |
| "ARIA labels just clutter the DOM" | ARIA labels are invisible and accessibility is a legal requirement (WCAG). |
| "Using magic numbers in styled-components is faster" | Magic numbers are technical debt; theme modifications become impossible without design tokens. |
| "Writing this component manually is faster" | This might be true for a single component; however, once the pattern repeats, UI Generator saves exponential time. |

## Related Skills

- **code-generator** — Use alongside route/page generator to place components generated by UI Generator into pages.
- **spec-writer** — This skill can be used beforehand to write the specification document that serves as input for UI Generator.
- **design-system-analyzer** — Extracts a config file by analyzing the project's existing design system.
- **test-generator** — Generates unit/E2E tests for the components produced by UI Generator.
- **storybook-generator** — Automatically generates Storybook documentation for the produced components.

## Self-Review

After completing this skill's process:

1. **Coverage Check:** Has every visual/functional element in the spec been converted to code? Are all states (loading, empty, error, success, disabled) covered?
2. **Edge Case Check:** Are edge cases such as long text, excessive rows, empty lists, API errors, network timeouts, and unauthorized access handled?
3. **Quality Check:** Does the code comply with the project's linting, formatting, and typing rules? Were the design system primitives used correctly? Are accessibility standards met? Were both rules in the Iron Law fully implemented?
