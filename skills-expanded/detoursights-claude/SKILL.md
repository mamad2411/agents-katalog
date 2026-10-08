# Detour Sights — Claude Code Guide

## Project Overview

Travel discovery web app built with Next.js 14 App Router. Users browse destinations, filter places by category, and view detailed place pages with AI-generated content.

## Tech Stack

- **Framework:** Next.js 14 (App Router, plain JS — no TypeScript)
- **Database:** Neon PostgreSQL
- **Styling:** CSS Modules + CSS custom properties (design tokens in `app/globals.css`)
- **Fonts:** Playfair Display (`--font-display`) + Inter (`--font-body`) via `next/font/google`
- **Images:** Cloudinary (URLs stored in DB)

## Project Structure

```
app/
  layout.jsx                          # Root layout — fonts, Header, Footer
  page.jsx                            # Home page (server) → renders HomePage.jsx
  HomePage.jsx / HomePage.module.css  # Home page UI — SearchBar, FeaturedDestinations, FeaturedPlaces
  globals.css                         # Design tokens (CSS custom properties)
  opengraph-image.jsx                 # OG image (Next.js file convention)
  robots.js                           # robots.txt
  sitemap.js                          # XML sitemap
  destinations/
    page.jsx                          # All destinations page
    DestinationsExplorer.jsx          # Client component — region filter + destination grid
    regions.js                        # Region definitions
  places/
    page.jsx                          # All places page (paginated)
    PlacesFilterBar.jsx               # Client component — category + destination filters
    PlacesPagination.jsx              # Client component — pagination controls
  privacy/
    page.jsx                          # Privacy policy page
  [destinationSlug]/
    page.jsx                          # Destination page (server)
    DestinationPage.jsx               # Destination UI — hero, places grid, PlacesFilter
    DestinationPage.module.css
    [placeSlug]/
      page.jsx                        # Place detail page (server)
      PlacePage.jsx                   # Place UI — composes all place sub-components
      PlacePage.module.css
      components/
        PlaceHero/                    # Hero image + title
        PlaceDetailsCard/             # Hours, price, address — includes PlaceHoursRow.jsx
        PlaceMoods/                   # Mood tags
        WhyVisitSection/              # AI-generated why-visit prose
        ProseSection/                 # Generic prose block (reused for multiple sections)
        SeasonalTipsSection/          # AI-generated seasonal tips
        LocalTipsSection/             # AI-generated local tips
        WhatToBringCard/              # AI-generated packing suggestions
        AccessibilityCard/            # AI-generated accessibility info
        PlaceReviews/                 # User reviews
        DestinationPlacesCarousel/    # "More places in X" carousel
        shared.module.css             # Shared section styles across place components
  api/
    destinations/
      route.js                        # GET /api/destinations
      [slug]/route.js                 # GET /api/destinations/[slug]
    places/
      route.js                        # GET /api/places
      [slug]/route.js                 # GET /api/places/[slug]
    nearby/
      route.js                        # GET /api/nearby — nearby destinations by coords

components/                           # Shared, reusable components
  Header.jsx / Header.module.css      # Server shell — renders HeaderClient
  HeaderClient.jsx / HeaderClient.module.css  # Client — scroll behavior, mobile state
  HeaderMenu.jsx / HeaderMenu.module.css      # Mobile nav menu
  SearchBar.jsx / SearchBar.module.css
  PlacesFilter.jsx / PlacesFilter.module.css  # Client — multi-select category filter
  FeaturedDestinations.jsx            # Homepage destinations carousel section
  FeaturedPlaces.jsx                  # Homepage places carousel section
  CarouselRow.jsx                     # Horizontal scroll carousel primitive
  NearbyDestinations.jsx              # Nearby destinations (uses geolocation API)
  PersonalizedSuggestions.jsx         # Personalized place suggestions
  Gallery.jsx / GallerySection.jsx / GalleryThumbnail.jsx  # Photo gallery
  PlaceMap.jsx                        # Embedded map for place detail
  WhyVisit.jsx                        # Standalone why-visit card (used outside place page)
  SetRecentDestination.jsx            # Client — persists recent destination to localStorage
  Footer.jsx / Footer.module.css

lib/
  prisma.js                           # Prisma client singleton
  analytics.js                        # GA4 event helpers
  media-queries.js                    # Shared breakpoint constants
  recentDestination.js                # Recent destination read/write (localStorage)
  utils/
    slug.js                           # Shared toSlug() utility
  scripts/
    destinations/                     # add-destinations.js, remove-destinations.js
    places/                           # import-scribekit-results.js, scribe-kit-content.json
    images/                           # get-destination-images.js, get-place-images.js

prisma/
  schema.prisma                       # DB schema
  seed.js                             # Seed data (91 destinations, 184 hand-curated places)

public/                               # Static assets (logos, icons — NOT destination images)
jsconfig.json                         # Path alias: @/* → ./*
```

## Rules

1. When modifying, refactoring, or updating code, always update relevant comments, docstrings, and JSDoc/TSDoc to reflect the changes.
2. If a comment becomes obsolete after a change, remove it.

## Key Conventions

- **Path alias:** Use `@/` for all imports (e.g. `@/components/Header`, `@/lib/prisma`)
- **Server vs client:** Pages are server components by default. Add `'use client'` only when state/interactivity is needed
- **CSS:** Always use CSS Modules + design tokens. Never inline styles or use Tailwind.
- **Design tokens:** Defined in `app/globals.css`. Always use `var(--token-name)` — do not hardcode colors or fonts.
- **Images:** Store Cloudinary URLs in the DB (`coverImageUrl` on Destination/Place). Use `next/image` with `remotePatterns` for Cloudinary. Static site assets go in `/public`.

## Design Tokens (key ones)

```css
--color-accent         /* #E8602C — terracotta, primary CTA */
--color-accent-dark    /* #C94E1F — hover state */
--color-accent-light   /* #FBF0EB — pill/tag backgrounds */
--color-ink            /* #1C2B3A — primary text */
--color-ink-secondary  /* #4A5D6E */
--color-ink-muted      /* #8A99A8 */
--color-bg             /* #FDFAF7 — page background */
--color-surface        /* #FFFFFF — card/panel background */
--color-border         /* #E8E0D8 */
--font-display         /* Playfair Display — headings */
--font-body            /* Inter — body text */
```

## Database

- **Provider:** PostgreSQL (Neon)
- **ORM:** Prisma 5
- **Key models:** `Destination`, `Place`, `PlaceAiGenData`, `Category`, `PlaceCategory` (join), `Mood`, `PlaceMood` (join), `SeasonalTipAiGen`, `Review`, `Photo`, `User`
- **Place slugs:** unique per destination via composite key `@@unique([destinationId, slug])` — not globally unique
- **Price range enum:** `FREE | BUDGET | MODERATE | EXPENSIVE | VERY_EXPENSIVE`

## Deployment

- **Deploy:** push to `main` — GitHub Actions runs lint, then migrations, then `vercel deploy --prod`. Vercel builds the source (no `--prebuilt`; the CLI's prebuilt file-tracing dropped `client-only`/`styled-jsx` from the function bundle and broke prebuilt deploys)
- **Git integration:** Vercel's automatic Git deploys are disabled on `main` via `vercel.json` (`git.deploymentEnabled.main = false`) so CI is the sole deployer — otherwise every push double-deploys (once from CI, once from the Git integration)
- **CI pipeline:** `.github/workflows/ci.yml` — lint → migrate → deploy (no E2E tests; they were removed to avoid DB writes and GA pollution)
- **Migrations:** run `npx prisma migrate deploy` locally before pushing if there are pending schema changes — CI runs migrations against Neon prod as part of the deploy job
- **Secrets required in GitHub:** `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`, `DATABASE_URL`, `DATABASE_URL_UNPOOLED`

## Common Commands

```bash
npm run dev          # Start dev server
npm run db:seed      # Seed database
npm run db:migrate   # Run migrations (dev)
npm run db:studio    # Open Prisma Studio
npm run db:generate  # Regenerate Prisma client after schema changes
npm run lint         # ESLint (zero warnings)
```

## Seed File Notes

- Located at `prisma/seed.js`
- 91 destinations, 184 hand-curated places — used for local dev resets only
- Has deduplication logic — safe to re-run
- Update `update: { description: d.description }` to propagate description changes on re-seed
- Production places (~980 total) are not in the seed file — they are imported via ScribeKit using `lib/scripts/places/import-scribekit-results.js`
