---
name: mindmapio
description: >
  Drive Mindmap.io maps directly over its HTTP node API: list and
  read maps, build node subtrees with client-minted ids, attach images and PDFs
  to nodes, and run the generative node operations (submit, auto-expand, retry,
  interrupt). It can also pass the user's bug reports and ideas to the
  mindmap.io team. Use when the user wants to create or grow a mindmap.io map, run
  prompts on nodes, fan a node out into follow-ups, or read a map/branch
  programmatically without the MCP server.
trigger: >
  User asks to build, read, or generate on a mindmap.io map from an agent — e.g.
  "create a map", "add a node and run it", "auto-expand this node", "put this
  screenshot on the map", "read my map" — and prefers calling the API directly
  over installing the MCP server.
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

**Create a node** — `POST /api/mindmaps/{mapId}/nodes` with `{nodeId, parentId, position?, data?}`. `nodeId` must be unique within the map; mint a uuid yourself, since reusing one returns `409`. `data` may carry `{messages, note, node_type, color}`, where `messages` is the node's content as a UIMessage array. The node is born structural (a draft); running it is a separate generative call. → `201` full node.

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

**Update a node** — `PATCH /api/mindmaps/{mapId}/nodes/{nodeId}` with any subset of `{messages, note, node_type, is_collapsed, model_provider, model_id, color, position}`. Send `messages` to replace the node's content. Send `position` to move the node among its siblings: it is the 0-based destination index (not a step), the siblings in between shift by one, and the parent never changes, so a retry lands in the same place. A position outside the siblings, or on the root, is a `400`. Pure tree mutation, no LLM call, no metering. → `200 {success}`.

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

### Node color

A node card can carry one of eight pastel tints. Set `color` in `data` on
create or at the top level on update: `rose`, `pink`, `amber`, `sage`, `mint`,
`sky`, `lavender`, `clay`. Send `null` to clear one. Anything outside the
palette is refused.

```bash
mm /api/mindmaps/MAP_ID/nodes/q1 -X PATCH -d '{"color": "amber"}'
mm /api/mindmaps/MAP_ID/nodes/q1 -X PATCH -d '{"color": null}'
```

An uncolored node has no `color` key at all when you read it back, so absence —
not `null` — is how "no color" reads. Coloring is not a content edit: it works
on any node type, and it is never refused by the lock that blocks editing a node
with a settled answer beneath it.

**The color is the user's meaning, not yours.** The product assigns nothing to
any key — people use them to group a branch, flag the threads they want to
return to, or keep two lines of thinking apart. It is presentational: it never
reaches the model, never changes what a node generates, and never encodes status
(the card's border carries that). So set a color when the user asks for one or
has described their scheme, in their terms, and do not invent a legend of your
own. When you reorganize or rebuild part of a map, carry each node's existing
color across — dropping it silently deletes the only thing the field was
holding.

### Attachments

A node can carry images and PDFs alongside its text. It is two steps: send the
bytes to the map, then reference the returned url from a node message. Nothing
here is metered and no model runs on your budget.

**Upload a file** — `POST /api/mindmaps/{mapId}/files`. The body is the file
itself, not a multipart envelope: set `Content-Type` to the file's own media
type and put its percent-encoded name in `X-Filename`. → `201 {id, url,
mediaType, filename, size, altText}`. Accepts `image/png`, `image/jpeg`,
`image/webp`, `image/gif` and `application/pdf`, up to 10 MB each and 5 per
node. A larger file returns `413`, any other type `415`.

This call sets its own headers, so use `curl` directly rather than the JSON `mm`
alias:

```bash
curl -sS -X POST "$MINDMAP_API_BASE_URL/api/mindmaps/MAP_ID/files" \
  -H "Authorization: Bearer $MINDMAP_API_TOKEN" \
  -H "Content-Type: image/png" \
  -H "X-Filename: diagram.png" \
  --data-binary @diagram.png
# → {"id":"att_9f2c1d4e","url":"/api/files/att_9f2c1d4e","mediaType":"image/png",
#    "filename":"diagram.png","size":81234,"altText":"A flowchart of the pipeline…"}
```

Attach it by appending a `file` part to the node's user message, through create
or update node. The `url` the upload returned is what goes in it:

```bash
mm /api/mindmaps/MAP_ID/nodes -X POST -d '{
  "nodeId": "d2",
  "parentId": "root",
  "data": {
    "messages": [{ "role": "user", "parts": [
      { "type": "text", "text": "The pipeline we are discussing." },
      { "type": "file", "mediaType": "image/png", "filename": "diagram.png", "url": "/api/files/att_9f2c1d4e" }
    ] }],
    "node_type": "data"
  }
}'
```

An image is described by the house model as it is uploaded, and that `altText`
is what a model without vision reads in the picture's place. So an attachment
is usable as context for everything below it without any further step.

**Read a file** — `GET /api/files/{attachmentId}` → the raw bytes. Whoever may
read the map may read its files: a published map's attachments are public, the
same file on a private map is owner-only. Save it to disk rather than piping it
into your context — it is an image or a PDF, not JSON.

```bash
mm /api/files/att_9f2c1d4e -o diagram.png
```

### Generative

**Submit a node** — `POST /api/mindmaps/{mapId}/nodes/{nodeId}/submit?force=true` with optional `{prompt?, modelId?}`. Runs the LLM and **blocks** until no ancestor is still generating, then returns the completed node `{nodeId, status, messages}`. `prompt` supplies the user text when the node has none yet; omit it to run the stored text. `modelId` overrides the house model. Submitting a node that already has children returns `409` — re-running it would invalidate the conversations hanging below it — and `force=true` lifts that for an expand node only, deleting its fan-out first. Metered; over budget returns `429`.

```bash
mm /api/mindmaps/MAP_ID/nodes/q1/submit -X POST -d '{}'
# re-run an expand node that has already fanned out, discarding its children
mm "/api/mindmaps/MAP_ID/nodes/q1/submit?force=true" -X POST -d '{}'
```

**Auto-expand a node** — `POST /api/mindmaps/{mapId}/nodes/{nodeId}/auto-expand`, no body. Generates follow-up prompts for the node's thread as `queued` child nodes, one per prompt, and returns `{nodeId, childIds}`. How many is the model's call, read from that thread, so it varies by node; there is nothing to size or steer. A level holds a handful, and wider material comes back grouped, one prompt per group, so its members arrive a level further down when you expand those children in turn. **One level only** — it does NOT run the children. Metered; over budget `429`.

```bash
mm /api/mindmaps/MAP_ID/nodes/q1/auto-expand -X POST -d '{}'
```

**Retry a node** — `POST /api/mindmaps/{mapId}/nodes/{nodeId}/retry?force=true` with optional `{prompt?, modelId?}`. Clears the prior error and re-runs, returning `{status, messages}`. Retrying an expand node that already has children returns `409` unless `force=true` (which deletes those children first). Metered; over budget `429`.

```bash
mm "/api/mindmaps/MAP_ID/nodes/q1/retry?force=true" -X POST -d '{}'
```

**Interrupt a node** — `POST /api/mindmaps/{mapId}/nodes/{nodeId}/interrupt`. A `generating` or `queued` node flips to `interrupted` with partial output preserved. Idempotent; not metered. → `200` final node.

```bash
mm /api/mindmaps/MAP_ID/nodes/q1/interrupt -X POST
```

### Publish

Publishing flips a map from private to public and mints a non-guessable public
id (slug). Owner-only; not metered. This is how you turn a map you built into a
shareable link or an iframe embed.

**Publish a map** — `POST /api/mindmaps/{mapId}/publish`. Mints a public id if
the map has none (re-publishing reuses the existing one) and flips visibility to
public. → `{publicId}`.

```bash
mm /api/mindmaps/MAP_ID/publish -X POST
# → {"publicId":"G_N4wWD2TiUIoHuO"}
```

**Unpublish a map** — `DELETE /api/mindmaps/{mapId}/publish`. Flips back to
private, which immediately `404`s every public/embed link (the revoke
mechanism). The public id is retained for re-publishing. → `{success:true}`.

```bash
mm /api/mindmaps/MAP_ID/publish -X DELETE
```

Build the shareable links from the `publicId`. The query frames the map on first
paint: `node=root`, the semantic `zoom` level (`full` default; `keyword`/`phrase`
open a large **reference** map zoomed-out so its whole shape shows at a glance),
`cz`, the canvas-zoom percent, and optionally `layout` (`tree`, `top-down` or
`both-sides`), which opens the link in that layout without changing the map's.

```
Viewer link:  https://mindmap.io/app/<publicId>?node=root&zoom=<level>&cz=<percent>[&layout=<layout>]
Iframe embed: https://mindmap.io/app/embed/<publicId>?node=root&zoom=<level>&cz=<percent>[&layout=<layout>]
```

So a zoomed-out reference map embeds as
`https://mindmap.io/app/embed/G_N4wWD2TiUIoHuO?node=root&zoom=keyword&cz=90`, and
a normal example/template map as `…?node=root&zoom=full&cz=100`.

> Via the MCP server, `publish_map` does both steps in one call — it publishes
> and returns `{publicId, viewerUrl, embedUrl}` already framed by the
> `zoom`/`cz`/`layout` you pass. `unpublish_map` reverses it.

### Layout

A map has a layout: how its branches are arranged on the canvas. Everyone who
opens the map sees it this way, public and embed links included. It is a view
setting, so the node tree is untouched. Owner-only; not metered.

**Set a map's layout** — `PUT /api/mindmaps/{mapId}/layout` with `{layout}`,
one of `tree` (branches grow right from the root, the default), `top-down`
(branches grow downward, like an org chart) or `both-sides` (the root in the
middle, its branches split left and right). → `{layout}`. An unknown value is
a `400`.

```bash
mm /api/mindmaps/MAP_ID/layout -X PUT -d '{"layout":"top-down"}'
# → {"layout":"top-down"}
```

`get_map` returns the current `layout` with the map. `top-down` reads best for
shallow maps with a few branches per node; `both-sides` suits a central topic
with many first-level branches.

> Via the MCP server, the same call is `set_map_layout` with `{mapId, layout}`.

### Feedback

Pass the user's bug report, idea, or other note to the mindmap.io team. Send it
only when the user asks you to report or pass something on, and write it in
their words: what they did and what happened. It lands in the team's inbox
linked to the token's user, and a reply comes by email from
support@mindmap.io to the account's address. Not metered.

**Send feedback** — `POST /api/feedback` with `{kind, message, context?}`.
`kind` is `bug` (something broken), `idea` (a feature request) or `other`.
`message` is at most 5,000 characters. `context.mapId` names the map it is
about, if any. → `{id}`. It takes five messages in a row, then one a minute;
past that it answers `429`, so wait rather than retry.

```bash
mm /api/feedback -X POST -d '{"kind":"bug","message":"Export to PNG cuts off the right-most branch","context":{"mapId":"MAP_ID"}}'
# → {"id":"…"}
```

> Via the MCP server, the same call is `send_feedback` with `{kind, message, mapId?}`.

### Rename

A map's title follows its root node's prompt until someone names it. Once
renamed, the name stays when the root changes, and shows in the map list and
the browser tab. `list_maps` marks a renamed map with `title_custom: true`.
Owner-only; not metered.

**Rename a map** — `PUT /api/mindmaps/{mapId}/title` with `{title}`, 1 to 100
characters; surrounding whitespace is trimmed. → `{title}`. An empty or longer
name is a `400`.

```bash
mm /api/mindmaps/MAP_ID/title -X PUT -d '{"title":"Japan trip, spring 2027"}'
# → {"title":"Japan trip, spring 2027"}
```

> Via the MCP server, the same call is `rename_map` with `{mapId, title}`.

## Pattern: agent-drives-recursion for auto-expand

Auto-expand does NOT recurse and does NOT run the children it creates — it only
queues one level of follow-up prompts. You drive the recursion: call
`auto-expand`, then `submit` each returned child yourself, and recurse if you
want to go deeper.

```bash
# 1. Fan a completed node out into queued follow-up children.
resp=$(mm /api/mindmaps/MAP_ID/nodes/q1/auto-expand -X POST -d '{}')

# 2. Submit each returned child to run it (each blocks on its ancestors).
echo "$resp" | jq -r '.childIds[]' | while read -r child; do
  mm "/api/mindmaps/MAP_ID/nodes/$child/submit" -X POST -d '{}'
done

# 3. To go deeper, auto-expand a child and repeat. Choose your own depth/breadth
#    budget — there is no server-side recursion cap, and the fan-out's width is
#    the model's call rather than a number you set.
```

Submit blocks until ancestors finish, so it is safe to submit children in
sequence; the generation gate guarantees each child sees complete parent
context.

## Errors

Responses carry `{error}` on failure. Common statuses: `401` (no/revoked
token), `403` (not the token user's map), `404` (missing map/parent/node), `400`
(malformed, or deleting the root), `409` (duplicate node id, or re-running a
node that already has children without `force`), `429` (over budget — body
carries an upgrade/buy-credits CTA). On `429`, stop generating and surface the
CTA rather than retrying blindly. Uploads add two of their own: `413` over the
10 MB cap, `415` for a file that is neither an image nor a PDF.

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
