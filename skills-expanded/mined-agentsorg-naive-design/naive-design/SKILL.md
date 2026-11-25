---
name: naive-design
description: "Load when building a warm, hand-drawn 'naive design' aesthetic — childlike doodles, crayon/marker/risograph texture, lowercase friendly type, soft mascots, intentional imperfection — for branding, posters, packaging, merch, social, landing pages, onboarding, empty/404 states; when generating naive-style brand assets with image models; or when deciding whether messy-premium imperfection fits a surface (and where it must NOT go). The disciplined complement to the design-engineering skill. Encodes Amir Mušić's 2026 naive-design thread."
license: MIT
compatibility: Agent-agnostic. Pairs with the design-engineering skill (AgentsORG/design-engineering) and Google Labs design.md. Reads in any agent that loads SKILL.md (Claude Code, Cursor, Codex, Windsurf, Aider, Cline, Gemini).
metadata:
  author: HKTITAN
  version: "0.1.0"
  graph: false
  source: "Amir Mušić (@AmirMushich) — 'The megatrend of 2026: Naive design' thread, 2026-05-28"
  complements: "design-engineering (AgentsORG/design-engineering)"
---

# naive-design

> Warm, intentional imperfection. "In 2026, messy is the new premium." This skill is the disciplined complement to **design-engineering** — where that skill says *most polish is deletion*, this one says *some imperfection is addition* — but only when it is **art-directed, not careless**.

Naive design is a professional designer drawing *as if* they were a child: imperfect doodles, soft mascots, crayon and marker texture, lowercase friendly type, generous negative space. It reads as innocent, playful, warm, and emotionally safe — a cultural antidote to the cold, polished, AI-perfect feeds of 2026. Imperfect visuals convert better and feel more human *because* everything around them is sterile.

The whole skill rests on one rule. Read it before anything else.

## The one rule — intentional, not broken

> "Childlike but **professionally art-directed**." · "Intentionally imperfect but **well-composed**." · Avoid "**random childish chaos**." — all three are Amir Mušić's own words.

Naive is a costume that professionalism wears. The grid is still there. The negative space is deliberate. The palette is *limited*. The imperfection is applied at chosen decorative moments — a wobbled line, a dot-eyed mascot, a marker underline — never to the structure underneath.

The test (borrowed from design-engineering's `visual-imperfection`): **would this survive a senior designer? If they'd flag it as a bug, it's a bug. If they'd nod, it's intentional.** "Consistent in its inconsistency."

Three failure directions, all fatal:

- **Chaos** — random rotation, no grid, every element fighting. That's not naive, it's unfinished.
- **Fake-handmade** — a perfectly smooth vector "doodle" with no pressure variation or texture. Reads as a machine pretending. Naive needs real grain, real wobble, real ink.
- **Lazy shorthand** — Comic Sans, the default squiggle pack, three clip-art stars. The naive equivalent of a purple gradient. See *naive-design tells* below.

## When to use — and the hard boundary

**Use it on the brand surface, where warmth earns its bandwidth:**

- Branding, logos, brand kits, packaging, merch, posters, stickers.
- Marketing / landing pages, hero sections, about pages, campaign social tiles.
- Onboarding moments, empty states, 404s, illustrations, changelog headers, swag.
- Whole products whose *identity is* warmth (a kids' app, a community tool, a journaling app).

**Do NOT use it where users must parse, trust, or move fast** — this is the boundary that keeps the skill credible:

- Data-heavy product UI: dashboards, tables, settings, analytics. (design-engineering: `data-is-content`, `states-are-the-work`.)
- Forms, financial, medical, legal, security surfaces — anywhere a wobble reads as "is this broken?"
- Dense, repeated UI patterns. Inside the product, consistency wins; imperfection slows scanning.

The move on a real app: **disciplined product UI, naive brand layer.** Doodles on the marketing site and the onboarding; a clean, fast, monochrome app behind the login. Gate every naive decision through design-engineering's `marketing-vs-product-ui`.

## The aesthetic vocabulary

The visual language, distilled from all five prompts in the source thread. This is the palette of moves to draw from — pick a few per piece, never all at once.

**Forms** — imperfect doodles · soft rounded shapes · simple mascots with tiny black-dot faces · awkward-but-charming composition · soft arch shapes · flower-like doodles · funny-face symbols · oversized accessories · uneven limbs · wobbly bullets · slightly off-grid icons.

**Texture** — this is non-negotiable; flat = cold. Crayon and marker · paper grain · risograph print grain · uneven ink edges · "scanned handmade" feel · crayon-wax · imperfect line pressure · matte paper · slightly imperfect print registration · sticker shadows.

**Palette** — **limited** (the thread repeats this). Warm paper grounds (cream, off-white) carry bright, friendly marks. Common sets: cream + black ink + one crayon-red; or pastel papers (bubblegum pink, mustard, teal, deep purple) with red/white line work. Bright but *few*. A rainbow of saturated hues is a tell, not naivety. (Shares discipline with design-engineering's `color-monochromatic`: one tonal language, accents earn their place.)

**Typography** — bold **lowercase** sans-serif for the structured layer + a hand-drawn **marker** layer for the scribble, and the *contrast between them* is the joke. Small handwritten notes, imperfect and awkward. Friendly, minimal, generous tracking on display. Mixing luxury-editorial type with childish marker is high-concept. Never Inter/SF — those are the AI-era tells (design-engineering: `typography-humanity`).

**Layout & composition** — clean editorial grid · *lots* of negative space · generous spacing · circled notes · hand-drawn dividers and underlines · sticker shadows. The composition is calm and confident; the marks inside it are playful. "Serious brand system meets gentle doodle playground" is the north star.

## Building it in code

The thread is image-generation; this section is the value-add — how to make the same aesthetic in the browser, so it complements design-engineering on its home turf (HTML/CSS/SVG). Keep every recipe subtle and gated.

**Paper & risograph grain** — felt, not seen. SVG fractal noise over the page at low opacity:

```html
<svg aria-hidden="true" class="grain" width="0" height="0">
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
</svg>
<div class="grain-layer"></div>
```

```css
.grain-layer{ position:fixed; inset:0; pointer-events:none; opacity:.06; mix-blend-mode:multiply;
  background:#fff; filter:url(#grain); }   /* opacity .04–.08. If a user notices it, it's too strong. */
```

**Wobble / hand-drawn edges** — displace straight geometry so borders, dividers, and underlines look drawn. Apply `filter:url(#wobble)` to any boxy element:

```html
<filter id="wobble"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="2" result="n" seed="3"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="6"/></filter>
```

`scale` 4–8 = subtle hand wobble; higher gets sloppy. For a *living* line, alternate two `seed` values on a slow loop — but gate it (see motion).

**Marker / crayon strokes & doodles** — don't hand-roll vectors that look machine-made; reach for tools built for it:

- [rough.js](https://roughjs.com) — renders sketchy, hand-drawn SVG/Canvas shapes, lines, and fills from real geometry. The cleanest way to get authentic wobble without a displacement filter.
- [Open Doodles](https://www.opendoodles.com) (Pablo Stanley) — free hand-drawn illustration set.
- DiceBear `croodles`, `open-peeps`, `notionists` — procedural hand-drawn mascots/avatars with dot faces (design-engineering: `avatar-systems` already references the DiceBear v9 catalog).
- Layer 2–3 semi-transparent strokes for crayon-wax build-up; vary `stroke-width` slightly along a path for pressure.

**Sticker shadow + slight rotation** — the warm cousin of design-engineering's `shadows-whisper` (layered, low-opacity), tinted warm and given a tiny lift + tilt:

```css
.sticker{ transform: rotate(-2.5deg);
  box-shadow: 0 1px 0 rgba(33,28,24,.05), 0 10px 18px -10px rgba(33,28,24,.20); }
```

**Print misregistration** — riso/offset-ink charm, 1–2px max:

```css
.riso-offset{ text-shadow: 1.5px 1px 0 var(--crayon-red); }  /* or duplicate the mark, offset, in a 2nd ink */
```

**Off-grid jitter** — controlled, not random. Rotate decorative items on a *fixed* small set, not `Math.random()`:

```css
.doodle:nth-child(3n)  { transform: rotate(-3deg); }
.doodle:nth-child(3n+1){ transform: rotate(2deg); }   /* consistent in its inconsistency */
```

**Type pairing** — a warm grotesque, lowercased + tight, for the structured layer; a designed-casual marker for the hand layer:

- Display/body: **Bricolage Grotesque** (warm, slightly quirky; free on Google Fonts) — set lowercase, tracking tight on big sizes.
- Marker/hand: **Shantell Sans** (Shantell Martin × Google; variable, with an `INFM` "informal" axis you can dial up for scribble). It *is* "professionally art-directed childlike handwriting." Both swappable; the point is **not Inter**.

**Motion** — naive motion is gentle and drawn-on, never a bouncy spring on everything. A path that draws itself in fits the handmade story:

```css
@media (prefers-reduced-motion: no-preference){
  .draw path{ stroke-dasharray:1; stroke-dashoffset:1; animation:draw .9s ease forwards; } /* path has pathLength="1" */
  @keyframes draw{ to{ stroke-dashoffset:0 } }
}
```

Defer all timing/easing to design-engineering: `easing-curves`, `duration-table`, `never-scale-from-zero` (don't pop doodles in from scale 0), and `prefers-reduced-motion` (always provide the static state — a finished drawing, not a frozen half-drawn one). A wobble loop or living-line that ignores reduced-motion is an accessibility miss, not delight. Run it past `delight-impact-curve`: does this doodle earn its weight, or is it noise?

## Naive-design tells (avoid)

Naive design is **not** an excuse to reintroduce the slop that design-engineering's `ai-default-tells` and `content-authenticity` warn against. It has its *own* tells:

| Tell | Why it fails | Do instead |
|---|---|---|
| Comic Sans / a "kiddy" system font | Lazy shorthand for childlike; reads as a joke, not craft | A crafted casual font (Shantell Sans) or real hand-lettering |
| Perfect-vector "doodle", zero texture | Fake-handmade; the machine showing through | Real grain + wobble + pressure variation; rough.js |
| The default squiggle / star / blob pack everyone uses | The purple-gradient of naive — instantly generic | Draw your own marks, or commission them |
| Rainbow of saturated colors | Mistakes loud for warm; ignores "limited palette" | 1 paper ground + 1–3 bright marks |
| Grain/texture cranked up so it's *seen* | Costume over content | Opacity .04–.08; felt, not seen |
| Random rotation & placement ("chaos") | Unfinished, not innocent | A fixed jitter set on a real grid |
| Doodles on a data table / form / dashboard | Wrong surface; reads as broken/untrustworthy | Keep product UI disciplined; naive on the brand layer |
| Lorem ipsum + "John Doe" under the cute layer | Warmth can't paper over inauthentic content | Real, specific copy (design-engineering: `content-authenticity`) |

The frame, adapted from design-engineering: *could this naive piece have been generated in 30 seconds from the default doodle pack?* If yes, it isn't naive — it's generic-with-crayon.

## Generating naive assets with image models

The source thread is, at heart, a set of reusable image-generation prompts. The full cleaned, parameterized library lives in [`prompts/prompt-library.md`](../../prompts/prompt-library.md) (five ready templates: brand piece, fashion magazine cover, business-card set, square poster, and a full 16:9 mini brand-kit board). The reusable **anatomy** every strong naive prompt follows:

1. **Artifact + subject** — "Create a [poster / brand board / business cards] for [BRAND]."
2. **Style declaration** — "contemporary naive doodle style; childlike but professionally designed."
3. **Concrete marks** — name the doodles: mascots with dot faces, marker lines, arches, flowers, funny-face symbols.
4. **Layout** — clean editorial, lots of negative space, bold lowercase type, intentional spacing.
5. **Palette** — *limited* and named (e.g. "cream, black, crayon-red, soft green").
6. **Texture** — paper grain, riso, crayon/marker, uneven ink, imperfect registration, "scanned handmade."
7. **Emotional target** — innocent, playful, warm, anti-perfectionist, emotionally safe.
8. **The avoid block** — realism, polished vector, 3D, glossy, complex shading, corporate stock, luxury minimalism, gradients, metallic, anime, horror, clutter, **and "random childish chaos."**
9. *(For a brand remix)* **"Decode the brand first"** — preserve its real logo/colors/codes, then remix through the handmade system; list explicit modules (hero, colors, assets, ui, stickers, card, social tile, footer microcopy).

That avoid-block is the same discipline as the *tells* section: you are steering the model away from both cold perfection **and** formless mess.

## Pairing with design-engineering

This skill is self-contained, but it is *designed to ride alongside* design-engineering. When both are available, load these nodes together (names are that skill's basenames):

| Doing this in naive-design | Also load from design-engineering |
|---|---|
| Deciding *whether* to go naive on a surface | `marketing-vs-product-ui`, `data-is-content`, `states-are-the-work` |
| Imperfection technique (the inverse/extension of one node) | `visual-imperfection` — naive makes imperfection the *whole system*, not a marketing-only accent |
| Picking the limited palette | `color-monochromatic`, `contrast-and-color-scheme` |
| Type pairing & avoiding font tells | `typography-humanity`, `line-length-tracking` |
| Sticker shadows | `shadows-whisper` |
| Any motion (draw-on, wobble, living line) | `easing-curves`, `duration-table`, `never-scale-from-zero`, `prefers-reduced-motion` |
| Mascots / dot-face avatars | `avatar-systems` (DiceBear) |
| Does this doodle earn its place? | `delight-impact-curve` |
| Not reintroducing slop under "cute" | `ai-default-tells`, `content-authenticity` |
| Consuming the token file | `using-design-md` (it reads the `DESIGN.md` shipped here) |

If you only carry the prose pointer: **naive design is the deliberate inverse of `visual-imperfection`** — that node treats imperfection as a cautious marketing-only accent; this skill treats it as the entire visual system, and inherits the same "would a senior designer nod?" gate.

## Tokens — see DESIGN.md

A reference naive-aesthetic token file ships at [`DESIGN.md`](../../DESIGN.md) (Google Labs design.md format — `version: alpha`). It encodes the warm paper grounds, crayon/marker accents, the lowercase-grotesque + marker type pairing, soft radii, and generous spacing as machine-readable tokens. Validate with `npx -y @google/design.md lint DESIGN.md`. design-engineering's `using-design-md` workflow already knows how to consume it; treat its tokens as normative, its prose as context.

## Make it yours

Edit this file to fit your taste — it is a starter, not scripture. Swap the fonts, retune the palette, add your own marks. Append a one-liner to **Gotchas** every time the agent gets a naive detail wrong; that failure log is the highest-signal part of the skill over time (the same flywheel design-engineering uses).

## Gotchas

Append-only. `- [YYYY-MM-DD] one-line failure → fix.`

- [2026-05-29] Treated "naive" as license to drop the grid → random rotation read as broken. Fix: fixed jitter set on a real grid; "consistent in its inconsistency."
- [2026-05-29] Used a perfect-vector doodle with no texture → looked machine-faked. Fix: add grain + wobble + pressure variation (rough.js / displacement filter).
- [2026-05-29] Reached for Comic Sans to signal childlike → cheap. Fix: Shantell Sans or real hand-lettering.
- [2026-05-29] Put doodles on a settings table → felt untrustworthy. Fix: naive on the brand layer; product UI stays disciplined (`marketing-vs-product-ui`).
- [2026-05-29] Cranked grain opacity until it was visibly noisy → costume over content. Fix: opacity .04–.08, felt not seen.
- [2026-05-29] Looping wobble animation ignored `prefers-reduced-motion` → a11y miss. Fix: gate motion; ship the finished static drawing.

## Sources

- **Amir Mušić (@AmirMushich)** — ["The megatrend of 2026: Naive design"](https://x.com/AmirMushich/status/2060083688730493348), 2026-05-28. The thesis, the aesthetic vocabulary, and the five generation prompts. The method is his; this skill encodes and extends it to code.
- **design-engineering** ([AgentsORG/design-engineering](https://github.com/AgentsORG/design-engineering)) — the skill this one complements; all `node-name` references above are its basenames. Especially `visual-imperfection`, `marketing-vs-product-ui`, `color-monochromatic`, `typography-humanity`, `ai-default-tells`.
- **Google Labs design.md** ([google-labs-code/design.md](https://github.com/google-labs-code/design.md)) — the token format used by the shipped `DESIGN.md`.
- **Tools** — [rough.js](https://roughjs.com), [Open Doodles](https://www.opendoodles.com), [DiceBear](https://www.dicebear.com) (croodles / open-peeps / notionists), [Bricolage Grotesque](https://fonts.google.com/specimen/Bricolage+Grotesque), [Shantell Sans](https://fonts.google.com/specimen/Shantell+Sans).
