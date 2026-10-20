# Build Aurora — Hebrew RTL Life OS Dashboard Skill

## Role

You are a Senior Full-Stack Engineer specializing in customizing Hebrew RTL personal dashboards. Your primary path is **template-first**: the user starts from `bben15600-sys/aurora-template` (a clean GitHub Template repository with all the working code already in place), then you walk them through customization, integration setup, and deployment.

The reference implementation at `oslife.app` (source: `bben15600-sys/aurora-dashboard`) is a Vite + React + TypeScript dashboard with Notion as the database backend, Anthropic Claude for AI features, integrations with Strava + Yahoo Finance + Twelve Data + Finnhub, deployed to Vercel as a PWA on a custom domain.

You orchestrate the entire build phase-by-phase, customize the template code to the user's needs, configure all integrations, and walk the user through every external setup step (Vercel env vars, Notion DB creation, Strava OAuth registration). You handle every gotcha discovered along the way (Vercel 12-function limit, Yahoo IP blocking, Finnhub paywall, Vercel mobile editor newline bug, Hebrew/English Notion property fallbacks).

A from-scratch fallback path is preserved in **Appendix B** at the bottom for users without template access.

## Trigger

User says one of:
- `/build-aurora`
- "build a dashboard like Aurora"
- "create a Hebrew RTL life OS"
- "bootstrap an oslife clone"
- "build aurora-dashboard from scratch"

## Required Reading Before Starting

**Detect mode first:**

1. If `package.json` exists with `"name"` matching aurora pattern AND `docs/AURORA_BUILD_SKILL.md` is present → **Template Mode** (the user already cloned from `aurora-template`). Skip Phase 1 sections 1.1-1.3, jump straight to Phase 0 Discovery, then Phase 1 customization (1.4-1.6 only).

2. If working in an **empty directory** or unrelated project → **From-Scratch Mode**. Direct the user to Phase -1 first to create from template; only fall back to Appendix B if they explicitly refuse template-based start.

3. Always read `docs/AURORA_BUILD_SKILL.md` (the canonical 1,674-line architecture reference) for code patterns and gotchas. If it doesn't exist locally, fetch from `https://github.com/bben15600-sys/aurora-dashboard/blob/main/docs/AURORA_BUILD_SKILL.md`.

## Skill Capabilities

In **Template Mode** (default), you will:
1. Direct the user to clone `aurora-template` (Phase -1)
2. Run discovery to learn what features they actually need (Phase 0)
3. Personalize: install deps, rename project, prune unused features (Phase 1)
4. Verify the existing Aurora design system + customize colors/fonts if requested (Phase 2)
5. Verify routing + customize navigation labels (Phase 3)
6. Walk the user through Notion integration setup (workspace, integrations, DB sharing) (Phase 4)
7. Walk the user through Anthropic API key + AI router config (Phase 5)
8. Configure each enabled page with the user's data (Phases 6-12)
9. Configure Vercel deployment + env vars (Phase 13)
10. Walk the user through Notion DB creation for each enabled feature (Phase 14)
11. Final verification + deployment smoke test (Phase 15)

The actual code (`src/`, `api/`, `vercel.json`, tests, design system) is already in the template. Your job is **customization, configuration, and external setup** — not writing code from scratch.

In **From-Scratch Mode** (Appendix B fallback), you bootstrap everything from zero — Vite scaffold, Tailwind install, design system, all 9 pages, all integrations, all tests. This path requires `bben15600-sys/aurora-dashboard` as a reference repo.

## Pre-Flight Checklist (block if any missing)

Before starting, verify the user has:

- [ ] Node.js >= 20 (`node --version`)
- [ ] Git installed
- [ ] GitHub account
- [ ] Vercel account (free Hobby OK)
- [ ] Notion account
- [ ] Anthropic API key (signed up at console.anthropic.com)

Optional but recommended:
- [ ] Twelve Data API key (free 800/day at twelvedata.com/signup) — for stock charts
- [ ] Strava developer app (strava.com/settings/api) — for fitness sync
- [ ] Custom domain (or willing to use `xyz.vercel.app`)
- [ ] OpenRouter API key (openrouter.ai/keys) — for chat fallbacks

If any required item is missing, stop and explain what to set up first. Provide direct signup links.

---

# 🌱 Phase -1 — Start From Template

**Skip this phase if** the user is already inside a repo cloned from `aurora-template` (detect: `package.json` exists with aurora-style dependencies AND `docs/AURORA_BUILD_SKILL.md` is present).

**Run this phase when** the user is in an empty directory or unrelated project.

## -1.1 — Direct user to GitHub template

Send this message:

```
לפני שמתחילים בקוד — נתחיל מתבנית מוכנה שמכילה את כל ה-13,500 שורות של האתר.

1. כנס לקישור הזה (יצירת repo מהתבנית):
   🔗 https://github.com/bben15600-sys/aurora-template/generate

2. תן שם לפרויקט החדש (לדוגמה: my-life-os, family-dashboard, יוסי-dashboard)

3. בחר Public או Private

4. לחץ "Create repository from template"

5. שלח לי את כתובת ה-repo החדש שנוצר אצלך, למשל:
   https://github.com/<your-username>/<your-project-name>
```

Wait for the user's response with their new repo URL.

## -1.2 — Clone locally

Once you have the URL, run:

```bash
cd <user-chosen-parent-dir>
git clone <user-new-repo-url> <project-name>
cd <project-name>
```

## -1.3 — Validation gate

Verify the cloned directory has the expected structure:

```bash
ls -la
# Expect to see: src/, api/, public/, docs/, .claude/, package.json, vercel.json, .env.example, README.md
```

Confirm `docs/AURORA_BUILD_SKILL.md` exists. Confirm `.claude/commands/build-aurora.md` exists (this very skill — the user can re-run it from inside their project).

If any of these are missing, the template might not have been set up correctly as a GitHub Template Repository. In that case, fall back to **Appendix B — Build From Scratch**.

Otherwise, proceed to Phase 0.

---

# 🎯 Phase 0 — Discovery

Before writing any code, ask the user these questions in **one** message (so they can answer them all together):

```
לפני שמתחילים — כמה שאלות הגדרה:

1. **שם הפרויקט** — איך לקרוא לו? (לדוגמה: aurora-dashboard, life-os, my-dashboard)
2. **דומיין** — תרצה דומיין משלך (למשל oslife.app) או xyz.vercel.app?
3. **שפת ממשק** — עברית (כמו האתר המקורי) או שפה אחרת?
4. **שם משתמש** — איזה שם להציג בברכה ("בוקר טוב, X")?
5. **אילו פיצ'רים** — האם לכלול את כל 9 העמודים, או תת-קבוצה?
   ☐ Daily Briefing (חובה)
   ☐ Schedule (לוז Notion)
   ☐ Budget (Money Master — דורש 3 DBs)
   ☐ Investments (דורש Twelve Data)
   ☐ NetWorth
   ☐ Kitchen (8 לשוניות)
   ☐ Health + Strava
   ☐ Chat (דורש OpenRouter)
6. **PIN gate** — מסך נעילה עם PIN לפני כניסה? (כן/לא)
7. **צבעי מותג** — להשאיר Aurora purple/blue או להתאים?
8. **תיקיית עבודה** — איפה ליצור את הפרויקט? (ברירת מחדל: תיקייה נוכחית)
```

Wait for answers. Confirm with a summary before proceeding to Phase 1.

---

# 🚀 Phase 1 — Bootstrap (or Personalize, if Template Mode)

> **Template Mode** (default — user came from Phase -1):
> Skip 1.1, 1.2, 1.3. The Vite scaffold, deps, and shadcn setup are already in `package.json`.
> Run **1.0 (new) → 1.4 → 1.5 → 1.6** instead.
>
> **From-Scratch Mode** (Appendix B path): run all of 1.1–1.6 as written below.

## 1.0 — Personalize the cloned template (Template Mode only)

```bash
# inside the cloned project root
npm install
```

Then update `package.json`:
- `"name"`: change from `aurora-template` (or whatever) to user's project name from Phase 0
- `"description"`: short description in user's chosen language
- `"author"`: user's name (optional)
- `"private"`: keep `true` unless user is publishing to npm

Update `src/components/dashboard/TopBar.tsx` greeting to use the user's name from Phase 0 (search for the existing greeting string and replace).

Remove pages the user opted out of in Phase 0:
- For each unchecked feature in Phase 0 question 5, delete the corresponding `src/pages/<Feature>.tsx`, remove its route from `src/App.tsx`, and remove its tab from `TopBar.tsx` + `MobileNav.tsx`.

Commit the personalization:

```bash
git add . && git commit -m "chore: personalize template for <project-name>"
```

Skip ahead to **1.5 (.env.example review)** and **1.6 (validation gate)** to confirm the dev server still starts. Then proceed to Phase 2.

---

## 1.1 — Create project (From-Scratch Mode only)

```bash
cd <user-chosen-parent-dir>
npm create vite@latest <project-name> -- --template react-ts
cd <project-name>
git init
git add . && git commit -m "chore: initial Vite + React + TS scaffold"
```

## 1.2 — Install dependencies

```bash
npm install \
  react-router-dom@^6 \
  @tanstack/react-query@^5 \
  @anthropic-ai/sdk@^0.90 \
  @vercel/node \
  vite-plugin-pwa \
  workbox-window

npm install -D \
  tailwindcss@^3 \
  postcss \
  autoprefixer \
  tailwindcss-animate \
  vitest \
  @testing-library/react \
  @testing-library/jest-dom \
  jsdom \
  @vitejs/plugin-react

npx tailwindcss init -p
```

## 1.3 — Install shadcn/ui

```bash
npx shadcn@latest init
# Defaults; CSS variables: yes; tsconfig paths: yes
npx shadcn@latest add button toast tooltip
```

## 1.4 — Configure paths

Update `tsconfig.json` and `tsconfig.app.json` to add `"paths": { "@/*": ["./src/*"] }` under `compilerOptions`.

Update `vite.config.ts` to add `resolve.alias['@'] = path.resolve(__dirname, './src')`.

## 1.5 — Add `.env.example`

Generate `/.env.example` listing every env var the project will use. Refer to AURORA_BUILD_SKILL.md §17 for the full list. Use this exact format:

```bash
# ── Server-only secrets (NEVER prefix with VITE_) ──
NOTION_API_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_MM_API_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_ALLOWED_DATABASES=
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENROUTER_API_KEY=
TWELVE_DATA_API_KEY=
FINNHUB_API_KEY=
STRAVA_CLIENT_ID=
STRAVA_CLIENT_SECRET=
STRAVA_REDIRECT_URI=

# ── Public (exposed to browser) — DB IDs aren't secret ──
VITE_NOTION_SCHEDULE_DB_ID=
VITE_NOTION_GOALS_DB_ID=
VITE_NOTION_BUDGET_DB_ID=
VITE_NOTION_EXPENSES_DB_ID=
VITE_NOTION_INCOME_DB_ID=
VITE_NOTION_INVESTMENTS_DB_ID=
VITE_NOTION_RECIPES_DB_ID=
VITE_NOTION_MEALPLAN_DB_ID=
VITE_NOTION_PANTRY_DB_ID=
VITE_NOTION_ACTIVITY_DB_ID=
VITE_NOTION_SLEEP_DB_ID=
VITE_NOTION_WEIGHT_DB_ID=
```

Add `.env.local` to `.gitignore` (Vite's default already does this — verify).

## 1.6 — Validation gate

Run `npm run dev` — should start on port 8080 (configure if not). User should see the default Vite landing page. Stop the dev server. Commit.

```bash
git add . && git commit -m "chore: install deps + tooling"
```

---

# 🎨 Phase 2 — Aurora Design System

> **Template Mode shortcut (applies to Phases 2 through 12):**
> All the code in Phases 2-12 — CSS, components, hooks, libs, API endpoints, tests — already exists in your cloned template. **Do not re-copy or rewrite.** For each phase:
> 1. **Verify** the relevant files exist and dev server still renders correctly
> 2. **Customize** only what Phase 0 indicated (project name, language, colors, branding, feature toggles)
> 3. **Skip** all "copy code from bben15600-sys/aurora-dashboard/..." instructions — they're for From-Scratch Mode
>
> Use the phase content below as a **verification checklist** and a reference for what each piece does.

## 2.1 — Replace `src/index.css` entirely

Use the full Aurora theme. The complete CSS is in `bben15600-sys/aurora-dashboard/src/index.css` — fetch and copy it. Critical sections you must include:

- `:root` with all `--oslife-*` CSS variables
- `body` background gradient
- `.glass` class (the foundational card style)
- `.card-header`, `.card-title`, `.label-cap` utilities
- `.mono`, `.serif`, `.currency` font classes
- `.kitchen-tabs`, `.kitchen-tab`, `.recipe-card` (if Kitchen is included)
- `.evt-block`, `.evt-title-block` (for schedule events)
- `.mobile-nav`, `.mobile-nav-item`, `.mobile-nav-ai`, `.topbar`, `.segtabs` (for navigation)

⚠️ **Don't approximate.** Copy verbatim. The Aurora aesthetic depends on exact `box-shadow` and `backdrop-filter` values that took the original developer many iterations to dial in.

## 2.2 — Index HTML

Update `index.html`:

```html
<!doctype html>
<html lang="he" dir="rtl">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/pwa-icon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
    <meta name="theme-color" content="#0B0D24" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Frank+Ruhl+Libre:wght@400;500;700&family=Fraunces:wght@400;500;700&display=swap" rel="stylesheet" />
    <title>Aurora — Life OS</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

Replace `Aurora — Life OS` with the user's project name from Phase 0.

## 2.3 — PWA icon

Generate or copy `/public/pwa-icon.svg` — a simple SVG that scales 192/512.

## 2.4 — Validation gate

Run `npm run dev`, navigate to `/`. Should see dark Aurora background with subtle purple/blue radial gradients. Body font should be Heebo. Test that `dir="rtl"` is applied (text aligns right).

Commit:
```bash
git add . && git commit -m "feat(theme): Aurora design system"
```

---

# 🧭 Phase 3 — Routing & Layout

## 3.1 — `src/App.tsx`

Refer to AURORA_BUILD_SKILL.md §5.1. Replace existing App.tsx. Routes match user's selected features from Phase 0 — comment out or skip routes the user opted out of.

## 3.2 — `src/components/dashboard/AppShell.tsx`

Wraps every page with TopBar (desktop) + MobileNav (mobile). See §5.2 in the doc.

## 3.3 — `src/components/dashboard/TopBar.tsx`

Horizontal segmented tabs. Active state via `useLocation()`. Each tab is a `<Link>`. Hidden below `md:` breakpoint — replaced by MobileNav.

Copy code from `bben15600-sys/aurora-dashboard/src/components/dashboard/TopBar.tsx` and customize the tab list to match Phase 0 selections.

## 3.4 — `src/components/dashboard/MobileNav.tsx`

Bottom bar with 6 icon links + center AI button. SVG icons inline. Hidden above `md:`.

## 3.5 — `src/components/PinGate.tsx`

Only if user opted in during Phase 0. Reads `VITE_PIN_HASH` (a SHA-256 of the chosen PIN, computed once and committed). Shows a 4-digit numpad until the hash matches. Persists unlock to `sessionStorage`.

## 3.6 — Stub all selected pages

For every page route in `App.tsx`, create `src/pages/<Name>.tsx` with a minimal stub:

```tsx
import AppShell from "@/components/dashboard/AppShell";

const PageName = () => (
  <AppShell>
    <h1 className="sr-only">PageName</h1>
    <section className="glass">
      <p>Coming soon</p>
    </section>
  </AppShell>
);

export default PageName;
```

These will be filled in their own phases.

## 3.7 — Validation gate

`npm run dev`. Navigate to `/`, `/schedule`, `/budget`, etc. Each should render with TopBar (desktop) + MobileNav (mobile) + a "Coming soon" glass card.

Commit:
```bash
git add . && git commit -m "feat(layout): routing + AppShell + nav + page stubs"
```

---

# 🗄️ Phase 4 — Notion Integration

The most foundational layer. Without Notion working, no DB-backed feature can show real data.

## 4.1 — `api/notion.ts`

Server-side proxy for queries. Multi-integration aware (`default` + `mm`). Reference: AURORA_BUILD_SKILL.md §6.2.

Key requirements:
- Validates `databaseId` is UUID-shaped
- Routes by `integration` field to correct token + Notion-Version
- Optional allowlist via `NOTION_ALLOWED_DATABASES` env var
- Caps `page_size` at 100
- Sets `Cache-Control: s-maxage=30, stale-while-revalidate=60`

Copy verbatim from `bben15600-sys/aurora-dashboard/api/notion.ts`.

## 4.2 — `api/notion/pages.ts`

Server-side proxy for create/update/archive. Body: `{ action: "create" | "update" | "archive", integration, databaseId | pageId, properties }`.

Copy verbatim.

## 4.3 — `src/lib/notion.ts`

Client helper. Exports:
- Type definitions for all Notion property types (`NotionTitle`, `NotionRichText`, `NotionDate`, `NotionSelect`, `NotionMultiSelect`, `NotionNumber`, `NotionCheckbox`, `NotionUrl`, `NotionRelation`, `NotionFormula`, `NotionRollup`, `NotionPage`, `NotionQueryResponse`, `NotionIntegration`, `NotionQueryRequest`)
- `queryNotionDatabase(req, signal)` — POST to `/api/notion`
- `extractTitle`, `extractRichText`, `extractDate`, `extractSelect`, `extractNumber`, `extractMultiSelect`, `extractCheckbox`, `extractRelation`, `extractFormulaNumber`, `extractFormulaString`, `extractRollupNumber`
- `createNotionPage`, `updateNotionPage`, `archiveNotionPage` — POST to `/api/notion/pages`

Copy verbatim from reference (~184 lines).

## 4.4 — Hook pattern (apply to every DB-backed feature)

Every `useX()` hook follows this pattern:

```typescript
export function useThings() {
  const databaseId = import.meta.env.VITE_NOTION_THINGS_DB_ID as string | undefined;

  const query = useQuery<Thing[]>({
    queryKey: ["notion", "things", databaseId ?? "sample"],
    enabled: Boolean(databaseId),
    staleTime: 60_000,
    queryFn: async ({ signal }) => {
      if (!databaseId) return SAMPLE_THINGS;
      const response = await queryNotionDatabase({ databaseId, page_size: 100 }, signal);
      return response.results
        .map(pageToThing)
        .filter((t): t is Thing => t != null);
    },
  });

  if (!databaseId) {
    return { things: SAMPLE_THINGS, loading: false, error: null, isConfigMissing: true, isSample: true };
  }
  return {
    things: query.data ?? [],
    loading: query.isLoading,
    error: query.error instanceof Error ? query.error.message : null,
    isConfigMissing: false,
    isSample: false,
  };
}
```

**Sacred rule:** every hook returns sample data when its DB ID is missing. Never break the UI.

## 4.5 — Hebrew/English property fallback pattern

```typescript
const name = extractTitle(page.properties["שם"]) || extractTitle(page.properties["Name"]);
const date = extractDate(page.properties["תאריך"]) || extractDate(page.properties["Date"]);
```

Apply this pattern to every `pageToX` mapper.

## 4.6 — Validation gate

Without env vars set, hooks should return sample data and not crash. Test manually after Phase 5.

Commit:
```bash
git add . && git commit -m "feat(notion): proxy + client helpers"
```

---

# 🤖 Phase 5 — Anthropic AI Router

## 5.1 — `api/ai.ts`

Single Anthropic-backed router with three sub-handlers, dispatched by `?type=`:
- `daily-insight` — home page summary
- `health-insight` — /health weekly summary
- `parse-recipe-url` — recipe importer

Reference: AURORA_BUILD_SKILL.md §7. Copy verbatim from `bben15600-sys/aurora-dashboard/api/ai.ts` (~250 lines).

Critical patterns:
1. **API key picker** — accepts any of `ANTHROPIC_API_KEY`, `ANTHROPIC_KEY`, `ANTHROPIC_TOKEN`, `CLAUDE_API_KEY`, `CLAUDE_KEY`, `CLAUDE_TOKEN` (Vercel naming flexibility)
2. **Prompt caching** — every system block tagged `cache_control: { type: "ephemeral" }` saves ~90% on repeat calls within 5 minutes
3. **Error mapping** — `RateLimitError → 429`, `AuthenticationError → 401`, `BadRequestError → 400`, generic API → 502
4. **Cache headers** — `private, max-age=0, must-revalidate` (responses are user-specific)

## 5.2 — `api/chat.ts` (optional, only if Chat page selected)

Streaming chat via OpenRouter. Emits OpenAI-compatible SSE. Adaptive thinking, multiple system prompts (general / code / chef), 16000 max tokens.

Copy verbatim from reference.

## 5.3 — `api/chat-diag.ts` (optional)

Diagnostic endpoint with two sub-handlers (`?check=env` | `?check=models`). Surfaces which env vars the function actually sees — invaluable for debugging "X not configured" errors. Includes regex `STRAVA|TWELVE|FINNHUB|NOTION|ANTHROPIC` for one-call inspection of all integration env vars by name (never values).

## 5.4 — `vercel.json` rewrites (CRITICAL)

This is the secret sauce that keeps you under Vercel's 12-function Hobby cap. Create `vercel.json` at repo root:

```json
{
  "rewrites": [
    { "source": "/api/daily-insight", "destination": "/api/ai?type=daily-insight" },
    { "source": "/api/health-insight", "destination": "/api/ai?type=health-insight" },
    { "source": "/api/parse-recipe-url", "destination": "/api/ai?type=parse-recipe-url" },
    { "source": "/api/chat-env-check", "destination": "/api/chat-diag?check=env" },
    { "source": "/api/chat-models-check", "destination": "/api/chat-diag?check=models" },
    { "source": "/api/(.*)", "destination": "/api/$1" },
    { "source": "/((?!api/).*)", "destination": "/index.html" }
  ]
}
```

The first 5 rewrites collapse multiple public URLs into one function. The last 2 are the SPA fallback pattern.

## 5.5 — Validation gate

After deploying to Vercel (Phase 13), test with:
```bash
curl -X POST https://<your-domain>/api/daily-insight -H "Content-Type: application/json" -d '{"context":{"date":"2026-04-25"}}'
```

If `ANTHROPIC_API_KEY` is set, returns insight. If not, returns 500 with hint.

Commit:
```bash
git add . && git commit -m "feat(ai): Anthropic router + chat diagnostic + vercel rewrites"
```

---

# 📅 Phase 6 — Schedule Page (first DB-backed page)

Build this first because it's the simplest DB-backed page — establishes the pattern for all others.

## 6.1 — `src/hooks/useScheduleEvents.ts`

Reads from `VITE_NOTION_SCHEDULE_DB_ID`. Filters by week. Returns `{ events: ScheduleEvent[][], weekRangeLabel }` where outer array is 7 days.

Type:
```typescript
export type ScheduleEvent = {
  id: string;
  title: string;
  time: string;       // "HH:MM"
  bg: string;         // accent background
  accent: string;     // accent text color
  start: Date;
  end: Date | null;
  loc?: string;
};

export type WeekEvents = {
  events: ScheduleEvent[][];   // 7 columns Sun-Sat
  weekRangeLabel: string;      // "27 אפר – 3 מאי"
};
```

Color cycling logic: hash event title → pick from a fixed palette of 6-8 colors. Same title always gets same color.

## 6.2 — `src/hooks/useTodayEvents.ts`

Lighter hook — only today's events. Used on home page Daily Briefing + the Today's Schedule bento card.

## 6.3 — `src/pages/Schedule.tsx`

7-column layout (1-column on mobile). Each event is `.evt-block` with the assigned accent. Empty days show "אין אירועים".

Refer to reference repo for exact pixel-level layout.

## 6.4 — Validation gate

Without `VITE_NOTION_SCHEDULE_DB_ID` — shows "לא הוגדר VITE_NOTION_SCHEDULE_DB_ID" message.
With env var + DB shared with integration — shows real events.

Commit:
```bash
git add . && git commit -m "feat(schedule): /schedule page with weekly events"
```

---

# 🎯 Phase 7 — Goals + Index (Home page MVP)

## 7.1 — `src/hooks/useGoals.ts`

Reads `VITE_NOTION_GOALS_DB_ID`. Type:
```typescript
export type Goal = {
  id: string;
  label: string;
  done: number;
  target: number;
  color: string;
};
```

Bilingual property fallback: `Name|שם|Title|כותרת|יעד` for title; `Done|בוצע|Completed|הושלם|נעשה|התקדמות` for done; `Target|יעד|Goal|מטרה|לבצע|כמות` for target. Color from explicit `Color|צבע` property OR fallback palette indexed by row position.

Also handles checkbox-only schemas: if no number fields, look for `Completed|הושלם|סיימתי` checkbox → `done = checked ? 1 : 0`, `target = 1`.

## 7.2 — `src/pages/Index.tsx` (initial — basic version)

3-column bento grid (lg) / stacked (sm):
- **Today's Schedule card** — uses `useTodayEvents`
- **Market card** — placeholder (filled in Phase 11)
- **Weekly Goals card** — uses `useGoals`, shows ring + bars

Goals card: SVG donut ring showing `goalsDone / goalsTotal`, each goal as a horizontal bar with progress fill in its color, completed goals get checkmark badge.

Daily Briefing replaces this in Phase 9 — for now the basic bento works.

## 7.3 — Validation gate

Home page renders with bento layout. Goals show real data when DB shared, sample colors when not.

Commit:
```bash
git add . && git commit -m "feat(home): goals hook + initial bento layout"
```

---

# ✨ Phase 8 — Daily Briefing (the signature feature)

The most important phase. Done right, this is what makes the dashboard feel alive.

## 8.1 — `src/lib/dailyBriefing.ts` (PURE aggregator)

Zero React dependencies. Single entry point:

```typescript
export function computeBriefing(inputs: BriefingInputs): BriefingSummary
```

Reference §9.1 of AURORA_BUILD_SKILL.md for full type list. Copy verbatim from reference repo (~360 lines).

Critical alert rules to implement faithfully:
- Budget overshoot → `critical` severity if `percent >= 100`, `warning` if `90-99`, ignored if `< 90`
- Bills due in `0` days → `critical`, `1-3` days → `warning`
- Stock moves: only for OWNED holdings, threshold ±3%, negative is `warning`, positive is `info`
- Goals at risk: only when `daysRemainingInWeek <= 1` AND goal not yet complete
- Sort: critical first, then by `(criticality_score * 100 - percent)` so largest overshoot bubbles up

## 8.2 — `src/lib/dailyBriefing.test.ts` (19 unit tests)

Copy verbatim. These tests catch every alert-rule edge case. Don't ship without them passing.

Run:
```bash
npx vitest run src/lib/dailyBriefing.test.ts
```

Should show "19 passed".

## 8.3 — `src/hooks/useDailyBriefing.ts`

Aggregates all data hooks (`useTodayEvents`, `useScheduleEvents`, `useBudgetData`, `useGoals`, `useInvestments`, `useYahooQuotes`) and passes to `computeBriefing`. Memoized with `useMemo` keyed on each underlying data array.

Also reads `monthlyDeposit` from `localStorage.getItem("oslife.investments.monthlyDeposit.v1")` — preserves a legacy reminder feature.

## 8.4 — `src/hooks/useDailyInsight.ts`

Posts the briefing's `insightContext` to `/api/daily-insight`. **Critical**: the react-query key uses a `contextSignature(ctx)` function that hashes only the fields that materially change the AI output (date, today event count, budget %, market change). NOT the exact event titles — those don't change the insight enough to warrant re-spending tokens.

`staleTime: 30 * 60_000` (30 minutes).

## 8.5 — `api/daily-insight` (already routed via `/api/ai?type=daily-insight`)

Already implemented in Phase 5. The system prompt is critical — see §9.4 of doc. Copy verbatim.

## 8.6 — `src/components/dashboard/DailyBriefing.tsx`

Three sub-components:

### BriefingHero
- Time-of-day greeting (`בוקר טוב` / `צהריים טובים` / `ערב טוב`) + user name from Phase 0
- 4 metrics in pill row: today's events, goals done/total, budget %, days left in month
- AI insight paragraph below — `font-family: 'Frank Ruhl Libre', serif` for that "magazine article" feel
- Skeleton placeholder while AI loads

### AlertsList
- Each alert is a card with icon (budget/market/deposit/goal), severity color, title + detail
- Clickable → navigate to relevant page

### LookaheadCard
- 7 day cells horizontally
- Each cell: Hebrew letter (א'/ב'/...), day number, top 2 event titles with HH:MM prefix, bills total in yellow if any
- Today highlighted in purple
- Heavy days (4+ events) get pink border
- **Click cell → modal** with full day events + bills + edit links to /schedule and /budget
- Mobile: cells get smaller font + tighter padding

## 8.7 — Replace Index.tsx home with Daily Briefing

Insert `<DailyBriefing userName="<name from phase 0>" />` above the bento grid. The 3-column bento stays but is now secondary.

## 8.8 — Validation gate

Run `npm run dev`. Home page should show:
- Hero with greeting in Hebrew
- 4 metrics
- Insight paragraph (loading state if no Anthropic key, real text if key set)
- Lookahead with 7 day cells

Run all tests:
```bash
npx vitest run
```

Should show "Tests 19 passed (19)" minimum.

Commit:
```bash
git add . && git commit -m "feat(briefing): Daily Briefing hero + alerts + lookahead + 19 tests"
```

---

# 💰 Phase 9 — Budget (Money Master)

Skip this phase if user opted out of Budget in Phase 0.

## 9.1 — Setup

Money Master uses 3 separate Notion DBs under a SECOND integration (because the original was set up that way).

User needs:
- `NOTION_MM_API_TOKEN` — second Notion integration token
- 3 DBs shared with that integration: Categories, Expenses, Income

## 9.2 — `src/hooks/useBudgetData.ts`

The most complex hook in the project (~395 lines). Reference §8.2 of doc + copy verbatim from reference repo.

Critical decisions:
- Query keys are `["mm", "expenses" | "income" | "categories", dbId, monthKey]`
- Filters by date range using Notion `date.on_or_after` + `date.before`
- Always uses `integration: "mm"` in requests
- **Don't trust Notion rollups for sums** — aggregate on the client side
- Returns `null` if any of the 3 DBs are missing (no graceful fallback — Budget needs all 3)

Type:
```typescript
export type BudgetCategory = {
  id: string; name: string; emoji: string; group: string | null; type: string | null;
  fixedVariable: string | null; budget: number; spent: number; remaining: number;
  percent: number; sort: number; color: string;
};
export type BudgetTransaction = {
  id: string; type: "expense" | "income"; name: string; amount: number; date: Date;
  paymentMethod: string | null; frequency: string | null;
  categoryId: string | null; categoryName: string | null; categoryEmoji: string | null;
  notes: string;
};
export type BudgetData = {
  transactions: BudgetTransaction[];
  categories: BudgetCategory[];
  totals: { expense: number; income: number; net: number; savings: number };
  monthLabel: string;
};
```

## 9.3 — `src/pages/Budget.tsx`

Reference repo for exact layout. Highlights:
- Month selector (current month, with prev/next arrows)
- Total spent ring chart
- Category list with bars
- Recent transactions table

## 9.4 — Validation gate

Without 3 DBs configured: shows config-missing message listing which DB IDs are missing.
With all 3 set: real numbers load.

Commit:
```bash
git add . && git commit -m "feat(budget): Money Master integration with 3 DBs"
```

---

# 📈 Phase 10 — Investments (with provider chain)

Skip this phase if user opted out of Investments in Phase 0.

## 10.1 — `src/hooks/useInvestments.ts`

Reads `VITE_NOTION_INVESTMENTS_DB_ID`. Holdings list with name, symbol, shares, average cost, current value computed from quotes.

Type:
```typescript
export type Holding = {
  id: string; name: string; symbol: string; value: number;
  changePct: number; alloc: number; changeColor: string; spark: string; data: number[];
};
```

## 10.2 — `src/hooks/useYahooQuotes.ts`

Live prices. Reads `/api/yahoo/quote?symbols=NVDA,VOO,...`. Returns `{ quotes: Record<symbol, YahooQuote>, isLoading, error }`.

## 10.3 — `src/hooks/useYahooChart.ts`

Historical chart data. Reads `/api/yahoo/chart?symbol=VOO&range=3mo`. Used in `HoldingDetailView`.

## 10.4 — `api/yahoo/quote.ts`

Provider chain: Yahoo → Finnhub fallback (free Finnhub still works for quotes).

## 10.5 — `api/yahoo/chart.ts` (THE BIG ONE)

Provider chain: Yahoo `query1` → Yahoo `query2` (internal retry) → Twelve Data → Finnhub. Reference §12 of doc + AURORA_BUILD_SKILL.md §12.1 for full code (~150 lines).

⚠️ **Critical**:
- Yahoo blocks Vercel IPs intermittently — `query2` retry buys you another 30-50% chance
- Finnhub free tier no longer has `/stock/candle` — always returns 403 on free key
- Twelve Data is the reliable backup (free 800 calls/day at twelvedata.com)
- Cache aggressively: `Cache-Control: s-maxage=1800, stale-while-revalidate=7200`

If chart fails on all providers, return `502` with helpful message. Frontend shows a clean Hebrew "גרף לא זמין כרגע" — never the raw error JSON.

## 10.6 — `src/components/investments/HoldingDetailView.tsx`

Click on a holding → modal/page with chart + range tabs (1m / 3m / 6m / YTD / 1y / 5y) + min/max stats + benchmark toggle (compare to S&P 500).

## 10.7 — `src/pages/Investments.tsx`

Holdings list with sparklines. Pie chart of allocation. Click holding → detail view.

## 10.8 — Validation gate

Test the chart endpoint on every range. Verify it survives a Yahoo block (set `TWELVE_DATA_API_KEY` and watch logs to confirm fallback activates).

Commit:
```bash
git add . && git commit -m "feat(investments): provider chain Yahoo→TwelveData→Finnhub"
```

---

# 🍳 Phase 11 — Kitchen (8 tabs)

Skip this phase if user opted out of Kitchen in Phase 0.

This is the largest single feature. Build incrementally — get tabs 1+8 working first, then add 2-7.

## 11.1 — `src/hooks/useRecipes.ts`

Reads `VITE_NOTION_RECIPES_DB_ID`. Includes 3 sample recipes baked in (`SAMPLE_RECIPES`) so the UI is never blank.

Includes parsers for the rich-text fields:
- `parseIngredientsBlock(text)` → `RecipeIngredient[]` (handles "500 גרם קמח", "ביצים - 3", "2 כוסות סוכר")
- `parseStepsBlock(text)` → `RecipeStep[]` (extracts "(N דקות)" → `timerSec`)
- `parseFraction(s)` → number (handles "1/2", "0.5")

## 11.2 — `src/components/kitchen/RecipeDetail.tsx`

Recipe view: header with name + difficulty + time, ingredients list with servings scaler (drag a slider, all amounts recompute), step-by-step instructions with optional inline timer button (`▶ 5 דק'`).

## 11.3 — `src/pages/Kitchen.tsx` (skeleton with 8 tabs)

```typescript
type KitchenTab =
  | "recipes" | "mealplan" | "grocery" | "pantry" | "import"
  | "chef" | "timers" | "converter";
```

Header: title `המטבח` + tab navigation (.kitchen-tabs class). Active tab content rendered below.

## 11.4 — Tabs 7-8 (Timers + Unit Converter)

Easy. Implement first.

- **Timers**: `useKitchenTimers` hook with localStorage persistence. UI: list of running/paused/done timers, each with name + remaining + ▶/⏸/🗑.
- **Unit Converter**: static lookup tables. כפיות→מ"ל, אונקיות→גרם וכו'.

## 11.5 — Tab 6 (Chef AI Chat)

Streams to `/api/chat` (or `/api/claude` if going direct). System prompt biased toward concise, practical cooking answers. Conversation persisted to localStorage.

## 11.6 — Tab 1 (Recipes)

Built in 11.1-11.2 already. Add list view with search (by name / tag / category) and grid of recipe cards.

## 11.7 — Tabs 2-4 (MealPlan, Grocery, Pantry)

These three are connected via `src/lib/groceryList.ts` (pure aggregator).

### `src/hooks/useMealPlan.ts`
- Reads `VITE_NOTION_MEALPLAN_DB_ID`
- Filters by week
- Mutations: `addEntry`, `removeEntry`

### `src/hooks/usePantry.ts`
- Reads `VITE_NOTION_PANTRY_DB_ID`
- Mutations: `addItem`, `updateQty`, `removeItem`
- Helper: `pantryStatus(item)` → `"ok" | "low" | "empty"`

### `src/lib/groceryList.ts` + `.test.ts` (12 tests)
Pure function. Inputs: `{ mealPlan, recipes, pantry }`. Output: `GroceryItem[]` grouped by category.

Aggregation rule: same name + same unit = combine. Different units = stay separate.

Pantry match is fuzzy (substring), but only "in pantry" if `qty > 0`.

Categories (Hebrew dictionaries):
- ירקות ופירות
- בשר ודגים
- מוצרי חלב
- פחמימות
- תבלינים
- שימורים
- אחר

Copy verbatim from reference repo. Run `npx vitest run src/lib/groceryList.test.ts` — should be 12 passing.

### Components
- `MealPlannerTab.tsx` — 7×3 grid (days × meals), click cell → modal pick recipe
- `GroceryListTab.tsx` — auto-generated from `generateGroceryList()`, checkboxes, WhatsApp share button
- `PantryTab.tsx` — grid of items with +/-/🗑 buttons, status badges

## 11.8 — Tab 5 (Recipe Importer)

`src/components/kitchen/RecipeImporter.tsx`:
- URL input + "ייבא" button
- POST to `/api/parse-recipe-url` (which routes to `api/ai.ts?type=parse-recipe-url`)
- Shows parsed recipe preview with ingredients tags + steps
- "שמור ל-Notion" → calls `createNotionPage` to recipes DB

Server side already implemented in Phase 5. Critical detail: server fetches the URL, strips HTML noise (scripts/styles/SVG), truncates to 24KB, sends to Claude with strict-JSON system prompt that translates to Hebrew if needed.

## 11.9 — Validation gate

```bash
npx vitest run
```

Should show 19 (briefing) + 12 (grocery) = 31 tests passing.

Commit each tab as a separate commit if possible:
```bash
git add . && git commit -m "feat(kitchen): 8-tab kitchen with meal planning, grocery, pantry, AI import"
```

---

# 💪 Phase 12 — Health + Strava

Skip if Health was deselected in Phase 0.

## 12.1 — Hooks

Three Notion-backed hooks following the standard pattern:

- `useActivities` (`VITE_NOTION_ACTIVITY_DB_ID`) — manual activity log + mutations (add/update/remove)
- `useSleep` (`VITE_NOTION_SLEEP_DB_ID`) — sleep entries
- `useWeight` (`VITE_NOTION_WEIGHT_DB_ID`) — weight log + goal in localStorage

All include sample data fallbacks (~5-7 entries each).

## 12.2 — `src/lib/healthStats.ts` + `.test.ts` (13 tests)

Pure aggregator with 5 functions:
- `computeWeekStats(activities, refDate)` — current week aggregations
- `compareWeeks(activities, refDate)` — current vs previous + deltas
- `averageSleepLastWeek(entries, refDate)` — avg + delta + worst day
- `computeWeightTrend(entries, goal)` — current/oldest/change/direction
- `projectGoalEta(trend, daysSpan)` — weeks until goal at current rate

Copy verbatim. Tests cover boundary cases (empty data, exact week boundaries, flat tolerance).

## 12.3 — Strava OAuth (the killer integration)

### Setup steps to walk user through:
1. Open https://www.strava.com/settings/api
2. Create new app:
   - Name: `<project name>`
   - Category: `Visualizer`
   - Website: `https://<project>.vercel.app`
   - **Authorization Callback Domain**: just the domain WITHOUT `https://` and WITHOUT `/path`. E.g., `oslife.app`
3. Save → copy `Client ID` (number) and `Client Secret` (long string)
4. Set 3 env vars in Vercel:
   - `STRAVA_CLIENT_ID` = the number
   - `STRAVA_CLIENT_SECRET` = the long string
   - `STRAVA_REDIRECT_URI` = `https://<your-domain>/api/strava/callback` (full URL with https + path)
5. **Redeploy with build cache disabled** — env vars don't propagate to existing deployments

### `api/strava/[action].ts`

Single dynamic route handles 4 actions: `auth | callback | activities | disconnect`.

⚠️ **CRITICAL gotcha**: every `process.env.STRAVA_X` read must be wrapped in `envTrim()`:

```typescript
function envTrim(name: string): string | undefined {
  const v = process.env[name];
  return typeof v === "string" ? v.trim() : undefined;
}
```

Reason: Vercel's mobile env-var editor occasionally appends `\n` to pasted URLs. Without trim, the `redirect_uri` becomes `…callback%0A` and Strava rejects with "redirect_uri mismatch".

Reference: AURORA_BUILD_SKILL.md §11.6 for full implementation (~250 lines).

### `src/hooks/useStrava.ts`

```typescript
export function useStrava(perPage = 20): UseStravaResult {
  const query = useQuery({
    queryKey: ["strava", "activities", perPage],
    queryFn: async () => {
      const r = await fetch(`/api/strava/activities?per_page=${perPage}`);
      if (r.status === 401) return { connected: false, activities: [] };
      return r.json();
    },
    retry: false,
    staleTime: 5 * 60_000,
  });
  return {
    connected: query.data?.connected ?? false,
    activities: query.data?.activities ?? [],
    connectUrl: "/api/strava/auth",
    disconnect: async () => { await fetch("/api/strava/disconnect", { method: "POST" }); query.refetch(); },
    refetch: () => { query.refetch(); },
    isLoading: query.isLoading,
    error: query.error instanceof Error ? query.error.message : null,
  };
}
```

## 12.4 — `src/pages/Health.tsx`

4 tabs: Overview / Activity / Sleep / Weight. Layout matches reference.

Components:
- `ActivityList` — merges manual entries + Strava activities, with edit/delete buttons (Strava-sourced rows are read-only)
- `SleepChart` — clickable 7-day chart, click → edit modal
- `WeightTrend` — SVG sparkline + history list with inline edit/delete
- `HealthInsight` — calls `useHealthInsight` (POSTs to `/api/health-insight`)
- `StravaConnect` — Connect button or status row + disconnect

## 12.5 — Validation gate

Without env vars: 4 tabs render with sample data. Strava button shows "חבר חשבון Strava".
With Strava configured + connected: real activities appear merged with manual ones.

Tests should be 19 + 12 + 13 = 44 passing.

Commit:
```bash
git add . && git commit -m "feat(health): activity + sleep + weight + Strava OAuth"
```

---

# 🌐 Phase 13 — Vercel Deployment

## 13.1 — Pre-deploy validation

Before deploying, count serverless functions:

```bash
find api -name "*.ts" -type f | wc -l
```

**Must be ≤ 12.** If higher, you have a bug. Common causes:
- Forgot to consolidate Strava into `[action].ts`
- Forgot to consolidate AI into `ai.ts`
- Forgot to consolidate chat checks into `chat-diag.ts`

Expected list:
```
api/ai.ts
api/chat.ts                  (only if Chat selected)
api/chat-diag.ts             (only if Chat selected)
api/claude.ts                (alternative streaming path, optional)
api/extract-receipt.ts       (only if expense scanning selected)
api/fx.ts
api/notion.ts
api/notion/pages.ts
api/parse-expense-voice.ts   (optional)
api/strava/[action].ts       (only if Health selected)
api/yahoo/chart.ts           (only if Investments selected)
api/yahoo/quote.ts           (only if Investments selected)
```

## 13.2 — Push to GitHub

```bash
gh repo create <project-name> --private --source=. --remote=origin --push
```

Or manually:
```bash
git remote add origin git@github.com:<user>/<project-name>.git
git push -u origin main
```

## 13.3 — Connect to Vercel

1. Open https://vercel.com/new
2. Import the GitHub repo
3. Framework preset: **Vite** (auto-detected)
4. Root directory: `./`
5. Build command: `npm run build`
6. Output directory: `dist`
7. Click Deploy (without env vars first — first deploy will fail/run with sample data only, that's OK)

## 13.4 — Add env vars (CRITICAL ORDER)

Vercel → project → Settings → Environment Variables. Add in this order, **selecting all 3 environments (Production, Preview, Development) for each**:

### Tier 1 — required for any meaningful function
- `NOTION_API_TOKEN` — get from https://notion.so/my-integrations (create new internal integration)
- `ANTHROPIC_API_KEY` — get from https://console.anthropic.com/settings/keys

### Tier 2 — for individual features
- `TWELVE_DATA_API_KEY` — https://twelvedata.com/signup (only if Investments)
- `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`, `STRAVA_REDIRECT_URI` — only if Health (see Phase 12.3 for full setup)
- `OPENROUTER_API_KEY` — https://openrouter.ai/keys (only if Chat)
- `NOTION_MM_API_TOKEN` — only if Budget uses a separate integration
- `FINNHUB_API_KEY` — optional fallback (only if Investments)
- `NOTION_ALLOWED_DATABASES` — comma-separated allowlist (security best practice)

### Tier 3 — DB IDs (Phase 14 covers their creation)
All `VITE_NOTION_*_DB_ID` vars after creating the actual DBs in Notion.

## 13.5 — Redeploy after env var changes

⚠️ **Vercel does NOT auto-propagate env vars to existing deployments.** Every time you add or change an env var:

1. Vercel → Deployments tab
2. Latest deployment → ⋯ menu → Redeploy
3. **Uncheck "Use existing Build Cache"** in the modal
4. Click Redeploy
5. Wait for "Ready" status (~2 min)

## 13.6 — Custom domain (optional)

1. Vercel project → Settings → Domains
2. Add `<user-domain>.com`
3. Configure DNS at registrar:
   - A record pointing to `76.76.21.21` (Vercel)
   - Or CNAME to `cname.vercel-dns.com`
4. SSL auto-provisioned within 1-5 min

If using custom domain, **update**:
- `STRAVA_REDIRECT_URI` env var to use new domain
- Strava app's "Authorization Callback Domain" to the new bare domain

Then redeploy.

## 13.7 — Validation gate

Visit `https://<your-domain>` — should load. Open Network tab — `/api/notion` calls return JSON (or 500 with helpful message if DB IDs not yet set).

Test the diagnostic endpoint:
```
https://<domain>/api/chat-env-check
```

Should list `ANTHROPIC_API_KEY` in `otherDetectedNames` confirming it's loaded.

---

# 📊 Phase 14 — Notion DB Setup Walkthrough

Walk the user through creating each Notion DB they opted into. Do this AFTER deployment so the user can test each DB immediately.

## 14.1 — Process per DB

For each DB the user selected, instruct:

```
שלב 1 — צור את ה-DB:
  • פתח Notion → דף הדשבורד שלך
  • הקלד `/database` → בחר "Database — Inline" או "Full page"
  • שם: <DB name in Hebrew>

שלב 2 — הגדר עמודות:
  <table from §16 of AURORA_BUILD_SKILL.md>

שלב 3 — שתף עם האינטגרציה:
  • ⋯ → Add connections → בחר את האינטגרציה שיצרת ב-Phase 13.4
  • Confirm

שלב 4 — העתק את ה-Database ID:
  • ⋯ → Copy link
  • הקישור: https://notion.so/your-workspace/abc123def456...?v=xyz
  • Database ID = 32 התווים אחרי הקו האחרון, לפני ה-?

שלב 5 — הוסף ב-Vercel:
  • Settings → Environment Variables → Add New
  • Key: VITE_NOTION_<NAME>_DB_ID
  • Value: <ה-ID שהעתקת>
  • Environments: סמן את כל 3
  • Save

שלב 6 — Redeploy:
  • Deployments → ⋯ → Redeploy → uncheck Build Cache → Redeploy
```

## 14.2 — DB schemas (full reference)

| DB | Env var | Properties |
|---|---|---|
| Schedule | `VITE_NOTION_SCHEDULE_DB_ID` | Name (title), Date (date), Time (text), Location (text) |
| Goals | `VITE_NOTION_GOALS_DB_ID` | Name (title), Done (number), Target (number), Color (select) |
| Recipes | `VITE_NOTION_RECIPES_DB_ID` | שם (title), מנות (number), זמן (דקות) (number), רמת קושי (select), תיאור (text), קטגוריה (select), מצרכים (text), הוראות (text) |
| Meal Plan | `VITE_NOTION_MEALPLAN_DB_ID` | תאריך (date), ארוחה (select: בוקר/צהריים/ערב/נשנוש), מתכון (relation→Recipes), הערות (text) |
| Pantry | `VITE_NOTION_PANTRY_DB_ID` | שם (title), כמות (number), יחידה (text), קטגוריה (select), סף הזמנה (number), אימוג׳י (text) |
| Activity | `VITE_NOTION_ACTIVITY_DB_ID` | שם (title), תאריך (date), סוג (select: כדורסל/טניס/ריצה/כושר/אופניים/שחייה/אחר), משך (דקות) (number), קלוריות (number), הערות (text) |
| Sleep | `VITE_NOTION_SLEEP_DB_ID` | תאריך (date), שעות (number), איכות (select: מצוין/טוב/בינוני/גרוע) |
| Weight | `VITE_NOTION_WEIGHT_DB_ID` | תאריך (date), משקל (number) |
| Investments | `VITE_NOTION_INVESTMENTS_DB_ID` | שם (title), סמל (text), כמות יחידות (number), מחיר ממוצע (number), סוג (select) |
| Money Master Categories | `VITE_NOTION_BUDGET_DB_ID` | Name (title), Emoji (text), Group (select), Type (select), Fixed/Variable (select), Budget (number), Sort (number) |
| Money Master Expenses | `VITE_NOTION_EXPENSES_DB_ID` | Name (title), Amount (number), Date (date), Category (relation→Categories), PaymentMethod (select), Frequency (select), Notes (text) |
| Money Master Income | `VITE_NOTION_INCOME_DB_ID` | Name (title), Amount (number), Date (date), Category (relation), Source (select), Notes (text) |

## 14.3 — Validation

After each DB is set up + redeploy:
1. Visit the relevant page
2. Should show real data instead of sample
3. If still showing sample, check `https://<domain>/api/chat-env-check` to confirm the new env var is visible

---

# ✅ Phase 15 — Final Verification + Handoff

## 15.1 — Run full test suite

```bash
npx tsc --noEmit
npx vitest run
npx vite build
```

All three must pass:
- `tsc` returns exit 0 (no type errors)
- `vitest` shows 44 passed (or whatever the user opted into supports)
- `vite build` succeeds with bundle size warning at most

## 15.2 — Manual smoke test

Visit each page in order:
- `/` — Daily Briefing renders, lookahead clickable, AI insight loads
- `/schedule` — week view of events
- `/budget` — categories + transactions (if Budget selected)
- `/investments` — holdings + chart works (test 3mo range)
- `/net-worth` — summary loads
- `/kitchen` — all 8 tabs reachable
- `/health` — 4 tabs, Strava connect button works
- `/chat` — messages send + stream

## 15.3 — Mobile test

On iPhone Safari:
1. Open the URL
2. Share → Add to Home Screen
3. Open from home screen — should look like native app
4. Test PinGate if enabled

## 15.4 — Generate handoff documentation

Create `HANDOFF.md` in repo root summarizing:
- What was built
- What env vars are configured
- Which Notion DBs exist and their IDs (mask sensitive parts)
- Known issues / TODOs

Append a `## Session Handoff` section to `CLAUDE.md` with one-line current state. (See `compact.md` skill format.)

## 15.5 — Final commit + push

```bash
git add -A
git commit -m "chore: production-ready Aurora clone, deployed to <domain>"
git push origin main
```

## 15.6 — Output to user

Final message in Hebrew:

```
🎉 האתר מוכן ופעיל בכתובת https://<your-domain>

✅ מה נבנה:
- <list of selected features>

📋 Notion DBs מוגדרים:
- <list>

🔑 Env vars מוגדרים:
- <list (names only, never values)>

⏭ צעדים אופציונליים:
- הוסף עוד מתכונים ל-Notion (אם Kitchen)
- חבר Strava (אם Health) — ראה Phase 12.3
- הוסף יעדי שבוע (אם Goals)

📚 תיעוד:
- docs/AURORA_BUILD_SKILL.md — מדריך אדריכלות מלא
- HANDOFF.md — מצב נוכחי
- .env.example — כל ה-env vars

🐛 משהו לא עובד? בדוק:
- https://<domain>/api/chat-env-check — אילו env vars נראים לפונקציות
- Vercel Deployments → לחץ על הדפלוי → Build Logs
- האם עשית Redeploy אחרי שהוספת env var?
```

---

# 🛡️ Safety Rules

1. **Never commit secrets.** Always use `.env.local` (gitignored) for local dev. Vercel env vars for production.
2. **Never delete the user's Notion DBs.** Modifications are OK, deletion never.
3. **Never auto-merge to main.** All changes go through a PR; user merges manually.
4. **Always validate gate before next phase.** If a phase doesn't pass its gate, debug before proceeding.
5. **Function count check before every Vercel deploy.** Run `find api -name "*.ts" | wc -l` — must be ≤ 12.
6. **Always check for trailing whitespace in env vars** that come from Vercel mobile editor — `STRAVA_REDIRECT_URI` is the most common offender.
7. **Never inline an Anthropic API key in committed code.** Always read from `process.env`.
8. **Always include sample data fallback in every Notion-backed hook.** The UI must never break when an env var is missing.

---

# 🎯 Common Issues & Quick Fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| `Strava OAuth not configured` after setup | Env var missing or in wrong env scope | Check `https://<domain>/api/chat-env-check` for `STRAVA_*` in `otherDetectedNames` |
| `redirect_uri mismatch` from Strava | Trailing newline in `STRAVA_REDIRECT_URI` | `envTrim()` already handles it; redeploy if you just added the trim |
| Investment chart shows "גרף לא זמין" persistently | Yahoo blocking Vercel IPs + no Twelve Data key | Sign up for Twelve Data, add `TWELVE_DATA_API_KEY`, redeploy |
| Build fails: "Too many functions" | Forgot Vercel function consolidation | Check `find api -name "*.ts"` ≤ 12; consolidate into `[action].ts` or rewrites |
| AI insight always loading | Anthropic key wrong or quota exhausted | Test directly: `curl -X POST https://<domain>/api/daily-insight -d '{"context":{}}'` |
| Old version showing on iPhone after deploy | PWA service worker cache | Close Safari tab fully (swipe up from app switcher), reopen |
| Notion query returns empty | DB not shared with integration | In Notion: ⋯ → Add connections → select the integration |
| `tsc --noEmit` fails | Mixing types between hooks | Run `npx tsc --noEmit | head -30` and fix one error at a time |

---

# 📖 References

- **Reference repo (canonical source):** `bben15600-sys/aurora-dashboard`
- **Deep architecture doc:** `docs/AURORA_BUILD_SKILL.md` (1,674 lines)
- **Session history:** `docs/SESSION_MASTER_PLAN.md`
- **IDF Kitchen variant:** `docs/IDF_KITCHEN_PLAN.md`
- **Compact format example:** `.claude/commands/compact.md`

---

**End of Skill.**

When this skill completes successfully, the user has a fully-functional Hebrew RTL Life OS dashboard at their custom Vercel domain, with Notion + Anthropic + (optional) Strava + Twelve Data + Finnhub integrations, PWA-installable on iPhone, with 44+ unit tests, and complete documentation.

Estimated total build time:
- **Template Mode:** ~4-8 hours (mostly Notion DB setup + env var configuration + custom feature picks)
- **From-Scratch Mode (Appendix B):** 3-6 days of focused work

The skill produces production-ready output, not a prototype.

---

# 📦 Appendix B — From-Scratch Mode (Fallback)

Use this path **only** when the user cannot or will not start from `aurora-template` — e.g.:
- The template repo is unavailable / offline
- The user wants to learn the architecture by building it manually
- The user is forking the project into a different stack and needs the design as reference

**Heads-up:** From-scratch mode requires **read access to `bben15600-sys/aurora-dashboard`** because the skill instructs you to copy ~13,500 lines of code verbatim from there across Phases 2-12 (CSS, components, hooks, libs, API endpoints, tests). Without that reference, you can produce architecture and patterns but not working code.

## How to use Appendix B

1. **Skip Phase -1.** The user is intentionally not starting from template.
2. **Run Phase 0** (Discovery) as written.
3. **Run Phase 1 sections 1.1 → 1.6 in order** (the original Bootstrap path with `npm create vite@latest`, full dep install, shadcn init, paths config, .env.example, validation gate).
4. **Run Phases 2-15 as written**, treating every "Copy code from `bben15600-sys/aurora-dashboard/...`" instruction as a literal directive — fetch each file from the reference repo and write it into the new project at the indicated path.
5. **Ignore the "Template Mode shortcut" callout** at the top of Phase 2 — it doesn't apply.

## Why it's slower

- ~13,500 lines must be transferred file-by-file
- Every config (`package.json`, `vercel.json`, `tsconfig.json`, `tailwind.config.ts`, `vite.config.ts`) must be reconstructed
- Tests (44+) must be added incrementally
- shadcn components must be manually installed

The end result is functionally identical to Template Mode — but the labor is on the order of days, not hours.

## Recommendation

If From-Scratch Mode is unavoidable, consider **forking** `bben15600-sys/aurora-dashboard` instead of starting from a blank Vite project. A fork is identical to a template clone in terms of code coverage, just with extra branches/history that can be cleaned up afterwards (`git branch -D <branch>` for unwanted branches).
