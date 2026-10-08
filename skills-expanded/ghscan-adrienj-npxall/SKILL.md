---
name: npxall-mcp
description: Call any npm package function directly from Claude Code via the npxall MCP server
---

# npxall MCP Server

npxall exposes a single `call` tool that installs any npm package on demand and invokes a function from it. Packages are cached server-side with LRU eviction — first call installs, subsequent calls are fast. No auth required.

## Installation

Add one of the following blocks to your Claude Code MCP settings (`~/.claude/settings.json` for global use, or `.claude/settings.json` for a specific project).

### Hosted server (recommended — no local setup)

```json
{
  "mcpServers": {
    "npxall": {
      "type": "http",
      "url": "https://mcp.npxall.com/mcp"
    }
  }
}
```

If your MCP client only supports the legacy SSE transport (e.g. older Claude Desktop):

```json
{
  "mcpServers": {
    "npxall": {
      "type": "sse",
      "url": "https://mcp.npxall.com/sse"
    }
  }
}
```

### Local dev server

Clone the repo and start with `node mcp/server.js`, then point at localhost:

```json
{
  "mcpServers": {
    "npxall": {
      "type": "http",
      "url": "http://localhost:3001/mcp"
    }
  }
}
```

The local server defaults to port `3001`. Override with the `PORT` environment variable.

## Usage

The server exposes a single `call` tool with these parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `package` | string | yes | npm package name, e.g. `"lodash"`, `"ms"`, `"@turf/turf"` |
| `method` | string | no | Function or method name exported by the package, e.g. `"camelCase"`, `"chunk"` |
| `args` | array | no | Arguments as native JSON values — numbers, strings, arrays, objects, no quoting needed |

**How resolution works:**
- If `method` is provided, the server calls `pkg[method](...args)`.
- If no `method` and the default export is a function, it is called directly with `args`.
- If no `method` and the export is not a function (a namespace object), the export is returned so you can inspect its shape.
- On a bad method name, the error lists up to 10 callable methods available on the package to help you find the right one.

## Examples

### 1. Single-function package — human-readable duration (ms)

```json
{ "package": "ms", "args": [86400000] }
```

Result: `"1d"` — `ms` exports one function, so `method` is not needed.

---

### 2. Named method on a namespace package (lodash)

```json
{ "package": "lodash", "method": "camelCase", "args": ["hello world"] }
```

Result: `"helloWorld"`

---

### 3. Passing an array argument — chunk (lodash)

```json
{ "package": "lodash", "method": "chunk", "args": [[1, 2, 3, 4, 5], 2] }
```

Result: `[[1,2],[3,4],[5]]`

---

### 4. Passing an options object — slugify

```json
{ "package": "slugify", "args": ["Hello World & Friends!", { "lower": true }] }
```

Result: `"hello-world-and-friends"`

---

### 5. Scoped package — GeoJSON bounding box (@turf/turf)

```json
{
  "package": "@turf/turf",
  "method": "bbox",
  "args": [{
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [2.3522, 48.8566] },
    "properties": {}
  }]
}
```

Result: `[2.3522, 48.8566, 2.3522, 48.8566]`

---

### 6. Date formatting (date-fns)

```json
{ "package": "date-fns", "method": "format", "args": ["2026-03-13T00:00:00.000Z", "dd MMM yyyy"] }
```

Result: `"13 Mar 2026"`

---

### 7. UUID generation (uuid)

```json
{ "package": "uuid", "method": "v4" }
```

Result: `"550e8400-e29b-41d4-a716-446655440000"` (random each call)

---

### 8. Discover available methods on an unfamiliar package

Pass a non-existent method name and the error response lists callable methods:

```json
{ "package": "change-case", "method": "???" }
```

Error response includes: `Available: camelCase, capitalCase, constantCase, dotCase, kebabCase, noCase, pascalCase, pathCase, sentenceCase, snakeCase`

Then call the one you need:

```json
{ "package": "change-case", "method": "snakeCase", "args": ["Hello World"] }
```

Result: `"hello_world"`

## Notes

- Args are **native JSON** — pass numbers as numbers, not strings: `[60000]` not `["60000"]`.
- First call for a package installs it on the server; expect a few seconds of latency.
- Cache is LRU-bounded (default 500 MB on the hosted server). Packages in active use are never evicted.
- Package names follow standard npm rules (`@scope/name` or `name`). Arbitrary shell characters are rejected.
- Not intended for production critical paths — designed for utility and convenience calls during development.
