---
name: launch-reel
description: Make a 40 to 70 second product launch video (fast cuts between colour fields, short rising headlines, mock product UI, music) for a SaaS product, developer tool, mobile app or suite, as openCanviz project JSON that imports on opencanviz.com. Use when asked for a launch video, promo reel, product teaser, announcement video or social clip for a product. The agent gathers facts about the product, writes a short spec, builds it with scripts/build.py, previews a contact sheet, and revises.
---

# Launch reel

A launch reel is a 40 to 70 second product video: the logo, short headlines that rise in, and
mock product UI (a dashboard filling in, an inbox, a phone screen, a pricing card) on flat
colour fields, cut to a beat. `scripts/build.py` does all the layout, timing and motion. You
write a spec: which scenes, in what order, with what words. Then you look at the result and
fix it.

The output is openCanviz project JSON. The user pastes it into **Import** on
https://opencanviz.com/create to edit, play and export it. `scripts/preview.mjs` renders it
locally first, so you can check your own work.

## Workflow

1. **Gather facts into a sources file.** Read what you can reach: the product's site, pricing
   page, README, docs, app store listing, the user's own description. Write what you learn to
   `sources.md`, one fact per line, with where it came from:
   - what it does, for whom, the three to five things people use it for
   - whether it has an assistant, chat, copilot or agent, and whether it writes or generates
   - platforms (web, iPhone, Android, CLI, API), tools it integrates with
   - prices exactly as published, figures exactly as published, dates of releases
   - brand colours (from the site's CSS or the user), the logo letter or mark
   - for a suite: every product's name, what it does, its colour, and what it replaces at what price

   Never invent a fact here. If you could not find something, leave it out; the reel works
   without it. Ask the user for screenshots of the real product if they have them.

2. **Pick a story and a style.** Stories set the order of scenes; styles set the look, the
   transitions and the music. Defaults: `showcase` and `classic`.

   | Story | Shape |
   | --- | --- |
   | showcase | logo, headline, then one product scene per capability with a headline between, end |
   | problem_solution | the pain, a headline naming the product as the answer, 2 or 3 product scenes, a stat, end |
   | before_after | logo, headline, split (old way vs new way), the scenes that make the after true, compare, end |
   | deep_dive | one feature in depth: setup, use, result, a stat for the outcome, end (plays 10% slower) |
   | rapid_fire | logo, feature_flash, two quick product scenes, logo_grid, end; few words (plays 25% faster) |
   | countdown | logo, a countdown of three reasons, one product scene proving the top one, end |

   | Style | Look | Music |
   | --- | --- | --- |
   | classic | Inter, white panels, hard cuts | pop, 116 bpm |
   | flat | bold colour blocks, no shadows, every scene pushes the last off | pop, 122 bpm |
   | glass | frosted panels over soft colour, blur transitions | chill, 96 bpm |
   | editorial | Playfair serif headlines, hairlines, ink wipes | piano, 88 bpm |
   | hand | sketchbook outlines, Caveat handwriting | ukulele, 104 bpm |
   | dark | developer dark mode, zoom-throughs | synth, 124 bpm |

3. **Write the spec** (`spec.json`). Shape:

   ```json
   {
     "brand": {"name": "Pinglet", "logo_letter": "P", "ink": "#111827", "paper": "#ffffff",
               "accents": ["#6d28d9", "#0ea5e9", "#f59e0b"], "mascot": false},
     "story": "showcase",
     "style": "dark",
     "scenes": [
       {"type": "logo"},
       {"type": "headline", "lines": ["Texts and passcodes", "in one call"], "underline": "one"},
       {"type": "snippet", "line": "Send your first SMS", "label": "send.js",
        "code": "await pinglet.sms.send({ to: '+447700900123', body: 'Your code is 4821' })",
        "status": "Delivered", "bg": "accent1"},
       {"type": "end", "cta": "Start free", "tagline": "SMS for developers"}
     ]
   }
   ```

   8 to 14 scenes (16 at most). Every scene type, its keys and its length limits are in
   `reference/scenes.md` (also printed by `python3 scripts/build.py --scenes`). Read it before
   writing a spec. Start from the closest example in `examples/`.

4. **Build.**

   ```bash
   python3 scripts/build.py spec.json --sources sources.md --out reel.json --audio reel.wav
   ```

   The build first checks the spec's claims against the sources (see Claims below). If one is
   not supported it prints why and stops with exit code 2. Fix the spec, or, if the claim is
   true, add the fact and where it came from to the sources. Do not reach for
   `--allow-unsourced` to get past a check; it exists for the user to override you.
   Add `--screenshot shot.png` (repeatable, needs Pillow) to fill `screenshot` scenes with the
   real product. `--audio` needs numpy and scipy; skip it if they are missing.

5. **Preview and look at it.** Once per machine: `cd scripts && npm run setup` (installs
   `@opencanviz/player` and Playwright's Chromium). Then:

   ```bash
   node scripts/preview.mjs reel.json            # reel.sheet.png, one frame per scene
   node scripts/preview.mjs reel.json --at 12.5  # one frame, full size
   ```

   Open the sheet image and check every tile: text inside its panel and readable on its
   field, no headline wrapping into a third line, product chips not covering UI, icons drawn
   (a sparkle where you expected a logo means the ref is not bundled), the mock data
   plausible for this product. Revise the spec and rebuild until every tile reads. If Node
   is not available, say so and skip this step; the build's checks still ran.

6. **Hand over.** Give the user `reel.json` and the sheet. To use it: open
   https://opencanviz.com/create, choose **Import**, paste the JSON, click
   **Import project**. Say that the music is not in the imported project (openCanviz projects
   carry narration, not a music bed). For a finished MP4 with the music, render it locally:

   ```bash
   node scripts/preview.mjs reel.json --mp4 --audio reel.wav   # needs ffmpeg
   ```

## Claims

Mock UI is sample data and may be invented: dashboard numbers, funnel stages, inbox mail,
kanban cards, chat answers, a document being edited. Use plausible invented names (Priya,
Dev team, Acme), never real customers. Everything a viewer would take as a fact about the
product must be in the sources, and the build checks it:

- `stat`: the figure is stated (digits or words; "two minutes" supports "2 min"), never an
  invented customer result
- `pricing`: the price, copied exactly
- `receipt`: every replaced tool and its price, named in the sources; a total only if stated
- `compare`: the competitor is named in the sources, otherwise the column is "Typical tools";
  mark the alternative as having whatever a normal alternative has
- `lineup`: every product is named in the sources
- `repo`: the sources say it is open source; stars and licence only if stated
- `timeline`: every date is stated
- `quote`: the sentence appears word for word
- `chat`, `phone_chat`, `file_chat`: the product has an assistant, chat, copilot or agent
- `doc_edit`, `pill_cycle`: the product writes, drafts or generates

No awards, user counts or testimonials unless sourced. No em dashes, no emoji, sentence case.

## Choosing scenes

- Products without AI get `dashboard`, `browser`, `snippet`, `inbox`, `funnel`, `toggle`,
  `form_builder`, `kanban`, `notifications`, `phone_app`. An AI scene for a product with no
  AI is the most common way a reel misrepresents a product; the build refuses it.
- Developer tools: `terminal` and `snippet`. Not for anyone else.
- Mobile apps and hardware companion apps: at least one `phone_app`. `phone_chat` only if the
  app has an assistant.
- Suites and bundles: open with `lineup`, give each product its own UI scene with
  `"product": {"name": "...", "color": "#..."}` (it plays in that colour and wears a name
  chip), and use `receipt` when the sources say what it replaces and what that costs.
- Put a headline between product scenes in `showcase` so the reel breathes.
- `screenshot` only with a real screenshot passed via `--screenshot`; it pans and zooms to the
  `focus` points you give (x, y from 0 to 1 across the image).

## Gotchas

- `bg`: product UI scenes sit on an accent (`accent1` to `accent3`); headlines sit on
  `paper`. A headline on an accent turns light automatically when the accent is dark.
- Dark brand colours make dark fields. Funnel bars and chart bars in a dark accent vanish on a
  dark field; check the sheet, and move that scene to a lighter accent or to `paper`.
- Accents: three colours that differ in hue, not three shades of the brand colour, or every
  field looks the same.
- Icons: `ph:<name>-bold` / `ph:<name>-fill` for UI glyphs, `logos:<name>` for brand marks.
  Square marks only: `logos:stripe`, `logos:hubspot`, `logos:aws` are wordmarks and the app
  wall drops them. `python3 scripts/build.py --icons slack` lists bundled matches.
- Don't put a real company's name in mock UI as if it were a customer or a sender
  (a "Stripe" row in a mock inbox reads as a partnership). Use a role: Billing, Dev team.
- Keep to the length limits in `reference/scenes.md`. Longer text shrinks to fit and a
  headline over 26 characters per line looks cramped.
- `brand.mascot: true` adds a smiley mascot scene; leave it off for serious B2B products.

## Files

- `scripts/build.py`: spec to project JSON, with the claim checks. Python 3.9+, standard
  library only; numpy + scipy for `--audio`, Pillow for `--screenshot`.
- `scripts/launch_reel/`: the builder (scenes, styles, stories, checks, audio) and
  `icons.json`, about 670 Iconify icons (Phosphor, MIT; Iconify `logos`, CC0) so builds need
  no network.
- `scripts/preview.mjs`: contact sheet or MP4 via headless Chromium and `@opencanviz/player`.
- `reference/scenes.md`: every scene, its keys and limits, and the claim table.
- `examples/`: `railhq` (a five-product suite, problem_solution), `pinglet` (a developer API,
  dark), `stridely` (a mobile app, flat), each a `spec.json` plus the `sources.md` it is checked
  against.
