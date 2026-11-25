---
name: go-mcp
description: Use when building an MCP server in Go with mark3labs/mcp-go — tools, resources, prompts, transports, structured errors.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [go-essentials, mcp-protocol, go-slog]
---

# Go MCP (mark3labs/mcp-go)

**Iron Law: tool failures return as MCP error CONTENT blocks (`IsError: true`), NEVER as Go errors back through the protocol. Always validate input. Always respect `ctx.Done()`.**

## Server skeleton

```go
import "github.com/mark3labs/mcp-go/server"
import "github.com/mark3labs/mcp-go/mcp"

s := server.NewMCPServer(
    "myserver",                  // name
    "0.1.0",                     // version
    server.WithToolCapabilities(true),
    server.WithResourceCapabilities(true, true),  // (subscribe, listChanged)
    server.WithPromptCapabilities(true),
    server.WithLogging(),
)

// Register tool
s.AddTool(mcp.NewTool("search",
    mcp.WithDescription("Search the index"),
    mcp.WithString("query", mcp.Required(), mcp.Description("user query")),
    mcp.WithNumber("limit", mcp.DefaultNumber(10), mcp.Min(1), mcp.Max(100)),
), searchHandler)

// stdio transport — for desktop clients
if err := server.ServeStdio(s); err != nil { log.Fatal(err) }
```

JSON schema is built from the `mcp.With*` options — sqlc-style. Don't hand-roll the schema; the helpers ensure protocol compliance.

## Tool handler — error contract

```go
func searchHandler(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
    query, err := req.RequireString("query")
    if err != nil {
        return mcp.NewToolResultError(err.Error()), nil   // user error → error content
    }
    limit := req.GetInt("limit", 10)

    results, err := svc.Search(ctx, query, limit)
    if err != nil {
        // Infrastructure failure — also error content, NOT a Go error.
        // Log the raw error server-side; return a generic message. `%v` on a DB/network
        // error leaks SQLSTATE, hostnames, table names to the MCP client (which may be a
        // browser via SSE/HTTP).
        slog.ErrorContext(ctx, "search failed", "err", err, "query", query)
        return mcp.NewToolResultError("search failed (see server logs)"), nil
    }
    return mcp.NewToolResultText(formatResults(results)), nil
}
```

**Returning a non-nil Go error from a handler crashes the MCP framing.** The client sees a protocol-level fault, not a tool failure. Always wrap into `mcp.NewToolResultError(...)` so the model can recover.

## Primitive: tool vs resource vs prompt

| Primitive    | Controller                 | Use for                                                            |
| ------------ | -------------------------- | ------------------------------------------------------------------ |
| **Tool**     | model decides when to call | actions with side effects, on-demand data fetch, computation       |
| **Resource** | client/user attaches       | URI-addressable data the model reads (`file://`, `db://orders/42`) |
| **Prompt**   | user explicitly invokes    | parameterized templates (slash-commands) the user runs             |

If unsure: tool is the default. Promote to resource when the data is browsable; promote to prompt when the user — not the model — initiates it.

## Resources

```go
s.AddResource(mcp.NewResource(
    "config://app/settings",
    "App Settings",
    mcp.WithResourceDescription("Current runtime config"),
    mcp.WithMIMEType("application/json"),
), func(ctx context.Context, req mcp.ReadResourceRequest) ([]mcp.ResourceContents, error) {
    // NEVER marshal the raw config struct — it contains DSNs, API keys, secrets.
    // SafeSettingsView is YOUR function — write a sanitizer that returns a copy
    // with credential fields zeroed or masked. Minimum shape:
    //   func SafeSettingsView(c Config) Config {
    //       c.DatabaseURL = redactDSNPassword(c.DatabaseURL)  // postgres://user:***@host/db
    //       c.StripeSecretKey, c.OpenAIAPIKey = "", ""
    //       return c
    //   }
    safe := SafeSettingsView(currentConfig())
    b, err := json.Marshal(safe)
    if err != nil {
        return nil, fmt.Errorf("marshal settings: %w", err)  // resource handlers CAN return Go errors
    }
    return []mcp.ResourceContents{
        mcp.TextResourceContents{URI: req.Params.URI, MIMEType: "application/json", Text: string(b)},
    }, nil
})
```

For dynamic URIs use `AddResourceTemplate` with `{var}` placeholders. Always set MIME type — clients route on it. **Validate template variables that resolve to filesystem or network paths** — a `file://{path}` template without allow-listing is a path traversal vector.

## Prompts

```go
s.AddPrompt(mcp.NewPrompt("review-pr",
    mcp.WithPromptDescription("Review a PR diff"),
    mcp.WithArgument("pr_url", mcp.RequiredArgument()),
), func(ctx context.Context, req mcp.GetPromptRequest) (*mcp.GetPromptResult, error) {
    url := req.Params.Arguments["pr_url"]
    return mcp.NewGetPromptResult("Review",
        []mcp.PromptMessage{
            mcp.NewPromptMessage(mcp.RoleUser,
                mcp.NewTextContent(fmt.Sprintf("Review %s for correctness, security, perf.", url))),
        },
    ), nil
})
```

## Transports

| Transport                                              | When                                                                                                                |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| **stdio** (`server.ServeStdio`)                        | desktop clients (Claude Desktop, IDE plugins); default                                                              |
| **SSE** (`server.NewSSEServer`)                        | _deprecated since spec 2025-03-26_ — kept for compatibility with older clients; prefer Streamable HTTP for new work |
| **Streamable HTTP** (`server.NewStreamableHTTPServer`) | current spec, single endpoint, request-response + server push; default for network MCP servers                      |

Pick stdio unless you need network access — fewer moving parts, no auth surface.

**If you must use SSE or Streamable HTTP**: wrap the MCP HTTP handler in an auth middleware BEFORE binding to any non-loopback interface. An unauthenticated network-bound MCP server exposes every registered tool, prompt, and resource to anyone on the network. Use `Skill(devkit:go-chi)` for the middleware pattern — at minimum, require a bearer token from a shared secret store (rotate frequently). Minimum wiring:

```go
// authMiddleware and verifyToken are defined per Skill(devkit:go-chi) § auth-middleware
// Signatures (for reference): authMiddleware(func(token string) (user, error)) func(http.Handler) http.Handler
sseHandler := server.NewSSEServer(s).Handler()
protected  := authMiddleware(verifyToken)(sseHandler)
// Bind 127.0.0.1 for desktop use. Bind 0.0.0.0 ONLY after auth + TLS + rate-limit are wired.
if err := http.ListenAndServe("127.0.0.1:8080", protected); err != nil { log.Fatal(err) }
```

The `authMiddleware` factory pattern comes straight from `Skill(devkit:go-chi)`. Bind to `127.0.0.1` for desktop use; bind to a non-loopback address ONLY when the auth layer is in place and the secret-store source is rotation-capable.

## Context cancellation

```go
func slowTool(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
    select {
    case <-ctx.Done():
        return mcp.NewToolResultError("cancelled"), nil
    case res := <-doWork(ctx):
        return mcp.NewToolResultText(res), nil
    }
}
```

If a tool can run > 1s, plumb `ctx` to every downstream call (DB, HTTP) and check `ctx.Done()`. The client cancels frequently — blocking tools hang the session.

## Anti-patterns

- Returning Go errors from handlers (`return nil, err`) — crashes framing; use `mcp.NewToolResultError`
- Missing `mcp.Required()` on inputs the tool needs — runtime nil-deref
- No schema constraints (`Min`, `Max`, `Enum`) — model passes garbage, you panic
- Tools that spawn goroutines without tying them to `ctx` — leaks on cancellation
- Resources without MIME types — clients can't route them
- Blocking I/O in stdio handlers without context check — session hangs
- Logging to stdout in stdio transport — corrupts the JSON-RPC stream; use stderr or `Skill(go-slog)` with a file/journal handler
- Wiring secrets into resource URIs (`db://user:pass@host`) — they leak in client logs

## Red flags

| Thought                                            | Reality                                                                         |
| -------------------------------------------------- | ------------------------------------------------------------------------------- |
| "Return the error, MCP will handle it"             | No. Error CONTENT, not Go error.                                                |
| "stdout is fine for logs"                          | stdio transport uses stdout; you just broke the protocol                        |
| "The model will figure out what arguments to pass" | The schema is the contract — be explicit; constrained inputs = fewer recoveries |
| "I'll add cancellation later"                      | First long tool call = first hung session                                       |

## Hand-off

For the underlying protocol semantics (capability negotiation, JSON-RPC envelope, transports): `Skill(mcp-protocol)`. For structured stderr logging: `Skill(go-slog)`. For request-context plumbing: `Skill(go-essentials)`.
