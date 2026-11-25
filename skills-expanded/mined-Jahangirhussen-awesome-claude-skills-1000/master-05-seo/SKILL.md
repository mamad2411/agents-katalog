---
name: master-05-seo
description: 05-SEO domain of the master skills library (all SEO, GEO and AEO work). Use when the task needs any search-visibility work (always via seo-master) and no more specific installed skill matches. Not when the work is paid advertising or non-search marketing.
---

# 05-SEO

## Purpose
Index for all SEO, GEO and AEO work: imported skills (read in place) and a pointer to the installed skills in this domain.

## When to use
The task needs any search-visibility work (always via seo-master).

## When NOT to use
- The work is paid advertising or non-search marketing.
- Another domain fits better (see `../ROUTER.md`).

## Inputs
The task, project context, and constraints; domain is inferred by the orchestrator.

## Core workflow
1. Check the imported skills below; if one fits, open its `SKILL.md` and follow it.
2. Otherwise open `INSTALLED.md` in this folder (installed skills per subdomain) and invoke the matching skill with the Skill tool.
3. For cross-domain needs follow `../DEPENDENCIES.md` instead of duplicating instructions.
4. Execute, verify, report.

## Decision rules
- Prefer the most specific skill; prefer installed canonical skills over imported generic ones.
- Open one skill at a time; do not read the whole folder.

## Edge cases and failure handling
- No fitting skill -> use general capability and say no adequate skill exists; do not invent one.
- Imported skill depends on an unavailable external service -> use the nearest installed alternative.

## Validation
Check the chosen skill's instructions match the task and that its output is verified with the matching testing/validation approach.

## Output requirements
The task result as a short `DONE`; no routing narration.

## Example
Request in this domain -> orchestrator selects the skill from the list below or `INSTALLED.md` -> follow its steps -> verify -> report.



## Related skills
`../ROUTER.md`, `../DEPENDENCIES.md`, `../RULES.md`, `INSTALLED.md`.

## seo-master parents
01 core, 02 google, 03 technical, 04 on-page, 05 off-page, 06 content, 07 local, 08 ecommerce, 09 woocommerce, 10 shopify, 11 wordpress, 12 saas, 13 erp, 14 pos, 15 programmatic, 16 image, 17 video, 18 international, 19 ai-seo, 20 geo, 21 aeo, 22 chatgpt, 23 claude, 24 gemini, 25 perplexity, 26 agentic, 27 schema, 28 analytics, 29 tools, 30 audit, 31 migration, 32 monitoring, 33 automation. Router: `~/.claude/skills/seo-master/ROUTER.md`.
