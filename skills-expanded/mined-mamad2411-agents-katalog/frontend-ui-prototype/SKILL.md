---
name: frontend-ui-prototype
description: Build a question-driven, browser-testable frontend prototype with a single index.html and locally downloaded raster assets. Use when turning a product idea, existing app, repository, screenshot, or live URL into a landing page or UI prototype before production implementation. Inspect product truth, ask concrete intake questions, research and select a suitable DESIGN.md direction, decide how real screenshots, photography, generated imagery, or illustration should be used, then create index.html, DESIGN.md, a Makefile, and any needed assets, and verify the result at desktop and mobile widths. Do not use for production application architecture, backend work, or pixel-perfect cloning.
---

# Frontend UI Prototype

Create a fast, disposable, visually credible prototype that helps the user make a design decision before production development.

The default implementation is intentionally simple:

```text
prototype/<slug>/
├── index.html
├── DESIGN.md
├── Makefile
└── assets/             # only when raster visuals are used
```

All page markup, styles, interactions, inline SVG, and prototype data belong in `index.html`. Do not create `src/`, `components/`, `package.json`, framework scaffolding, build configuration, or separate CSS/JS files unless the user explicitly requests a different delivery format.

## Core contract

1. Ask concrete questions before designing when required information is missing.
2. Inspect an existing product when one is available; treat it as product truth.
3. Research current references and appropriate `DESIGN.md` systems before coding.
4. Let the user select a design direction, unless they explicitly delegate the choice.
5. Decide the visual-evidence strategy: real product UI, photography, generated imagery, illustration, or no hero image.
6. Build one responsive `index.html` using CDN dependencies only when necessary; store any raster assets as downloaded local files alongside the prototype.
7. Include a prototype `Makefile` with zero-install local serving and validation commands.
8. Render and review the prototype at desktop and mobile widths.
9. Stop after prototype handoff. Do not silently turn it into production code.

## When to use

Use this skill for:

- a new product idea that needs a clickable visual prototype;
- a landing page for an existing application;
- a new page, screen, or flow concept inside an existing application;
- a redesign exploration before changing production UI;
- an original concept informed by screenshots, moodboards, websites, or competitor examples;
- experiments comparing screenshot-led, photography-led, or illustration-led art direction;
- rapid stakeholder review where one HTML file is the preferred artifact.

## Do not use

Do not use this skill for:

- production backend, authentication, database, billing, or infrastructure;
- framework architecture or reusable production component libraries;
- a frozen Figma handoff that should be implemented directly;
- pixel-perfect cloning of a third-party product;
- a tiny style adjustment where the design is already approved;
- a post-implementation audit that requires no new prototype.

## Mode detection

Choose one mode and state it before continuing.

### A. New concept

The user has an idea but no existing product. Define the smallest page or flow that can test the idea.

### B. Existing app to landing page

The user has a working application and wants a public marketing surface. Inspect the app, repository, routes, terminology, assets, and real workflows. The landing page must look like the public expression of the real product, not a generic SaaS template.

### C. Existing app UI prototype

The user wants a new or redesigned screen inside an existing product. Preserve recognizable navigation, interaction patterns, density, tokens, and terminology unless the prototype is intentionally testing a departure.

### D. Reference-led original

The user provides references. Extract principles such as hierarchy, pacing, typography, image treatment, and motion. Do not copy branding, proprietary text, or a distinctive composition one-for-one.

Read `references/modes.md` when mode boundaries are unclear.

# Workflow

## Delegate research to subagents

Whenever the host supports parallel subagents (for example Claude Code's Task tool or Codex subagents), delegate independent research and inspection to them, then synthesize their findings yourself. Work that parallelizes well:

- repository and existing-app inspection (Phase 0 and Phase 2);
- web research for `DESIGN.md` directions and references (Phase 3);
- screenshot capture across routes and viewport sizes.

Dispatch these as concurrent subagents, keep each task narrowly scoped, and merge the results before presenting decisions to the user. Fall back to doing the work inline when subagents are unavailable.

## Phase 0 — Read available context

Before asking questions:

1. Read the user's request carefully.
2. Inspect the current repository only when it is relevant.
3. Look for, in order:
   - `DESIGN.md`;
   - product README or brief;
   - existing routes and screenshots;
   - logo and brand assets;
   - global CSS, tokens, fonts, icons, and theme configuration;
   - adjacent UI that establishes product conventions.
4. Do not ask for information already present in the conversation, repository, or provided references.

## Phase 1 — Mandatory question gate

Ask only unanswered questions, in one compact message. Use the host's native question UI when available; otherwise ask in normal chat. Ask in the user's language: this skill's instructions are English, but every user-facing message, question, and prototype copy must match the language the user is writing in.

Ask no more than seven questions. Questions must request concrete decisions or facts, not abstract taste labels.

Cover these dimensions when they are not already known:

1. **Prototype decision:** What should this prototype help decide or prove?
2. **Audience:** Who is the primary visitor or user?
3. **Primary action:** What is the single most important CTA or task?
4. **Product source:** Is there an existing app, repository, live URL, screenshot, route, or test account that must be treated as the source of truth?
5. **Scope:** Which page, sections, screens, or interactions must be included?
6. **Visual boundary:** Which concrete aesthetics or references are desired, and which must be avoided?
7. **Visual evidence:** Should the prototype primarily use real app screenshots, photography, generated raster imagery, custom illustration, or typography/layout alone?

Good question examples:

- “What is the single action a visitor should take on this page?”
- “Which route in the existing app should I treat as the reference?”
- “In the hero, should a real product screen, photography, or illustration lead?”
- “Which two visual approaches must I strictly avoid?”

Bad question examples:

- “What kind of design would you like?”
- “Should it be modern?”
- “What is your color preference?” when brand colors are already visible in the app.

Do not create prototype files before this gate is resolved. Exception: the user explicitly says to make all choices autonomously or supplies enough information to answer every question.

After answers arrive, summarize the prototype contract in 5–10 concise bullets. Mark inferred items as assumptions.

Read `references/intake.md` for question selection rules.

## Phase 2 — Extract product truth

For an existing app or repository, inspect before selecting a design direction.

Extract:

- literal product category;
- target roles and primary user;
- strongest real user workflow;
- actual product terminology;
- real features that can be demonstrated;
- routes or screens that provide visual proof;
- logo, colors, fonts, icons, radius, shadows, and spacing behavior;
- current product strengths and visual weaknesses;
- claims that are unsupported and therefore forbidden.

For a landing page, separate **operational UI** from **marketing UI**:

- preserve brand recognition and product truth;
- amplify the strongest workflow and visual proof;
- do not paste the entire dashboard into a hero without composition;
- do not invent metrics, testimonials, customers, security certifications, integrations, pricing, or features.

If the app can run, capture relevant states at useful viewport sizes. If login is required and credentials were not supplied, ask only if that blocks product extraction.

Read `references/product-extraction.md`.

## Phase 3 — Research `DESIGN.md` directions

This phase is mandatory unless the user supplies an approved `DESIGN.md` and explicitly says not to research alternatives.

### 3.1 Check local design sources

1. Search for an existing `DESIGN.md` in the repository.
2. If found, read it and compare it with the actual product.
3. When `npx` is available, validate it with:

```bash
npx -y @google/design.md lint DESIGN.md
```

4. Do not assume an existing file is appropriate merely because it exists.

### 3.2 Search the web

Use current web research, but keep it targeted: inspect two or three credible alternative products or references that solve the same user problem, then stop once a defensible direction is clear. Start from:

- the official Google `DESIGN.md` specification for file structure and token rules;
- one or more current `DESIGN.md` libraries or catalogs;
- real products that solve a similar UX or marketing problem;
- current composition, typography, image, and illustration references.

Search using product-specific combinations, for example:

```text
<industry> <audience> landing page DESIGN.md
<visual attributes> <product type> design system
<primary workflow> product landing page reference
<brand adjectives> typography editorial web design
```

Do not search only for the user's requested color. Search by product category, audience, density, trust level, and intended emotional response.

### 3.3 Produce three candidates

Present three meaningfully different candidates. Each candidate must include:

- source and name;
- one-sentence visual thesis;
- why it fits the product and audience;
- what will be borrowed;
- what will be changed;
- asset strategy;
- risk or mismatch.

The candidates must differ structurally or conceptually, not only by color.

Example candidate families:

- product-led editorial with real app screenshots;
- warm human-centered composition with contextual photography;
- diagrammatic or illustration-led explanation of an abstract workflow.

### 3.4 Selection gate

Ask the user to choose Candidate A, B, C, or “custom hybrid.” Do not start coding until the user chooses, unless the user explicitly says “choose for me.”

If delegated, choose the strongest candidate and explain the decision in two or three sentences.

### 3.5 Create the adopted `DESIGN.md`

Create an original project-specific `DESIGN.md` that follows the official format:

- optional YAML frontmatter containing normative tokens;
- markdown rationale in the standard section order;
- exact colors, typography, spacing, radius, and component guidance;
- explicit screenshot, photography, illustration, icon, and motion rules;
- Do's and Don'ts.

Do not blindly copy a community file. If licensing or reuse rights are unclear, extract principles and write an original design system. Add a short “Research provenance” section listing the references and what was adapted.

Read `references/design-md-research.md` and use `templates/DESIGN.md` as a starting structure.

## Phase 4 — Decide visual and illustration strategy

Before building, choose one dominant visual-evidence strategy.

Use this priority order for an existing software product:

1. Real product screenshots or captured workflow states.
2. Existing brand assets and product media.
3. Carefully composed product mockups based on real screens.
4. Relevant licensed photography.
5. Generated raster imagery.
6. Original illustration.
7. Pure type, layout, texture, and data visualization with no hero image.

Use illustration when it:

- explains an abstract process;
- creates a product-specific brand world;
- communicates a concept that screenshots cannot;
- supports onboarding, empty states, or educational explanation.

Do not use illustration merely to fill space.

For raster visuals:

- download selected, stable, licensed image files into `prototype/<slug>/assets/` and reference them with relative paths;
- never embed or generate base64/data-URL raster images, even when portability would be convenient;
- never hotlink remote images in the finished prototype;
- use inline SVG only for simple original diagrams or decorative marks; use a coherent, established icon set only when an icon improves comprehension;
- keep visual choices purposeful: imagery should establish product, place, people, or a workflow; icons should clarify an action, state, or label rather than decorate empty space;
- avoid excessive image searches and downloads—select only the few assets needed to support the chosen visual thesis.

Never:

- fabricate a product screenshot when a real app exists;
- use generic floating 3D shapes, purple gradient orbs, or icon clouds;
- use unrelated stock photography;
- distort aspect ratios;
- hide important screenshots behind blur, extreme perspective, or unreadable cropping;
- hotlink unstable search-result thumbnails;
- present generated UI as if it were the real product.

Read `references/visual-assets.md`.

## Phase 5 — Build the single-file prototype

Create only:

```text
prototype/<slug>/index.html
prototype/<slug>/DESIGN.md
prototype/<slug>/Makefile
```

### `index.html` rules

The page must be valid semantic HTML and contain:

- `<!doctype html>`;
- language, charset, viewport, title, and description metadata;
- CDN imports in `<head>` or at the end of `<body>`;
- all CSS in inline `<style>` blocks;
- all JavaScript in inline `<script>` blocks;
- all prototype content and mock data inline;
- local raster image references must point to files in `assets/`, never base64/data URLs;
- accessible labels, focus states, and keyboard behavior;
- responsive layout without horizontal overflow;
- reduced-motion handling.

### CDN dependency policy

Use the fewest dependencies necessary.

**Default:**

```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

Tailwind's browser CDN is acceptable because this artifact is a prototype, not production.

**Icons:** Use one consistent icon family (Lucide by default) only when icons improve comprehension. Resolve the current stable version from official documentation and pin it. Initialize icons after the DOM loads. Do not mix icon styles, use emoji as UI icons, or add decorative icon clouds.

**Interaction:** Prefer vanilla JavaScript. Use Alpine.js only when several stateful interactions would otherwise create excessive imperative code. Pin the current stable version.

**Motion:** Prefer CSS transitions and the Web Animations API. Import Motion from a pinned CDN version only when timeline, scroll, spring, or orchestration behavior materially improves the prototype.

**Fonts:** Remote web fonts may be loaded with `<link>` tags. Use at most two families and ensure acceptable fallbacks.

Never use `@latest` for package imports in the final file. Record imported packages and versions in an HTML comment near the imports.

### Tailwind and design tokens

Use `DESIGN.md` as the source of truth and express it with the shadcn/tweakcn token contract inside one `<style type="text/tailwindcss">` block:

- `@custom-variant dark (&:is(.dark *));`
- `:root { … }` light tokens and `.dark { … }` dark overrides as CSS custom properties;
- `@theme inline { --color-*: var(--*); … }` to expose the tokens as utilities;
- `@layer base { *{ @apply border-border outline-ring/50; } body{ @apply bg-background text-foreground; } }`.

A [tweakcn](https://tweakcn.com) export pastes in directly. Ship both light and dark, toggling the `.dark` class with an anti-flash script placed before the Tailwind runtime. Never write the tailwindcss `@import` directive in this block — not even in a comment — its literal text silently breaks the browser CDN build.

Read `references/design-tokens.md` and start from `templates/index.html`.

### Interaction scope

Implement only the interactions needed to evaluate the design:

- working navigation anchors;
- mobile menu;
- tabs, accordion, modal, carousel, or demo controls only when relevant;
- primary CTA feedback;
- one or two meaningful motion moments;
- representative hover, focus, loading, empty, or error state where the decision depends on it.

Buttons must not be dead. A prototype CTA may scroll, open a modal, switch a state, or show a clear demo confirmation.

### Content rules

- Use realistic product-specific text.
- Reuse real terminology from the app.
- Do not use lorem ipsum.
- Do not repeat the same claim across multiple sections.
- Every section must have one job.
- Landing pages should usually stay within 4–7 main sections.
- Use one dominant CTA above the fold.

Read `references/single-file-prototype.md` and begin from `templates/index.html` when useful.

## Phase 6 — Create the prototype `Makefile`

Copy and adapt `templates/Makefile.prototype` to `prototype/<slug>/Makefile`.

Required targets:

- `make serve` — run a zero-install local static server;
- `make open` — open the prototype URL on macOS or Linux when possible;
- `make check` — verify required files and basic HTML structure;
- `make design-lint` — validate `DESIGN.md` through `npx -y @google/design.md`;
- `make clean` — remove only generated screenshots, temporary files, and local caches;
- `make reset` — run clean and return the prototype folder to its source state.

When the prototype uses downloaded visuals, `assets/` is part of the deliverable and must not be removed by `make clean` or `make reset`.

The Makefile must not run `npm install`, create `node_modules`, or require a package manager for `make serve`.

## Phase 7 — Browser verification and refinement

Run the prototype through a local HTTP server. Do not judge it only by reading HTML.

Verify at minimum:

- desktop: approximately 1440 × 900;
- tablet or compact desktop: approximately 1024 × 768;
- mobile: approximately 390 × 844.

Check:

- the primary value and CTA are understandable within three seconds;
- the page visually matches the adopted `DESIGN.md`;
- the existing app remains recognizable when it is the source;
- images and illustrations provide evidence or explanation rather than decoration;
- mobile order reflects content priority;
- no horizontal overflow, clipped text, broken image, or fixed-element collision exists;
- keyboard focus is visible;
- reduced-motion users are respected;
- all required interactions work;
- console errors are absent or documented.

Perform at least one critique-and-revision pass after the first render. Do not stop at the first visually acceptable screenshot.

Read `references/quality-gate.md`.

## Phase 8 — Handoff and stop

Report:

1. prototype mode and decision being tested;
2. selected `DESIGN.md` direction and research sources;
3. visual/illustration strategy;
4. exact files created;
5. CDN packages and pinned versions;
6. browser sizes and interactions verified;
7. known prototype limitations;
8. the next production decision, without implementing it.

Stop after the prototype files, including any required local assets, are complete. Do not migrate it into Next.js, React, Tailwind build tooling, or production routes unless the user explicitly requests that as a separate task.

# Hard rules

- Keep this skill's own instructions in English, but respond to the user, ask questions, and write prototype copy in the user's language.
- Delegate independent research and inspection to parallel subagents when the host supports them.
- Ask only unanswered, concrete questions.
- Do not code before the question and design-selection gates are resolved.
- Default to one self-contained `index.html`.
- Do not create package manifests or install dependencies.
- CDN dependencies must be necessary and version-pinned; Tailwind's official `@4` browser URL is allowed.
- `DESIGN.md` is required and must be researched or validated.
- A `Makefile` is required.
- Existing products are the source of truth for features, terminology, and screenshots.
- Real product screens outrank fake dashboards and generic illustration.
- Download raster visuals into the prototype's `assets/` directory and use relative paths; never use base64/data URLs or finished-prototype image hotlinks.
- Research a small set of relevant alternative products before choosing the direction; optimize research and output for signal, not token volume.
- Aim for modern, airy interfaces with deliberate whitespace, clear hierarchy, and restrained decoration; density may increase only where the product task requires it.
- Do not invent proof, metrics, customers, testimonials, or capabilities.
- Do not silently cross the prototype-to-production boundary.

# Output

The implementation artifact must be:

```text
prototype/<slug>/index.html
prototype/<slug>/DESIGN.md
prototype/<slug>/Makefile
```

The user-facing completion message must contain:

```md
## Prototype summary

## Design direction

## Visual evidence strategy

## Files created

## Verification

## Limitations

## Production decision remaining
```

# Anti-patterns

- Generating a Vite, React, or Next.js project for a rapid prototype.
- Asking vague style questions without inspecting the product.
- Coding immediately after the first prompt without a design-direction gate.
- Searching only for “modern landing page” and averaging random references.
- Copying a community `DESIGN.md` without adaptation or provenance.
- Creating a separate component file for every section.
- Importing five CDN libraries when vanilla JavaScript and CSS are enough.
- Using `latest` package URLs.
- Filling empty space with gradients, floating icons, or arbitrary illustration.
- Declaring the prototype complete without rendering it at desktop and mobile sizes.
