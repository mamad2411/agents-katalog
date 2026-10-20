---
name: kinetic-inflated-hero
description: Design or implement full-viewport kinetic typography heroes using inflated physical letterforms, Matter.js-style motion, Pretext-inspired type behavior, and SVG goo/blur effects. Use when the user asks for a memorable animated hero, kinetic brand object, inflated type, soft-body letters, or a Zine-style "invisible" AI-search hero.
---

# Kinetic Inflated Hero

Use this skill when designing or building a homepage hero whose main visual is kinetic typography, not a screenshot, card, dashboard mockup, or conventional centered H1.

The target feeling is a full-viewport brand object: loud, physical, electric, and memorable from a single screenshot.

## Core Direction

Create a full-viewport hero with a strict, high-contrast palette. The reference pattern is Zine's electric-blue hero: saturated blue background, oversized inflated white typography, restrained overlay copy, and compact glass/white CTAs.

The letterforms should feel physical and alive:

- inflated, soft, pressurized, and tactile
- drifting, colliding, stretching, squashing, and settling
- deflecting around support copy, navigation, and CTAs
- more like kinetic type or an interactive brand installation than a SaaS hero

Use Pretext-inspired kinetic typography as a directional reference, but do not default to ASCII/noise aesthetics unless the user asks. The default visual surface is inflated white type on a saturated field.

## Recommended Tools

For implementation, prefer:

- React / Next.js for the component surface
- Matter.js or equivalent physics for collision and obstacle behavior
- opentype.js when deforming real font outlines into soft-body glyphs
- SVG filters for goo, dilation, blur, and deformation
- CSS keyframes for small repeatable letter effects
- requestAnimationFrame only when needed for physics/render loops
- pointer and scroll inputs as optional forces, not mandatory gimmicks

If a project already has motion infrastructure, adapt to it instead of adding dependencies automatically.

## Hero Composition

A good composition usually has:

- a full-bleed hero section, height `100svh`
- a floating nav over the field, usually glass or translucent white
- one compact support-copy block near the lower center
- two compact CTAs below the support copy
- kinetic letterforms occupying the whole canvas, including edge/corner positions
- overlay text and buttons treated as obstacles that type flows around or avoids

For a Zine-style AI-search hero, use this content model:

```text
Your site is invisible to ChatGPT, Claude, Gemini, Perplexity, Grok.
```

Do not render this as a normal static headline. Embed it in the kinetic type system. Let the active AI model name rotate, swap, inflate, or collide into place.

Support copy:

```text
Zine is your always-on growth marketing engine. Agents that write, optimize, and watch your competitors across every channel, so you show up where your customers are looking.
```

CTAs:

```text
Start free
See how it works
```

## Signature Invisible-Word Effect

When the concept includes the word "invisible," make it the signature interaction.

The effect should feel like the word briefly disappears from the page:

- per-letter stagger
- defocus into blur
- opacity drop toward invisible
- tiny rotation or vertical drift
- a short hold while absent
- refocus back into place

Use CSS keyframes for this effect unless a richer animation system is already present. Keep it legible at rest and honor `prefers-reduced-motion`.

## Visual Restraints

Avoid:

- standard SaaS hero composition: centered headline plus product screenshot
- dashboard mockups inside the hero
- generic AI sparkles, glowing network nodes, or purple gradients
- multi-color gradients unless the user explicitly asks
- stock imagery
- cards or panels as the main visual device
- motion that overwhelms the CTA or makes the product claim unreadable

The hero can be experimental; the conversion controls should stay quiet and usable.

## Reference Asset

If available in this skill package, inspect `assets/zine-hero-reference.png` for the rough expected shape: electric-blue full viewport, sparse inflated white letterforms, lower-center copy and CTAs, and a floating nav.

## Contained Example

If available in the plugin package, inspect `../../examples/contained-ui-motion-demo.html` for a single-file HTML/CSS/JS implementation reference. It measures the hero's text blocks to size letter groups around them, uses the vanilla DialKit adapter for persistent Hero controls and a `Copy component` action, Matter.js bodies for pointer collision, a timed letter pop and synchronized per-letter invisible-word blur/refocus, and a reduced-motion fallback. Its `@font-face` URL points to OT2049 Bold in a sibling Zine checkout for local preview; replace that URL with a licensed font asset in another project. In production React/Next.js work, translate the structure into components, load local fonts with `next/font/local`, and use `opentype.js` plus Matter.js for real OT2049 soft-body glyph deformation when that level of fidelity is required.
