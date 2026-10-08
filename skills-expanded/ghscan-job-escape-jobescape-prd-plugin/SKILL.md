---
name: prd-funnel
description: Service context for writing a PRD targeting the `funnel` service — jobescape's multi-step conversion flow (quiz → selling page → checkout). Load this when `prd-writer` identifies `funnel` as the target service, or when a PRD mentions quiz steps, onboarding funnel, selling page, chase/super_chase discounts, A/B variants, paywall tests, or payment processors.
---

# funnel — service context for PRDs

## What this service is

The user-facing conversion funnel: a sequence of quiz steps (gender, age, goals, skills, income, etc.) that routes a user to a personalized selling page and checkout. Heavily A/B-tested via GrowthBook. This is the **runtime** — it consumes config produced by `funnel-constructor-editor`.

## How to use this context

Everything in this file is background for **you**: vocabulary, feasibility signals, scope traps, and the analytics naming convention. None of it is content for the PRD body — the PRD contains no technical details (see `prd-writer`). When a note below says a change is bigger than it looks, that means: scope it and question the PM accordingly — don't write the technicalities into the PRD.

## Tech stack — what matters for PRDs

- **Next.js 14** (App Router, SSR/dynamic rendering)
- **Effector** for state, persisted via `effector-storage` (answers survive page reloads)
- **GrowthBook** for feature flags and A/B variant routing (country- and attribute-aware)
- **PostHog + BigQuery** dual analytics pipeline
- **Payment processors** — Stripe, Adyen, Checkout.com, Google Pay, Apple Pay, Primer, Airwallex, Solidgate (which one is active depends on geo and flag)
- **Tailwind v4 + Radix UI** for the UI; Framer Motion / Lottie for animations

## User-visible surface

- `/chat-v3/gender` — entry step, routes to `/chat-v3/age`, `/chat-v3/goals`, etc.
- `/chat-v3/selling-page` — dynamic selling page; layout driven by `selling_version`
- `/` — rewrite to a Framer-hosted marketing site (not part of this service's code)
- `POST /api/analytics` — event sink (not user-facing, but load-bearing)

## Vocabulary PMs should use correctly

- **Funnel step** — one page in the quiz
- **Funnel version** (`funnel_version`) — overall flow variant
- **Quiz version** (`quiz_version`) — which question set is live
- **Selling version** (`selling_version`) — which selling-page layout (e.g. `v6.0.0`)
- **Chase / super_chase** — discount upsell variants, triggered by `discount` query param
- **Paywall test** — checkout-flow A/B variant
- **Persona** — cohort inferred from answers (not stored as a field; emergent)

## Analytics events — where and how

- **Hook:** `/src/shared/providers/analytics/useAnalytics.ts`
- **Sink:** `/src/app/api/analytics/route.ts` → Google Cloud Pub/Sub → BigQuery
- **Pattern:** `track(eventName, eventProps)` — props enriched server-side with user ID, version flags, UTM, device, geo
- **Naming:** events prefixed `pr_funnel_*` (e.g. `pr_funnel_landing_page_view`, `pr_funnel_start`, `pr_funnel_selling_page_view`, `pr_funnel_error`)
- **Dual pipeline:** PostHog also receives events with a different payload. A PRD that specifies an event **must say which pipeline is the source of truth** for its dashboards.

When proposing new events: follow the `pr_funnel_{surface}_{action}` convention.

## Figma / design

No in-repo Figma references. The selling-page UI is fetched from an external service (`fce-lib`, `getSellingPage()`), so design work for selling-page changes often lives alongside the constructor, not here.

**PM hook:** in the PRD's Design section, attach Figma URL AND the `selling_version` tag the design corresponds to — design and version flag must roll out together or users see a mismatched page.

## Typical PRD concerns for this service

1. **Version coordination** *(background)*. A new step, a new layout, or a new pricing tier usually means engineering coordinates several version flags. For the PRD: keep the scope crisp about which parts of the flow change (new step? new selling layout? new discount?) — the flag work is engineering's.
2. **Users mid-funnel.** Quiz answers persist across the session, so adding/removing a question affects users who are already partway through. For the PRD: ask the PM what those users should experience (see the new question, skip it, restart?) — that's a product decision. The migration mechanics are engineering's.
3. **Pricing matrix.** Chase vs super_chase, trial prices, currencies — PRD must include the full matrix (or link to it), not just "show a discount."
4. **Geo-locked behavior.** GrowthBook evaluates `country` and `domain`. A user changing networks (VPN) mid-funnel can be re-bucketed. PRDs with geo-gated features must say so explicitly.
5. **Analytics source of truth.** For each new event, name the dashboard system (PostHog or BigQuery) that owns it.
6. **Payment scope.** Payment features don't automatically work for every payment method and geo. For the PRD: ask the PM which payment methods and geos are in scope for v1 and which are explicitly deferred — that's a product scope decision.

## Gotchas to flag in PRDs

- **New quiz step = four artifacts minimum**: new route/page, form component, analytics events, GrowthBook variant config. Missing any one leaves the step broken for a cohort.
- **Selling-page content is externally served** via `fce-lib`. "Change the copy on the selling page" is a PRD for the constructor, not this service.
- **Trial/discount pricing differs between test and production environments** *(background)*. Feasibility note: pricing features are harder to verify before launch than they look; a timeline signal, not PRD content.
- **Event schema is unversioned.** Renaming an event prop is a breaking change for existing dashboards — propose a new event rather than editing an old one.
- **`funnel-constructor-editor` produces the configs this service renders.** If the change requires new block/component types in the selling page, the PRD has a cross-service dependency — say so in one plain-language sentence in the PRD Summary.
