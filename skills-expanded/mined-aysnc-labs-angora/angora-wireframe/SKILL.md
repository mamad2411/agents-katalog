---
name: angora-wireframe
description: Sketch or update a rough page wireframe in `src/pages/design-system/wireframes/` — ASCII art or gray placeholder boxes — showing structure and flow before real components or visual design exists. Trigger whenever the user wants to sketch, rough out, outline, or draft the structure of a page before building anything, or iterate on an existing wireframe's section order, proportions, or hierarchy. Phrases like 'sketch the careers page', 'rough out the pricing layout before we build', 'wireframe the blog detail', 'just boxes for now', 'draft the structure for /about', 'I need to see how the signup flow goes before committing' all trigger this.
argument-hint: <page-name>
---

# Wireframe: $ARGUMENTS

Sketch page structure (hierarchy, layout, flow) before committing to visual design.

## Before you start

1. **Read `src/system.md`** — intent and scope.
2. **Read `src/styles/global.css`** — know the container max-width and spacing tokens.
3. **Check if the wireframe already exists** — look for `src/pages/design-system/wireframes/<page-name>.astro`. If it exists, read it first.

## Ask: format preference

Use `AskUserQuestion` to ask the user which wireframe format they prefer:

- **ASCII** — wireframe stored as ASCII art in a `<pre>` block. ~100-200 tokens per page. Best for fast iteration.
- **Visual** — wireframe rendered as gray Tailwind boxes (`bg-muted border border-border`, placeholder text). More visual but more tokens.

## Output files

1. **Design system page** — `src/pages/design-system/wireframes/<page-name>.astro` (using `Layout` from `_layout/`)

No full-screen view needed — wireframes are working docs, not deliverables.

## Steps

1. **Ask format** — ASCII or Visual (see above).
2. **Sketch** — create the wireframe page showing page structure: header, hero, sections, footer. Use placeholder text and rough proportions.
3. **Visual review** — user opens page in browser (`pnpm dev`). The sidebar auto-discovers wireframe pages via `import.meta.glob` — no manual nav registration needed. Approves or iterates.
5. **Iterate** — ask user for feedback ("move CTA above fold", "make it 3 columns", etc.) and update the wireframe.
6. **Notes** — ask if they want to save notes with the wireframe (intent, constraints, open questions).
7. **Data sources** — walk through each section and capture data source decisions.

### ASCII format

Use a `<pre>` block with monospace box-drawing to show page structure:

```html
<pre class="font-mono text-sm leading-relaxed text-muted-foreground">
┌─────────────────────────────────────┐
│  Logo          Nav    Nav    [CTA]  │
├─────────────────────────────────────┤
│                                     │
│           Hero Headline             │
│           Subhead text              │
│        [ Primary ]  [ Secondary ]   │
│                                     │
├─────────────────────────────────────┤
│  Feature 1  │  Feature 2  │  Feat 3│
└─────────────────────────────────────┘
</pre>
```

## Notes and data sources

After sketching the wireframe and getting visual approval, capture the thinking behind the layout. This turns the wireframe from a sketch into a brief that `angora-compose-page` can act on.

### Notes

Ask the user: *"Any notes to save with this wireframe? Intent, constraints, open questions — anything the layout alone doesn't capture."*

Capture whatever the user shares. Good notes answer things like:
- What's the goal of this page? (conversion, education, trust)
- What constraints matter? (must work without images, CTA above fold)
- What's the tone? (confident, playful, minimal)
- Open questions or things still undecided

If the user has nothing to add, skip — notes are optional.

### Data sources

For each section in the wireframe, ask:

- "Will this content change? Is there more than one of these?" → **template** (reference a database table)
- "Is this one-off copy edited in code?" → **static**
- User unsure? → `data: undecided`

### Frontmatter format

Write notes and data sources together as a JS comment block in the Astro file's frontmatter:

```astro
---
import Layout from '../_layout/Layout.astro';
/*
  Notes:
  - Hero must convert to free trial signups — keep CTA above fold
  - Testimonials are the trust signal — show faces, not logos
  - Pricing should feel simple — no feature comparison matrix

  Data sources:
    - component: Hero
      data: static
    - component: Testimonials
      data: table:testimonials
    - component: Pricing
      data: table:pricing_tiers
*/
---
```

This is consumed by `angora-compose-page` when building the real page.

After wireframing, suggest building a layout: *"Want to assemble this as a layout with real components? Run `/angora` to build a layout for this page."* Layouts live at `src/pages/design-system/layouts/<page-name>.astro` and prove the composition works with real components before wiring up data.

### Visual format

Use gray Tailwind boxes with placeholder text:

```html
<div class="space-y-4">
  <div class="bg-muted border border-border rounded p-4 flex justify-between items-center">
    <span class="text-sm text-muted-foreground">Logo</span>
    <div class="flex gap-4 text-sm text-muted-foreground">Nav · Nav · Nav</div>
  </div>
  <div class="bg-muted border border-border rounded p-12 text-center">
    <p class="text-lg text-muted-foreground">Hero Section</p>
  </div>
</div>
```