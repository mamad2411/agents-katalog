---
name: data-craft
description: Generate beautiful themed HTML data displays. Six visual idioms with matched voices, rendered as self-contained HTML files. Use when the user asks for charts, dashboards, reports, tearsheets, briefings, data visualizations, or any data-driven document.
version: 1.0.0
---

# data-craft

You produce data-driven HTML documents in one of six named themes. Each theme has its own visual language *and* its own writing voice. Same skill, dramatically different output depending on which theme fits the task.

The point of data-craft is that the format and voice are matched to the content. A finance tearsheet should not just *look* like a Bloomberg terminal; it should *read* like one. A culture story should not just *look* like a Bauhaus broadsheet; it should *read* like one. You enforce that match.

---

## When to activate

This skill applies when the user asks for:

- A chart, dashboard, tearsheet, briefing, report, or data display
- A "state of X" piece, a "X by the numbers" piece, an industry roundup
- Visualization of data they provide (CSV, JSON, pasted numbers, verbal descriptions)
- A specific data-craft theme by name ("make me a Sand Hill piece on...")

This skill does NOT apply when the user asks for:

- A single chart inside another document (just generate the chart inline)
- A plain table or list
- Code that produces a chart programmatically (use the appropriate code skill)
- A presentation deck (use pptx skill)
- A Word document or PDF (use docx or pdf skills)
- Conversational responses about data

When the request is ambiguous (e.g., "show me Apple's revenue"), default to providing the data conversationally and ask if they want a full data-craft briefing.

---

## The six themes

You ship six themes. Each is a complete visual world plus a matched voice. Read the theme reference card in `themes/[theme-name].md` whenever you generate that theme — it contains the design tokens, voice profile, and layout patterns you must follow.

### Theme selection logic

When the user does not specify a theme, pick based on this decision flow:

1. **Did the user name a theme?** Use it. Theme names are case-insensitive. "sand hill", "SandHill", "Sand Hill" all match.
2. **Does the topic involve a stock ticker, market cap, earnings, P/E, or other equity terms?** → **Trading Floor**
3. **Does the topic involve developer tools, product launches, platforms, or "state of X" for a tech category?** → **Pitch Black**
4. **Is the topic aerospace, hard tech, scientific, or technical-with-credibility-needed (engineering reports, technical product specs, scientific R&D)?** → **Apollo White**
5. **Is the topic culture, music, sports, lifestyle, or has natural drama (lawsuits, fights, scandals)?** → **Helvetica Riot**
6. **Is the topic consumer brand marketing, food and beverage, hospitality, or warm/lifestyle-coded?** → **Sunday Press**
7. **Default for editorial / research / longform / "I want a magazine-quality essay"** → **Sand Hill**

If a topic genuinely doesn't fit any theme cleanly, say so. Suggest the closest fit and offer to proceed. Do not force-fit (e.g., do not put a wedding planning timeline in Trading Floor just because no theme is perfect).

### Theme summary table

| Theme | Background | Primary accent | Voice | Use when |
|---|---|---|---|---|
| **Sand Hill** | Cool cream `#f6f4ee` | Ochre `#c4711a` | Measured editorial, long sentences, em-dashes | Longform research, magazine essays |
| **Pitch Black** | Pure black `#000` | Electric green `#00ff88` | Short declarative, period-heavy | Product launches, dashboards, state-of-X |
| **Trading Floor** | Deep navy `#0a1428` | Amber `#ff9933` | Clinical terse, "as of" timestamps | Equity tearsheets, finance dashboards |
| **Helvetica Riot** | Near-white `#fafafa` | Red/Yellow/Blue primaries | Confident with attitude, periods as weapons | Culture, music, lifestyle, anything spicy |
| **Sunday Press** | Warm cream `#fbf4e8` | Terracotta `#c4622d` | Warm-confident, "here's what we made" | Consumer brand, hospitality, food/lifestyle |
| **Apollo White** | Pale blue-grey `#f7f9fc` | Electric blue `#0052ff` | Precise aerospace, spec-sheet feel | Aerospace, hard tech, scientific, technical-professional |

---

## Voice profiles per theme

Match the voice precisely. Theme + content + voice must align — that's the data-craft promise.

### Sand Hill voice

- Long sentences with em-dashes and subordinate clauses
- Drop cap on first paragraph of each section
- Pull quotes used for emphasis (not bold)
- Italic for editorial commentary, sparingly
- "As of [date]" attribution inline in prose
- Example hero: *"Eighteen months ago, the AI coding tools market did not exist as a commercial category."*

### Pitch Black voice

- Short. Declarative. Period-heavy.
- Stack three or four short sentences in a row for effect
- One accent-green word per headline maximum
- "// kicker" markers in mono for section labels
- A single dramatic pull-quote in a bordered callout
- Example hero: *"The robots are real now."* (full opening paragraph)

### Trading Floor voice

- Heavy parenthetical timestamps. "As of 2026-05-21 16:00 ET."
- Numbers are the headline; prose is connective tissue
- Symbol displayed huge (56px+) in amber
- "// section title" markers in mono caps
- Tables get amber row-highlighting for the most recent / focal row
- Example hero: `NVDA · $223.47 · $5.32T`

### Helvetica Riot voice

- Three-sentence punches with yellow inline highlights
- Periods as weapons
- Confident-with-attitude — like a Pentagram annual report
- Em-dashes for asides
- Example hero: *"Big music sued. Big music lost. Twice."*

### Sunday Press voice

- Warm-confident, "host who has done this before" energy
- Sentences flow, period-comma rhythm
- Welcoming language without becoming saccharine
- Italic terracotta for emphasis words
- Example hero: *"Five chains. Five playbooks. One latte."*

### Apollo White voice

- Precise, technical, spec-sheet feel
- Aerospace press-kit tone — "here is the engineering"
- Electric blue accent for headline emphasis words
- "// kicker" + "Status: [tag]" indicators with bullet dots
- "Per [source]" attribution inline
- Example hero: *"A trillion-dollar private rocket company goes public."*

---

## Layout patterns per theme

Each theme has signature layout moves. Reproduce them.

### Sand Hill layout

- Single-column body, ~680px max width
- Generous vertical spacing (48–80px between sections)
- Section eyebrows: small caps, ochre, with a hairline rule before
- Charts in `<figure>` blocks with caption + source line below
- Pull quotes break the column rhythm
- Drop cap on first paragraph of each section using CSS

### Pitch Black layout

- 12-column grid, dense tiles with `border: 1px solid var(--pb-line)`
- KPI hero strip: 4 stat tiles separated by 1px gap
- Subtle scan-line / grid background for atmosphere
- A pulsing green dot for "live" status
- Tables small fonts, tight padding, status tags

### Trading Floor layout

- Ticker bar (full width) at the top with brand, issue, "AS OF YYYY-MM-DD HH:MM ET"
- Hero strip: symbol + 3 KPI cells (price, market cap, 52W range)
- 12-column grid below with mixed widths
- Tables get amber row-highlighting for focal row
- Footer is a single dense paragraph with every source named

### Helvetica Riot layout

- Heavy 2-3px black rules between sections
- 3px black borders on tiles
- Hero numbers in oversized Inter 900 (80-100px) inside color-block tiles
- Geometric shapes (circles, rotated squares) as accents
- Asymmetric placement of issue badges, kickers, callouts
- Strict 5-color palette: red, yellow, blue, ink, paper. No exceptions.

### Sunday Press layout

- Rounded tile corners (`border-radius: 8px/14px`) — only theme with rounded corners on tiles
- Subtle SVG paper-grain texture via CSS noise filter
- Five-color tile system: each "entity" in a story gets its own color (terra/sage/mustard/navy/cream)
- Magazine-style pull quotes with oversized terracotta `"`
- Generous padding inside tiles (28px+)

### Apollo White layout

- Drafting-paper grid overlay via CSS gradients (80px squares, very low opacity)
- KPI strip at top: 4 spec cells in a single horizontal row, divided by hairline borders
- Crosshair brand mark in electric blue
- "Status: [X]" indicator in masthead with bullet dot
- Aerospace-style callout boxes with blue left rule and "// CONTEXT" label
- Tags carry meaning: blue=key, ghost=neutral, signal-red=warning

---

## Universal conventions

These apply to every theme, every output, every time.

### File format

- Output is a single self-contained HTML file
- No build step, no bundler, no backend
- ECharts loaded from `https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js`
- Fonts from Google Fonts (preconnect + stylesheet link)
- All CSS in a `<style>` tag in `<head>`
- All JS in a `<script>` tag at end of `<body>`
- Save to `/mnt/user-data/outputs/[topic-slug].html` or wherever the user specifies
- File size soft target: under 100 KB

### CSS variable naming

Prefix CSS variables with the theme's two-letter shorthand: `--sh-` (Sand Hill), `--pb-` (Pitch Black), `--tf-` (Trading Floor), `--hr-` (Helvetica Riot), `--sp-` (Sunday Press), `--aw-` (Apollo White). This makes the source readable and prevents cross-theme bleed.

### Methodology footer

Every piece ends with a `Methodology & sources` block at the bottom.

The footer names every figure that appears in the piece, with a date and a source. If a figure is an estimate, the footer says so explicitly. This is mandatory.

If the piece contains **no estimates at all** (all figures sourced directly from primary documents), say so explicitly in the footer with a sentence like *"No estimates in this piece — all figures sourced directly from [source]."* Positive acknowledgments build credibility just as much as labeled caveats.

Footer styling differs per theme (Pitch Black footer is dense mono, Sand Hill footer is small caps and serif, etc.) but the content structure is the same.

### Estimates are labeled in the rendered output

If a chart or table includes a value that is not directly disclosed, the rendered label includes `(est.)` or `est.` — not just in a footnote.

Enforce this visually:

- Pie/donut slices: append `est.` to the slice label when the figure is estimated
- Bar charts: append `est.` to the data label
- Tables: append `est.` to the cell value
- Series in legends: append `(est.)` suffix when the entire series is estimated

When a series is fully estimated, render its line as dashed rather than solid.

### Data verification

When the user asks for a piece about a topic with time-sensitive data (current revenue, recent earnings, market caps, GitHub stars, valuations, "latest" anything), use web search to verify the figures before generating.

Do not state figures from memory for:
- Stock prices, market caps, P/E ratios
- Quarterly or annual revenue for any public or private company
- User counts, subscriber counts, MAU/DAU
- Recent valuations or funding rounds
- GitHub stars, npm download counts
- Anything labeled "current" or "latest" in the user's prompt

When in doubt, search.

### When data is incomplete

- If a figure cannot be verified, either omit it OR include it with explicit `est.` labeling and source it in the methodology footer
- Never make up numbers
- Never present an estimate as a verified fact
- If the user provides their own data, use it verbatim and source it as "user-provided"

### Voice consistency

The voice does not break inside a piece. Pick a voice at the start and commit. Don't open Pitch Black with "The robots are real now" and then write a Sand Hill-style paragraph two sections later.

### Section structure (typical)

Most pieces follow this rough structure:

1. **Masthead** — brand strip with theme identity
2. **Hero** — eyebrow + headline + deck + byline (with em-dash separators)
3. **Section §01** — overview / topline (often with a 2-4 tile hero stat strip)
4. **Section §02** — data deep-dive (charts)
5. **Section §03** — comparison / lineup (table)
6. **Section §04** — narrative / playbooks / risks (prose tiles)
7. **Methodology footer**

You can drop or merge sections, but never skip the methodology footer.

---

## Chart conventions

- Use ECharts (`echarts.init(...)`) for all data visualization
- Backgrounds transparent (`backgroundColor: 'transparent'`)
- Use the theme's palette tokens for series colors — never hardcode hex outside `:root`
- Default tooltip styling: use theme ink color for background, paper for text, theme accent for emphasis
- Animation: subtle, 800-1000ms duration, with `animationDelay: (idx) => idx * 60` for staggered bars
- Axis labels in the theme's mono font, low opacity, all-caps for axis titles
- Always add the `est.` label inline when a data point is estimated

### Common chart types and when to use them

- **Bar (vertical or horizontal)** — comparison across categories, revenue by company
- **Stacked bar** — composition over time (e.g., Data Center vs Other revenue)
- **Line** — trends over time (subscriber growth, valuation history)
- **Dual-axis** — when a $ amount and a % rate need to share an x-axis
- **Donut / pie** — share/composition of a single point in time
- **Candlestick + volume** — stock price with daily OHLC
- **Gantt-style horizontal bar** — timelines, lawsuit/event sequences
- **Log scale** — when values span 3+ orders of magnitude (e.g., 17,000 stores vs 37 stores)

---

## Iteration handling

When the user asks for changes after the initial generation:

- **"Make X bigger/smaller"** — adjust the corresponding font-size or padding only
- **"Switch the accent color"** — update the relevant CSS variable; the change cascades
- **"Add a section about Y"** — write a new section in the same voice as existing sections
- **"Change to [theme]"** — regenerate with the new theme's palette, voice, and layout; do not just swap colors

Never silently change anything the user didn't ask about. If a requested change breaks the theme's identity (e.g., adding a fifth primary color to Helvetica Riot), push back and explain.

If the user iterates many times on the same piece, periodically re-render and screenshot it to verify nothing has subtly broken.

---

## Common pitfalls

These are mistakes you should not make. Each one is listed because it has happened.

### 1. Mixing voices across themes

Do not write Sand Hill prose in a Pitch Black layout. The voice profiles are not interchangeable. If the user asks for "Sand Hill but with more attitude," they want Helvetica Riot, not a hybrid.

### 2. Generic AI-aesthetic warm themes

When generating Sunday Press, avoid: hand-drawn doodles, soft purple gradients, fluffy pastels, "you've got this!" copy. Lean into the named aesthetic genealogy (mid-century editorial, letterpress) not "generic warm marketing."

### 3. Generic AI-aesthetic blue themes

When generating Apollo White, avoid: glowing cyan accents, neon highlights, "futuristic" gradient meshes. Lean into the named aesthetic genealogy (SpaceX press kit, NASA spec sheet) not "every B2B SaaS landing page."

### 4. Overloading Helvetica Riot

Helvetica Riot's discipline is its strict primary palette. Do not add greens, purples, pastels, or "supporting accents." Five colors only (red, yellow, blue, ink, paper). If you want more variety, you want a different theme.

### 5. Mismatched comp tables

When citing competitive figures (e.g., market caps of competitor companies), verify each one. A tearsheet with one wrong market cap loses all its credibility instantly. Use web search.

### 6. Stale data

For any topic involving "current" or "latest" figures, search before generating. Do not state figures from memory for time-sensitive metrics.

### 7. Pre-IPO and "in talks" funding rounds

A `$5B Series D in talks` is not a `$5B Series D closed`. Always label which. Same for valuations: "target $2T" is not "valued at $2T."

### 8. Forgetting the methodology footer

Every piece ends with a methodology footer. Always. No exceptions.

### 9. Mocking up data when the user asked for real data

If the user provides a specific topic (e.g., "build a tearsheet on Nvidia"), they want real Nvidia data, not placeholder numbers. Use web search to get current figures.

### 10. Putting financial advice or buy/sell recommendations in pieces

Pieces are informational, not advisory. Never recommend buying or selling a specific security. The footer should include a disclaimer for any financial piece.

### 11. Long kickers in narrow tiles

The mono-font "// KICKER" labels on color-block hero tiles can wrap or get visually clipped if the tile is narrow (1/3 width or less) and the kicker text exceeds ~24 characters. Keep tile kickers to **2-4 short words max** when the tile is in a 3-up or 4-up row. Examples that work: `// THE TRIUMPH`, `// Q2 FY26`, `// FIG 01`. Examples that fail: `// THE TRIUMPH · GROSS MARGIN BREAKDOWN`. If the kicker needs more context, move it to the tile body, not the kicker slot.

### 12. Editorial framing inside data labels

Editorial framing belongs in **prose, headlines, and callout text** — not inside chart labels, axis labels, table column headers, or data point annotations. A chart axis labeled "R&D OPEX" is correct; an axis labeled "AI COMPUTE BILLS" when the underlying figure is total R&D (which includes more than AI) is misleading even if the framing matches the editorial tone of the piece. The voice of the prose can be sharp; the labels on the data must be precise. Helvetica Riot's editorial license applies to *how you frame the numbers*, not *how you name them*.

---

## Edge cases

### When the user's topic doesn't fit any theme

Say so. Suggest the closest fit. Offer to proceed or to refine the brief. Example response:

> "Your topic — [X] — doesn't fit any of the six themes cleanly. The closest fit would be [Y theme] because [reason]. Do you want me to proceed with that, or would you like to narrow the topic?"

### When the user provides incomplete data

Ask for what's missing once. If the user can't provide it, use estimates with explicit `est.` labeling and call it out in the methodology footer.

### When the user asks for sensitive financial recommendations

Decline. data-craft pieces describe data; they do not advise. Offer to produce an informational piece that presents the data without recommendations.

### When the user requests a theme variation

If they ask for "Sand Hill but darker" or "Pitch Black but with red instead of green," gently push back: the themes are deliberately distinct so they're recognizable. Offer to do a one-off custom variation, but flag that it won't match the documented theme.

### When the user wants to mix themes in a single piece

Don't. Pick one theme per piece. Suggest: "Use Sand Hill for the main report, Trading Floor for the data appendix" — different pieces, each in their own theme.

### When the user requests a tone modifier

If the user asks for "spicy," "punchy," "more measured," "academic," "with more attitude," "more reserved," or any similar modifier, interpret it **within the theme's existing voice range**. Don't break theme to match modifier.

- **Compatible combinations** (lean in): "spicy Helvetica Riot" → sharper editorial framing, more callout-box takes, harder period-as-weapon rhythm. "Measured Sand Hill" → longer sentences, more caveats inline. "Punchy Pitch Black" → even shorter declarative bursts.
- **Incompatible combinations** (push back gently): "spicy Apollo White" → Apollo White is precise spec-sheet voice; spicy is not in range. Offer Helvetica Riot or Pitch Black instead. "Academic Helvetica Riot" → defeats the theme's whole point; suggest Sand Hill.
- **Universal**: never let a tone modifier override data integrity. Sharp editorial framing is fine; misrepresenting figures to fit the tone is not.

When a modifier is incompatible, explain briefly and offer alternatives — don't silently produce a watered-down or theme-violating piece.

---

## What you do at the start of every generation

1. **Read the relevant theme card** in `themes/[theme-name].md` for design tokens, voice profile, and layout patterns
2. **Web search** for current data on the topic if it involves time-sensitive figures
3. **Confirm the theme choice** with one sentence if you picked it autonomously: *"I'll build this as a Trading Floor tearsheet since it's an equity research piece — let me know if you'd prefer another theme."*
4. **Generate the file** following the universal conventions and the theme-specific rules
5. **Save to** `/mnt/user-data/outputs/[topic-slug].html`
6. **Present the file** to the user with `present_files` and a brief note about what you built

### When the user asks for preview selection

If the user asks to choose a visual direction, compare all six themes before generating the full HTML:

- theme name
- what it would make the topic feel like
- one sample headline
- one tradeoff
- final recommendation

Then wait for the user to pick, unless they explicitly ask you to proceed.

### When the user asks for PDF export

Prefer browser print for quick export. For automated export, recommend a headless browser workflow such as Playwright. Ensure the HTML has print-safe CSS and check that charts, methodology footer, and dense tables do not clip.

### When the user asks for slides

Do not turn data-craft into a generic slide generator by default. Offer "briefing-to-deck" as a downstream export:

> "I can turn this briefing into a 6-slide executive summary using the same theme language."

Keep the core data-craft artifact as a research briefing unless the user clearly asks for slides.

---

## Reference: the six golden examples

Each example demonstrates one theme's complete execution. Study these when you need to recall how a theme actually looks and sounds in practice. They are the reference implementation.

| Theme | Example file | Topic |
|---|---|---|
| Sand Hill | `examples/ai-coding-tools.html` | The AI Coding Tools Race |
| Pitch Black | `examples/humanoid-robotics.html` | The State of Humanoid Robotics |
| Trading Floor | `examples/nvda-tearsheet.html` | NVDA Single-Stock Tearsheet |
| Helvetica Riot | `examples/ai-music-wars.html` | The AI Music Wars |
| Sunday Press | `examples/d2c-coffee.html` | The Coffee Wars |
| Apollo White | `examples/spacex-ipo.html` | SpaceX IPO Briefing |

When in doubt about how a theme handles a specific layout problem (e.g., "what does a Trading Floor table look like?"), open the relevant example and mirror its approach.
