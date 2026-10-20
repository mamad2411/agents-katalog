---
name: follow-tool-node-modules-inspector
description: Set up and use Node Modules Inspector to examine node_modules interactively
argument-hint: "[scope]"
related:
  - follow-lang-nodejs
  - follow-lang-typescript
  - follow-tool-knip
  - follow-tool-usage
  - follow-tool-pkg-new
  - follow-tool-renovate
  - report
---

## Goal

Set up and use `node-modules-inspector` to inspect, debug, and analyze `node_modules` interactively

## Scope

For Node.js / TypeScript projects using `npm`, `pnpm`, or `bun`

- Use this skill to inspect the dependency graph, duplicates, sizes, and publish metadata of `node_modules`
- If the goal is finding unused dependencies/exports in source code → use `/follow-tool-knip` instead

- Latest: `node-modules-inspector@2.7.0` (verified 2026-09-24)

## Execute

### 1. Run Inspector

> Goal: open the interactive UI to examine dependencies

1. Run `bunx node-modules-inspector` at the project root
2. Or run it with the package manager the project uses, e.g. `bunx node-modules-inspector`
3. Wait until the UI opens in the browser
4. See details in 

### 2. Explore UI

> Goal: use the interactive UI to analyze dependencies

1. View the dependency tree, versions, and installed sizes
2. Search for duplicate packages or multiple versions
3. Check publish metadata and `publint` warnings when enabled
4. See details in 

### 3. Generate Reports

> Goal: run machine-readable reports for automation

1. Run `bunx node-modules-inspector report duplicates`
2. Run `bunx node-modules-inspector report sizes`
3. Run `bunx node-modules-inspector report maintainers`
4. Use the `--json` flag to output JSON
5. See details in 

### 4. MCP Server

> Goal: expose an MCP server for AI tools

1. Run `bunx node-modules-inspector mcp`
2. Register the stdio server in the client's MCP config
3. Use the tools `nmi:report-duplicates`, `nmi:report-sizes`, `nmi:report-maintainers`
4. See details in 

### 5. Static Build

> Goal: build a static report for hosting or CI artifacts

1. Run `bunx node-modules-inspector build`
2. Get the `dist/__node-modules-inspector` directory (v2 default outDir)
3. Serve with a static file server or host on GitHub Pages
4. See details in 

## Rules

### 1. Usage

- Use `bunx` by default; if the project has no bun, use the project's package manager
- Supports `npm`, `pnpm`, and `bun`
- No need to install it as a dependency for one-off use

### 2. Config

- Create `node-modules-inspector.config.ts` when custom default filters or `publint` are needed
- Don't hard-code sensitive paths in config

### 3. Reports

- Use `--json` when piping to a script or `jq`
- Use `--limit` and `--depth` to shrink the output
- In CI use the `report` subcommands instead of the UI

- Use /follow-lang-nodejs if needed
- Use /follow-lang-typescript if needed
- Use /follow-tool-knip if needed
- Use /follow-tool-usage if needed
- Use /follow-tool-pkg-new if needed
- Use /follow-tool-renovate if needed

## References

- [CLI reference](references/cli.md)


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `node-modules-inspector` runs via both `bunx` and the project's package manager
- The interactive UI analyzes dependencies on the spot
- Reports produced in both text and JSON
- The MCP server usable for AI tools
- The static build usable for sharing results

