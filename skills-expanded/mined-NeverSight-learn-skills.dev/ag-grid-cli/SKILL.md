---
name: ag-grid-cli
description: Use AG Grid MCP-style docs search, version detection, examples, definitions, and upgrade guidance through a lightweight local CLI wrapper. Use when working on AG Grid integration or migration tasks.
---

# AG Grid CLI

Use this skill when you need AG Grid documentation, examples, API references, version detection, or migration guidance, but you want a local CLI workflow instead of the AG Grid MCP server.

This CLI is modeled after the official AG Grid MCP server documentation:

- `search_docs`
- `detect_version`
- `set_version`
- `list_versions`
- `quick-start`
- `upgrade-grid`
- resources for `articles`, `definitions`, and `examples`

Reference:

- https://www.ag-grid.com/vue-data-grid/mcp-server/

## Purpose

The AG Grid MCP server gives LLMs framework-specific and version-specific AG Grid context. `ag-grid-cli` exposes the same practical capabilities as terminal commands so an agent can fetch the same class of information directly.

## Bootstrap

This skill is designed for zero-build consumption after install.

- no runtime compilation
- no runtime `npm install`
- bundled CLI is committed to the repo
- only runtime requirement: Node.js

Primary invocation:

```bash
node <skill-dir>/bundle/ag-grid-cli.cjs <command> [args...]
```

This is the default command agents should use after the skill is installed.
Do not assume `ag-grid-cli` is on `PATH`.

If the agent knows the installed skill path, run the sibling bundle directly.

Optional shortcut when available:

```bash
ag-grid-cli <command> [args...]
```

Portable fallback on any OS:

```bash
node <skill-dir>/bundle/ag-grid-cli.cjs <command> [args...]
```

Platform wrappers:

- macOS/Linux: `<skill-dir>/ag-grid-cli.sh`
- Windows cmd: `<skill-dir>\\ag-grid-cli.cmd`
- Windows PowerShell: `<skill-dir>\\ag-grid-cli.ps1`

Launcher behavior:

- the committed bundle is the canonical runtime
- wrappers call the committed bundle directly
- `ag-grid-cli` on `PATH` is only an optional convenience
- it requires Node, but does not run `npm install` at runtime
- then it executes the CLI

This keeps usage simple for agents embedded in another project: the user can add this skill folder, and the agent can run the committed bundle immediately.

Naming:

- installed CLI binary: `ag-grid-cli`
- repo-local Unix wrapper: `./ag-grid-cli.sh`
- repo-local Windows cmd wrapper: `ag-grid-cli.cmd`
- repo-local Windows PowerShell wrapper: `ag-grid-cli.ps1`
- repo-local portable bundle entry: `node bundle/ag-grid-cli.cjs`

## Agent Notice

After skill install, prefer the sibling bundle in the installed skill directory:

- `node <skill-dir>/bundle/ag-grid-cli.cjs ...`

Only use `ag-grid-cli ...` if you already know the binary is available on `PATH`.

If a prerequisite is missing, say it explicitly before continuing:

- `Node.js is required to run ag-grid-cli.`

Do not silently try to compile or install dependencies inside the installed skill directory.
Do not run `npm install` from the skill folder as a bootstrap step.

## Use This For

- detecting the AG Grid version and framework in a repo
- pinning a version/framework when detection is wrong or ambiguous
- searching docs before editing AG Grid code
- fetching full articles, API definitions, and examples
- generating a quick-start plan for a new or existing grid
- generating a migration plan for AG Grid upgrades

## Command Mapping

Official MCP concept -> CLI equivalent

- `detect_version` -> `ag-grid-cli detect-version`
- `set_version` -> `ag-grid-cli set-version --version <semver> --framework <framework>`
- `list_versions` -> `ag-grid-cli list-versions`
- `search_docs` -> `ag-grid-cli search-docs "<query>"`
- `articles` resource -> `ag-grid-cli articles list|get`
- `definitions` resource -> `ag-grid-cli definitions list|get`
- `examples` resource -> `ag-grid-cli examples list|get`
- `quick-start` prompt -> `ag-grid-cli quick-start`
- `upgrade-grid` prompt -> `ag-grid-cli upgrade-grid --to <semver>`

## Default Workflow

When working in an AG Grid repo, do this first:

1. Detect the current setup.
   - `node <skill-dir>/bundle/ag-grid-cli.cjs detect-version`
2. If detection fails or the repo is unusual, set it manually.
   - `node <skill-dir>/bundle/ag-grid-cli.cjs set-version --version 35.1.0 --framework vue`
3. Search docs before changing code.
   - `node <skill-dir>/bundle/ag-grid-cli.cjs search-docs "cell renderer"`
4. Pull exact resources when the task is implementation-heavy.
   - `node <skill-dir>/bundle/ag-grid-cli.cjs articles get <slug>`
   - `node <skill-dir>/bundle/ag-grid-cli.cjs definitions get <apiName>`
   - `node <skill-dir>/bundle/ag-grid-cli.cjs examples get <articleSlug> <exampleSlug>`

## Recommended Agent Behavior

- Prefer `detect-version` before `search-docs`.
- Prefer `node <skill-dir>/bundle/ag-grid-cli.cjs ...` as the default invocation.
- Do not spend turns probing `ag-grid-cli` on `PATH` unless the environment already indicates it exists.
- If the repo uses a non-semver tag like `latest`, let the CLI normalize it.
- Use `--json` when you need machine-readable output for chaining or parsing.
- Use `--plain` when you need stable line-based output for shell pipelines.
- Use explicit `--framework` and `--version` overrides in monorepos or mixed-framework repos.
- For upgrades across multiple major versions, use `upgrade-grid` and follow one major at a time.

## Search Guidance

Use natural language queries, same style as the MCP docs:

- `node <skill-dir>/bundle/ag-grid-cli.cjs search-docs "column sorting"`
- `node <skill-dir>/bundle/ag-grid-cli.cjs search-docs "cell renderers" --framework vue`
- `node <skill-dir>/bundle/ag-grid-cli.cjs search-docs "server side row model filtering" --version 34.3.0`
- `node <skill-dir>/bundle/ag-grid-cli.cjs search-docs "data grid performance" --framework react --limit 3`

When search results surface an API name or article slug, follow up with:

- `node <skill-dir>/bundle/ag-grid-cli.cjs definitions get <name>`
- `node <skill-dir>/bundle/ag-grid-cli.cjs articles get <slug>`

## Resource Workflows

List articles:

```bash
node <skill-dir>/bundle/ag-grid-cli.cjs articles list --framework vue
```

Read one article:

```bash
node <skill-dir>/bundle/ag-grid-cli.cjs articles get component-cell-renderer --framework vue
```

List API definitions:

```bash
node <skill-dir>/bundle/ag-grid-cli.cjs definitions list --version 35.1.0
```

Read one definition:

```bash
node <skill-dir>/bundle/ag-grid-cli.cjs definitions get cellRenderer
```

List examples:

```bash
node <skill-dir>/bundle/ag-grid-cli.cjs examples list --framework vue --language typescript
```

Read one example:

```bash
node <skill-dir>/bundle/ag-grid-cli.cjs examples get row-ids row-data --framework vue --language typescript
```

## Prompt Workflows

Quick start plan:

```bash
node <skill-dir>/bundle/ag-grid-cli.cjs quick-start --framework vue --typescript --feature pagination --feature row-grouping
```

Upgrade plan:

```bash
node <skill-dir>/bundle/ag-grid-cli.cjs upgrade-grid --to 35.1.0
```

Explicit upgrade path:

```bash
node <skill-dir>/bundle/ag-grid-cli.cjs upgrade-grid --from 33.2.0 --to 35.1.0 --framework react
```

## Output Contract

- Human mode: readable summaries and content blocks.
- `--json`: structured stdout.
- `--plain`: stable tab-separated or raw content output.
- Primary data goes to stdout.
- Errors go to stderr.

## Guardrails

- Do not guess AG Grid version-specific behavior when the CLI can resolve it.
- Do not skip version detection before migrations unless the user gave an explicit version.
- Do not jump multiple major AG Grid versions in one migration plan.
- Prefer fetching the exact article or definition when changing a fragile AG Grid API surface.

## Example Agent Loops

Implement a feature:

1. `node <skill-dir>/bundle/ag-grid-cli.cjs detect-version`
2. `node <skill-dir>/bundle/ag-grid-cli.cjs search-docs "set filter tree list" --framework vue`
3. `node <skill-dir>/bundle/ag-grid-cli.cjs definitions get ISetFilterParams`
4. `node <skill-dir>/bundle/ag-grid-cli.cjs examples list --framework vue --language typescript`

Plan an upgrade:

1. `node <skill-dir>/bundle/ag-grid-cli.cjs detect-version`
2. `node <skill-dir>/bundle/ag-grid-cli.cjs list-versions`
3. `node <skill-dir>/bundle/ag-grid-cli.cjs upgrade-grid --to 35.1.0`
4. `node <skill-dir>/bundle/ag-grid-cli.cjs articles get upgrading-to-ag-grid-34`
5. `node <skill-dir>/bundle/ag-grid-cli.cjs articles get upgrading-to-ag-grid-35`
