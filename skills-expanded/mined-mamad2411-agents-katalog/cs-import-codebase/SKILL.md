---
name: cs-import-codebase
description: >
  Import an existing codebase into CodeSpring as a visual feature map — core
  features (sidebar/nav pages) with nested sub-features and a "how it works"
  note per feature — then generate Frontend + Backend PRDs (via cs-create-prd)
  and run an independent background audit of the code vs the map. So CodeSpring
  understands the app and the user can design new features without duplicating
  or breaking what exists. Triggers, "import my codebase into CodeSpring", "map
  my existing app", "reverse engineer my app into features", "bring this project
  into CodeSpring", "visualize my code in CodeSpring".
allowed-tools: Bash(codespring:*) Bash(npx @codespring-app/cli:*) Bash(node:*) Bash(curl:*)
metadata:
  author: codespring
  version: "0.3"
---

# Import an existing codebase into CodeSpring

Turn a real repo into an accurate CodeSpring model: **core features → sub-features → notes → PRDs**, grounded in the code, then independently audit it. Drives the CLI + API so the map lands in the user's account automatically. This skill reads code and writes to CodeSpring; it does not modify the codebase.

Shared knowledge lives in the `codespring` skill's references — read them:
`references/analyze-codebase.md`, `references/mindmap-structure.md`, `references/prd-management.md`, `references/pitfalls.md`, `references/codespring-docs.md`.

## 0. Connect first
`codespring auth status` (login if needed) + `codespring status` (link if needed). Use the projectId from the LOCAL `.codespring/config.json`, never the global one, and print it. (See `pitfalls.md`.)

## 1. Definitions
- **Core feature** = highest-level unit, almost always a sidebar/nav item = a page. Read the sidebar/nav component first.
- **Sub-feature** = a capability nested under a core feature.
Card descriptions stay one sentence; depth goes in the note + PRDs.

## 2. Analyze the code (be accurate)
Follow `analyze-codebase.md`: frontend map (routes, components, what the user sees, navigation) and backend map (API routes + which features share them, data model, security, shared systems — credits/payments/refunds, jobs/cron/pipelines, storage/S3 buckets, auth/RLS, env vars — and infra). Set the real tech stack. Read files; don't guess.

## 3. Build the map (CLI)
```bash
codespring mindmap set-info --title "..." --description "..." --github "<repo url>"
codespring mindmap tech-stack --replace --add '[{"id":"tech-...","title":"...","description":"Frontend"}, ...]'
codespring mindmap features --add '[{"title":"Dashboard","description":"..."}, ...]'   # CORE features; keep the returned ids
codespring feature create --parent <coreId> --title "..." --description "..."           # sub-features
codespring mindmap note <coreId> --title "How it works — X" --text "$(cat note.txt)"    # one note per core feature; redirect output to /dev/null
```
Write each core feature's note using the depth from `analyze-codebase.md` §8–9 — it becomes the PRD generator's context.

## 4. Generate PRDs — via the cs-create-prd skill
Do NOT re-implement PRD mechanics here. For each core feature, use **`cs-create-prd`** (Both frontend + backend) — it captures the shared backend contracts (routes, data model, auth/RLS, jobs/cron, storage, payments/credits/refunds, env vars, dependency map) and attaches the PRD bridge nodes correctly. Loop it over the core features (mindful of the ≥120s timeout and dedupe rules it documents).

## 5. Verify the map (see pitfalls.md)
- `node-features.items.length` still equals the real core-feature count (re-parent any flattened sub-features).
- Each targeted feature has real PRD content and a `prdBridge` with `prdFrontend`/`prdBackend` carrying a valid `prdId`.
- Give the user their project link: `https://v2.codespring.app/project/<projectId>`.

## 6. Independent background audit (self-contained, read-only)
After the map is built, spawn a **background sub-agent** with a FULLY SELF-CONTAINED brief — give it NO context from the import work, so its comparison is unbiased. Its brief (agnostic):

> You are an independent auditor. Read-only: do not modify the codebase or the CodeSpring map.
> 1. **Inventory the whole codebase** — every router/route, page, DB table + enum, external provider, webhook, cron/job/pipeline, and the shared backend contracts (credits/refunds, generation/job pipelines, media/render compositions, storage/S3 conventions, auth/RLS, env vars).
> 2. **Read everything documented in CodeSpring** — every feature's notes and PRDs (via the `codespring` CLI).
> 3. **Compare with a critical lens and report**, prioritising **shared backend-infrastructure gaps and conflict risks** (the riskiest part when adding a new feature). Flag: anything in the code that's undocumented; anything that could cause a conflict or a duplicated/broken shared system when building something new; and anything documented but missing critical backend detail — each **rated by severity** with exact file/route/table references, plus a shortlist of what to add to CodeSpring to keep future feature-building conflict-free.

Run it in the background and tell the user you'll report when it's done. When it finishes, walk them through the findings and offer to fold the shortlist back into the notes/PRDs (or hand off to `cs-resync-codebase`).

## What good looks like
- CodeSpring holds an accurate map — right core features, nested sub-features, honest notes, FE/BE PRDs per feature.
- An independent, read-only audit has flagged undocumented code, shared-system conflict risks, and missing backend detail by severity — so new features can be built without duplicating or breaking what exists.
