---
name: tpl-frontend-astro-static
description: Template do pack (frontend/08-astro-static.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/08-astro-static.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do Site]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/08-astro-static.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — Astro 4 + TypeScript + Content Collections + React Islands
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Framework | Astro | 4.x |
| Linguagem | TypeScript | 5.x (strict) |
| Content | Markdown/MDX + Content Collections | built-in |
| Styling | Tailwind CSS | v4 |
| Islands | React 19 (interactive components) | latest |
| Deploy | Vercel / Netlify (static) or Node.js adapter | - |
| Tests | Vitest + Playwright | latest |

---

## ASTRO MENTAL MODEL

```
┌──────────────────────────────────────────────────────┐
│ DEFAULT: Everything is STATIC HTML — Zero JavaScript │
│                                                      │
│ When you NEED interactivity:                         │
│   → Create a React/Vue/Svelte component              │
│   → Add a client:* directive in the .astro page      │
│                                                      │
│ client:load    — hydrate immediately (critical UI)   │
│ client:idle    — hydrate when browser is idle         │
│ client:visible — hydrate when scrolled into viewport  │
│ client:media   — hydrate on media query match         │
│ client:only    — SSR skip, client-only render         │
└──────────────────────────────────────────────────────┘

RULE: Start with ZERO client:* directives. Add only when needed.
Every directive = more JS shipped to the browser.
```

---

## PROJECT STRUCTURE

```
src/
├── components/
│   ├── ui/            # Pure Astro components (zero JS)
│   │   ├── Card.astro
│   │   ├── Badge.astro
│   │   └── Hero.astro
│   └── interactive/   # React components with client:* directives
│       ├── SearchBar.tsx      # client:load (needs immediate interaction)
│       ├── TableOfContents.tsx # client:visible (only when scrolled)
│       └── Newsletter.tsx     # client:idle (can wait to hydrate)
├── content/
│   ├── config.ts      # Zod schemas for content collections
│   ├── blog/          # .md/.mdx files
│   │   ├── my-post.md
│   │   └── another.mdx
│   └── docs/
│       └── getting-started.md
├── layouts/
│   ├── BaseLayout.astro   # HTML skeleton + <head>
│   └── BlogLayout.astro   # Post-specific layout
├── pages/
│   ├── index.astro        # Homepage
│   ├── blog/
│   │   ├── index.astro    # Blog listing
│   │   └── [slug].astro   # Dynamic post page
│   └── api/
│       └── newsletter.ts  # API route (form handler)
└── styles/
    └── global.css
```

---

## CONTENT COLLECTIONS PATTERN

```typescript
// src/content/config.ts
import { z, defineCollection } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().max(160), // SEO-friendly
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    author: z.string().default('Admin'),
  }),
});

const docs = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    order: z.number(), // for sidebar sorting
  }),
});

export const collections = { blog, docs };
```

### Rendering Content

```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';
import BlogLayout from '@/layouts/BlogLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content, headings } = await post.render();
---

<BlogLayout title={post.data.title} description={post.data.description}>
  <article class="prose lg:prose-xl">
    <h1>{post.data.title}</h1>
    <time datetime={post.data.pubDate.toISOString()}>
      {post.data.pubDate.toLocaleDateString('pt-BR')}
    </time>
    <Content />
  </article>
</BlogLayout>
```

---

## ISLAND INTEGRATION (React in Astro)

```astro
---
// src/pages/blog/index.astro
import SearchBar from '@/components/interactive/SearchBar';
import { getCollection } from 'astro:content';

const posts = await getCollection('blog', ({ data }) => !data.draft);
---

<h1>Blog</h1>

<!-- React island: hydrates immediately (search needs to work right away) -->
<SearchBar client:load posts={posts.map((p) => ({ slug: p.slug, title: p.data.title }))} />

<!-- Pure Astro: zero JS -->
{posts.map((post) => (
  <article>
    <a href={`/blog/${post.slug}`}>{post.data.title}</a>
    <p>{post.data.description}</p>
  </article>
))}
```

---

## SEO & METADATA

```astro
---
// layouts/BaseLayout.astro
interface Props {
  title: string;
  description: string;
  ogImage?: string;
  canonical?: string;
}

const { title, description, ogImage, canonical } = Astro.props;
const siteUrl = import.meta.env.SITE;
---

<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content={description} />
  {canonical && <link rel="canonical" href={canonical} />}

  <!-- Open Graph -->
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:image" content={ogImage ?? `${siteUrl}/og-default.png`} />
  <meta property="og:type" content="website" />

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={title} />
  <meta name="twitter:description" content={description} />

  <link rel="sitemap" href="/sitemap-index.xml" />
</head>
<body>
  <slot />
</body>
</html>
```

---

## ROUTING TABLE (trigger → action)

| Trigger | Action |
|---------|--------|
| New page | `pages/path.astro` or `pages/path/index.astro` |
| Dynamic routes | `pages/[slug].astro` + `getStaticPaths()` |
| New content type | Add collection to `content/config.ts` with Zod schema |
| Interactive component | React component → use `client:visible` (default) |
| Blog listing | `getCollection('blog')` → filter `!data.draft` |
| API route | `pages/api/endpoint.ts` → export `GET`, `POST` |
| RSS Feed | `@astrojs/rss` → `pages/rss.xml.ts` |
| Sitemap | `@astrojs/sitemap` in `astro.config.mjs` |
| i18n | Folder-based: `pages/en/`, `pages/pt/` or `@astrojs/starlight` |

---

## PERFORMANCE RULES

- Images: ALWAYS use `<Image>` from `astro:assets` (auto WebP, lazy load)
- Fonts: Self-host with `@fontsource/*` packages (no Google Fonts CDN)
- No client-side navigation unless needed (View Transitions API optional)
- Prefetch: `<a data-astro-prefetch>` for faster navigations
- Bundle: check `npm run build` output sizes — every KB counts

---

## TESTING PATTERNS

```typescript
// tests/content-schemas.test.ts
import { describe, it, expect } from 'vitest';
import { z } from 'zod';

// Replicate your schema here for validation tests
const blogSchema = z.object({
  title: z.string(),
  description: z.string().max(160),
  pubDate: z.coerce.date(),
  draft: z.boolean().default(false),
});

describe('blog schema', () => {
  it('rejects description > 160 chars', () => {
    const result = blogSchema.safeParse({
      title: 'Test', description: 'a'.repeat(161), pubDate: '2024-01-01',
    });
    expect(result.success).toBe(false);
  });
});
```

---

## ENV VARS

```env
SITE=https://mysite.com
PUBLIC_GA_ID=G-XXXXXXX
```

## BUILD COMMANDS

```bash
npm run dev          # Dev server (fast refresh)
npm run build        # Static build to dist/
npm run preview      # Preview static build locally
npx astro check      # TypeScript + Astro diagnostics
npm test             # Vitest
npm run test:e2e     # Playwright
```

---

## QUALITY GATES

□ `npm run build` — 0 errors
□ Lighthouse: Performance 100, SEO 100, Accessibility 95+
□ No unused `client:*` directives
□ All images use `<Image>` component from `astro:assets`
□ `sitemap.xml` generated via `@astrojs/sitemap`
□ `robots.txt` configured
□ RSS feed generated for blog
□ All content collections validate with Zod schema

---

## FORBIDDEN

- NEVER add `client:load` when `client:visible` or `client:idle` works
- NEVER use `<img>` — always `<Image>` from `astro:assets`
- NEVER load Google Fonts from CDN (self-host with `@fontsource`)
- NEVER create `.tsx` pages (use `.astro` for pages, `.tsx` for islands)
- NEVER import heavy JS in Astro components (it won't tree-shake)
- NEVER skip `getStaticPaths` for dynamic routes in static mode
