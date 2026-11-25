---
name: taste
description: >-
  Design judgment for any web page or app screen. Use it whenever you design, redesign, restyle or
  polish a landing page, marketing or product site, portfolio, hero, one-pager, dashboard, settings or
  any other app screen, in any stack (HTML/CSS, React, Next.js, Vue, Svelte, Astro, Tailwind, Tauri),
  and whenever a page looks generic, templated or "AI-made". Principles, not a house style: the AI tells
  never to ship and why, how to present work like a top studio pitching a major client, when a device
  (mono, grids, numbers, labels, ASCII, dithering, imagery) earns its place, an optional ASCII/technical
  mode, when generated media beats code, and how to verify in a real browser at three widths. This is
  the entry point: it drives taste-skill's inspector and screenshots, and make-media for pictures.
---

# Taste

A generated page is the average of every page the model has seen. Nothing in it is wrong and nothing
in it was decided. The sites worth copying (Scale AI, Maritime, boat.dev) use the very devices
generators overuse (monospace captions, hairline grids, a floating pill nav, small uppercase labels)
and get away with it, because on those sites **each device carries information or comes from the
product's world**. So the line between slop and craft is *whether a device means something*, not
*which device it is*. This skill teaches the judgment; the `slop-guard` mod catches the mechanical
tells on every edit; neither forces a look.

## The run

1. **Find what is real.** The subject, the buyer, the one thing the page must get someone to do, the
   stack, any existing brand (colours, faces, logo), and the imagery that truly exists: the product's
   own UI, real photos, footage, a generator you can call (`make-media`), open collections
   (`node <taste-skill>/scripts/assets.mjs "<query>"`). Never plan around pictures you
   do not have. A vague brief: state your reading in one line and go; ask only when a fact blocks you.
2. **Inventory the subject:** eight to twelve things that belong to this product and no competitor
   (its name and what it means, its numbers, its constraint, its output, its artefacts: a command, a
   receipt, a timetable, a scan). The idea comes from this list.
3. **Write the idea in one sentence:** *On this page, [something from the inventory] becomes [one
   technique].* Maritime: the name becomes halftone dithering on every picture. boat: one boat = one VM,
   so the fleet *is* the chart. Scale: real footage and real scans with annotation keypoints, because
   labelling is the business. Put the nearest competitor in the sentence; if it still works, it is a
   category idea, not this product's.
4. **Write the argument before the markup:** one claim per section, each with its proof. Delete any
   section without a claim. This is how you escape hero, logos, three cards, testimonial, pricing, CTA.
5. **Write the copy deck in plain English** (`references/presenting.md` §2): what it is in under ten
   words, then the concrete nouns, then checkable specifics. No invented proof, ever.
6. **Decide the system once:** one ground, one ink, one accent (or one hue family); one sans, plus mono
   only where it means code or data; three to five type sizes far apart; one radius; generous section
   spacing; body text in full-contrast ink.
7. **Build it still, then add motion** that answers the story or the user. Respect reduced motion.
8. **Verify** (below), look at every screenshot, fix the top three problems, look again. Three rounds at
   most. Then **report like a studio** (`references/presenting.md` §4).

## Never use

These are the defaults that mean nothing. Each one is explained, with what to do instead, in
`references/never-use.md`. `slop-guard` blocks the four unmistakable ones at Stop (gradient text,
glows/rings/halos, the banned faces, placeholder or invented content) and warns on the rest.

1. **The template stack:** centred hero with two buttons, a logo row, three icon cards, testimonials,
   pricing, CTA, every section the same height. *It is the average, so it says nothing about you.*
2. **Purple/indigo gradients, gradient text, glows, halos, focus rings, glass, a soft shadow under every
   card.** *The first-wave generated look; recognised before a word is read.* Separate surfaces with a
   flat fill one shade off the ground; show focus by a fill change.
3. **The cream + terracotta "editorial" look and near-black + neon, as defaults.** *They were the cure
   for wave one and became wave three.*
4. **One medium radius (12-16 px) on everything; nested cards; coloured left-border cards.** *Stock
   component-library output.*
5. **Rounded friendly faces (Nunito, Quicksand, Comfortaa, Varela Round, Poppins, Figtree, DM Sans),
   default Inter/Roboto/system-ui; more than two faces; nine near-equal sizes.** One crisp sans with
   character (Instrument Sans, Geist, a Söhne-style grotesk) or the brand's own.
6. **A styled accent word in the headline** (italic, coloured, underlined), unless the brand does it.
7. **Hype and formula copy:** unlock, supercharge, seamless, elevate; "Welcome to X"; "not just X, it's
   Y"; tricolon slogans; a forest of em dashes. *Buyers skip words that could sell anything.*
8. **Invented proof:** fake logos, quotes, star rows, "Trusted by 10,000+ teams", vanity counters, fake
   YC badges. *Dishonest, and it reads as unfinished the moment anyone checks.*
9. **Fake product:** grey-bar dashboards, lorem numbers, stock "team" photos, AI images posing as the
   product or its users.
10. **Ornament with no job:** blobs, wavy dividers, crosshairs and crop marks, pulsing "live" dots,
    micro-meta strings (`A · B · C`), timestamps that say nothing, emoji as icons.
11. **Motion with no reason:** fade-up on every block, hover-lift on every card, bounce easing,
    `transition: all`, loops that mean nothing.
12. **Dashboard chrome on a landing page:** theme or motion toggles in the hero, status-pill legends,
    keyboard hints, internal "built / reviewed" tables, roadmap labels. Caveats live in docs and fine
    print.

## Devices: when one earns its place

Allowed when it **carries information or comes from the product's world**; cut it otherwise. Decide each
one by writing down what it carries. Full table and examples: `references/devices.md`.

| Device | Earns its place when | Costume when |
| --- | --- | --- |
| Monospace | the string is literally true: a command, its output, an ID, a price table of competitors (boat) | it is the "technical voice" for headings, labels or body |
| Hairlines, 1 px grids | they separate a real grid of comparable cells, a table, a list (Maritime's product grid) | they decorate: rules under every heading, boxes around single items |
| Index numbers | it is a real sequence or identifier (`Step 1 of 3` in a demo, `#8812` a load number) | 01 / 02 / 03 over sections that have no order |
| Small uppercase labels | each names a real category (Scale's `APPLICATIONS`, `PUBLIC SECTOR`), one or two per view | one sits above every heading |
| Floating or pill nav | it solves a real job (Maritime's bar becomes a pill only after scrolling, over content) | it is the default nav shape |
| Dark theme, one hue family | the subject lives there (night sea, terminal) | "premium" by reflex |
| ASCII, dither, pixel art, contour lines | it is the one technique, taken from the name or subject, and still carries data | it is a texture added for "tech" |
| Imagery | it shows the real product, real place or real work, or is source material code transforms | it stands in for content you do not have |
| Motion | it tells the story (scroll-scrubbed layers, a typing demo, a fleet that resizes) or answers the user | it decorates every block |

**Spend boldness in one place:** one memorable moment per page (the fleet, the 3D layers, the cost
calculator). Everything else stays quiet.

## Optional mode: ASCII / technical

Never the default. **Propose it** in one line when the product is for developers, agents or
infrastructure, and **wait for the user's yes**; never for consumer or regulated brands. Vocabulary:
halftone dithering (Maritime), pixel art (boat), true ASCII as text in `<pre>` with an `aria-label`,
wireframe or contour overlays and keypoints (Scale), terminal fragments, a tmux-style status bar, mono
for commands and captions. Rules:

- **One technique per site,** used everywhere (icons, hero, empty states).
- **Generated in code** (canvas, shader or precomputed text) from a real or generated source image, so it
  stays crisp, small, themeable and animatable. `make-media` makes source images and dithers them.
- **Body copy stays in the sans.** Every mono string is literally true: a real command, real output.
- **Reads on a phone; animation pauses under reduced motion; the look still carries information.**
- Put `{"mode":"technical"}` in the project's `.slop-guard.json` so slop-guard relaxes its label rule.

Detail and recipes: `references/devices.md` §3.

## Pictures: generate, find, draw, or code

- **Generate** (`make-media`): atmosphere and texture that do not exist yet (a sea at night, a material,
  a place); source images that code then dithers or ASCII-fies; a short ambient hero loop; a consistent
  illustration set; OG and social images.
- **Code wins** for anything with text, UI, diagrams, charts, icons, logos, pixel art, ASCII, dithering
  effects, wireframes. Real product screenshots and real UI fragments built as working components beat
  any generated product shot.
- **Never generate** customers, team photos, testimonials, the product's UI, or "real-world" footage
  presented as real. Scale's hero works *because* it is real.
- **List every generated asset in the build report:** file, model, prompt, cost, where it is used.

## Verify

Look in a real browser, never only at code. Run from the project root (`<taste-skill>` and
`<ui-ux-pro-max>` are where those skills are installed; each tool is used only if installed):

```bash
node <taste-skill>/scripts/inspect.mjs <url | path/to/index.html> --widths 1440,768,375   # measures + screenshots
node <taste-skill>/scripts/lint.mjs <source dir>                                           # static tells
```

- Read every screenshot it saves in `.taste-skill/inspect/`, at all three widths, after the last change.
  If a problem is visible in a screenshot it is real, whatever the code says.
- Fix every `FAIL`. Each `WARN` is wrong unless you can say in one sentence what the device carries
  (a mono caption that is a real command passes; a mono heading does not).
- App screens: add `--app`. Pages with scroll scenes: also `scripts/scenes.mjs`.
- UX floor (contrast, 44 px targets, forms, focus, CLS): query ui-ux-pro-max's checklist only, never
  its style or palette catalogue: `python <ui-ux-pro-max>/scripts/search.py "<outcome>" --domain ux`.
  Where it says "focus ring", show focus by a fill or colour change instead (the no-glow rule wins).
- A deeper second opinion before a PR, if gstack is installed: its `/design-review`.
- No taste-skill, Chrome or Node 22: take screenshots at 1440, 768 and 375 with whatever browser tool is
  available and say the inspector could not run. Never claim a check you did not run.

## Present like a studio

Restraint, real content, specific claims, one idea per section, and the craft details nobody asked for
(the empty state, the footer, install tabs per OS, fine print where caveats belong). The build report
leads with the idea sentence and the screenshots at three widths, then the system (ground, ink, accent,
face, sizes), what was cut and why, every generated or found asset, and what still falls short. Full
guidance and the report template: `references/presenting.md`.

## Other skills, and who decides what

Each applies only if installed; without them this skill still stands on its own.

- **taste** (this skill) decides: the idea, the argument, the system, which devices earn their place.
- **taste-skill** supplies tools: `inspect.mjs`, `lint.mjs`, `scenes.mjs`, `assets.mjs` (open
  collections). Its dealt directions (`draw.mjs`) are optional sparring, never the art direction.
- **make-media** makes images and short video (Gemini API with a spend cap, or the user's browser).
- **slop-guard** (mod) reports mechanical tells on each edit; a deliberate exception is
  `slop-ok: <reason>` on the line. A brand font goes in `.slop-guard.json` `"brandFonts"`.
- **ui-ux-pro-max:** UX and accessibility checks only.
- **frontend-design** agrees with this skill (structure encodes information); if both load, this one
  decides the house rules.

## Files

| File | Read it when |
| --- | --- |
| `references/never-use.md` | You want the why behind a tell, or what to do instead. |
| `references/devices.md` | Deciding on mono, grids, numbers, labels, nav, dark themes, ASCII/dither/pixel, imagery, motion; the technical mode recipes. |
| `references/presenting.md` | Writing the copy deck; the studio presentation; the build report template. |
| `references/studied-sites.md` | What Scale AI, Maritime and boat.dev each do, and the seven shared lessons. |
