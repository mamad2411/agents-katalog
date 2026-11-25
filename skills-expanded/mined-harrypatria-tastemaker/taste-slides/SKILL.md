---
name: taste-slides
description: Builds strategic HTML presentations - pitch, QBR, strategy, launch, sales, training, status - with takeaway titles, one idea per slide, token theming, Chart.js data slides, speaker notes, keyboard/touch navigation, overview mode and clean print-to-PDF, from a ready template. Use for "slides", "deck", "presentation", "pitch deck", "board update", "turn this report into slides".
---

# Taste Slides: every title is a takeaway

Reads `brand-guidelines.md` and `design-tokens.json`. If the environment has a native deck type, or the user asks for .pptx, use that and apply the same narrative and copy rules.

## Procedure

1. **Intake** (infer; ask max 2 questions): purpose, audience and the decision they must make, time limit, desired action at the end, supplied data, delivery mode (live, async, both). Budget 1-2 minutes per content slide.
2. **Narrative**: pick a structure from `references/narratives.md`. Open with the answer or the ask (pyramid principle).
3. **Outline as titles only**: each title a full-sentence takeaway ("Churn fell 18% after the onboarding change"), never a topic label ("Churn"). Read the titles alone: they must tell the whole story. Show this outline before building when the deck has 8+ slides.
4. **Archetype per slide** from the layout library; one idea, one focal point.
5. **Build** from `templates/deck.html` (keyboard, touch, notes, overview, print, reduced motion already wired). Fill tokens, slides, `data-notes`, chart data.
6. **Check** the gate below; produce `notes.md` (talk track, transition, likely question with answer, data source per slide).

## Limits

At most 30 words per slide (async: 60), 3 bullets of at most 12 words, 1 chart, 2 fonts and 2 weights. Minimum text 18px at the 1920x1080 artboard; body 28-32px; titles 56-72px. Margins 96px; 12-column grid; whitespace at least 30%.

## Charts

Type by question (taste-direction dataviz). Chart.js: `responsive: true`, `maintainAspectRatio: false` in a fixed-height box; colors read from CSS variables at init so themes work; labels at least 16px; light horizontal grid only; direct labels; one highlighted series; annotate the takeaway; `Intl.NumberFormat`; `<canvas role="img" aria-label="<takeaway>">` plus a visually hidden data table. Standard mode: pinned CDN version. Portable Mode: vendored file or inline SVG. No data supplied: label as illustrative sample in a footnote and in notes. Never invent metrics, customers, logos or quotes.

## Quality gate

- [ ] First slide states the answer or ask; last slide asks for one action.
- [ ] Titles alone tell the story; each is a takeaway sentence.
- [ ] One idea and one focal point per slide; word limits met; 18px minimum.
- [ ] Charts match their question, labelled, annotated, accessible, token-colored, real data.
- [ ] Keyboard, touch, overview, notes and print-to-PDF work; reduced motion honoured.
- [ ] Tokens only; contrast verified; no emoji, no third-party marks; speaker notes and sources included.
