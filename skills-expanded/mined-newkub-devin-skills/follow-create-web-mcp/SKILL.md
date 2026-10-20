---
name: follow-create-web-mcp
description: Add WebMCP tools to a web page via document.modelContext so agents can discover and invoke them
argument-hint: "[feature-or-tool-name]"
related:
  - follow-create-web
  - follow-create-mcp
  - use-agent-browser
  - use-chrome-devtools
  - deep-review-codebase
  - deep-research
  - follow-best-practice
  - deep-validate
---

## Goal

Add WebMCP tools to a web page/web app (page-provided tools that agents discover and invoke via `document.modelContext`) — the page acts like "an MCP server inside a client-side script" instead of an external process

## Scope

- Page (producer) side only — implement/register tools in an existing or new web app
- Boundary with related skills:
  - External MCP server (a stdio/HTTP process the client spawns) → `/follow-create-mcp`
  - Consuming/invoking WebMCP on an existing page → `/use-agent-browser` (`webmcp list`/`invoke`)
  - Inspecting/debugging the browser during development → `/use-chrome-devtools`
  - Choosing a framework / creating a new web project → `/follow-create-web`
- WebMCP is an experimental spec (W3C Web Machine Learning CG draft) — the declarative form-based API is still a spec TODO → use the imperative API and always research first
- Browser support: Chrome launch flag only (`agent-browser` enables it by default, `--no-webmcp` disables it) — Safari/Firefox/remote providers aren't supported yet → the page must work fully without WebMCP

## Execute

### 1. Research Spec

> Goal: Confirm the latest API before writing code — the spec is a draft and can change

1. Run `/deep-research` + `/follow-best-practice` — sources: `https://webmachinelearning.github.io/webmcp/` (spec) and `https://agent-browser.dev/webmcp` (consumer reference)
2. Confirm the current shape of `document.modelContext` and the status of the declarative API before implementing

### 2. Design Tool Surface

> Goal: Decide what to expose to agents

1. Start with read/query tools (`readOnlyHint: true`) — e.g. search, get-state, filter; add mutation tools only when necessary
2. `name`: 1-128 chars, only `[A-Za-z0-9_.-]` — use verb_noun such as `search_products`, `cart.add`
3. `description`: state when/how to use it plainly — the agent reads the description to decide whether to call it; never include hidden instructions or prompt injection
4. `inputSchema`: a JSON Schema object — keep only the fields that are needed (over-parameterization is a privacy risk per spec §6.3.3)
5. `annotations`: `readOnlyHint`, `consequentialHint`, `untrustedContentHint`, `debugging` — set them to match the real behavior

### 3. Implement Registration

> Goal: Register tools with the correct lifecycle

1. Always feature-detect first: `if (!('modelContext' in document)) return` — the API is a SecureContext (requires HTTPS/localhost)
2. Register when the document is fully active (DOM ready or framework mount) — registering too early raises `InvalidStateError`
3. `document.modelContext.registerTool({ name, title, description, inputSchema, execute, annotations }, { signal })` — keep the `AbortController` to unregister at teardown or on SPA route change
4. `execute: async (inputObject, { signal }) => {...}` — always validate input in the callback (inputSchema isn't enforced), honor `signal` for cancellation, return a JSON-serializable result
5. Cross-origin iframe tools: `registerTool(tool, { exposedTo: [origins] })`; in-page agents query with `getTools({ fromOrigins: [...] })`

### 4. Safety And UX

> Goal: Keep tools safe for both the agent and the user

1. Consequential actions (payment, delete, irreversible) → `consequentialHint: true` + a real UI confirmation — the agent may trigger them unintentionally (spec §6.3.2)
2. Output containing third-party/user-generated content → `untrustedContentHint: true`
3. `title` should be localized to the user's language for the browser UI
4. Never leak session/auth/private data through tool output — tools run in the user's authenticated context (spec §6.3.4)
5. Embedders that don't want the page to register tools → use the Permissions-Policy `tools=()`

### 5. Fallback

> Goal: The page stays fully functional without WebMCP

1. WebMCP is an enhancement — the regular UI must cover every flow; tools call the same app logic as the UI handlers, no separate logic
2. Never assume the agent will use WebMCP — pages that haven't registered anything always expose `tools: []`

### 6. Test Discovery And Invocation

> Goal: Verify the agent actually finds and calls the tools

1. Dev server running → `/use-agent-browser`: `agent-browser webmcp list --json` must show the registered tools
2. `agent-browser webmcp invoke <name> --params '{...}'` — test the happy path, invalid input, consequential confirmation, and cancellation
3. Debug the page side with `/use-chrome-devtools`: `evaluate_script` → `await document.modelContext.getTools()` and `list_console_messages` to see registration errors
4. Unit-test the `execute` callback logic separately from registration (WebMCP requires a Chrome flag — e2e via `/run-test e2e` is possible but the feature must be enabled)
5. SPA/iframe: verify tools come up and go down correctly per route via the `toolchange` event

### 7. Ship

> Goal: Review and validate before delivery

1. Run `/deep-review-codebase` — the `review-frontend` and `review-mcp` domains have a `### WebMCP` checklist for reviewing this implementation
2. Run `/deep-validate` then `/ship` per the project flow

## Rules

### 1. Trust Boundary

- Tool metadata (name/description) and output are untrusted input for the agent — write them to match real behavior, never embed instructions
- Agent input is untrusted for the page — validate every field of the `inputObject` in `execute` before processing
- Never auto-execute consequential tools without user-visible confirmation

### 2. Tool Design

- Start read-only — add mutation/consequential tools only with clear justification
- Minimal schema: only necessary required fields, `enum` for bounded values, `title` for display
- Tools should be idempotent where possible — the agent may retry or invoke them repeatedly

### 3. Lifecycle

- Register after the document is fully active; abort the `signal` to unregister on unmount/navigation
- Duplicate `name` within one document → `InvalidStateError` — namespace tools with `.` or `_` when there are multiple widgets

### 4. Formatting

- Never use `**` (bold markers); use backticks for APIs, commands, paths, and skill names
- Report results with `/report`

- Use /follow-create-mcp when needed
- Use /follow-create-web when needed
- Use /use-agent-browser when needed
- Use /use-chrome-devtools when needed

## Expected Outcome

- `agent-browser webmcp list` sees every registered tool
- `agent-browser webmcp invoke` works correctly across success, error, and cancel paths
- The page is fully functional on browsers that don't support WebMCP
- Consequential tools have `consequentialHint` + complete user confirmation
- Passes `/deep-review-codebase` and `/deep-validate`
