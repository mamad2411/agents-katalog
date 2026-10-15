---
name: cs-create-prd
description: >
  Specialist for creating CodeSpring PRDs. Interactive — it lists the user's
  core features, asks which one and whether to generate a Frontend, Backend, or
  Both PRD, then deep-dives the real code and generates the PRD(s) and attaches
  them to the feature's bridge on the canvas. The PRDs capture the shared
  backend contracts and design system so new features are built without
  duplicating or breaking what exists. Use when the user wants a PRD / spec for
  a feature. Triggers, "create a PRD", "make a frontend PRD", "make a backend
  PRD", "generate PRDs for this feature", "document this feature in CodeSpring",
  "spec out X so I can design new features".
allowed-tools: Bash(codespring:*) Bash(npx @codespring-app/cli:*) Bash(node:*) Bash(curl:*)
metadata:
  author: codespring
  version: "0.2"
---

# Create a PRD in CodeSpring

A PRD gives CodeSpring a full, accurate understanding of a feature so new features build on what exists instead of duplicating backend, re-creating a shared API route, or reinventing the design system. This skill makes the **Frontend** and/or **Backend** PRD for a chosen feature, grounded in the real code.

This is the single source of truth for how PRDs get made — other skills (e.g. `cs-import-codebase`) call this rather than re-implementing it.

Shared knowledge is in the `codespring` skill's references: `references/analyze-codebase.md`, `references/mindmap-structure.md`, `references/prd-management.md`, `references/pitfalls.md`, `references/codespring-docs.md`.

## 0. Connect first
`codespring auth status` (login if needed) + `codespring status`. Use the projectId from the **local** `.codespring/config.json`; print it. If the codebase isn't in CodeSpring yet, run `cs-import-codebase` first. This skill READS code and WRITES only to CodeSpring — never modify the codebase.

## 1. Ask what to generate (interactive)
Show the user their **core features** (from `codespring features` / the mindmap `node-features` items), then ask:
1. **Which feature?** (one, several, or all)
2. **Frontend, Backend, or Both?**
Wait for their choice unless they already said.

## 2. Deep-dive the real code
Read the actual code for the feature (don't guess). Pull in the depth from `analyze-codebase.md` §8–9. Cover:

### Backend PRD — capture the shared contracts (this is the riskiest part when adding new features)
- **Architecture & structure** — how the feature's code is organized and the conventions it follows.
- **Routers / API routes / endpoints** — path, method, request/response, and **flag every route shared by more than one feature**.
- **Data model** — tables + enums, key columns, relationships; reads vs writes.
- **Reusable server code** — actions/services/queries/hooks that already exist and should be reused, not re-implemented.
- **Shared backend systems** — call these out explicitly because new features collide with them:
  - hosting / deploy target (AWS, Vercel, Fly, etc.) and any platform limits
  - crediting / usage-metering systems; payment, subscription, and **refund** systems
  - background **jobs / pipelines / queues / cron**; long-running or async generation jobs
  - storage: **S3 conventions / buckets**, file paths, signed-URL patterns
  - media/render pipelines (e.g. Remotion/video compositions) if present
  - databases, migrations
  - **auth and row-level security (RLS)**
  - **environment variable names** that must be used or can be reused
  - webhooks (and signature verification)
- **Security** — authz, ownership checks, validation, secrets, RLS, webhook signing.
- **Reuse & dependency map** — a "reuse this, don't rebuild it" list, PLUS **what depends on this** so a future change doesn't silently break other features.

### Frontend PRD — capture the design system AND the navigation
- **Design tokens** — colors/branding, corner radius, spacing scale, typography, shadows (from Tailwind config / CSS vars / theme).
- **Component & UI styles** — the UI library and how buttons/cards/inputs/modals are styled, incl. states.
- **Layout, positioning & spacing** — grid/flex, columns, breakpoints, gaps; where things sit relative to each other. Be concrete.
- **What the user sees** — header, sections, cards, tables, empty/loading states, toasts.
- **Navigation / interaction map** — the concrete path: which nav item/button opens it → route → what it shows → what each interaction does; plus links FROM/TO other features.

### Write it into the feature's note first (it is the generator's context)
```bash
codespring mindmap note <coreFeatureId> --title "How it works — <Feature>" --text "$(cat note.txt)"   # redirect output to /dev/null
```

## 3. Generate (see prd-management.md)
```
POST /prds/generate  { projectId, bridgeNodeId: "bridge-feature-<featureId>", prdType: "frontend" | "backend" }
```
Timeout ≥120s (a client abort still creates the record → duplicates). For "Both", make two calls. After generation, read the PRD back (`codespring prd <id>`) and confirm the shared-systems detail above actually landed; if thin, enrich the note and regenerate, or `prd sync` a better version.

## 4. Attach to the canvas (see mindmap-structure.md)
Add `prdBridge → prdFrontend/prdBackend` nodes and `PUT /mindmaps/project/<projectId>`. For a **core** feature `prdBridge.data.featureId = "node-features"`; for a **sub-feature** it's that feature's sub-feature group node id. `itemId` = the selected feature id. If a `prdBridge` already exists for the feature, add the PRD node to it instead of creating a second bridge.

> The user can also generate PRDs in the CodeSpring web app (right-click the feature's PRD bridge → add + generate). If they'd rather do that, point them at `references/codespring-docs.md`.

## 5. Dedupe if needed + verify
Duplicates from timeouts → checkpoint then delete extras (`prd-management.md`). Verify (`pitfalls.md`): PRD content is real and includes the shared-systems detail; the canvas shows the `prdBridge` + PRD node(s) with valid `prdId`; and `node-features` still has the right core-feature count (re-parent any flattened sub-features). Give the user their project link.

## What good looks like
- The Backend PRD reads like a contract for the shared systems: routes (with the shared ones flagged), data model, auth/RLS, jobs/cron, storage/buckets, payments/credits/refunds, env vars, and a clear "reuse this / don't break this" dependency map.
- The Frontend PRD captures the design system and the concrete navigation path.
- Both are attached to the feature's bridge and grounded in the real code.
