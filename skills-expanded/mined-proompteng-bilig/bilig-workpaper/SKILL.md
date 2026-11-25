---
name: bilig-workpaper
version: 0.1.0
description: Use @bilig/workpaper WorkPaper state for workbook formulas, MCP editing, and tool integrations without driving spreadsheet UI.
tags:
  - agents
  - workbook-runtime
  - formulas
  - workpaper
  - mcp
  - typescript
---

# Bilig WorkPaper Agent Skill

Use this skill when an agent needs spreadsheet-style formulas but the work should run through files, terminal commands, TypeScript, HTTP routes, or MCP tools instead of Excel UI automation.

## When To Trigger

Trigger this skill for tasks involving:

- workbook-shaped business logic in Node.js services;
- formula readback after writing cells;
- quote, budget, payout, pricing, import-validation, or forecast models;
- agent spreadsheet tools that need deterministic cell addresses;
- MCP clients that can run a stdio server or call a Streamable HTTP endpoint;
- reduced formula/import bugs that need a local report.

Do not trigger it for manual spreadsheet editing, Office macros, VBA, pivots, charts, COM automation, or exact Excel desktop behavior unless the user explicitly asks to compare Bilig against an Excel oracle.

## Command Safety

Do not build shell commands by concatenating user text. Treat the commands below as literal templates, validate workbook paths before use, and reject values containing newlines, backticks, `$(`, `;`, `&`, `|`, `<`, or `>`. Prefer MCP client `command` plus `args` arrays or direct TypeScript calls when inserting user-provided paths or cell references.

## First Check: Agent Triage

Before wiring a client or opening a spreadsheet UI, print the compact decision
card:

```json
{
  "command": "npm",
  "args": ["exec", "--yes", "--package", "@bilig/workpaper@latest", "--", "bilig-agent-start", "--json"]
}
```

## First Check: Agent Evaluator

Before wiring a client, prove the published agent door with the package-owned evaluator.
It exercises MCP discovery, cell mutation, formula readback, JSON export, restart restore, and returns `verified: true`:

```json
{
  "command": "npm",
  "args": ["exec", "--yes", "--package", "@bilig/workpaper@latest", "--", "bilig-evaluate", "--door", "agent-mcp", "--json"]
}
```

For service-owned WorkPaper logic without MCP, run `bilig-evaluate --door workpaper-service --json`.
Use the lower-level challenge commands only when debugging the direct API loop or file-backed MCP JSON-RPC transcript:

```json
[
  { "command": "npm", "args": ["exec", "--package", "@bilig/workpaper@latest", "--", "bilig-agent-challenge", "--json"] },
  { "command": "npm", "args": ["exec", "--package", "@bilig/workpaper@latest", "--", "bilig-mcp-challenge", "--json"] }
]
```

## First Choice: MCP

Use MCP when the host can run a stdio server or call a Streamable HTTP server.
Configure stdio as an argument array, not a shell-concatenated string:

If the host supports installable skills, first check that the public skill
package is discoverable:

```sh
npx --yes skills@latest add https://bilig.proompteng.ai --list
npx --yes skills@latest add proompteng/bilig --skill bilig-workpaper --list
```

```json
{
  "command": "npm",
  "args": [
    "exec",
    "--package",
    "@bilig/workpaper@latest",
    "--",
    "bilig-workpaper-mcp",
    "--workpaper",
    "__WORKPAPER_PATH__",
    "--init-demo-workpaper",
    "--writable"
  ]
}
```

Run `bilig-evaluate --door agent-mcp --json` first. If the workbook contains
provider-backed formulas such as `IMPORTRANGE`, run
`bilig-evaluate --door agent-mcp --scenario provider-backed --json` to confirm
the adapter boundary. If the evaluator fails, run `bilig-mcp-challenge` and
treat its returned `tools` array as the source of truth for the currently published package. The core file-backed tools are:

- `list_sheets`
- `read_range`
- `read_cell`
- `set_cell_contents`
- `set_cell_contents_and_readback`
- `get_cell_display_value`
- `export_workpaper_document`
- `validate_formula`

When the server is started through `@bilig/workpaper@latest` with
`--from-xlsx ./pricing.xlsx`, `tools/list` also includes
`analyze_workbook_risk`. That tool is fixed to the source XLSX passed at
startup and reports workbook risk indicators before a workflow trusts the imported
WorkPaper. Without `--workpaper --writable`, edits stay in memory; add a
WorkPaper JSON path only when the task needs persisted file state. It does not
certify Excel compatibility.

For a maintained XLSX preflight transcript, run
`pnpm --dir examples/headless-workpaper run agent:mcp-xlsx-risk-preflight`.
It requires `analyze_workbook_risk`, `set_cell_contents_and_readback`,
`export_workpaper_document`, `Inputs!B3`, `Summary!B3`, `60000 -> 96000`,
and `verified: true`.

After a write, always read the dependent output cell and export the WorkPaper
document. If the listed tool set includes `set_cell_contents_and_readback`,
prefer it for stateless clients because the edit and dependent readback happen
in one tool call. If it is absent, call `set_cell_contents`, then `read_cell`
or `read_range`, then `export_workpaper_document`.

For remote MCP clients, use the stateless demo endpoint when the client supports
Streamable HTTP:

```text
https://bilig.proompteng.ai/mcp
https://bilig.proompteng.ai/mcp/workpaper
```

The remote endpoint is request-local and does not write user files. Use it for
connector smoke tests, tool discovery, and agent onboarding; use the file-backed
stdio command when the workflow must persist a project WorkPaper JSON file.

## Second Choice: Direct TypeScript

Use `@bilig/workpaper` directly when workbook logic belongs in a service, queue worker, test, or route:

```ts
import { buildA1WorkPaper } from '@bilig/workpaper'

const book = buildA1WorkPaper({
  Inputs: [
    ['Metric', 'Value'],
    ['Customers', 20],
    ['Average revenue', 1200],
  ],
  Summary: [
    ['Metric', 'Value'],
    ['Revenue', '=Inputs!B2*Inputs!B3'],
  ],
})

const proof = book.editAndReadback('Inputs!B2', 32, {
  readbackRange: 'Summary!B2',
})

console.log({
  editedCell: proof.editedCell,
  after: proof.afterReadback.displayValues,
  afterRestore: proof.restoredReadback.displayValues,
  persistedDocumentBytes: proof.persistedDocumentBytes,
  verified: proof.verified,
})

book.dispose()
```

## Formula Clinic

When the user has a reduced workbook formula/import bug, generate a local report through an argument array:

```json
{
  "command": "npm",
  "args": [
    "exec",
    "--package",
    "@bilig/workpaper@latest",
    "--",
    "bilig-formula-clinic",
    "./reduced.xlsx",
    "--cells",
    "Summary!B7,Inputs!B2"
  ]
}
```

The report is local. It does not upload workbook contents. Ask for a reduced public fixture rather than private customer spreadsheets.

## Required Verification

Return readback, not a write-only claim. A successful agent response should include:

- the exact edited sheet and A1 cell;
- before values for relevant inputs and dependent outputs;
- after values read from the recalculated workbook;
- persistence evidence from serialized or exported WorkPaper state;
- restore or reimport checks when file boundaries matter;
- limitations for unsupported formulas or Excel-only features.

If any readback step fails, report the blocker instead of claiming the workbook was updated.

## Reference URLs

- Compact docs map: https://proompteng.github.io/bilig/llms.txt
- Full host context: https://proompteng.github.io/bilig/llms-full.txt
- Host handbook: https://proompteng.github.io/bilig/headless-workpaper-agent-handbook.html
- Agent workbook challenge: https://proompteng.github.io/bilig/agent-workbook-challenge.html
- MCP server guide: https://proompteng.github.io/bilig/mcp-workpaper-tool-server.html
- OpenHands MCP setup: https://proompteng.github.io/bilig/openhands-workpaper-mcp.html
- OpenCode MCP setup: https://proompteng.github.io/bilig/opencode-workpaper-mcp.html
- Open WebUI tool setup: https://proompteng.github.io/bilig/open-webui-workpaper-mcp.html
- LobeHub MCP setup: https://proompteng.github.io/bilig/lobehub-workpaper-mcp.html
- AnythingLLM MCP setup: https://proompteng.github.io/bilig/anythingllm-workpaper-mcp.html
- Sim MCP setup: https://proompteng.github.io/bilig/sim-workpaper-mcp.html
- Formula clinic: https://proompteng.github.io/bilig/formula-bug-clinic.html
- Compatibility limits: https://proompteng.github.io/bilig/where-bilig-is-not-excel-compatible-yet.html
- Repository: https://github.com/proompteng/bilig
