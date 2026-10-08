---
name: carousels
description: "Turns a piece of Craig's content (an email, a YouTube script, an essay, or pasted text) into a polished image carousel publishable to both LinkedIn and Instagram from one set of 1080x1350 slides. Distills the source into 5-8 one-idea-per-slide beats, generates hand-drawn infographic illustrations with GPT Image (OpenAI), renders pixel-perfect on-brand slides via headless browser, assembles a LinkedIn PDF, and writes a caption. Triggers: 'make a carousel,' 'carousel from this email/script,' 'turn this into LinkedIn slides,' 'Instagram carousel from X.' Brand is locked to context/brand/03-visual-identity.md — output is identical styling every run."
---

# LinkedIn + Instagram Carousel Generator

Turn one strong piece of source content into a swipeable image carousel. One set of
4:5 slides serves both platforms — PNGs for Instagram, an assembled PDF for LinkedIn.

The brand is **locked**, not configurable: off-white `#F5F1E8`, ink `#0F0F0F`, muted
teal `#2A6F6A`, Inter type, hand-drawn infographic illustrations. Every run comes out
visually identical. Don't ask the user about themes, colors, or fonts.

Skill files (paths relative to repo root `/Users/craighewitt/Coding/second-brain`):
- `output/cowork-context/skills/carousels/assets/carousel.css` — brand stylesheet
- `output/cowork-context/skills/carousels/references/slide-layouts.md` — HTML patterns
- `output/cowork-context/skills/carousels/scripts/generate-image.mjs` — GPT Image (OpenAI)
- `output/cowork-context/skills/carousels/scripts/render.mjs` — slides → PNG + PDF

---

## Phase 0 — Preflight

Run these checks before anything else. If a check fails, surface the fix and stop
until it's resolved — don't proceed with a broken environment.

1. **Node** — `node -v` (need v18+; repo has v22).
2. **Headless browser** — `render.mjs` launches puppeteer. If puppeteer or its
   browser is missing, the script prints the install command. Don't pre-empt it;
   just run the render step and act on any error.
3. **OPENAI_API_KEY** — only needed if the carousel will have image slides. Check
   with `[ -n "$OPENAI_API_KEY" ] && echo set || echo missing`. If missing, tell
   the user:
   > GPT Image (OpenAI) needs an OpenAI API key. Create one at
   > platform.openai.com/api-keys, add billing, then run
   > `export OPENAI_API_KEY="sk-..."` in your shell (never commit it).

   If the user can't set a key right now, offer to build a **type-only carousel**
   (no image slides) — the skill still works fully without the key.

---

## Phase 1 — Intake

Get the source content. Accept either:
- **Pasted text** — an email, a section of a script, notes.
- **A local file path** — e.g. a script in `output/`, an essay draft.

Do **not** scrape URLs. If the user gives a URL, ask them to paste the content
(per `CLAUDE.md`).

Then read, once:
- `context/brand/02-voice.md` — for the caption voice.
- `context/brand/03-visual-identity.md` — confirm brand-surface palette/type.

Ask the user only for things that genuinely change the output (one short batch):
- Any specific **angle** to pull from the source? (optional)
- A **CTA word** for the final slide — what should people comment? (optional;
  default to a relevant word from the topic)
- A **lead magnet** to point to? (optional)

If the user already gave direction in their prompt, skip the questions.

Create the run folder: `output/carousels/<source-slug>-<YYYY-MM-DD>/` with
`images/` and `publish/` subfolders. Copy `carousel.css` into the run folder
(render needs it next to `slides.html`).

---

## Phase 2 — Editorial pass

This is the hard part — carousels live or die on editing, not rendering.

Distill the source into **5-8 beats, one idea per slide**. Let the source decide
the count: a tight 4-tip article is 7 slides; a dense essay might be 8. Never pad.

Structure:
- **Slide 1 — cover/hook.** The scroll-stopper. A promise or a provocative claim.
- **Slides 2 to N-1 — content.** One idea each. No slide explains two things.
- **Slide N — CTA.** Save / follow / comment-the-word.

For each content slide decide: is it **type-only** or an **image slide**? Image
slides are for ideas that are clearer drawn than written — a process, a
relationship, a before/after, a system. Aim for **2-4 image slides**, not every
slide. Type-only slides use the big-stat, steps, quote, comparison, or statement
layouts.

Write `01-slide-plan.md` in the run folder: for each slide, its number, role,
layout, one-line idea, and image/type-only flag.

---

## Phase 3 — Slide copy

Write the visible copy for every slide. Rules:
- Headline ≤ 12 words. Body ≤ 30 words. Social attention is short.
- One idea per slide — if copy needs two sentences of setup, split into two slides.
- Craig's voice: direct, practical, no hype, no "crushing it / game-changer."
- The cover earns the swipe; the CTA asks for the save + comment word.

---

## Phase 4 — Image generation

For image slides only. Skip entirely if building a type-only carousel.

For each image slide, write a two-paragraph prompt:

**Paragraph 1 (locked — brand illustration style, paste verbatim):**
> Hand-drawn minimalist infographic, black ink linework on a solid flat warm
> off-white background (hex #F5F1E8), single muted teal accent color (#2A6F6A),
> clean whiteboard sketch style, confident pen strokes, hand-lettered text, simple
> geometric icons, lots of white space.

**Paragraph 2:** describe the specific diagram — the concept, layout, labels, and
flow for that slide. Be concrete ("a 3-step horizontal flow: Draft → Review →
Publish, each a labeled box connected by arrows"). No stock-photo realism, no
gradients, no people. **Always end paragraph 2 with:** "The entire diagram,
including every icon and label, sits well within the frame with generous empty
margins on all four sides — nothing is cropped and nothing touches the edges."
The model otherwise tends to draw edge-to-edge and clip the outer labels.

Generate each one:
```
node output/cowork-context/skills/carousels/scripts/generate-image.mjs \
  --prompt-file <run>/images/slide-04-prompt.txt \
  --out <run>/images/slide-04.png
```
Write the prompt to a `.txt` file first to avoid shell-escaping issues. After
generating, the script **normalizes the image background to exactly `#F5F1E8`**
(the `--bg-hex` default) so the illustration sits seamlessly on a light slide —
no visible panel edge. Default size `1024x1024`, quality `medium`. Name each PNG
`slide-NN.png` matching its slide number. Because the linework is black, image
slides must use the light slide background, not the teal variant. (If you ever
need an image slide on a different background, pass `--bg-hex #RRGGBB` to match.)

---

## Phase 5 — Build slides.html + sample approval

Author `<run>/slides.html` using the patterns in `references/slide-layouts.md`.
One `.slide` div per slide, in order. Link `carousel.css` (the copy in the run
folder). Reference illustrations as `images/slide-NN.png`.

**Sample-approval checkpoint:** before rendering the whole set, render just the
cover so the user sees the styling:
```
node output/cowork-context/skills/carousels/scripts/render.mjs \
  --slides <run>/slides.html --out <run>/publish
```
Show the user `publish/slide-01.png`. If they want changes (copy, layout), edit
`slides.html` and re-render. Only continue once the cover is approved.

---

## Phase 6 — Render

Run the full render (same command as above — it renders every `.slide`):
```
node output/cowork-context/skills/carousels/scripts/render.mjs \
  --slides <run>/slides.html --out <run>/publish
```
Produces `publish/slide-01.png … slide-NN.png` (Instagram) and
`publish/carousel.pdf` (LinkedIn). All PNGs are exactly 1080×1350.

---

## Phase 7 — Caption

Write `publish/caption.md` with a caption that works for both platforms:
- **Hook line** that mirrors the cover slide.
- **2-4 short lines** of value — what the carousel teaches, why it matters.
- **CTA**: save the post, follow @thecraighewitt, comment the CTA word.
- Craig's voice. No hashtag soup — 3-5 relevant tags max at the end, optional.

If a LinkedIn vs Instagram split is worth it (different length/tone), write both
under clear headings. Otherwise one shared caption is fine.

---

## Phase 8 — Review + delivery

Open the rendered PNGs and check each against the brand:
- Only `#F5F1E8` / `#0F0F0F` / `#2A6F6A` (plus rare `#C75A2C` data callout).
- Inter only. No gradients, no drop shadows, no emoji in slide chrome.
- One teal element per slide.
- One idea per slide; text legible at phone size.
- Footer (handle + number) on every slide except the cover.
- Slide numbers in footers match actual count (`03 / 07`).

Fix any off-spec slide in `slides.html` and re-render. Then report the run folder
and tell the user: upload the PNGs to Instagram as a carousel, upload
`carousel.pdf` to LinkedIn as a document post, use `caption.md` for both.

Final deliverables in `output/carousels/<slug>-<date>/publish/`:
- `slide-01.png … slide-NN.png`
- `carousel.pdf`
- `caption.md`
