---
name: "astro"
description: "Astro framework: content-first sites, islands architecture, MDX collections, Cloudflare Workers/Pages deployment, View Transitions, SEO"
---

# Astro Skill

## When to activate
- Building a content site, blog, docs site, or marketing site
- Wanting zero JavaScript by default with optional interactive islands
- Deploying to Cloudflare Pages or Workers for global edge performance
- Building with MDX content collections (type-safe frontmatter)
- Adding View Transitions for smooth SPA-like navigation on a static site

## When NOT to use
- Highly interactive apps (dashboards, SaaS UIs) — use Next.js or SvelteKit
- When you need server-side sessions or complex auth — Next.js is better suited
- Real-time features — Astro is static/SSG-first

## Instructions

### Project setup

```bash
npm create astro@latest my-site
# Options: Blog / Documentation / Empty
# TypeScript: Strict recommended
# Dependencies: Yes

# Add integrations
npx astro add tailwind react cloudflare
```

### File structure

```
src/
├── content/
│   ├── config.ts          # collection schemas
│   └── blog/              # .md / .mdx files
│       └── hello-world.md
├── layouts/
│   └── BlogPost.astro
├── pages/
│   ├── index.astro        # becomes /
│   ├── blog/
│   │   ├── index.astro    # /blog
│   │   └── [slug].astro   # /blog/[slug]
│   └── rss.xml.ts         # RSS feed
├── components/
│   ├── Header.astro       # server-rendered
│   └── Counter.tsx        # React island (client:load)
└── styles/
    └── global.css
```

### Content collections (type-safe MDX)

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content'

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title:       z.string(),
    description: z.string(),
    pubDate:     z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage:   z.string().optional(),
    tags:        z.array(z.string()).default([]),
    draft:       z.boolean().default(false),
  }),
})

export const collections = { blog }
```

```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content'
import BlogLayout from '../../layouts/BlogPost.astro'

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft)
  return posts.map(post => ({
    params: { slug: post.slug },
    props: post,
  }))
}

const post = Astro.props
const { Content } = await post.render()
---

<BlogLayout frontmatter={post.data}>
  <Content />
</BlogLayout>
```

### Islands architecture — selective hydration

```astro
---
// Astro components: zero JS (server-rendered HTML only)
// React/Vue/Svelte components: hydrate when needed
---

<!-- Server-rendered — no JS shipped -->
<Header />
<ArticleContent />

<!-- Hydrate immediately on page load -->
<SearchBar client:load />

<!-- Hydrate when visible (lazy) -->
<CommentsSection client:visible />

<!-- Hydrate only on interaction -->
<ShareMenu client:idle />

<!-- Never hydrate (static) -->
<StaticWidget />
```

### Cloudflare Pages deployment

```typescript
// astro.config.mjs
import { defineConfig } from 'astro/config'
import cloudflare from '@astrojs/cloudflare'

export default defineConfig({
  output: 'server',   // or 'hybrid' — static + server on demand
  adapter: cloudflare({
    mode: 'directory',  // Cloudflare Pages Functions
    // or 'advanced' for Cloudflare Workers
  }),
})
```

```bash
# Deploy to Cloudflare Pages
npm run build
# Then connect repo to Cloudflare Pages dashboard
# Build command: npm run build
# Output dir: dist/
```

**Cloudflare Workers (edge SSR):**
```typescript
// src/middleware.ts — runs at the edge
import type { MiddlewareHandler } from 'astro'

export const onRequest: MiddlewareHandler = async (context, next) => {
  // Access Cloudflare bindings: KV, R2, D1, AI
  const { env } = context.locals.runtime
  const cache = await env.MY_KV.get('cached-data')
  return next()
}
```

### View Transitions

```astro
---
// src/layouts/Base.astro
import { ViewTransitions } from 'astro:transitions'
---

<html>
  <head>
    <ViewTransitions />
  </head>
  <body>
    <slot />
  </body>
</html>
```

```astro
<!-- Custom transition per element -->
<h1 transition:name="hero-title">Blog Post Title</h1>
<img transition:name="hero-image" src={heroImage} />
<!-- Elements with matching names animate between pages -->
```

### SEO patterns

```astro
---
// components/SEO.astro
const {
  title,
  description,
  image = '/og-default.png',
  canonicalURL = Astro.url,
} = Astro.props
---

<title>{title}</title>
<meta name="description" content={description} />
<link rel="canonical" href={canonicalURL} />
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:image" content={new URL(image, Astro.site)} />
<meta property="og:url" content={canonicalURL} />
<meta name="twitter:card" content="summary_large_image" />
```

### RSS feed

```typescript
// src/pages/rss.xml.ts
import rss from '@astrojs/rss'
import { getCollection } from 'astro:content'

export async function GET(context) {
  const posts = await getCollection('blog', p => !p.data.draft)
  return rss({
    title: 'My Blog',
    description: 'Latest posts',
    site: context.site,
    items: posts.map(post => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `/blog/${post.slug}/`,
    })),
  })
}
```

## Example

**User:** Build a developer blog with Astro — MDX posts with code highlighting, tag filtering, dark mode, RSS feed, and deploy to Cloudflare Pages.

**Expected output:**
- `src/content/config.ts` — blog collection with title, description, pubDate, tags, draft schema
- `src/pages/blog/[slug].astro` — dynamic post page with `getStaticPaths`
- `src/pages/blog/[tag].astro` — tag filtering page
- `src/components/SEO.astro` — OG tags, canonical URL
- `src/pages/rss.xml.ts` — RSS feed endpoint
- `astro.config.mjs` — Cloudflare adapter, Tailwind, MDX, syntax highlighting

---
