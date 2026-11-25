---
name: vibe-deck
description: >
  Vibe Deck — vibe-code professional slide presentations — describe what you
  want, AI builds it. Scaffolds a React + ECharts project, creates slides with
  charts, animations, theming, and PDF export. Use PROACTIVELY when the user
  mentions slides, deck, presentation, PPT, PPTX, slideshow, keynote, pitch
  deck, quarterly review, board meeting, investor update, sales deck, training
  deck, onboarding slides, report presentation, add a slide, build a deck,
  create slides, make a roadmap slide, put this data into a presentation,
  turn this Excel into slides, visualize this data as a deck. Also trigger
  when the user wants to modify, reorder, or delete slides in an existing
  slide-kit project. Also trigger when the user wants to share, export, or
  package the deck as a single HTML file for email or offline viewing.
  Chinese triggers: 做PPT, 做个deck, 写pptx, 创建演示, 制作幻灯片, 做幻灯片,
  加一页, 新增slide, 做演示文稿, 工作汇报, 述职报告, 季度回顾, 方案展示,
  写个汇报, 改一下这页, 调整幻灯片顺序, 删掉这页, 把数据做成图表展示,
  帮我做个路线图, 导出单个HTML, 分享给别人看.
---

# VibeDeck

## Step 0: Environment Check

Before anything else, verify that Node.js and npm are available. Try these commands (use whichever works on the current platform):

```sh
node --version    # or: where.exe node (Windows)
npm --version     # or: where.exe npm (Windows)
```

- **Both exist and Node.js ≥ 20** → continue silently (do not mention the check to the user).
- **Missing or version too low** → do NOT proceed. Instead:
  1. Run `uname -s` and `uname -m` (or `systeminfo` on Windows) to detect the user's OS and architecture.
  2. If you have web search capability, search for the latest recommended way to install Node.js on the user's platform, and provide the specific commands.
  3. If you cannot search, show this message in the user's language:
     > **中文**: VibeDeck 需要 Node.js 20 或更高版本。请访问 https://nodejs.org 下载并安装适合你操作系统的版本，安装完成后重新运行。
     >
     > **English**: VibeDeck requires Node.js 20 or later. Please visit https://nodejs.org to download and install the version for your OS, then try again.
  4. Stop here and wait for the user to install before continuing.

## Step 1: Check Project

Check if `slide-kit.config.js` exists in the current directory.

- **Exists** → this is an existing slide-kit project. Go to [Building Slides](#building-slides).
- **Does not exist** → no project yet. Go to [Creating a New Deck](#creating-a-new-deck), then continue to Building Slides if the user also described content.

---

## Creating a New Deck

### 1. Ask for title

Only ask for the **project title** (required). Show defaults for everything else:

> I'll set up the project with these defaults unless you want changes:
> - **Directory**: `./<title-slug>/`
> - **Theme**: `corporate-blue` (also available: `minimal`)
> - **Logo**: built-in SlideKit logo
> - **Presenter**: none (can set later in config)
> - **Password**: none
>
> Let me know if you want to change any of these, or I'll proceed.

See [theme-presets.md](reference/theme-presets.md) for theme details.

### 2. Scaffold the project

```bash
cp -r <this-skill-dir>/template/ <target-dir>
cd <target-dir>
git init
```

No network required — the template is bundled in this skill.

### 3. Configure

- **`slide-kit.config.js`**: set `title`, `theme`, `logo`, `presenter` as needed
  - Custom primary color: use `overrides.colors.primary` — variants auto-derived
  - Custom logo: copy to `public/`, reference as `/filename.svg`
- **`index.html`**: set `<title>`
- **`src/App.jsx`**: remove PasswordGate if no password

### 4. Generate agent instructions

Read [instruction-template.md](reference/instruction-template.md), replace placeholders, write to both `CLAUDE.md` and `AGENTS.md`.

### 5. Install and start

```bash
npm install
npm run dev
```

Report: project location, theme, dev server URL.

---

## Building Slides

### 1. Read context (do this BEFORE planning)

Read these three files first — skipping this step leads to duplicated content, wrong theme colors, or missed conventions:

- `CLAUDE.md` (or `AGENTS.md`) — theme, conventions, data sources
- `src/App.jsx` — current slide list and ordering (what already exists)
- `slide-kit.config.js` — active theme and presenter info

### 2. Understand the request

- What content should this slide show?
- Is there data involved? Where does it come from?
- **Narrative continuity**: new slide should follow logically from the previous one
- **No duplication**: if a data point is already shown elsewhere, present from a different angle
- **Unit consistency**: confirm the same units as existing slides ($K vs $M, etc.)
- **Content density**: Check [content-rules.md](reference/content-rules.md) for minimum content density standards — slides with sparse content (< 10 visual elements, single-line card descriptions) are not acceptable.

### 3. Choose layout

See [layout-templates.md](reference/layout-templates.md) for code templates:

| Layout | Best for |
|--------|----------|
| **FullChart** | Single large chart + KeyMessage |
| **SplitView** | Side-by-side comparison |
| **MetricGrid** | Dashboard with N metric cards |
| **ComparisonView** | Before/after |
| **DataTable** | Tool comparison, feature matrix, pricing |
| **TimelineFlow** | Roadmap, milestones, phased plans |

Built-in slide templates (import from `src/slides/`):

| Template | Use case |
|----------|----------|
| `SlideCover` | Cover page (reads config.title automatically) |
| `SlideDivider` | Chapter divider/transition |
| `SlideAgenda` | Table of contents |
| `SlideThankYou` | Closing/Q&A page |

### 4. Build the slide

- **Layout: MUST use `SlideLayout`** for all content slides — it enforces Title → KeyMessage → Content order. See [layout-templates.md](reference/layout-templates.md)
- Charts: [chart-components.md](reference/chart-components.md)
- Style: [style-guide.md](reference/style-guide.md)
- Content: [content-rules.md](reference/content-rules.md)
- Colors: `import { colors } from '../theme'`

### 5. Register (checklist)

```jsx
import SlideXxx from './slides/SlideXxx'

// In <Deck>:
<Slide title="Page Title"><SlideXxx /></Slide>
```

Before moving on, verify:
- [ ] `import` added at top of App.jsx
- [ ] `<Slide title="...">` — `title` is set (powers navigator, do NOT omit)
- [ ] Placed in correct position within `<Deck>` (narrative order)
- [ ] `footnote` prop set if slide uses external data

### 6. Storyline review (AFTER adding slides)

Every time new slides are added, re-read the full `<Deck>` in `App.jsx` and verify the overall narrative:

- [ ] **Logical flow**: Does each slide follow naturally from the previous one? Would the audience be confused by the transition?
- [ ] **Progressive disclosure**: Concepts introduced before they're referenced? (e.g., "What is a Skill?" must come before "Recommended Skills")
- [ ] **Audience-appropriate order**: For non-technical audiences, order from simple → complex, familiar → new (e.g., VS Code/Copilot before CLI tools)
- [ ] **No orphan slides**: Every slide belongs to a clear section. If a slide doesn't fit any section, it may not belong in this deck
- [ ] **Section balance**: Each section should have 2-5 slides. A section with 1 slide feels incomplete; a section with 8+ slides needs splitting
- [ ] **Title scan test**: Read ONLY the slide titles in order — does the story make sense from titles alone? If not, rename titles to be more descriptive

### 7. Layout verification (AFTER building)

After building each slide, visually verify the layout or use the layout checklist:

- [ ] **No bottom whitespace**: Content fills ≥ 80% of slide height. If bottom 20%+ is empty, use `justify-between` or add content
- [ ] **No bunched content**: Items should NOT cluster at the top with empty space below. Use `justify-center gap-4` or `justify-between` instead of `justify-start`
- [ ] **Consistent card heights**: In grid layouts, cards should have `h-full` so they stretch to fill their cell
- [ ] **Readable text hierarchy**: Title (28px font-black) → Section label (10px uppercase bold) → Card title (14px bold) → Body (12px) → Aux (10px). No adjacent sizes that blur hierarchy
- [ ] **Breathing room between sections**: Adjacent sections (e.g., "Details" and "Actions") need `mt-2` or `mt-3` gap — not `mt-auto` which pushes to bottom

### 8. Data extraction (if needed)

- Use `scripts/extract-xlsx.js` to inspect Excel structure
- Write a custom extraction script, verify totals match
- Save to `src/data/<name>.js`
- NEVER fabricate data

---

## Modifying Existing Slides

When the user asks to change, reorder, or remove slides in an existing deck:

### 1. Read context first

Same as Building Slides — read `CLAUDE.md`, `App.jsx`, and `slide-kit.config.js` before touching anything.

### 2. Editing a slide

- Open the slide component file (e.g., `src/slides/SlideRevenue.jsx`)
- Make the requested changes while preserving the existing layout pattern
- If the change involves data, update `src/data/` files and verify totals still match
- After editing, run the Layout verification checklist (Step 7 from Building Slides)

### 3. Reordering slides

- Reorder the `<Slide>` entries in `App.jsx` — this is the only file that controls order
- After reordering, run the post-edit verification below

### 4. Removing slides

- Remove the `<Slide>` entry from `App.jsx`
- Check if any other slide references data or concepts introduced by the removed slide — if so, move that context to an earlier slide
- Remove the slide component file if no longer imported
- Run the post-edit verification below

### 5. Replacing a slide's layout

If the user wants to change a slide from one layout to another (e.g., FullChart → SplitView):

- Read [layout-templates.md](reference/layout-templates.md) for the new layout's code template
- Rewrite the component using the new layout, preserving the data and keyMessage
- Verify the chart/content fits the new layout proportions

### 6. Post-edit verification (MANDATORY after ANY modification)

After every edit, reorder, or removal, do ALL of the following before reporting completion:

**Import cleanup** — scan `App.jsx` line by line:
- [ ] Every `import` at the top of `App.jsx` is actually used in the JSX below. Remove any that aren't (including leftover `config`, component, or data imports from removed slides)
- [ ] No slide component file imports modules that no longer exist

**Storyline review** — re-read the full `<Deck>` in `App.jsx` and verify:
- [ ] **Logical flow**: Does each slide follow naturally from the previous one?
- [ ] **Progressive disclosure**: Concepts introduced before they're referenced?
- [ ] **No orphan slides**: Every slide belongs to a clear section
- [ ] **Title scan test**: Read ONLY the slide titles in order — does the story make sense from titles alone?

Report the final slide order with titles to the user so they can confirm.

---

## Sharing as Single HTML

When the user wants to share the deck as a single portable HTML file (for email, IM, or offline viewing):

```bash
npm run build:single
```

This produces `dist-single/index.html` — a self-contained file with all JS, CSS, and SVG inlined. No server needed; just open in any browser.

**How it works:** `vite.single.config.js` uses `vite-plugin-singlefile` to inline all assets. The logo SVG is imported as a module (not a `/public` reference) so it gets bundled too.

**When to suggest this:** If the user says "share", "send to someone", "email the deck", "make it portable", "single file", "offline", or "不需要服务器".

**Limitations:**
- File size is ~380KB (ECharts + React bundle) — fine for sharing via email/IM, not ideal for web hosting
- Custom logos in `public/` (e.g., `config.logo = '/my-logo.png'`) are automatically inlined as data URIs by the build plugin — no extra steps needed

---

## Important Rules

- **NEVER fabricate data** — all numbers must come from source files
- When creating a project, generate BOTH `CLAUDE.md` and `AGENTS.md`
- `slide-kit.config.js` is the single source of truth for runtime config
- Slide components: `src/slides/Slide<PascalCaseName>.jsx`
- Data files: `src/data/<kebab-case-name>.js`
