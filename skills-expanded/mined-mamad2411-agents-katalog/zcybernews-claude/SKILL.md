@AGENTS.md

# ZCyberNews — Project Guide for Claude

This file gives Claude full context to continue working on this project from any session (Claude Code CLI, Claude Desktop, or claude.ai).

---

## What This Project Is

A professional cybersecurity and tech news site that:

- Serves **English and Simplified Chinese** articles with bilingual routing
- Uses **Git + MDX files** as the CMS (no database, no GUI CMS)
- Runs an **AI-powered pipeline** that ingests RSS feeds, generates articles with DeepSeek-V3, translates to Chinese with Kimi K2, and commits them automatically via GitHub Actions
- Deploys to **Malaysia VPS (Evoxt)** on every push to `main` via GitHub Actions (`.github/workflows/deploy-vps.yml`)
- Includes **threat intelligence sections** with IOC tables, MITRE ATT&CK matrix, and threat actor cards

---

## Rendering strategy (ISR everywhere, memoized content loader)

Every route in this project uses the global "default to ISR" rule from `~/.claude/CLAUDE.md`. Specific applications:

| Route                                                              | Strategy                                                                                      | Why                                                              |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `app/[locale]/articles/[slug]`, `app/[locale]/threat-intel/[slug]` | `revalidate = 3600`, `dynamicParams = true`, `generateStaticParams` returns top 50 per locale | 262+ articles total, old ones render on-demand                   |
| `app/[locale]/page.tsx` (homepage)                                 | `revalidate = 3600`                                                                           | Article feed, regenerated hourly                                 |
| `app/[locale]/tags/[tag]`                                          | `revalidate = 3600`, `dynamicParams = true`, top 20 tags pre-rendered                         | ~200 unique tags otherwise                                       |
| `app/[locale]/categories/[category]`                               | `revalidate = 3600`                                                                           | Only 12 pages (6 categories × 2 locales), safe to pre-render all |
| `app/sitemap.ts`, `app/robots.ts`                                  | `dynamic = 'force-dynamic'` + `revalidate = 3600`                                             | Enumerates all articles; was timing out at build                 |
| All `app/admin/**` and `app/api/admin/**`                          | Dynamic (Next.js default for auth'd pages)                                                    | Per-session / per-request                                        |
| `app/api/revalidate`                                               | Dynamic route handler                                                                         | Invalidates ISR caches on demand                                 |

**Content loader memoization (`lib/content.ts`)** — `getAllPosts()` uses an mtime-keyed `Map` cache shared across all routes and requests in a Node process. Cache auto-invalidates when the content directory's mtime changes (new MDX landed). Without this memo, 4 parallel routes each reparsed 262 MDX files → build time 7+ min with per-route 60s timeouts. With it, build is ~50s on the 2GB VPS. Preserve this pattern; do not bypass with direct `readFileSync` calls.

**Revalidation flow for content changes**:

1. Admin publish or AI pipeline commits MDX to `content/`
2. `deploy-vps.yml` content-only path pulls + calls `POST /api/revalidate?tag=articles`
3. Next visitor to a listing page triggers regeneration; the memo re-reads the directory (mtime changed) and re-parses
4. Result: new article live within ~10s of commit, zero downtime

---

## Zero-Downtime Publishing Architecture (CRITICAL — read before touching deploy/publish code)

This site has a **hard zero-downtime requirement**. The architecture below was built specifically to avoid the 2-3 minute 502 outages that used to happen on every article publish. Do not regress this.

### The three runtime paths

**1. Content-only pushes (~10s, zero downtime)** — the happy path, happens dozens of times per day

- Admin publishes via `/admin/compose` OR hourly AI pipeline on GitHub Actions commits to `main`
- `deploy-vps.yml` classify job detects only `content/**`, `public/images/articles/**`, `.pipeline-cache/**`, or `data/**` changed
- Routes to `content-only` job: SSH → `git pull` → `curl /api/revalidate?tag=articles` → done
- PM2 is NOT touched. No rebuild. ISR picks up new MDX files from disk on next regeneration cycle.

**2. Code pushes (~2-3 min, TRUE zero downtime via Option B)** — rare, happens a few times per week

- Any change outside `content/**` (lib, app, workflows, package.json, etc.)
- Routes to `full-deploy` job with this flow:
  1. **Build on GitHub Actions runner** (7GB RAM, clean Node 22) — `npm ci` + `npm run build`
  2. **Verify artifact** — prerender-manifest.json must exist
  3. **Rsync `.next/` to VPS** into `/home/zcybernews/zcybernews/.next-staging/` (does NOT touch live `.next`)
  4. **SSH to VPS:** `git pull` (source), `npm ci` (server-side deps), atomic directory swap (`mv .next .next-prev && mv .next-staging .next`)
  5. **`pm2 reload`** — cluster mode cycles workers one at a time, old workers drain while new workers pick up the fresh `.next`
  6. Health check: `curl http://localhost:3000` must return 200
- Old build keeps serving traffic the entire time the new build is being prepared.
- Rollback: `mv .next .next-crashed && mv .next-prev .next && pm2 reload zcybernews` — instant.
- **This replaced the old stop-build-start pattern on 2026-04-17** (commit after the SEV3 502 during deploy). The old pattern had 60-90s downtime per code deploy because it built on the 2GB VPS, requiring `pm2 stop` to avoid file write races. The new pattern has zero downtime because the build happens on a separate machine.

**3. Emergency rebuild** — workflow_dispatch with `force_full_rebuild: true`

- Use when ISR cache has gone sideways or VPS disk state is corrupted

### Implementation details

| Layer                         | Mechanism                                                                                                                                                              | File                                                                                 |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Article pages                 | ISR with `revalidate = 3600`, `dynamicParams = true`, `generateStaticParams` returns only 50 most recent per locale                                                    | `app/[locale]/articles/[slug]/page.tsx`, `app/[locale]/threat-intel/[slug]/page.tsx` |
| Admin publish (single locale) | Zod-validates frontmatter before commit, then fires `revalidatePath`                                                                                                   | `app/api/admin/publish/route.ts`                                                     |
| Admin publish (EN+ZH)         | **Single atomic commit** via Git Data API (createBlob × 2, createTree, createCommit, updateRef). Title+excerpt and body translations run in PARALLEL via `Promise.all` | `app/api/admin/translate-publish/route.ts`                                           |
| Revalidation endpoint         | Secret-guarded, accepts `?path=` and `?tag=`                                                                                                                           | `app/api/revalidate/route.ts`                                                        |
| GitHub commit helpers         | Atomic multi-file commit + single-file fallback                                                                                                                        | `lib/github-commit.ts`                                                               |
| Revalidate client             | In-process fetch to `localhost:3000/api/revalidate` with secret                                                                                                        | `lib/revalidate-client.ts`                                                           |
| Deploy workflow               | classify + content-only + full-deploy jobs                                                                                                                             | `.github/workflows/deploy-vps.yml`                                                   |
| PM2 config                    | Cluster mode `-i 2 --exec-mode cluster --max-memory-restart 750M`                                                                                                      | initialized via `deploy-vps.yml` on first-time start                                 |

### Required env vars

- **`REVALIDATE_SECRET`** (VPS `.env.local` + GitHub Secrets) — guards `/api/revalidate`. Generate with `openssl rand -base64 32`.
- **`GITHUB_TOKEN`** (VPS `.env.local`) — fine-grained PAT with `contents: write` for the admin publish Git Data API calls.
- **`GITHUB_REPO`**, **`GITHUB_BRANCH`** — commit target.

### How to preserve zero-downtime when modifying this

- **Never** add `pm2 stop` or `pm2 restart` to the full-deploy job. Use `pm2 reload`. The old build stays up until new workers are ready.
- **Never** trigger a full rebuild from a content-only push. If you add a new "content" path, update the `NON_CONTENT` grep regex in the classify job.
- **Never** make a publish API commit to GitHub more than once per operation. That would cause two push events → two deploys → potential race conditions.
- **Always** Zod-validate frontmatter before committing. Since we use ISR, malformed MDX now 500s at request time instead of failing the build — validation at the write boundary is the safety net.
- **When adding new admin-triggered mutations**, call `triggerRevalidate({ path, tag })` after the commit so the change appears in seconds.

### Migrating existing VPS from fork mode to cluster mode (one-time)

If the VPS is still running PM2 in fork mode, the first `pm2 reload` after deploy will do a best-effort restart (~2s gap), not true zero-downtime. To migrate:

```bash
pm2 delete zcybernews
pm2 start npm --name zcybernews -i 2 --exec-mode cluster --max-memory-restart 750M -- start
pm2 save
pm2 describe zcybernews | grep -E "(exec mode|instances)"   # should show cluster / 2
```

On 2GB VPS, 2 workers is tight (~200-400MB each). If OOM, fall back to 1 cluster worker (still graceful reload, just not simultaneous): `-i 1 --max-memory-restart 1000M`.

---

**GitHub repo:** https://github.com/jamesKhor/Zcybernews  
**Local path:** `C:\Users\jmskh\projects\zcybernews`

---

## Tech Stack

| Layer                         | Package                                               |
| ----------------------------- | ----------------------------------------------------- |
| Framework                     | Next.js 16 (App Router, TypeScript)                   |
| Styling                       | Tailwind CSS v4 + shadcn/ui                           |
| Content                       | gray-matter + next-mdx-remote                         |
| MDX plugins                   | remark-gfm, rehype-highlight, rehype-slug             |
| i18n                          | next-intl v4 (EN/ZH routing)                          |
| AI text — articles            | DeepSeek-V3 via `@ai-sdk/openai-compatible`           |
| AI text — Chinese translation | Kimi K2 (Moonshot AI) via `@ai-sdk/openai-compatible` |
| AI images (Phase 2)           | fal.ai FLUX.1-schnell (~$0.003/image)                 |
| Web search                    | Brave Search API or Tavily                            |
| Schema validation             | Zod v4                                                |
| Script runner                 | tsx                                                   |
| Locale middleware             | `proxy.ts` (Next.js 16 renamed middleware → proxy)    |
| Deploy                        | Malaysia VPS via `.github/workflows/deploy-vps.yml`   |

---

## Important Conventions

- **`proxy.ts`** is the locale + WeChat middleware file. Next.js 16 renamed `middleware.ts` → `proxy.ts`. Do NOT create a `middleware.ts` — it will show a deprecation warning.
- **WeChat default:** WeChat browser UA (`MicroMessenger`) is detected in `proxy.ts` and redirected to `/zh`. Other browsers use `Accept-Language` header for locale detection.
- **Content in Git:** Articles live in `content/en/posts/`, `content/zh/posts/`, `content/en/threat-intel/`, `content/zh/threat-intel/` as `.mdx` files.
- **Frontmatter validated by Zod** in `lib/types.ts` — `ArticleFrontmatterSchema`. Any AI-generated article MUST conform to this schema or it is skipped.
- **Default images** are SVGs in `public/images/defaults/{category}.svg`. Real AI-generated images go in `public/images/articles/` and override via the `featured_image` frontmatter field.
- **Category values** (exact enum): `threat-intel | vulnerabilities | malware | industry | tools | ai`
- **Language values**: `en | zh`

---

## Directory Structure

```
zcybernews/
├── app/
│   ├── [locale]/                  # en | zh
│   │   ├── layout.tsx             # Header + Footer wrapper, NextIntlClientProvider
│   │   ├── page.tsx               # Homepage
│   │   ├── articles/
│   │   │   ├── page.tsx           # Paginated listing (12/page)
│   │   │   └── [slug]/page.tsx    # Single article with IOCTable + MitreMatrix
│   │   └── threat-intel/
│   │       ├── page.tsx
│   │       └── [slug]/page.tsx
│   ├── api/
│   │   ├── feed/route.ts          # RSS/Atom feed
│   │   └── wechat/route.ts        # WeChat JSON feed (?locale=zh)
│   ├── layout.tsx                 # Root layout (fonts, metadata)
│   └── globals.css                # Dark cyber theme + prose styles
├── components/
│   ├── articles/
│   │   ├── ArticleCard.tsx        # Card used in listing pages
│   │   └── ArticleMeta.tsx        # Date, reading time, severity, CVE badges
│   ├── threat-intel/
│   │   ├── IOCTable.tsx           # "use client" — sortable, filterable, CSV export
│   │   └── MitreMatrix.tsx        # ATT&CK tactic columns, links to attack.mitre.org
│   ├── layout/
│   │   ├── Header.tsx             # "use client" — nav, locale switcher, mobile menu
│   │   └── Footer.tsx
│   └── ui/                        # shadcn/ui components (card, badge, button, etc.)
├── content/
│   ├── en/posts/                  # English articles (.mdx)
│   ├── en/threat-intel/           # English TI reports (.mdx)
│   ├── zh/posts/                  # Chinese articles (.mdx)
│   └── zh/threat-intel/           # Chinese TI reports (.mdx)
├── i18n/
│   ├── routing.ts                 # defineRouting — locales: [en, zh], default: en
│   ├── request.ts                 # getRequestConfig for next-intl
│   └── navigation.ts              # createNavigation helpers (Link, redirect, etc.)
├── lib/
│   ├── types.ts                   # ArticleFrontmatterSchema (Zod), IOCEntry, TTPEntry
│   ├── content.ts                 # getAllPosts, getPostBySlug, getRelatedPosts
│   ├── mdx.ts                     # compileMDX with remark/rehype plugins
│   └── utils.ts                   # cn() helper for shadcn
├── messages/
│   ├── en.json                    # English UI strings
│   └── zh.json                    # Chinese UI strings
├── public/images/defaults/        # SVG placeholder images per category
├── scripts/                       # AI pipeline (NOT YET BUILT — Phase 4)
├── .env.example                   # All required env vars documented
├── proxy.ts                       # next-intl locale + WeChat middleware
└── next.config.ts                 # withNextIntl wrapper
```

---

## Article Frontmatter Schema

Every `.mdx` article must have this frontmatter (validated by `lib/types.ts`):

```yaml
---
title: "Article Title"
slug: "url-slug"
date: "2026-04-09" # ISO 8601
updated: "2026-04-10" # optional
excerpt: "1-2 sentence summary for cards and meta tags"
category: "threat-intel" # threat-intel|vulnerabilities|malware|industry|tools|ai
tags: ["ransomware", "apt"]
language: "en" # en|zh
locale_pair: "slug-of-other-language-version" # optional
source_urls: ["https://..."]
author: "AI-generated" # or human name
featured_image: "/images/articles/slug.webp" # optional, overrides default
draft: false
scheduled_publish: "2026-04-10T09:00:00Z" # optional, hides until this time

# Threat intel fields (optional on regular posts)
threat_actor: "LockBit 4.0"
threat_actor_origin: "Russia"
campaign: "HL-SECTOR-2026-Q1"
severity: "critical" # critical|high|medium|low|informational
cvss_score: 9.8
cve_ids: ["CVE-2026-1234"]
affected_sectors: ["healthcare"]
affected_regions: ["North America"]
iocs:
  - type: "ip" # ip|domain|hash_md5|hash_sha1|hash_sha256|url|email|registry_key|file_path
    value: "1.2.3.4"
    description: "C2 server"
    confidence: "high" # high|medium|low
    first_seen: "2026-04-01"
ttp_matrix:
  - tactic: "Initial Access"
    technique_id: "T1190"
    technique_name: "Exploit Public-Facing Application"
    description: "optional detail"
---
```

---

## Article MDX Body Structure

Every article uses these exact H2 sections (AI prompt enforces this):

```
## Executive Summary
## Technical Analysis
## Indicators of Compromise
## Tactics, Techniques & Procedures
## Threat Actor Context
## Mitigations & Recommendations
## References
```

---

## Environment Variables

Copy `.env.example` to `.env.local` and fill in:

```bash
NEXT_PUBLIC_SITE_URL=https://zcybernews.com

# AI — primary article generation (cheap: ~$0.27/1M tokens)
DEEPSEEK_API_KEY=              # https://platform.deepseek.com
# AI — Chinese translation (better ZH quality)
KIMI_API_KEY=                  # https://platform.moonshot.cn

AI_PROVIDER=deepseek           # deepseek | kimi

# Web search for pipeline enrichment
BRAVE_SEARCH_API_KEY=          # https://api.search.brave.com

# Image generation (Phase 2, optional for now)
FAL_KEY=                       # https://fal.ai

# WeChat Official Account (optional)
WECHAT_APP_ID=
WECHAT_APP_SECRET=

# Cloudflare Pages deploy (for GitHub Actions)
CLOUDFLARE_API_TOKEN=
CLOUDFLARE_ACCOUNT_ID=
```

---

## Build & Dev Commands

```bash
npm run dev        # local dev at http://localhost:3000
npm run build      # production build (must pass before pushing)
npx tsc --noEmit   # type-check only
```

---

## Phase Completion Status

### ✅ Phase 0 — Bootstrap (DONE)

Next.js 16, Tailwind v4, shadcn/ui, all dependencies, `proxy.ts` locale middleware.

### ✅ Phase 1 — Content Layer (DONE)

- `lib/types.ts` — Zod schemas for all frontmatter fields
- `lib/content.ts` — `getAllPosts`, `getPostBySlug`, `getRelatedPosts`, `getAllTags`
- `lib/mdx.ts` — `compileMDX` with remark-gfm, rehype-highlight, rehype-slug
- Article pages: `/[locale]/articles/[slug]` with `generateStaticParams`
- Threat intel pages: `/[locale]/threat-intel/[slug]`
- Pagination on listing pages
- Category pages: `/[locale]/categories/[category]/page.tsx` ✅
- Tag pages: `/[locale]/tags/[tag]/page.tsx` ✅
- `app/sitemap.ts` — XML sitemap ✅
- `app/robots.ts` ✅

### ✅ Phase 2 — Core UI Components (DONE)

- `Header.tsx` — sticky nav, locale switcher (EN↔中文), mobile hamburger
- `Footer.tsx` — links, RSS/WeChat feed links
- `ArticleCard.tsx` — thumbnail, category badge, severity overlay, reading time
- `ArticleMeta.tsx` — date, reading time, severity badge, CVE IDs, threat actor
- `IOCTable.tsx` — client component: sort by type/value/confidence, type filter, copy-to-clipboard, CSV export
- `MitreMatrix.tsx` — tactic columns in ATT&CK order, technique badges linking to attack.mitre.org
- SVG placeholder images for all 6 categories in `public/images/defaults/`
- Dark cybersecurity theme in `globals.css`
- RSS feed API (`/api/feed`) and WeChat JSON API (`/api/wechat?locale=zh`)
- `components/seo/JsonLd.tsx` — NewsArticle JSON-LD structured data ✅
- `components/cve/CVEArticleBody.tsx` + `CVEBadge.tsx` + `CVEHydrate.tsx` — inline CVE cards ✅
- `lib/rehype-cve.ts` — rehype plugin for CVE auto-linking ✅
- `app/api/cve/[id]/route.ts` — NVD CVE data proxy ✅
- `components/search/SearchDialog.tsx` — Cmd/Ctrl+K search modal ✅
- `app/api/search/route.ts` — search API ✅

### ✅ Phase 3 — Search & Additional Pages (DONE)

- Category pages, tag pages, sitemap, robots — all built (see Phase 1 above)
- Search dialog (`components/search/SearchDialog.tsx`) + search API ✅
- JSON-LD structured data on article pages ✅
- Note: `pagefind` static search not used — server-side search API implemented instead

### ✅ Phase 4 — AI Content Pipeline (DONE)

All scripts built in `scripts/` directory:

```
scripts/
├── pipeline/
│   ├── index.ts              # orchestrator
│   ├── ingest-rss.ts         # fetch RSS feeds, normalize, deduplicate
│   ├── generate-article.ts   # DeepSeek-V3 article generation
│   ├── translate-article.ts  # Kimi K2 EN→ZH translation
│   └── write-mdx.ts          # serialize gray-matter + write to content/
├── ai/
│   ├── provider.ts           # DeepSeek + Kimi client factories
│   ├── prompts/
│   │   ├── article.ts
│   │   └── translation.ts
│   └── schemas/
│       └── article-schema.ts
├── sources/
│   └── feeds.ts              # RSS feed URLs
├── translate-existing.ts     # one-off: translate existing EN articles to ZH
└── utils/
    ├── cache.ts
    ├── dedup.ts
    └── rate-limit.ts
```

### ✅ Phase 5 — Admin Panel & AI Compose (DONE — built beyond original plan)

Full admin panel at `/admin` with:

- **`/admin/login`** — NextAuth v5 credential auth
- **`/admin/`** — dashboard
- **`/admin/feed`** — RSS feed reader, select articles to synthesize
- **`/admin/compose`** — AI article composer:
  - Feed mode (from RSS) + Paste mode (raw text)
  - Model picker: DeepSeek / Kimi / Auto (free OpenRouter → paid fallback)
  - Length selector: Short / Medium / Long (1000+ words, no upper cap)
  - Custom prompt instructions
  - Streaming NDJSON generation with live status panel (per-model progress)
  - Browser notification when generation completes (works across tabs)
  - Dynamic button label showing current step
  - Auto-save draft to localStorage
  - Edit/Preview toggle (markdown + rendered)
  - One-click Publish EN or Publish EN+ZH (auto-translates via Kimi)
- **`/admin/articles`** — article listing + edit
- **`/admin/sources`** — RSS source management (UI built, backend pending)
- **API routes:**
  - `POST /api/admin/synthesize` — streaming AI article generation
  - `POST /api/admin/translate-publish` — translate + commit EN+ZH to GitHub
  - `POST /api/admin/publish` — commit EN only to GitHub
  - `GET/POST /api/admin/articles` — article CRUD
  - `GET /api/admin/feed` — RSS feed fetching for admin

### ✅ Phase 5b — AI Provider (DONE — `lib/ai-provider.ts`)

- `parseEffectiveParams()` — detects MoE active-param suffix, filters tiny models
- `isUsableWriteModel()` — ≥12B effective params + ≥32k context window
- `getLiveFreeModels()` — live fetch from OpenRouter API, 5-min cache, hardcoded fallback
- `runWithFallback()` — per-model timeout (90s article / 60s translate), skips on 404/429/503/timeout
- `generateWithFallback(provider?)` — `deepseek` | `kimi` | `auto` (free first)
- `translateWithFallback()` — Qwen-first free models → Kimi → DeepSeek
- Both return `{ text, modelUsed, usedPaidFallback }`

### ✅ Phase 6 — GitHub Actions (DONE)

Both workflow files exist in `.github/workflows/`:

- `build-deploy.yml` — deploys to Vercel on push to main
- `ai-content-pipeline.yml` — daily scheduled article generation + commit

**⚠️ Known issue:** Vercel Hobby free tier has a **10-second serverless timeout** which kills AI generation routes. Options:

- Upgrade to Vercel Pro ($20/mo, 300s timeout) — recommended for production
- Self-host on Malaysia VPS (evotx: 1vCPU/2GB RAM) — zero extra cost, no timeout limit

### 🔲 Phase 7 — Production Deployment & VPS Setup (NEXT)

Move from Vercel free (10s timeout issue) to Malaysia VPS for production:

- [ ] Set up PM2 + Nginx on evotx VPS
- [ ] Configure Nginx with `proxy_read_timeout 300s` for AI routes
- [ ] Set up Let's Encrypt SSL via Certbot
- [ ] Add GitHub Action for auto-deploy on push (SSH + pull + rebuild + PM2 restart)
- [ ] Add all env vars to VPS (DEEPSEEK_API_KEY, KIMI_API_KEY, OPENROUTER_API_KEY, GITHUB_TOKEN etc)
- [ ] Point zcybernews.com DNS to VPS via Cloudflare (free DDoS + CDN)
- [ ] Smoke test: generate article, publish EN+ZH, verify on live site

### 🔲 Phase 8 — SEO & China Optimisation (TODO)

- [ ] Baidu site verification meta tag in ZH locale layout
- [ ] Baidu Analytics (百度统计) script in ZH layout
- [ ] `hreflang` tags — already partially done via `generateMetadata`, verify all pages
- [ ] Submit sitemap to Baidu Search Console
- [ ] Submit sitemap to Google Search Console
- [ ] og:image — generate real preview images per article (fal.ai FLUX or static templates)
- [ ] WeChat sharing meta tags (wx:card, wx:image) for Chinese social sharing
- [ ] Test site accessibility from mainland China (VPN-free routing via Cloudflare)

### 🔲 Phase 9 — Automated Pipeline Activation (TODO)

The scripts are built but the automated daily pipeline needs to be wired up and tested:

- [ ] Test `scripts/pipeline/index.ts` end-to-end locally
- [ ] Verify RSS dedup cache works correctly (`scripts/utils/cache.ts`)
- [ ] Add GitHub Actions secrets: `DEEPSEEK_API_KEY`, `KIMI_API_KEY`, `BRAVE_SEARCH_API_KEY`
- [ ] Enable `ai-content-pipeline.yml` schedule (currently needs secrets to work)
- [ ] Monitor first few automated runs, check article quality
- [ ] Add admin UI to view pipeline run history / last run status

### 🔲 Phase 10 — RSS Sources Admin UI (TODO)

UI shell exists at `/admin/sources` but backend is not wired:

- [ ] `GET /api/admin/sources` — return current feed list
- [ ] `POST /api/admin/sources` — add new feed URL
- [ ] `DELETE /api/admin/sources/[id]` — remove feed
- [ ] Persist sources (JSON file in repo or env var)
- [ ] Test feed URL before saving (fetch + parse validation)

---

## Key Design Decisions (for context)

1. **`proxy.ts` not `middleware.ts`** — Next.js 16 breaking change, already handled
2. **DeepSeek for articles, Kimi for translation** — DeepSeek is fastest/cheapest for EN; Kimi (Moonshot) has better Chinese quality
3. **OpenRouter free models first** — Auto mode tries ≥12B free models before paid; DeepSeek/Kimi as paid fallback
4. **Admin compose = primary editorial workflow** — admin selects RSS articles → AI synthesizes → review → publish EN+ZH in one click
5. **No `output: 'export'`** — API routes must stay live (AI generation, admin, CVE lookup)
6. **GitHub as CMS** — articles committed as MDX files, Vercel/VPS redeploys on push
7. **Vercel 10s timeout is a real problem** — AI generation regularly exceeds this; VPS deployment is the fix
8. **Antivirus note** — threat intel MDX files with IOC hashes may trigger AV false positives (harmless text files)

---

## How to Continue in a New Session

Tell Claude:

> "Read CLAUDE.md and continue"

Claude will read this file and have full context to continue immediately.
