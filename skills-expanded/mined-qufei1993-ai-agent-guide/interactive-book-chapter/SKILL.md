---
name: interactive-book-chapter
description: Create or update zero-build interactive HTML chapters (Chinese zh/ and English en/) for the AI Agent Full-Stack Roadmap static site. Use whenever the user asks to turn a Markdown chapter into an interactive HTML explainer, add a new chapter or English translation to ai-agent-guide, or update chapters.json and shared navigation.
---

# Interactive Book Chapter Skill

Turn technical Markdown chapters into zero-build, single-HTML interactive explainers for `ai-agent-guide`, keeping narrative flow, interactive labs, TypeScript references, and bilingual (`zh/` + `en/`) structure consistent.

## Site Layout

All static pages live under `docs/` (zero-build, ready for GitHub Pages), while runnable TypeScript examples live alongside them under `examples/`:

```text
├── docs/                       # GitHub Pages static site (isolated, zero-build)
│   ├── index.html              # Language router (auto-detects zh/en)
│   ├── chapters.json           # Bilingual catalog, siteUrl & langs availability
│   ├── sitemap.xml             # Auto-generated bilingual sitemap (xhtml:link)
│   ├── robots.txt              # Auto-generated robots.txt
│   ├── shared/
│   │   ├── tokens.css          # Design tokens, dark mode, layout, lab/code/hook primitives
│   │   └── site.js             # Global topbar, chapter drawer, floating TOC, lang switcher
│   ├── zh/<slug>.html          # Chinese chapter
│   └── en/<slug>.html          # English chapter (identical slug)
├── examples/                   # Runnable TypeScript examples for chapters
│   └── <module>/<slug>/
└── scripts/
    └── generate-seo.mjs        # Syncs chapter SEO tags, sitemap.xml & robots.txt
```

Read [html-architecture.md](references/html-architecture.md) before writing HTML: it documents the required `site.js` DOM contract, `tokens.css` class inventory, minimal page skeleton, inline SVG guidelines, and reusable JS boilerplate.

## Workflow

1. **Read the source chapter**: Extract the core engineering failure modes, real citations/URLs, and runnable TypeScript patterns.
2. **Design 2–3 interactive labs**: Pick mechanics that only become obvious through manipulation (e.g., attention decay, token budget overflow, rank fusion math, payload X-ray). Do not add decorative animations.
3. **Write BOTH `docs/zh/<slug>.html` AND `docs/en/<slug>.html` by default (Zero Bilingual Debt)**:
   - Unless the user explicitly requests a single language only, always deliver both `zh/` and `en/` in the same task so no translation backlog accumulates.
   - Link `../shared/tokens.css`, Prism.js (`prism-tomorrow.min.css`, `prism.min.js`, `prism-typescript.min.js`, `prism-json.min.js`), and `../shared/site.js`.
   - **GitHub Pages Bilingual SEO (Required in `<head>`)**: Read `siteUrl` from `docs/chapters.json` and include `<meta name="description">`, `<link rel="canonical">`, absolute-URL `<link rel="alternate" hreflang="zh-CN|en|x-default">`, Open Graph (`og:type`, `og:locale`, `og:title`, `og:description`, `og:url`), and a `TechArticle` JSON-LD block.
   - Reuse classes from `tokens.css` (including `.lab-toolbar`, `.split-2`, `.pane-box`, `.raw-stream`, `.pick-options`) instead of duplicating shared layout CSS in both HTML files.
   - Keep **identical section & lab anchor IDs** (e.g., `#lab-cleaning`, `#lab-chunking`, `#decision`) in both `zh/` and `en/` so `site.js` preserves `window.location.hash` when switching languages mid-page.
   - Keep `<nav class="topbar-nav">` with 4–5 section links; `site.js` moves them into `.floating-toc` on wide screens (`>= 1440px`) and keeps the topbar strictly for global navigation.
4. **Update `docs/chapters.json` & Regenerate Sitemap**: Add or update the chapter entry (`slug` matching `<slug>.html`, `status: "ready"`, and `"langs": ["zh", "en"]`), then run `node scripts/generate-seo.mjs` to refresh `docs/sitemap.xml` (with `xhtml:link` bilingual alternates) and `docs/robots.txt`.
5. **Verify (Code + Visual QA + Cross-Language Sync)**:
   - Run syntax checks (`node -e`) on **both** `zh/` and `en/` files and verify `0` console errors, interactive controls, hash-preserving `中 / EN` language switch, and light/dark themes in a real browser.
   - **Visual QA (Mandatory)**: Capture and inspect screenshots in both light and dark modes before finishing. Explicitly check: equal-height alignment in split panes, unified column alignment (`--page-width: 980px` across hero, prose, diagrams, and labs), dark-mode contrast inside code/highlight blocks, and zero stray ASCII straight quotes `""` in Chinese UI copy.

## Interactive Grammar (8 Core Patterns)

1. **Problem-first opening + 30-second TL;DR (`.tldr`)**: Start `.hero` with a concrete scenario, followed immediately by a `.tldr-card` listing 3 takeaways with `.tldr-go` jump buttons. Never open with a "What you will learn" list or end with a self-checklist.
2. **Experiential Section Rhythm (Hook → Interactive Lab → Visual Diagram → Concise Prose)**: Open each section with a 1–2 sentence hook (marked `p.key` so "Labs only" mode keeps it), jump into the lab so readers feel the failure mode firsthand, follow with a diagram, and close with concise prose and code.
3. **2–4 Choice-Driven & Mechanically Diverse Labs (`.lab-wrap`)**: Prefer "choice → consequence → fix" labs (`.pick-options` / `.pick-card` + `.outcome.bad/meh/good`) and manipulable sandboxes over static preset tabs or dense 20-number dashboards. **Anti-template rule**: keep the `.lab-card` shell consistent, but vary the *internal stage* across labs in the same chapter (e.g., inline document cut-line canvas, live parameter slider + distribution bar, split before/after X-ray)—never repeat the exact same "chip toolbar + 2-column box" layout for every lab.
4. **Self-Contained Lab Context**: State the test task, input payload, and constraints inside `.lab-body` so readers jumping straight to a lab never feel lost.
5. **Visual-First Diagrams (Theme-Aware Inline SVG)**: Use `.diagram-figure` with `tokens.css` CSS variables (`--bg-elevated`, `--text`, `--border`, `--teal-soft`, `--rose-soft`). Show state transformations, branching paths, or bottleneck contrast rather than plain "4 boxes + 3 arrows" labels.
6. **Predict → Verify in Lab (`.predict-hook` + `.predict-verify`)**: Pair counterintuitive predictions with a `.predict-verify` button that jumps to and configures the matching lab so readers verify the answer with their own eyes.
7. **Strict Data Provenance (`.src-tag` vs `.sim-tag` / `.bar-sim` / `.sim-zone`)**: Real benchmark/experiment numbers must carry `.src-tag` with a verifiable source; simulated or illustrative visuals must use `.sim-tag` / `.bar-sim` / `.sim-zone` (dashed border + diagonal stripes) and never share identical bar styling with real metrics.
8. **Code Integration (`details.code-fold` + Prism + Same-Repo GitHub Links)**: Keep runnable TypeScript inside `<details class="code-fold">` and sync key lab parameters into the code block + `Prism.highlightElement(codeEl)`. When linking to full runnable scripts in `examples/<module>/<slug>/`, always use full GitHub URLs pointing to this repository (`https://github.com/qufei1993/ai-agent-guide/blob/main/examples/...` or `tree/main/examples/...`)—never relative paths outside `docs/` (which 404 on GitHub Pages).

## Accuracy & Citations

- Preserve real citations, benchmark numbers, and source URLs from the Markdown source. Never invent paper metrics or fake links.
- Clearly label any pedagogical lab numbers as simulated (e.g., `模拟 16,000 Tokens 有效工作窗口` or `Simulated 16,000-token budget`) so readers never confuse interactive intuition with published benchmarks.

## Bilingual Sync Protocol (`zh/` ↔ `en/`)

- **Default dual-output**: Every new chapter generates both `docs/zh/<slug>.html` and `docs/en/<slug>.html` with the exact same `<slug>.html` and identical anchor IDs (`#section-*`, `#lab-*`, `#decision`).
- **Mandatory two-way sync on edits**: Whenever you edit, polish, fix a bug, or upgrade a lab in one language (e.g., `docs/zh/<slug>.html`), you **must** check whether its sibling (`docs/en/<slug>.html`) exists and immediately apply the equivalent structural, visual, or algorithmic fix to the sibling file in the same turn. If the sibling does not exist yet and the user asks to bring the chapter up to parity, create it.
- **Keep shared changes in `tokens.css` / `site.js`**: If a fix applies to shared layout or theme contrast (e.g., dark-mode active pill contrast, split-pane alignment), put it in `docs/shared/tokens.css` or `docs/shared/site.js` so all chapters in both languages inherit it automatically.
- **Idiomatic localization, not literal translation**: For `en/` chapters, rewrite prose and localize lab sample data into idiomatic engineering English (while keeping the exact same engineering failure mode and interactive mechanics).
- `site.js` reads `langs` from `docs/chapters.json` (with `cache: "no-cache"`) to enable or disable the `中 / EN` toggle without 404s and preserves `window.location.hash` on language switch.

## Chinese Writing Rules

- Use Chinese quotation marks `“”` (never straight ASCII `""` in Chinese prose).
- Never use em-dashes `——`; use commas, periods, or colons instead.
- Add spaces between Chinese characters and English words or numbers (e.g., `共 3 个实验台`, `使用 TypeScript 编写`).
- Do not use `第一、第二、第三` lists; use numbered `1. 2. 3.` or concise headings.
