---
name: effect-mcp-server
description: Build MCP (Model Context Protocol) servers with Effect using McpServer, McpSchema, Tool, and Toolkit. Use this skill when implementing MCP servers that expose tools, resources, and prompts to LLM clients via stdio or HTTP transports.
---

You are an Effect TypeScript expert specializing in building MCP (Model Context Protocol) servers using Effect's built-in MCP module.

## Effect Source Reference

The Effect v4 source is available at `~/.local/share/opencode/repos/github.com/Effect-TS/effect@main/`.
Inspect `git show effect@4.1.0:<path>` in that checkout for this baseline; main
may be ahead. Keep Effect-family package versions aligned. The MCP/AI APIs remain
`@stability unstable` and can change incompatibly in minor releases.

Reference these files:

- `packages/effect/MCP.md` — primary MCP guide with full examples
- `packages/effect/src/ai/McpServer.ts` — server implementation and API
- `packages/effect/src/ai/McpSchema.ts` — schema types, param helper, error classes

## What is MCP

Model Context Protocol (MCP) is a standard protocol for LLM tool integration. It allows AI clients (Claude, etc.) to discover and invoke tools, read resources, and use prompt templates exposed by a server. Effect provides a first-class MCP server implementation built on its Layer and Schema systems.

## Core Imports

```typescript
import { Cause, Context, Effect, Layer, Logger } from 'effect';
import { Schema } from 'effect';
import { McpProtocol, McpServer, McpSchema, Tool, Toolkit } from 'effect/ai';
```

For platform-specific transports:

```typescript
// Node.js stdio transport
import { NodeRuntime, NodeSink, NodeStream } from '@effect/platform-node';

// Or using NodeStdio
import { NodeRuntime, NodeStdio } from '@effect/platform-node';
```

## Architecture Overview

Merge resource, prompt, and toolkit registration layers, then pass them to the
transport's `registrations` option:

```typescript
const registrations = Layer.mergeAll(...resources, ...prompts, toolkitLayer);
const Server = McpServer.layerStdio({
  name: 'My Server',
  version: '1.0.0',
  protocols: [McpProtocol.v2025_11_25],
  registrations
}).pipe(Layer.provide(loggingLayer));
```

Handler service reads are request dependencies. Supply them through MCP middleware
(or HTTP router middleware for HTTP transports). To use a construction-time
service, capture it with `Layer.unwrap` and close over it in handlers; ordinary
`Layer.provide` cannot discharge `McpRequest<"Requires", S>` markers.

Every server runner requires a non-empty `protocols` option. Put the preferred fallback revision first; an exact initialization offer is selected when present, otherwise the first adapter is used where the transport permits fallback. `initialize` negotiates from its body even when the client sends an unsupported default protocol header. Subsequent requests validate `MCP-Protocol-Version`; unsupported explicit versions return `400`. Let initialization reach body negotiation.

## Protocol Revisions

Declare the protocol adapters the server supports:

```typescript
const protocols = [
	McpProtocol.v2026_07_28,
	McpProtocol.v2025_11_25,
	McpProtocol.v2025_06_18,
	McpProtocol.v2025_03_26,
	McpProtocol.v2024_11_05
] as const;
```

- `2024-11-05` and `2025-03-26` are compatibility revisions.
- `2025-06-18` supports form elicitation.
- `2025-11-25` adds sampling with tools, independently advertised form/URL elicitation modes, descriptor icons, and elicitation-complete notifications.
- `2026-07-28` is available as `McpProtocol.v2026_07_28`; it uses stateless
  request-scoped execution rather than the older initialized-session lifecycle.
- Duplicate versions or an empty protocol declaration fail layer construction with `Cause.IllegalArgumentError`.
- `v2024_11_05` over `layerHttp` uses Effect's single-endpoint Streamable HTTP compatibility transport. It does not recreate the historical two-endpoint HTTP+SSE transport, GET SSE, event resumption, session expiry, or client session termination.

Each part layer has type `Layer.Layer<never, never, ...>` — they register themselves with the McpServer service and produce no output type.

For HTTP requests without a protocol header, an existing session's negotiated
revision is used, not the first configured revision. Invalid version/session
requests return JSON-RPC error bodies. Keep missing headers distinct from an
explicitly unsupported revision.

## Tools and Toolkit

Server options accept `instructions` for initialization/discovery. Prompt
registration accepts `title`; callbacks receive decoded prompt parameters.

`Tool.Strict` controls MCP input schema generation and argument validation.
Strict tools reject unknown keys; non-strict tools ignore them during decoding.
Both report all missing/invalid fields together (`errors: 'all'`), including
unknown keys for strict tools. Strict dynamic tools require Effect schemas;
raw JSON Schema cannot supply runtime strict validation and is rejected at registration.

Parameters must encode to a JSON Schema with `type: 'object'` at the root. Use
`Schema.Class` or `Schema.Struct`, or omit parameters/use `Tool.EmptyParams` for
parameterless tools. Identified object schemas are supported: the adapter inlines
top-level references for input/output schemas and form elicitation, retaining
referenced definitions. It does not turn primitive result types into objects.

Nonrecursive named roots are no longer duplicated in `$defs` after inlining;
recursive definitions are retained. Do not construct custom root-relative `$ref`
paths into a duplicate root definition that may now be absent.

Tool failure projection depends on the negotiated protocol:

| Failure | 2024-11-05 through 2025-06-18 | 2025-11-25 and 2026-07-28 |
| --- | --- | --- |
| Invalid arguments | `-32602 Invalid params` | `isError: true` tool result |
| Internal handler/encoding failure | `-32603 Internal error` | `isError: true` tool result |
| Declared tool failure | `isError: true` tool result | `isError: true` tool result |

Declared failures omit `structuredContent`; an error with an empty `message`
uses its encoded failure value rather than returning empty text. Internal defects
and encoding failures are reported internally with generic client-facing messages.

Success projection is also version-specific. The 2024-11-05/2025-03-26 adapters
omit structured output. The 2025-06-18/2025-11-25 adapters expose object-root
output schemas and object-valued `structuredContent`, omitting primitive/array
structured values. The 2026-07-28 adapter supports JSON-valued structured output.
When a protocol omits string structured content, a single text block that exactly
mirrors its JSON encoding is unquoted to plain text; other text blocks are preserved.

### Defining Tools

Tools are defined with `Tool.make` specifying a name, description, parameter schemas, and success schema:

<!-- typecheck -->
```typescript
import * as Schema from 'effect/Schema';
import { Tool } from 'effect/ai';

const GreetTool = Tool.make('GreetTool', {
	description: 'Generate a greeting message',
	parameters: Schema.Struct({
		name: Schema.String,
		style: Schema.Union([
			Schema.Literal('formal'),
			Schema.Literal('casual')
		])
	}),
	success: Schema.String
});

const CalculatorTool = Tool.make('CalculatorTool', {
	description: 'Perform basic arithmetic',
	parameters: Schema.Struct({
		operation: Schema.Union([
			Schema.Literal('add'),
			Schema.Literal('subtract'),
			Schema.Literal('multiply'),
			Schema.Literal('divide')
		]),
		a: Schema.Number,
		b: Schema.Number
	}),
	success: Schema.Number
});

const NotifyTool = Tool.make('NotifyTool', {
	description: 'Send an optional notification',
	parameters: Schema.Struct({
		message: Schema.String,
		channel: Schema.optionalKey(Schema.String)
	}),
	success: Schema.Void
});
```

MCP callers may omit fields declared with `Schema.optionalKey`; do not assume the protocol sends an `arguments` object containing every field. A `Schema.Void` tool may return `Effect.void`; `undefined` is a successful tool result, not an internal error.

### Creating a Toolkit

Group tools into a `Toolkit`:

```typescript
const MyToolkit = Toolkit.make(GreetTool, CalculatorTool);
```

### Registering with McpServer

`McpServer.toolkit(toolkit)` creates a layer that registers the toolkit. Implementations are provided via `Toolkit.toLayer`:

```typescript
const ToolkitLayer = McpServer.toolkit(MyToolkit).pipe(
	Layer.provideMerge(
		MyToolkit.toLayer({
			GreetTool: ({ name, style }) => {
				const greeting =
					style === 'formal' ? `Good day, ${name}.` : `Hey ${name}!`;
				return Effect.succeed(greeting);
			},
			CalculatorTool: ({ operation, a, b }) => {
				switch (operation) {
					case 'add':
						return Effect.succeed(a + b);
					case 'subtract':
						return Effect.succeed(a - b);
					case 'multiply':
						return Effect.succeed(a * b);
					case 'divide':
						return Effect.succeed(a / b);
				}
			}
		})
	)
);
```

The pattern is always: `McpServer.toolkit(tk).pipe(Layer.provideMerge(tk.toLayer({...})))`.

Registration tracks `Tool.HandlerServices<Tools[keyof Tools]>`, including
parameter-decoding and result-encoding services, not just explicitly declared
tool dependencies. Provide these services as well as the handler layer.
Request context services are supplied by the transport and excluded from the
registration layer's external requirements.

### MCP Tool Annotations

Effect tool annotations are emitted as MCP tool hints:

- `Tool.Readonly` → `readOnlyHint`, default `false`
- `Tool.Destructive` → `destructiveHint`, default `true`
- `Tool.Idempotent` → `idempotentHint`, default `false`
- `Tool.OpenWorld` → `openWorldHint`, default `true`
- `Tool.Title` → annotation title; 2025-06-18 and 2025-11-25 preserve it in
  `tools/list` alongside the descriptor's top-level title and behavioral hints

These hints help clients decide how to present tools, but they are not authorization decisions. Always enforce access control in your server handlers.

## Resources

### Static Resources

Expose a fixed URI resource:

```typescript
const ReadmeResource = McpServer.resource({
	uri: 'file:///README.md',
	name: 'README',
	description: 'Project README file',
	mimeType: 'text/markdown',
	content: Effect.succeed('# My Project\n\nProject documentation.')
});
```

The `content` field is an `Effect` that can produce a `string`, `Uint8Array`, or a `ReadResourceResult`.

### Parameterized Resource Templates

Use tagged template literals with `McpSchema.param` for dynamic URIs:

```typescript
const idParam = McpSchema.param('id', Schema.NumberFromString);

const UserResource = McpServer.resource`file://users/${idParam}.json`({
	name: 'User Data',
	description: 'User information by ID',
	completion: {
		id: (_input: string) => Effect.succeed([1, 2, 3, 4, 5])
	},
	content: Effect.fn(function* (_uri, id) {
		return JSON.stringify({ id, name: `User ${id}` }, null, 2);
	}),
	mimeType: 'application/json'
});
```

Key points:

- `McpSchema.param(name, schema)` creates a named URI parameter with automatic codec (e.g. `Schema.NumberFromString` for path segments)
- `completion` provides auto-completion values for each parameter
- `content` receives `(uri, ...params)` — the full URI string followed by decoded parameter values
- `audience` can be `["assistant"]`, `["user"]`, or `["assistant", "user"]`

Resource-template requirements include both parameter decoding **and encoding**,
content services, and completion services. Completion handlers may accept a
second `CompletionContext` argument; `CompletionServices` includes requirements
from optional handlers too. Do not erase these requirements with assertions.

## Prompts

Define reusable prompt templates:

```typescript
const AnalysisPrompt = McpServer.prompt({
	name: 'Analyze Data',
	description: 'Analyze data and provide insights',
	parameters: {
		dataType: Schema.String,
		focus: Schema.Union([
			Schema.Literal('summary'),
			Schema.Literal('details')
		])
	},
	completion: {
		dataType: () => Effect.succeed(['sales', 'users', 'metrics']),
		focus: () => Effect.succeed(['summary', 'details'])
	},
	content: ({ dataType, focus }) =>
		Effect.succeed(
			`Please analyze the ${dataType} data and provide a ${focus} analysis.`
		)
});
```

- `parameters` uses `Schema.Struct.Fields` (same as Schema.Struct field definitions)
- `completion` provides auto-complete values per parameter
- `content` receives the decoded parameters and returns `Effect<string | Array<PromptMessage>>`

Prompt registration likewise propagates parameter decoding, encoding for
parameters with completions, and completion-handler requirements in addition to
content services. Reuse the inferred layer type instead of annotating away
service-dependent codecs.

## Elicitation

`McpServer.elicit` requests form-based structured input from the current client and decodes accepted content:

```typescript
const result = McpServer.elicit({
	message: `Please answer ("yes" | "no"):`,
	schema: Schema.Struct({
		answer: Schema.Union([Schema.Literal('yes'), Schema.Literal('no')])
	})
}).pipe(
	Effect.catchTag('ElicitationDeclined', () =>
		Effect.succeed({ answer: 'no' as const })
	)
);
```

- Returns `Effect<S["Type"], ElicitationDeclined, McpServerClient | S["DecodingServices"]>`
- Handle `ElicitationDeclined` with `catchTag` for fallback behavior
- If the user cancels, the effect is interrupted
- Identified object schemas (including named `Schema.Class` values) are accepted;
  the requested form still has to fit the negotiated revision's supported field shapes.
- The negotiated client must advertise form elicitation. In `2025-11-25`, an empty `elicitation` capability is treated as form support; explicit `elicitation.form` and `elicitation.url` capabilities are otherwise gated independently.

URL elicitation is a `2025-11-25` reverse-client operation. Use the scoped client facade, then notify that specific client when the external flow completes:

```typescript
const mcpClient = yield* McpSchema.McpServerClient;
const reverseClient = yield* mcpClient.getClient;

const response = yield* reverseClient.elicit(
	new McpSchema.ElicitRequestURLParams({
		mode: 'url',
		message: 'Authorize access',
		elicitationId: 'authorization-1',
		url: 'https://example.com/authorize'
	})
);

const server = yield* McpServer.McpServer;
yield* server.notifyElicitationComplete({
	clientId: mcpClient.clientId,
	elicitationId: 'authorization-1'
});
```

### Sampling With Tools

Server-initiated sampling is available through the same scoped reverse client. The `tools`, `toolChoice`, `tool_use`, and `tool_result` shapes require `2025-11-25` and a client that advertises `sampling.tools`; Effect rejects unsupported requests before sending them.

```typescript
const mcpClient = yield* McpSchema.McpServerClient;
const reverseClient = yield* mcpClient.getClient;

const sampled = yield* reverseClient.createMessage(
	McpSchema.CreateMessage.payloadSchema.make({
		messages: [
			McpSchema.SamplingMessage.make({
				role: 'user',
				content: McpSchema.TextContent.make({ text: 'What is the weather?' })
			})
		],
		tools: [
			new McpSchema.Tool({
				name: 'weather',
				inputSchema: {
					type: 'object',
					properties: { city: { type: 'string' } },
					required: ['city']
				}
			})
		],
		toolChoice: new McpSchema.ToolChoice({ mode: 'required' }),
		maxTokens: 128
	})
);
```

The reverse client also gates `includeContext` on `sampling.context`. Unsupported reverse operations fail with `McpReverseOperationUnsupported`; projection or transport failures use `McpReverseOperationError`.

## Icons And Server Metadata

Server runners accept `description`, `websiteUrl`, and `icons`. Icons use `McpSchema.Icon` with `src` plus optional `mimeType`, `sizes`, and `theme`:

```typescript
const serverIcon = new McpSchema.Icon({
	src: 'https://example.com/server.svg',
	mimeType: 'image/svg+xml',
	sizes: ['48x48', 'any'],
	theme: 'dark'
});
```

`McpSchema.Resource`, `McpSchema.ResourceTemplate`, `McpSchema.Prompt`, and `McpSchema.Tool` also accept `icons`. Add descriptor icons through the low-level `McpServer` registration surface (`addResource`, `addResourceTemplate`, `addPrompt`, or `addTool`); the high-level `resource`, `prompt`, and Effect `Toolkit` adapters do not currently expose an icon option. Revisions that do not support icons omit them during protocol projection.

## Transport Layers

### stdio Transport

For CLI-based MCP servers (most common — used by Claude Desktop, etc.):

```typescript
// The Stdio requirement is satisfied by NodeStdio.layer
McpServer.layerStdio({
  name: 'My Server',
  version: '1.0.0',
  protocols: [McpProtocol.v2025_11_25],
  registrations: Layer.mergeAll(/* resource, prompt, and toolkit layers */)
}).pipe(
  Layer.provide(NodeStdio.layer),
  Layer.provide(Layer.succeed(Logger.LogToStderr)(true))
);
```

For stdio transport, route logs to stderr with `Logger.LogToStderr`. Stdout is
reserved for protocol messages. `Logger.consolePretty` controls formatting;
the context reference controls its destination.

With a stateful protocol configured, pre-initialization stdio `ping` returns an
empty result without creating a session, even when a stateless adapter is listed first.

### HTTP Transport

For web-based MCP servers using Streamable HTTP:

```typescript
McpServer.layerHttp({
	name: 'My MCP Server',
	version: '1.0.0',
	path: '/mcp',
	protocols: [McpProtocol.v2025_11_25]
});
```

- Requires `HttpRouter.HttpRouter` in the context
- Implements single-endpoint Streamable HTTP with JSON-RPC
- The `path` parameter sets the HTTP endpoint path
- For stateful revisions, non-`initialize` HTTP requests with no session id return
  `400`; an unknown `Mcp-Session-Id` returns `404`. Keep and resend the session id
  from initialization. The 2026-07-28 stateless adapter uses request metadata instead.
- `allowSessionTermination: true` enables DELETE for stateful sessions. Successful
  termination returns `204`, interrupts active requests, and later use of the
  session ID returns `404`. Disabled or stateless-only endpoints return `405`.
- `allowSubscriptions: false` disables modern subscriptions and discovery
  `listChanged` support; the current request's progress/log notifications still
  work. This is independent of session termination.
- A POST whose reply-bearing calls were all canceled returns empty `200` SSE;
  another unexpectedly response-less POST is an internal `500`, not that same
  cancellation outcome.

### Request-scoped HTTP for serverless hosts

Use `layerHttpRequestScoped` when server execution must belong to an HTTP
request, for example on Workers. It takes only stateless protocol adapters
(currently `v2026_07_28`); a stateful adapter is a type error, or an
`IllegalArgumentError` for untyped input. Its options include server metadata,
`path`, `protocols`, `extensions`, and `allowedOrigins`, but not the long-lived
transport's session/subscription toggles.

Each POST owns execution through response-body completion. Registration is
shared, but request services take precedence over captured layer services. Tools,
resources, prompts, completions, multi-round input requests, and request-local
progress/logs work. Legacy reverse `elicit`, subscriptions, broadcasts, and
DELETE do not; discovery advertises `listChanged: false`. Use `layerHttp` on a
long-lived host when those features or sessions are required.

<!-- typecheck -->
```ts
import { McpProtocol, McpServer, Tool, Toolkit } from 'effect/ai';
import * as Effect from 'effect/Effect';
import * as Layer from 'effect/Layer';
import * as Schema from 'effect/Schema';

const Tools = Toolkit.make(Tool.make('Greet', {
  parameters: Schema.Struct({ name: Schema.String }),
  success: Schema.String
}));
const Endpoint = McpServer.layerHttpRequestScoped({
  name: 'Greetings',
  version: '1.0.0',
  path: '/mcp',
  protocols: [McpProtocol.v2026_07_28],
  registrations: McpServer.toolkit(Tools).pipe(
    Layer.provideMerge(Tools.toLayer({ Greet: ({ name }) => Effect.succeed(`Hello, ${name}`) }))
  )
});
// Provide Endpoint to the host's HttpRouter composition; do not launch a daemon per request.
```

### Transport requirements

All transports accept server metadata, nonempty `protocols`, optional `extensions`,
`cacheHints`, and a `registrations` layer. Registration construction errors and
services propagate into the transport layer. Built-in request services are
supplied by the transport; remaining request dependencies must be provided by
middleware. HTTP layers expose remaining request requirements through
`HttpRouter.Request` markers.

| Transport | Runtime requirement | Additional options |
| --- | --- | --- |
| `layerStdio` | `Stdio` | No HTTP route |
| `layerHttp` | `HttpRouter.HttpRouter` | `path`, `allowedOrigins`, `allowSessionTermination`, `allowSubscriptions` |
| `layerHttpRequestScoped` | `HttpRouter.HttpRouter` | `path`, `allowedOrigins`; sessionless protocols only |

`cacheHints: { tools: { ttl: '1 minute', cacheScope: 'private' } }` sets discovery
freshness for `v2026_07_28`. Without hints, results retain zero TTL and private
scope. `resources/read` always retains that default.

## Client Capabilities

Access the connecting client's capabilities from within tool/resource handlers:

```typescript
const caps = yield* McpServer.clientCapabilities;
// caps: ClientCapabilities
```

`McpServer.visibility` can hide registrations per request using middleware-provided
services. Visibility middleware also runs on list requests, once per registration;
`MiddlewareMethod` includes list methods. Duplicate local/global middleware runs
once. `McpTest.makeClient` tests registrations in memory over JSON-RPC encoding.

## Conditional Tool/Resource/Prompt Enabling

Use `McpSchema.EnabledWhen` to conditionally list prompts, resources, resource templates, or tools based on initialized client data. The filter runs against the client initialization payload.

```typescript
import { Context, Effect, Layer } from 'effect';
import { Schema } from 'effect';
import { McpSchema, McpServer, Tool } from 'effect/ai';

const requiresRoots = Context.make(
	McpSchema.EnabledWhen,
	(client) => client.capabilities.roots !== undefined
);

const ReadWorkspace = Tool.make('ReadWorkspace', {
	description: 'Read workspace roots when the client supports roots',
	success: Schema.String
}).annotateMerge(requiresRoots);

const WorkspacePrompt = McpServer.prompt({
	name: 'Workspace Summary',
	description: 'Summarize workspace roots',
	annotations: requiresRoots,
	content: () => Effect.succeed('Summarize the available workspace roots.')
});

const WorkspaceResource = Layer.effectDiscard(
	McpServer.registerResource({
		uri: 'workspace://roots',
		name: 'Workspace Roots',
		annotations: requiresRoots,
		content: Effect.succeed('[]')
	})
);
```

## Relationship to OpenAI MCP Tools

`McpServer` exposes a server that MCP clients connect to over stdio or HTTP. `OpenAiTool.Mcp` is different: it is an OpenAI provider-defined tool that lets an OpenAI model call a remote MCP server. When using OpenAI's hosted MCP integration, use the canonical `OpenAiMcp` custom name from `OpenAiTool.Mcp` and handle provider approval flow through normal tool approval request/response parts.

For your application to connect directly instead, use experimental
`effect/ai/McpClient` and `McpClientError`. The client supports `2025-11-25` and
`2026-07-28` over stdio/HTTP with an explicit revision and scoped lifetime;
`McpClient.toolkit(client, prefix?)` bridges discovered tools into an Effect AI
toolkit. This is not the server's scoped reverse-client facade. Read the tagged
client source before choosing transport/initialization options, and enforce local
authorization for discovered remote capabilities.

## JSON boundaries

MCP metadata/capability records now check object shape shallowly and expose
unknown values (`Readonly<Record<string, unknown>>`) rather than promising
recursive `Schema.Json` validation. Modern `structuredContent` can be unknown
at the schema boundary. Decode method/domain payloads explicitly; shallow
acceptance does not make arbitrary values JSON-serializable. Server tool-result
serialization still rejects non-JSON output.

`McpSchema.JsonRpcRequest`, `JsonRpcNotification`, `JsonRpcResponse`, and
`JsonRpcMessage` validate envelopes, not arbitrary method payloads: `params`,
`result`, and error `data` need their own schema decoding.

## Complete Example — stdio Server

```typescript
import { NodeRuntime, NodeStdio } from '@effect/platform-node';
import { Effect, Layer, Logger } from 'effect';
import { Schema } from 'effect';
import { McpProtocol, McpSchema, McpServer, Tool, Toolkit } from 'effect/ai';

// --- Tools ---
const GreetTool = Tool.make('GreetTool', {
	description: 'Generate a greeting',
	parameters: Schema.Struct({ name: Schema.String }),
	success: Schema.String
});

const MyToolkit = Toolkit.make(GreetTool);

// --- Resources ---
const ReadmeResource = McpServer.resource({
	uri: 'file:///README.md',
	name: 'README',
	mimeType: 'text/markdown',
	content: Effect.succeed('# Demo MCP Server')
});

const idParam = McpSchema.param('id', Schema.NumberFromString);

const ItemResource = McpServer.resource`file://items/${idParam}`({
	name: 'Item',
	completion: { id: () => Effect.succeed([1, 2, 3]) },
	content: Effect.fn(function* (_uri, id) {
		return JSON.stringify({ id, name: `Item ${id}` });
	}),
	mimeType: 'application/json'
});

// --- Prompts ---
const HelpPrompt = McpServer.prompt({
	name: 'Help',
	description: 'Get help on a topic',
	parameters: { topic: Schema.String },
	completion: { topic: () => Effect.succeed(['setup', 'usage', 'api']) },
	content: ({ topic }) => Effect.succeed(`Help me understand ${topic}`)
});

// --- Server ---
const Registrations = Layer.mergeAll(
	ReadmeResource,
	ItemResource,
	HelpPrompt,
	McpServer.toolkit(MyToolkit).pipe(
		Layer.provideMerge(
			MyToolkit.toLayer({
				GreetTool: ({ name }) => Effect.succeed(`Hello, ${name}!`)
			})
		)
	)
);
const ServerLayer = McpServer.layerStdio({
  name: 'Demo MCP Server',
  version: '1.0.0',
  protocols: [McpProtocol.v2025_11_25],
  registrations: Registrations
}).pipe(
	Layer.provide(NodeStdio.layer),
	Layer.provide(Logger.layer([Logger.consolePretty()])),
	Layer.provide(Layer.succeed(Logger.LogToStderr)(true))
);

Layer.launch(ServerLayer).pipe(NodeRuntime.runMain);
```

## Common Patterns

### Tool with effectful implementation

```typescript
const FetchTool = Tool.make('FetchData', {
	description: 'Fetch data from database',
	parameters: Schema.Struct({ id: Schema.String }),
	success: Schema.String
});

const FetchToolkit = Toolkit.make(FetchTool);

// Tool handler can use services from the context
McpServer.toolkit(FetchToolkit).pipe(
	Layer.provideMerge(
		FetchToolkit.toLayer({
			FetchData: ({ id }) =>
				Effect.gen(function* () {
					const db = yield* DatabaseService;
					const result = yield* db.findById(id);
					return JSON.stringify(result);
				})
		})
	)
);
```

### Multiple toolkits

```typescript
const ServerLayer = Layer.mergeAll(
	McpServer.toolkit(ReadToolkit).pipe(
		Layer.provideMerge(
			ReadToolkit.toLayer({
				/* ... */
			})
		)
	),
	McpServer.toolkit(WriteToolkit).pipe(
		Layer.provideMerge(
			WriteToolkit.toLayer({
				/* ... */
			})
		)
	)
	// resources and prompts...
);
```

### Resource content from Effect services

```typescript
const ConfigResource = Layer.unwrap(Effect.gen(function* () {
  const config = yield* ConfigService;
  return McpServer.resource({
    uri: 'app://config',
    name: 'App Config',
    content: config.getAll().pipe(Effect.map(JSON.stringify))
  });
}));
```

## Key Rules

1. **Merge registrations** — combine resource, prompt, and toolkit layers with `Layer.mergeAll`.
2. **Pass registrations to the transport** — `McpServer.layerStdio({ ..., registrations })` or the corresponding HTTP layer.
3. **stderr for stdio** — Never log to stdout when using stdio transport
4. **Toolkit pattern** — `McpServer.toolkit(tk).pipe(Layer.provideMerge(tk.toLayer({...})))` is the canonical pattern
5. **Schema for parameters** — `Tool.make` takes a schema with an encoded object
   root, not a raw field record. `McpServer.prompt` still takes a field record;
   resource template parameters take individual codecs.
6. **`McpSchema.param`** — Use for resource URI template parameters with automatic string codec
7. **`Effect.fn`** — Use for resource template content handlers that receive multiple arguments
8. **Launch with `Layer.launch`** — The server runs as a long-lived layer: `Layer.launch(ServerLayer).pipe(NodeRuntime.runMain)`
9. **Declare protocols explicitly** — Pass a non-empty `protocols` array to every `run`, `layer`, `layerStdio`, or `layerHttp`; put the fallback revision first
10. **Gate reverse operations by negotiated capabilities** — Sampling tools and URL elicitation are `2025-11-25` features and fail before transport when unsupported
