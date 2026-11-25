---
name: ecosystem-guide
description: "Navigating LLM tooling workflows. Use when choosing recall, search, SQLite, MCP, secret-safety, or skill validation tools."
metadata:
  last_updated: "2026-05-15"
  verified_against: "current local skill refresh"
---

# Agent Workflow Ecosystem Guide

Use this as the index for the LLM tooling system in this repo. If another skill mentions one of these tools or repo skills, keep it listed here so agents can understand how the ecosystem fits together.

## Tool Index

| Tool               | Use for                                                                |
| ------------------ | ---------------------------------------------------------------------- |
| `skills` repo      | Canonical portable Agent Skills source of truth                        |
| `check-skills`     | Validating/linting portable Agent Skills                               |
| `pirecall`         | Recalling and querying Pi sessions in `~/.pi/pirecall.db`              |
| `ccrecall`         | Recalling and querying Claude Code sessions in `~/.claude/ccrecall.db` |
| `nopeek`           | Loading secrets without exposing values to model context               |
| `mcp-omnisearch`   | Web search, AI answers, and content extraction                         |
| `mcp-sqlite-tools` | Safe SQLite inspection, querying, schema work, and backups             |
| `mcpick`           | Enabling/disabling MCP servers and profiles per task                   |
| `npmx.dev`         | Looking up npm package docs/types during research                      |

## Skill Index

| Need                                               | Skill                           |
| -------------------------------------------------- | ------------------------------- |
| Reporting failed tests/builds honestly             | `asshole`                       |
| Debugging CI, containers, or reproducible failures | `ci-debug-workflow`             |
| Cleaning AI-generated code noise                   | `deslop`                        |
| Choosing tools across this ecosystem               | `ecosystem-guide`               |
| Finding architecture and module-boundary refactors | `improve-codebase-architecture` |
| Handling secrets safely                            | `nopeek`                        |
| Coordinating parallel agents/sessions/worktrees    | `orchestration`                 |
| Developing Claude Code plugins                     | `plugin-dev`                    |
| Capturing reusable lessons or instruction updates  | `reflect`                       |
| Verifying sources before presenting claims         | `research`                      |
| Creating or improving skills                       | `skill-creator`                 |
| Planning risky or ambiguous work                   | `structured-rpi`                |
| Running explicit test-driven development           | `tdd`                           |
| Finding duplicated/inconsistent tech debt          | `techdebt-finder`               |

## Svelte Skill Router

| Need                              | Skill                                               |
| --------------------------------- | --------------------------------------------------- |
| Baseline Svelte guidance          | `svelte-core-bestpractices` or `svelte-code-writer` |
| Runes/reactivity/props            | `svelte-runes`                                      |
| Snippets, attachments, directives | `svelte-template-directives`                        |
| Scoped CSS and styling            | `svelte-styling`                                    |
| Components, forms, UI libraries   | `svelte-components`                                 |
| SvelteKit data/load/actions       | `sveltekit-data-flow`                               |
| SvelteKit routing/layout/errors   | `sveltekit-structure`                               |
| SvelteKit remote functions        | `sveltekit-remote-functions`                        |
| Deployment/build/library/PWA      | `svelte-deployment`                                 |
| LayerChart chart components       | `svelte-layerchart`                                 |

## Common Commands

```bash
pnpx pirecall recall "what did we decide?" --json
pnpx ccrecall recall "last auth work" --json
pnpx nopeek load .env --only DATABASE_URL
pnpx check-skills validate . --recursive
pnpx mcpick enable omnisearch sqlite-tools
```

## MCP Setup

Install common MCP tools when a harness supports MCP servers:

```bash
npm i -g mcp-omnisearch mcp-sqlite-tools mcpick
```

Use `mcp-omnisearch` for research, `mcp-sqlite-tools` for local databases, and `mcpick` for keeping MCP context lean.

## Skill Authoring + Validation

Use `skill-creator` for authoring, then validate before finishing:

```bash
pnpx check-skills validate ./my-skill
pnpx check-skills validate . --recursive --llm --quiet
pnpx check-skills validate . --recursive --no-quality
```
