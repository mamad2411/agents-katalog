---
name: lovable-to-nextjs
description: "Migrate a Lovable (Vite + React Router / TanStack Start) project to Next.js 16 App Router with approved-site preservation or in-place normalization. 10-phase pipeline with per-phase validation gates: stack detection, quality diagnostics, component migration + normalization, route mapping, SEO migration, old-stack cleanup, Vercel deployment. Optionally calls tech-stack-detect for deeper analysis and theme-switch for design token generation."
license: Proprietary
metadata:
  when_to_use: Use when the user has a Lovable project that needs to migrate to Next.js, says "migrate to Next.js" / "从 Lovable 搬到 Next" / "convert Lovable project", or asks about moving from Vite/TanStack to Next.js App Router. Also use when a project built with Lovable needs production-grade SEO, RSC, or Vercel deployment.
  compatibility: Requires Bash (git, npm/pnpm/bun, ripgrep), Read, Write, Edit, Glob, Grep. Optionally uses WebFetch. Optionally calls tech-stack-detect and theme-switch skills.
  author: harness-engineering
  version: "1.0.0"
  allowed-tools: Read Bash Write Edit Glob Grep WebFetch
---

# Lovable to Next.js 16 Migration Engine

Choose the workflow before changing files:
- For an accepted prototype or a published site with existing URLs, follow [preservation mode](references/preservation-mode.md) from source capture through production verification. Its M0–M8 gates govern this path. Use the stack and rewrite references for implementation details.
- For an in-place conversion with engineering normalization, follow phases 0–9 below. Record any approved changes to presentation, content, and URLs before editing.

## Core Principle

**Migration = Transport + Normalization.** Not "migrate first, clean later" — that doubles the cost. Every file you move is a refactoring window. Move it, clean it, move on.

Two responsibilities, equally important:

| Responsibility | Description |
|---|---|
| Transport | Page content, copy, interactions, visuals stay 1:1. What the user sees does not change. |
| Normalization | Hardcoded values → tokens, large files → split components, missing types → added, flat directories → organized. Visual output unchanged, code quality upgraded. |

## Next.js 16 request APIs

Await route params and page search params in server code, including dynamic metadata. Client navigation hooks return their values directly. See the [Next.js 16 upgrade guide](https://nextjs.org/docs/app/guides/upgrading/version-16#async-request-apis-breaking-change).

## Execution Pipeline

```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → [Phase 5] → Phase 6 → Phase 7 → Phase 8 → Phase 9
  Gate      Gate      Gate      Gate      Gate       Gate       Gate      Gate      Gate      Done
```

Each phase has: **Input → Steps → Gate**. Do not proceed to the next phase until the gate passes.

---

## Phase 0: Inventory + Diagnostics

**Goal**: Create migration branch, inventory all routes and dependencies, diagnose vibe coding issues.

### Step 0.1: Confirm project info from user

Ask the user these questions (if not already known):

1. **Target domain**? (e.g., `dubbing.ai`)
2. **Package manager**? (`npm` / `pnpm` / `bun`)
3. **i18n needed**? (yes → routes go under `[locale]`)
4. **Init strategy**? (root dir has existing project → Strategy A sub-dir / Strategy B in-place)

### Step 0.2: Create migration branch

```bash
git checkout -b feature/nextjs-migration
git push -u origin feature/nextjs-migration
```

### Step 0.3: Detect Lovable tech stack

Run `scripts/detect-lovable-stack.ps1` or follow `references/stack-detection.md` manually. The script identifies:

- Stack type (Vite + React Router vs TanStack Start)
- Route structure (`src/pages/` vs `src/routes/`)
- React version
- UI component library (shadcn/ui presence)
- Backend integration (Supabase, serverFn, etc.)
- SEO approach (react-helmet-async, TanStack head, none)

**Output**: A completed `§1.2 Current Status` table (see `references/stack-detection.md`).

### Step 0.4: Build route mapping table

Based on the detected stack, scan routes and produce:

| Original URL | Next.js File Path | Static/Dynamic | Notes |
|---|---|---|---|
| / | src/app/page.tsx | Static | Homepage |
| /pricing | src/app/pricing/page.tsx | Static | Pricing |
| /voice-changer/:slug | src/app/voice-changer/[slug]/page.tsx | Dynamic | Voice detail |

**Rule**: Migrated URLs must NOT change. Same paths, same content.

### Step 0.5: Classify dependencies

Read `package.json` and categorize:

| Category | Criteria | Action |
|---|---|---|
| Keep (blue) | Runtime libs not tied to Vite/Router | Reinstall after migration |
| Delete (red) | Vite plugins, old router libs, build tools | Remove in Phase 6 |
| Conditional (yellow) | Backend SDK / serverFn | Keep or delete per project needs |

### Step 0.6: Vibe coding quality diagnostic

Run `scripts/quality-diagnostic.ps1`. It checks:

1. Hardcoded hex colors (frequency count)
2. Oversized component files (> 300 lines)
3. Inline styles (`style={{ }}`)
4. `: any` type annotations
5. Flat component directories (no sub-organization)
6. SEO gaps (missing OG/json-ld/hreflang)
7. CLS risks (img without width/height/loading)
8. No performance strategy (no preload/font-display)
9. CSS redundancy (same color repeated N times)
10. Repeated long Tailwind class combinations

**Output**: Diagnostic report with impact counts per issue.

### Step 0.7: [Optional] Deeper stack analysis

Call the `tech-stack-detect` skill on the project's live URL (if deployed) to supplement the manual detection with automated 8-layer analysis.

### Gate 0

- [ ] Branch is `feature/nextjs-migration`
- [ ] Route mapping table covers all pages
- [ ] Dependencies classified into 3 categories
- [ ] Quality diagnostic report generated
- [ ] Project info confirmed (domain, pkg manager, i18n, init strategy)

---

## Phase 1: Next.js Skeleton + Design Tokens

**Goal**: Initialize Next.js 16, extract design tokens, configure security headers, copy UI base components.

### Step 1.1: Initialize Next.js 16

**Strategy A** (sub-dir, lower conflict risk):
```bash
mkdir next && cd next
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

**Strategy B** (in-place, existing project in root):
```bash
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

### Step 1.2: Configure TypeScript

Confirm `tsconfig.json` has:
```json
{ "compilerOptions": { "paths": { "@/*": ["./src/*"] } } }
```

### Step 1.3: Configure Tailwind

Check original project's Tailwind version. **Do not upgrade Tailwind during migration.** Keep same major version.

- v3: Keep `tailwind.config.ts` + `postcss.config` with standard plugins
- v4: Use `@theme { }` in CSS, `@plugin "tailwindcss-animate"` instead of JS config

### Step 1.4: Extract design tokens

This is the most critical normalization action. Use the Phase 0.6 color frequency data to map hardcoded colors to semantic tokens.

**Token mapping** (15 core + 4 advanced, validated across 5+ migration cases):

| # | Semantic Token | CSS Variable | How to determine from original project |
|---|---|---|---|
| 1 | Page background | `--background` | Most frequent background color |
| 2 | Body text | `--foreground` | Most frequent dark text color |
| 3 | Card background | `--card` | Card/panel background color |
| 4 | Card text | `--card-foreground` | Text inside cards |
| 5 | Popover background | `--popover` | Tooltip/dropdown background |
| 6 | Muted surface | `--muted` | Secondary/chip backgrounds |
| 7 | Muted text | `--muted-foreground` | Secondary/helper text |
| 8 | Border | `--border` | Divider/input border color |
| 9 | Input border | `--input` | Form input border (often same as border) |
| 10 | Brand primary | `--primary` | CTA button / link color |
| 11 | Primary text | `--primary-foreground` | Text on primary-colored surfaces |
| 12 | Accent | `--accent` | Hover state / secondary highlight |
| 13 | Focus ring | `--ring` | Focus ring color |
| 14 | Destructive | `--destructive` | Error / delete actions |
| 15 | Radius | `--radius` | Base border-radius value |

**[Optional] Call `theme-switch` skill**: Feed the extracted color frequency data to theme-switch. It will match the closest built-in theme and generate a complete `:root` CSS variable block — potentially better than manual 15-item filling.

### Step 1.5: Configure security headers

Fixed template (validated across all migration cases). Write to `next.config.ts`:

```ts
const securityHeaders = [
  { key: "X-Frame-Options", value: "SAMEORIGIN" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
];
```

Full `next.config.ts` template in `references/deployment.md`.

### Step 1.6: Configure fonts (must use `next/font`)

**Never use Google Fonts `<link>` tags.** This is the most common mistake in Lovable migrations. `next/font` provides automatic subsetting, `font-display: swap`, preload, and CSP nonce.

```ts
import { Inter } from "next/font/google";
const sans = Inter({ subsets: ["latin"], variable: "--font-sans", display: "swap", weight: ["400", "500", "600", "700"] });
```

### Step 1.7: Copy UI base components

Copy `src/components/ui/*` (shadcn/ui) and `src/lib/utils.ts`. **Every `src/components/ui/*.tsx` must have `"use client"` at the top.**

### Gate 1

- [ ] `npm run dev` starts without errors
- [ ] CSS variables (`--background`, `--foreground`, etc.) defined in `globals.css`
- [ ] All `src/components/ui/*.tsx` have `"use client"`
- [ ] `remotePatterns` covers all image CDN domains
- [ ] Fonts configured via `next/font` (not `<link>`)

---

## Phase 2: Component Migration + Normalization

**Goal**: Move all components, replace old router APIs, split large files, replace hardcoded values.

### Step 2.1: Replace old router APIs

See `references/code-rewrite.md` for full replacement rules. Key changes:

```
react-router-dom Link → next/link Link (to → href)
useNavigate() → useRouter().push() (from next/navigation)
react-helmet-async → export const metadata
@tanstack/react-router Link → next/link Link
```

### Step 2.2: Layer-based component migration

```
Level 0: Pure display (no router/hooks) → src/components/sections/ or shared/
Level 1: Depends on Level 0 + state/effects → add "use client"
Level 2: Page-level composition → prepare for Phase 4
Level 3: app/**/page.tsx → thin wrapper (metadata + Level 2 component)
```

Reorganize directories per `references/normalization-rules.md` (sections/layout/shared/ui).

### Step 2.3: Split large files

> 300 lines → must split. > 500 lines → must create sub-directory with multiple files.

### Step 2.4: Replace hardcoded styles

- Hardcoded hex → semantic token class (e.g., `bg-[#1a1a2e]` → `bg-background`)
- Inline `style={{ }}` → Tailwind class
- Repeated Tailwind arbitrary values (≥ 3 occurrences) → design token

### Step 2.5: Client boundary decisions

Add `"use client"` when component uses: useState, useEffect, onClick, Radix portals, carousels, framer-motion, useSearchParams, usePathname. Otherwise, default to Server Component.

### Gate 2

- [ ] `npx tsc --noEmit` 0 errors
- [ ] Zero remaining `react-router-dom` / `@tanstack/react-router` / `react-helmet-async` imports
- [ ] Component directories reorganized (sections/layout/shared/ui)
- [ ] Files > 300 lines split
- [ ] Inline styles replaced or TODO-marked

---

## Phase 3: Data / Types / Hooks

**Goal**: Move data files, type definitions, and custom hooks; fill in missing types.

### Steps

1. Copy `src/data/`, `src/types/`, `src/hooks/` to new project
2. Replace old router API usage in hooks (`useNavigate` → `useRouter().push()`)
3. Clean `: any` — replace with concrete types or add `// TODO: type`
4. Add `interface Props` to components missing them
5. Align dynamic route data functions with Next.js `params` types

### Gate 3

- [ ] Import paths resolve (`npx tsc --noEmit` no path errors)
- [ ] `: any` count near zero (only TODO-marked exceptions)
- [ ] Component props have explicit type interfaces

---

## Phase 4: Page Routes + SEO

**Goal**: Create all `page.tsx` files, migrate SEO metadata, add JSON-LD structured data.

### Step 4.1: Create static pages

```tsx
import type { Metadata } from "next";
import Pricing from "@/components/sections/Pricing";

export const metadata: Metadata = {
  title: "Pricing",
  description: "...",
  alternates: { canonical: "/pricing" },
};

export default function Page() {
  return <Pricing />;
}
```

### Step 4.2: Create dynamic pages (Next.js 16 / React 19 — async params)

```tsx
import { getVoiceBySlug } from "@/data/voiceChangerData";
import { notFound } from "next/navigation";
import type { Metadata } from "next";

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const voice = getVoiceBySlug((await params).slug);
  if (!voice) return {};
  return { title: voice.title, alternates: { canonical: `/voice-changer/${(await params).slug}` } };
}

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const voice = getVoiceBySlug((await params).slug);
  if (!voice) notFound();
  return <VoiceDetail voice={voice} />;
}
```

### Step 4.3: Create root layout

Full template in `references/seo-templates.md`. Key elements:

- `metadataBase` from `NEXT_PUBLIC_SITE_URL`
- Title template: `%s | BRAND_NAME`
- Navigation + Footer wrapping `{children}`
- Font CSS variable classes on `<html>`

### Step 4.4: Migrate SEO metadata

Full mapping table in `references/seo-templates.md`:

| Original | Next.js |
|---|---|
| `<title>` | `metadata.title` |
| `<meta name="description">` | `metadata.description` |
| `<link rel="canonical">` | `metadata.alternates.canonical` |
| OG tags | `metadata.openGraph.*` |
| Twitter cards | `metadata.twitter.*` |
| JSON-LD | `<script type="application/ld+json">` in layout |

### Step 4.5: Add JSON-LD structured data

**Required**: Organization + WebSite schemas in root layout. Additional schemas per page type. See `references/seo-templates.md` for all templates.

### Gate 4

- [ ] All route mapping table URLs accessible via `npm run dev`
- [ ] Visual content matches pre-migration
- [ ] Dynamic routes: valid slug renders, invalid slug → 404
- [ ] Each page has `<title>`, `<meta description>`, `<link canonical>`, OG tags

---

## Phase 5: API / Tool Pages (Optional)

**Goal**: Keep AI tool page UIs, replace backend calls with mocks.

1. Preserve complete UI components for tool pages
2. Replace `fetch` / API calls with mock data + `// TODO: connect API route`
3. Future API integration uses Next.js Route Handlers (`app/api/**/route.ts`)

### Gate 5

- [ ] Tool page UIs render without crashes
- [ ] All TODO annotations are traceable

---

## Phase 6: Clean Up Old Stack

**Goal**: Delete Vite, old router files, old dependencies; enable TypeScript strict mode.

### Step 6.1: Delete old framework files

```
vite.config.ts, index.html, src/main.tsx, src/App.tsx, src/pages/, src/routes/, wrangler.jsonc
```

### Step 6.2: Uninstall old dependencies

Remove all 🔴 category deps: `react-router-dom`, `@tanstack/react-router`, `react-helmet-async`, `vite`, `@vitejs/plugin-react`, `lovable-tagger`.

### Step 6.3: Update package.json scripts

```json
{ "dev": "next dev", "build": "next build", "start": "next start", "lint": "next lint" }
```

### Step 6.4: Enable TypeScript strict mode

In `tsconfig.json`: `"strict": true`, `"noImplicitAny": true`, `"strictNullChecks": true`.

Fix errors by priority:
1. Import path errors → fix paths
2. Possibly null/undefined → optional chaining or non-null assertion
3. Implicit any → add type annotations
4. Unfixable → `// FIXME(strict): reason` comment

### Gate 6

- [ ] `npm run build` succeeds with 0 errors
- [ ] `npx tsc --noEmit` passes in strict mode
- [ ] No remaining Vite / old router / helmet imports
- [ ] No 🔴 dependencies in package.json

---

## Phase 7: Local Validation

**Goal**: Page-by-page comparison, SEO verification, normalization audit.

Run `scripts/validate-migration.ps1` for automated checks, plus manual review:

| Check | Method |
|---|---|
| All pages render correctly | Visit each URL from route mapping table |
| Visual 1:1 match | Compare with pre-migration screenshots |
| SEO tags complete | `view-source` on each page |
| JSON-LD present | Search `application/ld+json` in source |
| Hardcoded colors reduced ≥ 80% | `rg "#[0-9a-fA-F]{6}" src/ --type tsx -c` vs Phase 0 count |
| No files > 300 lines | `find src/ -name "*.tsx" -exec wc -l {} \; \| sort -rn \| head -10` |
| Semantic HTML | `<nav>`, `<main>`, `<footer>`, `<section>` used correctly |

### Gate 7

All items in the full acceptance checklist (see `references/deployment.md` §Acceptance) must pass.

---

## Phase 8: SEO Infrastructure

**Goal**: sitemap.xml, robots.txt.

### Step 8.1: Create `src/app/robots.ts`

Template in `references/seo-templates.md`.

### Step 8.2: Create `src/app/sitemap.ts`

List all static routes + generate dynamic routes from data sources. Template in `references/seo-templates.md`.

### Gate 8

- [ ] `/sitemap.xml` returns all indexable URLs
- [ ] `/robots.txt` points to sitemap
- [ ] `/_next/static/*` has `X-Robots-Tag: noindex` header

---

## Phase 9: Vercel Deployment

**Goal**: Deploy to production, merge to main.

1. Confirm `npm run build` passes locally
2. Commit all changes to `feature/nextjs-migration`
3. Vercel Dashboard → Import this repo → Framework: Next.js
4. Configure env vars (`NEXT_PUBLIC_SITE_URL`, etc.)
5. Verify deployment on Vercel domain
6. Merge to `main`

Full deployment guide in `references/deployment.md`.

### Gate 9

- [ ] Vercel build succeeds
- [ ] All pages accessible on production URL
- [ ] `/sitemap.xml` accessible in production
- [ ] Production domain works (if DNS configured)

---

## Risk Handling

| Risk | Trigger | Action |
|---|---|---|
| Tailwind v3/v4 incompatibility | Styles missing after `npm run dev` | Check `content` paths in config; verify postcss.config matches version |
| Missing `"use client"` | Build errors about hooks in Server Component | Add `"use client"` to each reported file |
| Data only available client-side | Dynamic page needs client fetch | Move data to `src/data/`; or mark page `"use client"` with `useEffect` |
| CDN images 404 after deploy | `next/image` fails | Add domain to `remotePatterns` in `next.config.ts` |
| TypeScript strict breaks build | Many type errors after enabling strict | Fix by priority (paths → null checks → any → FIXME comments) |

---

## File Reference

| File | Purpose |
|---|---|
| `references/stack-detection.md` | Lovable tech stack detection commands + route mapping rules |
| `references/normalization-rules.md` | 7-category normalization rules (color/component/type/directory/SEO/CSS/performance) |
| `references/code-rewrite.md` | API replacement rules (Link/Navigate/Helmet/RSC boundary/fonts/images/env vars) |
| `references/seo-templates.md` | Metadata API templates, JSON-LD schemas, sitemap/robots generators |
| `references/deployment.md` | Vercel deployment config, security headers, acceptance checklist |
| `scripts/detect-lovable-stack.ps1` | Auto-detect Lovable tech stack (Vite vs TanStack Start) |
| `scripts/quality-diagnostic.ps1` | Vibe coding quality diagnostic (10-item check) |
| `scripts/validate-migration.ps1` | Post-migration validation automation |
