---
name: seo-26-agent-accessibility
description: Agent accessibility (SEO). Use when the request involves: agent accessible forms. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Agent accessibility

ID: 26.04 | Level: child | Parent: [AI Agent / Agentic SEO](../SKILL.md)

## Purpose
Agent accessibility within the seo-master tree: Accessibility review for agents.

## When to use
Triggers: agent accessible forms

## When NOT to use
- The topic is covered by a sibling skill: `../agent-discoverability`, `../machine-readable-content`, `../structured-content`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: OpenAPI tools, schema validator, Lighthouse accessibility, robots.txt, MCP/API docs.

## Core workflow
1. Label inputs; use buttons/links semantically
2. Provide predictable URLs for flows
3. Avoid blocking essential flows with CAPTCHA

## Decision rules and checks
- Labelled forms
- No CAPTCHA-only critical flows
- Stable URLs for actions

## Edge cases and failure handling
- Anti-bot walls -> allow documented API instead

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Accessibility review for agents. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Anti-bot walls
- Action: allow documented API instead
- Output: Accessibility review for agents.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
