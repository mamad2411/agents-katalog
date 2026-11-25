---
name: sanity-optimizations
description: Audit whether a Next.js + Sanity site uses Sanity efficiently and what it will cost. Runs three read-only auditors in parallel (`sanity-query-auditor` for GROQ over-fetching, query size and Sanity reads per route; `sanity-image-auditor` for image CDN use, widths and `sizes`, LQIP, preload; `sanity-delivery-auditor` for API CDN vs live API, draft-only Live/stega, static vs dynamic routes, cache tags, webhook scope), merges their findings into one report ranked by impact, and estimates Sanity and Vercel usage for 100–5,000 daily visitors against the Free and Growth quotas. Use when the user asks "optimize Sanity", "are we over-fetching", "how many queries per page", "is the CDN used", "are images the right size", "is the site static", "Sanity usage / quota / bill", "why is the site stale", or before the launch of a Next + Sanity site. Reports first; changes code only after the user picks the fixes.
---

# Sanity optimizations audit

Read-only until the user picks which findings to fix. The output is one findings report, a
fetches-per-route table, a usage estimate and an offer to fix.

| File | Use |
|---|---|
| `.agents/agents/sanity-query-auditor.md` | Checks Q1–Q11: GROQ shape and size, reads per route |
| `.agents/agents/sanity-image-auditor.md` | Checks I1–I10: transformer, widths and `sizes`, variants, raw URLs |
| `.agents/agents/sanity-delivery-auditor.md` | Checks C1–C8, K1–K10, B1–B3: CDN, draft mode, rendering, cache tags, bundles |
| [`references/starter-baseline.md`](references/starter-baseline.md) | What the starter already does right and its known gaps, by check ID |
| [`references/usage-model.md`](references/usage-model.md) | Pricing and quotas (with sources and date), definitions, formulas |
| [`scripts/usage-estimate.mjs`](scripts/usage-estimate.mjs) | Monthly Sanity + Vercel usage calculator, no dependencies |

Each check lives in exactly one auditor file; change it there.

## Phase 0: Scope

Settle these before the audit and put them at the top of the report:

- **Project and Next app path** (`web/` in the starter). A Nexity project? Then
  the auditors check `references/starter-baseline.md` instead of rediscovering it.
- **Versions** of `next`, `next-sanity`, `@sanity/client` (the app's `package.json`).
- **Data layer map**, one line each: client(s), fetch helper, tag map and webhook, image path,
  proxy/middleware. On a project not built from the starter:
  `rg -n "createClient\(|client\.fetch|sanityFetch|defineLive|revalidateTag|urlFor|next/image" src`.
- **What can be measured:** production URL, build env (ask; never read `.env` files), a logged-in
  Sanity CLI, the Sanity and Vercel usage pages. Whatever is missing goes under "Not checked".
- **Scope:** the whole site, or one area (only images, one route).

## Phase 1: Audit in parallel

Start the three auditors at once, each with the same brief: project root, Next app path,
starter-derived or not, versions, production URL if any, whether the Sanity CLI may be used,
and the scope. They are read-only and independent.

Agents without subagents: read each auditor file and walk its checklist in sequence (query,
image, delivery), producing the same output contract for each.

While they run, measure what static reading misses (skip what Phase 0 ruled out):

1. **Build route table.** `pnpm build` in the app. Every content route should be `○` or `●`;
   list any `ƒ` with its reason.
2. **Fetch log.** Temporarily add `logging: { fetches: { fullUrl: true } }` to `next.config`,
   `pnpm build && pnpm start`, open one route of each type and read the `HIT`/`MISS`/`SKIP`
   lines. Remove the setting afterwards.
3. **Response sizes.** Run the main queries in Vision or with `curl` against
   `https://<projectId>.apicdn.sanity.io/v<apiVersion>/data/query/<dataset>`; note the bytes and
   the `ms` field. This is `--responseKb`.
4. **Dataset** (Sanity CLI): document count vs plan (Free 10k, Growth 25k),
   `sanity documents query 'count(*[!(_id in path("drafts.**"))])'`; asset storage (100 GB on
   both plans).
5. **Real usage.** The Sanity project's usage page (sanity.io/manage → Usage) and Vercel's Usage
   tab beat any estimate; compare them with Phase 3 and explain the gap.

Page speed itself (Lighthouse, Core Web Vitals) is a separate measurement; when a fix here is
meant to speed up a page, measure it before and after with the same tool and settings.

## Phase 2: Merge

- **Dedupe:** the same file:line from two auditors is one finding with the higher severity and
  both IDs (a POST query read twice is Q5 + Q7; an untagged fetch on a dynamic route is K1 + K3).
- **Reconcile with measurements:** a route the delivery auditor calls static but the build marks
  `ƒ` is a finding; a duplicate read the fetch log shows as `HIT` is not.
- **Baseline:** on a starter project, mark each known gap as still present or fixed, and flag any
  "already right" row that regressed (usually High).
- **Rank** by severity, then by saving. **Critical** = fails or leaks drafts/tokens; **High** =
  breaks a quota or a Sanity limit at realistic traffic, or content stale for days; **Medium** =
  measurable waste or staleness; **Low** = tidy-up; **Info** = deliberate trade-off.

## Phase 3: Usage estimate

Run the calculator with the auditors' numbers and the measurements; list every input you
changed and its source:

```bash
node .agents/skills/sanity-optimizations/scripts/usage-estimate.mjs \
  --fetchesPerPage=9 --responseKb=40 --routes=60 --publishes=80 --purgeRoutes=60 \
  --imagesPerPage=8 --uniqueImages=250
node .agents/skills/sanity-optimizations/scripts/usage-estimate.mjs --help   # all inputs
```

| Input | From |
|---|---|
| `--fetchesPerPage` | query auditor: reads per cold render of a typical route, after dedupe |
| `--routes`, `--purgeRoutes`, `--uncachedTarget`, `--proxyPerPage` | delivery auditor |
| `--imageMode`, `--imagesPerPage`, `--uniqueImages`, `--variantsPerImage`, `--originalKb` | image auditor |
| `--responseKb` | Phase 1 measurement |
| `--visitors`, `--publishes`, `--builds` | the user or analytics; otherwise the defaults, marked as guesses |

Cached = static/ISR with tags; uncached = every view renders and reads Sanity.
`--imageMode=sanity` shows the cost if images moved to a Sanity loader. Formulas, defaults and
the pricing table are in `references/usage-model.md`. If the prices' check date at the top of the
script is more than a few months old, re-check sanity.io/pricing and vercel.com/pricing and
update the script's constants and the reference table before quoting.

## Phase 4: Report

```markdown
## Sanity optimizations audit: <project> (<date>)

Data layer: <client(s), fetch helper, tags, webhook, image path: one line each>
Versions: next <x>, next-sanity <x>, @sanity/client <x>

### Findings
| # | Sev | File:line | Issue | Fix | Estimated saving |
|---|---|---|---|---|---|
| Q5 | High | src/sanity/lib/queries.ts:475 | Page query is 181 KB, sent as POST, near the 300 KB CDN cap | Collapse whitespace; stop inlining sections twice | -35% query size now; removes the hard-fail risk |

### Already right
<short list: keep these when refactoring>

### Fetches per route
<query auditor's table, corrected by the fetch log>

### Rendering per route
<delivery auditor's table, corrected by the build output>

### Images
<image auditor's numbers>

### Usage estimate (per month)
<the script's two tables + inputs and their sources>
Plans: Sanity Free / Growth, Vercel Hobby / Pro, checked <date>: <links>

### Not checked
<what could not be measured and why: no build env, no production URL, no CLI login, no usage data>
```

"Estimated saving" is concrete where possible: requests per month from the usage model, KB per
response, reads per cold render, days of staleness. Write "latency only" or "none, correctness"
when that is the truth.

## Phase 5: Fix what the user picks

Ask which findings to fix, grouped: quick wins (tags, `cache()`, projections, `sizes`),
structural (query splitting, shell query, image loader), and content/ops (webhook filter, unused
assets). Do not start without an answer.

- One finding per commit-sized change. Keep `defineQuery`, run TypeGen (`pnpm -C web ts:typegen`),
  then `pnpm -C web typecheck` and the tests.
- A projection change changes the generated types: fix every consumer and, in the starter, the
  Sections Gallery fixtures; then run the `groq-parity-reviewer` agent (or walk its checklist).
- Tag changes touch both sides: the fetch call site and the webhook mapping (`tags.ts` →
  `tagsForDocumentType` in the starter). Publish a test document and confirm the route updates.
- Re-run the measurement that found the problem (query size, fetch log, build table, headers)
  and put before/after in the summary. No saving is claimed without a second measurement.
- Don't change the image pipeline (loader vs optimizer) on your own: it trades Vercel cost against
  Sanity bandwidth and visual quality, and in the starter it is a recorded decision
  (`docs/agents/web-images-links.md`). Present the numbers and let the user decide.
