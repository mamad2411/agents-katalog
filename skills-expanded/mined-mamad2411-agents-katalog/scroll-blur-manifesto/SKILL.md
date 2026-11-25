---
name: scroll-blur-manifesto
description: Design or implement quiet editorial manifesto sections where large text resolves from blurred ghost layers into sharp copy on scroll. Use when the user asks for scroll blur, blur-to-sharp transitions, Lenis/GSAP ScrollTrigger word reveals, or a warm editorial manifesto section.
---

# Scroll Blur Manifesto

Use this skill for the section after a loud hero: the moment where the argument comes into focus as the user scrolls.

The target feeling is quiet, precise, editorial, and inevitable. It should contrast with kinetic hero energy rather than compete with it.

## Core Direction

Build a restrained manifesto section with:

- warm near-white canvas
- black text at varying opacity
- compact bordered mono chip
- hairline rules when useful
- generous but controlled spacing
- one large left-aligned paragraph
- selected words highlighted as filled pills

This is not a feature grid, screenshot gallery, or card stack. It is a narrative transition.

## Recommended Tools

For implementation, prefer:

- Lenis for smooth scroll
- GSAP + ScrollTrigger for scrub-linked progress
- two text layers: one sharp, one statically pre-blurred
- opacity crossfades between layers for performance
- `prefers-reduced-motion` fallback with readable static text

Do not animate `filter: blur(...)` independently on dozens of words during scroll. That commonly janks. Pre-blur the ghost layer once, then animate opacity.

## Layout Pattern

The typical structure:

1. A small mono chip above the text, for example `Introducing Zine`.
2. A visually hidden complete sentence for crawlers and screen readers.
3. A sharp visible text layer split into word spans.
4. A matching ghost text layer in the same position with `filter: blur(6px-10px)`.
5. ScrollTrigger timeline that reveals ghost words first, then crossfades to sharp words.

Keep the paragraph measure broad but controlled, around `max-width: 960px-1080px` for desktop. Use `text-wrap: pretty` or `balance` where supported.

## Motion Choreography

The scroll behavior should be reversible and scrubbed:

- as the section enters, side labels/chips settle in from slight blur/opacity
- each word appears first as a blurred ghost
- the ghost state holds briefly so the blur is visibly felt
- the sharp layer rises as the ghost layer fades at the same position
- highlighted pill words participate in the same reveal
- when scrolling past, sharp words dissolve back through ghost blur and then out
- the final footnote or source line can be the last element standing

A useful ScrollTrigger shape:

```text
trigger: manifesto block
start: top 65%
end: bottom 30%
scrub: 1
```

Tune these values to the page rhythm.

## Zine-Style Manifesto Copy

For an AI-search growth product, this section can use:

```text
Your customers ask ChatGPT, Claude, Gemini, Etc., and take whatever answer appears. If you're not in it, you've disappeared. The problem isn't your product. It's that everything you publish just sits there. Zine puts agents on it: writing, optimizing, and watching across your site, blog, newsletter, and social, so you get a little more findable every week. You run the business. The agents do the rest.
```

Highlight these as electric-blue filled pills:

- ChatGPT
- Claude
- Gemini
- Etc.
- site
- blog
- newsletter
- social

## Visual Restraints

Avoid:

- generic fade-in reveals
- decorative blur blobs or gradient orbs
- cards around the manifesto text
- screenshot panels in this transition section
- centered hero-scale H1 treatment
- animated effects that obscure the paragraph at rest

The section should feel like chaos turning into clarity: after the loud hero, the product argument becomes readable.

## Contained Example

If available in the plugin package, inspect `../../examples/contained-ui-motion-demo.html` for a single-file HTML/CSS/JS implementation reference. Use the manifesto section as a concrete model for layered sharp and ghost text, Lenis-smoothed scroll, GSAP ScrollTrigger progress, its own persistent Section reveal panel using the vanilla DialKit adapter and a `Copy component` action, pre-blurred copy, highlighted pills, and reduced-motion fallback. In production work, preserve the same performance principle: pre-blur once, then animate opacity and transform.
