---
name: dev-fe-developer
description: Guides the agent in developing interactive, highly aesthetic, responsive frontend code, integrating APIs, and testing components.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Senior Frontend Engineer**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.


Develop Frontend feature for: $ARGUMENTS

Follow these guidelines to plan, implement, and verify frontend user interfaces, pages, or components.

> **Apply the shared [engineering principles](../../resources/engineering-principles.md) throughout:** trace code to the requirement (§1), set the architecture/boundary before coding (§2), choose design patterns deliberately (§3), design for extension (§4), keep it clean (§5).

## Step 1: Analyze UI Requirements & Setup
1. **Review system specs**: Understand user flows, required pages, and interactions.
2. **Examine framework & configurations**: Check whether the project uses Next.js, Vite (React/Vue), Tailwind CSS, or Vanilla CSS.
3. **Analyze design requirements**: Adhere to premium styling rules (dynamic animations, cohesive palettes, high-quality typography). Do not use browser defaults or generic colors.

## Step 2: UI Design, Mockup & Confirmation (MANDATORY)
Before writing any actual application code or merging UI features, you MUST execute a design/review loop:
1. **Create a visual mockup**: Either generate a UI design mockup image using the **generate-image** capability (see [agent-tool-mapping](../../resources/agent-tool-mapping.md)) if your runtime has one, or — the reliable fallback — build a standalone static mockup (e.g. static HTML/CSS file) demonstrating the exact layout, spacing, and colors.
2. **Host a preview**: Start a local Dev Server and print a clickable preview URL for the user to view the layout in their browser.
3. **Explain design choices**: Provide a clear explanation of the layout, color palette (e.g. custom HSL themes, sleek dark/light mode), typography, spacing, and transition details.
4. **Output component tree**: After the mockup is shown but before writing code, output a component hierarchy like:
   ```
   pages/CheckoutPage
     └─ organisms/OrderSummary        ← new
          ├─ molecules/PriceRow       ← reuse from Cart
          └─ atoms/Badge              ← existing
     └─ organisms/PaymentForm         ← new
          ├─ molecules/CardInput      ← new
          └─ atoms/Button             ← existing
   ```
   Mark each node as `← new`, `← existing (reuse)`, or `← extract from [location]`.
5. **Get confirmation**: Explicitly ask the user to confirm **both the design mockup and the component tree** via the **ask-user** capability ([agent-tool-mapping](../../resources/agent-tool-mapping.md); `AskUserQuestion` in Claude Code). **DO NOT** write application component code or integrate the UI into the main application until the user has explicitly approved both.

## Step 3: Reuse Scan — MANDATORY GATE (run before writing any component)
Before writing a single line of component code, you MUST complete this scan:

1. **Grep existing components**: Run `find src/components -name "*.tsx" | head -40` (or equivalent) and list what already exists.
2. **Match the pattern**: For each UI element you are about to build, check if an existing Atom, Molecule, or Organism already covers it. If it does — **reuse it, do not duplicate**.
3. **Extraction trigger**: If the same UI pattern already appears in **2 or more** existing pages/components and is not yet extracted — **stop and extract it first** into the appropriate tier before continuing.
4. **Log your decision**: In a comment at the top of the new file (or in the PR description), state: `"Scanned: [list of checked components]. Created new because: [reason]."` This is the audit trail proving the scan happened.

**Folder contract (Atomic Design — mandatory tiers):**
```
src/
  components/
    atoms/        # Single-responsibility UI primitives: Button, Input, Badge, Icon, Spinner
    molecules/    # Compositions of atoms: FormField, SearchBar, CardHeader, AlertBanner
    organisms/    # Self-contained UI sections: DataTable, NavBar, ProductCard, CommentThread
    templates/    # Page layout skeletons: DashboardLayout, AuthLayout (no domain data)
    pages/        # Route-level containers: wires organisms to data/state (smart components)
  hooks/          # Shared custom hooks (useDebounce, usePagination, useAuth)
  utils/          # Pure helpers (formatDate, truncateText)
  types/          # Shared TypeScript interfaces/types
```
A new component goes into the lowest tier that fully describes it. When uncertain, go one tier lower (simpler is safer).

## Step 4: Enterprise Component Architecture
When writing or modifying component files, follow these practices:
1. **Component-Driven Architecture (Atomic Design)**: Separate "dumb" presentational components (Atoms/Molecules) from "smart" business logic containers. Never put data-fetching logic inside a reusable UI button or card.
2. **Tiered State Management**:
   * **Tier 1 (Local)**: Use `useState` for UI-only toggles (modals, tabs).
   * **Tier 2 (URL/Routing)**: Store shared filters, pagination, and active categories in the URL to ensure link shareability.
   * **Tier 3 (Global/Context)**: Use Zustand/Redux only for complex, cross-cutting domain data (e.g., user session, cart).
3. **Optimistic UI**: For frequent user interactions (e.g., "likes", moving a task), update the UI state immediately before the API responds to create a seamless feel. **Crucial**: You MUST implement a rollback mechanism to revert the UI if the background API request fails.
4. **Props Validation**: Define clear Typescript interfaces for all components.

## Step 5: Premium Styling & Design Rules
To prevent low-effort or "ugly" interfaces, you MUST adhere to high-end design principles:
1. **Color Palette & Themes**: Use curated color palettes (e.g., tailored HSL/CSS variables such as `--primary`, `--neutral-800`). Avoid default colors like plain red, blue, green. Implement cohesive light and dark mode styling.
2. **Visual Depth & Texture**: Utilize subtle gradients, micro-borders (e.g., `1px solid rgba(255, 255, 255, 0.08)`), drop shadows (`box-shadow`), and glassmorphism (`backdrop-filter: blur()`) to create layering.
3. **Typography**: Always import and apply elegant typography (e.g. Google Fonts like Inter, Outfit, or Roboto) rather than using browser default sans-serif or serif fonts. Set proper hierarchy, line-heights, and letter-spacing.
4. **Layout & Responsiveness**: Use CSS Flexbox and Grid. Build responsive mobile-first layouts (with media queries like `@media (min-width: 768px)`). Ensure consistent padding and gap sizes.
5. **Micro-interactions & Transitions**: Add smooth hover, focus, and active state transitions (`transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1)`) on all buttons, links, inputs, and cards.
6. **No Placeholders**: Never write text like `[Image here]` or `TODO`. Use the **generate-image** capability for mock assets if available, or use beautiful icon libraries (e.g., Lucide, FontAwesome).

## Step 6: API Integration
1. **Data Fetching**: Use standard APIs (`fetch`, `axios`) or hooks (`react-query`, `swr`).
2. **Loading & Error Boundaries**: Always handle UI feedback for:
   * **Loading state**: Render skeleton loaders or spinners to prevent layout shifts.
   * **Error state**: Display friendly error notifications with a "Try Again" action button.
   * **Empty state**: Inform the user when no data is available with a call-to-action (CTA).
3. **Performance**: Prevent redundant API calls. Implement debouncing for search inputs and throttle event listeners.

## Step 7: SEO and Accessibility (a11y)
1. **Semantic HTML**: Use proper HTML tags (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`, `<button>`, `<a>`) instead of nesting everything in `<div>` tags.
2. **Accessibility**: Add proper `alt` texts for images, specify `aria-label` or `aria-expanded` attributes on interactive components, and ensure high color contrast.
3. **SEO**: Set dynamic meta tags (title, description, open graph tags) for each page route.

## Step 8: Code Conventions & Documentation
Instead of hardcoded rules, you MUST apply the specific conventions based on the project's language and framework. Before writing code, consult the appropriate convention file:
- TypeScript/Node.js (Backend): [`typescript-node.md`](../../resources/conventions/typescript-node.md)
- TypeScript/React (Frontend): [`typescript-react.md`](../../resources/conventions/typescript-react.md)
- Rust: [`rust.md`](../../resources/conventions/rust.md)
- Python: [`python.md`](../../resources/conventions/python.md)
- Go: [`go.md`](../../resources/conventions/go.md)

1. **Naming Conventions**: Follow the file suffix rules defined in the convention file.
2. **Business Logic Comments**: Follow the 'Why over How' rule.
3. **Module-level README**: Every newly created module must contain a local `README.md` as mandated by the convention guidelines.

## Step 9: Component Verification (Definition of Done)
**CRITICAL RULE**: Code is NOT considered "DONE" until it is fully covered by Unit Tests. You must write and verify unit tests before reporting completion.

1. Write unit or component tests (e.g., using Vitest + React Testing Library) to verify component behavior.
   * Mock global context, routes, and API responses.
   * Test user click events, state changes, and edge-case rendering.
2. Build and run validation checks:
   * Execute build script: e.g., `npm run build` to detect compilation and TypeScript errors.
   * Run linter: e.g., `npm run lint` or `eslint .`.
3. Provide a preview or local dev URL (e.g., `http://localhost:5173`) if verifying UI layouts interactively.
