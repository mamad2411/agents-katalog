---
name: unflat
description: Use when a website or landing page looks flat - one background color across the whole page, every section on the same plane, nothing reads as a separate block while scrolling (worst on a phone). Also use when asked to frame or ground a site's sections, give a page depth, texture or atmosphere, make a dark or light background less boring, or to "unflat" a page. For marketing and content pages built with plain CSS, Tailwind, CSS modules or CSS-in-JS; not for app dashboards.
---

# unflat

One reversible CSS block turns a single-tone page into a grained **desk** with smooth **plates** laid on it every other section, every layer tinted to the brand's own hue. No markup changes. Delete the block to revert.

## The picture

This is the whole look. The block produces exactly this and nothing else.

- **The desk.** The page background becomes a material: a fine grain tinted to the brand, light falling from the top left, the far corner in shade. It is the only textured surface on the page.
- **Plates.** Every other section is a plate: it spans the screen, `max(10px, 1.6vw)` in from each edge, square like a drawing sheet, with a hairline edge in the brand's tone and a deep soft shadow. It is smooth and a touch darker than the grain around it, so it reads as a panel laid on the desk.
- **Rhythm.** Plates and open sections alternate. The open section is the gap between two plates: plates never touch, and they carry no vertical margin of their own.
- **The band.** The hero, with any strip glued under it (stats, logos), is a full-bleed band in its own smooth tone, closed by a hairline. The first plate sits 28px below it. The footer rests on the desk.
- **One glow.** The plate the page wants acted on (the demo, pricing, the sign-up) has a soft glow of the accent underneath.
- **Wells.** The site's own cards, code blocks and screens sit one step darker than the plate, like screens set into it. On the desk they become solid objects instead of holes in the grain.
- **One tone.** Desk, band, plates, wells, edge, light and grain all take the accent's hue at a very low chroma. `scripts/tone.mjs` computes every value; nothing is picked by eye.
- **Phones keep the frames.** At 390px the plates are still 10px in from both edges with their full border, so each section is a distinct block while scrolling. That is where the effect matters most.

The block holds the recipe's rules and nothing else. It adds no motion, no extra colour, no pattern and no change to the site's layout.

## Workflow

### Step 0: Scope
Find the pages in scope and the global stylesheet: Next `app/globals.css`, Vite `src/index.css`, Astro `src/styles/global.css`, Nuxt `assets/css/main.css`, styled-components `createGlobalStyle`, plain HTML: the last `<style>` in `<head>`.

### Step 1: Audit
Follow `references/audit.md`. Output: a five-line summary, the token table (page bg, body text, accent, the card selectors, the container), the fixed and sticky elements, and the section list in order with height and contents.

Stop here and say why if the page already has three or more distinguishable planes with a consistent light, if it is deliberately flat or brutalist, if every section is full-bleed photography, or if it is an app shell or dashboard.

### Step 2: Tone
Run the tone script with the three colours from the token table:

```bash
node <skill-dir>/scripts/tone.mjs --bg "<page bg>" --text "<body text>" --accent "<accent>"
```

It picks the theme from the background, takes the hue from the accent (a grey accent gives a neutral palette) and prints every `--unflat-*` colour, the shadow, the glow and the two grain layers. Paste its output into the block's `:root` as it is.

### Step 3: Rhythm
Follow `references/rhythm.md`. Mark every section **band**, **plate** or **open**, with one reason each, pick the one **glow** plate, and write the list in your response before writing any CSS. This is the design decision of the whole job.

### Step 4: Write the block
Copy `references/recipe.css`. Paste the tone output into `:root`, then replace the placeholders with selectors per `references/rhythm.md`. A rule whose placeholder has no target on this site is deleted, never left with the placeholder in it, and the same token is removed from the print rule. Delete the recipe's header comment; keep the numbered rule comments.

Append the block at the end of the global stylesheet. For a single HTML file, insert it right before the last `</style>` with this one-liner (block saved as `unflat-block.css`); it writes exactly one newline between `/* unflat: end */` and `</style>`:

```bash
node -e "const fs=require('fs');const [f,b]=process.argv.slice(1);const s=fs.readFileSync(f,'utf8');const i=s.lastIndexOf('</style>');fs.writeFileSync(f,s.slice(0,i)+fs.readFileSync(b,'utf8').replace(/\s+$/,'')+'\n'+s.slice(i))" page.html unflat-block.css
```

### Step 5: Cards, masks, open sections
Follow `references/rhythm.md` §5–7: which cards become wells, which elements painted the old page colour to hide a line (they turn into dark patches on a plate, or boxes on the grain), and which open sections paint their own copy of the page colour over the desk.

### Step 6: Verify
Run the checklist in `references/guardrails.md` at 1440×900 and on phones at 390×844 and 360×780. With a browser tool, run its snippet and take the screenshots it lists. If the person has a phone on the same network as the dev server, give them the LAN address (`http://<this machine's IPv4>:<port>`) so they can check it on the real device.

### Step 7: Report
Seven lines:
1. The palette: theme and hue (from the tone script's comment line).
2. The rhythm, with the band, the plates (glow marked) and the open sections.
3. Wells, masks and open sections changed.
4. The file touched and where the block sits.
5. How to revert.
6. What the checks found at 1440, 390 and 360.
7. Any rule deleted for lack of a target, and any markup change made.

## Rules that do not bend

- **One block.** Everything lives between `/* unflat: start */` and `/* unflat: end */`, appended last. Nothing else in the codebase changes.
- **Colours come from `tone.mjs`.** Only `--unflat-inset`, `--unflat-first` and `--unflat-radius` are set by hand, and only as `references/rhythm.md` says.
- **Alternation.** The first section is never a plate. Two plates are never adjacent. Header, nav, footer and anything fixed or sticky are never plates.
- **The frames stay on phones.** The inset, the border and the shadow are the same at every width.
- **Contrast holds.** The tone script keeps a plate's base within about 2% lightness of the original page background, so the site's text colours keep their contrast. On a page darker than OKLab L 0.14 it lifts the plates further, so the desk has room below them; that only helps light text.
- **Nothing moves.** The block adds no `transition`, `animation`, `filter` or `backdrop-filter`.
- **Reversible.** Deleting the block restores the site byte for byte. If a markup annotation was unavoidable (`references/rhythm.md` §9), say so in the report.

## References

- `references/audit.md`: the flatness audit and a browser snippet that extracts tokens and the section list.
- `references/rhythm.md`: band, plates and open sections; selectors; glow; wells, masks and open sections; gotchas.
- `references/guardrails.md`: the checklist for desktop and phones, the verification snippet, the painting-order gotcha.
- `references/recipe.css`: the block skeleton.
- `scripts/tone.mjs`: derives every colour from the page background, the body text and the accent.
