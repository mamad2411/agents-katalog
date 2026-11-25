---
name: visual-library
description: >
  视觉风格宝库 — 一个逐渐累积的 HTML 产出物视觉风格系统。
  按产出物类型组织（report / slides / demo-pc / demo-mobile），每种类型下有多个可选风格预设。
  ALWAYS load this skill when generating any HTML artifact — report, slides, interactive demo, or visualization.
  Load alongside the task-specific skill (ai-product-tasting, pattern-tracker, etc.) to apply the right visual style.
  When the user says "帮我出一个报告/做个slides/做个demo"、"用XX风格"、"换个风格"、"加个新风格进来", trigger this skill.
---

# Visual Library — 视觉风格宝库

A growing collection of curated visual styles for HTML artifacts, organized by output type.
Not a CSS framework. A taste library — every preset is a set of opinionated design decisions
that produces a distinctive, non-generic result.

---

## Philosophy

1. **Anti-slop** — Every preset exists because it looks like a human designer made it, not an AI.
   If a style could be produced by any generic "make it pretty" prompt, it doesn't belong here.
2. **Accumulative** — This library grows over time. When you see a visual style you like (in a
   project, on the web, in someone else's work), distill it into a preset and add it.
3. **Opinionated, not flexible** — Each preset makes strong choices. Want something different?
   Pick a different preset, don't dilute an existing one.
4. **Three-file rule** — Every preset has exactly three deliverables: a token file (the decisions),
   an example file (proof it works), and a preview image or URL (so you can browse without reading CSS).

---

## Directory Structure

```
visual-library/
├── SKILL.md                          ← you are here (router + conventions)
├── CONTRIBUTING.md                   ← how to add a new preset
├── presets/
│   ├── html-report/                  ← long-form scrollable documents
│   │   ├── _README.md                ← category constraints & shared rules
│   │   ├── scholar/                  ← preset: 克制学术风
│   │   │   ├── TOKENS.md             ← design tokens + component specs
│   │   │   ├── example.html          ← working example file
│   │   │   └── preview.png           ← screenshot for browsing (or URL in TOKENS.md)
│   │   ├── editorial/                ← preset: 编辑部风 (future)
│   │   └── .../
│   ├── html-slides/                  ← 16:9 presentation decks
│   │   ├── _README.md
│   │   └── .../
│   ├── html-demo-pc/                 ← interactive demos, desktop viewport
│   │   ├── _README.md
│   │   └── .../
│   └── html-demo-mobile/             ← interactive demos, mobile-first
│       ├── _README.md
│       └── .../
└── gallery/                          ← (optional) collected reference screenshots
    └── .../                             with source URLs, for inspiration
```

---

## Output Types & Their Constraints

Each output type has fundamentally different constraints. A style that works for one
may not work for another — that's why presets live under their type, not globally.

### html-report
Long-form scrollable documents. Analysis reports, 品鉴报告, competitive briefs, pattern profiles.

**Hard constraints:**
- Single-column, max-width 780px, responsive to mobile
- Must be readable as a continuous scroll — no pagination
- Typography must support mixed Chinese + English + code
- Tables must handle 4-7 columns on desktop, horizontal scroll on mobile
- No JavaScript required (static HTML + CSS)

**Typical components:** header, sections, callouts, tables, diagrams, verdict cards, timeline, footnotes

### html-slides
Presentation decks for sharing, embedding, or presenting.

**Hard constraints:**
- Fixed 16:9 aspect ratio (1920×1080 authored, scaled to viewport)
- Keyboard + touch navigation
- Each slide is a self-contained visual unit
- Must work full-screen
- Minimal text per slide — visuals carry the message

**Typical components:** title slide, content slides, comparison slides, quote slides, closing slide

### html-demo-pc
Interactive demonstrations or prototypes, desktop viewport.

**Hard constraints:**
- Minimum 1024px viewport assumed
- May include interactive elements (buttons, inputs, tabs, state changes)
- React or vanilla JS
- Must feel like a real product, not a prototype wireframe

**Typical components:** nav, panels, cards, forms, data displays, modals

### html-demo-mobile
Interactive demonstrations, mobile-first (375px-428px primary).

**Hard constraints:**
- Touch-first interaction
- Bottom navigation pattern
- Large tap targets (min 44px)
- Single-column or swipeable layouts
- Performance-conscious (no heavy animations)

**Typical components:** bottom nav, cards, pull-to-refresh, swipeable panels, sheets

---

## How to Use This Skill

### When generating an HTML artifact:

1. **Identify the output type** from the task context (report? slides? demo?)
2. **Check available presets** under that type's folder
3. **If the user named a style** → load that preset's TOKENS.md
4. **If no style named** → suggest 1-2 presets that fit the task, or ask
5. **Generate** using the preset's tokens, components, and anti-patterns
6. **Drop the example.html path** in case the user wants to see the reference

### When the user wants to add a new style:

→ Follow CONTRIBUTING.md

### When the user says "换个风格":

→ Show available presets for the current output type (name + one-line description + preview link)
→ Let them pick
→ Regenerate with the new preset

---

## Preset Anatomy (TOKENS.md Format)

Every preset's TOKENS.md follows this structure:

```markdown
---
preset_name: scholar
chinese_name: 克制学术风
output_type: html-report
origin: "Computer Use 主战场分析报告 (2026-09-04)"
one_liner: "Noto Serif SC 标题 + Inter 正文 + JetBrains Mono 元数据，warm off-white 底，三色语义 callout"
tags: [analytical, bilingual, data-heavy, restrained]
---

## Design Decisions
[What this style chooses to do and NOT do — the taste, not just the tokens]

## Color Palette
[CSS custom properties with semantic names and usage notes]

## Typography
[Typefaces, scale, weights, line-height — with import link]

## Components
[Each component: what it looks like, when to use it, HTML snippet]

## Anti-Patterns
[What breaks this style — specific things to avoid]

## Full CSS
[Copy-paste ready CSS block]
```

---

## Currently Available Presets

| Type | Preset | Chinese | One-liner | Origin |
|------|--------|---------|-----------|--------|
| html-report | `scholar` | 克制学术风 | Serif 标题 + Sans 正文，三色 callout，verdict 深色卡 | Computer Use 深度拆解 (2026-09) |

> This table grows as presets are added. Keep it updated.

---

## Cross-Skill Integration

| Task Skill | Default Output Type | Recommended Preset |
|------------|--------------------|--------------------|
| ai-product-tasting (品鉴报告) | html-report | `scholar` |
| pattern-tracker (pattern profile) | html-report | `scholar` |
| pattern-tracker (library dashboard) | html-demo-pc | TBD |
| pattern-tracker (trend map) | html-demo-pc | TBD |
| ui-design-prompt | html-demo-pc / mobile | TBD |

As new presets accumulate, this mapping may offer multiple options per task.
