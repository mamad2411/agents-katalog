---
name: anime-80s
description: Turn any brand, product, event, sentence, theme, or reference photo into an original printed piece that looks like it came out of 1980s Japanese anime print culture - theatrical one-sheets, anime-magazine covers, solid colour-field posters, one-ink screenprints, package labels, riso overprints, colored-pencil plates, and giant-word posters. Use whenever the user asks for 80s anime, 90s anime, retro anime, old anime, cel animation, cel-shaded, city pop, showa anime, anime key art, anime movie poster, anime magazine cover, or wants their brand, product, merch, packaging, social post, podcast cover, or event "in an old anime style". The brief's subject is always the star; the anime look is only the rendering language. Invents original characters and hero objects - never existing franchise characters, logos, titles, or taglines. Produces the final generation prompt plus a generated raster image unless the user asks for prompt only.
---

# 80s Anime: Cel & Print

One look, applied to anything:

> cel-era anime drawing + a limited set of printing inks + visible paper + one period print format + title lettering with a katakana echo + press wear

**The direction, in one line: every output is a printed object from the cel era.** A poster, a label, a magazine cover, a tee print, a zine page. Never a full-colour digital illustration, never a screenshot, never a painted background. The drawing is 1980s anime; the medium is always ink on paper.

**The paper stays visible.** The ground is paper or a light-to-mid ink, never black, and 25-45% of the sheet reads as open ground. A sheet drowned in dark ink is off-style even when everything else is right.

The subject can be anything: a coffee roaster, an app launch, a bike shop tee, a sardine tin, a podcast, a single sentence. The anime look is how it is drawn, never what it is about. Do not output generic anime scenery unrelated to the brief.

## Default Deliverable

1. one compiled generation prompt;
2. one generated raster image;
3. a short recipe note naming format, era, palette, shot, lettering, and wear.

Generate with whatever image tool is available: a native image tool, an image API, or ChatGPT Images in a browser session the user is already signed into (open Images, type the prompt into the composer as one block with no line breaks, since Enter only inserts a newline, click Send prompt, attach any supplied photo, and wait about 1-2 minutes). For a retry, send a follow-up in the same chat that names the one failure and restates what stays unchanged. Save files to a folder the user names, otherwise `~/Desktop/Claude skills/anime-80s/`. Stop at prompt-only only when the user asks for it or no generator exists, and say which.

## 1. Read the Brief

Extract before composing:

- **Subject:** the one product, person, place, event, or idea that must stay recognizable.
- **Brand anchors:** 2-4 things that must survive translation exactly: product silhouette, signature colour, supplied logo, packaging layout, name. Never invent a logo. Reuse a supplied logo only as given, flat and unworn.
- **Intent:** launch or announcement, brand statement, merch, packaging, social cover, feature breakdown, or keepsake.
- **Words:** preserve supplied text exactly, in its language. With no text, invent one English title of 1-3 words and an optional tagline of 3-8 words; keep both identical across retries. Omit text only when the user asks for a text-free image.
- **Japanese echo:** default to a katakana transliteration of the title or brand name, 8 characters or fewer, as secondary lettering. Use user-supplied Japanese exactly. Never invent Japanese sentences. Omit when the user asks for English only.
- **Image role:** supplied photo to translate, supplied product to hero, or nothing.

Translating supplied material:

- **People** become an original cel character who keeps identity anchors: hair shape and part, glasses, facial hair, skin tone, signature garment, expression. Redraw them in era proportions; never paste a photoreal face onto a printed piece.
- **Products** become the **hero machine** (section 3): same silhouette, proportions, label layout and brand colours, drawn like the motorcycle or mecha in 80s key art.
- **Places** become a flat ink field, a simple ink horizon, or bare paper. Never a painted scenic background.

For a complex topic, pick one concrete moment or object. Do not illustrate every point.

### Recipe Manifest

Resolve the brief into this manifest before writing the prompt. Do not skip fields. Do not show it unless the user asks for process.

The catalogs in `system/` are the source of truth for IDs and values: `formats.json` (formats, shots, carriers), `palettes.json`, `lettering.json`, `eras.json`, `wear.json`. Read only the one you need for the current decision. When prose and a catalog disagree, the catalog wins.

```yaml
subject: <one recognizable subject>
brand_anchors: <2-4 anchors that must survive, or none>
intent: <one intent from Read the Brief>
exact_text: <supplied text, or invented 1-3 word title>
tagline: <supplied, invented 3-8 words, or none>
japanese_echo: <katakana transliteration, supplied Japanese, or none>
format: <format ID from system/formats.json>
carrier: <carrier ID or none>
ratio: <explicit ratio or the format default>
era: <era ID from system/eras.json>
palette: <palette ID allowed for the format>
hero_override: <brand hex replacing the palette's hero_slot, or none>
ink_budget: <the format's ink count>
shot: <shot ID from system/formats.json>
money_shot: <the one thing that reads at thumbnail size>
release_zone: <one quiet area of open ground: bare paper or a flat ink field>
character: <original design card, or none>
hero_machine: <product description with anchors, or none>
moment: <the ordinary in-between action>
contact_points: <what carries the body's weight, what each hand holds>
motion_device: <one from section 3, or none>
lettering: <primary role + support role from system/lettering.json>
wear: <effect IDs from system/wear.json>
seed: <stable hash of subject + exact_text + format + palette>
```

Defaults when the user has not chosen:

- era: `era_bubble` (1985-1989);
- format: the first match in Route the Format;
- ratio, palette, shot and lettering: the format's defaults in `formats.json`;
- hero override: a brand's signature colour replaces only the palette's `hero_slot`;
- wear: 2 effects from `wear.json`; 0-1 for packaging and logo-critical work;
- seed: preserve across retries.

Explicit user choices override defaults unless they break the originality firewall or the format's ink budget. Identical inputs resolve identical manifests: never vary format, palette or shot for novelty.

## 2. Route the Format

Walk the list top to bottom and take the first match unless the user names a format:

1. A package, label, tin, pouch, bottle, box or jar: **package label**.
2. Launch, release, event, date, or facts to announce: **one-sheet**. The facts become the billing block.
3. Several products, features or SKUs: **one-sheet**, with the line-up repeated small in one ink under the hero.
4. Merch, tee, tote, sticker, stamp, or an explicit one-ink request: **mono screenprint**.
5. A person is the brand face, or fashion, lifestyle or a social cover: **magazine cover**.
6. Explicit overprint, riso, zine, or two layers crossing: **overprint**.
7. Tea, café, books, wellness, plants, or a tender, quiet brief: **pencil plate**.
8. The phrase itself is the subject: **type sandwich**.
9. Otherwise: **colour field**.

Format anatomy (numbers live in the catalog):

- **Package label:** the real package seen flat and front-facing, filling most of the frame on a plain ground. The label art is printed in one or two inks; only the package's own material, such as a tin rim, pull ring, cap or seam, sits outside the print. Bust or object art, a worn display word across the top band, vertical katakana in markers down one side, and one small weight or volume line.
- **One-sheet:** three inks on poster cream. A letter-spaced tagline across the top edge; the hero machine large with the character smaller beside it; a massive condensed title in the lower third that the figure or machine nearly touches; a compressed billing block where brand facts read as film credits ("roasted by", "poured at") using supplied names only; one date line. No rating badges, sound-format logos or distributor marks.
- **Colour field:** the ground is a solid ink. The subject is rendered in exactly two more inks, a near-black shadow ink swallowing roughly half the form and one light ink for the lit planes, with the ground showing through as the third value. A huge worn display word across the top band, overlapped by the figure. Vertical katakana in circle and box markers down one side.
- **Mono screenprint:** one ink on a pale ground, or inverted with an ink ground and paper-negative linework. Inversion is the one place a saturated ink covers the sheet, and it only works when the cream linework and cut-out shapes keep it open: if the inverted sheet reads solid and heavy, print it the normal way round instead. Shading only by stipple and speckle. Must read at t-shirt scale.
- **Magazine cover:** three inks on cream paper. A heavy italic masthead spans the top, partly hidden behind the figure's hair; a full-body figure stands on bare paper, printed in one shadow ink and one light ink; a few small cover lines stack in one corner; issue number and month.
- **Overprint:** two inks that multiply. One carries the subject as engraving-like hatching or linework; the other carries brush strokes, loose doodles (arrows, stars, eyes, keys) or big brush katakana. Overlaps darken; that is physics, not a third ink.
- **Type sandwich:** one giant ultra-bold word cropped by the top edge and repeated, cropped or mirrored, at the bottom; the figure painted between them in loose brush and pencil with flat blush circles and one coloured detail such as nails or eyes; vertical katakana; one small registration-style circle mark with a date.
- **Pencil plate:** one colored pencil on kraft or tan paper; hatching and loose contour, objects and leaves filled flat in the same colour; a tender pose; no lettering, or one small handwritten word.

## 3. Cel Rendering Law

The drawing is 1980s anime; the surface is always print. Apply all of it, compressed into the format's ink budget.

1. **Keyline:** a traced warm near-black line, steady in weight and heavier on the outer contour, slightly broken as if photocopied. Never a thin uniform vector line.
2. **Two tones per surface:** base plus one hard-edged shadow shape. No soft shading on characters, clothes or props. Shadows are graphic shapes cut along form: under the jaw, down the far side of the face, inside cloth folds.
3. **Highlights are shapes:** hair gets one pale band or clumped streaks; eyes get 2-3 hard dots; glossy objects get sharp specular slashes. Hair is a handful of large clumped shapes, never individual strands.
4. **Flat everything:** no gradients. The single exception is an airbrushed specular sheen on a glossy hero machine, and only in formats with the inks to spare.
5. **Backgrounds are printed, not painted:** a flat ink field, bare paper, a simple ink horizon, or a halftone field. Never gouache scenery, never photoreal depth.
6. **One motion device at most:** speed lines, streaked ink, light trails, 4-point sparkles, an impact flash, a sweat drop, or a gag face for a comedy beat.
7. **Light:** a hard rim light as a cel shape, and shadows as flat shapes. No lens flares, bokeh or depth-of-field blur.

### Characters (always original)

- **Proportions and eyes** follow the era in `eras.json`: adults 7-8 heads tall, a small angled nose line, readable jaws on men, big volumetric hair with clumped silhouettes.
- **Wardrobe and props** come from the era: bomber, leather and denim jackets; high-waisted jeans with rolled cuffs; oversized tees; turtlenecks; shoulder pads; headbands, bandanas, hoop earrings, aviators; Walkman, cassette, pager, film camera.
- **Brand integration:** the character uses, wears, carries or rides the subject during an ordinary moment: pouring, pedalling, laughing mid-sentence, walking away, looking up. The product is part of the story, never held up to camera like an ad.
- **Pose physics:** every pose names what carries the weight. Seated hips rest fully on the seat with the thighs along it; a standing figure's weight lands on one clearly planted foot; a leaning figure's elbows or back touch the surface; hands visibly grip what they hold. Prefer simple grounded poses (standing, straddling a stopped bike with one foot down, sitting deep in a chair) over perches on rails, ledges and edges, which image models float.
- No cigarettes or alcohol in brand work unless the user asks for them.

### Hero Machine

When the subject is a product or object, draw it like the hero motorcycle in 80s key art: low three-quarter or top-down angle, crisp keyline, flat cel shadow, one or two hard specular slashes, optional speed lines. Keep brand anchors exact and add no fictional decals, sponsor stickers or logos. **Show the product's identifying silhouette whole and unobstructed at least once**; if a hand holds it, the hand grips a part that does not define the shape, and no prop may make it read as a different object.

## 4. Inks and Ground

Read `palettes.json`. Each palette names its slots, its `hero_slot` and the formats it serves.

- **Obey the format's ink budget:** mono screenprint and pencil plate 1 ink, package label 2, overprint 2, one-sheet, colour field, magazine cover and type sandwich 3. The ground is not an ink and overprint overlaps are not an ink.
- **Grounds may be a solid ink**, but only a light-to-mid one: cream, kraft, rice, pale sky, pink, mint, marigold, poster red. Never black or near-black, and never a dark ink covering the whole sheet.
- **Keep 25-45% of the sheet as open ground**, and keep the darkest ink under about a third of the area. This is the difference between a printed piece and a heavy digital poster.
- **Rotate the hue.** Blue is never the default, and no two pieces in a series lead with the same hue. Pick the family from the subject: food, beauty and youth lean hot pink, magenta, coral and marigold; nightlife, music and tech lean magenta, cyan and violet; outdoors and sport lean vermilion, teal and marigold; quiet, literary and botanical lean oxblood, indigo and green.
- **Brand colour override:** the brand's signature hex replaces the palette's `hero_slot` only, and the hero's shadow becomes a darker shade of it. If it clashes with the ground, pick another palette allowed for the format.
- **Colour words** ("make it pink") choose among palettes allowed for the routed format; if none fits, apply the colour as a hero override on the format's default palette.
- These are 1980s printing inks and cel paints: saturated but chalky, never glowing digital neon.

## 5. Lettering

Read `lettering.json`. Use one primary display role, one support role and the optional Japanese echo: never more than three voices.

- Scale jump: the title is 8-20 times the smallest type.
- Title 1-3 words, tagline 3-8 words, no body copy.
- The title must touch, sit behind or lock to the figure or hero machine. A title floating in its own safe zone is a failure.
- Japanese: 8 characters or fewer, set large enough to print cleanly, as a vertical marker column, a stacked logotype or cover-line texture. If it garbles after one retry, drop it rather than ship gibberish.
- Billing blocks and cover lines may be dense microtype texture. Any legible words must be supplied facts or plain generic labels. No real studio, staff or distributor names.
- No gradient type, chrome or 3D type, glow type, or modern esports lettering. Worn ink and slight misregistration are welcome on display type only.

## 6. Voice

Cel-era taglines are short, cool, and a little fatalistic or sweet. Write in English unless supplied otherwise. Pick one register:

- **Countdown:** a plain statement that something is about to happen, tied to a time or place from the brief.
- **Farewell:** an unfinished goodbye or promise to meet again, often trailing off with an ellipsis.
- **Dare:** a short challenge addressed to the viewer.
- **Summer promise:** a physical sensation or open direction, such as a road, a train line or a late hour.

Make it specific to the brief. No sales CTA, no hype adjectives, no productivity slogans, and never a franchise's tagline or a line you have used for an unrelated brief.

## 7. Wear

Read `wear.json`. Everything here is printed, so wear is press wear: paper speckle, screenprint stipple, riso grain, misregistration, halftone, fold creases, edge wear, worn title ink. Pick 2, or 0-1 for packaging and logo-critical work. It lives in the ink and the paper; it must never look like a filter laid over the image. Never wear down supplied logos or small legible facts.

## 8. Prompt Compiler

Write the prompt as six compact paragraphs in this order:

1. **Medium and frame:** the printed object and its format, carrier, ratio, era and year range, the phrase "looks like an original [year] print, scanned, not a modern digital illustration imitating one", the ground, the exact inks with hexes and slot roles, and the ink budget stated as a hard limit.
2. **Composition and camera:** the shot, the money shot, the release zone, where the title sits relative to the figure or machine, and the crop.
3. **Subject design:** the original character's design card (age, hair shape and colour, eyes, face, wardrobe, prop) and/or the hero machine with its brand anchors, plus the ordinary moment and the pose's contact points.
4. **Rendering:** keyline, two tones per surface, highlight shapes, hair as clumped shapes, flat printed background, one motion device, the light, and the ban on gradients.
5. **Lettering and words:** exact title, tagline, Japanese echo, lettering roles, scale and placement.
6. **Wear and avoids:** chosen wear effects, hard avoids, and the originality reminders.

Describe only visible outcomes. Never name studios, directors, artists, franchises, or write "in the style of".

## 9. Originality Firewall

References teach grammar; they are never sources to trace.

- **No existing characters or near-copies.** Change at least three of: hair silhouette, signature garment, signature colour combination, face marks, prop, companion animal. Combinations to avoid include: blue suit, yellow shirt and wild dark hair; a red biker jacket with a capsule emblem and a red sci-fi motorcycle; twin buns with a sailor uniform; a black cat with a crescent on its forehead.
- **No franchise marks:** no titles, logos, katakana logotypes, taglines, credits, studio or distributor marks, rating badges or film-format logos.
- **Recombine:** each format's default camera comes from a different source than its layout. Never pair a format with the shot, palette and lettering of the single reference that taught it.
- **Change at least four structural variables** from any supplied reference: subject and crop, format, title wording, title position, shot, palette, lettering role, inset or marker system, ratio, motion device.
- A supplied photo of the user's own product or person is content to preserve, not a reference to avoid.

## 10. Hard Avoids

Always exclude:

- anything that is not a printed piece: full-colour digital illustration, a screenshot, a painted scenic background, photoreal depth;
- black or near-black grounds, dark heavy sheets with no open ground, photographic inset panels;
- grunge overload, torn edges, heavy distressed borders;
- modern anime rendering: soft airbrushed skin, gradient irises, glossy game-art lighting, bloom, lens flares, bokeh, depth of field, 3DCG, thin uniform vector lines, 2010s moe proportions outside a gag beat, hyper-detailed hair strands;
- AI tells: plastic skin, extra fingers, melted lettering, fake Japanese gibberish, watermarks, signatures;
- vaporwave clichés: pink grid floors, palm-tree silhouettes, marble statues, scanline sunsets, random "aesthetic" Japanese;
- invented logos, sponsors, URLs, QR codes, badges;
- styled scenes and props around a package: hands, plants, coffee cups, wooden boards, models, hangers;
- more inks than the format's budget;
- existing franchise characters, marks or taglines.

## 11. Generate and Inspect

1. Generate the image from the compiled prompt.
2. Inspect it at full size and at thumbnail size.
3. Regenerate once, with the failure named in the revised prompt, when:
   - it reads as a digital illustration or a screenshot rather than something printed;
   - gradients, soft shading or painted scenery appear;
   - the sheet reads dark or heavy, with less than a quarter of it as open ground, or the ground is black;
   - the subject or a brand anchor is lost, altered or reads as a different object, or a fake logo appears;
   - a character resembles an existing franchise character;
   - a pose is physically wrong: hips floating above a seat, unsupported weight, limbs passing through objects, impossible joints, or extra or missing limbs;
   - the format exceeds its ink budget;
   - the title is garbled, floats detached from the figure, or lacks an 8x scale jump;
   - there is no single money shot at thumbnail size;
   - the Japanese is garbled (drop it on the retry);
   - the wear reads as a filter overlay.
4. If text still fails after one retry, deliver a text-light version and say the lettering should be set in a layout tool. Never present garbled text as correct.

## Output Format

````markdown
**Image**

![80s anime print](absolute-image-path-or-rendered-image)

**Final prompt**

```text
[prompt used for generation]
```

**Recipe**

- Format: [format] on [carrier], [ratio]
- Era: [era and year range]
- Inks: [palette name, hexes, budget; hero override if any]
- Shot: [shot] / money shot: [what reads at thumbnail]
- Lettering: [primary role + support role + Japanese echo]
- Wear: [effects]
- Originality: [one sentence on what makes the character and layout new]
````

## Quality Gate

- Does it read as a printed object rather than a digital illustration?
- Is the brief's subject the star, rather than generic anime scenery?
- Do the brand anchors survive exactly, with the product's silhouette readable and no invented logos?
- Does every surface follow base plus one hard shadow, with no gradients and no painted background?
- Is the ground paper or a light-to-mid ink, with 25-45% of the sheet reading as open ground?
- Is the character original, era-correct, and caught in an ordinary moment?
- Is the pose physically possible, with clear contact points carrying the weight?
- Is there one money shot and one visibly quieter release zone?
- Does the title touch or lock to the figure or machine with an 8x or greater scale jump?
- Is the Japanese echo short and correct, or absent?
- Does the piece stay inside its ink budget, and does the hue differ from the last piece in the series?
- Does the wear feel like paper and ink rather than a filter?
- Are at least four structural variables changed from every reference, with no franchise marks?
- Did the run generate an image unless prompt-only was requested?

## Example Triggers

- "Make an 80s anime poster for my coffee brand's launch next Friday."
- "Turn this sneaker photo into retro anime key art."
- "One-ink anime screenprint tee for my bike shop."
- "Old anime magazine cover for my podcast, here's my photo."
- "Design a sardine tin label in 80s anime style."
- "Show our three sauces as one 80s anime line-up poster."
- "Riso overprint anime flyer for a vinyl night, magenta and green."
- "Make my shop name into a giant-word anime poster."
