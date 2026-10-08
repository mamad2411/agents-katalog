---
name: design-system-first
description: How to make a visual change inside someone else's codebase — read the project's design system first, reuse what exists, and change only what was asked. Load this before any styling, layout, spacing, colour, type, or component work on a target project. Read it before acting on any general design-taste guidance, which it overrides.
---

# Design system first

You are changing a real product that other people built and maintain. Your taste is not the
authority here — the project's design system is. Someone chose those tokens, and every value you
invent is one they now have to notice, review, and live with.

## Before you change anything visual

1. Read the design system files `start_task` listed. If it listed none, find them: the theme or
   Tailwind config, the global stylesheet, the token file, the component directory.
   `start_task` also reports whether the project carries impeccable's own context — `PRODUCT.md`
   (what the product is and who it is for) and `DESIGN.md` (its tokens, and the reasoning behind
   them). When it does, that is the design system, written down on purpose. Read it first and
   follow it over any general taste guidance, this file included.
2. Find the closest existing thing to what you need — a token, a utility, a variant, a component.
3. Read a neighbouring component that already does something similar, and copy how it does it.

If you skipped straight to editing, you are guessing.

## Reuse before you invent

- A spacing value must come from the project's scale. Not `13px` because it looked right.
- A colour must be an existing token. Not a new hex, not a near-miss of one already there.
- A component must be the project's own. Not a new one that duplicates something in its library.
- A font size, weight, radius, and shadow all come from the scale, the same way.

If what you need genuinely does not exist, say so and propose adding it, naming what it would sit
next to. Adding a one-off value silently is the failure mode this exists to prevent — it looks
like the change worked and leaves the design system slightly worse every time.

## Change what was asked, not what you would redesign

A request to make one card roomier is a request about one card. You will notice other things while
you are in there — a weak hierarchy, a generic layout, an inconsistent accent. Say what you
noticed, then leave it alone. An unasked-for redesign arriving inside a small request is how a
reviewer loses trust in every future change.

Scope also decides how honest your edit intents are. "Also cleaned up the surrounding section" is
a different change from the one that was approved.

## When general design guidance disagrees with the project

Other design skills you may load describe what good looks like in the abstract: replace default
fonts, pick a single accent, break symmetric layouts, add texture. That guidance is for work with
no existing system, or for a redesign someone actually asked for.

Inside a target project, it loses to what the project already does. A codebase that uses Inter
everywhere and three accent colours has made a decision — possibly a bad one, but not yours to
overturn on a copy tweak. Use the general guidance for the parts still genuinely open to you:
spacing rhythm, hierarchy, states, transitions, alignment, and the wording of what you write.

The exception is a defect, not a preference: a missing focus ring, an unreadable contrast ratio,
a control with no hover or disabled state. Fix those when you are already in the file, and say
that you did.

## Before you say it is done

- Every value you added traces back to a token or an existing pattern — name them if asked.
- The diff touches only what the request covers.
- The change holds up at narrow widths, and in dark mode if the project has one.
- You have looked at it running, not just at the code.
