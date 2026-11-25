---
name: chanmeng-svg-product-card
description: >-
  Make an animated SVG product card that plays inside a GitHub README: one
  self-contained file, usually 1300 × 360, whose stage shows the product's real
  interface redrawn in vectors and running, with outlined text, CSS keyframes on one
  loop and a complete still frame for reduced motion. Use whenever someone wants an
  animated project card, a README demo that is not a GIF, a product showcase SVG, an
  animated profile card, or "show what my project does in the README", and to fix or
  audit an animated SVG that breaks on GitHub (blank fonts, lost animation, broken in
  an img tag). Also for: 项目宣传动图, SVG 动图, 产品卡片, README 动画卡片, 动态项目卡片,
  GitHub 主页项目展示动图. Not for a screen recording, a video or a promo film, for
  light and dark README image variants, or for a mascot, loader or logo animation
  that shows no product.
---

# SVG product card

A card earns its place when the motion carries information: code is typed and a plan
compiles, an agent drafts and fixes in passes, a phone scrolls and a log reacts. An
animated name with drifting confetti is a business card. So the work is mostly
reading the product and finding what it does that can be shown happening; the SVG
mechanics are solved by the kit.

`<skill-dir>` below is the folder holding this file.

## Before drawing

Read `references/field-guide.md` sections 1 to 5 now, and the technique you need from
section 6 when you reach it. Read `references/kit-api.md` when you write the builder.

Then, from the product's own repository and site:

1. **Tokens**: its CSS variables or token file. Copy hex values; a screenshot lies.
2. **Fonts**: its font loader. Confirm with `getComputedStyle` on the live page when
   it asks for system fonts.
3. **Wordmark**: the real logo file, used as it is. Typing the name in a similar font
   is not the wordmark. If only a symbol exists, use it, set the name in the product's
   own display font beside it, and say so at handover.
4. **Brand and claim rules**: what is forbidden, what a figure may be said about.
5. **Sources of copy**: its site's feature list, its interface strings, its film.
   Every word on the card comes from something already reviewed.

If the product is not in reach, ask for the repository or the live URL before drawing:
a card guessed from a description cannot be true to the product.

Now decide two things and state them in one line each before writing code:

- **The stage**: what does this product do that can be shown happening?
- **The still frame**: the one scene you would keep if the card could not move.

## Build

```bash
node <skill-dir>/scripts/init-kit.mjs --dest=scripts/cards --id=<card-id>
npm i -D opentype.js playwright-core      # the command prints what is missing
```

The kit is copied into the project on purpose: a card is rebuilt long after this skill
was used, by someone who may not have it. Pick a `--dest` that suits the project.

**Fonts come first:** the builder will not run until they exist. It needs the keys
`display`, `sans`, `sansBold` and `mono` for the panel; add more for the stage.

- Use **static** instances. A variable font gives its default weight, which may be
  Light.
- For an open font with no static file, `npm i -D @fontsource/<family>` ships one file
  per weight in its `files/` folder. Take the `.woff`; the kit cannot read `.woff2`.
- A product that asks for a system font, which you may not redistribute: use the
  closest open font and name the substitution at handover.

Once the fonts are in, `<dest>/<card-id>.mjs` runs as a card that passes the gates.
Keep it passing as you replace it, in this order: `THEME`, `COPY`, then the stage.

- **Nothing on the stage is drawn from imagination.** Compile it, quote it, ask it,
  follow its script, or redraw it from its components (field guide section 4). Make
  the builder read the real source and throw when it stops matching: that is what
  stops a card from going stale. For a TypeScript source, bundle it with esbuild and
  import the result, so the builder calls the product's real function.
- **A build must not touch anything live.** Calling a production API can change its
  data (a visitor counter ticks on every fetch) and makes the art differ per run.
  Fetch once, keep the file in `<dest>/assets/`, and refetch only behind a flag. Ask
  before the first fetch if the call has an effect.
- **The stage is the product's interface, not a slide about it.** No paragraph, no
  sentence beside a scene, no closing frame of figures, no role or client line. The
  page around the card says those. `panel()` refuses a fifth panel item or a sub-line
  that does not fit, because this is the mistake that cost a full redraw of twelve
  cards.
- **Motion budget:** two or three things moving at once, 4 to 6 seconds a scene,
  entrances of 0.2 to 0.45 s, nothing bounces. Loop length follows content.
- **Weight:** aim under 300 KB. Field guide section 8 has what things cost.

## Verify

Run these in order. A card is not done because one frame looks right.

```bash
node <dest>/<card-id>.mjs
node <dest>/lib/check-card.mjs <card>.svg
node <dest>/lib/capture-frames.mjs <card>.svg --at=<one time inside each scene, and the end of the last> --out=<scratch dir>
```

`check-card` errors are real failures. `capture-frames` exits non-zero when the image
does not decode, or the reduced-motion picture still moves. Its timed frames are exact,
so a tight transition can be checked to the tenth of a second. Keep the last time
before the loop's dip (`tl.dip()`, the final 0.4 s), or you capture the fade.

**Then look at the captures.** Open every one and check: text clipped by a window or
overlapping a neighbour; a scene that reads as dead; the panel and stage in both the
light and dark files; the reduced-motion still being the frame you chose. Nothing
else catches these. If you could not view the images, say so; do not report the card
as verified.

When the card is in a pushed README, open the live page and confirm the image decoded
and is playing. Only the real host proves it.

## Hand over

- The `.svg`, the builder, and the `<img>` line, with the `alt` set to the SVG's
  `<title>`: one sentence saying what happens on the stage, the part a screen reader
  cannot get from the outlines.

  ```html
  <img src="<path>/<card-id>.svg" width="100%" alt="<the SVG's title>">
  ```

- Each input the builder reads from outside the project, and what happens when it is
  missing (field guide section 9).
- Anything you could not source or verify, plainly. A chip invented from memory has
  shipped before; say which element has no evidence rather than keeping it quiet.

## When something breaks

| Symptom | Cause |
|---|---|
| Blank or wrong text on GitHub | Live `<text>`. Use `glyphs.text`, or `outlineTextElements` for embedded SVG |
| Static on GitHub, moves locally | Script or SMIL. Everything moves through CSS keyframes |
| Blank first seconds | A positive delay. Use `tl.shift(start)`, which never waits |
| Typing cover shows over a neighbour | Clip the row to its container |
| Reduced-motion still is empty | Elements authored in their start state. Author the finished frame |
| Build throws `no glyph` | Pass a `fallback` font with the same units-per-em |

Field guide section 11 lists the mistakes that have already been made once.
