---
name: mcp2web
description: Build MCP servers that serve HTML/CSS web UIs via the mcp2web protocol
version: 1.0.0
---

# mcp2web — Building Web UI MCP Servers

## Protocol Overview

mcp2web is a protocol standard for MCP servers that serve HTML/CSS web UIs. An Electron mini-browser connects to these servers and renders their HTML content.

### URI Schemes
- **Resources**: `mcp2web://<server-name>/<path>` — HTML pages served as MCP resources with `mimeType: "text/html"`
- **Tool Actions**: `mcp2web-tool://<tool-name>` — used as `<form action>` attributes to trigger MCP tool calls

### How It Works
1. MCP server registers resources (HTML pages) and tools (form handlers)
2. Electron browser connects via stdio, lists resources, renders them in a sandboxed iframe
3. Links (`<a href="mcp2web://...">`) trigger resource reads
4. Forms (`<form action="mcp2web-tool://...">`) trigger tool calls
5. Tool responses containing HTML are rendered as new pages

## Project Scaffolding

When creating a new mcp2web server, use this structure:

```
my-server/
├── package.json
├── tsconfig.json
└── src/
    ├── pages.ts    # HTML page template functions
    └── server.ts   # MCP server setup, resources, tools
```

### package.json
```json
{
  "type": "module",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.12.1",
    "zod": "^3.24.4"
  },
  "devDependencies": {
    "typescript": "^5.8.3"
  },
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js"
  }
}
```

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"]
}
```

## Resource Pattern

Register HTML pages as MCP resources:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({ name: "my-server", version: "1.0.0" });

server.resource("page-name", "mcp2web://my-server/page-name", async (uri) => ({
  contents: [{
    uri: uri.href,
    mimeType: "text/html",
    text: myPageFunction()
  }]
}));
```

## Tool Pattern

Register form handlers as MCP tools:

```typescript
import { z } from "zod";

server.tool("submit-form", {
  field1: z.string(),
  field2: z.string()
}, async ({ field1, field2 }) => ({
  content: [{
    type: "text",
    text: successPageFunction(field1, field2)
  }]
}));
```

## HTML/CSS Guidelines

### MUST follow:
- All CSS must be inline (`<style>` tags) — no external stylesheets
- All pages must be complete HTML documents (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`)
- Navigation links: `<a href="mcp2web://server-name/page-name">`
- Form actions: `<form action="mcp2web-tool://tool-name" method="POST">`
- Form inputs must have `name` attributes matching tool parameter names
- No external JavaScript dependencies
- No external images or fonts (use inline SVG or CSS-only graphics)

### Recommended:
- Dark theme for consistency with the mcp2web browser
- Responsive design with max-width containers
- Color scheme: bg #1a1a2e, text #e0e0e0, accent #0f3460, links #16c79a
- Clean typography with system fonts

## Server Entry Point Pattern

```typescript
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// ... register resources and tools ...

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Security Considerations
- Content is rendered in a sandboxed iframe (`allow-scripts allow-forms`, no `allow-same-origin`)
- Never include sensitive data in HTML responses
- Validate all tool inputs with Zod schemas
- Pages cannot access the parent window or Node.js APIs

## Security Best Practices

### Always escape user input in HTML

User-provided strings must be HTML-escaped before embedding in templates to prevent XSS:

```typescript
function escapeHtml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// Use it when rendering user data
`<p>${escapeHtml(userInput)}</p>`
```

### Add constraints to Zod schemas

Always set max lengths on string inputs and use format validators where applicable:

```typescript
server.tool("example", {
  name: z.string().max(100),
  email: z.string().email().max(254),
  description: z.string().max(1000),
}, async ({ name, email, description }) => { /* ... */ });
```

### Use non-guessable IDs

Use `crypto.randomUUID()` (built-in to Node.js) instead of sequential integers for resource identifiers:

```typescript
const item = {
  id: crypto.randomUUID(), // e.g. "a1b2c3d4-..."
  // ...
};
```
