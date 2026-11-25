---
name: super-seo-growth
description: "SEO growth: content optimisation, programmatic SEO, AI/GEO visibility, and ongoing performance improvements. Use after a baseline audit or run a quick check first."
---

# Super SEO Growth

## Overview
Drive organic growth through content quality, programmatic expansion, and AI search visibility.


## User Intent Examples
- "Need help with SEO Content for my product/site."
- "Create a plan for AI/GEO Visibility."
- "Audit or improve Programmatic SEO."

## Capabilities
- Content refresh, topical authority, and keyword coverage
- Programmatic SEO templates and scalable page strategies
- AI/GEO visibility, citation optimisation, crawler policy, and fan-out coverage
- Iteration plan with measurement and cadence

## Routing Map (Modules)
- **SEO Content** -> `references/modules/seo-content.md`
- **AI/GEO Visibility** -> `references/modules/seo-geo.md`
- **Programmatic SEO** -> `references/modules/seo-programmatic.md`

## Default Flow
1. If no recent audit or baseline is unknown, ask for the URL and last audit date.
2. If the request targets AI/GEO or LLM visibility, jump to the GEO module.
3. If the request targets scale via templates, jump to the programmatic module.
4. Otherwise, start with the content module.

## Minimal Intake Questions
Ask only what is missing:
- Primary URL(s)
- Target market/region
- Primary goal (traffic, leads, signups)
- Content scope (blog, landing pages, docs)

## Output Format
- Growth priorities with rationale
- Execution plan (content, programmatic, GEO)
- Measurement plan and cadence
- Risks and dependencies

## Bundled References
- `references/modules/`
- `scripts/`
- `assets/`
- `agents/`

## Compatibility Notes
- If any module references slash commands or tool-specific paths, translate them into plain-language steps.
- Keep outputs platform-agnostic unless the user specifies a specific tool, stack, or agent.

## Guardrails
- Do not invent search data or rankings.
- Tie every action to measurable outcomes.
- Keep recommendations implementable.
