---
name: mem-search
description: Search claude-mem's persistent cross-session memory database. Search for an index, filter, then fetch full details only for kept IDs, for 10x token savings. Use when the user asks "did we already solve this?", "how did we do X last time?", or needs work from previous sessions. Requires the claude-mem MCP.
license: MIT
---

# Mem Search

Recall past work across all sessions cheaply. Workflow: search, filter, fetch.

**Requires the claude-mem MCP.** This skill assumes the `search`, `timeline`, and `get_observations` tools are available. If they are not, claude-mem is not installed.

## When to use

Use when the user asks about PREVIOUS sessions, not the current conversation:

- "Did we already fix this?"
- "How did we solve X last time?"
- "What happened last week?"

If the answer is in the current conversation, just answer.

## The 3-layer workflow (always follow)

Never fetch full details without filtering first. The index is cheap, full observations are expensive: roughly 10x token savings by filtering before fetching.

### Step 1: search, get the index with IDs

Use the `search` tool:

```text
search(query="authentication", limit=20, project="my-project")
```

Returns a table of IDs, timestamps, types, titles (~50-100 tokens per result):

```text
| ID     | Time    | Type   | Title                       | Read |
|--------|---------|--------|-----------------------------|------|
| #11131 | 3:48 PM | obs    | Added JWT authentication    | ~75  |
| #10942 | 2:15 PM | bugfix | Fixed auth token expiration | ~50  |
```

Parameters:

- `query` (string) search term
- `limit` (number) max results, default 20, max 100
- `project` (string) project name filter
- `type` (string, optional) "observations", "sessions", or "prompts"
- `obs_type` (string, optional) comma-separated: bugfix, feature, decision, discovery, change
- `dateStart` (string, optional) YYYY-MM-DD or epoch ms
- `dateEnd` (string, optional) YYYY-MM-DD or epoch ms
- `offset` (number, optional) skip N results
- `orderBy` (string, optional) "date_desc" (default), "date_asc", "relevance"

### Step 2: timeline, get context around interesting results

Use the `timeline` tool:

```text
timeline(anchor=11131, depth_before=3, depth_after=3, project="my-project")
```

Or find the anchor automatically from a query:

```text
timeline(query="authentication", depth_before=3, depth_after=3, project="my-project")
```

Returns `depth_before + 1 + depth_after` items in chronological order, with observations, sessions, and prompts interleaved around the anchor.

Parameters:

- `anchor` (number, optional) observation ID to center on
- `query` (string, optional) find the anchor automatically if no anchor is given
- `depth_before` (number, optional) items before the anchor, default 5, max 20
- `depth_after` (number, optional) items after the anchor, default 5, max 20
- `project` (string) project name filter

### Step 3: fetch, full details for kept IDs only

Review the titles from step 1 and the context from step 2. Pick the relevant IDs, discard the rest.

Use the `get_observations` tool:

```text
get_observations(ids=[11131, 10942])
```

Always use `get_observations` for two or more observations: a single request instead of N.

Parameters:

- `ids` (array of numbers, required) observation IDs to fetch
- `orderBy` (string, optional) "date_desc" (default), "date_asc"
- `limit` (number, optional) max observations to return
- `project` (string, optional) project name filter

Returns complete observation objects with title, subtitle, narrative, facts, concepts, files (~500-1000 tokens each).

## Examples

Find recent bugfixes:

```text
search(query="bug", type="observations", obs_type="bugfix", limit=20, project="my-project")
```

Find what happened in a date range:

```text
search(type="observations", dateStart="2026-05-12", dateEnd="2026-05-18", limit=20, project="my-project")
```

Context around a discovery:

```text
timeline(anchor=11131, depth_before=5, depth_after=5, project="my-project")
```

Batch fetch details:

```text
get_observations(ids=[11131, 10942, 10855], orderBy="date_desc")
```

## Why this workflow

- Search index: about 50 to 100 tokens per result.
- Full observation: about 500 to 1000 tokens each.
- Batch fetch: one request instead of N individual requests.
- Roughly 10x token savings by filtering before fetching.

---

See full content at https://github.com/HermeticOrmus/mem-search-skills.
