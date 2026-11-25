---
name: aidesigner-frontend
description: >
  AI design engine via MCP. Generates production-ready inline-Tailwind HTML from natural
  language prompts with full repo context awareness (framework, tokens, components, routes).
  Use for UI generation, iteration, and design-system-consistent page creation.
license: UNLICENSED
metadata:
  author: AIDesigner (tyleryin)
  version: "0.1.2"
  mcp_servers:
    - aidesigner
  external_service: true
tags: [design, ui, frontend, mcp, html-generation]
created: 2026-04-04
---

# AIDesigner MCP — Frontend Design Generation

## Overview

AIDesigner is a design engine connected via MCP (HTTP server at `api.aidesigner.ai`).
It reads your entire repo context — framework, Tailwind/CSS tokens, existing components,
routes — and generates production-ready HTML that matches your project's look and feel.

**Why use this instead of writing HTML manually**: The MCP server has full context of your
design system. It produces inline-Tailwind HTML that respects existing tokens, spacing,
and component patterns. Iterate with natural language instead of CSS tweaking.

## MCP Server

- **Type**: HTTP (remote)
- **URL**: `https://api.aidesigner.ai/api/v1/mcp`
- **Auth**: OAuth (browser sign-in via `/mcp` in Claude Code)
- **Config location**: `.mcp.json` in project root (project-level) or `~/.claude.json` (user-level)

## Tools

| Tool | Purpose | Key Params |
|------|---------|------------|
| `generate_design` | Create new HTML/CSS from prompt | `prompt`, `viewport`, `mode`, `url` |
| `refine_design` | Iterate on previous design | `run_id_or_html`, `feedback`, `viewport` |
| `get_credit_status` | Check account balance | (none) |
| `whoami` | Verify auth connection | (none) |

### generate_design Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | yes | Detailed natural-language design description |
| `repo_context` | object | auto | Injected by MCP — never override |
| `viewport` | "desktop" / "mobile" | no | Default: desktop (1440px) |
| `mode` | "none" / "inspire" / "clone" / "enhance" | no | Default: none (pure prompt) |
| `url` | string | no | Reference URL for inspire/clone/enhance modes |

### refine_design Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `run_id_or_html` | string | yes | Previous run ID or full HTML string |
| `feedback` | string | yes | Natural language changes |
| `repo_context` | object | auto | Injected by MCP |
| `viewport` | "desktop" / "mobile" | no | Target viewport |

## When to Use

- **Every UI task**: When user asks for a new page, component, or redesign
- **Iteration**: "Make the hero section more premium", "use our brand colors"
- **Reference-based design**: Clone or get inspired by competitor sites
- **Mobile variants**: Generate desktop first, then refine for mobile viewport

## Workflow

1. **Check credits**: `get_credit_status` (if doing many generations)
2. **Generate**: Call `generate_design` with specific, detailed prompt
3. **Iterate**: Call `refine_design` with feedback on the previous run
4. **Adopt**: Run `npx @aidesigner/agent-skills adopt --id <run-id>` for porting guidance
5. **Port**: Review `.aidesigner/runs/<run-id>/design.html` and integrate into components

## Prompt Best Practices

- Always include "match our existing design system / project styles"
- Be specific: "hero section with gradient background, 48px heading, CTA button" not "make a landing page"
- For mobile: explicitly say "mobile viewport" or set viewport parameter
- Reference existing pages: "match the style of our dashboard page"

## Artifact Storage

Generated designs save to `.aidesigner/runs/{run-id}/`:
- `design.html` — the generated output
- `repo-context.json` — captured project context
- `request.json` — original request
- `summary.json` — generation summary
- `preview.png` — rendered preview

Add to `.gitignore`: `.aidesigner/*`

## Setup

```bash
# One-time init (run in project root)
npx -y @aidesigner/agent-skills init

# Then in Claude Code:
# /mcp → select "aidesigner" → OAuth sign-in

# Verify
npx @aidesigner/agent-skills doctor --all
```

## Agent Binding

Best-fit agents:
- **frontend-architect** (L2): Primary consumer — generates pages and components
- **ux-designer** (L3): Design iteration and refinement
- **rapid-prototyper** (L5): Quick UI prototyping
- **mobile-app-builder** (L3): Mobile viewport generation

## Cost Warning

Each generation consumes credits. Check `get_credit_status` before batch operations.
Prefer `refine_design` over new `generate_design` calls when iterating.

## Integration with DESIGN.md

If the project has a `DESIGN.md` (Google Stitch standard), reference it in prompts:
"Follow the design system defined in DESIGN.md" — the MCP already reads repo context,
but explicit reference ensures the AI agent passes the right tokens.
