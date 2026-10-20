---
name: follow-create-web
description: Select and create a web project by type — landing, saas, paas, or a given framework
argument-hint: "[scope]"
related:
  - design-web-prototype
  - design-html-prototype
  - follow-create-plugins
  - follow-create-web-mcp
  - deep-review-codebase
  - follow-lib-unocss
  - follow-design-system
  - follow-web-standard
  - follow-service-cloudflare
  - follow-tool-devfra
  - run-dev

---
## Goal

Choose the right web project type and hand the work off to the correct skill

## Scope

- Take the requirements and classify the web project: landing, saas, paas
- Delegate project creation to the appropriate skill
- Never implement the project directly yourself
- Add WebMCP tools to an existing site (page-provided agent tools) → `/follow-create-web-mcp`
- Layout/flow still unproven → prototype first: `/design-web-prototype` (multi-route, production-quality SolidJS) or `/design-html-prototype` (single-file quick mockup), then create the real project here

### Framework Skills

| Framework | Skill |
|---|---|
| Next.js | `/follow-create-web-nextjs` |
| Nuxt | `/follow-create-web-nuxt` |
| SvelteKit | `/follow-create-web-svelte` |
| SolidStart | `/follow-create-web-solidstart` |
| TanStack Start (Solid) | `/follow-solid-framework` |
| Docs site (single-page README+docs, Comark Vue → CF Workers) | `/follow-create-web-docs` |

- Default toolchain: `vite` (Rolldown-powered since v8) — always confirm the latest version with `/deep-research` + `/follow-best-practice` (never pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Gather Requirements

> Goal: understand the web project

1. Collect the project name, target users, and feature list
2. Identify the required integrations: auth, payments, dashboard, CMS, analytics
3. Determine SSR, SPA, or full-stack
4. If the user is unsure what kind of web project they want → ask before proceeding
5. Run `/deep-research` + `/follow-best-practice` to confirm the latest framework/toolchain versions before choosing a stack

### 2. Choose Web Type

> Goal: choose the web type

1. Static informational content → build a landing page following this skill's flow
2. Services + pricing + auth + dashboard → build a SaaS following this skill's flow
3. SaaS plus advanced UI/UX → build a PaaS/advanced app following this skill's flow
4. If a Rust TUI is required → run `/follow-create-tui-ratatui`
5. If the stack is unclear → use the default `/follow-solid-framework`

### 3. Delegate And Validate

> Goal: hand off the work and verify it

1. Invoke the chosen skill with the recorded requirements
2. Verify the skill completed everything in its expected outcome
3. Run `### 4. Robots Before Deploy` to set `robots.txt` according to site status
4. Run `/deep-validate` if there are complex flows

### 4. Robots Before Deploy (merged from `/follow-robots-txt`)

> Goal: set `robots.txt` correctly and safely for the site's status

1. Check current state: does `robots.txt` exist; is the site public or protected (Cloudflare Access, basic auth, login)
2. Decide the policy:

| Site status | robots.txt |
|---|---|
| Public, wants SEO | `User-agent: *` + empty `Disallow:` + `Sitemap: <url>` |
| Public, not ready to index | `User-agent: *` + `Disallow: /` + `<meta name="robots" content="noindex,nofollow">` in the SSR `<head>` |
| Behind Access / basic auth / login | `User-agent: *` + `Disallow: /` |
| Mixed public/private pages | `Disallow:` only the private paths |

3. Place the file by framework: Vite/SolidStart/TanStack Start/Next.js/Astro → `public/robots.txt`; SvelteKit → `static/robots.txt` — one file only, never split
4. Verify: after build the file is in the output dir; check `http://localhost:<port>/robots.txt` locally; `curl /robots.txt` after deploy
5. Never hardcode secrets or internal paths in `robots.txt`; re-check it after every build/deploy

## Rules

### 1. Stack Defaults

- If the user specifies no stack → use SolidJS + TanStack + oRPC + Elysia + UnoCSS for saas/paas, and SolidJS + TanStack + UnoCSS for landing
- If the user specifies another stack → follow that stack

### 2. Quality

- Run `/follow-single-responsibility` after creating major components
- Run `/deep-review-codebase` and `/deep-review-codebase` for SEO/bundle
- Run `/deep-review-codebase` before deploy
- Run `/implement-to-production` after the website is finished

### 3. Safety

- Never commit secrets into the repository
- Use `/follow-secret-manager` for API keys, DB URLs, and secrets
- Use `environment variables` for non-sensitive config
- If there are destructive changes → dry run first

### 4. Route Structure

- Structure `src/routes/` to mirror real URLs — a folder = a path segment (`settings/` → `/settings/*`, `business/$id.tsx` → `/business/:id`)
- Use `(group)` only when it is a pathless layout/guard boundary carrying a `route.tsx` shared by several routes (e.g. `(authed)` wrapping login-required routes) — 1 group = 1 layout boundary
- Never use `(group)` just to organize files without a `route.tsx` — if there is no shared layout, flatten the folders to match the URL

### 5. Formatting

- Do not use `**` (bold markers)
- Use backticks for paths, commands, and skill names
- Report with `/report`

- Use /deep-review-codebase if needed
- Use /deep-review-codebase if needed
- Use /follow-lib-unocss if needed
- Use /follow-design-system if needed
- Use /deep-review-codebase if needed
- Use /follow-service-cloudflare if deploying on Cloudflare
- Use /run-dev if needed
- Use /follow-create-plugins if needed
- Use /follow-create-web-mcp if needed
- Use /follow-web-standard when implementing UI markup/widgets — semantic HTML, native form validation, standard Web APIs before libraries
- Use /follow-tool-devfra if the site needs devtools (inspector/analyzer)
- Use /deep-test component for component tests and /deep-test e2e for user flows

## Expected Outcome

- Web type chosen according to the requirements
- Project created by the appropriate skill
- Type safety between client and server
- Tests passing, or a clear plan for them
- Ready to deploy, or already deployed successfully
