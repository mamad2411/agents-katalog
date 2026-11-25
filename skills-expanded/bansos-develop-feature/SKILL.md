---
name: bansos-develop-feature
description: Develop, review, test, or ship UI, SEO, data-flow, contributor, notification, and catalog changes for wauputr4/bansos and bansos.dev. Use when an AI agent needs to modify the SvelteKit and Cloudflare Pages site, work with folder-based listings or contributor profiles, verify local responsive UI, address PR reviews, or follow the repository's current validation and release workflow.
---

# Bansos Develop Feature

## Workflow

1. Read the repository README, `.github/CONTRIBUTING.md`, nearby route/component code, and current working-tree state before editing.
2. Trace shared data or component callers and fix the root cause in the smallest existing abstraction.
3. Preserve the SvelteKit prerender and Cloudflare Pages architecture. Do not add runtime state, secrets, or dependencies without a demonstrated need.
4. Keep public routes crawlable with accurate title, description, canonical, Open Graph, and structured metadata where the repository already supports them.
5. Reuse existing components, data helpers, theme tokens, icons, and responsive patterns.
6. Verify desktop and mobile behavior locally. Contributor shortlink pages intentionally omit the normal header/mobile navigation but keep the footer.
7. Use the folder-based add-entry flow for listing or contributor data instead of bypassing validation.
8. Run the narrowest relevant checks, then prepare a focused PR with screenshots or preview notes for visual changes.
9. When reviewing or merging, inspect unresolved review threads and current CI. Fix actionable findings, resolve satisfied conversations, and wait for required checks when requested.

## Current Project Constraints

- App: SvelteKit with Svelte 5 and `@sveltejs/adapter-cloudflare`.
- Hosting and previews: Cloudflare Pages.
- Listings: `src/lib/data/bansos/<slug>/index.json` plus optional/generated README.
- Contributors: `src/lib/data/bansos/contributors/<slug>/manifest.json` plus optional README/avatar.
- Canonical contributor profiles: `https://bansos.dev/<slug>/`; legacy `/contributor/<slug>/` is compatibility-only.
- Public `npx bansosdev`, form, and bot submission paths are disabled. Active public paths are email and Git clone/PR; maintainers use `npm run add:bansos` locally.
- Default Latest ordering comes from `publishedAt`; active Featured items belong in the featured surface rather than being duplicated in Latest.
- Generated catalog, commit-history, contributor, and LLM outputs must stay synchronized through repository scripts.

## Validation

Use only what the touched surface needs:

```bash
npm run validate:data
npm run check
npm run lint
npm run build
```

For UI changes, also run the local app and inspect the affected desktop and mobile routes. For notification scripts, use their dry-run or fixture path before touching a real webhook.

## Reference

Read `references/bansos-development-rules.md` for route, contributor, generated-data, and PR conventions.
