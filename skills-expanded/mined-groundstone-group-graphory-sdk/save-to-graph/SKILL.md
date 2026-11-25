---
name: save-to-graph
description: Turn any unstructured content - a chat session, a video transcript, an article, meeting notes - into durable, linked memory in Graphory. Learn the live schema, check what already exists, then write only what is new and connect it to existing nodes. Trigger on "remember this", "add this to my graph", "save this transcript", "ingest this article", "capture this", or whenever the user wants content kept as queryable memory.
---

# save-to-graph

The one ingestion loop. Whatever the content - a coaching video you just
watched, an article worth keeping, a chat session, a research paper - this skill
maps it into the user's Graphory graph cleanly: nothing duplicated, everything
connected to what is already there, only genuinely new information written.

Graphory does not run an LLM on the content. You do. You read and extract;
Graphory stores and serves. That keeps inference cost at zero and keeps the user
in control of their own data.

## The loop

**1. Learn the target shape.** Call `describe_schema()`. It returns the live
node labels, the allowed relationship types, recommended property names, and
what is already present in this graph. Never guess the vocabulary - ask for it.
The graph's schema is the contract; this call is how you read it.

**2. Extract.** Read the content and pull out the entities and relationships
that matter, mapped onto the schema you just fetched. Keep the user's real
words: a person's name, a company, a quote go in as-said, not rephrased into
something "cleaner".

**3. Check what already exists.** Before writing anything, `search_graph(...)`
for each entity. If the person, company, or source is already a node, reuse its
id - do not create a second one. This is the step that keeps the graph clean.

**4. Write only the delta, and link it.** New entities ->
`write_to_graph(action="add", ...)`. Every relationship, whether new-to-new or
new-to-existing -> `write_to_graph(action="connect", ...)`. The whole point is
connection: a tactic from a video should hang off the project it applies to; a
person in a transcript should link to the company they work for.

## Mapping content onto nodes

Graphory uses a small set of generic node labels (call `describe_schema` for the
current list) and expresses specifics through a `subtype` property rather than
new labels. A rough mapping:

| In the content | Node label | How |
|----------------|-----------|-----|
| The video / article / paper / page itself | `Asset` | `properties.subtype` = "video", "article", "paper" |
| The coach / author / speaker | `Person` | with `role` if known |
| Their company / fund / brand | `Organization` | a third-party company |
| You watching / reading / processing it | `Activity` | `subtype` = "watched", "read" |
| The chat session | `Activity` or `Thread` | |
| A named idea / tactic / topic worth keeping | `Asset` | `subtype` = "concept" or "tactic" |

"invoice", "video", "podcast", "tactic" are `subtype` values, never new node
labels. When in doubt about which label fits, let `describe_schema` decide -
do not invent labels or relationship names that it does not list.

## Tag learning material

Set `domain: content` on anything captured to learn from (videos, articles,
research). Use `domain: operations` for real business activity (emails,
invoices, your own decisions). It is a soft tag - everything lives in one graph
- but it lets the user later ask "just show me what I have been learning"
without a separate store.

## Verified call shapes

```python
describe_schema()  # no arguments - returns the live vocabulary for this graph

# does this entity already exist?
search_graph(query="Alex Hormozi", node_type="Person", limit=5)

# new entity
write_to_graph(
    action="add",
    node_id="person:alex-hormozi",
    label="Person",
    properties=json.dumps({"name": "Alex Hormozi", "role": "founder", "domain": "content"}),
    confidence=0.95,
    evidence="Host of the video the user saved",
)

# link it to something already in the graph (use a relationship name from describe_schema)
write_to_graph(
    action="connect",
    from_id="person:alex-hormozi",
    to_id="asset:video:harsh-truths",
    relationship="created",
    confidence=0.95,
)
```

For a whole transcript at once, prefer `ingest(payload=...)` over dozens of
`write_to_graph` calls. `payload` is a JSON string describing the item -
`{entity, source, type, title, body, date, url, metadata}` - where the
transcript text goes in the `body` field. It stores the source document and
extracts inline. See [`../../examples/`](../../examples/).

## Only add what is new

- If `search_graph` returns an existing node, reuse its id. Never write a
  duplicate.
- If the content contains nothing the graph does not already have, write
  nothing. "I read it; you already have all of it" is a good outcome - say so.
- New information about an existing entity is `action="connect"` or
  `action="correct"`, not a brand-new node.

## Confidence and provenance

`write_to_graph` is confidence-gated: `>= 0.90` merges, `0.70 - 0.89` goes to
the review queue, `< 0.70` is rejected. Use bands the user would expect: a
named, unambiguous entity is `0.95`; an inferred link ("probably the same
Sarah") is `0.70` and belongs in review, not auto-merged. Always pass
`evidence` - one phrase on why - so the user can audit it later.

## Safety rails

- **Never write secrets.** Redact API keys, passwords, and tokens out of content
  before extracting.
- **Never duplicate.** The search-before-write step is not optional.
- **Keep the user's words.** Names, companies, and quotes go in as-said. You are
  indexing reality, not editing it.
- **One graph.** Do not ask which graph or knowledge base - there is one.
  Separate signal with `domain: content` vs `operations`, not with separate
  stores.
- **Ask once when the entity is ambiguous.** If you cannot tell which company a
  piece is about, ask rather than guess.

## After saving

Tell the user in one sentence what changed: "Added 3 new things from that video
- the 'starving crowd' idea, linked to your pricing project - the rest you
already had." Do not echo the payload back.
