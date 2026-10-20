---
name: kb-mcp
description: Portable reference for building MCP (Model Context Protocol) servers — not grounded in this repo. Invoke when designing an MCP server's tool/resource/prompt surface, choosing a transport (stdio / SSE / WebSocket), or reviewing MCP security and Claude Desktop wiring.
last-verified: 2026-04-23
---

# MCP — Model Context Protocol Server Reference

> **Scope:** building MCP servers (tools, resources, prompts) that AI clients can consume.
> **Not grounded in this repo.** TimeKast Factory does not publish MCP servers — this skill loads in projects that do.

---

## 1. What is MCP?

**Model Context Protocol** — a standard for connecting AI systems with external tools and data sources.

| Concept       | Purpose                      |
| ------------- | ---------------------------- |
| **Tools**     | Functions AI can call        |
| **Resources** | Data AI can read             |
| **Prompts**   | Pre-defined prompt templates |

---

## 2. Server architecture

### Minimal project structure

```
my-mcp-server/
├── src/
│   └── index.ts      # Main entry (server bootstrap)
├── package.json
└── tsconfig.json
```

### Transport selection

| Transport     | Use when                                     |
| ------------- | -------------------------------------------- |
| **Stdio**     | Local, CLI-based, Claude Desktop wiring      |
| **SSE**       | Web-based, streaming (one-way server→client) |
| **WebSocket** | Real-time, bidirectional                     |

> Default to stdio for Claude Desktop integration; switch to SSE/WS only when the transport capability matters.

---

## 3. Tool design — principles

| Principle         | Description                                    |
| ----------------- | ---------------------------------------------- |
| Clear name        | Action-oriented (`get_weather`, `create_user`) |
| Single purpose    | One thing, done well                           |
| Validated input   | Schema with types AND descriptions             |
| Structured output | Predictable, JSON-parseable                    |

### Input schema — required fields

| Field       | Required?              |
| ----------- | ---------------------- |
| Type        | Yes — `object`         |
| Properties  | Define every parameter |
| Required    | List mandatory params  |
| Description | Human-readable         |

> The AI relies on the schema description to decide when to call the tool. Write descriptions for a smart colleague, not for yourself.

---

## 4. Resource patterns

| Type     | Use                       | Example URI        |
| -------- | ------------------------- | ------------------ |
| Static   | Fixed data (config, docs) | `docs://readme`    |
| Dynamic  | Generated on request      | `status://health`  |
| Template | URI with parameters       | `users://{userId}` |

### URI conventions

| Pattern       | Example             |
| ------------- | ------------------- |
| Fixed         | `docs://readme`     |
| Parameterized | `users://{userId}`  |
| Collection    | `files://project/*` |

---

## 5. Error handling

| Situation      | Response                       |
| -------------- | ------------------------------ |
| Invalid params | Validation error + message     |
| Not found      | Clear "not found" + identifier |
| Server error   | Generic error, log internals   |

**Best practices:** return structured errors (never raw stack traces), don't expose internal paths, log for debugging, provide actionable messages.

---

## 6. Multimodal handling

| Type   | Encoding           |
| ------ | ------------------ |
| Text   | Plain text         |
| Images | Base64 + MIME type |
| Files  | Base64 + MIME type |

> Validate MIME types on ingress; cap file size at the tool layer to prevent resource exhaustion.

---

## 7. Security principles

### Input validation

- Validate all tool inputs (schema + semantic)
- Sanitize user-provided data before passing to downstream systems
- Limit resource access (filesystem paths, URL allowlists)

### Secrets

- Use environment variables — never inline keys in code
- Don't log secrets (redact in error paths)
- Validate permissions before sensitive operations

---

## 8. Claude Desktop config

| Field   | Purpose               |
| ------- | --------------------- |
| command | Executable to run     |
| args    | Command arguments     |
| env     | Environment variables |

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/absolute/path/to/dist/index.js"],
      "env": { "API_KEY": "..." }
    }
  }
}
```

---

## 9. Testing

| Type        | Focus                  |
| ----------- | ---------------------- |
| Unit        | Tool logic             |
| Integration | Full server end-to-end |
| Contract    | Schema validation      |

---

## 10. Checklist

- [ ] Clear, action-oriented tool names
- [ ] Complete input schemas with descriptions
- [ ] Structured JSON output
- [ ] Error handling for all failure modes
- [ ] Input validation at tool entry
- [ ] Environment-based secrets
- [ ] Logging for debugging (without leaking secrets)
- [ ] Transport matches use case (stdio / SSE / WS)

---

## 11. Anti-patterns

| ❌ Don't                                    | ✅ Do                                       |
| ------------------------------------------- | ------------------------------------------- |
| Omit schema descriptions                    | Describe every param — AI reads these       |
| Return stack traces to the client           | Generic error message, log the stack        |
| Inline API keys in code                     | `env` vars + Claude Desktop config          |
| Build one god-tool with 20 params           | Split into focused single-purpose tools     |
| Skip input validation because "AI is smart" | Validate every input at the boundary        |
| Default to WebSocket "just in case"         | Stdio is enough for most local integrations |

---

> **Remember:** MCP tools should be simple, focused, and well-documented. The AI relies on descriptions to use them correctly.
