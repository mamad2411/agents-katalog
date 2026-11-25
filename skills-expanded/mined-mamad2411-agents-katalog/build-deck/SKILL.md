---
name: build-deck
description: >
  Phase 8 of the Investor Deck Coach. Renders 04-narrative/slides/NN-*.md plus brand-assets
  into the two deck deliverables: PITCH_DECK.pptx (Microsoft PowerPoint via
  python-pptx) and 04-narrative/DECK.html (Reveal.js via build_html_deck.py). Both
  wear the customer brand. Pre-checks ensure adversarial-review findings are
  addressed and chunk limits respected.
user_invocable: true
---

# Build Deck

When invoked, render the working slide files into the two deliverables.
This skill is mostly mechanical — the substantive work happened in
`/investor-coach:narrative` and `/investor-coach:adversarial-review`. The role here is to
verify pre-conditions, run the build scripts, and walk the result with
the founder.

## When to invoke

- After `/investor-coach:adversarial-review` is complete and the action list is
  resolved (either by slide revisions or by founder acknowledgment of
  residual risk).
- When slide files have changed since the last build.

## When NOT to invoke

- Before adversarial review — shipping a deck that hasn't survived the
  sweep risks the partner meeting.
- When `brand-assets/` is incomplete — the build script will fail.

---

## Execution

### Step 1: Pre-flight checks

Verify before invoking the scripts:

| Check | If fails |
|---|---|
| `brand-assets/tokens.css`, `tokens.json`, `logo.svg`, `type-stack.md` all exist | Return to `/investor-coach:brand-discovery` |
| Every `04-narrative/slides/NN-*.md` has front matter with `headline`, `investor_question`, `layout`, `chunk_count` | Return to `/investor-coach:narrative` |
| Every `chunk_count` in slide front matter ≤ 5 | Return to `/investor-coach:narrative` |
| Every numerical claim references a `pp-NNN` in slide front matter | Return to `/investor-coach:market-research` or `/investor-coach:narrative` |
| `ADVERSARIAL_REVIEW.md` exists and all Weak / None items are either addressed in slides or acknowledged in the report | Return to `/investor-coach:adversarial-review` |
| No `[TODO]` or `[PENDING]` markers in any slide file | Resolve before building |

If any check fails, surface the specific failure to the founder and
propose the corrective skill. Do not proceed.

### Step 2: Confirm slide order with founder

Read each `04-narrative/slides/NN-*.md` headline aloud (in order). Confirm with
the founder that the order matches `NARRATIVE.md`. If the founder
wants to reorder, do it now — the file rename is mechanical, the
build is deterministic.

### Step 3: Run the build scripts

Five scripts run in this phase. The first two render the presenter deck;
the next three render the investor-facing HTML pages shared externally.

**Presenter deck** (for live partner meetings):

```bash
# Microsoft PowerPoint
python3 scripts/build_pptx.py \
    .pitch/{slug}/04-narrative/slides/ \
    .pitch/{slug}/brand-assets/tokens.json \
    .pitch/{slug}/PITCH.yaml \
    .pitch/{slug}/04-narrative/DECK.pptx

# Reveal.js HTML (slide-by-slide, presenter notes view)
python3 scripts/build_html_deck.py \
    .pitch/{slug}/04-narrative/slides/ \
    .pitch/{slug}/brand-assets/tokens.css \
    .pitch/{slug}/PITCH.yaml \
    .pitch/{slug}/04-narrative/DECK.html
```

**Investor-facing HTML pages** (for DocSend-style sharing):

```bash
# Long-form scrollable web pitch (root PITCH.html)
python3 scripts/build_web_pitch.py \
    .pitch/{slug}/04-narrative/slides/ \
    .pitch/{slug}/brand-assets/tokens.css \
    .pitch/{slug}/PITCH.yaml \
    .pitch/{slug}/PITCH.html

# Investor-facing financial summary (root FINANCIALS.html)
python3 scripts/build_investor_financials.py \
    .pitch/{slug}/03-financials/MODEL.yaml \
    .pitch/{slug}/brand-assets/tokens.css \
    .pitch/{slug}/PITCH.yaml \
    .pitch/{slug}/FINANCIALS.html

# Investor-facing adversarial-review summary (root REVIEW.html)
python3 scripts/build_review_html.py \
    .pitch/{slug}/05-adversarial/ADVERSARIAL_REVIEW.md \
    .pitch/{slug}/brand-assets/tokens.css \
    .pitch/{slug}/PITCH.yaml \
    .pitch/{slug}/REVIEW.html
```

All five outputs share the same brand tokens. The presenter deck is for
talking through live; the three root HTML pages are for asynchronous
investor sharing.

The scripts emit warnings to stderr for:

- WCAG AA contrast issues per slide (VD-09)
- Truncated y-axes without annotation (VD-12)
- Body line length over threshold (VD-06)

Surface warnings to the founder. They may be acceptable in context
(e.g., an annotated axis break) but should be conscious decisions.

### Step 4: Concatenate speaker notes

The build scripts emit per-slide notes; concatenate them into
`04-narrative/speaker-notes.md` for printing. Format: one slide per section,
heading is the slide title.

### Step 5: Walk the deck with the founder

Open `04-narrative/DECK.html` and walk slide-by-slide. For each slide:

- Read the headline aloud
- Confirm the visual conveys the takeaway
- Surface any visual issue (overflow, contrast, density)

If issues surface, decide:

- Quick fix → edit the slide source, re-run the build
- Substantive issue → return to `/investor-coach:narrative`

### Step 6: Time check (optional preview)

Without going into full rehearsal, ask the founder to estimate how
long they'd spend on each slide. If the total deviates significantly
from 5/15/30 (target ≈ 25 minutes for the deck, ≈ 25 minutes for
Q&A in a 50-minute slot), flag it for rehearsal.

### Step 7: Transition

Once the founder is satisfied with the rendered deck, propose:

> "Materials are ready. Want me to run a rehearsal? I'll time you
> against the Sequoia 5-15-30 arc, throw 8–10 in-character investor
> questions at you from the adversarial report, and flag the
> answers that landed weak. Takes about 30 minutes."

If accepted, propose `/investor-coach:rehearsal`. If declined, propose
`/investor-coach:validate` as the final check.

---

## What the build scripts do

### `build_pptx.py`

- Reads each `04-narrative/slides/NN-*.md` and its YAML front matter
- Loads `brand-assets/tokens.json` for colour / type / spacing
- Selects the python-pptx layout based on `layout:` front matter
- Renders headline, body, image, chart, and footer (with proof-point
  citation) per slide
- Embeds speaker notes from the `## Speaker Notes` section
- Outputs a single `.pptx` file

### `build_html_deck.py`

- Reads each `04-narrative/slides/NN-*.md` and its YAML front matter
- Loads `brand-assets/tokens.css` and inlines it
- Wraps each slide as a Reveal.js `<section>` with the appropriate
  layout class
- Loads Reveal.js from CDN (single-page, self-contained HTML)
- Speaker notes available via Reveal.js notes view
- Outputs a single `.html` file

Both scripts share the same input shape and respect the same brand
tokens. The .pptx is for partner meetings and DocSend; the .html is
for live presenting and shareable links.

---

## Refusals

Refuse if:

- The founder asks to ship a deck with a chunk_count > 5 slide → "VD-02
  is a delivery floor. Let me split the slide."
- The founder asks to bypass the contrast warnings → "Contrast issues
  show up in partner meetings as 'I couldn't read the chart.' Let me
  fix the pairing."
- The founder asks to ship before adversarial review is addressed →
  "Either we address the Weak rebuttals or we record them as
  acknowledged residual risk. Shipping without either is shipping
  blind."

---

## Coaching gates

- **Show, don't tell:** open the rendered HTML deck and walk it with
  the founder. The deck speaks for itself.
- **Observation vs judgement:** "I notice the financials slide has
  six bullets" beats "this slide is too dense."
- **Respect iteration:** the first build rarely lands perfectly.
  Plan for one or two revision cycles.

---

## Gotchas

- **Don't build with unfilled placeholders.** If any slide has
  `[TODO]`, the build will ship them visibly.
- **Don't skip the founder walkthrough.** Build scripts are
  deterministic, but they don't see what a human sees (image crop
  awkwardness, surprising line breaks).
- **Don't re-run the build after every micro-edit.** Batch edits,
  then build, then walk through.
- **Don't lose speaker notes.** They live in slide files; the build
  preserves them. If the founder edits the slide visual without
  updating notes, notes drift.

---

## Output checklist

- [ ] All pre-flight checks pass
- [ ] `04-narrative/DECK.pptx` written (presenter — PowerPoint)
- [ ] `04-narrative/DECK.html` written (presenter — Reveal.js)
- [ ] `04-narrative/speaker-notes.md` written
- [ ] `PITCH.html` written (investor-facing — long-form web pitch)
- [ ] `FINANCIALS.html` written (investor-facing — financial summary)
- [ ] `REVIEW.html` written (investor-facing — adversarial summary)
- [ ] Build warnings surfaced to founder
- [ ] Founder walked through the rendered deck
- [ ] Founder reviewed `PITCH.html` (the shareable long-form version) and confirmed
- [ ] Visual issues either resolved or recorded
- [ ] Journal entry written (new file in `journal/`)
- [ ] Rehearsal proposed (or `/investor-coach:validate` if declined)
