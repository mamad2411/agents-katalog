---
name: follow-create-plugins
description: Create plugins/extensions/addons for any tool via target-specific follow-create-* skills
argument-hint: "[target] [spec]"
related:
  - follow-create-sdk
  - follow-create-web
  - follow-create-cli
  - follow-create-mcp
  - follow-create-web-mcp
  - deep-review-codebase
  - update-devin-global-skills
  - follow-best-practice
  - implement-to-production
  - ask-me
---

## Goal

Create a plugin/extension/addon for the specified target — this parent skill only dispatches; it does not implement target-specific workflows

## Scope

- Consolidates the capabilities of the former `follow-create-*plugin*`/`create-*-plugins` skills — one skill per target
- The argument is the target name (e.g. `vite`, `eslint`, `nvim`, `raycast`, `obsidian`, `bun`, `vscode`)
- If no target is given → `/ask-me` to pick a target from the table

## Execute

### Target Skills

| Target | Skill |
|---|---|
| `biome` | `/follow-create-biome-plugin` — Biome plugin (GritQL rules, diagnostics) |
| `browser-wxt`, `wxt`, `browser` | `/follow-create-browser-extensions-wxt` — browser extension with WXT |
| `bun` | `/follow-create-bun-plugin` — Bun plugin (`Bun.plugin`, preload, bundler) |
| `claude` | `/follow-create-claude-plugin` — Claude Code plugin (commands, hooks, agents) |
| `codex` | `/follow-create-codex-plugin` — Codex CLI plugin |
| `devin` | `/follow-create-devin-plugin` — Devin plugin/integration |
| `elysia` | `/follow-create-elysia-plugin` — Elysia plugin (lifecycle hooks, decorators) |
| `eslint` | `/follow-create-eslint-plugin` — ESLint plugin (rules, configs) |
| `nitro` | `/follow-create-nitro-plugin` — Nitro plugin |
| `nushell`, `nu` | `/follow-create-nushell-plugin` — Nushell plugin |
| `nvim`, `neovim` | `/follow-create-nvim-plugin` — Neovim plugin (Lua) |
| `obsidian` | `/follow-create-obsidian-plugin` — Obsidian plugin (TypeScript API) |
| `oxlint` | `/follow-create-oxlint-plugin` — Oxlint plugin |
| `powershell-module`, `ps`, `pwsh` | `/follow-create-powershell-module` — PowerShell module |
| `raycast` | `/follow-create-raycast-extensions` — Raycast extension (React + TypeScript) |
| `rolldown` | `/follow-create-rolldown-plugin` — Rolldown plugin |
| `storybook-addon`, `storybook` | `/follow-create-storybook-addon` — Storybook addon |
| `tauri` | `/follow-create-tauri-plugin` — Tauri plugin (Rust + JS API) |
| `tsdown` | `/follow-create-tsdown-plugin` — tsdown plugin/hooks |
| `tui-ratatui` | `/follow-create-tui-ratatui` — Ratatui widget/plugin |
| `vite` | `/follow-create-vite-plugin` — Vite plugin (hooks, transform, HMR) |
| `vitest` | `/follow-create-vitest-plugin` — Vitest plugin (reporters, environment) |
| `vscode`, `vs-code` | `/follow-create-vscode-extensions` — VS Code extension |
| `webmcp`, `web-mcp` | `/follow-create-web-mcp` — WebMCP tools on a web page (page-provided agent tools) |
| `zed` | `/follow-create-zed-extensions` — Zed extension |

1. Run `/deep-research` + `/follow-best-practice` for the chosen target, following the conventions in `/update-devin-global-skills` (done inside the dispatched target skill)
2. Determine the target from the argument (e.g. `/follow-create-plugins vite`)
3. If the target is supported → invoke the skill from the table and follow that skill's flow
4. If no target is given or it is unrecognized → `/ask-me` to pick a target from the table

## Rules

- The parent only dispatches — never duplicate a target skill's workflow in this file
- Always choose library/tooling first via `/deep-review-codebase` (techstack catalog)
- After scaffolding → `/implement-to-production` per convention

- Use /follow-create-sdk when needed
- Use /follow-create-web when needed
- Use /follow-create-cli when needed
- Use /follow-create-mcp when needed
- Use /follow-create-web-mcp when needed
- Use /update-devin-global-skills when needed
- Use /follow-best-practice when needed

## File Structure

Canonical file structure + layer table: [templates/file-structure-plugins.md](templates/file-structure-plugins.md)

## Expected Outcome

- The caller is dispatched to the workflow matching the target, then the plugin is built through that flow
