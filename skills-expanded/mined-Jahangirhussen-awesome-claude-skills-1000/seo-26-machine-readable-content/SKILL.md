---
name: seo-26-machine-readable-content
description: Machine-readable content (SEO). Use when the request involves: machine readable. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Machine-readable content

ID: 26.02 | Level: child | Parent: [AI Agent / Agentic SEO](../SKILL.md)

## Purpose
Machine-readable content within the seo-master tree: Markup review.

## When to use
Triggers: machine readable

## When NOT to use
- The topic is covered by a sibling skill: `../agent-accessibility`, `../agent-discoverability`, `../structured-content`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: OpenAPI tools, schema validator, Lighthouse accessibility, robots.txt, MCP/API docs.

## Core workflow
1. JSON-LD for entities and actions
2. Semantic HTML5 landmarks
3. Consistent data attributes

## Decision rules and checks
- Semantic HTML
- JSON-LD for entities and actions

## Edge cases and failure handling
- Content in images only -> add text

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Markup review. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Content in images only
- Action: add text
- Output: Markup review.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
