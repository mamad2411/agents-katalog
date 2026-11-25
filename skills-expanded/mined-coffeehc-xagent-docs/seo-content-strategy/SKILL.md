---
name: seo-content-strategy
description: Use when planning, drafting, reviewing, or improving SEO content strategy, keyword clusters, search intent mapping, content briefs, article outlines, on-page content, metadata, internal linking, topic authority plans, or content refresh recommendations. Prefer this Skill when the task needs intent, audience value, structure, evidence, and conversion alignment. Do not use for scraping, ranking guarantees, or black-hat SEO.
meta:
  version: 1
  display_name: SEO 内容策略
---

# SEO Content Strategy

## Purpose

Create useful search-oriented content plans that map intent, topic coverage, reader value, source needs, and conversion goals without promising rankings.

## Use When

Use for:

- keyword or topic clustering
- search intent analysis
- SEO content briefs
- article outlines
- blog/article SEO metadata and search-intent handoff when paired with `blog-writing-workflow`
- metadata drafts
- content refresh plans
- internal link suggestions
- topic authority roadmaps

## Material Gate

Identify:

- target audience, market, product, topic, and conversion goal
- keyword ideas or source material provided by the user
- search intent, funnel stage, and competitor examples if available
- expertise, evidence, or original data required for credibility

If live SERP or keyword volume is not available, label suggestions as strategy draft, not measured SEO data.

## Workflow

1. Clarify target reader and intent.
2. Group topics by problem, stage, and content type.
3. Define the content promise and reader outcome.
4. Create a brief with angle, outline, questions to answer, evidence needs, internal links, CTA, and metadata.
5. Distinguish educational, comparison, transactional, and support content.
6. Recommend refresh or consolidation when content overlaps.
7. Use `blog-writing-workflow` when the user wants the actual blog/article draft or publishing package.
8. Use `html-report-builder` for content audits, topic maps, or SEO plans.

## Checks

- Content serves a real reader need, not only keywords.
- Search intent matches format and CTA.
- Claims require evidence or firsthand expertise.
- No ranking, traffic, or revenue guarantee is made.
- Metadata is accurate and not clickbait.
- SEO suggestions are labeled as strategy when live keyword/SERP data is unavailable.
- Any source-needing claim is cited or marked as needing evidence.

## Outputs

- SEO content brief
- topic cluster map
- article outline
- metadata draft
- content refresh plan
- internal linking plan
- content audit summary

## Boundary

This Skill owns SEO content planning, intent mapping, brief structure, and content quality review. It does not own live ranking data, scraping, CMS publishing, analytics setup, link building, or search engine guarantees.

It must not run shell, Python, Node, npm, curl, MCP, scraping, SEO tools, CMS, analytics, browser automation, package install, publish, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
