---
name: seo-06-topical-authority
description: Topical authority (SEO). Use when the request involves: topical authority, topic coverage. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Topical authority

ID: 06.02 | Level: child | Parent: [Content SEO](../SKILL.md)

## Purpose
Topical authority within the seo-master tree: Coverage map: topic, status, URL.

## When to use
Triggers: topical authority, topic coverage

## When NOT to use
- The topic is covered by a sibling skill: `../content-clusters`, `../content-gap`, `../content-refresh`, `../content-strategy`, `../seo-copywriting`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console, GA4, Ahrefs/Semrush content gap, SERP analysis, content brief template, CMS.

## Core workflow
1. List the topic universe for your niche (core, subtopics, questions)
2. Cover subtopics with depth and consistent internal linking
3. Compare coverage vs competitors; fill gaps
4. Earn mentions/links to the cluster

## Decision rules and checks
- Map topic universe
- Cover subtopics in depth with internal links
- Measure coverage vs competitors

## Edge cases and failure handling
- Broad shallow coverage -> go deep on fewer topics first
- Clusters without links -> add hub/spoke links

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Coverage map: topic, status, URL. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Broad shallow coverage
- Action: go deep on fewer topics first
- Output: Coverage map: topic, status, URL.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
