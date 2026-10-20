---
name: base-config
description: Use when the user asks about the base plugin setup, the OpenRouter spend toolbar, or how their omp plugins/configuration are wired. Documents what the base plugin installs and how to customize it.
---

# Base plugin

This plugin ships your standard omp setup so a fresh machine needs no
reconfiguration.

## What it installs

- **OpenRouter spend toolbar** — status-bar entry showing this month's
  OpenRouter spend and remaining credits. Refreshes every 10 minutes; run
  `/openrouter` to force a refresh. Requires `OPENROUTER_API_KEY` in your
  environment. The "this month" figure is the key's `usage_monthly`
  (reset-window) number from `/api/v1/key`; lifetime totals from
  `/api/v1/credits` are the fallback.
- **Skills** — 79 vendored skills: the `golang-*` set
  (samber/cc-skills-golang), the mattpocock/skills engineering set,
  `test-roadmap` (Ovid/paad), `vercel-composition-patterns`,
  `vercel-react-best-practices`, `agent-browser`, `frontend-design`,
  `hallmark`, `beads`, plus this file.
- **MCP servers** — declared in `.mcp.json` at the plugin root.
- **Rules** — `rules/` at the plugin root; always-apply rules injected into
  every session. `grilling-via-ask` forces grilling rounds through the `ask`
  tool: 3 options per question, exactly one `recommended`.
- **Auto-setup** — installs missing required plugins (`@kryoz/caveman-plugin`,
  `@dietrichgebert/ponytail`, `@hypabolic/pi-hypa`) in the background on
  session start; restart or `/reload-plugins` activates them.
- **`/base-doctor`** — run it to verify envs (`OPENROUTER_API_KEY`), required
  plugins, the `hypa` binary, bundled skills, and OpenRouter API.

## Customizing

- Refresh interval: edit `REFRESH_MS` in `extensions/openrouter-usage.js`.
- Add an MCP server: edit `.mcp.json` in the plugin root, then run
  `/mcp reload`.
- Add a skill: add `skills/<name>/SKILL.md`.
