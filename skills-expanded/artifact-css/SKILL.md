---
name: artifact-css
description: OUTPUT IS ALWAYS A SINGLE `.html` FILE (never `.md`, never plain markdown, never a text response) styled with the artifact.css class vocabulary. Use this skill whenever producing a standalone HTML artifact that is meant to be read, reviewed, or interacted with as a document. This includes status reports, post-mortems, implementation plans, PR reviews, design systems, explainers, comparisons, slide decks, and interactive editors. Apply this skill any time the user asks for an HTML page, web page, report, dashboard, or any "show me" / "draw me" / "visualize" output that should look polished rather than developer-default. The skill provides a lightweight design system (artifact.css) with a unified color palette, typography, and component vocabulary so the artifact reads as a real document, not a rough sketch. Do not use for production apps, marketing sites, or anywhere a separate design system is already in play.
---

# artifact-css

> ## OUTPUT CONTRACT — READ BEFORE GENERATING
>
> **Every artifact produced under any `artifact-*` skill is a `.html` file. Never `.md`. Never markdown. Never plain text.**
>
> 1. The deliverable is a single `.html` file. If you find yourself writing `# heading` or `| table |` markdown syntax, STOP — you are violating the skill contract. Switch to HTML elements (`<h1>`, `<table>`, etc.) using the class vocabulary in this skill.
> 2. The file extension is `.html`. Not `.md`. Not `.markdown`. Not `.txt`.
> 3. The CSS is either linked (`<link rel="stylesheet" href="artifact.css">`) or inlined inside `<style>...</style>` in `<head>`. Default for agent-produced artifacts is inline (Mode B — single-file portable).
> 4. The output uses the class vocabulary documented below (`.panel`, `.callout`, `.kv-strip`, `.timeline`, `.badge`, `.note`, etc.). NOT raw HTML with no classes. NOT markdown with `*bold*` and `# headings`.
> 5. This contract applies even when the artifact is for internal planning, working notes, or one-time use. The shape of the output is HTML, always.
>
> If the user asks for "a plan", "a status update", "a review", "an explainer", "an editor" and the matching `artifact-*` skill is loaded, the answer is an HTML file written against the artifact.css vocabulary. No exceptions.
>
> ### Single file, multiple views — allowed
>
> "Single file" does NOT mean "single screen". A `.html` artifact may carry multiple internal views switched by JavaScript:
>
> - **Slide decks** (`artifact-deck`) — many slides, one file, arrow-key / click navigation.
> - **Clickable prototypes** (`artifact-flow`) — many screens, one file, hotspot or hash-router navigation.
> - **Multi-step wizards** — one file with stepper-controlled views.
> - **Before / after toggles, naïve / optimized comparisons, tabs of code samples** — all single file, internal view switching.
>
> The contract: one `.html` file delivered to the user. The number of "screens" inside that file is determined by the artifact shape — a slide deck is multi-slide by definition, a status report is single-page by definition. NEVER ship multiple `.html` files for one artifact request; if you feel the urge to split, you are violating the contract.

---

A lightweight stylesheet and a small vocabulary of patterns for the kind of HTML artifacts an agent produces inline. The goal: when the user asks for a status report or an explainer or a triage board, the output reads like a real document at a glance - same typographic rhythm, same palette, same components - regardless of which agent skill produced it.

## What's in the library

One file, `artifact.css`, ~16KB raw and ~4KB gzipped. No JavaScript, no build step, no external dependencies. Drop it into the `<head>` of any artifact and write semantic HTML against the class vocabulary below.

The library covers: tokens (color, type, spacing, radius, shadow), base typography (h1–h4, body, eyebrow, lead), section chrome (sec-head, sec-intro, rule), surfaces (panel, callout, note, prompt-box), inline atoms (tag, pill, badge, avatar, dot), buttons and inputs, tables, stat cards, key-value strips, highlights and tag lists, timelines and milestones, code blocks, diffs, and a small set of grid and utility helpers.

## How to use it in an artifact

Two delivery modes. Choose based on context.

**Mode A - link to the file.** Used when the artifact is hosted, or when the user has artifact.css available alongside the HTML.

```html
<link rel="stylesheet" href="artifact.css">
```

**Mode B - inline the file contents.** Used when the artifact must be a single portable HTML file (e.g. downloaded and opened locally, attached to an email, committed to a repo). Inline the entire contents of `artifact.css` inside a `<style>` block in `<head>`. The artifact stays self-contained.

For most agent-produced artifacts, Mode B is correct. The artifact's single-file nature is part of the value.

## The page skeleton

Every artifact starts from the same minimal scaffold:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>...</title>
  <style>/* contents of artifact.css */</style>
</head>
<body>
  <div class="page">

    <header>
      <p class="eyebrow with-rule">Section · context</p>
      <h1>Document title</h1>
      <p class="lead">One-sentence framing of what this document is and who it's for.</p>
    </header>

    <!-- sections go here -->

  </div>
</body>
</html>
```

`.page` is centered, 860px wide, with generous top/bottom padding. Use `.page-wide` (1120px) for dashboards or comparison sheets, and `.page-narrow` (680px) for prose-heavy explainers.

## Design tokens

All visual values are declared as CSS custom properties on `:root`. Override any of them by re-declaring in a later `:root` block to retheme the artifact.

**Surfaces:** `--ivory` (page background, #FAF9F5), `--paper` (#FFFFFF), `--oat` (#E3DACC, soft accent surface).

**Ink:** `--slate` (#141413, strongest), `--gray-700`, `--gray-500`, `--gray-300`, `--gray-200`, `--gray-100`.

**Accent / semantic:** `--clay` (#D97757, primary accent and "needs attention"), `--clay-d` (darker clay for hover), `--olive` (success / positive), `--rust` (danger / failed), `--sky` (info / neutral status).

**Fonts:** `--serif` for headings, `--sans` for body and UI, `--mono` for labels, code, and small all-caps text. All three are system font stacks; no web fonts required.

**Radii:** `--r-xs` 4px, `--r-sm` 8px, `--r-md` 12px, `--r-lg` 20px, `--r-pill` 999px.

**Spacing scale:** `--sp-1` through `--sp-8` (4, 8, 12, 16, 24, 32, 48, 64).

## Component vocabulary

The class names are short and predictable. They map 1:1 to the patterns observed in well-written HTML artifacts, so an agent who has internalized those patterns produces compatible markup automatically.

### Typographic atoms

- `.eyebrow` - small mono uppercase label above a heading. Add `.with-rule` for the small clay accent bar.
- `.lead` - slightly larger intro paragraph below an h1.
- `hr.rule` - thin divider used under h2 to mark section starts.

### Section chrome

```html
<section>
  <div class="sec-head">
    <span class="num">01</span>
    <h2>Milestones</h2>
    <span class="count">4 items</span>
  </div>
  <p class="sec-intro">A one-line orientation for the section.</p>
  ...
</section>
```

The `.num` chip and `.count` chip are both optional. Use `.num` when the document has explicit ordering (plans, decks).

### Surfaces

`.panel` is the workhorse: white background, 1.5px border, 12px radius. Use it to group related content. Add `.panel-flush` when the panel contains a table or other content that should bleed to the edges.

`.callout` is the oat-colored aside - use sparingly for one important thing per section.

`.note` is a white card with a colored left edge. Variants: `.note-success`, `.note-warn`, `.note-danger`, `.note-info`. Use for inline asides, open questions, and small warnings.

`.prompt-box` is the gray-100 box at the top of an artifact that quotes the user's prompt verbatim. It's a small honesty signal: this document was generated from that input.

### Inline atoms

- `.tag` and `.pill` - small mono labels. Tag is square-radius, pill is rounded.
- `.badge` - semantic chip. Variants: `.badge-clay`, `.badge-success`, `.badge-warn`, `.badge-danger`, `.badge-info`.
- `.avatar` - 36px round initials. `.avatar-sm` (26px) and `.avatar-lg` (48px).
- `.dot` - 9px status dot. Variants: `.dot-good`, `.dot-warn`, `.dot-bad`, `.dot-info`.

### Stat strip

```html
<div class="stats">
  <div class="stat">
    <div class="stat-num">42</div>
    <div class="stat-label">PRs merged</div>
    <div class="stat-delta up">+12 vs last week</div>
  </div>
  ...
</div>
```

Four columns on desktop, two on small screens. Add `.stat-accent` to a single card to highlight it.

Use `.kv-strip` instead when the values aren't big numbers but short text labels (e.g. "~2 weeks", "3 packages", "task_comments_v1").

### Tables

```html
<table class="table">
  <thead><tr><th>PR</th><th>Author</th><th class="num">+/-</th></tr></thead>
  <tbody>
    <tr><td>#247</td><td>danielle</td><td class="num">+412 / −38</td></tr>
  </tbody>
</table>
```

The `.num` class on a `<th>` or `<td>` switches it to monospaced tabular figures.

### Timelines

```html
<div class="timeline">
  <div class="milestone">
    <div class="when">Week 1 · Mon</div>
    <div class="axis"><span class="dot done"></span><span class="line"></span></div>
    <div class="body">
      <h3>Schema and API contract</h3>
      <p>...</p>
      <ul class="tag-list"><li class="tag">packages/db</li></ul>
    </div>
  </div>
  ...
</div>
```

Use `.dot.done` for completed milestones (olive), plain `.dot` for upcoming (clay outline).

### Code and diffs

`.code-block` wraps a `<pre>` for highlighted code. Inside the `<pre>`, apply `.kw` (keywords), `.st` (strings), `.cm` (comments), `.fn` (function names) to `<span>`s for color.

For diffs, see the `artifact-review` skill - the markup is more involved than belongs in this overview.

### Layout helpers

- `.grid-2`, `.grid-3`, `.grid-4` - equal columns, collapse to single column under 720px.
- `.grid-auto` - `repeat(auto-fill, minmax(280px, 1fr))`, for card galleries.
- `.row`, `.row-baseline`, `.row-between` - flex helpers.
- `.stack-sm`, `.stack`, `.stack-lg` - vertical flex stacks (8 / 16 / 32 gap).

### Utilities

`.muted`, `.ink`, `.accent`, `.mono`, `.serif`, `.sans`, `.small`, `.tiny`, `.uppercase`, plus margin top/bottom helpers `.mt-0` through `.mt-6` and `.mb-0` through `.mb-6`.

## Voice and density rules

The library encodes a few opinions worth respecting in the markup choices:

1. **One opinionated accent.** Clay is the only loud color. Use it for attention, hover, and one or two highlights per page. Olive, rust, and sky are reserved for true semantic signals.
2. **Serif headings, sans body, mono for the small bits.** Mono is for labels, codes, metadata, and anything that benefits from feeling like terminal output. It is not a body font.
3. **1.5px borders.** Not 1px. The slightly heavier stroke is the visual signature of this system.
4. **Generous white space.** `padding: 56px 24px 120px` on the page is intentional. Don't compress it.
5. **No emojis as icons.** Use SVG, a `.dot`, or a `.badge` instead.
6. **No drop shadows by default.** The token system includes `--shadow-sm` through `--shadow-lg`, but they're for hover states and floating elements, not for static panels.

## Choosing the right pattern skill

`artifact-css` is the foundation. For each common artifact archetype there's a more specific skill with full templates:

- `artifact-report` - status updates, post-mortems, incident timelines, PR writeups.
- `artifact-plan` - implementation plans, comparison sheets, roadmaps with milestones and risk tables.
- `artifact-review` - annotated PR reviews with diffs and margin comments.
- `artifact-explainer` - concept and feature explainers with collapsible sections, TL;DR, and glossary.
- `artifact-editor` - interactive editors with export buttons (triage boards, feature flag panels, prompt tuners).

Read the relevant pattern skill in addition to this one whenever its archetype applies.

## Interactivity layer (optional) — jQuery 4.0.0 + jQuery UI 1.14.2

The base library is pure CSS. When an artifact needs interactivity (collapsibles, tabs, sortable lists, drag-and-drop, sliders, dialogs, autocomplete, datepickers), opt-in to jQuery + jQuery UI.

**When to load it**
- Pattern skill is `artifact-explainer` or `artifact-editor` — always.
- Pattern skill is anything else — only if the artifact explicitly needs a widget jQuery UI provides.
- Static documents (reports, plans, reviews) — do NOT load it. They must remain pure HTML/CSS.

**Versions (pinned, current as of 2026-05-12)**
- jQuery `4.0.0` (released 2026-01-17)
- jQuery UI `1.14.2`

**Loader (drop into `<head>` after `<style>artifact.css</style>`)**

```html
<link rel="stylesheet"
      href="https://code.jquery.com/ui/1.14.2/themes/base/jquery-ui.min.css"
      integrity="sha384-pUvA/6DQjteMxpaV6uGxZ1QuYrFLJgrLMvBWf06VcJIg6ky/Y5m3UZJlrv11V1I+"
      crossorigin="anonymous">

<script src="https://code.jquery.com/jquery-4.0.0.min.js"
        integrity="sha384-fgGyf7Mo7DURSOMnOy7ed+dkq5Job205Gnzu6QIg0BOHKaqt4D76Dt8VlDCzcMHV"
        crossorigin="anonymous"></script>

<script src="https://code.jquery.com/ui/1.14.2/jquery-ui.min.js"
        integrity="sha384-tBcEcHGtNy7/Mx08+YxuvQ6v6s0N2jgehtFiT+bLtGwTj/txXtB/L5GqXfggm5sS"
        crossorigin="anonymous"></script>
```

Place scripts at end of `<body>` if first paint matters. SRI hashes guarantee integrity — never bump the version without recomputing them.

**Widget → use case map**

| jQuery UI widget | Use in artifacts |
|---|---|
| `.accordion()` | Collapsible FAQ / multi-section explainer body |
| `.tabs()` | Switching between code samples (JS / Python / curl) |
| `.tooltip()` | Inline glossary terms (hover to define) |
| `.sortable()` | Triage board columns · backlog reorder |
| `.draggable()` + `.droppable()` | Drag cards between columns |
| `.slider()` | Feature-flag ramp percentage · prompt-tuner numeric knobs |
| `.datepicker()` | Planning / scheduling artifacts |
| `.dialog()` | Export / copy-to-clipboard modal |
| `.autocomplete()` | Tag filter on large boards |

**Theme override.** Base theme ships gray default chrome. Each interactive skill bundles a small CSS block that re-maps jQuery UI classes to library tokens (clay accent, ivory background, 1.5px borders, serif headings). Override block belongs in the skill's own `artifact.css`, not the canonical library file. Canonical library stays widget-free.

**Fallback contract.** Every interactive template must degrade gracefully. If jQuery fails to load:
- Accordion sections render as plain visible blocks.
- Tabs render as stacked sections, each preceded by its tab label.
- Sortables render as plain `<ul>`.
- Sliders render as `<input type="range">` (native HTML5 fallback).

Achieve this by writing semantic HTML first (e.g., `<dl>` for accordion, `<ul>` for sortable, plain headings for tab panels), then progressively enhancing in `$(document).ready()`. Never inject critical content via JS — JS only rewires existing markup.

**Why jQuery and not vanilla.** Decision D9 in `PLAN.md`. Short version: mature widget set, stable APIs, single CDN, no build step, zero concept burden for downstream agents. Same philosophy as the CSS library.

---

## Example

`examples/basic.html` is a one-page artifact that uses every major component in the library. Open it locally to see the visual language. Copy its `<style>` block as the inline-mode artifact.css.
