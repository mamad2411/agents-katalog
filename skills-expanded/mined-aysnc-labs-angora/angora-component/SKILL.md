---
name: angora-component
description: Build or update a reusable UI component in `src/components/` — primitives, composites, landmarks, content components. Trigger whenever the user wants to create or modify any `.astro` file under `src/components/`, add a variant or state to an existing component, do a visual refactor (spacing, hover lift, type), or build a pattern named by use-case ('FAQ' → Accordion, 'testimonials section' → Carousel, 'trust logos' → Logo cloud). Phrases like 'build a pricing card', 'update Button.astro', 'the cards feel cramped', 'add a destructive variant', 'we need a breadcrumb', 'make an accordion', 'tooltip with placements' all trigger this, even without the word 'component'.
argument-hint: <name>
---

# Component: $ARGUMENTS

## Before you start

1. **Read `src/system.md`** — check anti-patterns and decisions log. Stay consistent.
2. **Read `src/styles/global.css`** — know the available tokens. All color values must come from the **semantic tokens inside `@theme`**. The primitive palette (defined outside `@theme`) generates **no Tailwind utility classes** — only semantic tokens produce usable classes. This is structural enforcement for dark mode compatibility.
3. **Read [design-principles.md](../docs/design-principles.md)** — hierarchy, spacing, typography, color, depth, dark mode, and finishing touches guidance.
4. **Read [tailwind-conventions.md](../docs/tailwind-conventions.md)** — Tailwind v4 syntax rules for consistent class authoring.
5. **Check existing components** — look in `src/components/`. If the component already exists, read it first. Understand what's there before making changes. If building a new component, read 2–3 existing project components to learn the established patterns (styling conventions, prop style, layout approach).
6. **If landmark or content** — read `src/components/Section.astro` to understand the Section pattern.

## Composition

**Four types: primitives, composites, landmarks, and content components.**

### Primitives

Atomic, single-purpose elements. Single file. Take props directly.

**Children-first composition.** Even for primitives, visual content (icons, badges, decorative elements) composes through `<slot />` — not through dedicated props. The consumer controls order by placement. This keeps the API surface minimal and the component maximally flexible.

```astro
<!-- Bad — prop for visual content -->
<Button icon={ArrowRight} label="Continue" />

<!-- Good — children control content and order -->
<Button>Continue <ArrowRight /></Button>
```

Only accept behavior/layout props (`variant`, `size`, `disabled`) and a default `<slot />`.

Examples: Button, TextInput, Toggle, Badge, Section, FormRow, FieldGroup.

### Composites

Layout shells that arrange content through sub-components, not prop bags. Directory structure groups the shell with its sub-components.

**The rule:** the shell has zero content props. Content flows exclusively through sub-components. The shell only accepts behavior/layout props (`variant`, `size`) and a default `<slot />`.

**Sub-components only — no content props on shells.** Every piece of content in a composite must be a sub-component. No string props for headings/text, no arrays for lists of items, no slot-based styled markup on the shell. If a section of a composite has content, it's a sub-component — even if it's "just a string." Sub-components own their own styling, defaults, and structure. The consumer composes what they need, omits what they don't.

**Why this is strict:** Content props create two problems. First, they couple content to the shell — adding/removing a section means changing the shell's interface. Second, they push decisions about rendering into the shell via conditionals (`{dataProtectionText && ...}`). Sub-components eliminate both: add a section by composing a sub-component, remove it by not including it.

**Reference patterns:**

```astro
<!-- Bad — prop bag -->
<Card imageSrc="/img.jpg" eyebrow="Engineering" title="Hello" description="..." />

<!-- Bad — content props on shell -->
<Footer newsletterHeading="..." dataProtectionText="..." navLinks={[...]} />

<!-- Good — sub-components only -->
<Card padding={false}>
  <CardImage src="/img.jpg" alt="..." />
  <CardBody>
    <CardEyebrow>Engineering</CardEyebrow>
    <CardTitle>Building reliable systems</CardTitle>
    <CardDescription>How we scaled our infrastructure.</CardDescription>
  </CardBody>
</Card>

<!-- Good — landmark composite with sub-components -->
<Footer>
  <FooterNewsletter />
  <FooterDataProtection>Legal text here...</FooterDataProtection>
  <FooterPartners>
    <FooterPartnerLogo src="..." alt="..." width={93} height={40} />
  </FooterPartners>
  <FooterSocial>
    <FooterSocialLink href="..." icon="facebook" label="Facebook" />
  </FooterSocial>
  <FooterNav>
    <FooterNavLink href="..." label="Privacy Policy" />
  </FooterNav>
</Footer>
```

The shell owns background, container, and spacing. Each sub-component owns its own heading (defaulted), typography, and layout. Consumers compose only the parts they need — no conditionals in the shell.

### Landmark components

A landmark component lives on its own without a Section — it participates directly in `section-flow` and owns its own semantic HTML element, container behavior, and spacing.

**Landmarks can be composites too.** A landmark that has multiple distinct content sections (e.g., a Footer with newsletter + data protection + partners + social + nav) should follow the composite pattern — shell + sub-components. Being a landmark (owns its semantic element and flow attributes) doesn't exempt a component from the composite rule. If the landmark has more than 3 content props, break it into sub-components.

**Classification questions** — ask during the spec step:
1. *"Is this a landmark component — a component that lives on its own without a section?"*
2. If yes: *"Does it have multiple distinct content sections? If so, it should be a composite with sub-components."*
3. **Reusability test:** *"Could this pattern appear inside a card, a sidebar, a settings page — or does it only ever exist as a standalone page section?"* If reusable → it's a **content component**, not a landmark. The page context (heading, section wrapper) is separate — the consumer provides it via `<Section>`.

**The "section" word trap.** When you hear "section" in a request, separate the pattern from the page context. Use this phrasing: *"I'm hearing two things — the pattern (accordion/carousel/grid) and the page context (a section with a heading). I'll build the pattern as a reusable component. When you use it on a page, you wrap it in `<Section>` to give it a heading. That way the component works anywhere, not just as a standalone page section."*

**Landmark structure:**

- **Renders its own semantic element** — the component renders a `<section>`, `<footer>`, `<nav>`, or `<header>` directly with `data-component` and flow attributes (`data-seamless`, `data-full-width`). Example: Hero renders `<section data-component="Hero" data-seamless data-full-width>`. The consumer never wraps it in Section.
- **Owns container layout** — some landmarks handle their own internal max-width and padding (e.g., Footer). Others rely on the flow utility for width constraints.

**Section reference:**
- `Section` is a thin semantic wrapper — it renders `<section>` with `@container`, `seamless` variant (`data-seamless` for `section-flow`), `fullWidth` mode (`data-full-width` — drops flow width constraints), `narrow` mode (constrains to `--container-narrow`), `withWrap` (re-constrains children of full-width sections to container width), `withPadding` (adds vertical padding without `data-seamless` behavior), and `title` prop (renders `<h2>` with automatic `aria-labelledby`). Section does NOT own width or horizontal padding — the flow utility (`section-flow`/`prose-flow`) handles all width constraints on direct children.
- Non-seamless sections get no vertical padding — `section-flow` handles spacing. Seamless sections get standardized vertical padding tied to `--section-gap`.
- Section accepts `aria-label` via props for sections without a visible heading.

### Content components

A content component sits inside a Section (or another container). It renders its own `@container` wrapper so container queries work anywhere — inside Section, in a specimen page, standalone. The consumer controls section behavior (seamless, narrow, title) via the wrapping Section.

```astro
<!-- Consumer controls the section context -->
<Section title="Our Components">
  <MyComponent>
    <MyComponentItem ... />
  </MyComponent>
</Section>

<!-- Same component works standalone — @container is self-provided -->
<MyComponent>
  <MyComponentItem ... />
</MyComponent>
```

**Content component structure:**
```astro
---
const { class: className, ...props } = Astro.props;
---
<div data-component="MyComponent" class:list={["@container", className]} {...props}>
  <div class="grid grid-cols-2 @sm:grid-cols-3 @md:grid-cols-4 grid-gap">
    <slot />
  </div>
</div>
```

The outer div provides `@container` (so container queries resolve against the component's own width). The inner div holds the layout. This means the component works anywhere without depending on an ancestor `@container`.

**Heading ownership — two-pattern distinction:**

- **Section-level headings** (the heading that labels the entire section, sitting above the content) belong to Section's `title` prop. Content components never accept a `heading` or `title` prop — the consumer provides it via the wrapping `<Section title="...">`.
- **Content headings** that are part of a component's internal layout are fine as sub-components — these are content headings, not section titles. The distinction: if the heading sits above the component and labels the section, use Section's `title` on a parent Section. If the heading is embedded inside the component's layout as part of its content composition, use a sub-component.

## Spacing

**Internal padding vs. outer spacing — never both on the same boundary.**

- **Two flow contexts** — `section-flow` for page-level rhythm (`--section-gap`: 4rem), `prose-flow` for typography-level rhythm (`--prose-gap`: 1.25em). Both include ambient `prose` via `@apply prose` — typography for raw HTML elements is automatic. Pages get `section-flow`, posts/articles get `prose-flow`. Components own zero vertical margin — spacing comes entirely from the parent flow context.
- **Non-seamless sections** — no vertical padding from Section. Content has no background to fill. `section-flow` margin provides all inter-section spacing.
- **Seamless sections** — Section adds vertical padding tied to `--section-gap`, so the breathing room inside a backgrounded section matches the gap between sections. Consistent rhythm everywhere.
- **Outer spacing** — landmark and content components NEVER set their own `margin-top`/`margin-bottom` on their outermost element. That's the flow context's job.
- **`section-flow`** — the page-level utility (defined in `global.css`) that controls vertical rhythm between sections. Gap controlled by `--section-gap`. Adjacent `[data-seamless]` sections get 0 gap so backgrounds butt up.
- **`prose-flow`** — the typography-level utility (defined in `global.css`) for blog posts and editorial content. Gap controlled by `--prose-gap`. Used when paragraphs, headings, images, and inline components flow at reading rhythm.
- **The doubling rule** — if a non-seamless component adds `py-*` AND sits inside `section-flow`, you get padding + margin = double whitespace. Non-seamless sections avoid this by having no vertical padding. Seamless sections are safe because adjacent seamless sections get 0 margin from `section-flow`, and the standardized padding provides consistent internal rhythm.

## File organization

**Primitives → single file. Composites → directory.**

```
components/
  Button.astro              ← primitive, single file
  Section.astro             ← primitive, single file (the section wrapper)
  TextInput.astro           ← primitive, single file
  Card/                     ← composite, directory
    Card.astro              ← shell (variant/layout props)
    CardImage.astro         ← image with placeholder fallback
    CardBody.astro          ← padded content wrapper
    CardEyebrow.astro       ← uppercase category label
    CardTitle.astro         ← title (accepts `as` prop for heading level)
    CardDescription.astro   ← body text
  Hero/                     ← landmark composite, directory
    Hero.astro              ← renders own <section> with data-component + flow attrs
    HeroTitle.astro
    HeroDescription.astro
    HeroActions.astro
  MyComponent/              ← content composite, directory
    MyComponent.astro       ← @container wrapper + grid (no Section)
    MyComponentItem.astro
```

The directory groups the shell with its sub-components. Consumers import from the directory: `import Card from '../components/Card/Card.astro'`.

## Output files

Every component requires three files:

1. **Component** — `src/components/<Name>.astro`
2. **Design system page** — `src/pages/design-system/<name>.astro` (using `Layout` from `_layout/`, shows all variants/states)
3. **Full-screen view content** — `src/pages/design-system/view/_content/<name>.astro` (pure markup, no FullScreen wrapper). The dynamic route at `view/[theme]/[...slug].astro` wraps this in FullScreen and applies the theme. This generates `/view/light/<name>` always, plus `/view/dark/<name>` when dark mode is enabled.

The sidebar auto-discovers design system pages via `import.meta.glob` — no manual nav registration needed. Just create the file and it appears. The `fullscreenHref` prop on `Layout` should point to `/design-system/view/light/<name>` (the toggle in the sidebar handles switching to the dark route).

## Steps

### 0. Semantic intent check

Before speccing anything, verify the user is asking for the right component. Ask: *"What does this need to DO?"* — not what it looks like.

**The "looks like" trap:** Designers coming from graphic design think in visual similarity — a collapsed accordion item looks like an input field (both are rectangles with text and a chevron). A card looks like a button (both are clickable rectangles). But components are defined by **behavior and semantics**, not shape:
- An **input** accepts text from the user
- An **accordion** expands/collapses content sections
- A **button** triggers an action
- A **card** groups related content for browsing
- A **disclosure** reveals supplementary information

If the user says "I want to use X for Y" and the semantic purpose doesn't match, push back immediately: *"[Component X] is for [its purpose] — what you're describing is [correct pattern], which is a different component with different semantics and a different accessibility contract. Let me build the right one."*

If the user asks for a component by a use-case name (e.g., "FAQ"), redirect to the generic pattern name (e.g., "Accordion") — see naming rule below.

This isn't gatekeeping — it's mentorship. Explain *why* the distinction matters (accessibility, reusability, semantic HTML) so the designer builds the right mental model.

### 0b. Exploration mode (when the user wants to compare directions)

Activate when the user asks to see multiple options, compare approaches, or explore directions — "show me a few takes on this hero," "I want to see some options," "what are some ways to do this."

**Write style definitions before building anything.** Each direction gets a written description that's specific enough to build from. Cover how it arranges content, how it uses type (scale contrast, weight, font character), what the color temperature and palette emphasis are, how dense or spacious it feels, whether it uses containers/cards or open space, and what the overall mood is.

Each definition must be a genuinely different design philosophy — not three variations of the same idea with tweaked spacing.

**Bad:** "Option A: Simple and clean with lots of space"

**Good:** "Option A: High-contrast typographic — large serif display heading against tight body text, deep vertical rhythm between sections, muted earth tones with one bold accent reserved for the primary action. No cards or containers — hierarchy carried entirely by scale and weight."

**The flow:**

1. Present style definitions (default 3 unless the user asks for a specific count)
2. Designer picks one — or says "build two so I can compare in the browser"
3. If comparing in browser: build each as a separate component with its own specimen page. Name them descriptively (`HeroEditorial.astro`, `HeroBold.astro`)
4. Designer reviews both specimen pages, picks one
5. Keep the chosen component, rename if needed, delete the other
6. Continue to the normal spec → build → audit flow with the chosen direction

### 1. Spec

Present a spec to the user covering:

- **Semantic purpose** — what does this component DO? What user need does it serve? Confirm the behavior matches the component type before proceeding
- **Purpose & hierarchy** — what is this component, who sees it, where on the page
- **Classification** — primitive (single element), composite (layout shell + sub-components), landmark (lives on its own without a Section), or content (sits inside a Section). Ask the designer: *"Is this a landmark component — a component that lives on its own without a section?"*
- **Section participation** — if landmark: renders its own semantic element with `data-component` and flow attributes. If content: provides its own `@container` and sits inside a consumer-provided Section
- **Composition** — if composite: name each sub-component, its responsibility, which are required vs optional
- **Variants** — only those that earn their place. Name each, describe the use case. Don't generate variants speculatively
- **States** — interactive states (hover/focus/active come free via pseudo-class variants), plus any `state` prop values if form-related
- **Responsive behavior** — how it adapts at narrow/medium/wide container widths
- **Prop API** — list props with types and defaults

Wait for the user to approve before building.

### 2. Build

- Build component files per the approved spec
- Semantic HTML + Tailwind utility classes. Always interactive (pseudo-class variants). Use `state` prop only for form states that can't be triggered by interaction (error, success, disabled). All color values from **semantic token utilities only** (`bg-card`, `text-foreground`, `border-border`, etc.) — never raw palette classes
- **Landmark checklist** (component lives on its own without a Section):
  - Renders its own semantic element (`<section>`, `<footer>`, `<nav>`) with `data-component` and flow attributes (`data-seamless`, `data-full-width`)
  - Does NOT set outer vertical margin — `section-flow` handles spacing
  - Content headings as sub-components are fine (e.g., HeroTitle)
- **Content component checklist** (component sits inside a Section):
  - Renders a `@container` wrapper div as its root — container queries work anywhere, no dependency on a parent `@container`
  - Inner div holds the layout (grid, flex, etc.) and queries the outer `@container`
  - Does NOT compose Section — the consumer wraps in `<Section>` to control title, seamless, narrow
  - Does NOT accept `heading`, `title`, `seamless`, or `narrow` props — those belong to the consumer's Section
  - Content headings as sub-components are fine
- Create design system page + full-screen view

### 3. Responsive check

Verify the component works at narrow (~320px), medium (~768px), and wide (~1280px) container widths. Typography scales automatically via `clamp()` tokens (requires a `@container` ancestor). Check: layout collapses/stacks logically, text doesn't overflow, interactive targets stay tappable (≥44px), images/media scale without breaking, spacing tightens proportionally. If layout doesn't adapt, add the missing `@sm:`/`@md:`/`@lg:` container query variants.

### 4. Accessibility test

Tell the user: "Running a11y tests next." Then run `pnpm test:a11y` immediately — this is verification, not a project change. Don't ask permission to run it (dev server must be running). Read the output and interpret every finding for the user:
- **Real issue** — explain what's wrong in plain language, propose a specific fix, explain why it matters.
- **False positive** — explain why it's safe to ignore (e.g., disabled states are intentionally dimmed, specimen context lacks form wrapping). Don't fix these.

Present findings and proposed fixes. Wait for approval before applying fixes only.

### 5. Audit + fix

Tell the user: "Running design system audit next." Then run `/angora-design-system-audit` immediately on the new component — same as above, verification not a change. The audit skips contrast and ARIA labeling (already covered by the a11y test) and focuses on design rules, token compliance (including semantic token enforcement — no raw palette classes), and responsive behavior. Fix any issues it finds — no confirmation needed for audit-driven fixes.

### 6. Present for review

Show the user what you've built. Reference the design system page URL (e.g., `/design-system/buttons`) so they can check it — don't tell them to start the dev server.

### 7. Visual review

User reviews in browser. Approves or iterates.

### 8. Update system.md

Only if you made a new decision worth recording (added to anti-patterns or decisions log). Most components won't need an update.

**Suggested component order:** Typography specimens, Navigation, Hero sections, Feature grids, Pricing tables, Testimonials, Logo clouds, Accordion, CTA sections, Footer. (Buttons, icons, cards, grid, Section, and forms are already built during init.)

## Markup Conventions

### Dev Tools Identification — with flow attributes

Every component's root element gets a `data-component` attribute matching the component name (PascalCase). This makes components instantly identifiable in browser dev tools, where Tailwind class soup otherwise gives no hint which component rendered an element.

```html
<button data-component="Button" class="inline-flex items-center ...">
<div data-component="Card" class="rounded-lg overflow-hidden ...">

<!-- Landmark components add flow attributes -->
<section data-component="Hero" data-seamless data-full-width class="relative min-h-[40.625rem] ...">
<footer data-component="Footer" data-seamless class="...">

<!-- Section uses its props to set flow attributes -->
<section data-component="Section" data-seamless data-full-width class="...">
```

Sub-components get it too: `data-component="CardBody"`, `data-component="HeroTitle"`. The DOM reads like a component tree. The `data-component` attribute is always first in the attribute list for consistency.

### Props & Naming

**Rules:**
- **Name components after the generic UI pattern, not the use case.** An accordion is an accordion even when used for FAQs. A carousel is a carousel even when used for testimonials. A disclosure is a disclosure even when used for terms of service. If a user asks for "an FAQ component," push back: *"That's an Accordion — FAQ is how you'd use it on a page. The component should be reusable for any expandable list."* Use the industry-standard pattern name from established design systems (Radix, shadcn, MUI, Headless UI).
- **Translate user intent to industry conventions.** This applies to component names, prop names, and values. When a user describes something in informal or use-case language, find the established convention that matches the intent — t-shirt sizes (`sm`, `md`, `lg`) for scales, standard variant names from major design systems for styles.
- Accept a `class` prop for additive styling (positioning, extra margin, layout context). Use `class:list` for merging.
- Forward unknown props to the root element via `{...props}` spread.

### Semantic HTML + Tailwind Classes

All components use semantic HTML elements styled with Tailwind utility classes. No custom elements, no Shadow DOM.

**Landmark component example (renders own element with flow attributes):**

```astro
---
const { class: className, ...props } = Astro.props;
---
<section
  data-component="Hero"
  data-seamless
  data-full-width
  class:list={["relative min-h-[40.625rem]", className]}
  {...props}
>
  <slot />
</section>
```

**Content component example (self-contained with `@container`):**

```astro
---
const { class: className, ...props } = Astro.props;
---
<div data-component="MyComponent" class:list={["@container", className]} {...props}>
  <div class="grid grid-cols-2 @sm:grid-cols-3 @md:grid-cols-4 grid-gap">
    <slot />
  </div>
</div>
```

**Rules:**
- Content: semantic HTML (`h1`-`h6`, `p`, `a`, `img`, `ul`, `figure`, `blockquote`, `section`, `nav`, `footer`)
- Layout/structure: Tailwind utility classes (`flex`, `grid`, `max-w-*`, `p-*`, `gap-*`)
- Long-form content: use the `prose` utility class for sections with flowing editorial text (paragraphs, lists, blockquotes). Components like cards and heroes should NOT use `prose` — they own their spacing explicitly via `gap-*` classes
- **Ambient prose convention:** `prose` is applied at the `<main>` level on layout pages as an ambient typography baseline. Its descendant selectors use `:where()` for low specificity, so any Tailwind utility class on a component naturally overrides it. Prose targets semantic elements (`<h2>`, `<p>`, `<a>`, `<ul>`, `<ol>`, `<blockquote>`) — components that render these need explicit classes to override prose when the default treatment isn't wanted:
  - **Blockquotes:** automatic protection via `data-component` (prose targets `blockquote:not([data-component])`). If a component uses a raw `<blockquote>` without `data-component`, add explicit counter-declarations (`border-l-0 pl-0 not-italic`)
  - **Lists:** prose adds `list-style-type: disc` and `padding-left: 1.5em` to `<ul>`/`<ol>`. Components that render UI lists (navigation, tags, non-content lists) must add `list-none p-0` to override. Content lists that *should* have bullets don't need anything — prose handles them
- No arbitrary values outside Tailwind's theme — all styling references theme tokens via utility classes
- Pixel translation: when a user specifies a value in pixels, map it to the nearest theme token first (e.g., "32px padding" → `p-8`). If no token fits, use `rem` for sizing and `em` for prose-relative spacing. Never hard-code arbitrary pixel values in components
- Landmark components render their own semantic element (`<section>`, `<footer>`, `<nav>`) with `data-component` and flow attributes. They don't use Section — Section is for content sections controlled by consumers
- Content components provide their own `@container` wrapper — don't depend on Section for container queries

**Change the component, don't override from outside.** When a component's default appearance needs to change, update the component file itself. Never override baked-in Tailwind classes from the consumer side via the `class` prop — Tailwind resolves same-specificity utilities by CSS source order, not HTML class attribute order, so `bg-highlight` passed via `class` won't reliably beat a component's built-in `bg-muted`. The `class` prop is for **additive** styling (positioning, extra margin, layout context) — not for overriding the component's own visual treatment. If you find yourself reaching for `!important` (`!bg-*`), that's a signal you're fighting the component instead of updating it.

**Icons: always import from `src/icons/`, never from the icon library directly.** Each icon in `src/icons/` is a thin Astro wrapper around the underlying library. This keeps the library swappable. `import ArrowRight from '@/icons/ArrowRight.astro'` — never import from the library package. If a needed icon doesn't exist in `src/icons/`, read an existing wrapper to learn the pattern and create one. When you add a new icon wrapper, also add it to the icons design system page (`src/pages/design-system/icons.astro`) so the gallery stays complete.

**Images: always use `<img>`, never CSS background images.** Use `<img>` with `object-fit: cover` (`object-cover` in Tailwind) for all imagery including hero backgrounds, card covers, and full-bleed sections. Position with Tailwind classes (`absolute inset-0`) inside a relatively-positioned container when used as a backdrop.

### ARIA Regions and Groups

Composites that render as page sections need accessible labels so screen readers can identify them. Primitives generally don't — native semantics are enough.

- **`<section>`** — always pair with `aria-labelledby` pointing to the section's heading, or `aria-label` if there's no visible heading. Landmark components wire `aria-labelledby` internally since they control their own heading markup. Section's `title` prop handles `aria-labelledby` automatically. Pass `aria-label` on Section for sections without a visible heading.
- **`<nav>`** — always add `aria-label` (e.g., `aria-label="Main"`, `aria-label="Footer"`). Critical when multiple navs exist on a page
- **`role="group"`** — use on related control clusters (e.g., a button group, a set of radio cards) with `aria-label` describing the group

```astro
<!-- Section with title handles aria-labelledby automatically -->
<Section title="Pricing">
  ...
</Section>

<!-- Section without visible heading -->
<Section aria-label="Call to action" seamless>
  ...
</Section>

<!-- Nav with label -->
<nav aria-label="Main">...</nav>

<!-- Control group -->
<div role="group" aria-label="Plan selection">
  <Card>...</Card>
  <Card>...</Card>
</div>
```

Accept `aria-label` as a prop on composites so consumers can override the default label in context.

### Container Queries, Not Media Queries

All responsive behavior uses container queries so components adapt to their container, not the viewport. No viewport-based responsive variants (`sm:`, `md:`, `lg:`) in component markup — only container query variants.

Tailwind v4 container query support:
- `@container` utility sets `container-type: inline-size` on the parent
- `@sm:`, `@md:`, `@lg:`, `@xl:` variants trigger at container breakpoints (640/768/1024/1280px)
- Named containers: `@container/card` → `@sm/card:` for targeted queries

```html
<!-- Content components provide their own @container wrapper -->
<div data-component="FeatureGrid" class="@container">
  <div class="grid grid-cols-1 @sm:grid-cols-2 @lg:grid-cols-3 grid-gap">
    <!-- cards -->
  </div>
</div>

<!-- Section provides @container on its root <section> element — content
    components don't depend on it, but it's there for inline content -->
<Section title="Features">
  <FeatureGrid>...</FeatureGrid>
</Section>
```

The only `@media` queries allowed are in `design-system.css` (tooling, not a deliverable).

### States

Components are interactive by default — they include pseudo-class variants (`hover:`, `active:`, `focus-visible:`) and transitions. No frozen "specimen mode" — this is the advantage of HTML over Figma.

**Form controls with native inputs** (Checkbox, Radio, Toggle) use hidden `<input>` elements with `sr-only peer` and Tailwind's `peer-checked:` variants. Interactivity, keyboard support, and accessibility come from the native element — no `state` prop needed. Use boolean props: `checked`, `disabled`. Add `name`/`value` for form submission and radio grouping.

**Form controls without native checked state** (TextInput, Textarea, Select) use a `state` prop for states that can't be triggered by design system interaction:

```astro
<!-- Error state — can't be triggered by clicking -->
<TextInput state="error" label="Username" value="ab" hint="Must be at least 3 characters" />

<!-- Renders to: -->
<input class="... border-destructive" data-state="error" />
```

Valid `state` values: `error`, `success`, `disabled`, `dragover` (file upload), `has-value` (search).

### Form Layout

Two primitives handle form layout spacing, both using `grid-gap` (`var(--grid-gap)`):

- **FormRow** — horizontal row (`flex flex-wrap`). Children grow to fill space by default (`grow` prop, defaults `true`). Set `grow={false}` for rows where children should stay at natural width (e.g., buttons). `align` prop controls vertical alignment (`start` | `center` | `end`).
- **FieldGroup** — vertical stack (`flex flex-col`). Wraps multiple FormRows or fields with standard vertical spacing.

```astro
<FieldGroup>
  <FormRow>
    <TextInput label="First name" />
    <TextInput label="Last name" />
  </FormRow>
  <FormRow>
    <TextInput label="Email" />
  </FormRow>
  <FormRow grow={false}>
    <Button>Submit</Button>
  </FormRow>
</FieldGroup>
```

**Primitive vs composite:** Primitives (button, badge, input) show all their own variants. Composites (hero, pricing, nav) show *their own* variants but render child primitives in default state only.
