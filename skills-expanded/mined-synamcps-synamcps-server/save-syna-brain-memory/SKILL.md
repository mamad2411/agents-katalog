---
name: save-syna-brain-memory
description: >-
  Saves chat history and summaries of SynaMCPs server logic or visual changes
  to the syna-brain MCP server as second brain memory. Use when finishing a
  meaningful change to server logic, APIs, data objects, securebus, admin/UI
  visuals, or when the user asks to remember, save to brain, or persist session
  context.
---

# Save chat history and summary to syna-brain

Use the **user-syna-brain** MCP namespace (`knowledge_search`, `knowledge_save`,
`knowledge_get`, `knowledge_delete`) as the project second brain.

## Storage

Default memory storage id (confirmed by successful `knowledge_save`):

`268fc510-74c5-475e-9e39-74f751aaef43`

Alternate:

`033870b5-72a8-42c9-a15e-6dcc2e4b7c7b`

If the server remaps `storageId` to another allowed storage, use the `storageId`
returned on the save response for later search/get.

If `knowledge_save` fails with an auth error, call `mcp_auth` on
`user-syna-brain`, then retry. Do not invent a substitute store.

## When to save

Save after work that changes durable understanding of this repo, especially:

- SynaMCPs **server logic** (handlers, MCP tools, policy, auth, data object kinds, securebus, workers)
- **Visual / UI** changes (admin, `/app`, landing-facing copy that lives here)
- Multi-step designs or decisions the next session would otherwise re-discover
- Explicit user request: “save to brain”, “remember this”, “persist this chat”

Skip for trivial typos, pure renames with no behavior change, or failed
explorations the user does not want kept.

## Workflow

1. **Search first** — `knowledge_search` on the memory storage with a focused
   query (feature name, package path, or topic). Note related `docId`s.
2. **Write a summary** — durable facts only; no secrets (tokens, private keys,
   `.env`, session cookies). Prefer architecture, APIs, file paths, decisions,
   and open follow-ups.
3. **Save** — `knowledge_save` with:
   - `storageId`: memory storage above
   - `mimeType`: `text/markdown`
   - `title`: `SynaMCPs | <area> | <short topic> | <YYYY-MM-DD>`
   - `text`: body using the template below
4. **Report** — in the user reply, mention that memory was saved (title +
   `docId` if returned). If save failed, say so and keep the summary in chat.

Do not delete prior memories unless the user asks to replace one; prefer a new
dated note that supersedes older context in prose.

## Memory note template

```markdown
# <topic>

## Context
- Chat / task: <one line>
- Date: <YYYY-MM-DD>

## Summary
<2–6 sentences: what changed or was decided>

## Server logic / behavior
- <bullet: packages, endpoints, MCP tools, invariants>

## Visual / UI (if any)
- <bullet: screens, components, UX notes>

## Key paths
- `path/to/file.go` — <why it matters>

## Decisions
- <decision and why>

## Open follow-ups
- <optional>

## Chat highlights
- <optional: critical Q/A or constraints from the session, not a full transcript>
```

## Tool call shape

Discover schemas with `GetDynamicTools` on namespace `user-syna-brain` if needed,
then invoke via `CallDynamicTool`:

- Search: `knowledge_search` — `{ storageId, query, topK }`
- Save: `knowledge_save` — `{ storageId, title, text, mimeType: "text/markdown" }`
