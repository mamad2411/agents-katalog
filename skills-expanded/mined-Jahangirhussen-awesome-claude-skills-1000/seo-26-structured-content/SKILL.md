---
name: seo-26-structured-content
description: Structured content (SEO). Use when the request involves: structured content. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Structured content

ID: 26.03 | Level: child | Parent: [AI Agent / Agentic SEO](../SKILL.md)

## Purpose
Structured content within the seo-master tree: Structure review.

## When to use
Triggers: structured content

## When NOT to use
- The topic is covered by a sibling skill: `../agent-accessibility`, `../agent-discoverability`, `../machine-readable-content`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: OpenAPI tools, schema validator, Lighthouse accessibility, robots.txt, MCP/API docs.

## Core workflow
1. Tables, lists, definitions with stable anchors
2. Consistent heading hierarchy
3. Avoid decorative-only structure

## Decision rules and checks
- Tables, lists, definitions
- Stable headings/anchors

## Edge cases and failure handling
- Layout tables -> use CSS

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Structure review. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Layout tables
- Action: use CSS
- Output: Structure review.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
