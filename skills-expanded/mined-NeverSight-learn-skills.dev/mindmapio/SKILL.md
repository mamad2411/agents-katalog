---
name: mindmapio
description: >
  Drive Mindmap.io maps directly over its HTTP node API: list and
  read maps, build node subtrees with client-minted ids, and run the generative
  node operations (submit, auto-expand, retry, interrupt). Use when the user
  wants to create or grow a mindmap.io map, run prompts on nodes, fan a node out
  into follow-ups, or read a map/branch programmatically without the MCP server.
trigger: >
  User asks to build, read, or generate on a mindmap.io map from an agent — e.g.
  "create a map", "add a node and run it", "auto-expand this node", "read my
  map" — and prefers calling the API directly over installing the MCP server.
---

# Drive Mindmap.io maps via the node API

This skill teaches you to drive [Mindmap.io](https://mindmap.io) maps by calling
its HTTP node API directly. It is the alternative to the `mindmapio-mcp` server:
same primitives, no MCP client required, just authenticated HTTP calls.

The API is the authoritative contract — match the shapes in the examples
exactly. A map's `data` is a tree of nodes, the same shape every read returns,
with camelCase fields like `nodeType` and `parentId`. The single-node write
endpoints take their own snake_case fields like `node_type`.

## Setup

Every call sends a personal access token as a bearer header. Generate the token
once in Mindmap.io: settings → API access. It acts as its user; regenerating it
immediately revokes the old one.

```bash
export MINDMAP_API_TOKEN="<your personal access token>"
export MINDMAP_API_BASE_URL="https://mindmap.io"   # optional, this is the default
```

Never print, echo, or commit the token. Send it on every request:

```
Authorization: Bearer $MINDMAP_API_TOKEN
```

A reusable curl alias for the examples below:

```bash
mm() { curl -sS -H "Authorization: Bearer $MINDMAP_API_TOKEN" \
  -H "Content-Type: application/json" "$MINDMAP_API_BASE_URL$@"; }
```

## Primitives

IDs are unprefixed everywhere. You mint node ids client-side, so you can
reference a node id you chose before it is persisted.

Node content is sent as `messages`: a UIMessage array (Vercel AI SDK shape).
Each message is `{role, parts}` and each part is `{type: "text", text}`. A
node's body — a prompt, a data node, a note's source turn — is a single `user`
message with one or more text parts.

### Read

**List maps** — `GET /api/mindmaps` → array of `{id, title, kind, created_at, updated_at}`, newest first.

```bash
mm /api/mindmaps
```

**Read a full map** — `GET /api/mindmaps/{id}` → `{id, title, kind, user_id, data}` where `data` is `{rootId, selectedId, nodes}` and `nodes` maps id → node.

```bash
mm /api/mindmaps/MAP_ID
```

**Read one node** — `GET /api/mindmaps/{mapId}/nodes/{nodeId}` → a `SubtreeNode` `{node, children}` with `children: []`. The node's own `children` array still lists child ids for navigation.

```bash
mm /api/mindmaps/MAP_ID/nodes/NODE_ID
```

**Read a subtree** — `GET /api/mindmaps/{mapId}/nodes/{nodeId}/subtree?depth=N` → nested `SubtreeNode`. Omit `depth` for the full subtree; `0` returns just the node, `1` the node and its immediate children.

```bash
mm "/api/mindmaps/MAP_ID/nodes/NODE_ID/subtree?depth=2"
```

### Structural write

**Create a map** — `POST /api/mindmaps` with `{title?, kind?, data?}`. Pass an initial `data` tree with a root node so later node primitives have a parent to hang from. → `201 {id, title?, kind?}`.

Each node has a type. A `data` node holds content you keep — a topic, reference text, a note. A `prompt` node is a question you run against a model with `submit`. The root usually holds the map's subject, so make it a `data` node:

```bash
mm /api/mindmaps -X POST -d '{
  "title": "My research map",
  "data": {
    "rootId": "root",
    "nodes": {
      "root": {
        "id": "root",
        "nodeType": "data",
        "messages": [{ "role": "user", "parts": [{ "type": "text", "text": "Topic" }] }],
        "children": []
      }
    }
  }
}'
```

**Create a node** — `POST /api/mindmaps/{mapId}/nodes` with `{nodeId, parentId, position?, data?}`. `nodeId` must be unique within the map; mint a uuid yourself. `data` may carry `{messages, note, node_type}`, where `messages` is the node's content as a UIMessage array. The node is born structural (a draft); running it is a separate generative call. → `201` full node.

```bash
mm /api/mindmaps/MAP_ID/nodes -X POST -d '{
  "nodeId": "q1",
  "parentId": "root",
  "data": {
    "messages": [{ "role": "user", "parts": [{ "type": "text", "text": "What is X?" }] }],
    "node_type": "prompt"
  }
}'
```

A data or note node carries its body the same way — a `user` message in `messages`:

```bash
mm /api/mindmaps/MAP_ID/nodes -X POST -d '{
  "nodeId": "d1",
  "parentId": "root",
  "data": {
    "messages": [{ "role": "user", "parts": [{ "type": "text", "text": "Reference notes for the branch." }] }],
    "node_type": "data"
  }
}'
```

**Update a node** — `PATCH /api/mindmaps/{mapId}/nodes/{nodeId}` with any subset of `{messages, note, node_type, is_collapsed, model_provider, model_id}`. Send `messages` to replace the node's content. Pure tree mutation, no LLM call, no metering. → `200 {success}`.

```bash
mm /api/mindmaps/MAP_ID/nodes/q1 -X PATCH -d '{
  "messages": [{ "role": "user", "parts": [{ "type": "text", "text": "What is X, precisely?" }] }]
}'
```

**Delete a node** — `DELETE /api/mindmaps/{mapId}/nodes/{nodeId}`. Cascades to descendants and reindexes siblings. The root cannot be deleted. → `200 {success}`.

```bash
mm /api/mindmaps/MAP_ID/nodes/q1 -X DELETE
```

**Delete a map** — `DELETE /api/mindmaps/{id}` → `200 {success}`.

```bash
mm /api/mindmaps/MAP_ID -X DELETE
```

### Generative

**Submit a node** — `POST /api/mindmaps/{mapId}/nodes/{nodeId}/submit` with optional `{prompt?, modelId?}`. Runs the LLM and **blocks** until no ancestor is still generating, then returns the completed node `{nodeId, status, messages}`. `prompt` supplies the user text when the node has none yet; omit it to run the stored text. `modelId` overrides the house model. Metered; over budget returns `429`.

```bash
mm /api/mindmaps/MAP_ID/nodes/q1/submit -X POST -d '{}'
```

**Auto-expand a node** — `POST /api/mindmaps/{mapId}/nodes/{nodeId}/auto-expand` with optional `{count?, direction?}` (`count` 1–4, default 2). Generates follow-up prompts as `queued` child nodes and returns `{nodeId, childIds}`. **One level only** — it does NOT run the children. Metered; over budget `429`.

```bash
mm /api/mindmaps/MAP_ID/nodes/q1/auto-expand -X POST -d '{"count": 3}'
```

**Retry a node** — `POST /api/mindmaps/{mapId}/nodes/{nodeId}/retry?force=true` with optional `{prompt?, modelId?}`. Clears the prior error and re-runs, returning `{status, messages}`. Retrying an expand node that already has children returns `409` unless `force=true` (which deletes those children first). Metered; over budget `429`.

```bash
mm "/api/mindmaps/MAP_ID/nodes/q1/retry?force=true" -X POST -d '{}'
```

**Interrupt a node** — `POST /api/mindmaps/{mapId}/nodes/{nodeId}/interrupt`. A `generating` or `queued` node flips to `interrupted` with partial output preserved. Idempotent; not metered. → `200` final node.

```bash
mm /api/mindmaps/MAP_ID/nodes/q1/interrupt -X POST
```

## Pattern: agent-drives-recursion for auto-expand

Auto-expand does NOT recurse and does NOT run the children it creates — it only
queues one level of follow-up prompts. You drive the recursion: call
`auto-expand`, then `submit` each returned child yourself, and recurse if you
want to go deeper.

```bash
# 1. Fan a completed node out into queued follow-up children.
resp=$(mm /api/mindmaps/MAP_ID/nodes/q1/auto-expand -X POST -d '{"count": 3}')

# 2. Submit each returned child to run it (each blocks on its ancestors).
echo "$resp" | jq -r '.childIds[]' | while read -r child; do
  mm "/api/mindmaps/MAP_ID/nodes/$child/submit" -X POST -d '{}'
done

# 3. To go deeper, auto-expand a child and repeat. Choose your own depth/breadth
#    budget — there is no server-side recursion or fan-out cap beyond count 1-4.
```

Submit blocks until ancestors finish, so it is safe to submit children in
sequence; the generation gate guarantees each child sees complete parent
context.

## Errors

Responses carry `{error}` on failure. Common statuses: `401` (no/revoked
token), `403` (not the token user's map), `404` (missing map/parent/node), `400`
(malformed, or deleting the root), `409` (duplicate node id, or re-expanding
without `force`), `429` (over budget — body carries an upgrade/buy-credits CTA).
On `429`, stop generating and surface the CTA rather than retrying blindly.

## Hello world

```bash
# create a map whose root is a data node holding the topic
MAP=$(mm /api/mindmaps -X POST -d '{"title":"Hello","data":{"rootId":"root","nodes":{"root":{"id":"root","nodeType":"data","messages":[{"role":"user","parts":[{"type":"text","text":"Hello"}]}],"children":[]}}}}' | jq -r '.id')
# add a prompt node under the root, then run it
mm /api/mindmaps/$MAP/nodes -X POST -d '{"nodeId":"q1","parentId":"root","data":{"messages":[{"role":"user","parts":[{"type":"text","text":"Say hi in one word."}]}],"node_type":"prompt"}}'
# run it and read the answer back
mm /api/mindmaps/$MAP/nodes/q1/submit -X POST -d '{}'
```

For the MCP-server route instead, see the project README.
