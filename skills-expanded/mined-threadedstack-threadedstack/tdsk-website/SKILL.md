---
name: "tdsk-website"
description: "Knowledge base for the marketing site and documentation portal"
tags: ["react", "vite", "mui", "mdx", "docs", "marketing", "shiki", "mermaid", "landing-page"]
---
# Website Repo Skill

## Overview

- Public marketing site + documentation portal (`@tdsk/website`)
- Vite 5 dev server on port 5884, React Router v7, MUI 6 + Emotion
- Marketing pages: Landing, Features, Pricing, Use Cases
- Docs portal: MDX from root `/docs` directory with sidebar nav, TOC, Shiki highlighting
- Path aliases: `@TAF/*` via `alias-hq`

## Directory Structure

```
repos/website/
├── configs/
│   ├── vite.config.ts / vite.workspace.ts    # Vite config (MDX, SWC, SVGR, docs plugins)
│   ├── website.config.ts                      # Env loader, port (5884), aliases
│   ├── remarkDocsLinks.ts                     # Remark plugin: .md links → /docs/slug, images → /docs-assets/*
│   └── vitePluginDocsAssets.ts                # Dev middleware + build copy for doc images
├── src/
│   ├── App.tsx             # HelmetProvider → ThemeProvider → GlobalStyles → RouterProvider
│   ├── router.tsx          # Routes: MarketingLayout + DocsLayout
│   ├── components/
│   │   ├── Docs/           # ComingSoon, DocsPrevNext, DocsSidebar, DocsTableOfContents, MDXComponents, MermaidBlock
│   │   ├── Header/         # Header, MobileMenu, ThemeToggle
│   │   ├── Footer/         # MarketingFooter, DocsFooter
│   │   ├── Landing/        # ArchitectureDiagram, CodePreview, CTABanner, Features, Hero, HowItWorks, Pricing, Testimonials, UseCases
│   │   └── Shared/         # CalloutBox, CodeBlock, FeatureCard, PageMeta, PricingCard, PricingTierGrid, pricingTiers.ts, SectionContainer, SectionHeader, StepItem
│   ├── pages/              # Landing, Features, Pricing, UseCases, docs/DocsPage
│   ├── layouts/            # MarketingLayout (Header+Footer), DocsLayout (Header+Sidebar+Footer)
│   ├── hooks/              # useMakeTheme, useActiveHeading, useScrollPosition
│   ├── state/              # themeTypeAtom (Jotai, localStorage-persisted)
│   ├── theme/              # GlobalStyles (fonts, scrollbar, gradients)
│   ├── constants/          # envs.ts
│   └── utils/
│       ├── docsContent.ts  # import.meta.glob() loader for /docs .md/.mdx + _meta.json
│       └── docsLoader.ts   # buildNavigation(), findContentModule() for slug → MDX
└── package.json
```

## Routing

Two layouts, all pages lazy-loaded with `React.lazy()`:

- **MarketingLayout** (Header + Outlet + MarketingFooter): `/` (Landing), `/features`, `/pricing`, `/use-cases`
- **DocsLayout** (Header + DocsSidebar + Outlet + DocsFooter): `/docs` (index), `/docs/*` (catch-all slug)
- `*` → Redirect to `/`

## Documentation System

Docs are loaded from root `/docs` directory (monorepo level, NOT inside `repos/website/`). The `docs/internal/` subdirectory is excluded and contains developer, meta, superpowers, payments, research, endpoints, business, and plans directories.

**Loading flow**: `docsContent.ts` uses `import.meta.glob()` to discover `_meta.json` + `.md/.mdx` files at build time. `docsLoader.ts` builds navigation from metadata and maps URL slugs to lazy MDX imports. `DocsPage.tsx` reads slug from `useParams()`, dynamically imports and renders with `<MDXProvider>`.

**`_meta.json` format**: `{ "label": "Section Name", "order": 1, "pages": ["slug1", { "slug": "slug2", "label": "Label" }] }`

**MDX overrides** (`MDXComponents.tsx`): Headings get auto-anchor IDs via `github-slugger`. Code blocks use `CodeBlock` with Shiki (github-dark). Tables/links/blockquotes/images wrapped with MUI. Custom MDX components: `<Note>`, `<Tip>`, `<Warning>` (map to `CalloutBox` severity variants).

**Docs asset handling**: Dev mode serves `/docs-assets/*` via Express middleware from docs root. Build copies images to `dist/docs-assets/`. The `remarkDocsLinks` plugin rewrites relative image paths and `.md` links.

## Integration Points

- **@tdsk/components**: `makeTheme`, `overlayScrollBody`, `useWindowResize`
- **@tdsk/domain**: `PlanLimits` for pricing tier definitions
- **Root `/docs`**: All documentation content via `import.meta.glob()`

## Commands

```bash
pnpm start    # Dev server (port 5884)
pnpm build    # Production build to /dist
pnpm preview  # Preview production build
pnpm test     # Vitest tests
pnpm types    # TypeScript type checking
```
