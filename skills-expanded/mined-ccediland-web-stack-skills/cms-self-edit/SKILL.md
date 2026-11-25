---
name: cms-self-edit
description: Give a non-technical client the ability to self-edit the content of an Astro 7 site on Cloudflare Workers Static Assets, with no lock-in, using a git-based CMS. Use when wiring a content editor into an Astro plus Cloudflare site, when a client must edit pages without touching GitHub, when setting up Sveltia CMS or mounting the admin under public/admin, when configuring the sveltia-cms-auth Worker, when storing media in Cloudflare R2, when adding Spanish and English i18n with AI translation, or when publishing through a drafts branch with CI. Also covers the escalation ladder to Pages CMS and Directus. Also owns content modeling — what becomes a collection, the Zod schema and its config.yml mirror. Trigger on add a CMS to Astro, let my client edit content, model the content, content collections schema, Sveltia CMS, git-based CMS, or admin panel for Astro. Not for business data rows (data-layer) or the site's CI gates (perf-ci-gates) — this skill wires the client editing layer.
---

# Client Self-Editing for Astro on Cloudflare

> Give a non-technical client a content editor for an Astro 7 site on Cloudflare Workers Static Assets, with no vendor lock-in. The default is Sveltia CMS, a client-side git-based admin mounted as a static file under public/admin that writes Markdown and YAML straight into the repo. A three-stage ladder escalates to Pages CMS, then Directus, when the editor's needs outgrow git.

## TL;DR
- Default to Sveltia CMS. It is a single-page admin served as a static file from public/admin, no backend, content stored as Markdown and YAML in the repo, so there is no lock-in and the files survive even if the CMS is swapped out.
- Mount public/admin as a static passthrough file. Astro does not inject its hash-based CSP meta element into public/ passthrough files, so /admin sits outside the site CSP from web-security-headers. Add a CSP for /admin explicitly in _headers.
- Critical caveat, repeated under Limitations: the OAuth login opens a popup and reads it back through postMessage, so Cross-Origin-Opener-Policy same-origin (the site default from web-security-headers) breaks login. Scope same-origin-allow-popups to /admin in _headers.
- Sveltia works on one branch only; Editorial Workflow does not exist yet. Publish by pointing the backend at a drafts branch, gating with the project CI, and merging to the production branch to go live.
- Media goes to the repo for small or mostly-static sites (Sveltia converts to WebP first), and to Cloudflare R2 above the threshold. The GitHub backend has no Git LFS, so large media must go to R2.
- DeepL is currently disabled in Sveltia. Use Google Cloud Translation, Gemini, or Mistral for AI translation.

## Reference materials — load when relevant

This SKILL.md is the verdict, the ladder, and the recipe in order. Load a reference only when its condition is met:

- references/content-modeling.md — load when deciding what becomes a collection at all, designing the Zod schema and its config.yml mirror, choosing documents versus rows (the data-layer boundary), or planning a schema change against existing content.
- references/sveltia-setup.md — load when mounting the admin panel, writing config.yml, or mapping collections to Astro content collections and Zod schemas.
- references/cloudflare-auth-worker.md — load when deploying sveltia-cms-auth, registering the GitHub OAuth App, choosing OAuth versus a personal access token, or hitting the COOP login failure.
- references/media-r2.md — load when deciding between repo media and R2, or when configuring the R2 bucket, token, CORS, and public URL.
- references/i18n-and-publishing.md — load when adding Spanish and English locales, wiring AI translation, setting up the drafts-branch publishing flow, or giving the client a preview URL.
- references/escalation-ladder.md — load when Sveltia is outgrown: when the client must never see GitHub (Pages CMS), or when content turns relational or multi-channel (Directus).

## Verdict — the three-stage ladder

Pick the lowest stage that meets the editor's needs. Each stage trades simplicity and zero-cost for a heavier dependency.

| Stage | Tool | Use when |
|---|---|---|
| 1 (default) | Sveltia CMS | A non-technical client edits content; a GitHub account per editor is acceptable; content is files for a static site |
| 2 | Pages CMS | The client must never see GitHub and needs passwordless magic-link login |
| 3 | Directus | Content is relational or multi-channel, needs instant publish without a rebuild, or needs a real editorial workflow with roles |

Stages 1 and 2 are git-based: content stays as files in the repo, no database, no lock-in. Stage 3 is database-backed and is a per-site engine, not a drop-in. Stages 2 and 3 are pointers in references/escalation-ladder.md, not full recipes.

## Architecture — how Sveltia sits in the stack

Sveltia is a static single-page app. The admin lives at public/admin/index.html and loads the npm bundle as a first-party script; its config.yml, next to it, declares the GitHub backend and maps collections to the site's Astro content collections. The editor signs in through a GitHub OAuth App fronted by a free Cloudflare Worker (sveltia-cms-auth), or with a personal access token for a sole admin. Saving an entry commits Markdown or YAML to a branch; media uploads go to the repo or to R2.

The load-bearing interaction is with web-security-headers (skill 2). Because /admin is a static passthrough file, Astro's native CSP meta element never lands on it, and the project _headers file carries no site-wide CSP. So /admin has no CSP by default. This skill adds a hardened CSP scoped to /admin in _headers, and overrides one site default there: COOP must be same-origin-allow-popups on /admin so the OAuth popup and its postMessage handshake survive.

## Setup

### 1. Mount the admin panel

Install the bundle as a first-party dependency rather than the CDN so the version is pinned and no third-party origin is needed in the CSP. Create public/admin/index.html that loads it, with a robots noindex meta so the admin is not indexed. See references/sveltia-setup.md.

### 2. Write config.yml and map collections

Put config.yml next to index.html. Use the GitHub backend, point branch at drafts, and set format to yaml-frontmatter. Use YAML frontmatter, never TOML, because Sveltia's TOML output is unreliable. Each Sveltia folder collection maps to one Astro content collection directory; field types map to the collection's Zod schema. See references/sveltia-setup.md for the field-to-Zod table and a round-trip example.

### 3. Authentication

For a sole technical admin, a GitHub personal access token needs no setup. For a non-technical client, deploy the sveltia-cms-auth Worker (free), register a GitHub OAuth App with callback at the worker plus /callback, set the worker environment variables, and set base_url in config.yml to the worker URL. See references/cloudflare-auth-worker.md, including the COOP fix.

### 4. Media

Default to committing media to the repo for small or mostly-static sites; Sveltia converts images to WebP and resizes client-side before commit. Move to R2 when media is large or frequent, or when uploads exceed GitHub's browser limit, because the GitHub backend has no Git LFS. See references/media-r2.md for the threshold rule and the R2 setup.

### 5. i18n and translation

For a Spanish and English site, use the multiple_folders structure with default_locale es, which maps cleanly to Astro's per-locale routing. For one-click translation, use Google Cloud Translation, Gemini, or Mistral; DeepL is disabled. See references/i18n-and-publishing.md.

### 6. Publishing

Sveltia commits to one branch. Point it at drafts, let the project CI run on that branch, and publish by merging drafts into the production branch. Give the client a preview of the drafts branch through a Cloudflare Workers Builds non-production branch and its aliased preview URL. See references/i18n-and-publishing.md.

### 7. Secure /admin

Add a /admin block to public/_headers, before the site-wide block, with a CSP that allowlists what Sveltia needs and a Cross-Origin-Opener-Policy of same-origin-allow-popups. The exact directive list and the GitHub, R2, and translation origins are in references/cloudflare-auth-worker.md.

### 8. Verify

CSP cannot be tested in astro dev. Build and preview or deploy, then open /admin, confirm login works (the popup completes), create and save a test entry, confirm it lands on the drafts branch as valid frontmatter Astro parses, and check the console for CSP violations.

## Gotchas

- Cross-Origin-Opener-Policy same-origin nulls window.opener in the login popup and login fails silently. Use same-origin-allow-popups scoped to /admin. Do not use COEP require-corp on /admin.
- Sveltia's TOML frontmatter generation is buggy. Use YAML frontmatter and set format to yaml-frontmatter.
- The GitHub backend has no Git LFS, so any file over GitHub's limits has to live in R2. Uploads through the browser cannot exceed GitHub's browser file size cap.
- The OAuth Worker URL does not belong in CSP connect-src or frame-src. The login is a top-level popup navigation, not a fetch or an iframe; only api.github.com and www.githubstatus.com (and R2 and the translation origin) belong in connect-src.
- Editorial Workflow does not exist yet, so there is no branch-per-entry. The drafts-branch pattern is a manual stand-in; only one draft is in flight at a time and the next merge publishes everything on drafts.
- Sveltia is a public beta from a single maintainer. Pin the version and re-verify on upgrade.

## Limitations and out-of-scope

- This skill does NOT design the site's content schema. Which collections and fields exist is per-project; this skill shows how to wire whatever schema exists into Sveltia and Astro.
- It does NOT cover e-commerce, search, or an enterprise editorial workflow. Those move the project to Directus (stage 3); see references/escalation-ladder.md for the boundary only.
- The performance CI gate is owned by perf-ci-gates (skill 3). A commit on drafts triggers the same ci.yml; this skill only points at it.
- Self-hosted SSO (Authentik) over the admin is an advanced option, not developed here.
- Sveltia is a single-maintainer public beta. File portability is total; config portability to another Decap-compatible CMS is high but bounded by Sveltia-only options (R2 media, the AI translation services, multiple_root_folders, UUID slugs, the locale-prefixed relation value_field, singleton collections). The CSP-and-/admin interaction is verified against current docs but re-check on upgrade.
- Pins are current as of 2026-08-17: sveltia/cms 0.191.2 (beta with near-daily release cadence; the 1.0 RC milestone is close — 38 of 41 issues closed — but GA has NOT shipped, so do not wait on it), astro 7.x, @astrojs/cloudflare 14.x, Node 22. The admin-panel smoke-test after the 0.167 to 0.191 jump (24 minors of churn) PASSED 2026-08-17: the npm bundle mounted per this recipe boots, parses config.yml, and renders all three auth flows unchanged. The Keystatic reconsideration gate remains unmet — only its Astro peer-dep block was lifted, the Cloudflare OAuth issue stays open — so Sveltia stands. Re-verify the version, the Editorial Workflow status, and the translation service list on each build, since these move quickly.
