---
name: sparql-query-wikidata
description: Use this skill whenever the user asks about real-world facts that could appear in Wikipedia or an encyclopedia — people, places, events, organisations, species, works of art, historical dates, geographic data, scientific concepts, and so on. Prefer live Wikidata data over relying on the model's training knowledge.
---

# Wikidata SPARQL Skill

## ⚠️ Mandatory workflow — never skip or reorder steps

**Follow every step below for every query — even when the entity or its Q-number seems obvious from training knowledge.**
Prior knowledge is unreliable for entity IDs and property sets. Skipping steps causes wrong IDs, wrong properties, and wrong results.

### Step 0 — Search before querying (use `wikidata_search`)
Before writing any SPARQL, resolve every unknown entity name and every property
name to its Q/P number with the `wikidata_search` tool.
Do **not** guess Q/P numbers from training knowledge — they are unreliable.

```
# Find the item for an entity
wikidata_search(term="Marie Curie")              → Q7186

# Find the property you need
wikidata_search(term="date of birth", type="property")  → P569
```

`wikidata_search` → `sparql_query_wikidata` is the **standard opening move**
for every Wikidata session. Run the search first, then build the SPARQL query
using the confirmed IDs.

### Step 1 — Check existing queries
Run `discover_sparql_queries`. Reuse or adapt any matching `.rq` file instead of writing from scratch.

### Step 2 — Resolve the entity ID from Wikidata (never assume a Q-number)
Look up the entity by label — do not rely on memorised Q-numbers:

```sparql
SELECT ?item ?itemLabel WHERE {
  ?item rdfs:label "München"@de .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "de,en". }
}
LIMIT 5
```

### Step 3 — Identify the entity type (P31)
Fetch the type so you know which domain file to read:

```sparql
SELECT ?type ?typeLabel WHERE {
  wd:Q1726 wdt:P31 ?type .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```

### Step 4 — Read the matching domain file (mandatory before writing the final query)
Match the P31 result to the table below and **read that file now**.
The domain file contains the correct property set and known pitfalls — do not guess.

| Domain file | Typical P31 types |
|-------------|-------------------|
| `./domains/city.md` | city (Q515), big city (Q1549591), human settlement (Q486972) |
| `./domains/person.md` | human (Q5) |
| `./domains/organisation.md` | business (Q4830453), nonprofit (Q163740), government agency (Q327333) |
| `./domains/creative-work.md` | film (Q11424), book (Q571), album (Q482994), TV series (Q5398426) |
| `./domains/chemical-compound.md` | chemical compound (Q11173), drug (Q12140) |

Load **only** the relevant domain file — do not load all of them.

> **If no domain file matches**, run a namespace inventory to discover available properties:
> ```sparql
> SELECT ?prop (COUNT(?value) AS ?count) WHERE {
>   wd:Q1726 ?prop ?value .
> }
> GROUP BY ?prop
> ORDER BY DESC(?count)
> LIMIT 30
> ```

### Step 5 — Write the domain-specific query
Use the `VALUES` clause with the property set from the domain file. Do not select all predicates with an unbound `?prop ?value` pattern:

```sparql
SELECT ?propLabel ?valueLabel WHERE {
  VALUES ?prop { wdt:P31 wdt:P17 wdt:P131 wdt:P1082 }  # taken from domain file
  wd:Q1726 ?prop ?value .
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en" .
    ?prop  rdfs:label ?propLabel .
    ?value rdfs:label ?valueLabel .
  }
}
```

### Step 6 — Present results faithfully
Only state what the queried data shows. Mark anything else as *"interpretation — not modelled in Wikidata"*.

---

## Key Wikidata concepts

| Concept | Description | Example |
|---------|-------------|---------|
| Entity (Q-item) | A Wikidata subject | `wd:Q64` = Berlin |
| Direct property (P-item) | Simple S→O statement | `wdt:P31` = instance of |
| Full statement (p:/ps:/pq:) | Statement with qualifiers | `p:P131/ps:P131` |
| Labels | Human-readable names | `rdfs:label` or `wikibase:label` service |

## Auto-injected prefixes

These are always available — **no PREFIX declaration needed**:

```
wd:       http://www.wikidata.org/entity/
wdt:      http://www.wikidata.org/prop/direct/
wikibase: http://wikiba.se/ontology#
p:        http://www.wikidata.org/prop/
ps:       http://www.wikidata.org/prop/statement/
pq:       http://www.wikidata.org/prop/qualifier/
rdfs:     http://www.w3.org/2000/01/rdf-schema#
schema:   https://schema.org/
skos:     http://www.w3.org/2004/02/skos/core#
owl:      http://www.w3.org/2002/07/owl#
xsd:      http://www.w3.org/2001/XMLSchema#
bd:       http://www.bigdata.com/rdf#
```

---

## Common patterns (reference)

### Look up a known entity by label
```sparql
SELECT ?item ?itemLabel WHERE {
  ?item rdfs:label "Berlin"@en .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 5
```

### Search entities by label substring
```sparql
SELECT ?item ?label WHERE {
  ?item rdfs:label ?label .
  FILTER(LANG(?label) = "en")
  FILTER(CONTAINS(LCASE(STR(?label)), "berlin"))
}
LIMIT 10
```

### All instances of a class (e.g. cities)
```sparql
SELECT ?city ?cityLabel WHERE {
  ?city wdt:P31 wd:Q515 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 20
```

### Efficient label fetching with wikibase:label service
```sparql
SELECT ?item ?itemLabel WHERE {
  ?item wdt:P31 wd:Q515 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 20
```

### Count instances of a class
```sparql
SELECT (COUNT(?item) AS ?count) WHERE {
  ?item wdt:P31 wd:Q515 .
}
```

### Multi-hop traversal (city → country → continent)
```sparql
SELECT ?city ?cityLabel ?country ?countryLabel ?continent ?continentLabel WHERE {
  ?city    wdt:P31  wd:Q515 ;
           wdt:P17  ?country .
  ?country wdt:P30  ?continent .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 20
```

### Statements with qualifiers (full statement model)
```sparql
SELECT ?item ?start ?end WHERE {
  ?item p:P39 ?stmt .             # P39 = position held
  ?stmt ps:P39 wd:Q11696 ;       # head of state
        pq:P580 ?start .
  OPTIONAL { ?stmt pq:P582 ?end }
}
LIMIT 10
```

> **⚠️ Never present inferences as Wikidata facts.** Every statement must be backed by a queried triple. Mark anything else as *"interpretation — not modelled in Wikidata"*.

---

## Tips

- **Always call `wikidata_search` first** to resolve entity and property names to Q/P IDs before writing any SPARQL. Never assume a Q or P number.
- Prefer `wdt:P<n>` (direct property) for simple facts; use `p:/ps:/pq:` only when you need qualifiers or ranks.
- Always `FILTER(LANG(?label) = "en")` when using `rdfs:label` directly to avoid multi-language result explosion.
- The `wikibase:label` service is faster and cleaner for label retrieval than joining on `rdfs:label`.
- Wikidata is huge — always use `LIMIT` (automatically enforced by the tool if omitted).
- If a query times out (Wikidata has a 60-second limit), narrow it with more specific `wdt:P31` values or add `LIMIT`.
- **Never use `wdt:P131*` path traversal** to reach a parent region — it causes timeouts. Use `wdt:P17` for country instead.
