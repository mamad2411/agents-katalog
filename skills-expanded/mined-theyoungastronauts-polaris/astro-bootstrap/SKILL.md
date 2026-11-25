---
name: astro-bootstrap
description: "Scaffold an Astro project (Tailwind v4, DaisyUI, landing page)."
disable-model-invocation: true
---

# Astro Bootstrap

On-demand command for scaffolding a new Astro site with Docker, Tailwind CSS v4, DaisyUI, and landing page conventions.

> **MANDATORY: This project runs entirely in Docker.**
> Every Docker file below (Dockerfile.dev, docker-compose.yml, Makefile) MUST be generated.
> The Makefile is the sole interface — never run `npm` directly on the host.

## Before You Start

Ask the user for these values:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{site-name}` | Project/directory name | `acme-landing` |
| `{compose-project}` | Docker Compose project name (kebab-case) | `acme-landing` |
| `{host_port}` | Host port for Astro (default: `4321`) | `4321` |
| `{domain}` | Production domain | `acme.com` |
| `{site-title}` | Display name for metadata | `Acme Inc` |
| `{site-description}` | Default meta description | `Build better widgets with Acme` |
| **Content collections** | Include content collections setup? | Yes / No |
| **Include Agentation?** | Browser annotation tool for visual feedback | Yes / No |

---

## Directory Structure

```
{site-name}/
├── src/
│   ├── pages/
│   │   ├── index.astro
│   │   └── 404.astro
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.astro
│   │   │   └── Footer.astro
│   │   ├── landing/
│   │   │   └── Hero.astro
│   │   ├── ui/
│   │   │   └── Button.astro
│   │   └── dev/                # If Agentation enabled
│   │       └── AgentationOverlay.tsx
│   ├── layouts/
│   │   └── BaseLayout.astro
│   ├── styles/
│   │   └── global.css
│   ├── content/              # If content collections enabled
│   │   └── blog/
│   │       └── first-post.md
│   └── content.config.ts     # If content collections enabled
├── public/
│   ├── favicon.svg
│   └── robots.txt
├── package.json
├── astro.config.mjs
├── tsconfig.json
├── .env
├── .gitignore
├── Dockerfile.dev
├── docker-compose.yml
├── Makefile
└── .mcp.json                 # If Agentation enabled
```

---

## File Templates

### package.json

```json
{
  "name": "{site-name}",
  "type": "module",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "astro dev --host",
    "build": "astro build",
    "preview": "astro preview --host",
    "check": "astro check"
  },
  "dependencies": {
    "astro": "^5",
    "@astrojs/sitemap": "^3"
  },
  "devDependencies": {
    "typescript": "^5",
    "tailwindcss": "^4",
    "@tailwindcss/vite": "^4",
    "daisyui": "^5"
  }
}
```

**If content collections enabled**: Also add `"zod": "^3"` to dependencies.

**If Agentation enabled**: Also add `"@astrojs/react": "^4"`, `"react": "^19"`, `"react-dom": "^19"` to dependencies and `"agentation": "^0"` to devDependencies.

### astro.config.mjs

```javascript
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://{domain}',
  output: 'static',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
```

**If Agentation enabled**: Import and add the React integration:

```javascript
import react from '@astrojs/react';

// Add to integrations array:
integrations: [sitemap(), react()],
```

### tsconfig.json

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### .env

```bash
PUBLIC_SITE_URL=https://{domain}
```

### .gitignore

```
# astro
dist/
.astro/

# dependencies
node_modules/

# environment
.env*.local

# editor
.DS_Store
*.swp

# docker
docker-compose.override.yml
```

### src/styles/global.css

```css
@import "tailwindcss";
@plugin "daisyui" {
  themes: light, dark;
}
```

### src/layouts/BaseLayout.astro

```astro
---
import { ViewTransitions } from 'astro:transitions';
import Header from '@/components/layout/Header.astro';
import Footer from '@/components/layout/Footer.astro';
import '@/styles/global.css';

interface Props {
  title: string;
  description?: string;
  ogImage?: string;
}

const {
  title,
  description = '{site-description}',
  ogImage = '/og.jpg',
} = Astro.props;

const canonicalURL = new URL(Astro.url.pathname, Astro.site);
---

<!doctype html>
<html lang="en" data-theme="dark">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />

    <title>{title} | {site-title}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonicalURL} />

    <meta property="og:type" content="website" />
    <meta property="og:url" content={canonicalURL} />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:image" content={new URL(ogImage, Astro.site)} />
    <meta property="og:site_name" content="{site-title}" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={title} />
    <meta name="twitter:description" content={description} />
    <meta name="twitter:image" content={new URL(ogImage, Astro.site)} />

    <ViewTransitions />
  </head>
  <body class="min-h-screen bg-base-100 text-base-content flex flex-col">
    <Header />
    <main class="flex-1">
      <slot />
    </main>
    <Footer />
  </body>
</html>
```

**If Agentation enabled**: Add the import to the frontmatter and the overlay inside `<body>`, after `<Footer />`:

```astro
---
import AgentationOverlay from '@/components/dev/AgentationOverlay.tsx';
---

<!-- Add after <Footer />, before </body>: -->
{import.meta.env.DEV && <AgentationOverlay client:only="react" />}
```

### src/components/layout/Header.astro

```astro
---
const navItems = [
  { label: 'Home', href: '/' },
  { label: 'About', href: '/about' },
];
---

<header class="navbar bg-base-200 border-b border-base-300">
  <div class="container mx-auto max-w-5xl">
    <div class="flex-1">
      <a href="/" class="text-xl font-bold text-primary">{site-title}</a>
    </div>
    <nav class="flex-none">
      <ul class="menu menu-horizontal px-1">
        {navItems.map((item) => (
          <li><a href={item.href}>{item.label}</a></li>
        ))}
      </ul>
    </nav>
  </div>
</header>
```

### src/components/layout/Footer.astro

```astro
---
const year = new Date().getFullYear();
---

<footer class="footer footer-center p-6 bg-base-200 text-base-content/70 border-t border-base-300">
  <p>&copy; {year} {site-title}. All rights reserved.</p>
</footer>
```

### src/components/landing/Hero.astro

```astro
---
interface Props {
  title: string;
  subtitle?: string;
  ctaText?: string;
  ctaHref?: string;
}

const {
  title,
  subtitle,
  ctaText = 'Get Started',
  ctaHref = '#features',
} = Astro.props;
---

<section class="hero min-h-[60vh] bg-base-200">
  <div class="hero-content text-center">
    <div class="max-w-2xl">
      <h1 class="text-5xl font-bold">{title}</h1>
      {subtitle && <p class="py-6 text-lg text-base-content/70">{subtitle}</p>}
      <a href={ctaHref} class="btn btn-primary btn-lg">{ctaText}</a>
    </div>
  </div>
</section>
```

### src/components/ui/Button.astro

```astro
---
interface Props {
  variant?: 'primary' | 'ghost' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  href?: string;
}

const { variant = 'primary', size = 'md', href } = Astro.props;
const Tag = href ? 'a' : 'button';
const classes = `btn btn-${variant} btn-${size}`;
---

<Tag href={href} class={classes}>
  <slot />
</Tag>
```

### src/pages/index.astro

```astro
---
import BaseLayout from '@/layouts/BaseLayout.astro';
import Hero from '@/components/landing/Hero.astro';
---

<BaseLayout title="Home" description="{site-description}">
  <Hero
    title="Welcome to {site-title}"
    subtitle="{site-description}"
    ctaText="Get Started"
    ctaHref="#features"
  />

  <section id="features" class="container mx-auto max-w-5xl px-4 py-16">
    <h2 class="text-3xl font-bold text-center mb-12">Features</h2>
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div class="card bg-base-200 shadow-md">
        <div class="card-body">
          <h3 class="card-title">Feature One</h3>
          <p class="text-base-content/70">Description of the first feature.</p>
        </div>
      </div>
      <div class="card bg-base-200 shadow-md">
        <div class="card-body">
          <h3 class="card-title">Feature Two</h3>
          <p class="text-base-content/70">Description of the second feature.</p>
        </div>
      </div>
      <div class="card bg-base-200 shadow-md">
        <div class="card-body">
          <h3 class="card-title">Feature Three</h3>
          <p class="text-base-content/70">Description of the third feature.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="bg-base-200 py-16">
    <div class="container mx-auto max-w-5xl px-4 text-center">
      <h2 class="text-3xl font-bold mb-4">Ready to get started?</h2>
      <p class="text-base-content/70 mb-8 max-w-lg mx-auto">
        Join thousands of users building with {site-title}.
      </p>
      <a href="/signup" class="btn btn-primary btn-lg">Sign Up Free</a>
    </div>
  </section>
</BaseLayout>
```

### src/pages/404.astro

```astro
---
import BaseLayout from '@/layouts/BaseLayout.astro';
---

<BaseLayout title="Page Not Found">
  <div class="min-h-[60vh] flex flex-col items-center justify-center px-4">
    <h1 class="text-6xl font-bold text-base-content/20 mb-4">404</h1>
    <p class="text-xl mb-8">Page not found.</p>
    <a href="/" class="btn btn-primary">Back to Home</a>
  </div>
</BaseLayout>
```

### public/robots.txt

```
User-agent: *
Allow: /

Sitemap: https://{domain}/sitemap-index.xml
```

### public/favicon.svg

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" fill="none">
  <rect width="36" height="36" rx="8" fill="#570DF8"/>
  <text x="50%" y="55%" dominant-baseline="middle" text-anchor="middle" font-size="20" fill="white" font-family="system-ui">A</text>
</svg>
```

---

## Content Collections (if enabled)

### src/content.config.ts

```typescript
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

### src/content/blog/first-post.md

```markdown
---
title: "First Post"
description: "Welcome to the blog."
pubDate: 2025-01-01
---

This is the first blog post. Edit or delete this file to get started.
```

### src/pages/blog/index.astro

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '@/layouts/BaseLayout.astro';

const posts = (await getCollection('blog'))
  .filter((post) => !post.data.draft)
  .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
---

<BaseLayout title="Blog" description="Latest posts from {site-title}">
  <div class="container mx-auto max-w-3xl px-4 py-16">
    <h1 class="text-3xl font-bold mb-8">Blog</h1>
    {posts.length === 0 ? (
      <p class="text-base-content/70">No posts yet.</p>
    ) : (
      <ul class="space-y-6">
        {posts.map((post) => (
          <li>
            <a href={`/blog/${post.id}`} class="card bg-base-200 shadow-md hover:shadow-lg transition-shadow">
              <div class="card-body">
                <h2 class="card-title">{post.data.title}</h2>
                <p class="text-base-content/70 text-sm">{post.data.description}</p>
                <time class="text-xs text-base-content/50">
                  {post.data.pubDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
                </time>
              </div>
            </a>
          </li>
        ))}
      </ul>
    )}
  </div>
</BaseLayout>
```

### src/pages/blog/[id].astro

```astro
---
import { getCollection, render } from 'astro:content';
import BaseLayout from '@/layouts/BaseLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { id: post.id },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await render(post);
---

<BaseLayout title={post.data.title} description={post.data.description}>
  <article class="container mx-auto max-w-3xl px-4 py-16">
    <header class="mb-8">
      <h1 class="text-4xl font-bold mb-2">{post.data.title}</h1>
      <time class="text-sm text-base-content/50">
        {post.data.pubDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
      </time>
    </header>
    <div class="prose prose-lg max-w-none">
      <Content />
    </div>
  </article>
</BaseLayout>
```

---

## Agentation (if enabled)

Only generate these files if the user opted into Agentation.

### src/components/dev/AgentationOverlay.tsx

```tsx
import { Agentation } from "agentation";

export default function AgentationOverlay() {
  return <Agentation />;
}
```

### .mcp.json

```json
{
  "mcpServers": {
    "agentation": {
      "command": "npx",
      "args": ["agentation-mcp", "server"]
    }
  }
}
```

---

## Docker (REQUIRED — do not skip)

### Dockerfile.dev

```dockerfile
FROM node:22-alpine

WORKDIR /app

# Install dependencies first for layer caching
COPY package.json package-lock.json* ./
RUN npm install

# Copy application code
COPY . .

EXPOSE 4321

CMD ["npm", "run", "dev"]
```

### docker-compose.yml

```yaml
name: {compose-project}

services:
  site:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "{host_port}:4321"
    env_file:
      - .env
```

### Makefile

```makefile
# {compose-project} - Makefile
PROJECT_NAME = {compose-project}
DOCKER_COMPOSE = docker compose --project-name $(PROJECT_NAME)

# ============================================================================
# Docker
# ============================================================================

.PHONY: build up down restart stop ps logs bash wipe

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up --detach

down:
	$(DOCKER_COMPOSE) down

restart: down up

stop:
	$(DOCKER_COMPOSE) stop

ps:
	$(DOCKER_COMPOSE) ps

logs:
	$(DOCKER_COMPOSE) logs -f site

bash:
	$(DOCKER_COMPOSE) exec site sh

wipe:
	@echo "WARNING: This will delete all containers and volumes!"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	$(DOCKER_COMPOSE) down -v --remove-orphans

# ============================================================================
# Development
# ============================================================================

.PHONY: dev preview astro-check

dev: up logs

preview:
	$(DOCKER_COMPOSE) exec site npm run preview

astro-check:
	$(DOCKER_COMPOSE) exec site npm run check

# ============================================================================
# Dependencies
# ============================================================================

.PHONY: install add

install:
	$(DOCKER_COMPOSE) exec site npm install

add:
	$(DOCKER_COMPOSE) exec site npm install $(filter-out $@,$(MAKECMDGOALS))

# ============================================================================
# Build
# ============================================================================

.PHONY: build-site

build-site:
	$(DOCKER_COMPOSE) exec site npm run build

# Catch-all for npm commands
%:
	@:
```

---

## Post-Bootstrap Checklist

1. Create project directory
2. Generate all files from templates above (replace placeholders)
3. Verify Docker files exist: `Dockerfile.dev`, `docker-compose.yml`, `Makefile`
4. Copy `.env` from template above
5. `make build && make up`
6. Verify page loads at `http://localhost:{host_port}`
7. `make astro-check` — should pass cleanly
8. If content collections: verify blog index renders at `/blog`
9. If Agentation: verify overlay renders in dev mode, check `.mcp.json` exists
10. Commit initial scaffold
