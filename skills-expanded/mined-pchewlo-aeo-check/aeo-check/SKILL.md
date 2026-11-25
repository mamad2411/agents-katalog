---
name: aeo-check
description: Run aeo-check on a website's code (or a live URL) to find answer engine optimisation problems that stop ChatGPT, Claude, Perplexity, Gemini and Google AI Overviews from crawling, understanding, citing or buying from the site, then fix them. Use when asked to check or improve AEO, GEO, AI search visibility, llms.txt, robots.txt for AI crawlers, structured data, or agent readiness.
---

# aeo-check

aeo-check scans HTML, JSX/TSX, Vue, Svelte, Astro and Markdown plus robots.txt, sitemap.xml and llms.txt, and reports findings with a file, line, rule id, severity, reason and fix.

## 1. Run it

From the root of the site's repository:

```sh
npx --yes github:pchewlo/aeo-check --format json > /tmp/aeo.json
```

If aeo-check is installed in the project, `npx aeo-check --format json` works too. Other useful forms:

- `aeo-check <dir>` to check a sub-folder such as `site/` or `apps/web`
- `aeo-check https://example.com --max-pages 20` to check a deployed site as a crawler sees it (no JavaScript); use this to confirm fixes on a preview URL
- `aeo-check --since origin/main` to report only files changed on the branch
- `aeo-check --list-rules` to see every rule
- `--ai` adds judgement checks with Claude (needs `ANTHROPIC_API_KEY`); leave it off unless the user asks

Exit code 1 means findings at or above `--fail-on` (default `error`); 2 means a usage error.

## 2. Read the report

The JSON has `overall` (0-100), `counts`, `site.findings` (robots.txt, sitemap, llms.txt, host headers), `files` (components and scripts) and `pages` (each with `route`, `score` and `findings`). Each finding has `ruleId`, `severity`, `file`, `line`, `message`, `why` and `fix`.

Work in this order:

1. Errors in the `crawl` category (robots blocks, noindex, client-only content, hash routing). Nothing else matters until crawlers can fetch the text.
2. Other errors (missing titles, invalid JSON-LD, canonical mistakes, unusable Book/Buy buttons).
3. Warnings, page by page, starting with the lowest-scoring pages.
4. Info findings only if the user wants a thorough pass.

## 3. Fix

Apply the `fix` text from each finding, matching the project's framework:

- Next.js app router: `export const metadata` (title, description, `alternates.canonical`, `openGraph`, `robots`) per page; `metadataBase` in the root layout; `app/robots.ts`, `app/sitemap.ts`; JSON-LD in a `<script type="application/ld+json">` rendered by a Server Component.
- Static HTML: edit `<head>` directly; put robots.txt, sitemap.xml and llms.txt at the web root (`public/` in most frameworks).
- Client-only content: move data fetching to the server (Server Components, `getStaticProps`, Astro/SvelteKit `load`, prerendering). Do not paper over it with a `<noscript>` copy.
- Hash routing: switch to the History API router of the framework in use.
- llms.txt: follow https://llmstxt.org: `# Site name`, `> summary`, then `## Section` lists of `- [Page](absolute URL): what it covers`.

Rules for the agent doing the fixing:

- Do not invent facts. Author names, publication dates, prices, cancellation terms, statistics and their sources must come from the user or the existing content. If they are missing, list them as questions for the user instead of making them up.
- Ask before removing a `noindex`, a robots.txt block or an X-Robots-Tag header: some sites are private on purpose.
- Keep JSON-LD consistent with the visible page; never mark up content that is not shown.
- Keep copy changes minimal and in the site's existing voice. Rewrites for `answer-first`, `self-contained-passages` and `question-headings` should keep the meaning and only move the answer to the front or name the subject.

## 4. Verify

Re-run aeo-check and compare `overall` and `counts` with the first run. Report to the user: what was fixed, the before and after scores, and anything left that needs their input (facts, deliberate noindex, content to expand or delete).
