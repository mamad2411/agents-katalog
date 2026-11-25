---
name: design-master
description: "Unified design mega-skill for all artifact types: web pages, landing pages, dashboards, UI components, posters, graphics, and interactive artifacts. Combines best practices from frontend-design, ui-ux-pro-max, canvas-design, and web-artifacts-builder with a built-in quality gate."
group: design
triggers:
  - "дизайн"
  - "UI"
  - "компонент"
  - "страница"
  - "дашборд"
  - "постер"
  - "лендинг"
  - "визуал"
  - "сделай красиво"
output: "production-ready HTML/CSS/JS artifact or UI component"
calls: []
---

# Design Master — Unified Design Intelligence

This skill governs all design work. Use it whenever producing any visual artifact.
It detects the artifact type, applies the correct approach, and enforces quality standards
before delivery.

---

## Trigger Conditions

Use this skill when the user asks to:
- Build a web page, landing page, or website section
- Create a dashboard, admin panel, or UI component
- Make a poster, visual, graphic, or presentation
- Build an interactive artifact or React component
- "Make it look good / beautiful / professional"
- Design anything — if it has visual output, this skill applies

---

## Step 0: Context — Is there an existing UX/UI?

Before any other step — ask one question:

> "Это новый проект или в нём уже есть существующий UX/UI?
> Если есть — опиши коротко: что сейчас есть, что тебя не устраивает
> концептуально (не визуально)?"

**If project is new** → proceed to Step 1 as normal.

**If UX/UI already exists** → do NOT go to Step 1 immediately.
First perform an audit and propose concepts:

### 0a. Audit the existing UX

Ask the user to describe (or look in the project):
- What is the current navigation paradigm? (sidebar / tabs / wizard / flat list)
- What is the user's mental model? (what they "do" in the app)
- What are the key user flows? (3–5 of them)
- What works poorly — not visually, but behaviorally?

### 0b. Propose 2–3 conceptually different directions

Each direction is a different UX paradigm, not a different color.

Example format:
> **Направление A: [Название]**
> Парадигма: [одно предложение о том, как пользователь взаимодействует]
> Навигация: [как организована]
> Ключевое отличие от текущего: [что меняется концептуально]
>
> **Направление B: [Название]**
> ...
>
> **Направление C: [Название]**
> ...

**Mandatory structure of three directions:**
- **Direction A — Evolution:** same paradigm, improved. Fixes known issues without changing the model.
- **Direction B — Alternative:** different navigation model or information organization principle.
- **Direction C — Destructive:** ask "what if we remove [the main entity of the current UX]?"
  Examples: no sidebar → command palette; no cards → timeline; no tables → conversational UI.
  Direction C must make the user either accept the challenge or consciously explain why not.

Wait for the user's choice. Only after they choose → proceed to Step 1.

**Rules:**
- "Make the same thing prettier" is not a valid direction if the user asked for a redesign from scratch.
- Direction C is mandatory. If the user rejects it — record the reason in one line before continuing.

---

## Step 1: Artifact Type Detection

Before doing anything, identify the artifact type:

| Keywords / Context | Type | Approach |
|---|---|---|
| landing page, website, hero, about, pricing | **Web / Landing** | Bold aesthetic + CSS variables |
| dashboard, admin, monitor, KPI, table, stats | **Dashboard / UI** | Severity system + component library |
| poster, visual, graphic, infographic, art, illustration | **Poster / Graphic** | Philosophy-first + 90% visual |
| React, shadcn, interactive, component, app | **Interactive** | React 18 + Tailwind + shadcn/ui |
| Ambiguous | Default to **Web / Landing** approach |

---

## Step 1b: Style Direction — Ask Before Generating

**If the user hasn't specified a style** — show the menu and wait for a choice.
Never choose a style independently as a "safe default".

**Web / Landing:**
> Какой характер у дизайна?
> `A` Brutally minimal · `B` Editorial/magazine · `C` Retro-futuristic
> `D` Organic/natural · `E` Luxury/refined · `F` Maximalist chaos
> или опиши ключевое слово / референс

**Dashboard / UI:**
> Тема:
> `A` Dark & sharp (синевато-тёмный) · `B` Light & clean (белый, минимал)
> `C` Vibrant (яркие акценты) · `D` Terminal (зелёный/чёрный)

**Poster / Graphic:**
> Mood:
> `A` High contrast · `B` Pastel/soft · `C` Psychedelic/glitch · `D` Geometric

If the user provided a reference or style — skip this step, use their description directly.

---

## Step 2: Pre-Flight Design System (all types except Poster)

Before writing any code, generate the design system:

```bash
py ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
```

Extract from user request:
- **Product type**: SaaS, dashboard, landing page, e-commerce, portfolio, etc.
- **Industry**: fintech, healthcare, gaming, beauty, etc.
- **Style keywords**: minimal, playful, dark mode, elegant, etc.

For multi-page projects, persist the design system:
```bash
py ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

**If Python is unavailable** — skip this step and apply the rules in Step 3 manually.

---

## Step 3: Type-Specific Approach

### A. Web / Landing Page

**Aesthetic Direction — choose ONE and commit:**
brutally minimal · maximalist chaos · retro-futuristic · organic/natural · luxury/refined
· editorial/magazine · brutalist/raw · art deco/geometric · industrial/utilitarian · soft/pastel

**Rules:**
- NEVER use Inter, Arial, Roboto, or system fonts as primary — pick a distinctive display font
- NEVER use purple gradients on white backgrounds
- NEVER produce cookie-cutter centered layouts — use asymmetry, diagonal flow, overlap
- Use CSS variables for ALL colors and spacing (never hardcoded hex in component code)
- One bold typographic statement per section (large display, tight tracking, dramatic weight)
- Backgrounds: gradient meshes, noise textures, geometric patterns, grain overlays — not solid white/grey
- Animations: staggered page load reveals, scroll-triggered entrances, hover states that surprise
- Animation timing: 150–300ms micro-interactions, transform/opacity only (never width/height)

**Structure:**
```css
:root {
  --bg: ...;         /* page background */
  --surface: ...;    /* card backgrounds */
  --text: ...;       /* primary text */
  --muted: ...;      /* secondary text */
  --accent: ...;     /* primary brand color */
  --accent2: ...;    /* secondary accent */
  --r: ...;          /* border radius */
}
```

---

### B. Dashboard / Admin Panel / UI Components

**Rules:**
- Use the full severity color system consistently (see CSS below)
- Dark OR light theme — never unintentional mixing
- ALL icons: SVG only (Heroicons or Lucide) — zero emoji in UI
- KPI cards always have top-border severity indicator
- Every clickable element has `cursor-pointer`
- Hover states: color/shadow transitions only, no layout shift
- Tables: left border by severity on rows

**Dark theme CSS variables (copy verbatim):**
```css
:root {
  --bg:      #07090f;
  --surface: #0d1117;
  --s2:      #131c27;
  --s3:      #18253a;
  --border:  #1e2d3d;
  --border2: #2a3f57;
  --text:    #dce8f6;
  --muted:   #4e6278;
  --muted2:  #637b95;
  --accent:  #38bdf8;
  --green:   #34d399;
  --crit:    #f43f5e;
  --high:    #fb923c;
  --med:     #fbbf24;
  --low:     #60a5fa;
  --r:  5px;
  --r2: 8px;
}
```

**Component vocabulary** (from `ui-component-library`):

| Class | Component |
|---|---|
| `.kpi` / `.kpi-row` | Stat cards with top color strip |
| `.s-ring` (SVG) | Score ring: `r=13`, C=82, rotate(-90deg) |
| `.badge-SEVERITY` | Severity pill (CRITICAL/HIGH/MEDIUM/LOW) |
| `.sig-col` / `.sig-row` | Horizontal signal bars (width ∝ score%) |
| `.bchart` / `.brow` | Bar chart: label + track + fill + stat |
| `.panel` / `.panel-hdr` | Surface card with uppercase header |
| `.sec-hdr` | Section header with right-extending decorative line |

For full component CSS + HTML, reference `~/.claude/skills/ui-component-library/SKILL.md`.

---

### C. Poster / Graphic / Visual

**Rules:**
1. **Philosophy first** — write 4–6 sentences about the aesthetic vision BEFORE any code.
   What emotion does it evoke? What composition principle guides it? What is the one idea?
2. **90% visual, 10% text** — text is a sparse visual element, not explanatory prose
3. Output as self-contained HTML artifact (inline CSS, SVG, or Canvas API)
4. Composition: asymmetric balance, golden ratio or rule of thirds, deliberate negative space
5. Color: 2–3 colors maximum, one dominant, one accent, one neutral
6. The work should feel as if it took countless hours — refinement over addition
7. Embed subtle conceptual references — informed viewers intuit meaning, others see beauty

**Template structure:**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { width: 800px; height: 600px; overflow: hidden; background: ...; }
    /* All styles inline — no external dependencies */
  </style>
</head>
<body>
  <!-- 90% visual elements: SVG, canvas, geometric shapes, typography as art -->
</body>
</html>
```

---

### D. Interactive Artifact (React / shadcn / Tailwind)

**Stack:** React 18 + TypeScript + Tailwind CSS 3 + shadcn/ui

**Rules:**
- NEVER: excessive centered layouts, purple gradients, uniform rounded corners, Inter font
- shadcn/ui components: Button, Card, Dialog, Select, Input, Badge, Tabs, etc.
- Self-contained single HTML file (bundle with Vite/Parcel if needed)
- For generative/parametric work: seed-based randomness for reproducibility
- Include interactive parameter controls (sliders, toggles) for generative artifacts
- P5.js for algorithmic/generative art — seed navigation (prev/next/random/jump)

**Anti-patterns to avoid:**
```
❌ <div className="flex flex-col items-center justify-center min-h-screen">
❌ gradient-to-r from-purple-500 to-blue-500
❌ rounded-full on every element
❌ font-family: Inter everywhere
```

---

### D2. Library Palette — When to Use What

#### animate-ui (animated components, React + Tailwind + Motion)

Use when: wow-effects needed, animated backgrounds, live buttons, micro-interactions.

**Install via Shadcn CLI:**
```bash
npx shadcn@latest add "https://animate-ui.com/r/<component-name>"
```

**Components by category:**

| Category | Components |
|----------|-----------|
| **Buttons** | `button`, `copy-button`, `flip-button`, `liquid-button`, `ripple-button`, `icon-button`, `github-stars-button`, `theme-toggler-button` |
| **Backgrounds** | `bubble`, `fireworks`, `gradient`, `gravity-stars`, `hexagon`, `hole`, `stars` |
| **Animate UI** | `avatar-group`, `code`, `code-tabs`, `cursor`, `tabs`, `tooltip`, `github-stars-wheel` |
| **Radix UI** | `accordion`, `alert-dialog`, `checkbox`, `dialog`, `dropdown-menu`, `files`, `hover-card`, `popover`, `progress`, `radio-group`, `sheet`, `sidebar`, `switch`, `tabs`, `toggle`, `tooltip` |
| **Community** | `flip-card`, `motion-carousel`, `notification-list`, `pin-list`, `playful-todolist`, `radial-menu`, `radial-nav`, `share-button`, `user-presence-avatar` |

**Rules:**
- Always check `prefers-reduced-motion` — animate-ui doesn't do this automatically
- Liquid/Ripple buttons — only for primary CTA, not all buttons
- Gravity Stars / Fireworks backgrounds — only for hero sections, not under content

---

#### heroui (production UI library, 50+ components, npm)

Use when: production-ready component library needed with accessibility (React Aria), forms, tables, navigation.

**Install:**
```bash
npm install @heroui/react
# or individual component:
npx heroui-cli@latest add <component-name>
```

**Provider (required at root):**
```tsx
import { HeroUIProvider } from "@heroui/react";
export default function App() {
  return <HeroUIProvider><YourApp /></HeroUIProvider>;
}
```

**Components by category:**

| Category | Components |
|----------|-----------|
| **Form** | Input, Select, Checkbox, Radio, Switch, Textarea, Autocomplete, Slider, Calendar, DatePicker |
| **Navigation** | Navbar, Breadcrumbs, Tabs, Pagination, Link |
| **Feedback** | Alert, Badge, Spinner, Progress, Toast |
| **Overlays** | Modal, Popover, Dropdown, Tooltip, Drawer |
| **Data** | Table, Card, Avatar, Image, User, Chip |

```tsx
import { Button } from "@heroui/react";
// variants: solid | bordered | light | flat | faded | shadow | ghost
// colors:   default | primary | secondary | success | warning | danger
<Button color="primary" variant="shadow">Action</Button>
```

**Rules:**
- HeroUI has its own theme — don't mix with Tailwind custom colors without configuration
- For dark mode: add `dark` class to `<html>` — HeroUI picks it up automatically
- Don't use together with shadcn/ui on the same components — style conflicts

---

**Library selection for Interactive tasks:**

```
Need animations / wow-effects / live backgrounds?
├── Yes → animate-ui (+ shadcn/ui for base components)
└── No → need full product UI with forms and tables?
    ├── Yes → heroui
    └── No → shadcn/ui (default)
```

---

## Universal Design Rules (All Types)

### Typography
- Body: line-height 1.5–1.75, max 65–75 characters per line
- NEVER use emoji as icons — SVG icons only (Heroicons, Lucide, Simple Icons)
- Font pairing: distinctive display font + refined body font
- Minimum 16px body text on mobile

### Accessibility (CRITICAL)
- Color contrast minimum 4.5:1 for normal text
- All interactive elements: visible focus ring
- Icon-only buttons: `aria-label` required
- All images: `alt` text
- Form inputs: `<label for="">` required
- `prefers-reduced-motion` must be respected

### Touch & Interaction (CRITICAL)
- Minimum 44×44px touch targets
- `cursor-pointer` on ALL clickable elements
- Button disabled during async operations
- Error messages appear near the problem

### Layout
- `viewport-meta`: `width=device-width, initial-scale=1`
- No horizontal scroll at any breakpoint
- Responsive at: 375px / 768px / 1024px / 1440px
- Fixed navbars: add `top-4 left-4 right-4` spacing, account for height in content

### Icons
- Icon set: Heroicons or Lucide — consistent across project
- Brand logos: verify from Simple Icons before using
- Fixed viewBox (24×24) with consistent sizing

---

## Quality Gate — MANDATORY before delivery

Run this checklist internally before showing the result. If ANY item fails, fix it first.

```
DESIGN QUALITY GATE
═══════════════════════════════════════════════════════
[ ] 1. Typography distinctive?
        → Not Inter/Arial/Roboto without customization
        → Has a clear typographic personality

[ ] 2. Would a designer be impressed?
        → If answer is "probably not" — redesign the boldest element
        → One thing should be truly memorable

[ ] 3. No purple gradient on white?
        → If yes — replace with something intentional

[ ] 4. Color contrast ≥ 4.5:1?
        → Check primary text against its background
        → Check muted text too (often fails)

[ ] 5. Hover states without layout shift?
        → cursor-pointer on every clickable element
        → Transitions use color/opacity, not width/height

[ ] 6. Responsive at 375px, 768px, 1440px?
        → No horizontal scroll
        → Text readable without zooming

[ ] 7. SVG icons, zero emoji?
        → Search output for emoji characters
        → Replace all with SVG equivalents
═══════════════════════════════════════════════════════
ALL 7 MUST PASS. Do not deliver until they do.
```

---

## Integration with Sub-Skills

| When | Delegate to |
|---|---|
| Need full design system generated via Python | `ui-ux-pro-max` (run search.py) |
| Building dark dashboard with components | `ui-component-library` (copy component CSS/HTML) |
| Need brand color extraction from PDF/PNG | `extract-brand-palette` |
| User explicitly requests detailed UX audit | `ui-ux-pro-max` (full checklist mode) |
| Need animated components / wow backgrounds | `animate-ui` (Shadcn CLI install) |
| Need production UI kit with 50+ components | `heroui` (npm install @heroui/react) |

---

## Quick Decision Tree

```
User wants something visual?
├── Dashboard / data / KPI / admin?
│   └── → Approach B (Dashboard) + ui-component-library
├── Poster / graphic / visual art?
│   └── → Approach C (Philosophy-first)
├── React / interactive / generative?
│   └── → Approach D (React/shadcn)
└── Everything else (web, landing, page)?
    └── → Approach A (Web/Landing) + pick bold aesthetic direction
```

Every path ends with: **Quality Gate (all 7 checks)**.

---

## Delivery

### File structure
When creating a Web / Landing artifact — always save as `<project-slug>/index.html`,
not a flat file in the root directory. Create the folder first.

```bash
mkdir <project-slug> && write to <project-slug>/index.html
```

### Preview (Windows + VS Code Remote SSH)
```bash
cd <project-slug> && py -m http.server 3000
```
> Use `py` (Python Launcher) — not `python` or `python3`.
> On Windows, `python` may resolve to the Microsoft Store stub (exit code 49).

**VS Code Remote SSH:** port 3000 appears in the **Ports** tab automatically →
click the globe icon or open `http://localhost:3000` in your browser.
