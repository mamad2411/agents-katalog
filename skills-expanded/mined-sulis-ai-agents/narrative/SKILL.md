---
name: narrative
description: >
  Phase 6 of the Investor Deck Coach. Assembles the Sequoia spine with the
  stage-appropriate variant, applies Pyramid + SCQA per slide, and produces
  NARRATIVE.md plus one slides/NN-*.md file per slide with front matter
  (investor-question, layout, proof-point references, chunk count). All
  numerical claims trace to proof-points; all titles are conclusions.
user_invocable: true
---

# Narrative

When invoked, compose the deck's story arc and individual slide working
files. The narrative is the bridge between research/financials and the
build step — slides written here are what `/investor-coach:build-deck` renders.

## When to invoke

- After `/investor-coach:market-research` PASS and `/investor-coach:financial-model` complete.
- When restructuring an existing pitch (e.g., founder shifts target
  audience).

## When NOT to invoke

- Before research or financials are complete. The narrative grounds in
  proof-points; if they don't exist, the narrative invents.
- During Phase 7 (adversarial sweep) — revise narrative AFTER the
  sweep, not during.

---

## Execution

### Step 1: Read stage and select variant

Read `PITCH.yaml` `stage`. Apply the variant from
`sequoia-pitch-framework.md`:

| Stage | Variant | Heaviest slides |
|---|---|---|
| Angel / Pre-seed | SQ-V1 | SQ-01 What's Changed, SQ-09 Team |
| Seed | SQ-V2 | SQ-05 Pain, SQ-06 Solution |
| Series A | SQ-V3 | SQ-07 Market, SQ-10 Financials |
| Series B | SQ-V4 | SQ-03 Fast Facts, SQ-10 Financials |

The variant determines how much real-estate each slide gets in
content depth — not whether the slide exists.

### Step 2: Write NARRATIVE.md first (ND-07)

**Compose the arc before composing individual slides.** Use the
`NARRATIVE.md` template:

1. One-sentence pitch
2. Opening hook (Slides 1–4) — title + investor question + speaker
   plan + proof-points per slide
3. Core argument (Slides 5–7)
4. Evidence build (Slides 8–10)
5. The close
6. Planned Q&A redirects (top 3 anticipated objections — IO-NN refs)
7. Appendix slide list
8. Coherence check — read slide titles in sequence and confirm they
   convey the pitch

Walk the arc with the founder. Iterate. **Lock the arc before writing
slides.**

### Step 3: Compose individual slides

For each slide (`slides/01-whats-changed.md` through
`slides/10-financials.md`):

1. Use the `slide.md.template`.
2. Set front matter:
   - `slide_id`, `slide_role` (SQ-NN), `layout`
   - `headline` — a **conclusion**, not a label (ND-02, ND-04)
   - `investor_question` — exactly one (ND-01)
   - `proof_points:` — list every `pp-NNN` cited on the slide
   - `chunk_count:` — total visible chunks (must be ≤ 5, VD-02)
3. Write the slide body:
   - 3–5 bullets OR a single visual OR a chart with takeaway caption
   - No "About us" sections
4. Write speaker notes (≤ 80 words, bullet form):
   - Talking points
   - Source citation ("pp-NNN states …")
   - Verbal transition to next slide (ND-08)
5. For argument slides (SQ-01, SQ-05, SQ-08), include the SCQA section
   in the slide file (ND-03).

### Step 4: Enforce voice (PL / ND-10)

Grep slide titles and bodies for prohibited words:

```
revolutionary | disruptive | unprecedented | game-changing |
best-in-class | cutting-edge | world-class | amazing | incredible |
leading | innovative (as adjective without specification)
```

Replace each with the specific underlying claim + metric. If the
claim cannot be specified, cut it.

### Step 5: Term-consistency sweep (ND-09)

Cross-reference every term used in slides against `GLOSSARY.md`. When
a term in a slide doesn't match the glossary, fix the slide (or, if
the slide use is correct and the glossary is stale, update the
glossary).

### Step 6: Claim-to-proof traceability (ND-05)

Walk every numerical claim on every slide. Verify each maps to a
`proof-points/pp-NNN-*.md` listed in the slide's front matter. If a
claim has no proof-point — return to `/investor-coach:market-research` or cut
the claim.

### Step 7: Headline-only coherence check

Read the slide headlines in order:

> Slide 01 headline → Slide 02 headline → … → Slide 10 headline

A reader who sees only the headlines should be able to summarise the
pitch. If headlines don't string together, fix them (typically the
slide is doing too many things, or the title is a label, not a
conclusion).

### Step 8: Transition

Walk the slide titles with the founder. Then propose
`/investor-coach:adversarial-review`.

---

## Layout-to-content mapping

| Layout | Use for | Content shape |
|---|---|---|
| `title` | SQ-01 What's Changed, SQ-02 What You Do, the close | Large headline, optional one-line subtitle |
| `title-content` | Most slides | Headline + 3–5 bullets OR one supporting visual |
| `two-column` | Pain/Solution comparison, Before/After | Two parallel panels |
| `full-image` | Product visuals, founder photos | Image-led, headline overlaid or above |
| `chart` | Market sizing, financials | Chart + takeaway caption |
| `quote` | Customer pain (SQ-05) | Single customer quote + attribution |
| `team` | SQ-09 Team | 1–4 founder cards |
| `comparison-matrix` | SQ-08 Competition | 2×2 positioning matrix or feature comparison |

Layout is chosen for the content, not the other way around.

---

## Refusals

Refuse if:

- The founder asks for a "vision" slide separate from the rest → "If
  vision belongs anywhere, it's in SQ-01 What's Changed. A separate
  vision slide usually means the pitch hasn't decided what it's
  selling."
- The founder asks for a topic-label title ("Market") → "The title is
  the takeaway, not the topic. Let's write what you want them to
  remember."
- The founder asks to put a number on the slide that has no
  proof-point → "Either we source it or we cut it. I won't ship a
  deck with unsourced numbers."

---

## Coaching gates

- **Show, don't tell:** when a slide is dense, count the chunks
  visibly with the founder. CL-01 makes itself.
- **Offer alternatives:** when a title is a label, propose two
  conclusion-style alternatives. Let the founder choose.
- **Respect iteration:** narrative is the most-revised artifact.
  Founders often need 2–3 rounds before the arc clicks. Don't rush.

---

## Gotchas

- **Don't compose slides before NARRATIVE.md is locked.** The arc
  must be coherent first; slides without an arc become a feature
  list.
- **Don't allow chunk count > 5 to ship.** Visual density is a deck
  killer.
- **Don't bury the ask.** SQ-10 ends with the ask in plain language.
- **Don't write 10 slides without checking SQ-14 (slide count
  discipline).** If the deck is naturally 11–15 slides, that's fine;
  if it's 20+, the appendix needs to absorb some of them.

---

## Output checklist

- [ ] `NARRATIVE.md` complete and reviewed with founder (ND-07)
- [ ] One `slides/NN-*.md` per spine slide (10 minimum)
- [ ] Every slide has front matter with `investor_question`, layout, proof-points, chunk_count
- [ ] Every headline is a conclusion, not a label (ND-02, ND-04)
- [ ] Argument slides have SCQA blocks (ND-03)
- [ ] Every numerical claim linked to a proof-point (ND-05)
- [ ] No slide exceeds 5 chunks (ND-06)
- [ ] Speaker notes contain verbal transitions (ND-08)
- [ ] Term consistency verified against GLOSSARY.md (ND-09)
- [ ] No prohibited PL words (ND-10)
- [ ] Speaker notes ≤ 80 words, bullet form (ND-11)
- [ ] Headline-only coherence check passes
- [ ] Next step (`/investor-coach:adversarial-review`) proposed
