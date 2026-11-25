---
name: mcp-servers
description: Builds, secures and tests Model Context Protocol (MCP) servers - choosing MCP vs a CLI or API, tools, resources and prompts, stdio vs Streamable HTTP transport, task-shaped tool design, logging rules, OAuth for remote servers, input validation, testing with the MCP Inspector, and versioning. Use when creating or reviewing an MCP server, exposing an API or database to AI agents through MCP, or debugging an MCP server that fails to connect, hangs or confuses the model. Not for designing the agent loop itself (use building-agents).
license: MIT
---

# MCP Servers

An MCP server is an API whose user is a model. Design a few task-shaped tools with clear descriptions and concise results, keep the protocol stream clean, validate everything, and give the server only the privileges its tools need.

The protocol evolves through dated spec versions. **Before writing code, read the current specification and SDK docs at modelcontextprotocol.io**, and follow them where they differ from this skill.

## When to use

- Exposing a service, database, internal API or local capability to AI agents and assistants.
- Reviewing an MCP server for security or usability.
- An MCP server won't connect, hangs, or the model keeps calling its tools wrongly.

## MCP or something else?

| Situation | Choose |
|---|---|
| Many different AI clients (IDEs, chat apps, agents) should use the same capability | MCP server |
| The agent already has a shell and a good CLI exists | Often just the CLI, documented in a skill or instructions |
| One app calling one API from your own code | Call the API directly as a tool in that app |
| Read-mostly reference content | MCP resources, or plain files/docs the agent can read |

## Primitives

| Primitive | Controlled by | Use for |
|---|---|---|
| Tools | The model decides when to call | Actions and queries: search, create, update, run |
| Resources | The application/user decides what to attach | Read-only context identified by URI: files, records, schemas |
| Prompts | The user picks them (often as slash commands) | Reusable, parameterized prompt templates for workflows |

Clients may also offer capabilities to servers (for example sampling, roots, elicitation). Use them only if the clients you target support them; check the spec and client docs.

## Transports

| Transport | Use for | Notes |
|---|---|---|
| stdio | Local servers launched by the client as a subprocess | Simplest. The client owns the process lifetime. |
| Streamable HTTP | Remote or shared servers | Needs authentication, TLS, and Origin checks. |
| HTTP+SSE (older) | Legacy only | Deprecated in favor of Streamable HTTP. Don't build new servers on it. |

**stdio rule: stdout carries protocol messages only.** Any `print`, `console.log` or library banner on stdout corrupts the stream and breaks the connection. Send all logs to stderr (or a log file, or the protocol's logging messages).

For local HTTP servers, bind to `127.0.0.1`, not `0.0.0.0`, and validate the `Origin` header to block DNS-rebinding attacks.

## Workflow

1. **List the user tasks** the server should support ("find a customer's open tickets", "create a draft invoice"). Design tools around tasks, not around your API's endpoints.
2. **Pick the SDK.** Official SDKs exist for TypeScript and Python (the Python SDK includes the high-level FastMCP API) and for several other languages; check modelcontextprotocol.io for the current list and API. Don't hand-roll JSON-RPC.
3. **Define each tool**: name, description, JSON Schema input, result shape, errors, side effects. Run it through [references/tool-design-checklist.md](references/tool-design-checklist.md).
4. **Implement** with input validation, timeouts on downstream calls, pagination, and error results the model can act on.
5. **Choose transport and auth.** stdio for local use with credentials from environment variables or the OS keychain; Streamable HTTP plus OAuth for remote use.
6. **Test with the MCP Inspector** (`npx @modelcontextprotocol/inspector <command to start your server>`): list tools, call each one with valid, invalid and edge-case inputs, and check the raw messages.
7. **Test with a real client and model** on a set of realistic requests. Read which tools the model picks and with what arguments; fix descriptions where it goes wrong.
8. **Document** installation, configuration (env vars, scopes), each tool, and the permissions the server needs.
9. **Publish or deploy** only after the user approves; it's outward-facing.

## Tool design essentials

- **Few, high-level tools.** A model handles 5-15 well-designed tools better than 60 endpoint wrappers. Combine multi-call sequences into one tool.
- **Descriptions are the documentation**: what it does, when to use it, when not to, parameter meanings with examples, side effects.
- **Strict input schemas**: types, `required`, enums, formats, bounds. Validate again in code; the schema is a hint to the model, not a guarantee.
- **Concise results**: relevant fields only, readable names next to IDs, pagination with a cursor and a "more results" note, truncation of large text.
- **Errors as tool results**: report tool execution failures as a result with the error flag set (`isError: true`) and a message saying how to fix the call, so the model can recover. Reserve protocol errors for protocol problems (unknown tool, malformed request).
- **Annotations** (such as read-only, destructive, idempotent hints) help clients decide when to ask for confirmation. They are hints from the server, so clients shouldn't trust them from unknown servers, and your server must still enforce safety itself.
- Newer spec versions support structured tool output with an output schema; use it when clients consume results programmatically and the client supports it.

## Security

- **Least privilege**: the server's credentials can do only what its tools need. Prefer read-only tools; make write tools explicit and narrow.
- **Authorization for remote servers**: follow the MCP authorization spec (OAuth 2.1-based) for the protocol version you target; read the current version before implementing. Validate that access tokens were issued for your server (audience). Don't pass the client's token through to upstream APIs; obtain your own upstream credentials.
- **Per-user scoping**: every tool call checks that the authenticated user may access the requested data. Never trust user IDs passed as tool arguments.
- **Validate inputs** against injection: parameterized SQL, no shell string building, paths confined to allowed roots (resolve and check for `..`), URL allowlists for fetches (prevent SSRF).
- **Destructive operations** (delete, send, pay, deploy) should be separate tools, marked destructive, and designed so the client asks the user first. Consider a dry-run/preview step.
- **Untrusted content**: data your tools return (web pages, tickets, emails, documents) may contain prompt-injection text. Return it as data, don't add instructions around it, and don't let content from one source trigger privileged actions.
- **Secrets**: from environment variables or a secret store, never in tool descriptions, results or logs.
- **Limits**: timeouts, result size caps, and rate limits per user.

## Versioning and compatibility

- The client and server negotiate a protocol version at initialization. Support the versions your target clients use, and test with each important client.
- Treat tool names and input schemas as a public API: add optional parameters freely, but don't rename tools or remove or retype parameters without a new tool name or a major version.
- Keep a changelog; note which spec version and SDK version you build against.

## Debugging

| Symptom | Check |
|---|---|
| Client can't connect (stdio) | Something writes to stdout; the command path or interpreter is wrong; missing env vars. Run the exact command from the client config in a terminal. |
| Connection drops or hangs | Unhandled exception in a handler, a blocking call without timeout, or a crash logged only to stderr. Check stderr/client logs. |
| Tool never called | Vague name or description, or overlap with another tool. |
| Wrong arguments | Missing parameter descriptions/examples, IDs the model can't know, loose schema. |
| Model gets lost after a call | Result too large or unstructured; add pagination and trim fields. |

## Anti-patterns

- **One tool per REST endpoint** - the model has to orchestrate many calls and picks wrong ones.
- **Logging to stdout** on a stdio server.
- **Returning raw API payloads** thousands of tokens long.
- **Exceptions instead of error results** - the model can't recover.
- **Admin credentials** for a server that mostly reads.
- **Trusting tool arguments** for identity or permissions.
- **Building on HTTP+SSE** for new remote servers.
- **Coding from memory of an old spec** instead of reading the current one.

## Done when

- Tools are task-shaped, pass the checklist, and were exercised in the Inspector with valid, invalid and edge-case inputs.
- A real client and model used the tools correctly on realistic requests.
- stdout is clean on stdio; remote servers use Streamable HTTP with authorization per the current spec, TLS and Origin validation.
- Inputs are validated, user access is checked per call, credentials are least-privilege, and destructive tools are separated and marked.
- The README documents setup, configuration, each tool, required permissions, and the targeted spec version.

## References

- [references/tool-design-checklist.md](references/tool-design-checklist.md) - read when defining or reviewing tools.
