---
name: explain-pr-up
description: Create a standalone HTML artifact that presents a pull request for review. Shows before/after code changes, file-by-file tour with annotated diffs, risk map, review focus areas, and a short summary. Use when the user asks to write up a PR, summarize code changes visually, create a PR review document, show before and after diffs in HTML, or prepare a change walkthrough for reviewers.
---

# Explain PR Up

## Overview

Create a self-contained HTML document that shows what a pull request changed and why. A reviewer opens the file in any browser and sees the full picture — no scrolling through terminal diffs.

Use `assets/pr-review-template.html` as a starting structure, then replace every placeholder with real data from the PR.

## Writing Style

Write the way `explain-issue-html` writes: short, plain, concrete.

1. Use short sentences. One idea per sentence.
2. Use simple words. Say "blank" not "null, empty, or whitespace-only." Say "breaks" not "introduces a regression in."
3. Define technical terms before using them. If the reader needs to know what "ABN" or "debtor sync" means, say it once in plain words first.
4. Show a concrete example before a general rule. Instead of "adapters preserve existing values field-by-field," show:
   ```
   Before: sync sends blank → name gets erased
   After:  sync sends blank → name stays "John"
   ```
5. Do not stack multiple changes into one long sentence. Break them into a list.
6. Prefer "what the user sees" over "what the code does." Say "the name disappears from the form" not "the adapter overwrites the nested contact object."
7. Avoid passive voice when you can. Say "sync erases the name" not "the name is erased by the sync."
8. Avoid jargon soup. Do not write "nested contact/address adapters preserve existing values field-by-field." Write "if the sync sends a blank name, we keep the old name."

## Workflow

1. Gather the PR data.
   - Read the diff (`git diff`), commit messages, and any PR description.
   - List every changed file, the line counts (+/−), and whether each file is new, modified, or deleted.
   - Read enough surrounding context to understand each change.

2. Classify each file by review risk.
   - **safe** — small addition, type-only, test, config, or obviously correct.
   - **worth a look** — logic change that is straightforward but worth scanning.
   - **needs attention** — new core logic, tricky edge case, error handling, or security-sensitive.

3. Write the PR story in plain language.
   - **TL;DR**: A bullet list (5–7 items). Each bullet is one short sentence that a high-school student can understand. No jargon without a one-line definition first. **Do NOT include bullet characters** (`\2022`, `•`, `-`, etc.) in the `<li>` text — the CSS `li::before` rule renders bullets automatically.
   - **Flow diagram**: Only if the changed files are **related** — one calls another, they share a data pipeline, or they pass data between them. Do not draw a flow for files that are independent/unrelated changes. For complex flows, use inline SVG (see below).
   - **Short summary**: 2–3 sentences. What changed? Why? Written so someone who has never seen this code can follow.
   - **Before / After**: what happened before this PR vs. what happens now. Use bullet points. Keep each bullet to one line.
   - **File-by-file tour**: most important file first. For each file:
     - One sentence: *why* this file changed (not just *what*).
     - A code block showing the change **with surrounding context** — include the full function or method, not just the changed lines. If the class is very large, show the relevant method plus a few lines above and below. Unchanged context lines have no special class (they appear in default off-white). Only changed lines get `.add` or `.del` spans. This gives the reviewer enough context to understand the change without switching to an IDE.
   - **Review focus**: 2–3 numbered items. Point to the exact lines or decisions that matter most. Say why they matter.

4. Build the HTML artifact.
   - Save to the path the user requested.
   - If no path is given, use `docs/<pr-number-or-short-name>-review.html`.
   - Keep all CSS inline. No external CDNs, no bundlers, no servers required.

5. Review your own text before finishing.
   - Read every sentence. If it has more than one comma, split it.
   - If a bullet point wraps to a third line, it is too long. Shorten it.
   - Replace any fancy word with a simpler one.

## Sections

Include these sections unless the PR clearly does not need one:

1. **Header** — PR number, title, branch → target, author, +/− line counts.
2. **TL;DR** — Bullet list of what changed. Each bullet is one short sentence. Write so a high-school student can follow. No jargon without explaining it first. Max 5–7 bullets.
3. **Flow diagram** (conditional) — Only include when changed files are **related**: one calls another, they share a data pipeline, or data flows between them. Skip entirely if files are independent changes (e.g., unrelated config + unrelated test). A horizontal block-box diagram where each box = a function/module name, boxes connect with arrows (→). Clicking a box opens a **popup** showing that file's code change — the user stays on the flow view and can click other boxes to compare.
4. **Before / After** — Side-by-side panels. Short bullet points only.
5. **Risk map** — Colored chips (safe / worth a look / needs attention) that link to file sections.
6. **File tour** — Collapsible cards per file, each with:
   - File path, badge (new/mod/del), +/− stats.
   - One sentence explaining *why* this file changed.
   - A code block showing the change **in context**: include the full function or method. Unchanged lines have no `.add`/`.del` class. Only mark changed lines with `.add` (green) or `.del` (red). If the entire file is new and short, show it all.
7. **Review focus** — Numbered cards with the 2–3 most important review points.
8. **Checklist** (optional) — Interactive checkboxes for reviewer sign-off.

## Design Principles

- Palette: `--ivory`, `--slate`, `--clay`, `--oat`, `--olive` (from Anthropic HTML effectiveness examples).
- Serif headings (`ui-serif, Georgia`), sans body (`system-ui`), mono for code and paths.
- Rounded 12px cards, 1.5px borders, minimal decoration.
- Dark code blocks (`--slate` background) with warm off-white text.
- **Code diff colors follow Claude Code style:**
  - Added lines: green background (`rgba(46,160,67,0.20)`), solid green left border (`#3fb950`). Text stays readable.
  - Deleted lines: red background (`rgba(248,81,73,0.20)`), solid red left border (`#f85149`), strikethrough text.
  - Unchanged context lines have no highlight — just the default dark background.
- Responsive: single column below 900px.
- No animations, no gradients, no decoration for decoration's sake.

## Code Diff Rendering

For each file's key change, show the **full function or method** containing the change. Unchanged context lines have no special class — they appear in the default off-white text. Only changed lines get `.add` or `.del` spans:

```html
<div class="code"><pre>
<span class="kw">function</span> <span class="fn">processOrder</span>(order) {
  <span class="kw">const</span> total = order.items.reduce((s, i) => s + i.price, 0);
<span class="del">- <span class="kw">if</span> (total > 100) <span class="kw">return</span> applyDiscount(total);</span>
<span class="add">+ <span class="kw">const</span> discount = total > 100 ? <span class="fn">getDiscount</span>(order.tier) : 0;</span>
<span class="add">+ <span class="kw">return</span> { total: total - discount, discount };</span>
  <span class="fn">logOrder</span>(order.id, total);
}
</pre></div>
```

Notice: the function signature, unchanged lines, and closing brace provide context. Only the actual changes are highlighted.

Classes:
- `.kw` — keywords (const, await, if, return)
- `.fn` — function names
- `.str` — string literals
- `.cm` — comments
- `.add` — added lines (green background, green left border — Claude Code green)
- `.del` — deleted lines (red background, red left border, strikethrough — Claude Code red)

## Flow Diagram

**When to include:** Only when changed files are related — one calls another, they share a data pipeline, or data flows between them. Do NOT include if the changed files are independent (e.g., a config change + an unrelated test fix).

**When to skip:** Single-file changes, config-only changes, files that don't interact with each other.

### Simple flow (2–4 steps)

Build with CSS flexbox boxes and arrow connectors. Each box:
- Shows the function or module name.
- Has a `data-popup="file-N"` attribute linking to the matching file's `<details id="file-N">` element.
- **On click, opens a popup/modal** showing that file's code change. The user stays on the flow view and can click other boxes to compare changes. The clicked box gets an `.active` highlight.
- Uses the same card styling (rounded, bordered) as the rest of the page.

The popup is powered by a small inline `<script>` at the bottom of the page (see template). It clones the `.file-body` content from the matching `<details>` into a centered overlay. Close with ×, click outside, or Escape.

```html
<div class="flow">
  <a data-popup="file-1" class="flow-box">functionX</a>
  <span class="flow-arrow">→</span>
  <a data-popup="file-2" class="flow-box">functionY</a>
  <span class="flow-arrow">→</span>
  <a data-popup="file-3" class="flow-box">functionZ</a>
</div>

<!-- Popup container (one per page, populated by JS) -->
<div class="flow-popup-overlay" id="flow-popup-overlay">
  <div class="flow-popup">
    <div class="flow-popup-head">
      <span class="path" id="flow-popup-path"></span>
      <button class="flow-popup-close" id="flow-popup-close">&times;</button>
    </div>
    <div class="flow-popup-body" id="flow-popup-body"></div>
  </div>
</div>
```

### Complex flow (5+ steps, branching, or loops)

For complex logic with branching paths, error handling, or many nodes, use inline SVG instead of CSS boxes. Follow the SVG craftsmanship guidelines from [dogum/html-artifacts diagrams-and-illustrations](https://github.com/dogum/html-artifacts/blob/main/skill/references/diagrams-and-illustrations.md):

- Use `viewBox` (not fixed width/height) so the diagram scales.
- Highlight the happy path in a distinct color; failure paths in muted secondary.
- Use `<marker>` arrowheads on edges for directionality.
- Group nodes with `<g>` and label them for readability.
- Make nodes clickable (`<a xlink:href="#file-N">`) to navigate to file sections.
- Add a legend in the corner if more than 2 path types exist.

```html
<figure>
  <svg viewBox="0 0 600 200" role="img" aria-labelledby="flow-title">
    <title id="flow-title">Code change flow</title>
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
              markerWidth="6" markerHeight="6" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" fill="currentColor"/>
      </marker>
    </defs>
    <!-- nodes and edges here -->
  </svg>
</figure>
```

## Template

The starter template is:

```text
assets/pr-review-template.html
```

Read the file, replace all `{{PLACEHOLDER}}` values with real PR data, then add or remove sections to match the actual number of files and review points. Do not leave any placeholder text in the final artifact.
