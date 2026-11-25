---
name: selfgraph
description: Use the SelfGraph SDK (Python or TypeScript) to build and query a knowledge graph from text. Use this when a task needs to turn documents or notes into a graph of entities and relationships, extract structured facts with an LLM, give an agent persistent memory (entity preferences and decision traces), version facts as they change over time, or retrieve graph-grounded context (source passages plus relationships) for RAG and question answering. Covers ingestion (insert.text and insert.ontology), typed CRUD over entities, relations, preferences, and decisions, keyword plus graph retrieval, and running against any graph backend (Neo4j, Memgraph, FalkorDB, Kuzu, HydraDB). Reach for this whenever the task mentions a knowledge graph, graph memory, entity or relationship extraction, or graph-grounded retrieval with SelfGraph.
---

# SelfGraph

SelfGraph is a Python and TypeScript SDK that turns unstructured text into a queryable, versioned knowledge graph. The SDK owns all the logic (merge, versioning, id derivation, validation); a pluggable store holds the graph (Neo4j, Memgraph, FalkorDB, embedded Kuzu, or HydraDB).

Properties to rely on:

- Every method is async, so `await` SDK calls (`SyncSelfGraph` is the same API without `await`).
- Ids are deterministic and every insert is an idempotent upsert, so re-inserting a fact does not duplicate it or bump a version.
- Relations and preferences are versioned: changing them creates a new revision and keeps the history. Decisions are updated in place.
- Every graph has a `namespace` (default `"default"`); reads and writes never cross namespaces, so keep one per tenant.
- Out of scope by design: embeddings, vector or semantic search, and GraphRAG. Retrieval is lexical (BM25 and substring) plus graph traversal.

## Install

```bash
pip install selfgraph                  # Neo4j, openCypher, HydraDB, CRUD, ontology insert, BM25 seeding
pip install "selfgraph[llm]"           # LLM extraction for insert.text
pip install "selfgraph[ner,tokenizer]" # LLM-free spaCy extraction, token budgeting
pip install "selfgraph[falkordb,kuzu]" # those backends; kuzu is embedded, no server
pip install "selfgraph[all]"           # llm, ner, tokenizer, falkordb, kuzu, mcp
```

## Quick start

```python
import asyncio
from selfgraph import LLMConfig, Neo4jStore, SelfGraph


async def main():
    async with SelfGraph(
        store=Neo4jStore("bolt://localhost:7687", auth=("neo4j", "password")),
        llm=LLMConfig(provider="openai", model="gpt-4o-mini"),
    ) as graph:
        await graph.insert.text("Acme acquired Beta Corp in 2021. Jane Doe led the deal.", source_id="doc1")
        acme = await graph.entities.get("company:acme")
        result = await graph.retrieve("who led the Acme acquisition")
        print(result.context)


asyncio.run(main())
```

`async with` initializes on entry and closes on exit (the store also initializes lazily on first use). Closing a graph closes its store, so build a new store for each `SelfGraph`. `llm=` is only needed for `insert.text`.

## Ingesting data

```python
res = await graph.insert.text(text, source_id="doc1", metadata={"url": "..."}, event_time=None)
```

`res` has `entities`, `relations`, `preferences`, `decisions`, `merges`, and `warnings`. Extraction chunks the text and writes Source, SourceVersion, and Chunk provenance; with a `source_id`, `retrieve()` can return the source passages. Without an LLM, `insert.text` falls back to spaCy NER (the `ner` extra) or a regex pass, which mislabel more and flag themselves in `res.warnings`.

For structured facts, skip extraction (no LLM, deterministic):

```python
await graph.insert.ontology(
    {
        "entities": [
            {"id": "company:acme", "type": "Company", "name": "Acme"},
            {"type": "Company", "name": "Beta Corp"},  # id derived: company:beta
        ],
        "relations": [
            {
                "from_entity": "company:acme",
                "type": "ACQUIRED",
                "to_entity": "company:beta",
                "properties": {"year": 2021},
            },
        ],
        "preferences": [],
        "decisions": [],  # each: title, optional steps (relation ids, default [])
    },
    source_id="import-1",
)
```

No passages are created, so retrieval over these facts is relationships-only. Unknown keys in an ontology, schema, `instructions`, or `prompts` raise `ValidationError` naming the closest valid key (`unknown key 'entites' in ontology; did you mean 'entities'?`).

Id rules:

- An omitted entity id is `type:canonical-name` (`entity_id(type, name)` computes it; organization-like types drop `The` and suffixes like `Inc`). Relation ids are hashes (`relation_id(from, type, to)`).
- An explicit entity id is lowercased with whitespace runs hyphenated (`Person:Jane Doe` is `person:jane-doe`), keeps punctuation, must be `type:name` with both parts non-empty, and must carry the entity's type as its prefix (`id 'company:x' does not match type 'Person'`). With a schema, an alias-form prefix (`org:acme` for alias `org` of `Company`) is rewritten to the canonical id.
- An explicit id is never re-derived from the name, so `person:jane` named `Jane Doe` and a later `Jane Doe` without an id are two entities unless a resolver merges them. Pass explicit ids when you need to reference a fact later, such as in decision `steps`.
- Entity types may contain only letters, digits, spaces, `_`, `-`, and `.`. Property keys cannot be empty or whitespace. Aliases are trimmed, and a blank alias or one equal to the entity's name (ignoring case) is dropped.

## Schema (optional)

A `schema` on the graph or on one insert declares the entity and relation types you expect. It is SDK-only (nothing is written to the backend), guides `insert.text` extraction, and validates every write, including entity and relation `create` and `update` and so the CLI and MCP tools.

```python
from selfgraph import Schema

schema = Schema(
    entities=[
        {"name": "Person", "aliases": ["user"], "properties": [{"name": "age", "type": "integer", "required": True}]},
        {"name": "Manager", "parent": "Person"},
        {"name": "Company", "aliases": ["org"]},
    ],
    relations=[{"type": "WORKS_AT", "from": {"types": ["Person"], "max_count": 1}, "to": {"types": ["Company"]}}],
)
res = await graph.insert.ontology(ontology, schema=schema)
for w in res.warnings:
    print(w.code, w.message)
```

`schema_mode` is `"warn"` (default: violations go to `res.warnings`, or for `create` and `update` to the `selfgraph` logger, and the write proceeds), `"strict"` (a violation raises `ValidationError` before writing, except that `insert.text` drops each off-schema extracted item with a `dropped_off_schema` warning; strict needs a schema), or `"off"`. A per-insert `schema` or `schema_mode` overrides the graph's. Type and relation aliases are rewritten to the canonical name before ids are derived, and a child type inherits its `parent`'s properties and satisfies its endpoints.

`max_count` is also checked against the stored graph as a contradiction: `contradiction="warn"` (default) keeps both with a `contradiction` warning, `"supersede"` retires the oldest current relations (by `event_time`, else write time) until the cap holds, and `"off"` skips the check. Set it on the graph or per `insert.text`, `insert.ontology`, or `relations.create`. A retired relation has `is_current=False`, `invalidated_at`, and `invalidated_by`; `relations.get` returns `None` for it and `relations.list` hides it unless `include_invalidated=True`; creating it again reasserts it (ranking details in `docs/schema.md`).

`Schema.from_neo4j_ontology(data)` and `schema.to_neo4j_ontology()` convert to and from the Neo4j graph schema JSON that neo4j-graphrag uses. See `docs/schema.md`.

## Entity resolution (optional)

`resolver` on the graph or one insert folds a new entity into an existing one that names the same thing. `"exact"` (default) merges nothing beyond derived ids; `"default"` merges on an id match, a shared external id, or a case-folded name or alias match; `"fuzzy"` adds same-type names at 0.92 similarity or above, guarded so differing numbers, initials, or generational suffixes never merge; `"llm"` (needs `llm=`) also asks the LLM about names in `[0.8, 0.92)`. Only entities without an explicit `id` whose derived id is not stored are candidates, and each is offered only entities of compatible types (schema `parent` counts). The survivor keeps its id, name, type, and values; the absorbed entity adds aliases and fills missing external ids and properties.

```python
res = await graph.insert.ontology(ontology, resolver="default")
res.merges  # one MergeRecord per merge; warning code "entity_merged"
await graph.entities.merges("company:acme")  # Page[MergeRecord]
await graph.entities.unmerge(res.merges[0].id)  # recreate the absorbed entity, move its refs back
```

See `docs/resolution.md`.

## Entities

```python
e = await graph.entities.create(
    "Acme", "Company", aliases=["Acme Inc"], external_ids={"crunchbase": "acme"}, properties={"stage": "seed"}
)
await graph.entities.get("company:acme")  # None when missing
await graph.entities.list(type="Company", name=None, limit=50, cursor=None)  # Page: items, next_cursor
await graph.entities.update("company:acme", properties={"stage": "series-a"})
await graph.entities.delete("company:acme")
```

`create` takes `name` then `type` and raises `ConflictError` for an existing id. `update` merges properties, aliases, and external ids (`remove_properties`, `remove_aliases` drop entries); it cannot change the type, which is part of the id. `delete` cascades to the entity's relations, preferences, evidence, and the decision traces that reference it; a decision that only lists it as an alternative drops that alternative.

## Relations (versioned)

```python
r = await graph.relations.create("person:jane", "WORKS_AT", "company:acme", properties={"title": "CEO"})
await graph.relations.get(r.id)
await graph.relations.list(from_entity="person:jane", type=None, to_entity=None)
await graph.relations.update(r.id, set_properties={"title": "Chair"})
await graph.relations.versions(r.id)  # newest first
await graph.relations.delete(r.id)
```

`update` makes a new revision. Endpoints and type are immutable; create a new relation to change them.

## Preferences (agent memory)

```python
p = await graph.preferences.create("person:jane", "database", "company:acme", kind="preference", strength=0.9)
await graph.preferences.list("person:jane", key=None, kind=None)
await graph.preferences.update(p.id, strength=1.0)
await graph.preferences.update(p.id, clear=["strength", "about_entity"])
await graph.preferences.delete(p.id)
```

`create` takes `subject_entity`, `key`, then `value_entity` (an existing entity). `kind` is `"preference"` or `"disinterest"`. In `update`, `None` keeps a field; `clear` removes `strength`, `about_entity`, or `event_time`.

## Decision traces

```python
await graph.decisions.create(
    "Pick the database",
    steps=[r1.id, r2.id],  # relation ids, optional
    actor_entity="person:jane",
    outcome_entity="company:acme",
    alternative_entities=["company:other"],
    rationale="Needs temporal history.",
    id="decision:db",
)
await graph.decisions.list(actor_entity="person:jane", status=None)
await graph.decisions.update("decision:db", status="reversed")
await graph.decisions.delete("decision:db")
```

In `update`, an explicit `None` clears `actor_entity`, `summary`, `rationale`, `outcome_entity`, or `event_time`, and so does naming it in `clear`, which also empties `alternative_entities` or `steps`.

## Retrieval

```python
result = await graph.retrieve(
    "who led the Acme acquisition", strategy="bfs", depth=3, k=20, max_nodes=200, budget_tokens=3000, as_of=None
)
result.context  # passages, relationships, preferences, decisions, nearest first; ready for a prompt
result.seeds  # entities matched from the query, with scores
result.subgraph  # entities, relations, preferences, decisions collected
```

`strategy` is `"bfs"`, `"dfs"`, or `"ppr"` (personalized PageRank). `depth` is hops from each seed, `k` the max seeds, and `max_nodes` caps the subgraph; `budget_tokens` trims only `result.context`. `as_of` (a datetime or ISO 8601 text; no offset means UTC) reads the graph as it was at that valid time (`event_time`, else write time). Seeding scores every entity in two id-ordered passes, so its cost grows linearly with the graph. See `docs/retrieval.md`.

## Maintenance (explicit, never automatic)

```python
await graph.maintenance.decay(half_life_days=30, dry_run=False)
plan = await graph.maintenance.prune(min_relevance=0.05)
await graph.maintenance.prune(older_than=cutoff, types=["Session"], dry_run=False)
await graph.maintenance.consolidate(dry_run=False)
```

`decay` stores a `relevance` score in `[0, 1)` on entities and current relations without a new version; retrieval uses it only to break seed ties. `prune` needs `min_relevance` or `older_than` and deletes through the normal cascades. `consolidate` merges parallel relations with the same endpoints and type into the lowest id, moving decision steps to the survivor; it never deletes a decision. All three are dry runs unless `dry_run=False` (CLI `--apply`). See `docs/maintenance.md`.

## Backends

```python
from selfgraph import CypherStore, FalkorDBStore, HydraDBStore, KuzuStore, Neo4jStore

Neo4jStore("bolt://localhost:7687", auth=("neo4j", "password"), database=None)
CypherStore("bolt://localhost:7687", auth=("user", "password"))  # Memgraph and other Bolt engines
FalkorDBStore(host="localhost", port=6379)  # falkordb extra
KuzuStore("graph.kuzu")  # kuzu extra, embedded, one process at a time
HydraDBStore("bolt://127.0.0.1:17687", auth=("neo4j", "<token>"))  # HydraDB 0.4.0 or newer
```

SDK behavior is identical across backends. To target another database, implement the `GraphStore` primitives. `await graph.run_cypher(query, params)` is a backend-specific escape hatch: it can write, is not namespace-scoped, and sees each backend's physical layout.

## CLI and MCP

```bash
selfgraph init
selfgraph insert text "Acme acquired Beta."
selfgraph entity get company:acme
selfgraph retrieve "who led the acquisition" --context-only
selfgraph mcp
```

`selfgraph mcp` serves 34 tools over stdio that mirror the SDK (listed in `docs/mcp.md`). Configure with flags or `SELFGRAPH_STORE`, `SELFGRAPH_URI`, `SELFGRAPH_AUTH`, `SELFGRAPH_DATABASE`, `SELFGRAPH_NAMESPACE`, `SELFGRAPH_LLM_PROVIDER`, `SELFGRAPH_LLM_MODEL`, `SELFGRAPH_LLM_API_KEY`, `SELFGRAPH_LLM_BASE_URL`, `SELFGRAPH_LLM_TIMEOUT`, `SELFGRAPH_LLM_CONCURRENCY`, `SELFGRAPH_SCHEMA`, `SELFGRAPH_SCHEMA_MODE`, `SELFGRAPH_RESOLVER`, `SELFGRAPH_CONTRADICTION`, `SELFGRAPH_INSTRUCTIONS`, and `SELFGRAPH_PROMPTS`. With no store and no URI they use embedded Kuzu at `~/.selfgraph/default.kuzu`. Time arguments are ISO 8601 text; no offset means UTC. The MCP `run_cypher` tool is read-only and not namespace-scoped, so filter on `ns`. CLI exit codes: 0 success, 1 runtime failure, 2 invalid input, 130 interrupted, 141 closed stdout (`docs/cli.md`).

## TypeScript

`npm install @hydradb/selfgraph` (Node 20+) gives the same API in pure TypeScript over the same graph. Methods are camelCase and options go in a trailing object; model fields and option keys keep their Python names.

```ts
import { KuzuStore, SelfGraph } from "@hydradb/selfgraph";

const graph = new SelfGraph(new KuzuStore("graph.kuzu"), { namespace: "default" });
await graph.insert.ontology({ entities: [{ type: "Company", name: "Acme" }] });
const result = await graph.retrieve("Acme", { strategy: "ppr", max_nodes: 50 });
await graph.runCypher("MATCH (n) RETURN count(n) AS n");
await graph.close();
```

Optional features are peer packages: `kuzu`, `falkordb`, `ai` plus an `@ai-sdk/*` provider, `js-tiktoken`, and `@modelcontextprotocol/sdk`. `llm` takes an `LLMConfig`, an AI SDK model object, or an `LLMClient`. There is no spaCy path and no sync client. In an update, `null` clears a decision field but keeps a relation or preference field. See `docs/typescript.md`.
