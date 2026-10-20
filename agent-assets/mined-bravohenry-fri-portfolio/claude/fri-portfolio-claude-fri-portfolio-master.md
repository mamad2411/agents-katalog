# fri-portfolio — Agent-powered portfolio + content platform
Next.js 16 + TypeScript + Tailwind CSS 4 + marked + Vercel SSG

<directory>
content/ — Agent write target: markdown + frontmatter (2 subdirs: diary, weekly)
src/app/ — Next.js App Router (5 routes: /, /diary, /weekly, /diary/[slug], /weekly/[slug])
src/components/ui/ — Shared UI primitives: GlassPanel, TechBorder, ProgressBar
src/components/home/ — Homepage dashboard components (9 client components with animations)
src/components/content/ — Content page components: EntryList, EntryPage
src/lib/ — Content pipeline: content.ts (abstraction layer), markdown.ts (renderer + link preview), og.ts (OG metadata fetcher)
src/styles/ — globals.css: theme vars, Tailwind, all keyframe animations
public/ — Static assets: core.mp4, avatar.jpg, favicon.png
docs/ — Design spec and implementation plan
</directory>

<config>
next.config.ts — Next.js configuration
tailwind.config.ts — Brand colors (neon-pink, neon-coral) + custom font families
tsconfig.json — TypeScript paths (@/ alias to src/)
postcss.config.mjs — PostCSS with Tailwind plugin
eslint.config.mjs — ESLint configuration
</config>

## Content Pipeline
Agent writes `content/{type}/{slug}.md` with frontmatter (title, date, summary).
`lib/content.ts` reads filesystem, parses frontmatter, renders via `lib/markdown.ts`.
Bare URLs in markdown auto-enriched to glass-panel link preview cards at build time.
OG metadata cached in `.cache/og/` for fast rebuilds.

## Content Types
- **Weekly** (`/weekly`) — Public, English, design engineering content. Primary navigation.
- **Diary** (`/diary`) — Semi-private, Chinese, personal journal. Hidden easter egg nav.

## Key Conventions
- Homepage components are `"use client"` (animations/timers via useEffect)
- Content pages are server components (zero JS, pure SSG via generateStaticParams)
- Visual theme: cyberpunk, neon pink #ec4899, glass morphism, VT323 pixel font
- Agent workflow: git push to content/ -> Vercel auto-build -> live

## Agent Authoring Contract
```yaml
---
title: "Article Title"
date: 2026-03-29
summary: "Optional one-liner for list page"
---

Markdown content here. Bare URLs on their own line become link preview cards.
```

[PROTOCOL]: update this file when architecture changes, then check subdirectory CLAUDE.md files
