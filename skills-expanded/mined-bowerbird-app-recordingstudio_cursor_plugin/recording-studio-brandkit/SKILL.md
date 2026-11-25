---
name: recording-studio-brandkit
description: Generate a Recording Studio brand-kit board (logo, palette, type, applications). Use when a host needs identity direction before screens. This is an image job. Flatpack ViewComponents, tokens, and named themes apply only when the board hands off to code.
---

# Recording Studio brandkit

Taste and branding are direction. Implementation is always Flatpack ViewComponents, tokens, and named themes. The dummy default is `html data-theme="rounded"` plus core `UsesDefaultLayout`. Hosts get a named theme (for example `featured-in`), not forked CSS. Never Tailwind, shadcn, GSAP, custom CSS kits, or third-party UI libraries on gem, dummy, or Admin screens. If a look is missing, add a Flatpack token or component first.

Adapted from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) `skills/brandkit` (MIT, Leonxlnx). See `docs/taste-skill-attribution.md`.

This skill generates brand images. It does not restyle dummy, gem, or Admin. After the board exists, map tokens into a named Flatpack theme with `recording-studio-taste`, `recording-studio-flatpack`, and `recording-studio-ui`. Direction packs: `recording-studio-soft`, `recording-studio-minimalist`, `recording-studio-brutalist`. Web or mobile comps: `recording-studio-imagegen-web`, `recording-studio-imagegen-mobile`.

## When to use

- A host needs a logo system, identity deck, or visual-world board
- You need palette, type, and metaphor before picking a named theme
- The user asked for brand guidelines, not a coded screen

Keep this an image job until someone asks for screens. Then hand off to Flatpack. Do not implement the board as a Tailwind page.

## Before generating

Infer strategy: category, audience, product job, emotional promise, trust level, metaphor, what to avoid.

A brand kit is a visual argument.

1. What does this brand represent?
2. What is the core metaphor?
3. How does the logo express that?
4. How does the system scale across UI, print, and detail?
5. Why is it ownable?

Do not pick symbols at random. Developer tools lean frame, bolt, grid. Security leans shield, eye, seal. Luxury leans monogram, paper, emboss. Recording Studio hosts should feel like a product people work in, not a generic AI spark.

## Logo

Simple, memorable, scalable, usable as icon, wordmark, badge, and UI mark.

Methods (use one, or two at most): monogram plus meaning, product action, metaphor fusion, negative space, construction geometry.

Avoid generic lightning, random animals, fake crests, copied famous marks, clipart, sparkles, inconsistent variants.

## Default board

One overview image unless asked for more. Default `3 × 3`, aspect `4:3` or `16:10`, clean gutters, little text.

Panels:

1. Logo cover
2. Construction / geometry
3. Digital application (browser or app chrome as identity, not a fake dashboard)
4. Tagline
5. Color system
6. Type specimen
7. Physical application
8. Image direction
9. System detail (chips, inputs, icon row)

Allowed layouts: `3×3`, `2×3`, `2×2`, `1×3`, `4×2`.

Rhythm: quiet, functional, emotional, technical, atmospheric, detailed. Not every panel equally loud.

## Visual modes

Pick one: dark developer, dark operator, dark nature, dark security, light editorial / compliance, luxury / beauty, voice, cultural / experimental.

One palette: base, primary accent, secondary accent, neutrals. Accents repeat across panels. No rainbow. No default purple-blue AI glow.

Text is sparse: name, one tagline, one URL, a few labels. No lorem, no paragraphs, no unreadably tiny menus.

Taglines stay short and specific. Avoid corporate soup.

## Images and mockups

Art-directed, palette-matched. No generic office stock, no robot clichés.

Mockups are identity applications: browser chrome, app icon, card, badge, input. Not a feature demo and not a soulless dashboard.

## Anti-generic

No floating icon clouds, startup mesh gradients, overdesigned marks, messy collages, inconsistent logos, cheap neon, PowerPoint boards.

If references are supplied, steal rhythm, density, and restraint. Do not copy the mark, name, or slogan.

## Handoff to code

When screens come next:

- Extract canvas, surface, text, accent, radius, and type roles
- Put them on a named Flatpack theme
- Dummy / gem / Admin stay rounded unless opted in
- Compose with `recording-studio-flatpack`. Do not rebuild the board in custom CSS

A Taste critique of the board is welcome (what the system is, what is strong, what would look better, one highest-leverage change) before anyone writes views.
