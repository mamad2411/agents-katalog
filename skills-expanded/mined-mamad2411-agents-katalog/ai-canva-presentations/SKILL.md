---
name: ai-canva-presentations
description: >-
  Build a professional-looking presentation (pitch deck, client proposal, course intro, monthly
  client report, or internal team deck) fast, using a Claude-structures → Canva-builds → polish
  workflow — a full 12-slide deck in roughly 26 minutes with no designer. Use when the user asks
  for a presentation, pitch deck, slide deck, Canva presentation, or client proposal deck, or says
  things like "make me a deck," "build a pitch deck," "turn this into slides," or "I need a
  presentation for [audience]." Covers the exact structuring prompt, when to drive Canva directly
  via the Canva connector vs. handing off a paste-ready structure, the slide archetypes that always
  work (cover/content/data/CTA), the one-idea-per-slide discipline, presenter tools (speaker notes,
  Q&A polling, PPTX export), and a timing checklist to sanity-check the build isn't running long.
metadata:
  version: 1.0.0
---

# AI Canva Presentations

Source: a TikTok carousel by @earchoe ("AI Canva · Carousel 14 of 21") on building agency-quality
decks with Claude + Canva. Original content authored for this repo from that carousel — not a
vendored code repo.

The core claim, and the reason this workflow beats opening a blank PowerPoint: **AI generates the
structure and the layout; the human's only job is the message and the polish.** Splitting those two
jobs across two tools — Claude for narrative structure, Canva for visual generation — is faster and
more consistent than asking one tool (or a human) to do both at once.

## The 3-step workflow

**Step 1 — Claude structures.** Do not open Canva first. Get the structure locked here, using this
exact template (fill the brackets, keep the constraints — they're load-bearing, see "The one
mistake to avoid" below):

> Build a **[pitch deck / proposal / course intro / client report / internal deck]**.
> Topic: **[topic]**. Audience: **[who]**. Goal: **[outcome]**.
> Give me: 1) a 12-slide structure with a title per slide, 2) a key message per slide (1-2
> sentences, one idea only), 3) the best visual type per slide (cover / content / data / CTA — see
> slide archetypes below).

Output this as a numbered slide-by-slide list — title, key message, visual type — not prose. This
list is what gets handed to Canva next.

**Step 2 — Canva builds.** Two paths, pick based on what's available in the session:

- **Canva connector is live (`mcp__Canva__*` tools present):** drive it directly instead of asking
  the user to paste anything by hand.
  1. Call `mcp__Canva__request-outline-review` with `design_type` implied by `presentation`,
     mapping each item from Step 1 into a `pages` entry (`title` = slide title, `description` = the
     key message as hyphen bullets, one idea only — do not let this tool's own summarization
     re-merge slides). Set `length` to match the slide count (12 slides → `balanced`). If the user
     has a brand kit, call `mcp__Canva__list-brand-kits` first and pass `brand_kit_id`.
  2. This surfaces an outline-review widget — wait for the user's actual approval before
     continuing. If they ask for changes, update `pages` and call `request-outline-review` again.
     Never call `generate-design-structured` on an unapproved or guessed outline.
  3. Once approved, call `mcp__Canva__generate-design-structured` with the same approved
     `presentation_outlines`.
  4. To hand back a file instead of a live Canva link, check `mcp__Canva__get-export-formats` for
     the design, then `mcp__Canva__export-design` (`pptx` for PowerPoint, `pdf` otherwise).
- **No Canva connector this session:** hand off a paste-ready block instead of a live build. Format
  Step 1's output as one line per slide (`Title — key message — visual type`) under a header that
  says "paste this into Canva → Magic Design → select Presentation format," and give the user the
  Step 3 polish list below to do by hand. Don't claim you built the deck if you only produced the
  structure.

**Step 3 — Polish.** Whichever path built the shell, finish it:
- Replace any placeholder copy with Step 1's actual key messages, verbatim, not paraphrased.
- Generate on-brand images per slide with Canva's Dream Lab (image-generation tool inside Canva) —
  don't leave stock-photo placeholders on content slides that need a real visual.
- Data slides: let Canva's Magic Charts generate the chart from the real numbers, then Magic Write
  to draft the one explanatory sentence — don't hand-build charts.
- Run brand colors/fonts pass last, after content is final — don't polish copy that's about to move.

## The one mistake to avoid

**Filling every slide with all the information.** The AI defaults to density unless explicitly
constrained — always brief it with "one key message per slide" and "no more than 3 bullet points."
Great presentations are sparse: one bold statement, one supporting visual, one actionable takeaway
per slide. Everything else (the caveat, the extra stat, the citation) belongs in the speaker notes
or a follow-up document, not on screen — a slide covered in text loses the audience, who read
instead of listening. Enforce this at Step 1 (in the prompt) and again at review (cut, don't shrink
the font).

## Slide archetypes that always work

Pick one of these four per slide in Step 1 — don't invent a fifth without a reason:

| Archetype | Contents | Notes |
|---|---|---|
| **Cover** | One bold title. One subtitle. Logo. Full-bleed image or solid color. Nothing else. | Sets the tone — the most common failure is overcrowding the cover. |
| **Content** | One key message as a large headline. Up to 3 supporting bullets. One supporting image or icon. | Covers ~80% of all slides in a well-built deck. |
| **Data** | One key number, large and central. One sentence explaining what it means. | Magic Charts generates the chart; Magic Write explains it. |
| **CTA** | One action. One contact detail. One QR code or link. | The last slide decides what happens next — one ask, zero friction. |

## The 5 presentation types this workflow fits best

1. **Pitch decks** — problem, solution, market, product, traction, team, ask. Canva carries the
   visual storytelling; Claude (Step 1) structures the narrative arc.
2. **Client proposals** — what you do, what you've done, what you'll do for them, what it costs.
   Aim for "premium deliverable," not a generic template.
3. **Course/module introductions** — welcome slide, learning objectives, module overview,
   instructor bio. The goal is setting tone fast, not depth.
4. **Monthly client reports** — build the report shell once as a template, then only the data
   changes month to month; Canva's data tools + Canva Sheets can pull numbers into charts
   automatically on repeat builds.
5. **Internal team presentations** — strategy updates, onboarding decks, quarterly reviews. Use a
   brand kit so these look company-standard every time without a manual pass.

Anything else (a single powerful claim, a live product demo, a dense technical spec) is probably a
worse fit for this workflow — say so rather than forcing it into 12 slides.

## Presenter tools beyond the slide deck

Mention these when the deliverable includes presenting live, not just handing over a file:

- **Presenter View** — speaker notes visible to the presenter only, audience sees just the slides;
  works in any browser, no separate software.
- **Speaker notes via Magic Write** — per slide: "Write speaker notes for this slide: [paste slide
  content]." Full notes in seconds; don't write these by hand if Magic Write is available.
- **Live Q&A / polling** — Canva's live-presentation mode lets the audience submit questions or vote
  from their phone, no separate app.
- **PPTX export** — any Canva presentation exports to `.pptx` for clients who need PowerPoint
  specifically (`mcp__Canva__export-design` with `format.type: "pptx"`, after confirming support via
  `get-export-formats`).

## Timing checklist — sanity-check the build

Rough benchmark for a professional 12-slide deck, ~26 minutes total. If any step is running well
past its budget, that's a signal to simplify rather than push through:

| Step | Budget |
|---|---|
| Claude — structure + key messages (Step 1) | 5 min |
| Canva — generate all slide layouts (Step 2) | 3 min |
| Fill copy + adjust to brand | 10 min |
| On-brand images for key slides (Dream Lab) | 5 min |
| Speaker notes (Magic Write) | 3 min |

## Quality bar — self-check

- Does Step 1's output have exactly one key message per slide, ≤3 bullets, and a named visual
  archetype (cover/content/data/CTA) — not a wall of text?
- Did Step 2 actually build in Canva (via the connector) when it was available, rather than
  defaulting to a manual hand-off the user didn't ask for?
- Is every slide's copy the real key message from Step 1, not leftover placeholder text?
- Do data slides carry one number + one sentence, not a dense table?
- Does the last slide give one unambiguous action?
- If presenting live matters, were speaker notes and presenter tools actually offered, not just the
  static deck?

## Related skills

- `pptx` — when the deliverable must be an editable native PowerPoint file rather than a Canva link.
- `premium-html-presentation`, `the-design-system-prompt` — cinematic HTML decks, for when Canva
  isn't the right tool (e.g. the deck needs to live as a code artifact, not a Canva file).
- `brand-guidelines` — Anthropic-specific brand application; for other brands use the user's own
  Canva brand kit via `mcp__Canva__list-brand-kits`.
- `carousel-writer` — same one-idea-per-slide discipline, applied to social carousels instead of
  presentations.
- `design-review-audit` — audit the finished deck against a general design-quality checklist.
