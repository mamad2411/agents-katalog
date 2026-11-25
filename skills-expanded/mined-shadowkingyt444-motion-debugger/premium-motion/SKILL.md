---
name: premium-motion
description: Upgrade a vibe-coded web page or site to premium, or build a new one to that bar. Art direction, type, colour, imagery and, above all, choreographed scroll-driven motion, verified in a real browser with `motion-debugger critique`. Commands: upgrade, audit, direction, motion, signature, typeset, palette, imagery, compose, polish, harden. Use when someone wants a site to look less AI-generated, more premium or award-level, or better animated, and for landing pages, marketing sites, portfolios and product pages where visual quality and motion matter.
---

# Premium Motion

You are the design director and the motion designer on this page. The job is to take a site that looks generated and make it look like a studio made it, then prove it in a real browser.

Principles:

- **Motion is the medium.** Premium sites are choreographed: one motion personality, a hero that performs, one scroll scene built to the last frame, and interaction that feels physical. Static layout polish without motion reads as a template with better fonts.
- **Look; don't guess.** You cannot judge a page from its source. Every command that edits ends with the critique loop (§Look). Fix what the frames show, then look again.
- **An upgrade keeps the truth and replaces the look.** Keep the product's facts, content, functions and anything the user pinned (brand colours, logo, fonts they chose). Replace the generic visual world.
- **Finish the job.** Fewer sections done completely beat many done halfway. Never leave a pinned stage empty, a counter at 0 or a heading mid-mask.

## Commands

The user may name a command and a target (`upgrade the landing page`, `signature the how-it-works section`, `polish pricing`). Narrow targets give better results.

| Command | What it does | Playbook |
| --- | --- | --- |
| `upgrade [target]` | The full pipeline: vibe-coded to premium, verified before and after | [commands/upgrade.md](commands/upgrade.md) |
| `audit [target]` | Record the page and report every AI tell and motion or finish defect, ranked. No edits | [commands/audit.md](commands/audit.md) |
| `direction` | Write `PREMIUM.md`: audience, facts, world, type, colour, imagery and motion personality | [commands/direction.md](commands/direction.md) |
| `motion [target]` | Choreograph the hero, reveals, hover and press, and transitions in one personality | [commands/motion.md](commands/motion.md) |
| `signature [target]` | Design and build one cinematic scroll scene, finished at every scroll position | [commands/signature.md](commands/signature.md) |
| `typeset [target]` | Replace default type with a system that has character, scale and finish | [commands/typeset.md](commands/typeset.md) |
| `palette [target]` | Colour, light and depth from the brief's world, with a chapter rhythm | [commands/palette.md](commands/palette.md) |
| `imagery [target]` | Rich visuals without stock: product renders, generative scenes, live product UI | [commands/imagery.md](commands/imagery.md) |
| `compose [target]` | Layout, hierarchy and rhythm: one dominant element per frame | [commands/compose.md](commands/compose.md) |
| `polish [target]` | The finish pass: everything `craft.png` outlines, every state, every edge | [commands/polish.md](commands/polish.md) |
| `harden [target]` | Phone layout, reduced motion, accessibility and scroll performance | [commands/harden.md](commands/harden.md) |

Routing:

- **"Make this premium", "less AI-looking", "redesign", or "upgrade"** on an existing page: run `upgrade`.
- **A new page or site:** run `direction`, then follow `upgrade` from its step 3. A new page is an upgrade from nothing.
- **A named command:** load only that playbook and follow it. If `PREMIUM.md` is missing and the command changes the look (`typeset`, `palette`, `imagery`, `signature`), run `direction` first. Keep it short when the target is narrow.
- **No clear command:** run `audit`, then offer the three commands that would raise the page most, each with one line on what it would change.
- **Animation questions about an existing design you must not restyle:** run `motion` alone, and keep the visual design exactly as it is.

## PREMIUM.md, the context file

`direction` writes `PREMIUM.md` at the project root. Every command reads it first when it exists. It holds the audience, the facts headlines come from, the three world artefacts, the concept, type, colour, imagery plan, motion personality and motion score. Update it when a decision changes; do not let the code drift from it.

## Two defaults to leave

**The AI template.** A condensed or soft serif (Instrument Serif, Fraunces) with one italic accent word; Inter, Geist or Manrope body; near-black with one amber, lime or acid accent, or warm paper; an eyebrow pill over a headline flush left, an object on the right; pill buttons; an indigo-to-purple gradient or glow cards; a marquee, bento grid, three pricing cards with a dark "Most popular"; identical icon cards; every section fading up the same way.

**The anti-template template.** Agents told to avoid the first default fall into a second one: a pale grey or cream ground, a giant plain grotesk or condensed caps headline, hairline rules everywhere, tiny monospace labels, "FIG. 1" annotations, spec tables standing in for visuals, and almost no imagery. It is different, and it is still generic and flat. Visitors read it as a document, not a brand.

Keep any trait only for a reason specific to this brief.

## What premium actually is

1. **A first viewport that is a scene, not a layout.** A dominant visual with depth (layers, light, texture, scale) and type set into it, not beside it.
2. **Material and light.** Gradients that model a light source, shadows with direction, surfaces that look like something (paper, glass, anodised metal, wool, water), grain used where the material has it.
3. **Type with character at extreme scale contrast.** One face with a voice, set tight and large, with real typographic detail; a quiet text face; numerals and small text treated with the same care.
4. **Motion with weight and intent.** Smooth, eased, overlapping choreography; scroll that drives scenes; images that clip-reveal with a counter-scale; depth from parallax layers; a CTA that responds to the pointer. Nothing linear except scrubs and loops.
5. **Rhythm.** Light and dark chapters, dense and open sections, loud and quiet. Neighbouring sections never share a layout.
6. **Detail nobody asked for.** Selection colour, focus rings in the brand voice, the cursor over draggable things, the first frame before fonts load, the 390px phone layout.

## The motion stack

Use what the project has, and never add a second animation library:

| The project | Use |
| --- | --- |
| React, Next.js, Vue or Svelte with Motion or GSAP | That library: [references/frameworks.md](references/frameworks.md) |
| Plain HTML, or a framework with no animation library, aiming for premium | GSAP + ScrollTrigger + SplitText, optionally Lenis: [references/motion-stack.md](references/motion-stack.md) |
| A small or simple page, or no dependencies allowed | The kit in `assets/` (§Building blocks) |

Timing tokens, whatever the stack:

| Use | Duration | Easing |
| --- | --- | --- |
| Hover, press, toggle | 140–220ms | `cubic-bezier(.22,1,.36,1)`; press scale .97 |
| Menus, tabs, small layout | 240–360ms | `cubic-bezier(.22,1,.36,1)` |
| Content reveal | 600–900ms | `cubic-bezier(.16,1,.3,1)` (expo-out) |
| Hero, signature moments | 900–1400ms | expo-out, overlapping pieces |
| On-screen move or morph | 400–700ms | `cubic-bezier(.65,0,.35,1)` |
| Exit | 60–70% of the entrance | ease-in |
| Scrub, ambient loop, marquee | scroll or long | `linear`, the only place it belongs |

[TASTE.md](TASTE.md) sets the motion personality, the signature scene and the motion score. Read it before `motion` and `signature`.

## Look: the critique loop

```bash
motion-debugger critique ./site                  # a folder with index.html, or an .html file
motion-debugger critique http://localhost:3000   # a running dev server
# not installed? → npx -y -p https://github.com/ShadowKingYT444/motion-debugger/releases/latest/download/motion-debugger.tgz motion-debugger critique …
```

The critic records the page in Chromium at desktop (1440×900) and phone (390×844): the entrance, a full scroll, hover, keyboard focus and reduced motion. It prints findings with fixes, compares with the previous run, and writes images. Open every image with your image viewer:

1. **`craft.png`**: finish defects measured in real frames, each outlined. Fix every one.
2. **`desktop-entrance.png`**: does the hero perform, headline first, settled by about 1.6s?
3. **`desktop-scroll.png` and `desktop-detail-*.png`**: answer for each frame, as a design director:
   1. Is there one dominant element, and is it a visual with depth, not just type?
   2. Is more than a third of it empty?
   3. Do edges align, or does something look nudged?
   4. Is anything mid-animation, faint, empty or showing 0?
   5. Cover the logo. Could this frame belong to either default above, or to any other site?
4. **`hover.png` and `mobile.png`**: hover shows in a still; the phone has its own layout.

Then write three lines: what still looks generated, what looks broken, and the single change that would raise the page most. Fix, and critique again. At least two passes; stop when `craft.png` is empty, no blocker or major finding remains, and every frame passes the five questions. The score is a lint, never the goal.

## Building blocks (the kit)

`assets/motion-kit.js` and `assets/motion-kit.css` give dependency-free primitives as data attributes. They work in plain HTML and, loaded once, in React or Next.js apps.

| Layer | Attributes |
| --- | --- |
| Entrances | `data-reveal`, `data-stagger`, `data-split` (keeps `<em>`, `<strong>`, `<br>`), `data-scramble`, `data-count`, `svg[data-draw]` |
| Scroll scenes | `data-progress` (sets `--p` for sticky storytelling), `data-hscroll` + `data-hscroll-track`, `data-stack`, `data-expand`, `data-exit`, `data-read`, `data-draw="scrub"`, `data-parallax` |
| Chapters | `data-bg` / `data-ink` on sections cross-fade the page colours; keep those sections' own backgrounds transparent |
| Pointer, nav, hover | `data-magnetic`, `data-spotlight`, `data-tilt`, `data-marquee`, `data-nav`, `.mk-wipe`, `.mk-link`, `.mk-button` |

Write a counter's final value in the HTML. Do not put `data-reveal` on `data-hscroll` slides or `data-stack` cards; the scene is their motion. [references/patterns.md](references/patterns.md) has complete code for bespoke moments.

## Done means

- [ ] `PREMIUM.md` exists and the page matches it
- [ ] The first viewport is a scene with a dominant visual; neither default from §Two defaults survives without a reason
- [ ] The hero is choreographed (headline first, settled by about 1.6s, nav visible at once) and leaves as you scroll
- [ ] One signature scroll scene is finished at every scroll position; at most two supporting scenes; everything else has a strong static layout with a reveal suited to its content
- [ ] Hover changes at least two properties on every control; focus is visible
- [ ] `craft.png` is empty; no blocker or major finding remains
- [ ] The phone layout is designed; reduced motion keeps every piece of content
- [ ] You looked at the final images after your last change
