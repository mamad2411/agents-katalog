---
name: publish-results
description: Required after any benchmark run that changes a public number, before any release PR merges, and for any edit to the README benchmark section, docs/compare.md or the website. It carries one result to every place a reader sees it, the README, docs, comparison, website, FAQ data and report, so no page is left stale. CI enforces it through tests/claims.test.mts.
---

# Publish results everywhere

A result is not delivered until every reader sees the same numbers. One stale page makes the whole project look careless. This skill lists every place a result lives. `tests/claims.test.mts` fails CI when a page drifts from the rows or carries a stale claim, so a forgotten page cannot merge.

## When to run it

- A benchmark run changes a number you publish: a cost, a pass count, a ratio, a competitor's result.
- A release PR is about to merge.
- A change alters what the docs promise: a default, a review rule, a model choice.

## 1. Update the source of truth

`bench/results/headline.json` holds every public number, the rows it comes from, the pages that must show it, and the stale phrases that must not appear.

- Point each entry at the committed rows and the arm, and set `shown` to the value the pages print.
- Add every new page that shows a number to `surfaces`.
- When a claim stops being true, add its old wording to `banned`.

Run `node --test tests/claims.test.mts`. It recomputes each number from the rows, so a typo or a stale total fails here.

## 2. Update every surface

Change all of them in the same PR. Never one now and the rest later.

| Surface | What to update |
|---|---|
| `README.md` | The table cell under the banner, the `## Benchmarks` tables, "Where AutoMode does not win", the `## How it compares` paragraph and any review or model claim |
| `docs/compare.md` | The feature table's cost row, "Measured on the same sessions", "Where the others are ahead" and the switch section |
| `site/app/(home)/page.tsx` | `RESULTS` (the chart widths come from it), the stat cards, `#fit`, the FAQ list, which also feeds the FAQ schema that search engines and AI assistants read |
| `site/content/docs/benchmarks/results.mdx`, `site/content/docs/compare.mdx` | The tables, "Where AutoMode does not win" and the byline dates |
| `site/content/docs/guides/*.mdx`, `faq.mdx`, `concepts/prompt-cache.mdx` | Any number, and any claim about reviews or models. The calculator's per-step costs live in `site/components/calculator.tsx` |
| `bench/experiments/<report>.md` | The results section, the fixes and the limits |
| `marketing/posts/*.md` | Every post that is not `sent`. `tests/marketing.test.mts` fails on a number that left the README or `headline.json` |
| `CHANGELOG.md` | A line under `[Unreleased]` when the shipped behavior changed |

## 3. Keep it honest

- Every number comes from committed rows in `bench/results/`. Never round in AutoMode's favor, and never invent a competitor result. Use our own run, or the project's published result, cited as theirs.
- Lead with the most common usage: mixed sessions, and people who run Opus.
- Keep the "where it does not win" section. A claim without its limit is marketing, not evidence.
- Meta descriptions stay between 100 and 165 characters (`tests/site.test.mts`).

## 4. Check, then verify live

```bash
node --test tests/claims.test.mts tests/site.test.mts
git ls-files '*.md' '*.html' | xargs grep -nE "<an old number or claim>"
```

- Build the site (`npm run build` in `site/`), serve `site/out/` under `/AutoMode/`, and look at it at desktop and phone widths. The site is dark only.
- After the merge, wait for the `pages` workflow, then fetch the live site and confirm it shows the new numbers: `curl -s https://mralexivy.github.io/AutoMode/ | grep '<a new number>'`.

Then follow `ship-change` for the issue, branch and PR.
