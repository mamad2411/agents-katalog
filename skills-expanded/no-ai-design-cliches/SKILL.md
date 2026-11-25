---
name: no-ai-design-cliches
description: >-
  Avoid the default visual choices that make a web UI look AI-generated, and
  make intentional ones instead. Use this WHENEVER you build or style a web
  page, component, landing page, or app screen with CSS or a UI framework. The
  purple-to-blue diagonal gradient, glassmorphism cards everywhere, a centered
  hero with an emoji and two gradient buttons, neon glow on dark, and default
  system-font-only type are the look that signals "a model designed this".
  Replace each default with a deliberate choice about type, color, spacing, and
  layout that fits the actual product.
---

# No AI design cliches

There is a house style that generated UIs fall into: a violet-to-indigo gradient
background, frosted glass cards, a dead-centered hero with a big emoji, two pill
buttons (one filled gradient, one outline), and everything floating in generous
symmetric padding. None of it is broken, but together it reads as a default, the
visual equivalent of lorem ipsum. The fix is not a different cliche; it is making
each choice on purpose.

The rule: for type, color, and layout, pick something because it fits this
product, not because it is the safe generated default.

## The tells, and what to do instead

- **Purple/indigo gradient on everything.** The `#7c3aed -> #4f46e5` diagonal is
  the signature. Choose a palette from the product's actual brand or content.
  Flat color, or a restrained gradient, beats the default violet.
- **Glassmorphism by default.** `backdrop-filter: blur` frosted cards stacked
  everywhere. Use real surfaces and borders; reserve blur for when there is a
  reason (an overlay over content).
- **Emoji as hero art and feature icons.** A giant rocket in the hero, emoji
  bullets in the feature grid. Use real iconography and real imagery (see
  `prefer-icons`).
- **Everything centered.** Centered hero, centered feature cards, centered CTA.
  Centering everything removes hierarchy. Use a left-aligned, asymmetric layout
  where it earns attention.
- **System-font-only with no type scale.** Default `font-family` and three
  near-equal sizes. Choose a typeface on purpose and set a real scale with clear
  jumps between heading and body.
- **Neon glow on pure black.** `box-shadow` glow on a `#000` background for
  "tech" vibes. Pick a considered dark surface (not pure black) and use shadow
  for depth, not decoration.
- **Two gradient pill buttons, side by side.** Define a real primary action and a
  quieter secondary one; they should not look like twins.

## How to make it intentional

- Start from the content and brand, not a template. What does this product feel
  like, and what is the one action you want?
- Set a type scale and a small color palette first, then build with them.
- Establish hierarchy: one clear focal point per screen, not five equal cards.
- Use whitespace to group and separate, not just to fill.
- When you do use a gradient, glow, or blur, be able to say why it is there.

## Before you deliver

Look at the screen and ask: could this exact treatment sit on any other product
unchanged? If the gradient, the centered emoji hero, and the glass cards would fit
a hundred other sites, it is the default look. Replace the borrowed choices with
ones that fit this product's content, type, and brand.

For the words on the page, pair this with `no-filler-phrases`, `no-em-dashes`,
and `no-fancy-ascii`. For icons specifically, see `prefer-icons`.
