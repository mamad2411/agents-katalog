---
name: mongodb-mcp-server
description: guidance for using the mongodb mcp server for direct mongodb database inspection in clients that expose mongodb tools. use when chatgpt needs to confirm or switch an existing connection, inspect databases and collections, query data, explain performance, export results, use mongodb knowledge search, or troubleshoot direct mongo connection issues without relying on atlas-specific workflows. adapt to the actual tool surface exposed by the running client instead of assuming every mongodb mcp capability is available.
---

# MongoDB MCP Server

Use this skill for direct MongoDB server work.
Treat Atlas, Atlas Local, and Assistant features as out of scope unless the user explicitly asks for them.

This skill must adapt to the actual MongoDB MCP tools exposed by the running environment. Do not assume the full server catalog is available. In this workspace, the currently exposed MongoDB tool surface is effectively read-only and includes metadata, query, export, diagnostics, knowledge search, and `switch-connection`, but not `connect`, config/debug resources, or write tools.

## Core operating stance

- Prefer direct database tools first.
- Prefer an already active or environment-configured connection over passing a connection string during the chat session.
- Prefer read and metadata operations first.
- State the active connection, database, and collection before querying or mutating.
- When the user asks for a write, explain that the current client does not expose write tools.
- If a tool is unavailable, adapt to the exposed tool surface instead of assuming the server is broken.

## Connection rules

Use this order:

1. Check whether there is already an active connection by attempting a harmless metadata call such as `list-databases`.
2. If the server was started with `MDB_MCP_CONNECTION_STRING`, prefer reusing that connection.
3. Use `switch-connection` when the user wants to move from one MongoDB deployment or environment to another and that tool is exposed.
4. Do not promise runtime `connect` in this client unless the tool is visibly exposed.
5. After switching connections, reuse that same connection for the rest of the task.

Important guidance:

- Do not ask the user to paste secrets into normal chat unless there is no safer option in their MCP client.
- If `connect` is not exposed, direct connection setup must come from the MCP server configuration or an existing active connection.
- If diagnostic resources like `debug://mongodb` or `config://config` are not exposed, rely on the available tool outputs and error messages instead.
- Treat this client as inspection-first: avoid describing mutation workflows as if they are runnable here.

## Default workflow for direct MongoDB tasks

### 1) Establish or confirm the connection

- `list-databases` to confirm an active connection when possible
- `switch-connection` when the user explicitly wants a different deployment

In this client, assume the connection already exists unless `switch-connection` is used.

### 2) Discover the namespace

- `list-databases`
- `list-collections`
- `collection-schema`
- `collection-indexes`
- `collection-storage-size`
- `db-stats`

Use these before writing queries when the collection shape is not already known.

### 3) Read and analyze

- `count` for quick volume checks
- `find` for sample documents or targeted retrieval
- `aggregate` for grouped metrics, reshaping, joins, or multi-stage analysis
- `explain` for query-plan and performance evidence
- `mongodb-logs` for recent server-side events or failures

### 4) Export

- `export` when the user needs a saved result set or handoff
- use the returned `exported-data://...` URI or local export path when the client provides one

### 5) Write requests in this client

This client does not currently expose write tools.

When the user asks to create, update, delete, rename, or drop data:

- explain that the current MongoDB MCP surface is read-only
- avoid describing write commands as if they are immediately runnable here
- if useful, explain that writes would require a different MCP configuration or client exposure

## Sample prompts for each tool and resource

Use these as patterns. Rewrite them to fit the user's actual database names, collection names, filters, and limits.

### Connection and switching

- `list-databases`: `Confirm the active MongoDB connection by listing the available databases.`
- `switch-connection`: `Switch from the staging MongoDB connection to production and confirm which connection is now active.`

### Discovery and metadata

- `list-databases`: `List all databases on the current MongoDB connection.`
- `list-collections`: `Show me all collections in the sales database.`
- `collection-schema`: `Inspect the schema for sales.orders so I can see the common fields and types.`
- `collection-indexes`: `List the indexes on sales.orders and tell me which ones support order lookup by customerId and createdAt.`
- `collection-storage-size`: `How large is the sales.orders collection? Show the storage size in MB.`
- `db-stats`: `Show database stats for sales so I can understand document counts and storage usage.`

### Reads and analysis

- `count`: `Count how many orders in sales.orders have status \"pending\".`
- `find`: `Find 10 recent orders in sales.orders where status is \"pending\" and show orderId, customerId, total, and createdAt.`
- `aggregate`: `Aggregate sales.orders to show total revenue by month for the last 12 months.`
- `explain`: `Run an explain plan for finding orders by customerId and createdAt in sales.orders.`
- `mongodb-logs`: `Show the most recent MongoDB server log events related to failed queries or connection problems.`

### Export

- `export`: `Export the result of the pending orders query from sales.orders to JSON so I can download or inspect it later.`
- `exported-data://{exportName}` or local path: `Open the returned export resource or file path for the last orders export so I can inspect the saved JSON.`

### Write requests

- `write limitation`: `This MongoDB MCP client currently exposes read/query/export tools but not write tools, so I can inspect the target data and explain the exact mutation you would run once writes are enabled.`

### Diagnostic resources

- `mongodb-logs`: `Show the most recent MongoDB server log events related to failed queries or connection problems.`
- `config://config` when exposed: `Read the MCP server config resource and tell me whether readOnly mode or disabled tools are preventing writes.`
- `debug://mongodb` when exposed: `Read the MongoDB debug resource and explain why the latest connection attempt failed.`

### MongoDB knowledge tools

- `list-knowledge-sources`: `List the MongoDB knowledge sources available in the assistant knowledge base.`
- `search-knowledge`: `Search the MongoDB knowledge base for Atlas Search operator syntax or aggregation guidance.`

## Query planning rules

- Run `collection-schema` before writing non-trivial filters or projections against an unfamiliar collection.
- Run `collection-indexes` before giving performance advice.
- Use `explain` when recommending index changes or query rewrites.
- Prefer `count` over a full `find` when only totals are needed.
- Prefer `find` for spot checks before `update-many` or `delete-many`.
- Prefer `aggregate` when the user asks for grouped summaries, funnels, or cross-field computations.

## Troubleshooting rules

When tools fail or behavior is unexpected:

1. Start with available metadata calls such as `list-databases` or `list-collections` to distinguish connection issues from empty data.
2. Read `debug://mongodb` if that resource is exposed.
3. Read `config://config` if that resource is exposed.
4. If writes are unavailable, assume the current MCP environment does not expose them rather than promising mutation support.
5. If connection switching is unavailable, assume the connection must come from startup configuration.
6. Distinguish clearly between connection failure, authentication failure, authorization failure, empty collections, and tool suppression.
7. Remember that an empty collection can make `collection-schema` return no inferred schema even when the collection exists.

## Response pattern

When reporting results after tool use, include:

1. active connection used
2. database and collection, if applicable
3. tool or sequence of tools used
4. key result in plain language
5. caveats such as read-only mode, disabled tools, empty collections, missing indexes, limits, or skipped writes

## Bundled references

- See `references/tool-catalog.md` for the direct-connection MongoDB tool inventory.
- See `references/setup-and-safety.md` for connection setup and troubleshooting guidance.
- See `references/live-tool-surface.md` for the currently observed MongoDB MCP runtime in this client.
- See `evals/evals.json` for starter evaluation prompts for this skill.
