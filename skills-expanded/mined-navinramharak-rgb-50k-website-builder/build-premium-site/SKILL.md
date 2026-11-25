---
name: build-premium-site
description: Build a premium, cinematic, scroll-animated website that looks like it cost $50,000 or more. Use when the user wants to build or redesign a website, landing page, or one-pager; asks for an "animated site", "scroll animations", "parallax", a "premium/expensive-looking site", a "$50k site", a "cinematic" or "scroll-stopping" site, or says their site "looks generic/cheap" and wants it elevated. Covers brand discovery, reference gathering, design tokens, choosing a signature scroll moment, the GSAP motion system, building section by section, and QA in the browser.
---

# Build a Premium, Cinematic, Scroll-Animated Site

Build sites that make someone stop scrolling and think "how did they build this." The bar is $50,000 and up: every section moves, the opener carries one move nobody expects, and the craft holds up when a stranger scrubs the page back and forth. Generic templates fail this bar. Follow the order below, because the order is the method.

Reach for the six references as needed (progressive disclosure). Do not paste their full contents into the build unless the task needs it:
- `references/reference-gathering.md`: how to collect five to eight references with assigned roles and turn them into a design evidence memo. The step that decides whether the craft has anything worth executing on.
- `references/motion-system.md`: copy-paste-ready GSAP + ScrollTrigger + SplitText + Lenis code, the fonts gate, reduced-motion guard, static fallback, and every core recipe.
- `references/signature-moves.md`: the library of opener moves. Pick exactly one.
- `references/premium-eye.md`: the five-tell pre-ship diagnostic, the anti-patterns list, and a plain-English glossary.
- `references/workflow.md`: the repeatable end-to-end process.
- `references/setup-and-deploy.md`: the beginner playbook for install, preview, and deploy. Point non-technical users here and to the README.

A working starter site lives in `assets/starter-template/`. It already carries the whole motion system for an example brand. Prefer re-branding it over building from a blank file, unless the user needs something the template cannot express.

## 1. Understand the brand first

Never open a code file before the brand is clear. Ask for, or confirm, these before building. Keep it to a few sharp questions, not an interrogation:

- The name, and in one sentence what they do.
- Who it is for, and what it refuses to be. Sharp exclusion makes a strong brand.
- The one feeling the site must create in the first five seconds (calm authority, raw energy, precision, warmth, awe). Everything downstream serves this feeling.
- The real assets they already have: logo or wordmark vector, product photos, product video, brand colors, brand fonts. Real footage of the actual product always beats generated footage of it.
- Where it will live and who ships it (them, a developer, a platform like Shopify).

Write this down as a short brand file before coding. `assets/starter-template/BRAND-TEMPLATE.md` is the structure to fill in: positioning, voice with banned words, the core headline, a three-line manifesto, the design tokens, wordmark, items, stats, and the chosen signature move. The headline and the copy matter more than any animation. A weak claim with great motion is still a weak site.

## 2. Gather references before designing anything

This is the step everyone skips and the one that separates a site that reads "AI made this" from one that reads "a human with taste made this." Do not design from a blank screen.

Follow `references/reference-gathering.md`. In short: write the direction as one specific sentence, collect five to eight references (no more) with an assigned role each (mood, brand system, hero hook, structure, micro-detail), and reject anything that fights the direction sentence. References that contradict each other produce a build that commits to nothing.

Then write the **design evidence memo**: one page naming the hierarchy, section sequence, type scale, space and density, imagery treatment, motion behavior, CTA placement, and three patterns to avoid. A folder of screenshots is not a deliverable; the memo is. It becomes the thing the finished site gets checked against at QA.

**Stop here and confirm the direction and the memo with the user before designing.**

## 3. Establish the design system as tokens

Design decisions carry more weight than any single animation. Lock these before building, and lock them as a named token set, not as ad-hoc values:

- **Type pairing.** One display face with real presence (heavy, condensed, or high-contrast) plus one clean grotesk for body, plus a monospace for labels and section numbers. The display type IS the layout. Proven pairs: Clash Display + Satoshi, Anton + Inter, Fraunces + Satoshi. Avoid default system stacks for display.
- **Palette.** One background, one type color, and ONE accent used sparingly (emphasis words, indices, hover states). A tight palette reads expensive; a rainbow reads cheap. A light site with dark full-bleed media bands often hits harder than all-dark, because the dark sections become title cards.
- **Space and rhythm.** Generous whitespace on one consistent spacing scale. Number every section in mono caps (for example `01 Philosophy` with a slash or middot separator). It reads editorial and expensive.

**Write the tokens into CSS custom properties before writing any section**, covering colors, spacing steps, radii, shadows, type sizes, and easings. From that point on, no arbitrary value may appear anywhere in the stylesheet. This single rule is what stops a page from looking assembled out of unrelated prompts, and it is checked at QA.

No generic templates, no stock hero layouts, no default component-library look. If it could be any brand, it is not done.

## 4. Choose exactly ONE signature scroll moment

Pick one move for the opener from `references/signature-moves.md` that fits this specific brand and feeling. One unexpected move, in the opener, executed flawlessly. Two moves compete for attention; zero moves is a brochure. Match the move to the brand: mask zoom-through for a strong wordmark, scroll-scrubbed video for a product that transforms, logo assembly for something that builds things, clip-path reveal for a mood shift, and so on. The hero-hook references from step 2 should make the choice obvious. Never reuse the same opener move across different sites, so no two builds feel the same.

## 5. Get the assets, and write the generation prompts yourself

Assets set the grading, which sets the palette, so gather them before scaffolding. Use the client's real media first; real footage of the actual product always beats anything generated.

When something has to be generated, **write the prompt for the user rather than asking them to write it.** They give a casual one-line brief ("a perfume bottle floating mid-air, soft blurred background") and the reply is a complete prompt covering subject, lighting direction and temperature, mood, composition and depth of field, aspect ratio, and style cues. Use the same prompt structure and grading across the whole set so it looks shot by one photographer. For motion, one motion only per prompt, five seconds, looped, camera move described in plain words; multiple motions in one prompt confuse the model.

Two practical notes worth passing on: in most generation tools the **aspect ratio and output resolution are panel settings, not prompt text**, so remind the user to set them there and bump resolution before generating (keep the ratio in the prompt too, it reinforces). And compress everything for web before it ships: video under about 5MB, a poster frame extracted, images at quality-80, and every asset localized rather than hotlinked to a generation CDN, because those links expire and break the live site silently.

## 6. Build on the motion system

Build every section on the system in `references/motion-system.md`. The non-optional spine:

- GSAP 3.13 + ScrollTrigger + SplitText + Lenis from CDN.
- The **fonts gate**: keep content hidden until `document.fonts.ready` (raced against a ~2500ms timeout), then reveal and boot all motion. SplitText measured against fallback fonts breaks.
- The **reduced-motion** path: `prefers-reduced-motion` shows everything settled, with zero motion.
- The **static fallback**: if the libraries fail to load, flag the page static and show everything readable. Nothing is ever permanently hidden.
- `fromTo` (never `to`) inside scrubbed timelines, with `invalidateOnRefresh: true`.
- Staggered reveals with heavy easing (power3/power4 out for entrances, power2.inOut for scrubs). Scrub 0.8 to 1, never instant. Luxury reads as weight.

Then give every section motion drawn from the recipes: staggered SplitText line reveals, section reveal-on-scroll, parallax, count-ups, a pinned scroll-scrubbed section, scroll-scrubbed video, a velocity-reactive marquee. Nothing sits static. Animate transform, opacity, and clip-path, not layout properties, so it holds 60fps.

**Solved problems get imported, not rebuilt.** Contact forms, footers, pricing tables, marquee strips, and logo walls have been polished by hundreds of designers already, and form validation, keyboard handling, and edge cases take days to get right from scratch. Pull them from a `~~component registry` and restyle them to the token set. Three rules keep this from wrecking coherence: an imported component never sets the visual language (it adopts the tokens or it does not ship), it is never used for the signature moment, and anything imported is treated as inspiration to remix rather than a locked template. If a component drags in a dependency, say why it earns its place before installing it.

## 7. Follow the end-to-end process

Run the full process in `references/workflow.md`: brand and the one feeling, references and the memo, assets, the signature move, build section by section, QA in the browser, a dedicated mobile pass, then deploy or hand off. Heavy building can be delegated to a build sub-agent and then reviewed against this bar.

## 8. Always QA in the browser

A site is not done until it has been watched moving in a real browser. Before calling anything finished, preview it (see `references/setup-and-deploy.md`) and check, at 1440px and at 390px, scrolling the full page down AND up several times:

- Every animation fires, lands cleanly, and reverses cleanly on up-scroll.
- Reduced-motion mode shows a complete, readable, motionless page.
- Mobile is handled: shorter pins, stacked fallbacks for horizontal galleries, no custom cursor on touch.
- No scroll trap (a pin the user cannot scroll past), and no horizontal overflow.
- No text clips, and no pop or jump at any crossfade or unpin. Type passes contrast against every frame of any video behind it, not just the first.
- **Token audit:** no color, shadow, radius, spacing value, or type size exists outside the token set defined in step 3.
- **The five tells** from `references/premium-eye.md`: space, one accent, one type personality, one loud thing per viewport, one ask. Then re-read the design evidence memo; if the page contradicts a pattern the memo said to follow, that is a bug, not a style choice.

When something feels average, the fix is never "more animations." It is one sharper signature move executed flawlessly, plus ruthless cleanup of anything that clips, pops, or stutters.

## 9. Point beginners to the playbook

If the user is not technical, point them to `references/setup-and-deploy.md` and the plugin README for how to install, what the project folder looks like, how to preview locally (a simple local server), where to put images and video and how to keep them small, and how to deploy free on Netlify or GitHub Pages. The glossary at the end of `references/premium-eye.md` translates every term in this plugin into plain words. Offer to walk them through it. The whole point is that anyone can ship this.

## Non-negotiables

- References and a design evidence memo before any design decision. Never design from a blank screen.
- Every value comes from the token set. No arbitrary colors, spacing, radii, shadows, or type sizes.
- Every section moves. Nothing sits static.
- Smooth heavy easing and staggered reveals everywhere.
- A fonts gate, so nothing ever flashes unstyled.
- Reduced-motion path and static fallback, always. The page must render even when motion is off or a CDN is down.
- Test every animation in a real browser before shipping.
- One signature move, in the opener, executed flawlessly, never repeated across sites.
- None of the anti-patterns in `references/premium-eye.md` ship.
- Make them say "how did they build this."
