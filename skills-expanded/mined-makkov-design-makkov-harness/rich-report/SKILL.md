---
name: rich-report
description: Use whenever the result of a task is a research, analysis, comparison, plan, roadmap, audit, strategy, recommendation or any multi-section deliverable meant to be read, even if the user did not ask for an artifact. Turns it into a polished, interactive, landing-page-grade Artifact page (real tables, charts, timelines, navigation, icons, simplified explanations) and, on revisions of the same topic, edits the existing artifact in place instead of creating a new one. Triggers on research results, research, breakdown, compare, make a plan, roadmap, audit, strategy, report, brief, analysis, comparison, plan.
---

# Rich report: deliverables as presentable Artifact pages

Every substantial deliverable should look like a designed product page, not a formatted text dump. This skill is the content layer. The technical page contract (CSP, themes, mobile, title, icon) comes from the built-in `artifact-design` skill. Load that first, then follow this one. Where they conflict on how much design effort a plan or memo deserves, this skill wins: installing it is a request for the full treatment.

## When to apply

Apply to: research results, comparisons, plans and roadmaps, audits, strategies, recommendations, any report with several sections or any table of data.

Do not apply to: short answers, quick explanations, code changes, command output, yes/no questions. Those stay in chat. If unsure, ask yourself whether the result has 3+ sections or a table; if yes, apply.

## Step 0: one artifact per topic (do this before creating anything)

Revisions must edit the existing artifact, not create a new one.

1. Check whether this session already published an artifact on this topic. If yes, this request is a revision, whatever the wording ("the inputs changed", "add", "recalculate", "also consider", "make it shorter").
2. Revise with `Edit` on the same local file, then call `Artifact` with the same `file_path` (and the `url` if known). Never write a second file for the same topic. Keep the `<title>` unchanged.
3. Update content everywhere the changed input flows (numbers, charts, TL;DR, recommendations), not only the paragraph the user mentioned. Add or refresh a small "What changed" block near the top (date plus 2-4 bullets). Keep only the latest few entries.
4. Create a new artifact only when the topic is genuinely different, or the user asks for a separate version.
5. If the session was resumed and the file is gone, find the artifact with `Artifact` action `list`, read it, and update it by `url`. If you cannot tell whether a topic matches, ask in one short line.
6. Name the local file after the topic (for example `traffic-channels.html`) and keep that name for the whole session.

## Build process

1. Load `artifact-design` (page contract). Load `dataviz` when there are charts. Load `artifact-capabilities` only if the page must store input or live data (rare for reports).
2. Pick the structure before styling (see Anatomy).
3. Map each piece of content to the right component (see table). Prefer showing over describing.
4. Use the house style below. Start from `skeleton.html` in this skill folder: copy its tokens, fonts and component CSS as they are, replace the sample content, delete components the content does not need. Do not invent a new palette or font pair per topic. Keep the two `impeccable-disable` comments at the top of `<style>`: without them the Impeccable design hook reports false contrast failures (it mixes the light and dark tokens) and false cramped padding (it ignores the padding on table cells) on every page. Because the padding check is off, give any new bordered or filled component you add at least 12px of padding yourself.
5. Write the file, take one preview look if the session offers one, fix what it shows, publish.
6. Reply in chat with the link and 2-3 lines: the main conclusion and what to look at first. Do not paste the report into chat.

## House style (fixed for this harness)

Linear-inspired: neutral black-and-white surfaces with Linear's lavender-blue accent, minimal, precise, fintech/IT. Reference: getdesign.md/linear.app/design-md. This look is the harness default, so it overrides the generic advice in `artifact-design` to vary palette and fonts per subject, including its warning about common fonts.

- **Surfaces**: dark theme follows Linear's surface ladder (canvas `#010102`, surfaces `#0f1011` to `#18191a`, hairlines `#23252a`, text `#f7f8f8`); light theme is the same ladder inverted (canvas `#fbfbfc`, white cards). Never use true black `#000` as the dark canvas.
- **Accent**: Linear lavender-blue `#5e6ad2` (as text, links and icons on dark use `#828fff`, in the starter as `--accent-text`). It is the only chromatic color, and it is used sparingly but visibly, only for marks: the recommended or key row marker, the key bar in a chart, the active item and icon in the contents rail, takeaway icons, timeline dots, links, the "recommended" pill, the report ID chip, focus rings. Never as a page, section or card background, never as a large fill, never a second accent hue.
- **Status color** (green, amber, red) appears only as a small dot inside a pill or as a severity mark, never as a fill, background or heading color.
- **Depth**: hairline 1px borders and the surface ladder. No drop shadows, no gradients, no glow, no decorative blobs. In dark mode a 1px top edge highlight (`--edge`) on cards.
- **Type**: Onest (free Google Fonts grotesk with wide script coverage, close to Linear's own face; Inter is avoided because the Impeccable design hook flags it as overused) at 400, 500, 600 only, never 700+. Display headings 600 with strong negative tracking (about -0.035em at hero size, -0.025em for section headings), body 15px, captions 12-13px. JetBrains Mono only for IDs, dates and code tokens. Numbers use tabular figures.
- **Shape**: radius 8px for controls, 12px for cards and tables, pill only for chips, tabs and status pills. Spacing on a 4px grid, about 80px between sections.
- **Voice of the page**: dense, calm, left-aligned, no centered hero, no marketing flourish. The content (tables, charts, timelines) is the protagonist.
- **Charts**: grayscale ramp with the key value in the accent. Add status colors only when the color itself carries meaning.
- **Variation between reports** comes from structure and content (which components, diagrams, units, terms of the subject), not from changing the palette or fonts.

## Anatomy of a page

- **Header**: name of the work, one-line subtitle (what question it answers), date, status or scope chips.
- **Key takeaways**: 3-4 cards right under the header with the answer, so a skimming reader gets the result in 10 seconds.
- **Navigation**: sticky side table of contents on desktop, horizontal chip bar on phone, with the current section highlighted.
- **Sections**: each opens with a heading that states the conclusion, then a one-sentence plain summary, then the evidence (table, chart, diagram), then optional details collapsed.
- **Closing sections** when relevant: risks, assumptions, open questions, sources, next steps.

## Content to component

| Content | Component |
|---|---|
| Table of data | Real `<table>` in a scroll container: sticky header, sortable columns, filter or search when 8+ rows, numeric columns right-aligned with tabular numbers, status as colored pills |
| Options compared | Comparison cards or matrix with a highlighted recommended option; tabs when each option needs detail |
| Steps, phases, schedule | Timeline or roadmap with real dates or durations; Gantt-like bars if overlapping |
| Numbers over time or shares | Chart drawn to scale (inline SVG for simple, Chart.js 4.4.1 from jsDelivr for complex), with direct labels and an emphasized key value |
| Headline figures | KPI tiles only if the figures are the point of the page |
| Risks | Severity pills plus likelihood and impact, sorted by severity |
| Process or relationships | Diagram (native mermaid block or inline SVG), not a paragraph |
| Pros and cons | Two-column list with icons, not prose |
| Assumptions that drive numbers | Small interactive controls (slider, toggle) that recompute the result, only when it genuinely helps |
| Long reasoning | Short answer first, details in `<details>` accordions |
| Jargon | One-line plain definition on first use (tooltip or inline), or a small glossary |
| Quotes, sources | Source list with links; label estimates as estimates |

## Simplifying complex text

- Lead with the conclusion, then the reason. One idea per block, at most ~4 lines per paragraph.
- Replace explanations of structure with a picture: diagram, comparison table, annotated example.
- Use "in short" callouts for the hard parts. Write for a smart reader outside the field.
- Use concrete numbers and examples instead of adjectives.

## Interactivity: purposeful only

Sorting, filtering, tabs, accordions, scenario sliders, copy buttons, scroll-spy navigation. Every interactive element must change what the reader sees in a useful way. No decorative animation. Everything meant to be read is visible on load (no opacity-0 reveals waiting for scroll). Respect `prefers-reduced-motion`.

## Icons

Inline SVG only (stroke 1.5px, `currentColor`, one consistent set, drawn in the `skeleton.html` sprite style). Use them as meaningful markers for sections, statuses and list items. No emoji as markers, no icon fonts (blocked by CSP). Numbering (01, 02) only where the order is real information.

## Truthfulness

- Numbers, quotes and sources come from the actual research. Never invent data to fill a chart or table.
- Mark estimates, assumptions and low-confidence items visibly (a pill or note).
- If a conclusion rests on thin evidence, say so in the takeaway.

## Technical reminders (details in artifact-design)

- No `<!DOCTYPE>`, `<html>`, `<head>`, `<body>` tags. `<title>` is a 2-4 word name, never "Name: explainer". Pass a one-sentence `description` and a generic `icon` word on first publish.
- Libraries only from cdnjs, cdn.jsdelivr.net/npm, unpkg, with exact pinned versions. Everything else inline.
- All colors are tokens defined on `:root` with both dark blocks; `body` has an explicit background. Chart text and lines use the tokens too (read them with `getComputedStyle` for Chart.js).
- Works at 400px wide with no horizontal page scroll; tables and code scroll inside their own container. Side gutter uses the two `max()` paddings and the `claude:viewport-fit-sides` meta.
- No Print or Download buttons, no `mailto:` links, no `alert/confirm/prompt`.
- Page language follows the user's language unless told otherwise.

## Final checklist

- [ ] Same-topic revision edited the existing file and republished the same path
- [ ] Answer is visible without scrolling; takeaways match the body
- [ ] Every table is a real table; every process or comparison has a visual
- [ ] Charts only on real numbers, to scale, readable in both themes
- [ ] Looks specific to this subject, not a template
- [ ] Phone width fine; both themes fine; no console errors
