---
name: angora-design-system-audit
description: Review any component (`src/components/`), design-system page, layout specimen, or site page (`src/pages/*.astro`) against Angora's design rules — semantic token usage (no raw palette classes), `data-component` attributes, landmark vs content classification, heading ownership, flow spacing, container queries, accessibility extras not caught by `pnpm test:a11y`, and anti-patterns from `src/system.md`. Trigger whenever the user wants to audit, review, check, verify, or 'go through' existing work for violations, typically after building. Phrases like 'audit the pricing page', 'go through Button.astro', 'check the new Footer', 'run the audit', 'look over src/components/ and report violations' all trigger this.
argument-hint: [path]
---

# Audit: $ARGUMENTS

## Before you start

1. **Read `src/system.md`** — intent, accessibility standard, anti-patterns, decisions log.
2. **Read `src/styles/global.css`** — the token definitions you're validating against.
3. **Read [design-principles.md](../docs/design-principles.md)** — the full set of design principles informing this review.
4. **Read [tailwind-conventions.md](../docs/tailwind-conventions.md)** — Tailwind v4 syntax rules to validate against.
5. **Determine the audit scope** — is the target a component (`src/components/`), a design system page (`src/pages/design-system/`), a layout (`src/pages/design-system/layouts/`), or a site page (`src/pages/*.astro`)? Some rules only apply to specific scopes (marked below). Layouts are full-page compositions — audit them like site pages (Page Rules apply) but note they use placeholder content, so skip SEO checks.

Then validate the target against the rules below.

## Hard Rules (always enforced)

### Tokens & Scoping

| Rule | Check |
|------|-------|
| Token compliance | No arbitrary values. All styling via Tailwind utility classes referencing theme tokens |
| **Semantic token enforcement** | **No raw palette utility classes.** Components and pages must use only semantic token classes (`bg-background`, `bg-card`, `text-foreground`, `text-muted-foreground`, `border-border`, `bg-primary`, etc.). Grep for violations: `bg-gray-*`, `text-gray-*`, `border-gray-*`, `bg-white`, `text-white`, `bg-black`, `text-black`, `bg-primary-[0-9]`, `text-primary-[0-9]`, `border-primary-[0-9]` (raw scale references). The primitive palette lives outside `@theme` so these classes shouldn't exist — but inline styles, arbitrary values (`bg-[#...]`, `text-[var(--gray-*)]`), and accidental palette references still need catching. **Exception:** style guide page (`index.astro`) uses inline `style` attributes with `var(--gray-50)` etc. for palette swatches — this is intentional |
| Pixel translation | No hard-coded pixel values in components. User-provided pixel values should map to the nearest theme token (e.g., "32px" → `spacing-8` / `p-8`). If no token fits, use `rem` for sizing and `em` for prose-relative spacing. Flag any arbitrary `[Xpx]` values |
| Scoping | Component styles via Tailwind classes on elements. No global CSS selectors in component files |
| No true black | Never `#000`, `rgb(0,0,0)`, or `black`. Use semantic tokens (`text-foreground`, `bg-foreground`) which resolve to near-black |
| No generated colors | No `color-mix()`, `lighten()`, `darken()`, or `rgba()` for text on colored backgrounds. All colors from semantic tokens or explicit palette values |

### Component Contracts

| Rule | Check |
|------|-------|
| Component naming | Component names must follow the generic UI pattern, not a use case. Flag components named after their content (e.g., `FAQ` instead of `Accordion`, `Testimonials` instead of `Carousel`). The name should be reusable |
| `data-component` with flow attributes | Every component's root element has `data-component="Name"` (PascalCase). Sub-components too (`data-component="CardBody"`). Attribute appears first in the attribute list. Landmark components also set flow participation attributes (`data-seamless`, `data-full-width`) on their root element |
| Landmark components | Landmark components (Hero, Footer, Nav) live on their own without a Section. They render their own semantic element (`<section>`, `<footer>`, `<nav>`) with `data-component` and flow attributes. Flag landmarks wrapped in `<Section>` |
| Content components | Content components render a `@container` wrapper div as their root so container queries work anywhere. They do NOT compose Section internally. Flag content components that import or render Section internally |
| Heading ownership | Content components must not accept a `heading` or `title` prop — a parent `<Section title="...">` provides the section heading. Content headings that are part of internal layout are fine as sub-components |
| No outer vertical margin | Landmark and content components never set `margin-top`/`margin-bottom` on their outermost element. That's the flow context's (`section-flow`/`prose-flow`) job. Flag any `mt-*`/`mb-*`/`my-*` on a component's root |
| Content props on composite shells | Composite shells must have zero content props — content flows exclusively through sub-components. Flag any string or array prop on a composite shell that represents displayable content (headings, descriptions, legal text, nav links). Even "simple" string props must be sub-components. Landmarks are not exempt |
| No visual content via props | Visual content flows via children and sub-components, never as props. Flag any prop that passes markup or rendered content (named slots used to pass styled markup into the shell where a sub-component should be used instead). The shell's only job is layout and behavior — content ownership belongs to sub-components |
| Images as `<img>` | All imagery uses `<img>` elements with `object-fit: cover` where needed. No CSS `background-image` for content images (heroes, cards, full-bleed sections). Position with `absolute inset-0` inside a relative container for backdrops |
| States | All components interactive by default (pseudo-class variants for `hover:`, `active:`, `focus-visible:` + transitions). Form `state` prop only for non-interactive states (error, success, disabled). Composites: own variants only, child primitives in default state |

### ARIA & Accessibility

Contrast ratios and ARIA labeling are covered by the automated a11y test suite (`pnpm test:a11y`). When dark mode exists, tests run against both `/view/light/*` and `/view/dark/*` routes — each mode must independently meet AA. The audit focuses on what automated testing can't catch:

| Rule | Check |
|------|-------|
| Target sizes | Interactive targets ≥ 44px. Check at narrow widths too |
| Color independence | Don't rely on color alone to convey meaning — always a secondary indicator (icon, text, border, pattern) |
| EAA extras (manual) | If standard is EAA: verify text spacing override tolerance, 200% text resize. (`lang` and reflow are covered by the a11y test) |
| Dark mode contrast | If dark mode exists: verify semantic token pairs provide sufficient contrast in both modes. Check that `--color-*-foreground` has ≥ 4.5:1 contrast against its paired `--color-*` in both light and dark values. The a11y test catches most issues, but token-level mismatches (e.g., light primary text on light primary bg) need manual verification when new tokens are added |

### Semantic HTML

| Rule | Check |
|------|-------|
| Semantic elements | Content uses semantic elements (`section`, `nav`, `h1`–`h6`, `p`, `a`, `button`, `input`, `figure`, `blockquote`, `ul`/`ol`, `footer`). No `<div>` where a semantic element fits |
| Heading hierarchy | Heading levels don't skip (no `h1` → `h3`). Components accept an `as` prop or similar for heading level flexibility |

### Responsive

| Rule | Check |
|------|-------|
| Container query syntax | Responsive variants use `@sm:`, `@md:`, `@lg:`, `@xl:` (container queries). No `@media` / no viewport-based `sm:`/`md:`/`lg:` in component markup. Only exception: `design-system.css` (tooling) |
| Responsive behavior | Component actually adapts at narrow (~320px), medium (~768px), and wide (~1280px) container widths. Check: multi-column layouts stack to single column; text doesn't overflow or clip; interactive targets stay ≥ 44px; images/media scale without breaking aspect ratio; spacing reduces proportionally at narrow widths |
| `@container` ancestor | Content components provide their own `@container` wrapper. Section provides `@container` on its root `<section>` element. For inline content inside Section, Section's `@container` is sufficient. Flag content components that use container query variants (`@sm:`, `@md:`, `@lg:`) but don't have their own `@container` wrapper |

## Design Rules (always enforced, require judgment)

### Hierarchy

| Rule | Check |
|------|-------|
| Three-tier emphasis | Clear primary/secondary/tertiary emphasis using size + weight + color together |
| Three-tier text color | Exactly three text color tiers: `text-foreground` (or `text-card-foreground`) for primary content, `text-muted-foreground` for secondary/tertiary. Flag any raw grey class usage — semantic tokens enforce the correct tiers. If a third visual tier is needed, use font size or weight rather than an additional color |
| Font weight discipline | Only two weights: normal (`font-normal`/`font-medium`, 400–500) and bold (`font-semibold`/`font-bold`, 600–700). Flag `font-thin`, `font-extralight`, `font-light` (under 400) |
| Label treatment | Labels should be de-emphasized (smaller, lighter, thinner). Combine labels and values when possible ("12 left in stock" not "In stock: 12") |
| Grey on colored backgrounds | No grey text on colored backgrounds. On primary/destructive/colored surfaces, use the paired `-foreground` token (e.g., `text-primary-foreground` on `bg-primary`). Never use opacity-based text on colored backgrounds — it looks washed out |

### Spacing

| Rule | Check |
|------|-------|
| Proximity grouping | Related elements closer together, groups further apart. No ambiguous spacing where the relationship between elements is unclear |
| Generous whitespace | Err on the side of generous whitespace. Flag areas that feel cramped — especially padding inside cards, space between section heading and content |

### Typography

| Rule | Check |
|------|-------|
| Line length | 45–75 characters. Use `max-w-[Xch]` (prefer `ch` units) on text containers. Constrain paragraphs independently if container has full-width elements |
| Line height | Proportional to font size: 1.5–1.75 for body text, 1.0–1.2 for display/heading text. Wider content may need up to 2.0 |
| `text-wrap: balance` | Headings (`h1`–`h4`, display text) should have `text-wrap: balance` to prevent orphan lines. The `prose` utility applies this automatically |
| `text-wrap: pretty` | Body text (`p`, `li`, `blockquote`) should have `text-wrap: pretty` to prevent single-word last lines. The `prose` utility applies this automatically |
| Letter-spacing | Headlines should tighten tracking (`tracking-tight` or `tracking-tighter`). Small uppercase UI text (badges, eyebrows, nav labels under `text-lg`) should widen (`tracking-wide`). Display-size uppercase text (`text-xl` and above) keeps normal tracking — the large size already provides legibility. See `system.md` Conventions for the full letter-spacing policy |
| Center-align limits | Center-aligned text only for very short blocks (1–3 lines). Body copy and longer text must be left-aligned. Flag centered paragraphs |
| Tabular numbers | Numbers in tables, stats, and vertically-aligned contexts should use `tabular-nums` (`font-variant-numeric: tabular-nums`) |

### Color

| Rule | Check |
|------|-------|
| Meaning, not decoration | Color communicates meaning. Greys for structure, color for emphasis and action |
| Semantic color usage | Red for errors/destructive, yellow/amber for warnings, green for success. Don't repurpose semantic colors for decoration |

### Depth

| Rule | Check |
|------|-------|
| Consistent application | Similar elements at the same elevation. Light source from above. In dark mode, tonal elevation (lighter surface = higher) conveys depth — shadows have reduced visibility |
| Shadow interaction | Interactive elevated elements: hover increases shadow (lift), active decreases shadow (press). Flag elevated buttons/cards without shadow transitions |
| Fewer borders | Prefer box shadows, different background colors, or extra spacing over borders for visual separation. Flag heavy `border` usage where a subtler technique would work |

## Page Rules (site pages and layouts — `src/pages/*.astro` and `src/pages/design-system/layouts/`)

Skip this section when auditing components or design system specimen pages.

| Rule | Check |
|------|-------|
| Flow context | Pages use `<main class="section-flow">` for inter-section spacing. Posts/articles use `<article class="prose-flow">` |
| Manual typography in content zones | Flag manual typography classes on `<h2>`, `<p>`, `<a>` inside content zones — prose handles these. Only flag inside `section-flow` or `prose-flow` zones where ambient prose applies |
| Blockquote prose protection | Blockquotes inside prose zones need protection via `data-component` (prose targets `blockquote:not([data-component])`) or explicit counter-declarations (`border-l-0 pl-0 not-italic`) |
| List prose protection | UI lists (navigation, tags, non-content lists) inside prose zones must have `list-none p-0` to override prose's list styles. Content lists that should have bullets need no override |
| Landmark vs content wrapping | Landmark components (Hero, Footer, Nav) live on their own in `section-flow` — don't wrap them in `<Section>`. Content components sit inside `<Section>` |
| Section component | Content sections on the page use the Section component. No raw `<section>` elements with manual padding for content sections |
| Seamless usage | Sections with background colors/images use `<Section seamless>` (or the landmark's flow attributes). Adjacent seamless sections should butt up (0 gap) |
| Background rhythm | Page has visual rhythm — some variation in section backgrounds (alternating light/dark, or strategic use of color). Flag a page where every section is the same plain background |
| Composition purity — single file | Design system layout directories (`src/pages/design-system/layouts/`) must contain only one `.astro` file. Flag extra files |
| Composition purity — zero classes | In layouts and site pages, no Tailwind utility classes on raw HTML elements. Only `section-flow` on `<main>` is allowed. If a `<div>` needs a class, a component is missing |
| Composition purity — no client code | Flag inline `<script>` tags in layouts and site pages. Use Preact islands via components instead |
| Composition drift | When auditing a layout that has a corresponding site page (or vice versa), check for structural divergence — different section order, missing/extra sections, different component usage. Copy differences are expected (placeholder vs real content). Structural differences are a bug |
| SEO | Site pages (not layouts) have `<title>`, `<meta name="description">`. Template-driven pages wire SEO from table fields (`meta_title`, `meta_description`). Flag missing OG tags on public-facing pages |

## Soft Rules

- **Anti-pattern violations** — anything listed in `system.md` Anti-Patterns section.
- **Pattern consistency** — does this component follow the conventions established by existing components? Read 2–3 peers to compare.
- **Personality alignment (swap test)** — could you swap this component's styling for the most generic version and the design wouldn't feel different? If yes, it's defaulting — flag it.
- **Prose utility** — `prose` is applied at the `<main>` level as an ambient typography baseline. Its descendant selectors use `:where()` for low specificity, so any Tailwind class on a component naturally overrides it. The only local `prose` usage is for nested content zones that need their own vertical rhythm. Components (cards, heroes) should NOT use `prose` — they own their spacing explicitly via `gap-*` classes.
- **Finishing touches** — are there opportunities to supercharge defaults? Custom list bullets, styled blockquotes, accent borders, subtle background decoration. Don't mandate these, but suggest where they'd elevate the work.

## Output

Report all violations with: file path, line number, rule category, rule name, and suggested fix.

Severity levels:
- **Error** — hard rule violation. Must fix.
- **Warning** — design rule violation. Should fix — explain why.
- **Info** — soft rule suggestion. Propose, don't mandate.

Group findings by file, then by severity. Fix all errors and warnings before showing components to the user.
