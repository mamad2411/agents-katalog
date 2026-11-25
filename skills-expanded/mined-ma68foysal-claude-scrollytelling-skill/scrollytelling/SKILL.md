---
name: scrollytelling
description: Build award-level scrollytelling websites and product landing pages, where a hero product stays on screen through a pinned scroll "film", opens, twists, sprays or pours, travels into later sections and copy arrives beside it, using GSAP ScrollTrigger and Lenis smooth scrolling in one self-contained HTML file. Use this skill whenever someone asks for a scroll-animated, scroll-driven, Apple-style or Awwwards-style site, a product reveal on scroll, a "bottle/jar/box opens as you scroll" effect, a premium homepage or landing page with smooth scroll and motion, pinned or sticky storytelling sections, parallax product pages, or a beauty, fragrance, drink, watch or gadget homepage that should feel high-end, even if they never say "scrollytelling".
---

# Scrollytelling

Build a homepage that tells one product's story as you scroll. The page pins a stage, and scrolling plays a film: the product sits in a hero, then opens, gives something (a drop, a mist, a swirl of cream), travels to the side while copy arrives next to it, crosses to the other side for the details, and finally becomes part of the closing headline. Around that spine sit calmer sections: ingredients, ritual, collection, footer.

The output is one HTML file the user can open locally (plus an `assets/` folder when you cut products out of photos). It uses GSAP 3 + ScrollTrigger and Lenis from public CDNs, so there is no build step.

## Why this works (keep it in mind while designing)

Great scroll sites are not "sections that fade in". They have three things:

1. **One subject the camera follows.** The same product element is visible from the hero to the last scene. It changes state (closed, opening, open, giving, packaged) and position (centre, left, right, into a word). Moving one element between scenes is what makes the page feel like a single shot rather than a stack of blocks.
2. **Motion that comes from what the product is.** Soda gets bubbles, perfume gets mist, a botanical cream gets drifting pollen and leaf shadows, a watch gets ticking callouts. Pick one ambient motif and run it through every section. That is the difference between "animated" and "art-directed".
3. **Copy that lands next to the product at the right moment.** Each scene has one job: one headline, one or two sentences, maybe one action. Panels alternate sides so the product keeps moving.

## Workflow

### 1. Turn the brief into a concept (a few minutes, not a questionnaire)

If the user names a product or brand, use it. If not, propose one: a fictional brand, one hero product, its audience and its ambient motif. Default to a fictional brand. Never put a real company's name, logo or packaging on the page unless the user says it is theirs, because the result would read as an impersonation.

Settle these before writing code, and tell the user in a few lines:

- Product and fictional brand name
- Palette (4 to 6 named colours) and whether the page is light, dark or both. Users who say "natural", "soft" or "clean" usually mean light only.
- Two typefaces (a characterful display face and a quiet body face) from Google Fonts
- The ambient motif
- The scene list (next step)

Read `references/art-direction.md` for palettes, type pairings and the clichés to avoid.

### 2. Write the scene list before any code

Write a short storyboard. For each scene: product state, product position, what moves, the copy, any interaction. A typical film is 5 to 7 scenes. For example:

| # | Scene | Product | Copy | Notes |
|---|---|---|---|---|
| 1 | Hero | Closed, centre, on a pedestal | Big headline, one line of context | Intro on load, idle float |
| 2 | Open | Cap twists, unscrews, lifts away | "Twist to open" chip | Highlight sweeps the cap |
| 3 | Give | A drop falls / mist sprays / cream shows | Short caption | Particle burst, ripple |
| 4 | Story | Moves left, slight tilt | Panel right: headline, 2 lines, price, Add to bag | Background tint shifts |
| 5 | Details | Crosses right | Panel left: 3 facts with callout lines to the product | Numbers count up |
| 6 | Close | Repacked, shrinks into a word | Headline with image slots | Shared-element handoff |

`references/scene-playbook.md` has a catalogue of proven scenes (pinned film, macro callouts, spray, carton boxing, image-in-text headline, horizontal garden walk, stacking cards, mask reveals, velocity marquee, and the product dissolving into its ingredients) with working code. Pick from it rather than inventing everything.

### 3. Decide how the product is rendered

This decision shapes everything, so make it consciously:

| Approach | Use when | Strength | Watch out |
|---|---|---|---|
| **Drawn in code** (inline SVG built from parts) | The product must open, twist, spray, change colour, or be boxed | Every part moves independently; colour variants are free | Must be drawn with care (gradients, highlights, shadows) or it looks flat |
| **Photo cut-outs** (transparent WebP parts) | The user wants it to look real | Photographic realism | You need the parts as separate images, shot from the same angle |
| **Hybrid** | Real photo jar, but it must start closed | Real body, drawn lid that sits exactly on the measured rim, then hands off to the real lid photo as it rises | Match the drawn part's shading to the photo |

Secondary things (ingredients, lifestyle, collection cards, images inside words) should be **real photos**, not illustrations. Users consistently find drawn secondary objects cheapen the page.

`references/product-assets.md` explains how to draw a convincing product in SVG, how to source unbranded photos, and how to cut parts out of a photo with `scripts/cutout.py`.

### 4. Build from the starter

Copy `assets/starter.html` and replace its placeholders. It already contains the parts that are easy to get subtly wrong: Lenis wired to ScrollTrigger, the pinned stage with a product that opens and travels between two panels, an ambient particle canvas, a hide-on-scroll header, a slide-out bag with a free-shipping bar, a reduced-motion fallback, and theme tokens.

Keep the file structured so each scene maps cleanly to a future Shopify section (see `references/shopify-handoff.md` if the user mentions Shopify or a theme).

### 5. Verify like a director, not like a linter

Serve the folder locally (for example `python -m http.server 5173`) and open it in a browser you can control. Then:

- Jump the pinned timeline to each scene and look at it. A helper for the browser console is in `references/motion-engineering.md` ("Jump to a scene").
- Check a phone viewport (375 x 812) and a desktop one (around 1366 x 800). Phone needs its own choreography, not a squeezed desktop.
- If the page supports dark mode, check both themes.
- In emulated viewports, screenshots can lag one frame behind a scroll jump. Take a second screenshot, or measure with `getBoundingClientRect()` when you need certainty (for example "is the cap centred on the neck?").
- Scroll forwards and backwards through each transition. Bugs often only appear on the way back.

### 6. Deliver

Tell the user where the file is, how to run it, what each scene does, and what is honestly not done (for example "the lid can't look fully closed from these photos", or "checkout isn't connected"). Mention what a real product shoot would need if photos limited you.

## Engineering rules that prevent the usual bugs

These all come from real failures. The reasons matter more than the rules, so read `references/motion-engineering.md` for code.

- **Use `fromTo`, not `from`, inside scrubbed timelines with `invalidateOnRefresh: true`.** On refresh the timeline is reset and re-recorded; a `from()` then records its own start state as the end state and the element stays hidden for good.
- **Call `lenis.resize()` whenever ScrollTrigger refreshes.** Pinning adds page height after Lenis has measured it, and Lenis otherwise stops the user scrolling halfway down the page.
- **Give moving parts two nested wrappers: one that translates, one that rotates.** Tweening x, y and rotation on the same SVG element (especially with `svgOrigin`) makes the part land off-centre on the way back.
- **Add `immediateRender: false` to later `fromTo` tweens on an element that an earlier tween already animates**, otherwise the later start state is applied at page load.
- **Hide anything that rises "out of the floor" with a static clip-path on an outer group**, so it does not show through transparent glass while it travels.
- **Write every scene's positions as functions** (`x: () => mobile() ? 0 : -innerWidth * .22`) so a resize or orientation change recomputes them.
- **Set `history.scrollRestoration = 'manual'`** and scroll to the top on load so the intro always plays from the start.
- **Respect `prefers-reduced-motion`.** Skip Lenis and pins, and lay the panels out as normal content.
- **Measure geometry instead of guessing** whenever an element must land in a specific place, such as a box going into a gap in a headline. Use `offsetLeft`/`offsetTop` chains, because ancestors with transforms distort `getBoundingClientRect()` during animation.

## Content rules

- Write real, specific copy in the brand's voice: ingredients with percentages, sizes in ml, times ("sinks in within 40 seconds"). Never lorem ipsum.
- Buttons say what they do ("Add to bag", "Check out"). Forms are handled in script; never post them anywhere.
- If you invent reviews for a concept, label them as sample content, and add a footer line saying the brand is fictional and where photos came from.
- Credit Unsplash (or the source) in the footer.

## Files in this skill

- `assets/starter.html`: the template to copy. Start here.
- `assets/particle-morph.js`: the product-dissolves-into-ingredients engine (scene 16), plus ambient dust
- `references/scene-playbook.md`: scene catalogue with code
- `references/motion-engineering.md`: GSAP and Lenis setup, timeline patterns, debugging helpers
- `references/product-assets.md`: drawing products in SVG, photo sourcing, cut-outs, hybrid lids
- `references/art-direction.md`: concepts, palettes, typography, copy, what to avoid
- `references/shopify-handoff.md`: turning the page into Shopify sections and blocks
- `scripts/cutout.py`: cut product parts out of a photo into transparent WebP
- `scripts/contact_sheet.py`: build a contact sheet from Unsplash photo IDs to pick images quickly
