# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Sentinel** is a visual AI investigation board that exposes online scams and finds legitimate deals.
The UI is a detective's cork-board (React Flow canvas) where evidence cards fly in with animations and connect with red strings. The backend is the primary development focus.

Two modes:
- **Investigate** — drop any URL; agents run WHOIS, SSL, Safe Browsing, scraping, Reddit, ScamAdviser, brand-impersonation, and seller checks, then stream evidence cards and a 0–100 threat score.
- **Shop** — enter a product query (or image); agents search Google Shopping, run 4 fraud checks per listing, and stream results + a best-pick verdict.

## Commands

```bash
npm run dev            # Start dev server → localhost:3000
npm run build          # Production build
npm run lint           # ESLint

# Library-level test (no server required)
npm run test:pipeline  # End-to-end: search → fraud validate → seller check
npm run test:pipeline "Nike Air Max" 5  # custom query, check top 5

# HTTP-level test (requires npm run dev to be running)
npm run test:api refine      "I want a jacket"
npm run test:api shop        "Sony WH-1000XM5 headphones"
npm run test:api investigate "https://example.com/product"
npm run test:api compare     "https://example.com/product"

# Single seller check
npx tsx scripts/test-seller-check.ts "https://www.amazon.com/dp/..."
```

## Tech Stack

- **Framework:** Next.js 16 (App Router), React 19, TypeScript strict mode
- **Styling:** Tailwind CSS 4, class-variance-authority, tailwind-merge, clsx
- **UI Components:** Radix UI (Dialog, Tooltip, Slot)
- **Visualization:** React Flow — investigation board with custom nodes
- **Animation:** Framer Motion — card fly-in, threat meter pulse
- **State:** Zustand (`src/lib/investigationStore.ts`)
- **Validation:** Zod
- **AI:** OpenAI SDK (chat completions + Responses API), Perplexity (fallback search)
- **Scraping:** Bright Data SERP API, Bright Data Web Unlocker, Browserbase/Stagehand
- **React Compiler** enabled in `next.config.ts`

Path alias `@/*` → `./src/*`.

## Backend File Map

### API Routes (`src/app/api/`)

| Route | Method | Body | Response | Purpose |
|---|---|---|---|---|
| `/api/investigate` | POST | `{ url }` | SSE stream | Full URL investigation |
| `/api/deepen` | POST | `{ investigationId, focus }` | SSE stream | Drill deeper on a specific angle |
| `/api/compare` | POST | `{ url }` | SSE stream | Agentic price comparison |
| `/api/shop` | POST | `{ text?, imageBase64?, imageMediaType?, searchQueries? }` | SSE stream | Product search + fraud checks |
| `/api/shop/refine` | POST | `{ query, history?, forceSearch? }` | JSON | Guided Discovery query refiner |
| `/api/search` | POST | varies | SSE stream | Generic search endpoint |
| `/api/investigate-demo` | POST | `{ url }` | SSE stream | Demo/mock investigation |

### Core Libraries (`src/lib/`)

| File | Purpose |
|---|---|
| `agent.ts` | OpenAI Responses API orchestration loop — runs tools, streams `card`/`narration`/`threat_score` events |
| `shopping-agent.ts` | Shopping pipeline — vision query → product search → parallel fraud validation → best pick |
| `query-refiner.ts` | Guided Discovery engine — gpt-4o-mini decides if query is specific enough, or asks highest-info-gain clarifying question |
| `scoring.ts` | Threat score calculation (incremental + final) |
| `stream.ts` | `createSSEResponse()` — ReadableStream + `send(event, data)` / `close()` helpers |
| `investigationStore.ts` | In-memory investigation state (cards, connections, threat score) |
| `known-domains.ts` | Allowlist of trusted retailer domains |

### Tools (`src/lib/tools/`)

| File | Tool name | What it does |
|---|---|---|
| `whois.ts` | `whois_lookup` | Domain registration date, registrar, country |
| `ssl.ts` | `ssl_analysis` | Certificate issuer, validity, expiry |
| `safe-browsing.ts` | `safe_browsing_check` | Google Safe Browsing API |
| `scraper.ts` | `scrape_red_flags` | Scrapes page for scam patterns (urgency timers, missing policy, etc.) |
| `reddit.ts` | `reddit_search` | Reddit posts about the domain |
| `scamadviser.ts` | `scamadviser_check` | ScamAdviser trust score API |
| `brand-impersonation.ts` | `brand_impersonation_check` | LLM detects typosquatting / lookalike domains |
| `seller-check.ts` | `seller_check` | Two-step: fetch product page → extract seller profile URL → fetch seller page → LLM extracts name/rating/reviews/age |
| `serpSearch.ts` | — | Bright Data SERP → Google Shopping results as `ProductResult[]` |
| `validate-product.ts` | — | 4 fraud checks: price anomaly, semantic domain, community sentiment, safety DB |
| `priceSearch.ts` | `price_search` | Perplexity finds same product on other retailers |
| `brightdata.ts` | — | Bright Data structured scraper for price comparison |
| `browserbase.ts` | — | Browserbase/Stagehand AI browser fallback scraper |
| `fraudCheck.ts` | — | Additional fraud check helpers |
| `webSearch.ts` | — | Generic web search helper |
| `queryUnderstand.ts` | — | Query understanding utilities |
| `error-classify.ts` | — | Error classification helpers |
| `index.ts` | — | Tool registry: OpenAI function definitions + `executeTool()` dispatcher |

### Types (`src/types/index.ts`)

Key shared types:
- `EvidenceCard` — the universal unit streamed to the frontend (id, type, severity, title, detail, source, confidence, connections, metadata)
- `CardSeverity` — `"critical" | "warning" | "info" | "safe"`
- `ProductResult` — raw product from Google Shopping
- `FraudCheck` — individual check result (name, status, detail, severity 0–1)
- `ProductVerdict` — `"trusted" | "caution" | "danger"`
- `RefineResult` — `{ type: "question", ... } | { type: "ready", ... }`
- `ConversationMessage`, `RefinementOption` — Guided Discovery types
- `SSEEvent`, `SearchSSEEvent` — typed SSE event unions

## SSE Streaming Format

**Important:** Sentinel uses a non-standard SSE format. The event name is embedded *inside* the JSON data, not as a separate `event:` field:

```
data: {"event":"narration","data":{"text":"Searching..."}}
data: {"event":"product","data":{...ProductResult...}}
data: {"event":"done","data":{"summary":"..."}}
```

Frontend and `scripts/test-api.ts` both parse `parsed.event` / `parsed.data` from the JSON.

### SSE events by endpoint

**`/api/investigate` and `/api/deepen`:** `card | connection | threat_score | narration | done | error`

**`/api/shop`:** `narration | all_products | product | fraud_check | verdict | best_pick | done | error`

**`/api/compare`:** `narration | card | connection | done | error`

## Key Patterns & Conventions

### Lazy OpenAI initialization
Always use this pattern — never call `new OpenAI()` at module load time:
```typescript
let _openai: OpenAI | null = null;
const getOpenAI = () => (_openai ??= new OpenAI());
```

### Two-step seller page fetch
`seller-check.ts` fetches raw HTML (not stripped text) first so it can extract the seller profile URL via regex, then fetches the profile page separately. Both texts are combined with section labels before the LLM call.

### Seller URL regex
Must match both relative and absolute hrefs. Use `resolve()` helper to normalize:
```typescript
const amazonSpMatch = rawHtml.match(/href="([^"]*\/sp\?[^"]*seller=[A-Z0-9]+[^"]*)"/i);
const resolve = (href: string) => {
  const decoded = href.replace(/&amp;/g, "&");
  return decoded.startsWith("http") ? decoded : `${origin}${decoded}`;
};
```

### Fatal Flags in fraud scoring
`validate-product.ts` has a `FATAL_FLAGS` array checked before normal additive scoring. Matches (e.g. known malware site, implausible domain) short-circuit the score to 0 or 5.

### Guided Discovery flow
1. Frontend: `POST /api/shop/refine { query, history }` → `{ type: "question", ... }` — loop
2. Frontend: user picks option → append to history, repeat
3. Frontend: `POST /api/shop/refine { query, history }` → `{ type: "ready", refinedQuery, searchQueries }`
4. Frontend: `POST /api/shop { searchQueries }` → SSE stream

## Environment Variables

| Variable | Used by | Required for |
|---|---|---|
| `OPENAI_API_KEY` | All LLM calls | Semantic domain check, seller LLM, query refiner, vision |
| `BRIGHT_DATA_API_KEY` | `serpSearch.ts`, `seller-check.ts`, `brightdata.ts` | Product search (primary), seller page fetching |
| `BRIGHT_DATA_SERP_ZONE` | `serpSearch.ts` | Bright Data SERP zone name |
| `BRIGHT_DATA_UNLOCKER_ZONE` | `seller-check.ts` | Web Unlocker zone for seller pages (different from SERP zone) |
| `PERPLEXITY_API_KEY` | `serpSearch.ts`, `priceSearch.ts` | Product search fallback, retailer link discovery |
| `GOOGLE_SAFE_BROWSING_KEY` | `safe-browsing.ts` | Safety database check |
| `SCAMADVISER_API_KEY` | `scamadviser.ts` | ScamAdviser trust score |
| `BROWSERBASE_API_KEY` | `browserbase.ts` | AI browser fallback scraper |
| `BROWSERBASE_PROJECT_ID` | `browserbase.ts` | Browserbase project |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/test-pipeline.ts` | Library-level E2E: search → validate → seller check. No server needed. |
| `scripts/test-api.ts` | HTTP-level: hits live Next.js routes. Server must be running. |
| `scripts/test-seller-check.ts` | Quick seller check on a single URL. |
