---
name: build
description: >
  Build frontend components from design prototypes. Triggers on: "build from design",
  "implement this design", "prototype to code", "design to frontend", "implement this UI",
  "turn this design into code", "code this mockup".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Agent
---

# Frontend Craft — Design to Components

Transform design prototypes into maintainable, component-based frontend code through structured analysis and incremental generation.

## Core Principles

1. **Components, not pages** — Always generate one component at a time. Never produce an entire page in a single pass.
2. **Tokens, not values** — Every visual property (color, spacing, font size) must reference a design token. No hardcoded hex codes, pixel values, or magic numbers.
3. **Libraries first** — Use existing component library primitives (shadcn/ui, Radix, Element Plus, etc.) before building custom implementations. Do not reimplement datepickers, modals, tables, or select menus.
4. **Match conventions** — In existing projects, mirror the established code style, naming, directory structure, and patterns exactly.
5. **Confirm before code** — The architecture plan (Phase 2) must be confirmed by the user before any code is written.

---

## Phase 0: Input Validation

### Required Inputs

1. **Design prototype** — image file path (PNG, JPG, WebP), PDF path, or screenshot
2. **Tech stack** — framework + styling + component library

### Procedure

1. Verify the design file exists and is readable. Use the **Read** tool for images and PDFs.
2. If the user did not specify a tech stack, ask with **AskUserQuestion**:
   - Framework: React / Next.js, Vue 3 / Nuxt, Svelte / SvelteKit, Other
   - Styling: Tailwind CSS, CSS Modules, styled-components / CSS-in-JS, UnoCSS, Other
   - Component library (optional): shadcn/ui, Radix UI, Headless UI, Element Plus, Naive UI, None
3. Detect whether this is an existing project or a new one:
   - Scan for `package.json`, `tsconfig.json`, `vite.config.*`, `next.config.*`, `nuxt.config.*`, `svelte.config.*`
   - **Existing project**: scan code conventions before proceeding:
     - Naming conventions (file names, component names, variable names)
     - Directory structure (where components, pages, styles live)
     - Already-used component libraries and utilities
     - State management approach (useState, Zustand, Pinia, Svelte stores, etc.)
     - Styling approach in use
   - **New project**: note that scaffolding is needed in Phase 3

---

## Phase 1: Design Analysis

Read the design prototype using the **Read** tool. Produce a structured analysis covering:

### 1.1 Visual Hierarchy

Identify top-level layout regions: header, navigation, sidebar, main content, footer, overlays. Note their spatial relationships and nesting.

### 1.2 Color System

Extract colors and classify them:

| Role | Example | Usage |
|------|---------|-------|
| Primary | `#3B82F6` | CTAs, active states, links |
| Secondary | `#6366F1` | Supporting accents |
| Accent | `#F59E0B` | Highlights, badges |
| Neutral | `#1F2937`, `#F3F4F6` | Text, backgrounds, borders |
| Semantic | `#EF4444`, `#22C55E` | Error, success states |

Refer to [DESIGN-ANALYSIS.md](references/DESIGN-ANALYSIS.md) for extraction methodology.

### 1.3 Typography System

Identify font hierarchy:

| Level | Properties |
|-------|-----------|
| Heading 1 | font-family, size, weight, line-height |
| Heading 2 | ... |
| Body | ... |
| Caption / Small | ... |

### 1.4 Spacing System

Infer the base spacing unit and common patterns. Look for the smallest repeated gap and derive the scale (e.g., 4px base: 4, 8, 12, 16, 24, 32, 48, 64).

### 1.5 Interactive Elements

Catalog all interactive elements: buttons (variants, sizes), inputs, selects, toggles, checkboxes, links, tabs, modals, dropdowns.

### 1.6 Responsive Clues

If the design includes multiple viewport sizes, note breakpoint behavior. If only one size is provided, infer a reasonable responsive strategy.

---

## Phase 2: Architecture Planning

**This phase requires user confirmation before proceeding to code.**

### 2.1 Component Tree Decomposition

Apply Atomic Design principles. Refer to [COMPONENT-ARCHITECTURE.md](references/COMPONENT-ARCHITECTURE.md) for methodology.

Break the design into:

- **Atoms**: Smallest indivisible UI elements (Button, Input, Badge, Avatar, Icon)
- **Molecules**: Combinations of atoms (SearchBar, FormField, NavLink, Card)
- **Organisms**: Complex sections composed of molecules (Header, Sidebar, ProductGrid, CommentSection)
- **Templates**: Page-level layouts that arrange organisms
- **Pages**: Templates populated with real content and data

For each component, define:
- Name
- Responsibility (one sentence)
- Props interface draft (key props, types, defaults)
- State requirements (local state, context, global store)
- Children / composition pattern

### 2.2 Design Tokens

Map the Phase 1 analysis to the tech stack's token format:

| Tech Stack | Token Format |
|-----------|-------------|
| Tailwind CSS | `tailwind.config.ts` — extend theme |
| CSS Modules / vanilla | CSS custom properties in `variables.css` |
| styled-components | Theme object in `theme.ts` |
| UnoCSS | `uno.config.ts` — extend theme |

Tokens must cover: colors, spacing scale, typography scale, border radii, shadows, breakpoints.

### 2.3 File Structure Plan

Propose the directory layout for new components, following existing project conventions (or sensible defaults for new projects).

### 2.4 Reusable Library Components

Identify which components from the chosen component library can be used directly or composed, avoiding custom reimplementation.

### 2.5 State Management Plan

Based on complexity, recommend:

| Complexity | Approach |
|-----------|---------|
| Simple (single component state) | Local state (useState, ref, $state) |
| Shared across siblings | Lift state / Context / provide-inject |
| App-wide or complex | Zustand, Pinia, Svelte stores |

### 2.6 User Confirmation Gate

Present the full architecture plan to the user via **AskUserQuestion**:

- Component tree (names and hierarchy)
- Design tokens summary
- File structure
- Library components to use
- State management approach

Options: **Approve** / **Approve with changes** / **Revise**

**Do not write any code until the user approves.**

---

## Phase 3: Foundation Setup

### New Project

1. Scaffold using the appropriate CLI tool via **Bash**:
   - `npx create-next-app@latest` / `npm create vite@latest` / `npx nuxi init` / `npm create svelte@latest`
2. Install styling dependencies (Tailwind, etc.)
3. Install chosen component library

### Existing or New Project

1. Generate design tokens configuration file:
   - Tailwind: extend `tailwind.config.ts`
   - CSS variables: create or update `globals.css` / `variables.css`
   - Theme object: create `theme.ts`
2. Generate base layout component(s) — the outermost shell (e.g., root layout with header/sidebar/main slots)
3. Install additional dependencies as needed via **Bash**

---

## Phase 4: Component Generation

This is the core phase. Generate components **one at a time**, in dependency order.

### Generation Order

1. Atoms (no dependencies on other custom components)
2. Molecules (depend on atoms)
3. Organisms (depend on molecules and atoms)

### Per-Component Rules

For each component:

1. **Follow project conventions** — match existing naming, file structure, export patterns
2. **Use design tokens** — every color, spacing, font-size, border-radius, shadow must come from tokens. No hardcoded values.
3. **Prefer library components** — use the chosen component library's primitives where applicable
4. **Responsive handling** — include at minimum mobile + desktop breakpoints
5. **TypeScript types** — if the project uses TypeScript, define a props interface
6. **File size limit** — if a component exceeds ~100 lines, extract sub-components
7. **Accessibility baseline** — semantic HTML, aria labels for non-obvious elements, keyboard focusability for interactive elements

Refer to [CODE-GENERATION.md](references/CODE-GENERATION.md) for tech-stack-specific conventions.

### Generation Pattern

For each component:

```
1. Create the component file
2. Define the props interface (TS projects)
3. Implement the component using design tokens and library primitives
4. Add responsive styles
5. Export the component
```

---

## Phase 5: Page Assembly

Once all components are generated:

1. **Compose the page** — import and arrange organisms within the template/layout
2. **Add data fetching** — if the design implies dynamic content, add data fetching logic appropriate to the framework (Server Components, `getServerSideProps`, `useFetch`, `load` functions)
3. **Add routing** — configure routes if the page needs to be accessible via URL
4. **Wire up interactions** — connect state, event handlers, and any cross-component communication

---

## Phase 6: Quality Review

Run through the checklist in [QUALITY-CHECKLIST.md](references/QUALITY-CHECKLIST.md).

Key checks:

- [ ] All colors reference design tokens
- [ ] All spacing values reference the spacing scale
- [ ] No inline magic numbers
- [ ] TypeScript interfaces defined for all component props (TS projects)
- [ ] Interactive elements have hover, focus, and active states
- [ ] Semantic HTML tags used appropriately
- [ ] Basic keyboard navigation works for interactive elements
- [ ] Responsive styles cover at least mobile + desktop
- [ ] No unused imports
- [ ] No component file exceeds 200 lines

### Deliverables

After completing the review, provide:

1. Summary of generated components (name, file path, line count)
2. Design token configuration location
3. Remaining items that require follow-up:
   - Real API endpoints to connect
   - Additional interaction states to implement
   - Missing assets (icons, images) to replace placeholders
   - Animations or transitions not covered

---

## Reference Documents

- [DESIGN-ANALYSIS.md](references/DESIGN-ANALYSIS.md) — How to extract visual systems from design prototypes
- [COMPONENT-ARCHITECTURE.md](references/COMPONENT-ARCHITECTURE.md) — Component decomposition and props design methodology
- [CODE-GENERATION.md](references/CODE-GENERATION.md) — Tech-stack-specific code conventions and patterns
- [QUALITY-CHECKLIST.md](references/QUALITY-CHECKLIST.md) — Complete quality verification checklist
