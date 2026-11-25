---
name: git-backed-knowledge-site
description: Build a password-gated, git-backed wiki/documentation site (Next.js block-content docs site + JSON-per-section git CMS + Vercel pipeline). Use when asked to create a knowledge base, internal wiki, team documentation site, or onboarding workshop site — especially when both humans and agents must edit content and deploys run on Vercel.
---

# Git-Backed Knowledge Site (the "Workshop" pattern)

A production-proven pattern for team knowledge sites: a chapter-book
documentation site where content is plain JSON in git, anyone with the site
password can edit in-browser with live preview, agents edit via HTTP or git,
and every change is an attributed, revertable commit that auto-deploys.

## When to use
- New internal wiki / team knowledge base / onboarding "workshop" site.
- Docs site where non-engineers AND agents must edit content safely.
- Any chapter-book knowledge product (learn-inference.com-style curriculum).

## Architecture (the 8 pillars)

1. **Stack**: Next.js App Router (beware: middleware is renamed `src/proxy.ts` in Next 16+ — read `node_modules/next/dist/docs/`), Tailwind v4 `@theme` tokens, strict TS, static generation via `generateStaticParams`.
2. **Content contract first**: `src/content/types.ts` — a discriminated-union `Block` model (lead/p/h2/h3/list/callout/media/code/table/checklist/terms/quote/cards/steps) — plus `src/content/manifest.ts` (chapters → sections with slug/title/summary/minutes/priority + provenance fields `status/owner/proof/source`). Everything renders through ONE `BlockRenderer`, so all pages stay visually consistent and an editor preview is pixel-exact for free.
3. **Content storage**: one JSON file per section at `content/sections/<chapter>/<section>.json` (`Block[]`). A `scripts/build-content.mjs` prebuild/predev step validates every file against a zod mirror of the Block schema and emits a gitignored generated module; consumers import `CHAPTER_CONTENT` from a stable barrel. Malformed content fails the build, never the site.
4. **Docs shell**: sidebar with numbered chapter groups, breadcrumbs, on-page TOC (scroll-spy), reading progress, prev/next in book order, ⌘K search (title/summary fuzzy + full-text body matches with highlighted snippets from a flattened index), light+dark themes purely via CSS custom properties + `data-theme` + a no-flash head script.
5. **Knowledge-governance features** (what makes it a *team* wiki): a `/start` onboarding tutorial (N must-know items, localStorage progress, links validated against the manifest at build time); a `/status` ledger bucketing every section (canon / wip / needs-review) from deterministic rules over manifest status strings + content callouts; optionally a `source-audit.ts` publication gate that renders unverified pages as deliberately-withheld panels (owner + missing authority) and excludes their text from search.
6. **Password gate**: `src/proxy.ts` checks an httpOnly cookie = SHA-256 of the passphrase (rotating the password invalidates all sessions); a `/gate` page + `/api/gate` POST; `X-Robots-Tag: noindex`; exempt `/api/cms/*` (must return 401 JSON, never redirect agents to an HTML login).
7. **Git CMS**: `GET/POST /api/cms/section` — zod-validate, then commit the section JSON to the default branch via the GitHub contents API (the serverless function holds a fine-grained PAT: ONE repo, Contents read/write only; users and agents never see it). Auth: the site-gate cookie grants write when no separate `EDIT_PASSWORD` is set; agents use `Authorization: Bearer CMS_AGENT_TOKEN`. Optimistic concurrency via a `baseSha` echo → 409 on conflict. Dev mode (no token) writes to disk. UI: an Edit link on every section → `/edit/[chapter]/[section]` structured block editor with a live preview **rendered by the real BlockRenderer**; a `/changes` commit log with one-click revert.
8. **Pipeline**: GitHub repo connected to Vercel; every save/push auto-deploys (~30–60s). Content edits and code changes ride the same rail.

## Build workflow

1. **Design round before building**: produce 3 genuinely different single-file HTML mockups of the homepage (real fonts via Google Fonts CDN), screenshot them, present with an evaluation table + recommendation, and let the user pick. Do not skip this — generic "dark docs site" looks get rejected. Write the winning direction into `DESIGN.md` as the contract, including exact palette hexes, type choices, and motifs.
2. **Write the contracts yourself, first**: `types.ts`, `manifest.ts` (full IA with real titles/summaries even if body copy is placeholder), and section stubs. This enables conflict-free parallel agent builds.
3. **Parallelize with one-file-per-agent**: a shell/design-system agent owns `src/app` + `src/components`; N content agents each own exactly one chapter file; a stabilizer agent builds/lints/audits coverage afterward.
4. Placeholder policy if content isn't ready: prose may be lorem, but headings, media labels ("VIDEO — <exact asset>"), table headers, and term names must be REAL so the content swap is mechanical. Media blocks render styled placeholder panels; support `src` for real images later (next/image inside the same frame).
5. Flatten to the JSON content store (pillar 3) BEFORE inviting outside editors, with a **parity gate**: byte-compare old vs generated `CHAPTER_CONTENT` before deleting anything.
6. Add the gate, CMS, and governance features. Verify with Playwright at 1440 and 390 widths in BOTH themes, and LOOK at the screenshots rather than trusting green exit codes.

## Guardrails (each cost real debugging time)

- **Vercel silently BLOCKS deploys for unassociated commit authors** (`COMMIT_AUTHOR_REQUIRED`). Every commit — human, agent, and CMS-generated — must use a GitHub-associated identity, e.g. `<id>+<user>@users.noreply.github.com`. Put editor attribution in the commit MESSAGE, never the git author field. Check deployment state via `vercel ls` or the API after the first push; an "UNKNOWN"/"BLOCKED" state means this.
- **Merge content overlays at SECTION level, never chapter level** — a chapter-level `Object.assign` lets a later overlay silently drop an earlier overlay's sections in the same chapter (this class of bug has hidden finished articles).
- **Playwright full-page screenshots race IntersectionObserver reveals** — below-fold sections appear blank in stitched captures. Scroll through the page first, or don't gate content-critical sections behind reveal animations.
- When integrating content branches that fork from old shells: take the CONTENT layer only (`git checkout <branch> -- content/ src/content/...`), never merge whole — stale shell files will revert redesigns.
- API editors should always echo `baseSha` from GET into POST, or they get last-write-wins instead of 409 conflict protection.
- Grep pitfalls: JS object keys without hyphens are often unquoted — searching for `"key"` gives false "missing content" results.
- The zod schema must use `strictObject` and mirror `types.ts` exactly; keep a pointer comment in `types.ts` so drift is caught in review.

## Env vars (production)

| var | purpose |
|---|---|
| `SITE_PASSWORD` | read-gate passphrase (code fallback ok for bootstrap) |
| `CMS_GITHUB_TOKEN` | fine-grained PAT, one repo, Contents R/W — the user must paste this themselves (never move their credentials between services for them) |
| `CMS_AGENT_TOKEN` | random bearer for agent edits (generate, store in `.env.local`) |
| `EDIT_PASSWORD` | optional: splits write access from read access |

## Success criteria

- `pnpm build` green with all sections prerendered; lint clean; parity gate passed.
- Both themes screenshot-verified desktop + mobile; no horizontal overflow.
- Live loop proven end-to-end: browser edit → attributed commit → auto-deploy → visible → revert from `/changes` → site restored. Prove it with a marker block you add and then remove.
- Unauthed `/api/cms/*` returns 401 JSON; the gate redirects everything else; `X-Robots-Tag: noindex` present on gated responses.
