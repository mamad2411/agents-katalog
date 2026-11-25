---
name: targetbay-email-template-design
description: Use when designing or fixing how an ecommerce email looks — template layout and width, visual hierarchy, email-safe typography, colour and contrast, dark mode appearance, CTA design, imagery and images-off rendering, or building a reusable module library for campaigns and transactional messages.
license: MIT
metadata:
  author: TargetBay
  version: "1.0.0"
  homepage: https://targetbay.com
---

# TargetBay Email Template Design

Design guidance for ecommerce email templates — layout, hierarchy, type, colour, calls to action and
imagery. This is the visual layer only. *Which* message to send and when belongs to the lifecycle
flows; whether it arrives at all belongs to deliverability. Both live in the
[best practices skill](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-email-sms-best-practices).
Wiring the automation that sends it — the trigger, the operations, the guardrails — belongs to the
[automation recipes skill](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-marketing-automation-recipes).

Email is constrained design, and the constraint is the renderer rather than taste. A design that
ignores that is not bolder — it is one that some share of the list cannot read.

No markup in these documents: they cover the design decision, and the templating layer implements it.
Where the best practices skill already owns a rule — contrast targets, alt text, dark mode client
behaviour, which message to send — these documents cite it rather than restating it.

## Design Decision Order

Work down this order. Each level is worth nothing if the one above it fails.

1. **It renders** — width, column count, blocks that survive in the weakest client
2. **It is readable** — contrast, type size, images off, dark mode
3. **It is scannable** — hierarchy, spacing and block order, so the message lands before it is read
4. **It has one obvious action** — a call to action the eye finds without searching
5. **It looks like the brand** — colour personality, type personality, imagery

When a brand guideline and a level above it conflict, the level above wins and the guideline gets an
email-specific exception.

## Quick Reference

| Need to... | See |
|------------|-----|
| Choose width, column count, spacing and block order | [Layout](./references/layout.md) |
| Pick fonts that actually render, and set a type scale | [Typography](./references/typography.md) |
| Build a palette that passes contrast and survives dark mode | [Colour and Dark Mode](./references/colour-and-dark-mode.md) |
| Decide which blocks a template needs, and in what order | [Anatomy](./references/anatomy.md) |
| Design the button; decide how much of the message is imagery | [CTA and Imagery](./references/cta-and-imagery.md) |
| Make it work on a phone — stacking, tap targets, first screen | [Layout](./references/layout.md) |
| Fix something that renders wrong in a specific client | [Layout](./references/layout.md), then [Colour and Dark Mode](./references/colour-and-dark-mode.md) |
| Write the preheader, or lay out a product grid | [Anatomy](./references/anatomy.md) |
| Size, crop, compress or animate an image | [CTA and Imagery](./references/cta-and-imagery.md) |
| Review a design before it ships | [Design QA](./references/design-qa.md) |

## Start Here

**Designing a template set from scratch?**
[Layout](./references/layout.md) (the grid everything sits on) →
[Typography](./references/typography.md) and [Colour](./references/colour-and-dark-mode.md) (the
tokens) → [Anatomy](./references/anatomy.md) (which blocks, in which order) →
[Design QA](./references/design-qa.md) before the first send. Design the module set once; designing
per campaign is how a brand drifts.

**Opened, but nothing happens after?**
[CTA and Imagery](./references/cta-and-imagery.md) first — competing buttons, a call to action below
the fold, or a hero image carrying the whole offer so it vanishes with images off. Then
[Anatomy](./references/anatomy.md) for block order: the offer stated after the scroll is an offer
most of the list never sees.

**Looks broken in Outlook, or in dark mode?**
[Colour and Dark Mode](./references/colour-and-dark-mode.md) for anything that disappeared, went
grey-on-grey or turned into a bright rectangle. [Layout](./references/layout.md) for anything that
collapsed, stretched or gained a gap. Confirm against
[Accessibility](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/accessibility.md),
which describes how three classes of client handle dark mode differently.

**Building a reusable module library?**
[Anatomy](./references/anatomy.md) — block inventory and template governance — with
[Layout](./references/layout.md) for the spacing scale every module shares.
