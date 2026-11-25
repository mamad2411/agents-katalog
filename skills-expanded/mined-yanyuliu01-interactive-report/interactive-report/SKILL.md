---
name: interactive-report
description: >
  Generate editorial-quality interactive HTML documents for analysis, research, and structured information.
  Use this skill whenever the user says "summarize", "analyze", "整理", "总结", "做一个分析", "帮我梳理",
  "生成报告", or provides raw content (meeting notes, data, articles, financials) to be organized visually.
  Covers SWOT/Porter frameworks, data insights, meeting minutes, competitive comparisons, equity research,
  paper reviews, and any scenario where interactive HTML beats plain text. Even "帮我分析一下X" should trigger
  this skill. Also callable as a downstream skill by other skills needing interactive HTML rendering.
---

# Interactive Report Skill

Generate publication-quality interactive HTML documents. The output should read like a well-edited magazine 
article with embedded interactive elements — NOT like a SaaS dashboard or web app.

## Core Design Philosophy

**Content is the protagonist. Interaction is the supporting actor.**

The #1 mistake AI models make when generating interactive HTML is treating it as "building an app." The correct 
mental model is "typesetting a publication" — like a high-quality online longread or research brief, where 
interactive widgets (tabs, sliders, charts) are woven into the reading flow to aid comprehension.

Key principles:
- **Single-column reading flow** (max-width ~780px, centered) — never a multi-panel dashboard layout
- **Narrative arc** — Hero → Context → Analysis → Evidence → Conclusion, not just a grid of widgets
- **Three-typeface system** — serif for headings, sans-serif for body, monospace for labels/metadata
- **Numbered sections** with `section-label` dividers (e.g., `01 · 核心问题`) to create rhythm
- **Interactions embedded in prose** — a chart follows a paragraph that introduces it, not the other way around
- **Custom SVG diagrams** over generic chart libraries when the concept is structural (relationships, flows, comparisons)

## Workflow

### Step 0: Determine if called directly or as downstream

**Direct call**: The user asks you to analyze/summarize/organize something. You own the full pipeline — 
content research, information architecture, writing, and rendering.

**Downstream call**: Another skill has already structured the content and is asking you to render it as 
interactive HTML. In this case, respect the upstream skill's content organization, section ordering, and 
emphasis. Apply only the design system and component library from this skill. Do NOT reorganize the content 
or add new sections unless the upstream skill explicitly allows it.

### Step 1: Identify the scene type

Read the user's request and classify it into one of these scene types:

| Scene Type | Signals |
|---|---|
| **framework** | SWOT, Porter, BCG matrix, 波特五力, 竞争分析框架 |
| **data-insight** | 数据, 指标, 趋势, dashboard, 仪表盘, KPI, metrics |
| **meeting** | 会议, 纪要, minutes, 讨论, 待办, action items |
| **comparison** | 对比, 比较, vs, 竞品, 比选, 评测 |
| **research** | 行研, 研报, 股票, 财报, 公司分析, equity |
| **paper** | 论文, paper, arXiv, 精读, 文献, 综述 |
| **general** | anything else that needs structured presentation |

**Theme selection**: Two themes are available — "warm" (cream/paper, `#F7F5F0`) and "cool" (dark, `#101117`).
If the user specifies a preference, use it. If not, ask the user which theme they prefer before generating.
Both themes share the same component library and work identically — only the CSS variables differ.

### Step 2: Read the design system

**→ Read `references/design-system.md` now.** It contains the complete CSS variable definitions, typography 
rules, and base HTML structure for both themes. You MUST use these exact variables — do not invent your own 
color palette or font stack.

### Step 3: Read the component library

**→ Read `references/components/INDEX.md` first.** It lists all component files and tells you which ones 
to load based on your scene type. Then read the relevant component files:

- `references/components/layout.md` — Hero, Section Label, Widget Frame, Footer (ALWAYS read this)
- `references/components/content.md` — Callout, Formula, Metrics, Badges, Segmented Bar (ALWAYS read this)
- `references/components/interactive.md` — Tabs, Slider, Sortable Table, Chart.js (read if needed)
- `references/components/cards.md` — Comparison Grid, Risk Grid, People, Links, Verdict (read if needed)
- `references/components/svg-patterns.md` — SVG diagram templates (read if custom diagrams needed)

**Why hardcoded components matter**: This skill will be used across different models with varying frontend 
capabilities. By providing exact, tested code blocks, we ensure consistent output quality regardless of model 
strength. The model's job is to SELECT and ASSEMBLE components, not to invent CSS from scratch.

### Step 4: Plan the information architecture

Before writing any code, plan the document structure. Every document should follow this skeleton:

```
Hero (title, subtitle, metadata)
├── 01 · Context / Background
├── 02 · Core Analysis (main interactive section)
├── 03 · Supporting Evidence (charts, data, diagrams)
├── 04 · Implications / Impact
├── 05 · Key Actors / Entities (people, companies — if relevant)
├── 06 · Resources / References (if relevant)
└── Footer
```

Not all sections are needed for every document. A meeting summary might only need Hero → Topics (tabs) → 
Action Items → Timeline. A stock analysis needs all sections. Use judgment, but ALWAYS have:
- A Hero with contextual metadata
- At least one interactive widget embedded in the reading flow
- A concluding section with a callout box summarizing the key takeaway

**→ For scene-specific templates and assembly guides, read `references/templates.md`.**

### Step 5: Research content (direct call only)

If called directly (not downstream), you need to fill the document with accurate, substantive content. 
This is NOT a layout exercise — the content quality matters as much as the presentation.

- Use web search to gather current, accurate data
- For financial analysis: get real financial metrics, not placeholder numbers
- For paper reviews: read the actual paper or reliable summaries
- For competitive comparisons: verify feature claims against official sources
- Estimate data only when real data is unavailable, and label estimates clearly

### Step 6: Assemble and output

Assemble the HTML as a single self-contained file:
- All CSS in a `<style>` block in `<head>`
- All JS in a `<script>` block before `</body>`
- External dependencies (only Chart.js if charts are needed): load from CDN
- The ONLY allowed CDN dependency is: `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js`
- Everything else must be vanilla HTML/CSS/JS

Output the file:
- If `present_files` is available: save to `/mnt/user-data/outputs/` and present
- If creating an artifact: output as a single `.html` file
- If called downstream: return the HTML string to the calling skill

## Rules for Cross-Model Consistency

These rules exist because this skill will run on models with varying frontend capabilities. Following them 
ensures consistent output quality.

### ALWAYS do:
1. **Copy CSS variables verbatim** from design-system.md — never approximate colors or font stacks
2. **Copy component HTML structure verbatim** from components.md — adjust content, not markup
3. **Use the widget-frame wrapper** (with macOS dots) for ANY interactive element
4. **Use section-label dividers** (`01 ·`, `02 ·`, ...) for every major section
5. **Include the three-typeface system** — serif + sans + mono, as defined in design-system.md
6. **Keep max-width: 780px** on the page container
7. **Use SVG for structural diagrams** (relationships, flows, comparisons) — not Chart.js
8. **Use Chart.js ONLY for data with axes** (bar, line, radar, pie) — and follow the exact config pattern from components.md
9. **Put all JS at the end** in a single `<script>` block — no inline `onclick` except for simple tab/toggle
10. **Test the output mentally**: does it read like a magazine article? Or does it look like a Notion dashboard?

### NEVER do:
1. ❌ Use dark theme background for academic/consulting/research content (use warm theme)
2. ❌ Create multi-column dashboard layouts — always single-column reading flow
3. ❌ Use `display: grid` for the page layout (only for card grids within sections)
4. ❌ Import fonts from Google Fonts — use only system font stacks
5. ❌ Use any JS framework (React, Vue, etc.) — vanilla JS only
6. ❌ Create generic "card grids" as the main content — cards supplement prose, not replace it
7. ❌ Skip the Hero section — every document needs one
8. ❌ Use emoji as the primary visual language — use sparingly, prefer styled labels
9. ❌ Generate placeholder content like "Lorem ipsum" or "这里是描述" — every line must be substantive
10. ❌ Create more than one CDN dependency

## Content Quality Rules

These rules govern the relationship between prose, interaction, and visual elements. They are the 
difference between "a good-looking tool" and "a document that teaches."

### Narrative before interaction
The first section after the Hero must be **context/explanation**, not a control panel. Users need to 
understand "why" before they operate "how." An interactive widget should never appear before the concept 
it visualizes has been introduced in prose. Think of it as: textbook page first, lab exercise second.

### Co-locate related interactive elements
When multiple interactive elements are semantically linked (e.g., an array visualization, its step 
controls, and its call stack), put them inside a SINGLE widget-frame. Do not scatter them across 
separate sections — users should not need to scroll between related state.

### Prose depth per section
Every section must contain at least 2-3 sentences of substantive prose BEFORE any interactive widget. 
A section that is only a widget with no surrounding explanation fails the editorial test. Card grids 
with one-line descriptions do not count as prose — they are summaries, not explanations.

### Narration over logging
Dynamic explanatory text (step descriptions, status updates) must be written as complete natural 
language sentences, as if a teacher is narrating. Example: "比较 arr[3]=3 与 pivot=10：3 ≤ 10，需要
换入左区。" NOT: "compare: arr[3]=3, pivot=10, result=less". The former teaches; the latter reports.

### Concept diagrams are mandatory
Any document explaining a process, algorithm, or system MUST include at least one custom SVG diagram 
that illustrates the core concept visually. A document with only interactive widgets but no static 
concept diagram has a gap — the widget shows "what happens" but the diagram shows "how it works."

### Pointer and state annotation
When visualizing algorithms or processes with moving pointers/cursors/indices, explicitly label their 
current positions in the visualization (e.g., "i", "j", "pivot" markers above array bars). Users 
should never have to guess which element is being referenced — color alone is not enough.

## When called as downstream skill

If another skill calls this one to render pre-structured content:

1. The upstream skill provides: content hierarchy, section titles, body text, data points
2. This skill provides: HTML structure, CSS design system, interactive components, layout
3. Merge them: map upstream sections to this skill's component library
4. Respect upstream ordering — do not reorder sections
5. Apply the theme that best fits the upstream content type
6. Add interactive elements (tabs, sliders, charts) where they genuinely aid comprehension — 
   don't force interactivity where a simple paragraph suffices

## Reference files

| File | When to read | What it contains |
|---|---|---|
| `references/design-system.md` | Always, before writing any HTML | CSS variables, themes, typography, base structure |
| `references/components/INDEX.md` | Always, to decide which component files to load | Component index with loading guide per scene type |
| `references/components/layout.md` | Always | Hero, Section Label, Widget Frame, Footer |
| `references/components/content.md` | Always | Callout, Formula, Metrics, Badges, Segmented Bar |
| `references/components/interactive.md` | When tabs/sliders/tables/charts needed | Tabs, Slider, Sortable Table, Chart.js config |
| `references/components/cards.md` | When comparisons/people/links needed | Comparison Grid, Risk Grid, People, Links, Verdict, Timeline |
| `references/components/svg-patterns.md` | When custom SVG diagrams needed | 5 reusable SVG patterns |
| `references/templates.md` | When you need scene-specific guidance | Assembly guides for each scene type |

Read design-system.md and the relevant component files before generating ANY output.
