---
name: webmcp-agent
description: A skill for guiding AI Agents to interact with WebMCP web pages, triggered immediately after the AI Agent calls the browser (e.g., via chrome-devtools MCP or similar MCPs/Tools) to enter a page
metadata:
  author: Ryan
  version: "1.0.1"
---

## Reference
### What Is WebMCP
WebMCP is a proposed web standard that lets websites expose structured tools to AI agents through navigator.modelContext, replacing screen-scraping with explicit contracts.

WebMCP is a proposed web standard that lets a website expose actions as tools instead of forcing agents to reverse-engineer the interface. The site describes what can be done. The browser mediates access. The agent calls a tool instead of guessing which pixels to click.
The standard lives at navigator.modelContext. The authoritative definition belongs to the W3C WebMCP spec and the Chrome team’s design documents, not to the MCP-B packages. MCP-B exists to help you use that standard today, then extend it when you need browser MCP features beyond the standard.

### WebMCP API
Refer to [Standard API Document](./resources/standard-api.md)

## When to Trigger
Triggered immediately after the AI Agent calls the browser (e.g., via chrome-devtools MCP or similar MCPs/Tools) to enter a page. Once triggered, execute the steps in [How to Use](#how-to-use) immediately.

## How to Use

1. Execute [listTools script](./scripts/listTools.js) to get the list of all `WebMCP tools`. **If an exception is thrown, skip the subsequent steps.**
2. Read the return value of `listTools()`, which is an array where each element is an object containing three properties: `description`, `name`, and `inputSchema`, corresponding to `tool description`, `tool name`, and `JSON Schema string for tool input parameters`.
3. Decide whether to call these `tools` as needed. If required, execute the `navigator.modelContextTesting.executeTool(tool.name, inputSchema)` method, where `tool.name` is the name of the tool and `inputSchema` is the JSON Schema string of the tool's input parameters. Note that `executeTool` returns a `Promise<string>` which resolves to the execution result.

Refer to [Standard API Document](./resources/standard-api.md)