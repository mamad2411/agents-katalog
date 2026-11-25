---
name: seo-26-agent-discoverability
description: Agent discoverability (SEO). Use when the request involves: agent discoverability, llms.txt. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Agent discoverability

ID: 26.01 | Level: child | Parent: [AI Agent / Agentic SEO](../SKILL.md)

## Purpose
Agent discoverability within the seo-master tree: Discoverability checklist.

## When to use
Triggers: agent discoverability, llms.txt

## When NOT to use
- The topic is covered by a sibling skill: `../agent-accessibility`, `../machine-readable-content`, `../structured-content`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: OpenAPI tools, schema validator, Lighthouse accessibility, robots.txt, MCP/API docs.

## Core workflow
1. Publish sitemap and clear nav
2. Optional llms.txt pointing to docs
3. Link to API docs

## Decision rules and checks
- Crawlable pages, sitemap
- llms.txt optional
- Clear docs/API pointers

## Edge cases and failure handling
- Hidden docs -> publicly link

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Discoverability checklist. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Hidden docs
- Action: publicly link
- Output: Discoverability checklist.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
