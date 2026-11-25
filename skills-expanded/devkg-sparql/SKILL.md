---
name: devkg-sparql
description: Query the Dev Knowledge Graph via SPARQL instead of grepping raw session files. Use this when asked about technologies, relationships between tools, session history, where a topic was discussed, or cross-platform knowledge. Prefer provenance-first SPARQL (message + session) over label-only CONTAINS or grep.
user-invocable: true
allowed-tools:
  - Bash(curl:*)
  - Bash(jq:*)
---

# DevKG SPARQL Query Skill

## CRITICAL CONTEXT-SAFETY RULE

**NEVER READ LARGE SPARQL RESULTS, SESSION FILES, JSONL, LOGS, OR GENERATED ARTIFACTS ALL AT ONCE.** Always add `LIMIT`, select only needed variables, inspect counts first, and summarize. Never dump huge result sets, ID lists, raw JSON, or transcript content into chat.

Query the developer knowledge graph at `http://localhost:3030/devkg/sparql` via SPARQL. This graph contains extracted knowledge triples, entities, Wikidata links, and session metadata from **Claude Code, pi, Codex, Cursor, ChatGPT, DeepSeek, Grok, and Warp** sessions.

**Content limit:** `sioc:content` on messages is capped at ~2000 characters at ingest. SPARQL is enough to **locate sessions and reason lightly** from triples + snippets. For full quotes or deep thread reconstruction, normalize `hasSourceFile` and read the JSONL only when needed.

## Retrieval Strategy (read this first)

| User intent | Do this first | Do NOT start with |
|-------------|---------------|-------------------|
| "Where / which sessions discussed X?" | **Template 5** (topic + intent + provenance) | Label-only Template 6, or grep |
| "What do we know about technology X?" | Template 1 (entity + provenance) | Grep |
| "How does X relate to Y?" | Template 2 | Grep |
| "Find the exact message wording" | Template 5 or 9 → then JSONL only if snippet truncated | Grepping all projects |

**Default for session-discovery questions:** multi-signal filter (topic **and** intent terms) on **both** triple labels and `sioc:content`, always joining `extractedFrom` / `extractedInSession`, ordered by `DESC(?created)`, with `LIMIT`.

When Fuseki returns provenance hits, **do not** fall back to grep. Grep only if Fuseki is down or returns 0 rows after a provenance query.

## Execution Pattern

Always use this pattern (POST, URL-encoded query, JSON output). Include Fuseki auth when required:

```bash
curl -s -X POST 'http://localhost:3030/devkg/sparql' \
  -u admin:admin \
  -H 'Accept: application/sparql-results+json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "query=YOUR_SPARQL_HERE" \
  | jq -r '.results.bindings[] | [.var1.value, .var2.value] | @tsv'
```

Adjust the `jq` expression to match your SELECT variables. Use `@tsv` for compact tabular output. Always `LIMIT` results.

For multi-line queries, use double quotes around the `--data-urlencode` value and escape inner quotes:

```bash
curl -s -X POST 'http://localhost:3030/devkg/sparql' \
  -u admin:admin \
  -H 'Accept: application/sparql-results+json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "query=PREFIX devkg: <http://devkg.local/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?label WHERE {
  ?e a devkg:Entity ; rdfs:label ?label .
  FILTER(LANG(?label) = \"\")
} LIMIT 10" \
  | jq -r '.results.bindings[] | .label.value'
```

## Fallback Rule

If Fuseki is unreachable (curl fails or times out) **or** a provenance query (Template 5/8) returns 0 results, then fall back to grep-based session search:
```bash
grep -rli "keyword" ~/.claude/projects ~/.pi/agent/sessions ~/.cursor/projects 2>/dev/null | head -20
```
Then read matching JSONL files with bounded Python extraction. Only use this as a last resort.

## Resolving `hasSourceFile` to Disk (and Pruned Sources)

`hasSourceFile` is NOT always a real absolute path. Normalize before any `Read`:

| `hasSourceFile` prefix | Real on-disk location |
|---|---|
| `/Users/...` | absolute path — use as-is |
| `/claude-sessions/<munged>/<file>` | `~/.claude/projects/<munged>/<file>` |
| `/pi-sessions/<munged>/<file>` | `~/.pi/agent/sessions/<munged>/<file>` |
| `/codex-sessions/<path>` | `~/.codex/sessions/<path>` |
| `/cursor-sessions/projects/<slug>/...` | `~/.cursor/projects/<slug>/...` |

```bash
resolve_session_path() {
  local sf="$1" p=""
  case "$sf" in
    /Users/*)                    p="$sf" ;;
    /claude-sessions/*)          p="$HOME/.claude/projects/${sf#/claude-sessions/}" ;;
    /pi-sessions/*)              p="$HOME/.pi/agent/sessions/${sf#/pi-sessions/}" ;;
    /codex-sessions/*)           p="$HOME/.codex/sessions/${sf#/codex-sessions/}" ;;
    /cursor-sessions/projects/*) p="$HOME/.cursor/projects/${sf#/cursor-sessions/projects/}" ;;
    *)                           p="$sf" ;;
  esac
  local stem="${p%.jsonl}"
  if [ -f "$p" ];              then echo "FILE:$p";                    return; fi
  if [ -f "$stem" ];           then echo "FILE:$stem";                 return; fi
  if [ -d "$stem/subagents" ]; then echo "SUBAGENTS:$stem/subagents";  return; fi
  if [ -d "$p/subagents" ];    then echo "SUBAGENTS:$p/subagents";     return; fi
  echo "PRUNED:$p"
}
```

**If the path is `PRUNED`**, do NOT grep the filesystem. Re-query KnowledgeTriples for that session via `extractedInSession` and reconstruct from labels + any remaining `sioc:content`.

## Result Formatting

Present SPARQL results as markdown tables. Never dump raw JSON to the user.

## Prefixes (copy into every query)

```sparql
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:     <http://www.w3.org/2002/07/owl#>
PREFIX prov:    <http://www.w3.org/ns/prov#>
PREFIX sioc:    <http://rdfs.org/sioc/ns#>
PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX devkg:   <http://devkg.local/ontology#>
PREFIX data:    <http://devkg.local/data/>
PREFIX wd:      <http://www.wikidata.org/entity/>
```

## Ontology Cheat Sheet

### Classes

| Class | Parent | Description |
|-------|--------|-------------|
| `devkg:Session` | `prov:Activity`, `sioc:Forum` | A working session (conversation) |
| `devkg:Message` | `sioc:Post`, `prov:Entity` | A message in a session |
| `devkg:UserMessage` | `devkg:Message` | Human message |
| `devkg:AssistantMessage` | `devkg:Message` | AI message |
| `devkg:ToolCall` | `prov:Activity` | Legacy tool invocation nodes (may be absent in new ingests — do not rely on them) |
| `devkg:ToolResult` | `prov:Entity` | Legacy tool output (may be absent in new ingests) |
| `devkg:CodeArtifact` | `prov:Entity`, `schema:SoftwareSourceCode` | Code file/snippet |
| `devkg:Entity` | `prov:Entity` | Extracted technical concept |
| `devkg:KnowledgeTriple` | — | Reified triple (subject→predicate→object) with provenance |
| `devkg:Project` | `prov:Entity` | A development project |
| `devkg:Developer` | `prov:Agent` | Human developer |
| `devkg:AIModel` | `prov:Agent` | AI model (Claude, GPT, etc.) |
| `devkg:Topic` | `skos:Concept` | Knowledge topic |

### Structural Predicates (Session/Message graph)

| Predicate | Domain → Range | Notes |
|-----------|---------------|-------|
| `devkg:usedInSession` | Message/ToolCall → Session | Links content to its session |
| `devkg:hasParentMessage` | Message → Message | Thread structure |
| `devkg:mentionsTopic` | Message → Topic | Topic tagging |
| `devkg:invokedTool` | AssistantMessage → ToolCall | Tool usage |
| `devkg:hasToolResult` | ToolCall → ToolResult | Tool output |
| `devkg:producedArtifact` | Activity → CodeArtifact | Code generation |
| `devkg:belongsToProject` | Session → Project | Project membership |
| `devkg:extractedFrom` | KnowledgeTriple → Message | Triple provenance |
| `devkg:extractedInSession` | KnowledgeTriple → Session | Triple provenance |
| `devkg:tripleSubject` | KnowledgeTriple → Entity | Reified subject |
| `devkg:tripleObject` | KnowledgeTriple → Entity | Reified object |
| `devkg:triplePredicateLabel` | KnowledgeTriple → xsd:string | Predicate name |

### Key Datatype Properties

| Property | On | Value |
|----------|----|-------|
| `sioc:content` | Message | Message text (truncated ~2000 chars at ingest) |
| `rdfs:label` | Entity/Session/Project | Display name |
| `dcterms:created` | Session/Message | ISO datetime |
| `devkg:hasSourcePlatform` | Session | `claude-code`, `pi-coding-agent`, `codex`, `cursor`, `chatgpt`, `deepseek`, `grok`, `warp` |
| `devkg:hasSourceFile` | Session | Logical path to raw source — normalize before `Read` (see "Resolving `hasSourceFile` to Disk") |
| `devkg:hasToolName` | ToolCall | Legacy — prefer KnowledgeTriples + message content for discovery |
| `devkg:hasWorkingDirectory` | Session | Project directory path |
| `owl:sameAs` | Entity | Wikidata URI (e.g., `wd:Q28865`) |

### Knowledge Predicates (24 total)

These connect `devkg:Entity` to `devkg:Entity` via direct edges AND are stored as `devkg:triplePredicateLabel` strings on reified `devkg:KnowledgeTriple` nodes:

`uses`, `dependsOn`, `enables`, `isPartOf`, `hasPart`, `implements`, `extends`, `alternativeTo`, `solves`, `produces`, `configures`, `composesWith`, `provides`, `requires`, `isTypeOf`, `builtWith`, `deployedOn`, `storesIn`, `queriedWith`, `integratesWith`, `broader`, `narrower`, `relatedTo`, `servesAs`

## Query Templates

### 1. Entity Lookup — "What do we know about X?"

Returns all relationships (outbound + inbound) for an entity, with source file and content snippet for provenance. Use `CONTAINS` for fuzzy matching.

```sparql
SELECT DISTINCT ?direction ?predicate ?otherLabel ?sourceFile ?platform
       (SUBSTR(?content, 1, 150) AS ?snippet) WHERE {
  {
    ?triple a devkg:KnowledgeTriple ;
            devkg:tripleSubject ?s ;
            devkg:triplePredicateLabel ?predicate ;
            devkg:tripleObject ?o ;
            devkg:extractedFrom ?msg ;
            devkg:extractedInSession ?session .
    ?s rdfs:label ?sLabel .
    ?o rdfs:label ?otherLabel .
    FILTER(CONTAINS(LCASE(STR(?sLabel)), "ENTITY_LOWER"))
    BIND("outbound" AS ?direction)
  } UNION {
    ?triple a devkg:KnowledgeTriple ;
            devkg:tripleSubject ?o ;
            devkg:triplePredicateLabel ?predicate ;
            devkg:tripleObject ?obj ;
            devkg:extractedFrom ?msg ;
            devkg:extractedInSession ?session .
    ?obj rdfs:label ?oLabel .
    ?o rdfs:label ?otherLabel .
    FILTER(CONTAINS(LCASE(STR(?oLabel)), "ENTITY_LOWER"))
    BIND("inbound" AS ?direction)
  }
  OPTIONAL { ?session devkg:hasSourceFile ?sourceFile }
  OPTIONAL { ?session devkg:hasSourcePlatform ?platform }
  OPTIONAL { ?msg sioc:content ?content }
}
ORDER BY ?direction ?predicate
```

Replace `ENTITY_LOWER` with the lowercase entity name (e.g., `neo4j`, `opentelemetry`).

The `sourceFile` column is a logical path to the original JSONL/JSON file — normalize it with `resolve_session_path` (see "Resolving `hasSourceFile` to Disk") before `Read`; if it resolves to `PRUNED`, reconstruct from the triples instead.

### 2. Entity-to-Entity — "How does X relate to Y?"

```sparql
SELECT DISTINCT ?predicate ?sourceSnippet WHERE {
  ?triple a devkg:KnowledgeTriple ;
          devkg:tripleSubject ?s ;
          devkg:triplePredicateLabel ?predicate ;
          devkg:tripleObject ?o ;
          devkg:extractedFrom ?msg .
  ?s rdfs:label ?sLabel .
  ?o rdfs:label ?oLabel .
  OPTIONAL { ?msg sioc:content ?c . BIND(SUBSTR(?c, 1, 150) AS ?sourceSnippet) }
  FILTER(
    CONTAINS(LCASE(STR(?sLabel)), "ENTITY_X") &&
    CONTAINS(LCASE(STR(?oLabel)), "ENTITY_Y")
  )
}
```

### 3. Predicate Search — "What uses/enables/solves X?"

```sparql
SELECT DISTINCT ?subjectLabel ?objectLabel WHERE {
  ?triple a devkg:KnowledgeTriple ;
          devkg:tripleSubject ?s ;
          devkg:triplePredicateLabel "PREDICATE" ;
          devkg:tripleObject ?o .
  ?s rdfs:label ?subjectLabel .
  ?o rdfs:label ?objectLabel .
  FILTER(CONTAINS(LCASE(STR(?subjectLabel)), "ENTITY_LOWER")
      || CONTAINS(LCASE(STR(?objectLabel)), "ENTITY_LOWER"))
}
```

Replace `PREDICATE` with one of the 24 predicates (e.g., `uses`, `integratesWith`).

### 4. Session Listing — "What sessions exist?"

```sparql
SELECT ?session ?platform ?created ?title WHERE {
  ?session a devkg:Session .
  OPTIONAL { ?session devkg:hasSourcePlatform ?platform }
  OPTIONAL { ?session dcterms:created ?created }
  OPTIONAL { ?session dcterms:title ?title }
}
ORDER BY DESC(?created)
LIMIT 50
```

### 5. Topic + Intent → Sessions (PRIMARY for "where did we discuss X?")

**Use this first** for session discovery, career/product/person questions, or "exact piece of a session."
Do **not** start with label-only Template 6.

Replace `TOPIC_LOWER` (required) and add intent terms in the second FILTER (at least one).
Example: topic=`linkedin`, intent=`profile|career|roberto|headline|authority`.

```sparql
SELECT DISTINCT ?created ?platform ?sourceFile ?subj ?pred ?obj
       (SUBSTR(REPLACE(STR(?content), "\n", " "), 1, 200) AS ?snippet)
WHERE {
  {
    # Path A: KnowledgeTriple labels match topic + intent
    ?kt a devkg:KnowledgeTriple ;
        devkg:tripleSubject ?s ;
        devkg:tripleObject ?o ;
        devkg:triplePredicateLabel ?pred ;
        devkg:extractedFrom ?msg ;
        devkg:extractedInSession ?sess .
    ?s rdfs:label ?subj .
    ?o rdfs:label ?obj .
    FILTER(LANG(?subj) = "" && LANG(?obj) = "")
    BIND(LCASE(CONCAT(STR(?subj), " ", STR(?obj))) AS ?tripleText)
    FILTER(CONTAINS(?tripleText, "TOPIC_LOWER"))
    FILTER(
      CONTAINS(?tripleText, "INTENT1")
      || CONTAINS(?tripleText, "INTENT2")
      || CONTAINS(?tripleText, "INTENT3")
    )
  }
  UNION
  {
    # Path B: message text matches topic + intent (catches misses in entity extraction)
    ?msg a ?msgType ;
         sioc:content ?content ;
         sioc:has_container ?sess .
    FILTER(?msgType IN (devkg:AssistantMessage, devkg:UserMessage))
    ?kt a devkg:KnowledgeTriple ;
        devkg:extractedFrom ?msg ;
        devkg:extractedInSession ?sess ;
        devkg:tripleSubject ?s ;
        devkg:tripleObject ?o ;
        devkg:triplePredicateLabel ?pred .
    ?s rdfs:label ?subj .
    ?o rdfs:label ?obj .
    FILTER(LANG(?subj) = "" && LANG(?obj) = "")
    BIND(LCASE(STR(?content)) AS ?msgText)
    FILTER(CONTAINS(?msgText, "TOPIC_LOWER"))
    FILTER(
      CONTAINS(?msgText, "INTENT1")
      || CONTAINS(?msgText, "INTENT2")
      || CONTAINS(?msgText, "INTENT3")
    )
  }
  OPTIONAL { ?msg sioc:content ?content }
  OPTIONAL { ?sess devkg:hasSourcePlatform ?platform }
  OPTIONAL { ?sess devkg:hasSourceFile ?sourceFile }
  OPTIONAL { ?sess dcterms:created ?created }
}
ORDER BY DESC(?created)
LIMIT 40
```

Present as a **session table** grouped by `sourceFile` (date, platform, hit count, 1–2 sample facts/snippets). Reason from triples + snippets when possible; open JSONL only if the user needs full wording beyond the 2000-char cap.

If intent is unknown, keep topic FILTER and drop the intent FILTER (broader recall).

### 6. Topic Search (label-only) — fallback entity scan

Simpler label scan. Prefer Template 5 when the user asks *where* or *which sessions*.

```sparql
SELECT DISTINCT ?session ?platform ?created ?sourceFile WHERE {
  ?triple a devkg:KnowledgeTriple ;
          devkg:extractedInSession ?session .
  { ?triple devkg:tripleSubject ?e . ?e rdfs:label ?label . }
  UNION
  { ?triple devkg:tripleObject ?e . ?e rdfs:label ?label . }
  FILTER(CONTAINS(LCASE(STR(?label)), "TOPIC_LOWER"))
  OPTIONAL { ?session devkg:hasSourcePlatform ?platform }
  OPTIONAL { ?session dcterms:created ?created }
  OPTIONAL { ?session devkg:hasSourceFile ?sourceFile }
}
ORDER BY DESC(?created)
LIMIT 30
```

### 7. Cross-Platform Overlap — "What entities appear across platforms?"

```sparql
SELECT ?label (GROUP_CONCAT(DISTINCT ?platform; separator=", ") AS ?platforms)
       (COUNT(DISTINCT ?platform) AS ?platformCount) WHERE {
  ?triple a devkg:KnowledgeTriple ;
          devkg:tripleSubject ?e ;
          devkg:extractedInSession ?session .
  ?session devkg:hasSourcePlatform ?platform .
  ?e rdfs:label ?label .
  FILTER(LANG(?label) = "")
}
GROUP BY ?label
HAVING(COUNT(DISTINCT ?platform) > 1)
ORDER BY DESC(?platformCount)
LIMIT 40
```

### 8. Wikidata Enrichment — "What is X?"

```sparql
SELECT ?label ?wikidataURI ?description WHERE {
  ?entity a devkg:Entity ;
          rdfs:label ?label ;
          owl:sameAs ?wikidataURI .
  FILTER(STRSTARTS(STR(?wikidataURI), "http://www.wikidata.org"))
  FILTER(CONTAINS(LCASE(STR(?label)), "ENTITY_LOWER"))
  FILTER(LANG(?label) = "")
  OPTIONAL { ?entity dcterms:description ?description }
}
LIMIT 20
```

### 9. Full-Text Content Search — "Find messages mentioning keyword X"

Searches **both** user and assistant messages (assistant text holds most extractable knowledge).

```sparql
SELECT ?platform ?created ?sourceFile
       (SUBSTR(REPLACE(STR(?content), "\n", " "), 1, 200) AS ?snippet)
WHERE {
  ?msg a ?msgType ;
       sioc:content ?content ;
       sioc:has_container ?session .
  FILTER(?msgType IN (devkg:AssistantMessage, devkg:UserMessage))
  OPTIONAL { ?session dcterms:created ?created }
  OPTIONAL { ?session devkg:hasSourcePlatform ?platform }
  OPTIONAL { ?session devkg:hasSourceFile ?sourceFile }
  FILTER(CONTAINS(LCASE(?content), "KEYWORD_LOWER"))
}
ORDER BY DESC(?created)
LIMIT 20
```

### 10. Session Insight Pack — "Summarize what session S knew"

Given a session URI or `sourceFile`, return predicate mix + sample provenance facts (no JSONL required for a light summary).

```sparql
SELECT ?pred (COUNT(?kt) AS ?n) WHERE {
  ?sess devkg:hasSourceFile ?sourceFile .
  FILTER(CONTAINS(STR(?sourceFile), "SESSION_PATH_FRAGMENT"))
  ?kt a devkg:KnowledgeTriple ;
      devkg:extractedInSession ?sess ;
      devkg:triplePredicateLabel ?pred .
}
GROUP BY ?pred
ORDER BY DESC(?n)
LIMIT 24
```

Follow with sample facts:

```sparql
SELECT ?subj ?pred ?obj
       (SUBSTR(REPLACE(STR(?content), "\n", " "), 1, 160) AS ?snippet)
WHERE {
  ?sess devkg:hasSourceFile ?sourceFile .
  FILTER(CONTAINS(STR(?sourceFile), "SESSION_PATH_FRAGMENT"))
  ?kt a devkg:KnowledgeTriple ;
      devkg:extractedInSession ?sess ;
      devkg:tripleSubject ?s ;
      devkg:tripleObject ?o ;
      devkg:triplePredicateLabel ?pred ;
      devkg:extractedFrom ?msg .
  ?s rdfs:label ?subj . ?o rdfs:label ?obj .
  FILTER(LANG(?subj) = "" && LANG(?obj) = "")
  OPTIONAL { ?msg sioc:content ?content }
}
LIMIT 15
```

### 11. 2-Hop Neighborhood — "What connects to X and what connects to those?"

Traverses outbound edges from X, then follows outbound edges from each neighbor. Shows the subgraph reachable in 2 hops.

```sparql
SELECT DISTINCT ?aLabel ?p1 ?bLabel ?p2 ?cLabel WHERE {
  ?t1 a devkg:KnowledgeTriple ;
       devkg:tripleSubject ?a ;
       devkg:triplePredicateLabel ?p1 ;
       devkg:tripleObject ?b .
  ?a rdfs:label ?aLabel .
  ?b rdfs:label ?bLabel .
  FILTER(LANG(?aLabel) = "" && LANG(?bLabel) = "")
  FILTER(CONTAINS(LCASE(?aLabel), "ENTITY_LOWER"))
  OPTIONAL {
    ?t2 a devkg:KnowledgeTriple ;
         devkg:tripleSubject ?b ;
         devkg:triplePredicateLabel ?p2 ;
         devkg:tripleObject ?c .
    ?c rdfs:label ?cLabel .
    FILTER(LANG(?cLabel) = "")
  }
}
ORDER BY ?bLabel ?cLabel
LIMIT 40
```

For bidirectional 2-hop (also follows inbound edges), add a second UNION branch that reverses subject/object in each hop.

### 12. Hub Detection — "What are the most connected entities?"

```sparql
SELECT ?label (COUNT(DISTINCT ?triple) AS ?degree) WHERE {
  {
    ?triple a devkg:KnowledgeTriple ;
            devkg:tripleSubject ?e .
    ?e rdfs:label ?label .
    FILTER(LANG(?label) = "")
  } UNION {
    ?triple a devkg:KnowledgeTriple ;
            devkg:tripleObject ?e .
    ?e rdfs:label ?label .
    FILTER(LANG(?label) = "")
  }
}
GROUP BY ?label
ORDER BY DESC(?degree)
LIMIT 20
```

### 13. Cross-Session Entity Overlap — "What sessions share knowledge?"

```sparql
SELECT ?s1File ?s2File
       (COUNT(DISTINCT ?label) AS ?shared)
       (GROUP_CONCAT(DISTINCT ?label; separator=", ") AS ?sharedEntities)
WHERE {
  ?t1 a devkg:KnowledgeTriple ;
      devkg:tripleSubject ?e1 ;
      devkg:extractedInSession ?sess1 .
  ?t2 a devkg:KnowledgeTriple ;
      devkg:tripleSubject ?e2 ;
      devkg:extractedInSession ?sess2 .
  ?e1 rdfs:label ?label .
  ?e2 rdfs:label ?label .
  FILTER(LANG(?label) = "")
  FILTER(STR(?sess1) < STR(?sess2))
  OPTIONAL { ?sess1 devkg:hasSourceFile ?s1File }
  OPTIONAL { ?sess2 devkg:hasSourceFile ?s2File }
}
GROUP BY ?s1File ?s2File
HAVING(COUNT(DISTINCT ?label) > 2)
ORDER BY DESC(?shared)
LIMIT 10
```

### 14. Path Discovery — "How does X connect to Y?" (via intermediate entities)

```sparql
SELECT DISTINCT ?p1 ?midLabel ?p2 WHERE {
  {
    ?t1 a devkg:KnowledgeTriple ;
        devkg:tripleSubject ?a ;
        devkg:triplePredicateLabel ?p1 ;
        devkg:tripleObject ?mid .
    ?t2 a devkg:KnowledgeTriple ;
        devkg:tripleSubject ?mid ;
        devkg:triplePredicateLabel ?p2 ;
        devkg:tripleObject ?b .
  } UNION {
    ?t1 a devkg:KnowledgeTriple ;
        devkg:tripleSubject ?mid ;
        devkg:triplePredicateLabel ?p1 ;
        devkg:tripleObject ?a .
    ?t2 a devkg:KnowledgeTriple ;
        devkg:tripleSubject ?mid ;
        devkg:triplePredicateLabel ?p2 ;
        devkg:tripleObject ?b .
  } UNION {
    ?t1 a devkg:KnowledgeTriple ;
        devkg:tripleSubject ?a ;
        devkg:triplePredicateLabel ?p1 ;
        devkg:tripleObject ?mid .
    ?t2 a devkg:KnowledgeTriple ;
        devkg:tripleSubject ?b ;
        devkg:triplePredicateLabel ?p2 ;
        devkg:tripleObject ?mid .
  }
  ?a rdfs:label ?aLabel .
  ?b rdfs:label ?bLabel .
  ?mid rdfs:label ?midLabel .
  FILTER(LANG(?aLabel) = "" && LANG(?bLabel) = "" && LANG(?midLabel) = "")
  FILTER(CONTAINS(LCASE(?aLabel), "ENTITY_X"))
  FILTER(CONTAINS(LCASE(?bLabel), "ENTITY_Y"))
  FILTER(?a != ?b && ?a != ?mid && ?mid != ?b)
}
LIMIT 20
```

Present as: `ENTITY_X --p1--> intermediate --p2--> ENTITY_Y`

### 15. Project Knowledge Map — "What does project X know about?"

```sparql
SELECT ?label (COUNT(DISTINCT ?triple) AS ?mentions) WHERE {
  ?session devkg:belongsToProject ?project .
  ?project rdfs:label ?projectLabel .
  FILTER(CONTAINS(LCASE(?projectLabel), "PROJECT_LOWER"))
  ?triple a devkg:KnowledgeTriple ;
          devkg:extractedInSession ?session .
  { ?triple devkg:tripleSubject ?e . ?e rdfs:label ?label . }
  UNION
  { ?triple devkg:tripleObject ?e . ?e rdfs:label ?label . }
  FILTER(LANG(?label) = "")
}
GROUP BY ?label
ORDER BY DESC(?mentions)
LIMIT 30
```

### 16. Sibling Entities — "What else uses/requires/enables the same thing as X?"

```sparql
SELECT DISTINCT ?siblingLabel ?predicate ?sharedLabel WHERE {
  ?t1 a devkg:KnowledgeTriple ;
      devkg:tripleSubject ?x ;
      devkg:triplePredicateLabel ?predicate ;
      devkg:tripleObject ?shared .
  ?t2 a devkg:KnowledgeTriple ;
      devkg:tripleSubject ?sibling ;
      devkg:triplePredicateLabel ?predicate ;
      devkg:tripleObject ?shared .
  ?x rdfs:label ?xLabel .
  ?sibling rdfs:label ?siblingLabel .
  ?shared rdfs:label ?sharedLabel .
  FILTER(LANG(?xLabel) = "" && LANG(?siblingLabel) = "" && LANG(?sharedLabel) = "")
  FILTER(CONTAINS(LCASE(?xLabel), "ENTITY_LOWER"))
  FILTER(?x != ?sibling)
}
ORDER BY ?predicate ?sharedLabel
LIMIT 40
```

## Wikidata Graph Traversal

Many entities in the local graph have `owl:sameAs` links to Wikidata QIDs. You can **cross into Wikidata's public SPARQL endpoint** to discover knowledge that doesn't exist locally — drug classes, software ecosystems, related technologies, disambiguation, etc.

**Wikidata endpoint:** `https://query.wikidata.org/sparql`

**Execution pattern** (same as local, but different URL + requires User-Agent header):

```bash
curl -s -X POST 'https://query.wikidata.org/sparql' \
  -H 'Accept: application/sparql-results+json' \
  -H 'User-Agent: DevKG/1.0' \
  --data-urlencode "query=YOUR_SPARQL_HERE" \
  | jq -r '...'
```

**Rate limits:** Wikidata allows ~60 requests/minute for anonymous users. Add 1-second delay between queries if doing batch lookups.

### Workflow: Local → Wikidata → Back to Local

1. **Start local:** Use Template 1 to find what you know about entity X
2. **Get QID:** Use Template 8 to retrieve the `owl:sameAs` Wikidata URI
3. **Cross to Wikidata:** Use the QID in Wikidata templates below to discover new knowledge
4. **Come back:** Use what you learned to ask better local queries (e.g., discovered a peer → check if it exists locally)

### W1. Entity Properties — "What does Wikidata know about QID?"

Returns all direct properties with human-readable labels. Use this first to understand what's available.

```sparql
SELECT ?propLabel ?valLabel WHERE {
  wd:QID ?p ?val .
  ?prop wikibase:directClaim ?p .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
} LIMIT 30
```

Key properties to look for:
- `instance of` (P31) — what kind of thing it is
- `subclass of` (P279) — broader category
- `has use` (P366) — what it's used for
- `programmed in` (P277) — implementation language (software)
- `uses` (P2283) — technologies it depends on
- `part of` (P361) — larger system it belongs to
- `ATC code` (P267) — drug classification (medications)
- `route of administration` (P636) — how a drug is taken

### W2. Peer Discovery — "What else is the same kind of thing as X?"

Given a QID, finds its `instance of` class, then finds all other instances of that class. Discovers alternatives and competitors.

```sparql
SELECT ?peerLabel ?peerDescription WHERE {
  wd:QID wdt:P31 ?class .
  ?peer wdt:P31 ?class .
  FILTER(?peer != wd:QID)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
} LIMIT 20
```

Examples:
- Neo4j (Q1628290) → `instance of: graph database management system` → finds ArangoDB, JanusGraph, Amazon Neptune, Dgraph, etc.
- Fosfomycin (Q183554) → `instance of: type of chemical entity` → (too broad, use P2868 "subject has role" or ATC code instead)

### W3. Disambiguation — "Is this the right entity?"

When an entity label is ambiguous, fetch the Wikidata description to verify. Use this before trusting an `owl:sameAs` link.

```sparql
SELECT ?label ?description WHERE {
  wd:QID rdfs:label ?label .
  wd:QID schema:description ?description .
  FILTER(LANG(?label) = "en")
  FILTER(LANG(?description) = "en")
}
```

### W4. Broader Categories — "What category tree does X belong to?"

Traverses `subclass of` (P279) upward to find the classification hierarchy.

```sparql
SELECT ?classLabel ?superClassLabel WHERE {
  wd:QID wdt:P31 ?class .
  ?class wdt:P279* ?superClass .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
} LIMIT 20
```

### W5. Relationship Bridge — "How do two entities connect in Wikidata?"

When two local entities have Wikidata links but no direct local connection, check if Wikidata knows a relationship.

```sparql
SELECT ?propLabel WHERE {
  wd:QID_X ?p wd:QID_Y .
  ?prop wikibase:directClaim ?p .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
```

If no direct link, try 2-hop:

```sparql
SELECT ?propLabel1 ?midLabel ?propLabel2 WHERE {
  wd:QID_X ?p1 ?mid .
  ?mid ?p2 wd:QID_Y .
  ?prop1 wikibase:directClaim ?p1 .
  ?prop2 wikibase:directClaim ?p2 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
} LIMIT 10
```

### W6. Batch QID Lookup — "Enrich all linked entities at once"

First get all QIDs from the local graph, then query Wikidata for their classes in one request.

**Step 1 (local):** Extract QIDs

```sparql
SELECT ?label (REPLACE(STR(?wikidata), "http://www.wikidata.org/entity/", "") AS ?qid) WHERE {
  ?e a devkg:Entity ; rdfs:label ?label ; owl:sameAs ?wikidata .
  FILTER(LANG(?label) = "")
  FILTER(STRSTARTS(STR(?wikidata), "http://www.wikidata.org"))
}
```

**Step 2 (Wikidata):** Get classes for multiple QIDs at once (use VALUES clause):

```sparql
SELECT ?item ?itemLabel ?classLabel WHERE {
  VALUES ?item { wd:Q1628290 wd:Q183554 wd:Q28865 }
  ?item wdt:P31 ?class .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
```

### When to Use Wikidata Traversal

| Question | Local enough? | Use Wikidata? |
|----------|--------------|---------------|
| "What does X integrate with?" | Yes (Template 1) | No |
| "What kind of thing is X?" | Maybe (if `isTypeOf` exists) | **Yes** (W1, W4) |
| "What are alternatives to X?" | Maybe (if `alternativeTo` exists) | **Yes** (W2) |
| "Is this the right entity?" | No | **Yes** (W3) |
| "How does X relate to Y globally?" | No | **Yes** (W5) |
| "What drug class is X in?" | No | **Yes** (W1 → ATC code, P2868) |
| "What language is X written in?" | Maybe | **Yes** (W1 → P277) |

## Tips

- **Session discovery ("where / which sessions"): always start with Template 5** (topic + intent + provenance). Do not start with label-only Template 6 or grep.
- Always use `DISTINCT` — duplicate triples exist from lang-tagged vs untagged literals.
- Always use `FILTER(LANG(?label) = "")` to avoid duplicate rows from lang-tagged literals.
- Entity labels are lowercase in the graph. Always use `LCASE()` in FILTER for safety.
- Multi-signal filters beat single keywords: topic (`linkedin`) **and** intent (`profile`, `career`, `roberto`).
- For "What integrates with X?" questions, use Template 1 (bidirectional) — the relationship may be stored in either direction.
- `KnowledgeTriple` nodes carry provenance: `extractedFrom` → source message, `extractedInSession` → session. Always project these when the user needs *where*.
- `sioc:content` is capped at ~2000 chars — enough to locate and lightly reason; open JSONL only for full fidelity.
- When following `hasSourceFile`, **normalize the path first**. If `PRUNED`, reconstruct from triples — do not grep.
- If Fuseki returned provenance hits, **do not** fall back to grep.
- Combine templates: e.g., Template 5 → Template 10 (session insight) → Template 8 (Wikidata) as needed.
- **Start with Template 12 (hubs)** when exploring an unfamiliar graph.
- **Use Template 14 (path discovery)** before concluding two concepts are unrelated.
- **Use Template 16 (siblings)** to discover alternatives and peers.
- Prefer relationship predicates (`uses`, `dependsOn`, `solves`, …) over treating the graph as a tag cloud of labels.
