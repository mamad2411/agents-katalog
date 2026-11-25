---
name: fabrico-planning-migration
description: "Plan the migration of a legacy web app to a modern target — modern web (Next.js/React), native iOS (SwiftUI), or cross-platform mobile (React Native/Expo). Maps old behavior to a target stack, builds a feature-parity matrix, plans data and auth migration, adapts desktop UX to mobile where needed, and flags risks. Use after reverse-engineering a SPEC.md and before rebuilding with /fabrico-autopilot."
---

# Planning a legacy migration / modernization

Bridge a (reverse-engineered) `SPEC.md` to a concrete rebuild on a chosen target. The SPEC stays
platform-agnostic; this skill produces a `MIGRATION-PLAN.md` that pins the target, proves feature parity, and
surfaces what won't port 1:1 — so the autopilot build has a clear, de-risked path.

## Inputs

- A `SPEC.md` (ideally from `fabrico-reverse-engineering-spec`, with a Source-mapping appendix).
- The chosen **target** (or pick one with the framework below).
- Any constraints: offline support, App Store distribution, existing backend/API to keep, data export access.

## Output

`MIGRATION-PLAN.md` containing: chosen target + rationale, stack mapping, feature-parity matrix, data-migration
plan, auth/session plan, UX-adaptation notes, risk register, and a phased rollout. This plan + the SPEC are what
`/fabrico-autopilot` (via the engineering manager) consumes.

## Step 1 — Choose the target (if not given)

| Target | Best when | Default stack |
| --- | --- | --- |
| **Modern web** | reach via browser, SEO, desktop+mobile web, fastest path | Next.js (App Router) + TS + Tailwind, Prisma + Postgres, Auth.js |
| **Native iOS** | iOS-only, deep platform integration (push, widgets, offline), App Store first | Swift + SwiftUI, async/await, Core Data/SwiftData, URLSession |
| **React Native / Expo** | iOS **and** Android from one codebase, team knows JS/TS | Expo + React Native + TypeScript, React Navigation, TanStack Query |

Trade-offs to weigh: audience/platforms, team skills, offline & device features, distribution (web vs App Store),
budget/time, and whether an existing backend/API is kept (web & RN reuse REST/GraphQL easily; native iOS too, but
UI is rebuilt). Record the decision and rationale.

## Step 2 — Stack & pattern mapping

Map legacy patterns to target equivalents, e.g.: server-rendered multi-page → SPA/RSC or native navigation;
jQuery/Bootstrap widgets → component library; server sessions → token/session strategy of the target; synchronous
page reloads → async data fetching + optimistic UI. Produce a table: *legacy concern → target approach*.

## Step 3 — Feature-parity matrix

From the SPEC's Source-mapping appendix, list every feature/story and mark: **port as-is**, **adapt** (changed for
the target — say how), or **drop** (with reason + user sign-off). This matrix is the contract for "did we reach
parity". No feature leaves the legacy app silently.

## Step 4 — Data migration

Decide: greenfield schema rebuilt from the inferred model, or migrate existing data. If migrating, plan
export → transform → import, identity/relationship preservation, and a verification step (counts, spot checks).
If you lack access to the legacy database, note it as a blocker for the data step (the app can still be rebuilt
with seed/demo data).

## Step 5 — Auth, sessions & integrations

Plan how users authenticate on the target, whether existing accounts/passwords migrate (often a reset flow is
simpler and safer), and how each integration from the SPEC is handled (keep same provider, swap, or stub behind an
interface until keys are provided — never block the whole build on one integration).

## Step 6 — UX adaptation (esp. web → mobile)

Desktop-era patterns rarely port 1:1 to mobile. Note adaptations: dense tables → cards/lists with filters; hover
actions → tap/long-press/swipe; multi-column forms → steppers; mouse-only interactions → touch; deep menus →
tab/stack navigation. Keep behavior/intent from the SPEC; change the presentation to fit the target.

## Step 7 — Risk register & phasing

List risks (data loss, integration gaps, parity misses, platform limits, scope creep) with mitigations. Choose a
rollout: big-bang rebuild for small apps, or **strangler-fig / module-by-module** for large ones (rebuild
high-value modules first, run old and new in parallel, cut over per module). Sequence the epics accordingly.

## Guidance

- **Preserve behavior, modernize presentation.** Parity is about what users can do and the data, not pixels.
- **De-risk integrations and data early** — they cause the most surprises in migrations.
- **Make the parity matrix the source of truth** for "done", and feed the chosen target into the SPEC's
  "Target" section before the build runs.
