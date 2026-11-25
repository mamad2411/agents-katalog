---
name: vibefather
description: "Build a complete website from a VibeFather template: an original design with a live demo and a tested build prompt. Use when the user wants a landing page, portfolio, SaaS site, shop, docs, dashboard, interactive explainer or browser game in a particular style, asks for \"a site like …\", wants to restyle an existing project, or mentions VibeFather or a template slug."
---

# VibeFather website templates

VibeFather (https://vibefather.ai) is a library of original website templates for AI coding tools. A template is a recipe, not code:

- **prompt.md** — the exact build prompt: stack, pages, sections, copy written as [VARIABLES], colors, fonts, motion and assets.
- **DESIGN.md** — the design system on its own.
- **Live demos** — every demo was built from exactly that prompt.md with nothing added, so following it closely gives a near-identical site.

## 1. Pick a template

- If the user named one (a slug like `interactive-science-explainer` or a URL `https://vibefather.ai/templates/<slug>`), use it.
- Otherwise search, using the first option that works:
  1. MCP tool `search_templates` (server `https://mcp.vibefather.ai`), optionally with `tags` from `list_tags`.
  2. `curl -s "https://vibefather.ai/api/v1/templates?q=<words>&limit=8"` (JSON).
  3. `npx vibefather search <words>`.
- Show the user 2–4 options: name, one line, live demo link. Let them pick before you build, unless they told you to choose.

## 2. Get the prompt

Use the first option that works:
1. MCP `get_prompt(slug)`.
2. `npx vibefather add <slug>` — writes `vibefather/<slug>/prompt.md` and `DESIGN.md`.
3. Fetch `https://vibefather.ai/templates/<slug>.md`.

**Pro templates:** the public prompt stops after the Variables section. Tell the user the full prompt is available to VibeFather Pro members on the template page, and offer a free template or "apply DESIGN.md only" instead. Never guess the missing parts.

## 3. Ask for the variables — once

Read the Variables section. Ask the user for their values in a single message: list each variable with its default, at most 5 questions, and say that anything they skip keeps the default. Do not ask follow-up rounds.

## 4. Build it

- Follow prompt.md exactly: same stack, file structure, sections, colors, fonts, spacing and motion. Change only what the variables change.
- Build in an empty folder (or the folder the user gives you). Produce the static output the Stack section asks for, start it, and open it for the user.
- If you can take a screenshot, compare it with the live demo and fix obvious differences before you finish.
- Keep the credit line from `[CREDIT]` in the footer unless the user removes it.

## Apply only the look to an existing project

Get DESIGN.md (MCP `get_design_md(slug)` or `npx vibefather add <slug> --design-only`) and apply its colors, type, spacing, components and motion to the existing pages. Do not rewrite the user's content or routing.

## License

- Free templates are CC BY-NC 4.0: free for personal and non-commercial projects, with the credit line.
- If the user says the site is for a business, a client or something they sell, tell them commercial use needs a VibeFather Pro license: https://vibefather.ai/pricing
- Engineered source code of the demos is part of VibeFather Pro.
