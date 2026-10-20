# Allsberry Insurance

Custom Next.js marketing + lead-capture site for Allsberry Insurance Agency (Corona, CA). Erin/Brahm handoff.

## Stack
- Next.js 16 App Router (webpack), React 19, TypeScript
- Tailwind CSS 4
- Framer Motion, Lucide, qrcode.react
- React Hook Form + Zod
- next-intl (i18n)
- nodemailer (`/api/leads`)
- Vercel Analytics + Speed Insights

## Layout
- `src/app/` — App Router pages (home, quote, agents, blog, evidence-of-insurance, team-attribution)
- `src/components/` — header, hero, product grids, carrier wall, footer, theme toggle
- `src/i18n/` — next-intl messages
- `src/lib/` — shared utilities, constants
- `messages/` — translation JSON
- `public/` — illustrations, email-signatures, favicons
- `scripts/` — bootstrap-local, build-local, clean-local, IndexNow submitter
- `src/proxy.ts` — Basic Auth gate for `/team-attribution` when env set

## Deploy
- Vercel (auto from main)
- Domain: `allsberryagency.com` (`www` redirects to apex)
- Node `22.17.1` (`.nvmrc`)
- Local builds use `.next-build` dir; Vercel uses default `.next`

## Conventions
- 800-line file max, organized by feature/domain
- Immutability enforced
- No hardcoded values — constants/config files
- No console.log in committed code
- Run `npm run check` (lint + typecheck) before committing
- Use `npm run setup` first when running off external `/Volumes/...` drive

## Do not touch
- `src/proxy.ts` Basic Auth logic — env-driven by `TEAM_ATTRIBUTION_USERNAME`/`PASSWORD`
- SITELEADS / Stealth ID tracking snippet integration — route-aware loader preserves agent attribution across client navigations
- `OWNER_ACTIONS_FOR_ERIN.md`, `ERIN_HANDOFF_MESSAGE.md`, `BRAHM_ERIN_MEETING_PREP.md` — handoff docs, do not silently rewrite
- `.next-build/` — local build output, ignored

## Open questions / known gaps
- `/api/leads` emails the office and optionally forwards to Zapier; AgencyZoom remains Zapier-side, not a first-party API
- `/api/chat` remains a stub with no site UI
- Team-attribution Basic Auth creds live in Vercel env, not in repo
- `allsberryagency.vercel.app` is a stale alias (404); live Vercel alias is `allsberry.vercel.app`

## Project design and source routing

Before substantive design or implementation, read the repository-root `brand.md`; it governs durable brand intent. Existing DESIGN.md derives implementation details and does not override it.

Verified local entrypoints: `/Volumes/SitHub/clients/allsberryins/brand.md`, `/Volumes/SitHub/clients/allsberryins/DESIGN.md`, `/Volumes/SitHub/clients/allsberryins/README.md`, `/Volumes/SitHub/clients/allsberryins/package.json`.

For substantial visual work, use the live `sigdesign` skill and current capability routing. Keep brand decisions human-owned; keep accessibility, reduced motion, responsive behavior and screenshot-based verification explicit. A historical design example is not a default for this project.
