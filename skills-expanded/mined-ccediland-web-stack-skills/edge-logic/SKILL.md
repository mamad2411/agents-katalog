---
name: edge-logic
description: Add edge logic to an Astro 7 site on Cloudflare Workers Static Assets — A/B testing, redirects, geo-personalization, and feature flags — defaulting to LESS at the edge. Use when running an A/B test, adding redirect rules, geo-targeting content by country, adding feature flags or a kill switch, or deciding whether logic belongs in a Worker, zone rules, or the client. Explains why Astro middleware cannot intercept prerendered pages, why run_worker_first bills every matched pageview against the shared free cap with a 429 mode, the Workers Caching billing trap, and Flagship's unpriced beta status. Covers the _redirects file, Redirect Rules, Bulk Redirects, request.cf geo fields, and the custom Worker entry wrapping the adapter handler. Trigger on A/B test, redirect rules, feature flags, geo targeting, edge personalization, or run_worker_first. Not for security headers or middleware-for-headers (web-security-headers), perf budgets (perf-ci-gates), or composing a build (stack-integration-playbook).
---

# Edge Logic — A/B, geo, flags, redirects on Workers Static Assets

> A THIN skill on purpose. On a fully prerendered site on the Free plan, the technically-best edge logic is repeatedly the least edge logic: client-side A/B assignment, build-time flags, `_redirects` in git, client-side geo. The Worker earns its invocations only when the initial HTML itself must differ per visitor. What this skill really carries is four traps that make the obvious approaches silently wrong, plus the decision tables that keep each job on its cheapest honest surface.

## Contents

- The routing and billing model
- The four traps
- Fork e1 — A/B testing
- Fork e2 — Where edge logic lives
- Fork e3 — Geo personalization
- Fork e4 — Feature flags
- Fork e5 — Redirect surface
- Snippet 1 — Client-side A/B assignment
- Snippet 2 — Geo endpoint
- Snippet 3 — Custom Worker entry
- Platform pins and review-gates
- Limitations

## The routing and billing model

Ten lines that decide everything else on this stack (Workers Free, fully prerendered, Worker = assets + `main` for `/_actions/*`):

1. A request that matches a static asset is served from the asset layer — free, unlimited, cached at the nearest Cloudflare location. The Worker never runs.
2. Only when NO asset matches does the Worker `main` run — that is how `/_actions/*` works, and each such request is a billed invocation.
3. `run_worker_first` (wrangler config) inverts rule 1 per pattern — boolean, glob array, `!` exceptions (`"run_worker_first": ["/experiment/*", "!/_astro/*"]`). Matching requests ALWAYS invoke the Worker, billed, even when an asset exists.
4. All billed invocations share ONE Free-plan budget — 100,000 requests/day — with everything else the Worker does, including the forms endpoint. Over the cap, `run_worker_first` requests get a 429.
5. CPU per invocation is 10 ms on Free — a cookie check plus `env.ASSETS.fetch()` rewrite fits easily; that is never the constraint. The request COUNT is.
6. The Worker can serve any variant by rewriting the pathname and fetching it from the assets binding — assignment happens per-request in the Worker, so nothing visitor-specific ever lands in a shared cache.
7. Zone-level surfaces (Redirect Rules, Bulk Redirects, Transform Rules) run BEFORE the Worker and cost zero invocations.
8. `_redirects` runs in the asset layer — zero invocations, lives in git, deploys with the site.
9. Astro middleware is NOT in this picture for prerendered pages (trap 1).
10. Asset requests being free has one carve-out already — the Workers Caching product (trap 3).

## The four traps

### Trap 1 — Astro middleware cannot intercept prerendered pages

Middleware looks like the natural interception point and silently is not, for three INDEPENDENT reasons, each sufficient alone:

- Middleware runs at BUILD time for prerendered pages — its output is baked into the HTML; at runtime there is nothing to run.
- The asset layer answers first — without `run_worker_first`, a prerendered page matches an asset and the Worker (where the Astro server entry and its middleware live) is never invoked.
- Even worker-first, the adapter handler short-circuits — `app.match(request)` misses (prerendered routes are not in the server manifest) and the handler falls back to the ASSETS binding without entering the render pipeline where middleware executes.

Middleware is live only for on-demand routes. "Add Astro middleware" as the answer to edge logic on a prerendered site is the misconception this skill exists to prevent. (Middleware for security HEADERS on on-demand routes is web-security-headers' territory, not this skill's.)

### Trap 2 — run_worker_first couples pageviews to the shared invocation cap

Turning on worker-first for HTML routes puts every pageview — humans, bots, crawlers — on the same 100k/day budget as the forms endpoint, and the failure mode is a 429 on the pages themselves. A marketing site doing under ~30–50k HTML requests/day sits comfortably; a crawl spike or a traffic hit eats the budget for everything at once. Scope the globs to exactly the routes that need interception, always exclude subresources (`!/_astro/*` and friends), and treat "the whole site worker-first" as a Paid-plan decision ($5/mo, 10M included requests, no 429 mode).

### Trap 3 — Workers Caching bills the free asset requests

Enabling the Workers Caching product (2026) charges EVERY request to the Worker at the standard rate — including static asset requests that are normally free and unlimited. On Free that silently moves the entire site's traffic onto the 100k/day cap. Do not enable it on this stack; treat any future product that touches asset serving with the same suspicion, because "asset requests are free" is the load-bearing assumption of this whole skill.

### Trap 4 — Flagship is a beta with no published pricing

Flagship is Cloudflare's native feature-flag product (public beta 2026-05-26) — native Workers binding, targeting rules, percentage rollouts, audit history, edge-local evaluation, config propagation in seconds, `wrangler flagship` CLI, OpenFeature SDKs including a browser client. Two honest caveats — it ships assignment, not measurement (no stats engine anywhere in its docs; experiment analytics stays on the analytics layer), and NOTHING about pricing or plan gating is published. Usable on Free during beta; GA may gate it. It is this skill's most volatile pin — re-verify before recommending it in any client build.

## Fork e1 — A/B testing

| Option | Invocation cost | Failure mode | When it wins |
|---|---|---|---|
| Client-side assignment — both variants in the prerendered HTML, inline head script assigns before paint, exposure event to analytics | Zero | Flicker if the script is late; variant markup visible in source | DEFAULT for a mostly-static site on Free |
| Worker-first — cookie assignment + variant asset rewrite via `env.ASSETS.fetch()` (Cloudflare's own canonical example) | Every matched HTML request, shared cap | 429 over cap (trap 2) | Flicker measurably hurts the metric, or the variant must be SEO-visible / correct without JS |
| Worker-first + Flagship as the config plane | Same as above | Same, plus beta risk (trap 4) | You already run worker-first and want rollout percentages and a kill switch without redeploys |

Lean — client-side. It is the only option with zero invocations, no coupling to the forms cap, and no 429 mode; measurement lives in the analytics layer either way (Flagship has no stats engine). Flip when flicker demonstrably contaminates the metric under test, when the experiment changes SEO-visible structure, or when the site moves to Workers Paid (worker-first becomes effectively free at marketing-site scale).

## Fork e2 — Where edge logic lives

| Option | Verdict |
|---|---|
| Zone rules (Redirect Rules, Transform Rules, Bulk Redirects) | FIRST CHOICE when a declarative surface can express the job — zero invocations, runs before the Worker |
| Custom Worker entry — wrangler `main` pointing at your file that wraps the adapter handler (snippet 3) + scoped `run_worker_first` globs | The one sanctioned interception point when real logic is needed |
| Astro middleware | NON-OPTION for prerendered pages (trap 1, three reasons) |

Lean — declarative first, custom entry when there is logic. Flip when pages move to on-demand rendering: middleware comes back to life there, and most of this skill's prerendered-specific guidance changes shape with it.

## Fork e3 — Geo personalization

| Option | Cost | When it wins |
|---|---|---|
| Client-side heuristics — `Intl.DateTimeFormat().resolvedOptions().timeZone` + `navigator.language` | Zero network | Coarse cases ("is this visitor plausibly in MX") |
| Tiny on-demand endpoint returning `request.cf` fields (snippet 2), cached in `sessionStorage` | ~1 invocation per session | Real country/city/timezone needed |
| `/cdn-cgi/trace` parse | Zero invocations | Undocumented fields — test per project, never rely by default |
| Worker-first edge rewrite of geo variants | Trap 2 profile | Geo content must be in the initial HTML (SEO, no-JS) |

Lean — heuristics for coarse, endpoint for real geo; both keep the site fully static. `request.cf` (country, city, region, timezone, latitude, longitude, isEUCountry, colo, asn) is available on ALL plans including Free; in Astro read it as `Astro.request.cf` on on-demand routes only — on prerendered pages it is a build-time artifact, not the visitor. Flip to edge rewrite when geo variants must be crawlable and SEO-distinct.

## Fork e4 — Feature flags

| Option | Verdict |
|---|---|
| Build-time env flags — evaluated during `astro build`; flipping = git push, Workers Builds rebuilds | DEFAULT — zero products, zero invocations, zero page weight on a fully prerendered site |
| Flagship binding — `[[flagship]]` in wrangler, `env.FLAGS.getBooleanValue(...)` | For runtime toggles in code that ALREADY runs in the Worker (`/_actions/*`, worker-first routes). Beta caveats in trap 4. Prerendered pages need its browser SDK or a rebuild |
| DIY Workers KV flags | NEVER on this stack — Free caps at 1,000 writes/day, and Flagship (itself KV+DO-backed) dominates it with a UI, targeting, and audit at the same documented cost of nothing |

Lean — build-time default; Flagship only where Worker code already runs. Flip when Flagship GA lands with pricing (re-run this fork with numbers), or when flags must flip mid-incident faster than a Workers Build completes (the browser SDK then covers page-level flags too).

## Fork e5 — Redirect surface

| Surface | Free quota | Runs where | Wins when |
|---|---|---|---|
| `_redirects` (Static Assets) | 2,000 static + 100 dynamic rules, path-only, 1,000 chars/rule | Asset layer, zero invocations | DEFAULT — path-to-path moves; lives in git, deploys with the site |
| Redirect Rules (Single Redirects) | 10 rules/zone, wildcards yes, regex no | Zone edge, before the Worker | Cross-host or scheme redirects, apex-to-www — anything path-only `_redirects` cannot express. Budget the 10 |
| Bulk Redirects | 15 rules, 5 lists, 10,000 URL redirects | Account-level edge | Domain migrations and legacy URL maps past 2,000 rows or spanning zones |
| Worker code | Burns the shared cap per hit | Worker | Only computed targets (per-cookie, per-geo) no declarative surface expresses. Last resort on Free |

Lean — `_redirects` in git by default. Note the drift surface: Redirect Rules and Bulk Redirects live in the dashboard, not the repo — document them in the site's own docs when used, because nothing in git will show them.

## Snippet 1 — Client-side A/B assignment

Inline pre-paint script so the variant class exists before first render (no flicker). Under Astro's hash-based CSP an inline script needs the single-sourced manual-hash pattern — one exported constant imported by BOTH the config (which hashes it) and the layout (which renders it) — exactly like the no-flash scheme script this stack already ships. Do not duplicate the string.

```js
// src/lib/ab-test.js — export const AB_SCRIPT = `...` (single-sourced, hashed in astro.config)
(() => {
  var KEY = 'ab-hero';
  var v = localStorage.getItem(KEY);
  if (!v) {
    v = Math.random() < 0.5 ? 'a' : 'b';
    localStorage.setItem(KEY, v);
  }
  document.documentElement.dataset.abHero = v;
})();
```

Both variants ship in the HTML; CSS shows one — `html[data-ab-hero='a'] .variant-b, html[data-ab-hero='b'] .variant-a { display: none; }`. Fire ONE exposure event to the analytics layer from a bundled script after load (the experiment is unreadable without exposure counts). Reduced-payload rule: this pattern is for variant-sized differences (a hero, a CTA, a section), not whole-page forks — two full pages belong to the worker-first option.

## Snippet 2 — Geo endpoint

```ts
// src/pages/api/geo.ts — the ONE on-demand route this job needs
export const prerender = false;

export async function GET({ request }: { request: Request }) {
  const cf = (request as { cf?: Record<string, unknown> }).cf ?? {};
  return Response.json(
    { country: cf.country ?? null, city: cf.city ?? null, timezone: cf.timezone ?? null },
    { headers: { 'cache-control': 'no-store' } },
  );
}
```

Client side, call it once per session — `sessionStorage` the result — so the cost is ~1 invocation per visitor, not per pageview. Personalize after load; the page itself stays prerendered and free.

## Snippet 3 — Custom Worker entry

The documented adapter mechanism for edge logic on request paths (the old `workerEntryPoint` adapter option was REMOVED):

```ts
// src/worker.ts
import { handle } from '@astrojs/cloudflare/handler';

export default {
  async fetch(request: Request, env: unknown, ctx: unknown) {
    // edge logic here — runs for /_actions/*, unmatched routes,
    // and any run_worker_first patterns declared in wrangler.jsonc
    return handle(request, env, ctx);
  },
};
```

Point wrangler `main` at this file IN THE DEPLOY CONFIG ONLY. This stack runs the split-config pattern (the playbook's forms recipe documents it): the root `wrangler.jsonc` carries `main` + `assets` + `build.command` for `versions upload`, while the Vite plugin reads a minimal `wrangler.vite.jsonc` WITHOUT `main` via the adapter's `configPath` — pointing the plugin at a `main` that does not exist yet breaks `astro build`. Scope `run_worker_first` globs in the same deploy config, with `!` exceptions for `/_astro/*` and other subresources (trap 2).

## Platform pins and review-gates

Platform surfaces, not npm packages — verified 2026-08-17 against Cloudflare and Astro primary docs; re-check quarterly or on changelog hits:

| Surface | Pinned fact | Review-gate |
|---|---|---|
| `run_worker_first` | boolean / glob array / `!` exceptions; matched requests always billed; over-cap 429 | Young syntax — re-verify semantics AND billing wording |
| Asset-first precedence | assets answer first; asset requests free and unlimited | Workers Caching already carved one exception — watch for more erosion of "assets are free" |
| Workers Free caps | 100k req/day, 10 ms CPU, Error 1027 semantics | Per-plan numbers move; re-read the limits page |
| `request.cf` geo | standard fields on ALL plans; only botManagement gated | Field availability per plan |
| KV Free | 100k reads / 1,000 writes per day, 1 GB | Only matters if the KV fork ever reopens |
| Flagship | public beta 2026-05-26, `[[flagship]]` binding, NO published pricing | HIGHEST volatility — GA may bring pricing or plan gating; re-check before any client recommendation |
| Adapter contract | `Astro.request.cf` (not `locals.runtime`), custom entry via wrangler `main` + `handle` from `@astrojs/cloudflare/handler`, `workerEntryPoint` removed | This API surface moved in BOTH current majors (13 and 14) — pin per-major |
| Redirect quotas | `_redirects` 2,000+100 · Redirect Rules 10 · Bulk 10,000 URLs | Quota table per plan |

## Limitations

- This skill does NOT cover: security headers or middleware-as-header-transport (web-security-headers owns middleware); performance budgets and CI thresholds (perf-ci-gates); the analytics layer that measures the experiments this skill assigns (the playbook's analytics recipe); full-build composition order (stack-integration-playbook).
- Everything here assumes the fully-prerendered deploy shape. A site that moves to on-demand rendering re-opens middleware, changes the billing math, and should re-run forks e1–e3 from scratch.
- Flagship guidance is beta-era and pricing-blind by necessity; treat every Flagship mention as carrying its review-gate.
- Verified 2026-08-17. Cloudflare platform surfaces move faster than npm pins — the review-gate table above is the maintenance contract.
