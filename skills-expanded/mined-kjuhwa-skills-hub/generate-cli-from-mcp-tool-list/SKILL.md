---
name: generate-cli-from-mcp-tool-list
description: Auto-generate a yargs-based CLI from an MCP server's tool list and JSON schemas so every tool becomes a subcommand with typed positional args for required fields and flags for optional ones.
category: cli
version: 1.0.0
version_origin: extracted
tags: [cli, yargs, codegen, mcp, json-schema]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/ChromeDevTools/chrome-devtools-mcp.git
source_ref: main
source_commit: 0a6aaa52ebacb2db834ffa437863e5844aa3730b
source_project: chrome-devtools-mcp
source_path: scripts/generate-cli.ts
imported_at: 2026-04-18T00:00:00Z
---

# Generate CLI from MCP Tool List

## When to use

- You already have an MCP server with N tools and want a shell CLI that mirrors them without hand-writing N yargs commands.
- You want the CLI to stay in sync with new/renamed tools automatically when you rebuild.
- You want required parameters to be positional (`mycli click <uid>`) and optional parameters to be flags (`--fullPage`).

## How it works

- In a `scripts/generate-cli.ts` build step, spin up the real MCP server via `StdioClientTransport`, call `client.listTools()`, and walk each tool's `inputSchema` (standard JSON Schema).
- Convert each property to a `{name, type, description, required, default, enum}` record. For each tool, emit an entry `{description, category, args}` into a `commands` map.
- Write that map to a generated TS file (`cliDefinitions.ts`) as a `const` export. Ship it as source — generated, but checked in — so the CLI binary can run without a codegen step.
- In the CLI entry (`bin/mycli.ts`), read `commands`, and for each entry register a yargs command: required args become `y.positional(name, {type, choices, default})`, optional args become `y.option(name, ...)`. Fallthrough handler calls `sendCommand({method:'invoke_tool', tool:name, args})`.
- Filter inappropriate tools at generation time (e.g. skip tools whose schema is an array or nested object — shells don't pass JSON well).

## Example

```ts
// scripts/generate-cli.ts
const tools = (await client.listTools()).tools.filter(t =>
  t.name !== 'fill_form' && t.name !== 'wait_for' // skip complex schemas
);
const commands = Object.fromEntries(tools.map(t => [t.name, {
  description: t.description,
  category: toolNameToCategory.get(t.name),
  args: schemaToCLIOptions(t.inputSchema), // {name,type,required,default,enum}
}]));
fs.writeFileSync(OUTPUT_PATH, `export const commands = ${JSON.stringify(commands, null, 2)} as const;`);

// bin/mycli.ts - at runtime
for (const [name, def] of Object.entries(commands)) {
  const required = Object.entries(def.args).filter(([,a]) => a.required);
  let cmdStr = name + required.map(([n]) => ` <${n}>`).join('');
  y.command(cmdStr, def.description, y => {
    for (const [argName, opt] of Object.entries(def.args)) {
      opt.required ? y.positional(argName, {...}) : y.option(argName, {...});
    }
  }, async argv => sendCommand({method:'invoke_tool', tool:name, args: argv}));
}
```

## Gotchas

- JSON-Schema `type` can be a union (`["string","null"]`); treat that as the non-null variant or skip the tool. Yargs doesn't model nullable well.
- Map schema types to yargs types explicitly: `integer|number → number`, `array → array`, everything else → `string`. Don't assume `type: 'object'` tools make sense in a shell.
- Pass `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS=true` (or your equivalent) when booting the server for codegen — you don't want to spam telemetry from a build script.
- Keep an escape hatch in the CLI binary to disable tools that make no sense in a shell (e.g. `fill_form` requiring nested JSON). Filter at generation, not at runtime.
- Pre-generate at build time, don't call `listTools()` on every CLI invocation — that would defeat a fast daemon-backed CLI.
