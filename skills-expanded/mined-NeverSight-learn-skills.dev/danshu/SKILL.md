---
name: danshu
description: >-
  Create restrained Chinese A4 PDF reports, briefs, handouts, and research
  notes in the 丹书 style: warm parchment, vermilion focus, serif hierarchy,
  curved diagrams, data visualization, negative space, and polished PNG exports.
---

# 丹书

丹书 is a Chinese editorial document style built on Kami's restraint: warm paper, one vermilion focus color, serif-led hierarchy, quiet curves, and enough negative space for judgment to breathe.

## Output Contract

Produce, unless the user narrows the scope:

- A4 portrait PDF as the formal deliverable.
- HTML source beside the PDF.
- One PNG per page when the user mentions sharing, screenshots, WeChat, preview, or image output.
- A contact-sheet preview only as QA support, not as the main image deliverable.

Use Chinese by default when the source is Chinese. Keep English only for compact labels such as `FIELD BRIEF · 01` when they add editorial rhythm.

## Visual Tokens

- Paper: `#f5f4ed`
- Card ivory: `#faf9f5`
- Vermilion focus: `#A33A2A`
- Soft vermilion curve: `#DDBBB2`
- Primary text: `#141413`
- Body text: `#3d3d3a`
- Subtext: `#504e49`
- Metadata: `#6b6a64`
- Border: `#e8e6dc`
- Soft grid: `#e5e3d8`

Never use the old Kami ink-blue token in 丹书 output. Vermilion should remain under roughly 5% of the page surface.

## Typography

- Chinese: `TsangerJinKai02` first, then Source Han Serif / Songti fallbacks.
- English fallback: Charter or Georgia.
- Use one serif family per page.
- H1: 26-30pt, line-height 1.08-1.16.
- Section title: 13-15pt, with a thin vermilion left bar or top divider.
- Body: 9.5-10.5pt, line-height 1.42-1.55.
- Tiny metadata: 6.4-7.5pt.
- Avoid synthetic bold, italics, pure white, cool grays, gradients, and heavy shadows.

## Workflow

1. Extract the source faithfully.
   - For PDF input, use `pypdf` text extraction and verify page count.
   - For `.pages`, first try conversion; if unavailable, use the embedded preview only as a fallback and state the limitation.
   - Do not invent statistics. If a number is absent, write a qualitative claim or mark the gap.

2. Distill before layout.
   - Pull out thesis, audience, time window, stakeholders, requirements, scoring, risks, and any quantifiable numbers.
   - Rewrite bureaucratic phrasing into concrete judgment.
   - Remove filler such as “高质量发展”, “赋能”, “全方位”, unless quoted as an anti-example.

3. Choose page count.
   - One-pager: one sharp thesis, 3-5 metrics, one diagram, one conclusion.
   - 3-page brief: page 1 thesis + key metrics; page 2 structure/topic map; page 3 decision/scoring/next action.
   - Longer reports: use chapters only when each page can reach 60-80% useful density.

4. Visualize only where the diagram teaches faster than prose.
   - Assign a semantic role before drawing any curve: time, route, flow, comparison, grouping, attention, or boundary.
   - Do not reuse the same curve silhouette across adjacent pages. Vary direction, amplitude, openness, and anchoring only when the meaning changes.
   - Time ranges: mostly horizontal, low-amplitude curve or stepped timeline.
   - Options or topics: card map with separate local arcs, bracket curves, or enclosure paths; avoid one repeated wave behind every card.
   - Process: S-curve or stepped path with numbered anchors. Keep each number physically paired with its text.
   - Comparison: use split baselines, opposing arcs, or bar structure; do not use a decorative flow curve.
   - Spatial fieldwork or route tasks: use a route line, map-like path, or checkpoint path instead of a generic S-curve.
   - Scoring or weights: stacked horizontal bar.
   - Category comparison: restrained bar chart.
   - Proportions: donut only when the parts sum to 100 and there are <= 6 parts.

5. Typeset with negative space.
   - Leave one quiet zone per page.
   - Keep cards rectangular with radius <= 8pt.
   - Use curves as structure, not decoration; if removing the curve does not change comprehension, replace it with a divider, grid, bracket, or empty space.
   - Let text overlap a pale curve if needed, but never separate numbered dots from their labels.

6. Verify visually.
   - Render each page to PNG.
   - Inspect full page and zoomed details for: title overlap, curve/text collisions, right-edge overflow, card crowding, footer collisions, and stray old blue.
   - Export page PNGs at 2K-4K long edge when requested.

## Writing Rules

- Prefer “这份作业不是写一篇……” over “这份作业不是让学生写一篇……”.
- Replace abstract nouns with observable behavior.
- Every page should contain at least one sentence of judgment, not just a list of facts.
- For education documents, write for students first and administrators second.
- Keep one final sentence that the reader can remember.

## Embedded Layout Reference

Use this root-level `SKILL.md` as a self-contained TRAE/Codex-compatible version. Do not assume supporting files are installed.

### Core Patterns

- Opening page: one judgment-led title, one short thesis paragraph, one restrained metric block, one quiet curve or timeline.
- Structure page: use 2-4 cards, a comparison pair, or a route map. Cards should clarify categories, not decorate fragments.
- Decision page: use numbered questions, a scoring bar, or a next-action ladder. Keep the final conclusion isolated with negative space.
- Fieldwork or class handouts: foreground who does what, when, with what evidence, and how it will be judged.

### Curve Grammar

- Give every curve a job before drawing it: time, route, flow, comparison, grouping, attention, or boundary.
- Vary curves across pages. Repeating the same soft wave creates mannerism, not structure.
- Time: use a mostly horizontal, low-amplitude curve or stepped timeline.
- Process: use an S-curve or checkpoint path; each numbered dot must sit physically near its label.
- Comparison: prefer split baselines, opposing arcs, or bars. Avoid using a decorative wave where a bar chart would explain better.
- Spatial or fieldwork tasks: use map-like routes and checkpoints.
- If a curve can be removed without changing comprehension, replace it with a divider, bracket, grid, or empty space.

### Chart Choices

- Time series: soft line or stepped timeline.
- Ratios and weights: stacked horizontal bar.
- Category comparison: restrained bar chart.
- Proportions: donut only when parts sum to 100 and there are six or fewer parts.
- Relationships: small flow map, bracket, or paired cards.

### Final QA

- Confirm page count, file names, and requested export formats.
- Render every page to PNG before delivery.
- Check title overlap, right-edge overflow, curve/text collisions, card crowding, footer collisions, and stray old blue.
- Confirm vermilion remains a focus color rather than a dominant background.
- For TRAE-installed use, keep all critical instructions inside this file.
