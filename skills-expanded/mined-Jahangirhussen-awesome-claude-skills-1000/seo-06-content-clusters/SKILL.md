---
name: seo-06-content-clusters
description: Content clusters (SEO). Use when the request involves: topic cluster, pillar, hub and spoke. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Content clusters

ID: 06.03 | Level: child | Parent: [Content SEO](../SKILL.md)

## Purpose
Content clusters within the seo-master tree: Cluster diagram: pillar, spokes, anchors.

## When to use
Triggers: topic cluster, pillar, hub and spoke

## When NOT to use
- The topic is covered by a sibling skill: `../content-gap`, `../content-refresh`, `../content-strategy`, `../seo-copywriting`, `../topical-authority`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console, GA4, Ahrefs/Semrush content gap, SERP analysis, content brief template, CMS.

## Core workflow
1. Pick pillar topic with substantial search demand
2. Create supporting posts for subtopics/questions; each targets a distinct intent
3. Link pillar <-> supporting pages both ways with clear anchors
4. Update cluster as new content is added

## Decision rules and checks
- 1 pillar + supporting posts
- Bidirectional internal links
- Avoid cannibalization

## Edge cases and failure handling
- Spokes compete with pillar -> differentiate intent
- Pillar too thin -> expand with summary of each subtopic

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Cluster diagram: pillar, spokes, anchors. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Spokes compete with pillar
- Action: differentiate intent
- Output: Cluster diagram: pillar, spokes, anchors.

## Dependencies (load only if needed)
- pillar-content-architecture (installed skill)

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
