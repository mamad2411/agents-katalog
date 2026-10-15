---
name: marketing-image-generation
description: Generate high-quality marketing images, ad creatives, launch visuals, social cards, blog headers, product mockups, thumbnails, and campaign assets. Use when the user asks to create, design, iterate on, or prompt an image for marketing, growth, social media, paid ads, landing pages, newsletters, or product launches.
---

# Marketing Image Generation

## Core Workflow

1. Identify the asset type: ad, social post, blog header, hero image, launch graphic, thumbnail, email banner, product mockup, or campaign visual.
2. Gather only missing essentials: goal, audience, channel, dimensions or aspect ratio, required copy, brand constraints, product context, and output count.
3. Check available context before asking: README, `DESIGN.md`, brand files, existing screenshots, product copy, and any user-provided reference images.
4. Draft a concrete visual direction before generating: subject, layout, composition, style, color palette, typography direction, lighting, mood, camera/framing, and constraints.
5. Use the image generation tool only when the user has explicitly asked for an image asset or visual mockup.
6. Review the result against the brief, then iterate with targeted changes instead of rewriting the whole concept.

## Marketing Defaults

- Prefer one strong focal point over collages.
- Make the product, benefit, or audience instantly legible at thumbnail size.
- Use short text in images. If copy is required, preserve it exactly and keep it to a headline or label.
- For product-led assets, show a plausible interface, workflow, or user outcome rather than decorative UI fragments.
- For paid ads, optimize for immediate comprehension, contrast, and a clear emotional hook.
- For editorial/blog assets, prefer a concept-driven image that supports the article thesis without repeating the title literally.

## Patterns to Avoid (AI Slop)

These are the tells of machine-generated marketing design. They cluster because
they're what an image/layout model reaches for by default — which is exactly why
they read as generic. The goal isn't to memorize a blocklist; it's to recognize
the family so you avoid the next variant too. The underlying principle: every
element should earn its place by carrying meaning or hierarchy. If it's there only
to look "designed," cut it.

Avoid these unless the user explicitly asks for one:

- **Eyebrow pills above the headline.** The little rounded badge with label text
  ("✨ INTRODUCING", "NEW", "v2.0") floating above the H1. It almost never adds
  information the headline doesn't already carry, and it's the single most common
  AI-layout tell. Lead with the headline itself.
- **Gradient-filled or glowing buttons.** Multi-color gradient fills, neon glow,
  or animated-looking sheen on CTAs. Use a single solid accent color with a
  flat or very subtle shadow. A button should look pressable, not radioactive.
- **The default purple→pink/violet tech gradient.** Indigo-to-magenta backgrounds
  (the generic "AI startup" wash) signal template, not brand. Anchor color in the
  product's actual palette. A gradient is fine when it's restrained and on-brand —
  the problem is reaching for *that* gradient as a default.
- **Emoji and sparkle (✨/🚀/⚡) ornament.** Decorative emoji used as design
  elements rather than content. They cheapen the composition and date instantly.
- **Glassmorphism everywhere.** Frosted, semi-transparent blurred cards stacked in
  depth for no functional reason. One blurred foreground card can work (see
  `examples/blurred-bg-foreground-component.html`); a whole scene of them is slop.
- **Generic startup imagery.** Floating dashboards without context, handshake
  photos, rocket/lightbulb metaphors, vague abstract 3D — blobs, glossy spheres,
  isometric doodads, gradient orbs that don't represent anything.
- **Decoration over hierarchy.** Heavy drop shadows on every element, oversized
  border-radius on everything, neon glow text, and centered-everything with no
  size/weight contrast. Polish comes from clear hierarchy and spacing, not effects.
- **Dense copy.** Paragraphs, multi-sentence subheads, or stacked feature lists
  crammed into an image. If it can't be read at thumbnail size, it doesn't belong
  in the image — move it to the surrounding page.
- **Fake credibility filler.** Invented "Trusted by" logo rows, placeholder star
  ratings, or stat trios with made-up numbers. Use real assets or omit them.

If the user *wants* one of these (e.g. "give me that glassy gradient look"), do it
well — this list is about defaults, not absolute prohibition.

For HTML/Satori-rendered assets, the bundled libraries are the slop-free starting
point: the layout skeletons in `examples/layouts/` lead with the headline (no
eyebrow pills), use solid-fill buttons, and rely on hierarchy over effects; the
backgrounds in `examples/backgrounds/` give you restrained, on-brand washes and
grids instead of the default purple→pink gradient. Start from those (see the
Reusable Layouts and Reusable Backgrounds sections below) rather than improvising
decoration.

## Prompt Template

Use this structure when calling the image generation tool:

```text
Create a [asset type] for [product/company/campaign].

Goal: [conversion goal or message]
Audience: [specific audience]
Format: [dimensions/aspect ratio/channel]
Composition: [primary subject, layout, focal point, depth, framing]
Style: [visual style, medium, brand feel]
Color and lighting: [palette, contrast, mood]
Text: [exact text, or "no text"]
Brand constraints: [logo usage, typography direction, do/don't]
Avoid: [specific visual cliches, clutter, wrong objects, unsafe claims]
```

## Reusable Backgrounds

For HTML/Satori-rendered assets (OG cards, Vercel `ImageResponse`, og-playground),
start from the background library in `examples/backgrounds/`. Each file is a single
JSX snippet you make the outer container and drop content inside. Categories: dark
(dot/line grids, grid-glow, mesh aurora, spotlight, crosshatch, vignette), light
(grids, blueprint, grid-fade, pastel mesh, warm/cool washes), and vibrant
(sunset, ocean, mesh, stripes, gradient+grid). Rendered previews are in
`/images/backgrounds`. See `examples/backgrounds/README.md` for the catalog and the
Satori constraints (no `conic-gradient`; dotted patterns need percentage color
stops; per-layer `backgroundSize` for grid + glow; fake fades with a same-color
radial overlay).

## Reusable Layouts

For HTML/Satori-rendered assets, `examples/layouts/` has 18 generic, brand-free
layout skeletons (placeholder copy only): heroes (centered, split), feature trio,
stat trio, big number, testimonial, social-proof bar, logo cloud, announcement
banner, blog header, pricing card, CTA banner, checklist, how-it-works steps,
comparison columns, product/browser showcase, terminal window, and event/webinar
card. Make a layout the root element, swap copy/colors/screenshots, and pair it
with a background from `examples/backgrounds/`. Rendered previews are in
`/images/layouts`; see `examples/layouts/README.md` for the catalog.

## Channel Guidance

- LinkedIn or X launch image: 16:9 or 1.91:1, bold single message, product screenshot or conceptual hero, readable at feed size.
- Instagram or TikTok cover: 4:5 or 9:16, centered subject, high contrast, minimal text, strong hook.
- Blog header: 16:9, editorial composition, room for title overlay if needed, avoid ad-like CTA styling.
- Landing page hero: wide composition, clean negative space, product context, brand-consistent lighting and palette.
- Paid ad: clear benefit, high contrast, direct product/category cues, no tiny UI details, no dense copy.

## Iteration Rules

When revising a generated image:

- Change one or two variables at a time: composition, color, copy, product prominence, realism, or format.
- Preserve what worked from the previous result explicitly.
- If text rendering is poor, reduce the amount of text or move text into the surrounding page instead of forcing dense copy into the image.
- If brand fit is weak, anchor the next prompt in concrete brand traits: colors, typography feel, product screenshots, website style, or visual references.

## Output

Return the generated image and a brief note with:

- The intended use case and format.
- Any assumptions made.
- Suggested next iteration only when there is a clear improvement path.
