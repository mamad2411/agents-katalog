---
title: "Site Navigation — skill"
description: "Find pages, feeds, and machine-readable resources on mikedemo.dev."
canonical: "https://mikedemo.dev/skills/site-navigation/SKILL.md"
last-updated: "2026-10-03"
---

# Site Navigation

Find your way around mikedemo.dev, the AI project portfolio of Mike "Demo" Demopoulos.

## When to use

Use this skill when you need to locate a page, the sitemap, or the machine-readable entry points of the site.

## Key pages

- `/` — home (level-select hero)
- `/projects/` — all projects (level select index)
- `/projects/<slug>` — project detail page
- `/agent-skills/` — plain-language guide to AI agent skills
- `/claude-code-skills/` — Claude Code skills guide
- `/bugle-crowns/` — the Agentic Football Cup team page
- `/licenses/` — open-source licenses

## Machine-readable entry points

- `/llms.txt` — agent orientation index (start here)
- `/llms.md` — expanded machine-readable reference
- `/api/v1/projects.json` — all projects as JSON
- `/api/v1/projects/<slug>.json` — one project as JSON
- `/openapi.json` — OpenAPI 3.1 spec for the JSON files
- `/sitemap.xml` — every public page
- `/.well-known/ard.json` — agentic resource discovery catalog
- `/.well-known/agent-card.json` — A2A agent card
- `/.well-known/agent-skills/index.json` — this skill index
- `/auth.md` — authentication (none required; everything is public and read-only)
- `/pricing.md` — pricing (everything is free)

## Notes

- Fully static site: no POST endpoints, no chat, no login, no rate limits.
- Markdown twins of key pages are served at `/index.md`, `/auth.md`, `/pricing.md`, `/llms.md`.
