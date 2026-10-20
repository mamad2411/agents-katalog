---
name: generate-tool-reference-with-token-counts
description: Generate your MCP tool reference docs by booting the real server, calling listTools, and including a tiktoken cl100k_base count in the title so you and your users can see the context-budget cost at a glance.
category: build-tooling
version: 1.0.0
version_origin: extracted
tags: [docs, codegen, tiktoken, tokens, mcp]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/ChromeDevTools/chrome-devtools-mcp.git
source_ref: main
source_commit: 0a6aaa52ebacb2db834ffa437863e5844aa3730b
source_project: chrome-devtools-mcp
source_path: scripts/generate-docs.ts
imported_at: 2026-04-18T00:00:00Z
---

# Generate Tool Reference with Token Measurements

## When to use

- You maintain MCP tool docs by hand and they drift from the tool descriptions.
- You want "how many tokens does my server's tool list cost?" as a first-class number in the docs so adding a verbose description has a visible cost.
- You want a single source of truth: tool `.describe()` text in code, everything downstream (docs, CLI help, marketing README) derived.

## How it works

- In a `scripts/generate-docs.ts`, spawn the built MCP server via `StdioClientTransport`, call `client.listTools()`, pull JSON-schema `inputSchema` and `description` for each.
- Count tokens: `tiktoken.get_encoding('cl100k_base').encode(JSON.stringify(tools, null, 2)).length`. That's a decent proxy for GPT-4 / Claude-3.5 context cost.
- Title the generated markdown like `# Tool Reference (~18,472 cl100k_base tokens)` so the cost shows up prominently in both the file and the auto-TOC.
- Generate two docs from the same pipeline by passing different startup args: `createTools({slim:true})` produces a slim reference, full mode produces the fat one. Show both token counts.
- Auto-insert a TOC into your README between `<!-- BEGIN AUTO GENERATED TOOLS -->` and `<!-- END AUTO GENERATED TOOLS -->` markers; idempotent regeneration.
- Cross-link tool names inside descriptions: when a description mentions another tool by name, wrap it as `[\`tool_name\`](#tool_name)` automatically.

## Example

```ts
async function measureServer(args: string[]) {
  const transport = new StdioClientTransport({command: 'node', args: ['./build/src/bin/server.js', ...args]});
  const client = new Client({name:'measurer', version:'1.0.0'}, {capabilities:{}});
  await client.connect(transport);
  const {tools} = await client.listTools();
  const enc = get_encoding('cl100k_base');
  const tokens = enc.encode(JSON.stringify(tools, null, 2)).length;
  enc.free();
  await client.close();
  return {tokenCount: tokens, tools};
}

// inside generateReference:
let md = `# ${title} (~${(await measureServer(args)).tokenCount} cl100k_base tokens)\n\n`;
// ...render tool categories, cross-link tool names in descriptions, write to OUTPUT_PATH.
```

## Gotchas

- `cl100k_base` is approximate for modern Claude/GPT; it's a trend indicator, not the exact billed count. Don't quote it as authoritative — just use it to compare slim vs. full, and to alert on regressions.
- `enc.free()` is required — tiktoken leaks native memory otherwise and long build scripts bloat.
- When you spawn your server for codegen, set an env var like `NO_USAGE_STATISTICS=true` so every doc build doesn't generate telemetry noise.
- Keep the generated file under version control; downstream consumers (site builders, search) shouldn't need to re-run the server to read the reference.
- If two tools both describe each other, the cross-link regex can double-wrap. Run the replacement on longest names first and skip matches already inside `[...]`.
