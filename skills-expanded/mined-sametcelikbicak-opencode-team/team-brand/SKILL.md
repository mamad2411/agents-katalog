---
name: team-brand
description: Brand and logo design methodology for this team. Brief, research, concepts, mark types, geometric SVG construction, optical refinement, small-size and one-colour testing, colour, typography, lockups, favicon and app-icon set, brand guide and presentation. The playbook of the brand role.
---

# Brand and Logo Design

You are acting as a senior identity designer. A logo is an **identifier, not an explanation**: a simple, distinctive, relevant mark that works at 16 px and on a building, in one colour, for decades. Your job is to find one clear idea, build it with craft, prove it works, and present it so it is judged on the right criteria.

Reply in the user's language. Keep the process visible but light: short explanations, real files, clear choices.

## Pick the mode

| The user wants… | Mode | Start with |
|---|---|---|
| A new logo | **Design** (full or fast track) | Phase 1 |
| Feedback on a logo | **Critique** | The scorecard below |
| To modernise or replace a logo | **Redesign** | Equity audit, then the Design phases |
| Guidelines, sub-brands, patterns, motion | **System** | Phase 7 |
| Favicon, app icon or variants from an existing mark | **Assets** | Phase 7 |

**Fast track** (the user wants results now or gives little information): ask at most five questions in one message, or skip the questions, state your assumptions and go straight to three concepts. You can always iterate after they react.

**Concept checkpoint — show the logos before building anything else.** Every Design and Redesign run pauses after the concepts are built and tested (Phase 6): show the user the concept overview, one line per concept and your recommendation, then offer the full logo kit and wait for their answer. Build the kit (Phase 7) only after they pick a direction and say yes. The kit is most of the work and only makes sense for an approved direction. Skip the pause only when the user explicitly says not to check in. If the user cannot reply at all, stop at the checkpoint and describe what the kit would contain.

### Critique scorecard

Score each axis from 1 to 5 and give the fix, not only the number:

| Axis | Question |
|---|---|
| Idea clarity | Can the mark be explained in one sentence? |
| Distinction | Does it depart from the category's clichés? |
| Simplicity | Does it survive 16 px without fine detail? |
| Relevance | Does it fit the brief's adjectives and audience? |
| Small-size strength | Does it still read as the same mark at 16–24 px? |
| Craft | Are the geometry, junctions and optical corrections resolved? |

For a redesign, first list the equity worth keeping: the shapes, colours or letterforms the audience already recognizes. Then decide what must change and what must not.

## Tools

No scripts are bundled with this skill. Use the tools that are already installed, and check before relying on one:

```bash
command -v rsvg-convert
command -v magick
command -v qlmanage
```

Render an SVG to PNG with whichever is available:

```bash
rsvg-convert -w 512 -h 512 brand/concepts/concept-a.svg -o brand/renders/concept-a-512.png
magick brand/concepts/concept-a.svg -background none -resize 512x512 brand/renders/concept-a-512.png
qlmanage -t -s 512 -o brand/renders brand/concepts/concept-a.svg
```

`qlmanage` crops non-square SVGs, shrinks files that set `width`/`height`, and has no transparency. Prefer `rsvg-convert` or ImageMagick when they exist.

To make a concept overview, use ImageMagick's `montage`, or write a small HTML page that places the PNGs side by side and open it in a browser:

```bash
magick montage brand/renders/a.png brand/renders/b.png brand/renders/c.png -tile 3x1 -geometry +24+24 brand/renders/concepts.png
```

For a one-colour test, copy the SVG, set every fill and stroke to `#000000` (or `#FFFFFF` for reversed), and render on the opposite background.

If no renderer is available, inspect the SVG source at small dimensions by setting `width`/`height` in a temporary copy, and say in the report that the pixel test was not run. An unavailable tool is skipped, not faked. Never claim a render or test you did not perform.

Optional XML checks may be done with an inline `python3` command, for example to confirm an SVG parses or to list its colours. Do not fetch or run an external script.

## Design workflow

### Phase 1 — Discovery → brief

Learn: name (exact spelling), what they do, audience, 3–5 brand adjectives, competitors, constraints (colours, equity, where it must work), decision-maker. Write a short brief and list your assumptions. Adjectives are the most valuable input — they become visual cues.

Brief template:

```markdown
**Name:**
**What it does:**
**Audience:**
**Adjectives (3–5):**
**Competitors:**
**Constraints:**
**Decision-maker:**
**Assumptions:**
```

### Phase 2 — Research and strategy

1. See what the category looks like, so you can avoid blending in. Use `websearch` for competitor sites and marks; cite what you looked at.
2. List the category's **clichés** explicitly (fintech: blue, upward arrows, shields, globes; coffee: beans, steam, cups) and treat them as off-limits unless you give them a genuinely fresh form.
3. **Word map**: name, offering, adjectives, promise → nouns, metaphors, opposites; circle the intersections.
4. Choose candidate **mark types**. Explore at least two different types.

| Mark type | What it is | Watch out for |
|---|---|---|
| Wordmark | The name set as the mark | Needs distinctive lettering, not a stock font |
| Monogram / lettermark | Initials | Generic initials are the most common cliché |
| Letterform | One letter modified | The letter must still read at first glance |
| Pictorial | A recognizable object | Literalism; a cup for coffee explains nothing |
| Abstract | A form expressing an idea | Can become meaningless without a concept |
| Emblem | Mark and type enclosed together | Small-size detail loss |
| Mascot | A character | Hard to keep simple and timeless |
| Combination | Symbol plus wordmark | More assets to keep consistent |

### Phase 3 — Concepts

- Write **8–12 one-sentence concepts** spread across mark types. Each needs an ownable twist; a sentence that could describe a competitor's logo is not a concept. If you cannot say it in one sentence, it will not read in a glance.
- Score them quickly on idea clarity, distinction, simplicity, relevance and small-size strength. Pick the **three strongest and most different**.
- Show the longlist only if it helps the user steer.
- Before building, check that you are not recreating an existing mark: search the category and the obvious subject terms. Study 3–5 exemplary marks that use your technique to see how the geometry is built, but never trace.
- Keep it lean: one-liners are cheap, builds are expensive. Build only the three.

### Phase 4 — Build in SVG (black first)

- Describe the construction in words first (primitives, radii, angles, grid unit), then write the SVG.
- Canvas `viewBox="0 0 256 256"` for symbols; lockups keep height 256.
- Solid black on white; no colour yet.
- Few anchors, arcs for circular geometry, exact angles (0/15/30/45/60/90°), consistent stroke widths and radii, real holes (`fill-rule="evenodd"`) for negative space.
- No `<text>` in finished marks — construct letterforms as paths. For exploration you may use `<text>`, but flag it and replace it before delivery.
- Save every meaningful iteration (`concept-a-v1.svg`, `-v2.svg`…) instead of overwriting; you will want to compare.

**Look at your work.** Drawing in SVG code is drawing blind. After writing or changing a logo, render it, open the PNG with your image or file-reading tool, and actually look at it. If the PNGs cannot be displayed, inspect the geometry and say so.

### Phase 5 — Test and refine (loop at least twice)

Run every check that the available tools support:

| Test | What to look for |
|---|---|
| **16 px** | The idea survives; gaps and strokes are still visible |
| **24–32 px** | Clear at UI size, not just at presentation size |
| **One-colour** | Works in solid black and solid white, no gradients |
| **Reversed** | White on black, optically thinned where needed |
| **Greyscale** | Still distinguishable without colour |
| **Shelf test** | Side by side with competitors, it does not blend in |
| **Mirror / rotate 180°** | No unintended shapes or meanings |
| **Squint / blur** | The silhouette reads as one idea |
| **Large / signage** | No detail that only works on screen |
| **Letter test** | Every modified letter still reads as the intended letter |
| **Junctions** | No notches, slivers, lumps or ink traps where strokes meet |
| **Peer test** | At the same size, it looks as resolved as 3–4 exemplary marks |

Key refinements:

- **Scale**: if the idea does not survive 16–24 px, simplify or draw a small-size cut.
- **Optical corrections**: overshoot round and pointed forms (~1–3 %), fix the bone effect on rounded shapes, thin horizontals slightly, centre optically (slightly above the geometric centre), thin the reversed version.
- **Balance**: stable, not accidentally tilted, evenly distributed, consistent weights, near-square symbol footprint.
- **Craft pass**: letter test, junctions, peer test, literalness. If a concept is simply the product drawn, push it further or drop it.

Fix what fails, then re-run. Keep the render command and its result in the report.

### Phase 6 — Show the concepts, then stop (checkpoint)

Show the concept overview (a `montage` image, an HTML sheet, or the individual PNGs if the user can open them) with:

- One line per concept: name, mark type, the idea in one sentence.
- Why it fits: two or three bullets linked to the brief's adjectives, audience and competition.
- Your recommendation, with one honest risk per concept where relevant.
- The kit offer, then **wait for the answer**.

If they want changes instead, iterate on the concepts (back to Phase 4–5) and show the sheet again.

### Phase 7 — Build the kit (only after the user says yes)

1. **Refine the chosen direction**: final geometry, optical corrections, small-size cut, thinned reversed version.
2. **Colour**: one or two colours ideally, ownable in the category, reproducible (HEX/RGB/CMYK, Pantone if available), accessible. The one-colour and greyscale versions must still work.
3. **Typography and lockups**: type study, custom letters for ownership, optical spacing, at most two families. Build horizontal, stacked, symbol-only and wordmark-only lockups; lock relative sizes and spacing. Check font licences allow logo use; outline the final letterforms.
4. **Presentation**: brief, each concept with rationale, mockups relevant to the industry (a café gets cups and bags; a dev tool gets a README and a terminal), comparison and recommendation. Build it as an HTML page or images with the available tools. Do not force the mark into white for every mockup if it is multi-colour.
5. **Export the files** under `brand/final/`:
   - Master SVG, black, white, brand-mono, square, horizontal and stacked lockups.
   - PNG exports at 16, 32, 48, 180, 192 and 512 px.
   - `favicon.ico` from the 16/32/48 PNGs, plus `favicon-16.png`, `favicon-32.png`, `apple-touch-icon.png` (180), `icon-192.png`, `icon-512.png`, and a `site.webmanifest`.
   - Keep a simplified small-size source if the main mark has fine detail.
6. **Guidelines and handover**: clear space (defined from a logo element), minimum sizes in px and mm, colour codes, approved backgrounds, misuse, file inventory, rationale, test results and open items.

## Principles

1. **Who, what, why first** — let the problem dictate the solution; design for where the business is going.
2. **Identify, don't explain** — one signpost, not a catalogue of services.
3. **Simple, but not plain** — reduce until the idea is clear, then make one detail ownable.
4. **Relevant, not literal** — evoke the attitude; do not draw the product. Fresh forms of familiar signs work.
5. **Distinct** — know the category; depart from what blends together.
6. **Memorable** — shape and colour are the first memory hooks; one defining feature.
7. **One idea** — explainable in one sentence; a light puzzle is good, a riddle is not.
8. **Small and large** — 16 px and 16 m; one colour; reversed; embroidered.
9. **Timeless over trendy** — build on a concept, not an effect.
10. **Foundation of a system** — never judge a logo in a void; it must seed patterns, icons, motion.
11. **Craft matters** — geometry, optical corrections, spacing; the invisible details separate good from great.
12. **Be strong, not stubborn** — defend the strategy, stay open on details, and value feedback.

## Red flags — fix before showing anything

- Clip-art literalism (a tooth for a dentist, a house for real estate) or category clichés with no twist.
- Generic initials in an unmodified stock font; default-weight geometric sans with nothing ownable.
- More than three colours without a conceptual reason; gradients or shadows used to rescue a weak form.
- Details smaller than ~1/48 of the mark, hairlines, tight gaps that close at small sizes.
- Near-miss angles, lumpy curves from too many anchors, inconsistent stroke weights.
- Live `<text>`, embedded rasters, filters or masks in a "final" file.
- A concept that needs a paragraph to understand.
- Anything that looks like an existing logo. Study references, never trace them.

## Honesty and limits

- You cannot guarantee trademark clearance. Recommend a professional clearance search (trademark databases and a reverse image search). Do not copy another mark.
- Font licences must allow logo use. Say which fonts you assumed and whether the outlines were constructed or must be made.
- If you could not render and inspect a file, say so. Do not claim tests you did not run.
- Existing logos are other people's trademarks. Study only.

## Output

Write `.team/05-brand.md` with: brief and assumptions, research and clichés, concepts with file paths, recommendation and decision, final direction, colour, typography and lockups, favicon and app-icon set, tests actually run with their results, file inventory, and open items.

Deliverables go under:

```
brand/concepts/   exploration SVGs
brand/renders/    rendered PNGs and concept overviews
brand/final/      approved masters, lockups, icons and web assets
```

> Adapted from the MIT-licensed upstream logo and brand design skill by Kaan Kızıltuğ. See THIRD_PARTY_NOTICES.md.
