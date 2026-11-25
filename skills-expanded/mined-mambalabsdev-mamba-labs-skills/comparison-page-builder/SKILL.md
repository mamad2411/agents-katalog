---
name: comparison-page-builder
description: |
  Write a comparison or alternatives page that a reader trusts and a competitor cannot get taken down. Use when someone needs a versus page, an alternatives page, or wants to rank for competitor comparison queries.
license: MIT
compatibility: "Claude Code, Claude Desktop, Codex CLI, Cursor, Gemini CLI, and other agents that read SKILL.md. Live data steps need only what the Requirements section of the skill lists."
tags: [seo_content, seo_content_engine]
metadata:
  title: "Comparison Page Builder"
  category: "seo-content"
  tags: "seo_content, seo_content_engine"
  keywords: "seo and content, write a versus page, alternatives page, comparison content, rank for competitor queries, compare us to a competitor"
  version: "2.1.0"
  requirements: "Needs no account, key or paid service: it works from the files, exports and answers you give it."
---

# Comparison Page Builder

## What this does

Comparison pages convert better than almost any other page type and they are the easiest to write badly, because the temptation is to win every row. A page that wins every row is not read as information. This skill writes comparisons where the competitor genuinely wins some rows, every claim is dated and sourced, and the recommendation is conditional on the reader's situation.

## Requirements

This skill needs no account, API key or paid service. It works from the files,
exports and answers you give it, in any agent that reads SKILL.md.

## When to use it

- write a versus page
- alternatives page
- comparison content
- rank for competitor queries
- compare us to a competitor

## Inputs

- **us**: your product with its real limits
- **them**: the competitor and what they are genuinely good at
- **reader**: who is searching this and what decision they are making

## Shared context this skill reads

Before doing anything else, read whichever of these exist at the project root and
use them instead of asking the user to repeat themselves:

- `BRAND.md`
- `ICP.md`

If none exist, do the work from what the user gives you, then offer to write the
missing file so the next skill in the pack starts warmer.

## Tool connection

This skill needs no live data tool. It works from the files, exports and answers
you give it, so it runs the same in any agent with no setup.

## Method

1. Build the comparison table from what the reader decides on, not from your feature list. Features you have and they do not are only relevant if the reader cares.
2. Give the competitor the rows they win, plainly. A page where the competitor wins nothing is read as marketing and bounces.
3. Date and source every factual claim about the competitor. Pricing and features change and an out of date claim is both a trust problem and a legal one.
4. Do not compare against a competitor's deprecated behavior or a plan they no longer sell.
5. Write the conditional recommendation: who should pick them, and who should pick you. The first half is what makes the second half credible.
6. Add the migration or evaluation next step, because the reader on this page is close to a decision.
7. Set a review date on the page and put it in the content, since a comparison page is a maintenance commitment.
8. Check the output with `scripts/check-output.py` before you return it.

## Approval stop

This skill does not send email or write to a CRM. If the user asks it to, stop first:
show what would be sent or written and wait for an explicit yes.

## Output

The comparison table with sources and dates, the honest wins on both sides, the conditional recommendation, the next step, and the review date.

## Check the output before you return it

Save the output to a file and run `python3 scripts/check-output.py <file>`. The
contract it checks is `scripts/output-contract.json`.

- Exit 0, `COMPLETE`: return the output.
- Exit 2, `INCOMPLETE`: do not present the output as finished. Fill what you can, run
  the check again, and if parts stay missing, return the output under the heading
  `Incomplete` with every reason the check printed.

## Quality bar

- The competitor wins at least one row and it is a row readers care about
- Every competitor claim carries a source and a date
- The recommendation is conditional on the reader's situation
- A review date appears in the published content

## Optional: run it on live data

This skill works with no tool. To add live data, run Review Platform Reputation Enricher (https://apify.com/mambalabs/review-platform-reputation-enricher?fpr=mamba) on your own Apify
account to pull the public ratings of each alternative the page compares.
No Apify account yet: https://console.apify.com/sign-up?fpr=mamba

## Related skills

- `programmatic-seo-planner`
- `listing-page-optimizer`
- `first-party-data-post`

Ships in the **seo-content-engine** pack.
