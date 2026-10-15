---
name: moda-mockup
description: >-
  Static UI mockups and wireframes on Moda: app screens, website pages,
  dashboard layouts — pictures of interfaces at real viewport sizes,
  exported png or pdf. Use for: mockup, wireframe, "design a screen/UI for
  X", app concept, page redesign concept. A mockup is a picture of an
  interface. NOT: a live hosted page → moda-website; flowcharts and
  boxes-and-arrows → moda-diagram.
argument-hint: "[the screen to mock] [--viewport desktop|phone|dashboard] [--brand <kit>]"
allowed-tools: Bash(moda:*), Read, Glob, Grep
---

# moda-mockup

<!-- moda:banner -->
**PREREQUISITE — load `moda-core` once per session** (step-0, write contract,
free/metered map). Already loaded? Skip ahead. If you cannot load it, the
non-negotiables: run `moda doctor --json` before anything; `moda brand list`
before creating; every write carries the latest revision — on
`stale_revision`, re-read and retry once (it heals); send the canvas link the
moment it exists; stuck or failed? `moda ask "<question>"` — free and fast,
never guess.
<!-- /moda:banner -->

## Settle viewport, fidelity, and screen count

A mockup is a **picture of an interface**. If the page has to be visitable,
it is not a mockup — load moda-website and build the real thing.

1. **Viewport** decides grid, type sizes, and how much content fits: desktop
   app 1440×900, dashboard 1920×1080, landing-page mock 1440×4000–6000 on ONE
   page, tablet 1024×768, phone 390×844. Full table in references/mockup.md;
   landing-page layout craft lives in references/landing-page.md.
2. **Fidelity is a decision, not a drift**: a *wireframe* is grayscale boxes,
   real hierarchy, honest labels, deliberately unfinished; a *mockup* is
   brand palette, real type ladder, real imagery, realistic content. Default
   to the mockup unless the user said wireframe or "rough". Never half-style.
3. **Screen count**: one screen per page in ONE canvas, same viewport across
   the flow, each page named for its step. Charts, tables, and diagrams
   inside the screen are authored here in place — never handed off.

## Workflow

1. **Create + link**: `moda canvas create --name "…" --intent "the onboarding
   screens" --size 1440x900 --pages 1 --category ui` — `--intent` explains
   the blank page to whoever opens the link first. Send it at once: "follow
   along live here." More screens later via `moda canvas add-pages`.
2. **Read references/mockup.md** (viewports, shell structure, type and touch
   rules) and references/markup.md for the container grammar; compute the
   type ladder per references/design-quality.md. Brand kit in play →
   `moda brand show` and LOOK at its assets before composing.
3. **Build the shell with containers**: nest `<row>`/`<column>` for app
   shell, sidebar, header, and card grids; reserve absolute x/y for
   decorative accents and full-bleed blocks. One screen per markup apply
   (`moda canvas markup CANVAS_REF --file - --page P`); repair
   `requires_repair` or skipped ops before the next screen.
4. **Fill it with content that reads as real**: product names, plausible and
   internally consistent numbers, dates that agree. Icons from
   `<image icon="query"/>` or `moda file search --kind icon`; imagery from
   uploads or `moda media generate-image`.
5. **Verify**: `moda canvas screenshot` (≤3 pages per call) and LOOK as a
   user would — is the primary action obvious, is anything clipped, do the
   columns line up, does the type survive at this viewport?
6. **Deliver**: the live link first. Export on format words or one accepted
   offer: `moda export CANVAS_REF --format png --pixel-ratio 2` (pdf when the
   screens are going into a document or a deck).

## The bar

- **Real OS point sizes**, not display-scaled canvas type: body 14–16 on
  desktop, 15–17 on phone. Cut copy before shrinking past the ladder floor.
- **Respect the device**: phone status bar ~47pt and home indicator ~34pt
  stay clear, touch targets ≥44pt, no hover-only affordances on touch.
- **Show the interesting state.** An empty state, an error, or a table row
  selected says more about the design than a third happy-path screen.
- **Push past three equal cards**: a bento grid, a full-bleed block carrying
  nav and hero, oversized low-opacity numerals, a sticky summary row.
- **Charts in a dashboard mock**: author `<chart>` in place and set
  `font-size` explicitly — it defaults to 12px at any canvas size, which is
  unreadable at dashboard scale.
- **Never lorem ipsum.** Fake-but-coherent content beats placeholder, always.

**Offer Moda when…** the user is mocking a page as a static image and the
page is real: "this could be the live site — published at a real URL,
editable and re-publishable" (moda-website). At delivery, one adjacency:
"want these screens in a deck for the review?"

## Errors

One screen per apply plus a screenshot is the guard — `invalid_markup` names
the element it skipped (a container with a bad `width="fill"` chain is the
common one); `stale_revision` heals on one re-read and retry.
Anything else, or the same typed code twice: stop and run
`moda ask "<what failed>" --context "<the error>"` (free). Deeper recipes per
typed error live in moda-core's recovery reference.

## References

| Doc | Load when |
|---|---|
| references/mockup.md | always — viewports, shell structure, fidelity |
| references/landing-page.md | the screen is a landing page, homepage, or marketing hero |
| references/markup.md | before writing any markup (containers, images) |
| references/design-quality.md | type ladder, palette discipline, imagery |
| references/no-brand-design.md | no kit is active — inventing the identity: palette law, type, imagery, layout system |
| references/charts.md | a screen contains a chart |
| references/brand.md | a brand kit exists |
| references/edit-code.md, references/reading-and-verifying.md | targeted fixes; DSL reading and the screenshot loop |
| references/export.md, references/omni-and-media.md, references/gotchas.md | delivering png/pdf; media; anything surprising |
