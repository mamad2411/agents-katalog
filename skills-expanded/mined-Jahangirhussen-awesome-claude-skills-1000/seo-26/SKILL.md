---
name: seo-26
description: 26. AI Agent / Agentic SEO (SEO). Use when the request involves: ai agent seo, agentic, llms.txt, webmcp, machine-readable website, agent discoverability. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 26. AI Agent / Agentic SEO

ID: 26 | Level: parent | Parent: SEO Master

## Purpose
Make sites usable by AI agents.

## When to use
Triggers: ai agent seo, agentic, llms.txt, webmcp, machine-readable website, agent discoverability

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: OpenAPI tools, schema validator, Lighthouse accessibility, robots.txt, MCP/API docs.

## Core workflow
1. Offer crawlable pages, sitemap, clean semantic HTML
2. Document APIs (OpenAPI) and make actions discoverable
3. Use labelled forms and stable URLs; avoid CAPTCHA-only flows
4. llms.txt is optional with low proven impact

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Actions need JS-only interactions -> provide accessible fallback

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Agent readiness checklist. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Actions need JS-only interactions
- Action: provide accessible fallback
- Output: Agent readiness checklist.

## Children
- [Agent discoverability](agent-discoverability/SKILL.md)
- [Machine-readable content](machine-readable-content/SKILL.md)
- [Structured content](structured-content/SKILL.md)
- [Agent accessibility](agent-accessibility/SKILL.md)

## Topics handled here (no separate child)
- llms.txt: optional, low proven impact
- WebMCP/API discoverability: documented APIs, OpenAPI, predictable endpoints

## Related installed skills (kept in place; invoke only if needed)
- `mcp-builder`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
