---
name: data-layer
description: Wire external and business data into an Astro 7 site on Cloudflare Workers Static Assets with a build-time-first data layer — content-collection loaders reading a seed JSON or Supabase at build time, one zod schema as the data contract, and rebuild-on-change via a Supabase webhook hitting a Cloudflare Deploy Hook. Use when adding a catalog, menu, product list, pricing table, schedule, or any external dataset to a site, when choosing between build-time data and client-side fetching, when wiring Supabase reads into Astro content collections, when typing external data with zod, or when setting up rebuilds when data changes. Trigger on load data from Supabase, add a catalog or menu from a database, content collection loader for external data, rebuild the site when data changes, or client-side data fetching in Astro. Not for editorial content a client edits (use cms-self-edit), lead capture and form writes (stack-integration-playbook forms recipe), or multi-skill composition (stack-integration-playbook).
---

# data-layer

> External data on this stack is BUILD-TIME by default: a content-collection loader reads a seed file or Supabase when the site builds, one zod schema is the contract for both sources, and freshness comes from a rebuild trigger — not from shipping a database client to the browser. Every escalation up the tier ladder has a byte, CSP, or deploy-shape cost that must be earned by the brief.

## Reference materials — load when relevant

This SKILL.md is the verdict, the tier ladder, and the rebuild cycle. Load references only when their content is needed:

- `references/build-time-loader.md` — load when implementing the loader: the `file()` tier-zero recipe, the custom Supabase build-time loader with digest/meta incremental updates, and the zod typing pattern.
- `references/rebuild-wiring.md` — load when wiring freshness: Supabase Database Webhook (pg_net) → Workers Builds Deploy Hook, Vault for the hook URL, and the repository_dispatch variant.
- `references/client-side-escalation.md` — load ONLY when a brief genuinely needs per-visitor or real-time reads: the measured costs, the publishable-key + RLS pattern, and the live-collections boundary.
- `references/brand-contract-seam.md` — load when the site consumes a governed brand repo: the data-pointer rule (data-map → seed catalog.json → Supabase, same schema) and the graduation path.

## Verdict

Default is a custom content-collection loader that reads the data source at build time, validated by ONE zod schema that serves every tier. The site stays fully prerendered (the Worker remains assets-only), pages ship zero data-fetching JavaScript, CSP stays at connect-src 'self', and the CI byte budget never sees a database client. Freshness is a rebuild: a Supabase Database Webhook POSTs a Workers Builds Deploy Hook and the site redeploys with fresh data, usually within a couple of minutes. Escalate beyond build-time only when the brief needs per-visitor or genuinely real-time data — and account for the escalation's costs explicitly.

## The tier ladder

Each step up must be earned; each row names its cost.

| Tier | Pattern | Cost | Take the step when |
|---|---|---|---|
| 0 | `file()` loader over a seed JSON in the repo (e.g. `data/catalog.json`) | None — no external source, no secrets | The dataset is small, changes rarely, and edits-by-commit are acceptable; also the day-one state of a brand-contract data pointer |
| 1 | Custom loader reading Supabase AT BUILD TIME (the default once a live data home exists) | A Supabase project + the rebuild wiring; zero bytes shipped, zero CSP change | Data changes independently of deploys, or a non-developer edits it in Supabase |
| 2 | Client-side supabase-js reads from the browser | ~53 KB gzip measured for the client (budget line), CSP connect-src widened to the project origin, publishable key exposed by design (RLS is the boundary) | The brief needs per-visitor or high-frequency data (availability, live pricing) that a rebuild cannot honestly serve |
| 3 | Live content collections (request-time loaders) | Pages flip to on-demand — the Worker gains a main entry and the deploy shape changes; per-request latency and runtime cost | Per-request freshness IS the product; this is an architecture decision, not a data tweak — involve the composition playbook |

Never mix tiers casually: a site sits at the lowest tier its brief allows, and a jump is a documented decision.

## The rebuild cycle (tier 1 freshness)

Supabase Database Webhook (pg_net, fires async on INSERT/UPDATE/DELETE) → POST to a Cloudflare Workers Builds Deploy Hook (a unique per-branch URL; an unauthenticated POST triggers build+deploy, so the URL itself is the credential — store it in Supabase Vault and read it at call time, never inline in the trigger SQL). Deploy Hooks deduplicate queued builds and rate-limit at 10 builds/min per Worker, which absorbs pg_net's per-row firing on bulk edits.

Documented variant — GitHub Actions `repository_dispatch` instead of the direct hook: choose it when a rebuild must pass CI gates before deploying, or when you want a committed data snapshot for audit. It costs an extra hop and a PAT; the direct hook is the native default.

## Typing — one zod schema as the contract

One hand-written zod schema, imported from `astro/zod` (Astro 7 bundles zod 4 — no separate dependency), is the single contract artifact: it validates the seed file in the `file()` parser AND the Supabase rows in the custom loader via `parseData`, so schema drift FAILS THE BUILD instead of shipping wrong pages. Supabase generated TypeScript types are a cross-check, never the source — generated types do not validate runtime data. This is the same schema the brand contract's data-map names when the site consumes a governed brand repo (see the seam reference).

## Keys and client gotchas

- Use the new Supabase key model from day one: `sb_publishable_...` in anything that ships or could leak, `sb_secret_...` only server-side. Legacy `anon`/`service_role` JWT keys are deprecated with support ending at the end of 2026 — never teach or wire the legacy pattern.
- The new keys travel on the `apikey` header; never put them in an Authorization Bearer header.
- Unauthenticated Realtime connections cap at 24 hours — relevant only at tier 2+.
- Tombstone: `@astrojs/db` is deprecated on npm and was REMOVED in Astro 7. It solved this problem with a second database and libSQL lock-in; do not reach for it, and treat any tutorial built on it as expired.

## Pins (verified 2026-08-17) and review-gates

| Pin | Value | Review-gate |
|---|---|---|
| `@supabase/supabase-js` | 2.112.3 | Re-verify on major v3; re-measure the ~53 KB gzip client cost then |
| zod | none — use Astro's bundled `astro/zod` (zod 4) | If Astro ever unbundles zod, pin standalone zod 4.x and update imports |
| Workers Builds Deploy Hooks | platform feature (GA 2026-04) | Platform surface, not a package — re-verify the endpoint shape on Cloudflare changelog before reusing in a new project |
| Supabase key model | `sb_publishable_` / `sb_secret_` | Hard date: legacy keys sunset end of 2026 — any doc still showing `anon` keys is stale |

## Limitations and out-of-scope

- This skill does NOT cover form submissions, lead capture, or any WRITE path from the site — that is the forms recipe in stack-integration-playbook.
- It does NOT cover editorial content (pages, posts) that a client edits — that is cms-self-edit; the boundary is data that lives in rows versus content that lives in documents.
- Tier 3 (live collections) is documented here only as a boundary; implementing an on-demand architecture is a composition decision made with stack-integration-playbook.
- Supabase is this stack's canonical data home; the loader pattern is source-agnostic but the wiring recipes assume Supabase.
