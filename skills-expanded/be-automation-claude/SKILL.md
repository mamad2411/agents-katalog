# CLAUDE.md

Guidance for Claude Code (or any agent) working on this repo.

## What this is

**Helios** — an AI-native backend infrastructure generator. The user configures a stack visually; the backend emits a real, buildable repository as a zip. Claude Sonnet 4.6 powers an in-app copilot that audits the stack and explains trade-offs.

The UI is Next.js 15 (App Router) + React 19 + Tailwind + Framer Motion + Zustand + Radix primitives. The generation backend is Node-runtime Next.js API routes using `archiver` for streaming zip output and `@anthropic-ai/sdk` for SSE chat.

## Quick commands

```bash
npm run dev     # local dev server on :3000
npm run build   # production build
npm run start   # start production server
npm run lint    # Next.js ESLint
```

No tests yet. No prisma / no DB — state is Zustand only, per-tab.

## Architecture in one screen

```
Browser                          Next.js server
──────────                       ──────────────
Zustand store  ──┐
(src/lib/store)  │
                 │  POST /api/generate        → Zod validate → generate() → archiver zip stream
                 │    body: {config, endpoints}
                 │    resp: application/zip
                 │
                 └─▶ POST /api/ai/chat        → Anthropic SDK messages.stream() → SSE
                      body: {messages, config?}
                      resp: text/event-stream
```

The client is the source of truth for `StackConfig` and `Endpoint[]`. The server is stateless — it takes the current state and emits artifacts.

## Directory map

- `src/app/` — Next.js App Router. Each page is a route.
  - `page.tsx` — Landing (marketing). Now leads with an **intent input** that routes to `/start`.
  - `start/` — Intent-driven architect flow. Single text field → Claude proposes a complete `StackConfig` via forced tool use.
  - `dashboard/` — Workspace overview.
  - `builder/` — **Core surface.** 10 tabs (Runtime, Database, Cache, Queue, APIs, Security, Deployment, Scaling, CI/CD, Monitoring) + architecture preview + AI assistant + summary.
  - `api-builder/` — REST/gRPC endpoint editor.
  - `autopilot/` — Connect a GitHub repo, audit it, open a PR with fixes.
  - `preview/` — Generated repository browser with Download zip CTA.
  - `deploy/` — Provider grid + credentials + simulated deploy flow.
  - `show/[slug]/` — **Public**, server-rendered read-only architecture page with OG image + Fork CTA.
  - `api/architect/route.ts` — intent → streaming SSE → `ArchitectureProposal`.
  - `api/share/route.ts` — publish a proposal; returns `{slug, url}`.
  - `api/generate/route.ts` — zip stream endpoint.
  - `api/ai/chat/route.ts` — Anthropic SSE endpoint.
  - `api/autopilot/analyze/route.ts` — static audit of a GitHub repo via Octokit.
  - `api/autopilot/propose/route.ts` — Claude drafts the PR file contents.
  - `api/autopilot/open-pr/route.ts` — commits + opens PR via GitHub Git Data API.
- `src/components/`
  - `ui/` — shadcn-style primitives (Button, Card, Tabs, Switch, Slider, Badge, Input, Tooltip, ScrollArea, SelectableCard, Dropdown, Toast, Separator, Kbd).
  - `layout/` — Sidebar, Topbar, WorkspaceShell.
  - `landing/` — hero + features + demo + logo wall + CTA.
  - `builder/` — ArchitecturePreview, StackSummary.
  - `shared/` — Logo, Terminal, AIAssistant, DownloadRepoButton, BrandIcon.
- `src/lib/`
  - `store.ts` — Zustand: `config`, `endpoints`, `workspace[s]`. Mutators: `set`, `patch`, `addEndpoint`, `removeEndpoint`, `updateEndpoint`, `addEnvVar`, `removeEnvVar`, `setWorkspace`, **`applyProposal(config)`**.
  - `schema.ts` — Zod schemas for API request validation. Mirrors store types.
  - `architect-schema.ts` — Zod for `/api/architect`'s `ArchitectureProposal` (summary + decisions[] + config + predictions).
  - `share-store.ts` — in-memory Map for published proposals, keyed by slug. MAX 1000. Swap for KV later.
  - `proposal-from-config.ts` — synthesize a minimal valid `ArchitectureProposal` from a manual `StackConfig` (used by /builder + /preview publish flows).
  - `sse.ts` — `readSSE(response)` async generator for client-side consumption of `text/event-stream` responses.
  - `utils.ts` — `cn()`, `formatBytes()`, `shortId()`.
  - `autopilot/` — GitHub repo analyzer, Claude-driven PR proposer, committer.
    - `schema.ts` — Zod for audit, findings, PR proposal.
    - `analyzer.ts` — `auditRepo(token, ref)`: fetches key manifests via Octokit, infers stack, returns findings + score.
    - `proposer.ts` — Claude tool-use call that generates full file contents for selected findings.
    - `committer.ts` — creates blob → tree → commit → ref → PR via Git Data API (one commit for many files).
  - `generators/` — Templated file emitters.
    - `index.ts` — `generate(config, endpoints) → GeneratedFile[]`.
    - `common.ts` — README, env, Dockerfile, docker-compose, K8s, Helm, CI, OpenAPI.
    - `go.ts` / `typescript.ts` / `python.ts` / `others.ts` (Rust/Java/Kotlin).
- `src/data/stack-options.ts` — Catalog of languages, frameworks, DBs, caches, queues, auth, deployments, monitoring, CI. Brand ids in this file must match keys in `BrandIcon`'s registry.

## State model

`StackConfig` is the single source of truth. Anything user-configurable in the builder lives here. The architecture preview, stack summary, and recommendations card are all *derived* from it.

```ts
type StackConfig = {
  name: string
  language: "go" | "typescript" | "python" | "rust" | "java" | "kotlin"
  framework: string           // id scoped to language
  database: string            // "postgres", "mongodb", "neon", …
  cache: string               // "redis", "memcached", …
  queue: string               // "rabbitmq", "kafka", "nats", …
  api: "rest" | "grpc" | "graphql" | "trpc"
  auth: string                // "clerk", "auth0", …
  deployment: string          // "vercel", "aws", "k8s", …
  scaling: string
  monitoring: string
  cicd: string
  docker: boolean
  kubernetes: boolean
  helm: boolean
  tracing: boolean
  rateLimit: boolean
  audit: boolean
  autoscale: boolean
  replicas: number
  region: string
  envVars: { key: string; value: string; secret?: boolean }[]
}
```

`Endpoint` represents a single REST/gRPC route (`id`, `method`, `path`, `summary`, `auth`, optional `requestSchema` / `responseSchema`).

## Generators

`generate()` composes a repo from `commonFiles()` + a language-specific file set. Adding a new language:

1. Add to the `StackConfig["language"]` enum in `src/lib/schema.ts` and `src/lib/store.ts`.
2. Add options in `src/data/stack-options.ts` (language entry + matching frameworks, and the language's meta in `common.ts` if commands differ).
3. Create `src/lib/generators/<lang>.ts` exporting `<lang>Files(config, endpoints): GeneratedFile[]` — must include a Dockerfile, a main entry file, and a CI-friendly layout.
4. Wire it into `src/lib/generators/index.ts`.
5. Optionally add a brand in `src/components/shared/brand-icon.tsx`.

Generators must output **plain text** files — no binary. Use `dedent` / template strings, keep paths POSIX (forward slashes), and keep filenames deterministic; `generate()` sorts by path for stable zip contents.

## AI chat

`src/app/api/ai/chat/route.ts`:
- Model: `claude-sonnet-4-6`.
- System prompt is split into two blocks — static persona + the current `StackConfig` as a cached ephemeral block (`cache_control: { type: "ephemeral" }`). Repeated turns hit the prompt cache.
- Streams via `client.messages.stream(...).on("text", …)`. Forwarded to the client as SSE (`event: text` / `event: done` / `event: error`).
- Returns **503** with `{ error: "missing_api_key" }` when `ANTHROPIC_API_KEY` is not set. `AIAssistant` renders a friendly banner for that case — do not crash the UI when the key is missing.
- The client strips any leading `assistant` turn before POSTing — Anthropic requires the message array to start with `user`.

## Design system

- **Dark-first.** Tokens in `src/app/globals.css` under `:root`. Don't ship light-mode styles unless asked.
- **Glassmorphism** via `.glass` / `.glass-strong` classes. Avoid over-blurring — 12–18px is the sweet spot.
- **Aurora + dot backgrounds** via `.aurora`, `.dot-bg`, `.grid-bg`, `.mask-radial`. Prefer composing these over one-off CSS.
- **Typography:** Inter for UI, JetBrains Mono for code. Loaded from Google Fonts in `src/app/layout.tsx`.
- **Brand tiles:** Always render stack choices with `<BrandIcon id={...} size={22} />`. Each registry entry has a real accent color, real SVG path, or branded monogram — do not add plain lucide icons for known brand ids.
- **Rounded corners:** `rounded-lg` for buttons / pills, `rounded-xl` for cards, `rounded-2xl` for hero sections.
- **Animations:** Use Framer Motion's `initial/animate/transition` with subtle y-translate + opacity. Keep durations ≤ 0.5s; avoid spring for UI chrome.

## Conventions

- **Client vs server components:** default to server; add `"use client"` only when you need state, effects, or Framer Motion. Pages that read `useStackStore` must be client.
- **No external API calls from client components** except to `/api/*` routes.
- **Handlers > hrefs for placeholder destinations.** Show a toast with meaningful context instead of linking to `#`. Every clickable element in the product has a handler — keep that invariant.
- **Toasts** via `toast({ title, description?, kind: "success" | "info" | "error" })` from `src/components/ui/toast.tsx`. The `Toaster` is already mounted globally.
- **Dropdowns** use the in-house primitive in `src/components/ui/dropdown.tsx` — don't reach for Radix DropdownMenu unless you need focus trapping / nesting.
- **Imports use `@/…` alias** (configured in `tsconfig.json`).
- **No barrel files** in `src/components/ui/` — import each primitive directly.
- **Icons:** lucide-react for UI glyphs, `BrandIcon` for stack choices. Don't mix them for the same concept on the same page.

## Things to watch out for

- `package-lock.json` is checked in — keep it in sync when adding deps.
- The generators return raw source files with hardcoded module paths like `github.com/your-org/<name>`. If you add a language, prefer the same convention so the README stays accurate.
- `ANTHROPIC_API_KEY` is optional at build time but required at runtime for `/api/ai/chat`. Do not crash the app if it's missing — `route.ts` must return a structured 503.
- `archiver` requires Node runtime — the `/api/generate` route sets `export const runtime = "nodejs"`. Do not change to edge.
- `SelectableCard`'s outer tile has its own `h-9 w-9` container. Pass `BrandIcon size={22}` so it fits without a double-tile look.
- The workspace dropdown (`Dropdown` primitive) needs `className="block w-full"` on its root to span the sidebar width.
- When adding a new stack option to `src/data/stack-options.ts`, either add a matching entry to `src/components/shared/brand-icon.tsx` or accept the monogram fallback — do not introduce generic lucide icons in the selectable cards.

## Things not to do

- Don't run `git config --global …` — keep identity changes scoped to the repo (`git config user.email "…"`).
- Don't commit `.env*.local` or `.claude/` (both are gitignored).
- Don't add a CSS framework beyond Tailwind. Don't add another state library. Don't add a component library on top of the current primitives.
- Don't replace the Zustand store with Redux/Jotai/Context. Don't add persistence unless asked.
- Don't lift the AI copilot into global state — it's a panel, rendered per-page via `WorkspaceShell.right`.

## Glossary of ids (must stay consistent)

- Languages: `go`, `typescript`, `python`, `rust`, `java`, `kotlin`.
- Go frameworks: `gin`, `fiber`, `echo`, `chi`.
- TS frameworks: `nestjs`, `express`, `fastify`, `hono`.
- Python frameworks: `fastapi`, `django`, `litestar`.
- Rust: `axum`, `actix`.
- Java: `spring`, `quarkus`.
- Kotlin: `ktor`, `spring-kt`.
- Deployments: `vercel`, `railway`, `render`, `fly`, `aws`, `gcp`, `azure`, `k8s`.
- APIs: `rest`, `grpc`, `graphql`, `trpc`.

New ids must be added to **three** places: `stack-options.ts`, the matching generator, and (ideally) `BrandIcon`'s registry.
