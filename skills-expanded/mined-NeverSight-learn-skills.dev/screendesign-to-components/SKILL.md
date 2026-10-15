---
name: screendesign-to-components
description: 'Extracts Angular components from a screen design image. Analyzes the design pixel-perfectly, decomposes it into a component tree, identifies reusable shared UI, and implements each component with Tailwind CSS / DaisyUI. Use when the user provides a screenshot, mockup, or screen design and wants it turned into Angular components.'
---

# Screendesign → Components

## Purpose

Transform a screen design (image / screenshot / mockup) into a fully implemented, pixel-perfect Angular component tree. Every visual area of the design becomes an explicit component or sub-component — nothing is left as unstructured HTML.

## Workflow

### Phase 0 — Product Context & Source Material

Before visual analysis, collect all available context for the screenshot.

1. **Locate the source image** and record its filename, dimensions, and target feature name.
2. **Search `docs/` for PRDs or functional documentation** related to the screenshot, feature name, route, business term, or nearby domain language:
   - use `rg -n "<feature|route|domain term>" docs`
   - check common files such as `docs/prd*.md`, `docs/**/prd*.md`, `docs/**/requirements*.md`, `docs/**/spec*.md`, and `docs/**/user-stories*.md`
   - if no docs exist, explicitly note "No matching product docs found" in `docs/screendesign-conversion/<feature-name>.md`
3. **Extract functional requirements** from matching docs:
   - user roles and permissions
   - data fields and validation rules
   - workflows, states, and business rules
   - API/backend expectations
   - wording, localization, and compliance constraints
4. **Map visible UI to likely logic.** If the screenshot implies behavior (forms, filters, tabs, selections, sorting, calculations, navigation, persistence, permissions, or async data), plan and implement that logic unless the user explicitly scopes the task to static UI only.
5. **Document assumptions and open questions** in `docs/screendesign-conversion/<feature-name>.md` before coding.

### Phase 1 — Visual Analysis

1. **Open the image** with `view_image` (or ask the user to share it).
2. **Segment the design into visual zones.** For every distinct area, note:
   - position, size, spacing, alignment
   - typography (font weight, size, color, line-height)
   - colors, backgrounds, borders, shadows, border-radius
   - icons, images, illustrations
   - interactive affordances (buttons, inputs, links, toggles, dropdowns)
3. **Produce a component tree** in outline form before writing any code:

   ```
   ScreendesignRoot
   ├── HeaderBar
   │   ├── Logo
   │   └── NavLinks
   ├── HeroSection
   │   ├── Headline
   │   └── CTAButton        ← candidate for shared UI
   ├── CardGrid
   │   └── FeatureCard (×3)  ← candidate for shared UI
   └── Footer
   ```

4. **Produce a logic plan** next to the component tree:
   - component responsibilities
   - signals/state/resources/services needed
   - events and outputs
   - validation and error handling
   - route/query-param behavior
   - data fixtures, API contracts, or stores
5. **Present the tree and logic plan to the user** and wait for confirmation before proceeding. If the user has feedback, revise both first.

### Phase 2 — Shared-UI Audit

Before creating any feature component, check whether a reusable primitive already exists in the workspace.

1. **Scan `libs/shared/ui` and any project-specific UI library** for existing shared components (buttons, cards, dividers, badges, inputs, modals, etc.).
2. **Compare** each candidate in the component tree against the inventory:
   - If a matching component exists → reuse it, adapting inputs/variants as needed.
   - If a similar component exists but lacks a required variant → extend it (add an `@Input`, a CSS variant, or a story).
   - If no match exists → **create it in the shared UI library** (normally `libs/shared/ui`) using the project's generators, not inside the feature library or the app.
3. **Log the audit result** in a brief table before moving on:

   | Design Element | Existing Component | Action |
   |---|---|---|
   | CTA Button | `libs/shared/ui` – *none* | Create `ButtonComponent` in shared UI |
   | Feature Card | `libs/shared/ui` – *none* | Create `CardComponent` in shared UI |
   | Divider | `libs/shared/ui` – *none* | Create `DividerComponent` in shared UI |

### Phase 3 — Implementation

Follow this order strictly:

1. **Shared UI components first.** For each new shared component:
   - Scaffold with `@analog-tools/generator` or the appropriate Nx generator.
   - Implement the component with Tailwind CSS / DaisyUI classes.
   - Match the desktop design pixel-perfectly: exact spacing (`gap-*`, `p-*`, `m-*`), exact colors (design tokens / CSS variables preferred over arbitrary values), exact typography, exact border-radius, exact shadows. Record the desktop reference width used for verification.
   - Add `@Input()` / signals for every variant visible in the design or reasonably anticipated.
   - Write a unit test (TDD: RED → GREEN → REFACTOR).
   - Write a Storybook story covering every visual state and variant.
   - Export from the shared UI public API.

2. **Feature components second.** For each non-shared component:
   - Place it in the appropriate feature library under `libs/<feature>/src/lib/ui/` (or `page/`, `pages/` as applicable).
   - Compose it from shared UI primitives wherever possible.
   - Implement remaining layout and feature-specific markup with Tailwind CSS.
   - Pixel-perfect adherence: compare against the design image zone by zone.
   - Write a unit test.
   - Write a Storybook story.

3. **Page / container component last.**
   - Assemble feature components into the page layout.
   - Ensure responsive behavior: enforce pixel-perfect governance at the desktop reference viewport (the design width used as the pixel-perfect baseline). Mobile and tablet layouts should be intentionally adapted rather than exact pixel matches; document the reference viewport in `docs/screendesign-conversion/<feature-name>.md`.
   - Wire up the logic plan from Phase 1: data bindings, signals, computed values, resources, stores, forms, route/query params, events, permissions, persistence, and async states as needed.
   - If docs/PRD imply backend integration, add or update the API/client/service layer following existing project patterns. If the endpoint does not exist and implementing it is in scope, add it; otherwise use a documented fixture and mark the backend gap.
   - If the screenshot is interactive, implement visible and implied interactions rather than leaving static markup: buttons act, filters filter, tabs switch, forms validate/submit, menus open/close, and navigation targets resolve.
   - For data-driven sections (lists, tables, repeaters):
      - Implement loading, empty, and error states even if the design doesn't show them.
      - Provide skeletons, spinners, or placeholder rows for loading states and clear, actionable empty-state UI that matches the design tone.
      - Implement graceful fallback/error UI and include logging/observability hooks where appropriate.
      - Ask the user which data source, service, or mocked API to bind to (or request a sample JSON fixture). If none is provided, wire to a clearly documented fixture in `libs/<feature>/testing/fixtures/` and note it in the docs.
      - For long or unbounded lists, design for wrapping, virtualization, or pagination and document the expected UX (infinite scroll vs. pagination) in `docs/screendesign-conversion/<feature-name>.md`.

### Phase 3 — Implementation: Final Checklist (Gate)

Before moving to Phase 4, run this checklist for every shared UI component and for the assembled feature/page. Consider this a hard gate: do not proceed to verification until every required item is either completed or intentionally noted in `docs/screendesign-conversion/<feature-name>.md` as an accepted deviation.

Per-component checklist:

- [ ] Scaffolding: component created with the proper generator and placed under the shared UI library (or extended if reusing).
- [ ] Implementation: markup and Tailwind/DaisyUI classes implemented in component template.
- [ ] Pixel fidelity (desktop): spacing, alignment, border-radius, shadows, and layout match the desktop reference design (document reference width).
- [ ] Tokens/colors: colors and semantic tokens used where possible; arbitrary values only if documented.
- [ ] Typography: font family, weight, size, line-height, and letter-spacing match the design.
- [ ] Inputs/variants: `@Input()` / signals exist for visible variants and anticipated variants.
- [ ] Logic: visible or implied behavior from the screenshot and docs is implemented or documented as out of scope.
- [ ] Data/API: fixtures, services, stores, or backend routes are wired according to the logic plan.
- [ ] Accessibility: ARIA attributes, keyboard focus, and semantic HTML verified.
- [ ] Tests: unit test(s) added (TDD flow observed).
- [ ] Stories: Storybook story(s) added covering all states and variants (SDD).
- [ ] Exported: component exported from the shared UI public API (or the appropriate lib index).
- [ ] No duplication: confirmed no duplicate component already exists; if similar, component was extended instead.
- [ ] Documentation: assumptions, missing tokens, or intentional deviations logged in `docs/screendesign-conversion/<feature-name>.md`.

If any item is unchecked, stop and resolve it before continuing. If an item cannot be completed (blocked by missing design token, legal copy, or asset), mark it in the documentation file and add a short "blocked" note to the PR description so reviewers can triage.

### Git workflow

- For every screendesign conversion, create a branch named `screendesign-conversion/<feature>` where `<feature>` is a short, lowercase, hyphenated identifier derived from the feature name (for example `navigation` or `hero-section`). Replace spaces with hyphens and remove special characters.
- Work on that branch and commit logical chunks (component creation, tests, stories, docs) together. Include tests and Storybook stories in the same branch as their components.
- When the Phase 3 checklist is complete, push the branch and open a pull request using the GitHub CLI (`gh`). The PR title should follow the pattern: `screendesign: add <feature> components` and the PR body should:
   - summarize the component tree and shared-UI audit,
   - list the Phase 3 checklist items and mark done/blocked items,
   - link to the original design file (`screendesigns/<file>`),
   - reference any fixtures used (e.g. `libs/<feature>/testing/fixtures/`).
- Example commands (replace `feature` and file paths as appropriate):

```bash
feature="navigation"          # sanitized feature name
branch="screendesign-conversion/$feature"

git checkout -b "$branch"
# make commits (components, tests, stories, docs)
git add -A
git commit -m "screendesign: add $feature components, stories, tests, and docs"
git push -u origin "$branch"

gh pr create --title "screendesign: add $feature components" \
   --body "Summary: Add component tree, shared-ui audit and implementation for $feature.\n\nDesign: screendesigns/Navigation.png\n\nChecklist: see docs/screendesign-conversion/$feature.md" \
   --reviewer team-name
```

- If `gh` is not configured in the environment or the user prefers manual PR creation, push the branch and include instructions in the conversion docs indicating how to open the PR manually. Document the chosen PR flow in `docs/screendesign-conversion/<feature-name>.md`.

### Phase 4 — Pixel-Perfect Verification

After implementation:

1. **Run the implemented UI** at the exact desktop reference viewport used by the source image. Use Storybook for isolated components and the real app/page for assembled layout.
2. **Capture screenshots** of the implemented components/page with Playwright or the browser tool:
   - reference screenshot stays unchanged
   - implementation screenshot uses the same viewport, device scale factor, theme, locale, auth state, seeded data, and route state
   - store screenshots under `docs/screendesign-conversion/<feature-name>/`
3. **Compare screenshot against reference pixel by pixel.** Use visual diff tooling where available (Playwright screenshot assertions, pixelmatch, ImageMagick compare, or equivalent). Record:
   - viewport and device scale factor
   - diff tool/command
   - mismatch count or percentage
   - diff image path
   - accepted tolerance, if any
4. **Analyze every meaningful mismatch zone by zone.** Check:
   - Spacing and alignment (use browser dev-tools overlay if available).
   - Typography: font-family, weight, size, line-height, letter-spacing, color.
   - Colors: backgrounds, borders, text, shadows — match design tokens or hex values exactly.
   - Icons: correct icon, correct size, correct color.
   - Interactive states: hover, focus, active, disabled — if shown in the design.
   - Responsive breakpoints: at minimum `sm`, `md`, `lg`.
5. **Refine and iterate until match is acceptable.** If the implementation is not a 1:1 match to the reference at the baseline viewport:
   - adjust components/styles/data/assets
   - capture a new screenshot
   - run another pixel comparison
   - repeat until the diff is limited to documented, intentional deviations
6. **Final gate:** Do not mark the task complete until `docs/screendesign-conversion/<feature-name>.md` contains the final screenshot paths, diff evidence, mismatch summary, and any accepted deviations.

## Rules
- Log your insights or assumptions or unclear issues in a `docs/screendesign-conversion/<feature-name>.md` file as you go, so the team can review and refine the design system and shared UI over time.
- Always search `docs/` for matching PRDs or functional docs before coding. Use discovered product requirements to drive UI behavior, data wiring, and validation.
- If the screenshot implies logic, implement that logic. Static-only conversion is allowed only when explicitly requested or when logic is documented as blocked/out of scope.
- Always finish with screenshot capture and pixel-level comparison against the reference. A visual eyeball check is not enough.
- If the first comparison is not 1:1, refine and rerun the comparison. Iterate until the remaining diff is intentional and documented.
- **No unstructured HTML blobs.** Every visual section becomes a named Angular component.
- **No arbitrary colors or spacing.** Use Tailwind design tokens, DaisyUI theme variables, or CSS custom properties. Only use arbitrary values (`[#ff00ff]`, `[13px]`) when absolutely no token matches. Then note the missing token and consider proposing it for addition to the design system. Log these cases in the `docs/screendesign-conversion/<feature-name>.md` file.
- **No duplication.** If two areas look the same, they share a component.
- **Accessibility is mandatory.** Every interactive element gets proper ARIA attributes, focus management, and keyboard support.
- **Mobile is not a shrunken desktop.** Design mobile layouts intentionally.
- **Composability over monoliths.** Prefer small, single-responsibility components composed together over large templates.
- **Always TDD + SDD.** Every component gets tests and stories. No exceptions.

## Inputs Expected

- A screen design image (PNG, JPG, Figma export, screenshot).
- Optionally: the target feature name / library where feature components should live.
- Optionally: specific design tokens or color palette to use.

## Outputs Delivered

- Component tree outline (confirmed by user).
- Product-doc/PRD findings and logic plan.
- Shared-UI audit table.
- Implemented Angular components with:
  - Pixel-perfect Tailwind CSS styling.
  - Implemented visible/implied logic, data wiring, and states.
  - Unit tests (TDD).
  - Storybook stories (SDD).
  - Proper exports from library index files.
- Documentation of assumptions, missing tokens, screenshot paths, pixel-diff evidence, and intentional deviations in `docs/screendesign-conversion/<feature-name>.md`.
