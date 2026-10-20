---
name: agent-tool-mcp-builder
description: Designs agent tools and builds MCP servers (tool schemas, naming, error shapes, auth, context-efficient results) when exposing capabilities to an LLM agent or scaffolding a Model Context Protocol server.
when_to_use: User is building an MCP server, defining tools/function schemas for an agent, or fixing tools that the model misuses, returns bloated results, or mis-routes. NOT for general REST/GraphQL APIs for humans (use rest-graphql-contract).
---

## When to Use

Reach for this when an LLM agent — not a human — is the caller:

- Scaffolding an **MCP server** (stdio or streamable HTTP) that exposes tools/resources/prompts.
- Defining **tool / function-call schemas** for a model (the `input_schema`, descriptions, result shape).
- **Fixing tools the model misuses**: wrong tool picked, args malformed, results so large they blow the context window, or the model can't tell success from failure.

NOT for human-facing REST/GraphQL APIs — those optimize for client devs and stable contracts, not for a model reading schemas at inference time. Use `rest-graphql-contract` there.

Core mental model: **the model is your end user.** It reads only the tool name + description + param schema before deciding. Every result it gets back consumes context it pays for. Design for "a smart reader who sees the schema and nothing else."

## Steps

1. **Pick transport + deployment before writing tools.**
   - **stdio** (subprocess, JSON-RPC over stdin/stdout) — local single-user tools, the default for desktop/CLI agent clients. No auth layer; the OS process boundary is the trust boundary. The host spawns one process per client, so concurrency = multiple independent processes (see step 6).
   - **Streamable HTTP** — remote/multi-tenant, web-hosted. Needs real auth (below) and must handle concurrent requests in one process.
   - Never log to **stdout** on a stdio server — stdout is the JSON-RPC channel and any stray `print` corrupts the protocol. Log to **stderr** only.

2. **Choose auth by deployment, not by habit.**
   - stdio local → **none** (process isolation). Read secrets from env vars the host injects; never take API keys as tool params (they land in model context + transcripts).
   - Remote internal → **static bearer / API key** in the `Authorization` header.
   - Remote multi-user → **OAuth 2.0**; keep token refresh server-side. The model never sees the credential — your server injects it at egress when calling the downstream API.

3. **Name and scope tools for a model picking from a list.**
   - `verb_noun`, specific: `search_orders`, `create_invoice` — not `orders`, `do`, `query`. The name is the model's primary routing signal.
   - **One tool = one job.** A `manage_users(action=create|delete|list)` mega-tool forces the model to get `action` right *and* shapes a vague schema. Split into `create_user` / `delete_user` / `list_users` so each gets a tight schema and a name the model can match.
   - Keep the active set **focused** (rough ceiling ~20–40 well-named tools). Past that, the model mis-routes. If you have a large library, expose a search/discovery tool and load schemas on demand rather than dumping all of them into context.
   - **bash vs. dedicated tool:** a `bash`/`run_command` tool gives breadth but an opaque string the host can't gate, render, or parallelize. Promote an action to a **dedicated tool** when you need to: gate it (irreversible/external — `send_email`, `delete_*`), enforce an invariant (reject an edit if the file changed since last read), render custom UI, or mark it parallel-safe (read-only `glob`/`grep`). Rule: start with bash for reach, promote when you must gate/render/audit/parallelize.

4. **Write the param schema and description for the model.**
   - JSON Schema `input_schema`: `type:"object"`, `properties` with a `description` on **every** field, `required` listing only truly-required params, `enum` for fixed value sets, `additionalProperties:false`.
   - Descriptions are **prescriptive about *when* to call**, not just what the tool does — e.g. *"Call this when the user asks about current order status or recent shipments."* On models that reach for tools conservatively, trigger conditions in the description measurably raise should-call rate. Put the same trigger in the tool description itself, not only the system prompt.
   - Set `strict: true` (or the server's strict-schema equivalent) when the downstream call needs exact params — it constrains the model's args to the schema instead of validating after the fact.
   - **Tool name/type pairs are load-bearing** for built-in/server tools — `text_editor_20250728` pairs with name `str_replace_based_edit_tool`; mixing a type with the wrong name 400s. Match your versioned tool `type` to its expected `name`.

5. **Make results discriminated and errors actionable.**
   - Return a **discriminated shape** the model can branch on: a `status: "ok" | "error" | "empty"` (or typed result variants), never a bare string the model has to pattern-match.
   - On failure, return the error **as a tool result with an error flag set** (`is_error: true` on the result block) and an **actionable message** — *"Location 'xyz' not found. Provide a valid city name."* — not an exception that kills the loop, and not a silent empty result. The model reads the message and retries or asks; a stack trace or `null` teaches it nothing.
   - Validate inputs **inside** the tool before doing work; surface validation failures the same way so the model can correct its own args.

6. **Trim results for context efficiency — this is where most tool servers fail.**
   - **Default to summaries.** Add a `summary`/`detail` mode and a `limit`; return aggregates + top-N, not full dumps. A tool that returns 5K rows of JSON burns thousands of tokens the model rarely needs. (Mirror of the read-tool convention: `summary=true` unless individual rows are required.)
   - **Paginate** large lists (`cursor`/`page` + `limit`); never return an unbounded set.
   - For **large/tabular** payloads, prefer **CSV or YAML over JSON** — same data, far fewer tokens (no repeated keys/braces). Reserve JSON for small structured results the model branches on.
   - **Offload huge outputs to a file/handle**: if a result would exceed a large threshold (tens of K tokens), write it to a path/resource and return a **preview + the handle** so the model can fetch the slice it needs. (Hosted toolsets do this automatically past ~100K tokens — replicate the pattern.)
   - **Programmatic / composed calls:** when the model would otherwise chain N tool calls (each result hitting its context), let it run a script that calls tools as functions and returns only the final output — intermediate results never enter context. Worth it for sequential calls or large filtered-down intermediates.

7. **Handle concurrency safely for the transport.**
   - stdio: the host spawns **one subprocess per client** — within a process, JSON-RPC requests can interleave, so don't hold shared mutable state across `await` points without guarding it; do hold per-request state on the stack.
   - HTTP: multiple concurrent requests share **one** process — make handlers reentrant, use connection pools (don't open a DB connection per call), and never stash request-scoped data in module globals.
   - Mark read-only tools as parallel-safe where the framework allows; serialize anything with side effects.

8. **Add observability + rate limiting (remote especially).**
   - Log each call's tool name, arg keys (not secret values), latency, and result size to **stderr / your logger** — never stdout on stdio.
   - Rate-limit per-caller on remote servers; return a clear retryable error (with retry guidance) on limit, so the agent backs off instead of hammering.

9. **Test with the MCP inspector, then verify the model actually calls it right.**
   - Run the server under the **MCP inspector** (`npx @modelcontextprotocol/inspector <server-cmd>`) — confirm tools enumerate, schemas validate, and a hand-entered call returns the expected discriminated shape and error shape.
   - Then close the loop with a real model: give it a task that *should* trigger the tool and confirm it (a) picks the right tool, (b) fills args validly, (c) gets a result small enough to act on. A tool that passes the inspector but the model never calls (or always mis-calls) is not done — fix the **name/description**, not the prompt.

## Common Errors

- **Logging to stdout on a stdio server.** Any `print`/`console.log` corrupts the JSON-RPC stream and the client silently breaks. Everything diagnostic goes to **stderr**.
- **Returning raw, unbounded results.** The #1 context killer. 5K rows of pretty-printed JSON = thousands of wasted tokens. Add `summary`/`limit`/pagination and prefer CSV/YAML for tabular data **before** shipping.
- **Mega-tools with an `action` discriminator.** `manage_x(action=...)` makes the model get both the action and a loose schema right. Split into one tool per action.
- **Vague names / what-not-when descriptions.** `query`, `data`, `do` give the model nothing to route on. A description that says *what* the tool does but not *when to call it* leaves the model guessing — and newer models under-call by default, so the trigger condition has to be explicit.
- **Errors as exceptions or silent nulls.** An exception ends the agent loop; a `null`/empty result looks like success. Return a result with the error flag set + an actionable message so the model can recover.
- **API keys as tool parameters.** They land in model context and the transcript/event history. Inject credentials server-side from env/vault at egress; the model never sees them.
- **Mismatched versioned tool name/type pair** (built-in tools). The `type` and `name` are a fixed pair — swapping one without the other 400s.
- **Per-call DB connections / shared mutable state on HTTP servers.** Concurrent requests share the process; use pools and keep request state off module globals.
- **Schema drift the model can't see.** Changing return shape without updating the description means the model branches on a contract that no longer holds. Keep the description and the actual result shape in sync.

## Verify

- [ ] Transport chosen deliberately (stdio = local/no-auth; HTTP = remote/+auth); secrets come from env/vault, **never** from tool params.
- [ ] Every tool: `verb_noun` name, single responsibility, description states **when to call**, `input_schema` has a `description` on each field + `enum`/`required`/`additionalProperties:false`.
- [ ] Results are discriminated (`status`/typed variants); errors return an error-flagged result with an actionable message — not exceptions, not silent nulls.
- [ ] Large results trimmed: summary mode + pagination + limit; CSV/YAML for tabular; oversized output offloaded to a handle with a preview.
- [ ] Concurrency safe for the transport (no stdout logging on stdio; pooled connections + reentrant handlers on HTTP).
- [ ] Rate limiting + per-call logging (to stderr/logger) in place on remote servers.
- [ ] **Passed the MCP inspector** (tools enumerate, schemas validate, success + error shapes correct) **and** a real model picks the right tool, fills valid args, and gets a context-sized result.
