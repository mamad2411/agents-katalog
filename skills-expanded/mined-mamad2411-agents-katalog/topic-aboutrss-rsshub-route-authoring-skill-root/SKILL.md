---
name: rsshub-route-authoring-skill
description: >-
  Author PR-ready RSSHub routes — namespace.ts, route handler, Radar rules and PR
  description — that survive code review. Distilled from 2,727 route PRs. Use when asked
  to write, fix or review an RSSHub route, add an RSS feed for a website via RSSHub,
  contribute a route to DIYgod/RSSHub, or when working with cheerio selectors,
  cache.tryGet, parseDate, Radar rules, or the RSSHub PR template. Trigger on RSSHub, RSS
  route, RSS feed for X, 给 X 做 RSS 订阅, namespace.ts, DataItem. Do not use for
  deploying RSSHub, debugging runtime errors, tuning cache/config, or non-RSSHub scraping.
license: MIT
compatibility: >-
  Must run inside an RSSHub checkout, which requires Node.js and pnpm 10. An authenticated 
  GitHub CLI (`gh`) is needed to fetch the auto-review rule list and to run the tooling 
  under tools/. Run `npm i` once in this folder for the verification scripts under scripts/.
allowed-tools: "Read Write Edit Glob Grep WebFetch Bash(git:*) Bash(node:*) Bash(npm:*) Bash(pnpm:*) Bash(gh:*)"
metadata:
  version: "1.0.0"
  corpus: "2727 route PRs, collected 2026-09-11"
---

# RSSHub route authoring

Produces route code that can be merged into [DIYgod/RSSHub](https://github.com/DIYgod/RSSHub).

Two rules decide almost everything:

1. **Every defensive construct needs a number.** `.first()`, `.last()`, `.trim()`, `?? ''`,
   a custom `User-Agent`, a fallback date, a pagination parameter — prove it with a count or
   delete it.
2. **Read the project's own rules first.** They supersede anything remembered from training
   data, and they change over time. In this order:
   - `AGENTS.md` in the working directory — the contributor guide, 49 numbered rules
   - `.github/prompts/pr_review_rules.md` in the RSSHub repo — the 26 rules the auto-review
     bot enforces:

     ```bash
     gh api repos/DIYgod/RSSHub/contents/.github/prompts/pr_review_rules.md
     ```

   - <https://docs.rsshub.app/joinus/> — the narrative docs

## Workflow

### 0. Environment

- Work inside an RSSHub checkout (a fork is fine). Nothing here works standalone.
- Install dependencies, then start the dev server on port 1200:
  `pnpm i` followed by `pnpm dev`.
- `pnpm` is the package manager. Install it however suits your platform — `npm i -g pnpm`,
  `brew install pnpm`, `winget install --id pnpm.pnpm`, `scoop install pnpm`, or the standalone
  install script. If your shell cannot execute `pnpm` directly (a common case is a script
  execution policy on Windows PowerShell), invoke the binary by its full name instead —
  `pnpm.cmd` on Windows.
- Verify the toolchain before writing code: an incomplete install surfaces as an unrelated
  `Cannot find module …` during typecheck and blocks every commit.

### 1. Load the rules

- `AGENTS.md` in the working directory — it is the authoritative rule set
- <https://docs.rsshub.app/joinus/> — the narrative docs
- The auto-review bot's own rule list lives at `.github/prompts/pr_review_rules.md` in the
  RSSHub repo — fetch it when you need authoritative wording:

  ```bash
  gh api repos/DIYgod/RSSHub/contents/.github/prompts/pr_review_rules.md
  ```

  It currently holds 26 rules and **its numbering changes over time**, so match rules by
  substance rather than by number.
- If `docs.rsshub.app` is unreachable from your environment, fetch the Markdown source from
  the docs repository with `gh api` instead of the rendered site

### 2. Confirm the route does not already exist

Search `lib/routes/` for the domain before writing anything. If a namespace exists, add to it
rather than creating a variant.

### 3. Analyse the source

- Prefer an API over HTML; prefer HTML over Puppeteer.
- Confirm the page is server-rendered before reaching for a browser.
- Fetch the **first page only** — never expose pagination parameters, and never add a custom
  `limit` (RSSHub has a built-in one).
- Decode non-UTF-8 responses (`iconv-lite` for GBK and similar).
- Check for a structured payload before parsing markup: `__NEXT_DATA__` / `__NUXT__`,
  `application/ld+json`, or a WordPress REST API at `/wp-json/wp/v2/…`.
- Check whether the site already publishes an equivalent feed. If it does, say so before
  writing the route — see `references/anti-patterns.md` §0.

### 4. Write `namespace.ts` and the route file

```ts
import type { Namespace } from '@/types';

export const namespace: Namespace = {
    name: '<site display name>',
    url: 'www.example.com', // no protocol
    lang: '<language code>', // e.g. en, ja, zh-CN
};
```

```ts
import type { Data, Route } from '@/types';
import ofetch from '@/utils/ofetch';

export const route: Route = {
    path: '/<route>/:param?',
    categories: ['<one category>'],
    example: '/<namespace>/<route>/<concrete-value>',
    name: '<route name — must not repeat the namespace name>',
    maintainers: ['<your github handle>'],
    radar: [{ source: ['www.example.com/<path>'], target: '/<route>' }],
    handler,
};

async function handler(): Promise<Data> {
    // …
}
```

A namespace directory without `namespace.ts` is not registered at all — it is mandatory.

### 5. Build items

- Absolute links: `new URL(href, baseUrl).href`
- Wrap detail fetches in `cache.tryGet`, caching **the whole returned object**
- `pubDate` via `parseDate`, normalised with `timezone(…, <utc offset>)` when the source omits
  timezone information; never `new Date()`; never an event time (an exhibition opening, a
  match kickoff) used as the publish time
- `description` holds body content only — no duplicated title/author/date, `<br>` not `\n`
- Build markup with JSX + `renderToString`; embed source HTML with `raw()` from `hono/html`;
  never `dangerouslySetInnerHTML`

### 6. Radar

Inline in `Route['radar']` — never a separate `radar.ts`. `source` has no protocol and keeps
the same subdomain as the namespace `url`; `target` matches the route path and omits
parameters the source URL does not contain.

### 7. Verify with evidence

This is the step that gets skipped, and it is the one that causes the most review churn. Run
`scripts/verify-selectors.mjs` against the real page and record:

- how many elements each selector matches per item → justifies or kills `.first()` / `.last()`
- how many items have padded text → justifies or kills `.trim()`
- that every link is absolute and unique

Then run `scripts/pre-submit-check.mjs`, and confirm the feed renders at
`http://localhost:1200<example>`.

### 8. Submit

Commit as `feat(route): …`, push, and open the PR by passing the body as a file:

```bash
gh pr create --title "feat(route): add <site> <what> route" --body-file /tmp/pr-body.md
```

Never let the description travel through a rendered view — the template contains a `routes`
fence that collides with any fence wrapped around it, and the result is broken markdown. The
title is checked by CI and must be lower-case conventional-commit form; `Feat:` and
`feat:add …` both fail it. Check both before opening the PR:

```bash
node scripts/pre-submit-check.mjs --title "feat(route): add <site> <what> route"
```

**Before using `references/pr-template.md`, compare it with the template GitHub injects into
the new PR form** — the official template changes over time, and the injected one is
authoritative. See `references/pr-template.md` for the title rules and the four-backtick
fallback when a human has to copy the body by hand.

Opening the PR starts the automated phase; it does not end your work. Continue with step 9.

### 9. Finish the automated phase

This phase is entirely mechanical, so run it yourself rather than handing back to the user:

1. Wait for the checks, then read them:

   ```bash
   gh pr checks
   gh pr view --comments
   ```

2. Fix whatever they report: a `Failed ❌` against any path in the `routes` block, or a rule
   cited by the auto-review pass.
3. Commit as a **new commit** — never amend once a review exists — and push again.
4. Repeat.

**How to tell you are done — and why you must then stop pushing — is in
`references/review-response.md`. Read it there.** Do not improvise a test for "clean": the
bot's wording has changed more than once and the details matter.

**Guardrail: cap the loop and then ask the user.** Three fix-and-push cycles is a reasonable
default. If the bot is still citing a rule by then, you are guessing rather than fixing, and
each further push re-runs the entire suite and buries the maintainer's own notifications —
which is precisely what the milestone rule exists to prevent.

A clean automated pass is not a review. Waiting for a maintainer happens on their schedule, so
that is where a single session ends. Cleaning up once the PR is settled — deleting the branch,
keeping the fork — is also in `references/review-response.md`.

## Before committing

Walk the pre-submit checklist in `references/anti-patterns.md`, and check
`references/engineering-traps.md` for LF line endings, TypeScript annotations, and branch
setup.

## After the PR: feedback (opt-in only)

This skill is built from real review feedback, so new feedback is genuinely useful. But:

> **Never file anything without asking the user first.** Do not open issues, do not open pull
> requests, do not query this repository's issues, and do not make network calls on the user's
> behalf unless they explicitly ask you to.

**Offer feedback at two points only — and never in between.**

1. **When the automated phase ends.** Only if the auto-review bot cited something that is
   *absent from the rule catalogue* in `references/anti-patterns.md`. A finding the skill
   already documents is the catalogue working as intended, not a gap — asking about it
   interrupts a phase you are meant to finish unaided.
2. **Once the PR is settled** — merged or closed. By then a maintainer may have raised
   something, and human feedback is the highest-value signal this skill gets. Reread
   `gh pr view --comments` first; the interesting comments are the human ones, not the bot's.

Do not offer feedback while the automated loop is still running. Finish it first.

When you do offer it, the choice is: write it to a local file (e.g.
`observations/<date>-<topic>.md`), report it upstream, or skip it. Only report if they pick
that, and say first that the issue will be public and filed under **their** GitHub account.

For how to report — templates, whether it clears the evidence threshold, and what happens to
your issue afterwards — follow `CONTRIBUTING.md`. That file owns the procedure; do not restate
it. Never edit `references/anti-patterns.md` directly.

## References

- `references/anti-patterns.md` — 1,987-PR corpus: what gets flagged, with counts
- `references/review-response.md` — CI checks, decoding comments, answer templates, after the
  PR is settled
- `references/engineering-traps.md` — line endings, TS annotations, branch setup
- `references/examples.md` — copy-paste templates for the API / HTML / Puppeteer strategies
- `references/pr-template.md` — PR template and how to fill it (verify before use)
- `tools/` — the pipeline that produced the corpus; for skill maintainers, not for agents
