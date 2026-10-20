# GraphQL Federation Gateway

## Summary

**One-sentence:** GraphQL federation via Apollo Router creates a unified supergraph from independently deployed domain subgraphs with depth/complexity limits and CI-validated composition.

**One-paragraph:** Defines the gateway configuration for Apollo Router federation v2: subgraph entity ownership with @key, query depth/complexity/alias limits, persisted queries, JWT auth at the router, and CI-validated rover supergraph compose. Output is a gateway config artefact plus a CI workflow that blocks merges on composition errors or breaking subgraph changes.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'GraphQL federation gateway' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф конфігу до того, як він потрапить у CI.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Multiple teams maintaining independent GraphQL services that need a unified client API.
- Migrating from REST to GraphQL across multiple services without a big-bang rewrite.
- Building a composite data layer where entities are owned by different services but cross-referenced in queries.
- Need GraphQL-specific query controls (depth, complexity, persisted queries) at a single gateway layer.

## Skip If (ANY kills it)

- Single-team GraphQL monolith — federation adds operational overhead without benefit when one team owns the schema.
- REST-only backends where GraphQL is not used — use a REST gateway pattern instead.
- Simple BFF where one gateway aggregates a few REST endpoints — REST aggregation is simpler.
- Team without GraphQL expertise — federation v2 directives have a significant learning curve.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Subgraph schemas | GraphQL SDL | each service repo |
| Apollo Router version + flavor | config | engagement charter |
| Auth contract (JWT issuer + JWKS) | URL + claims map | identity provider |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/api-gateway-patterns` | Establishes the gateway role this methodology refines for GraphQL. |
| `solo/dev/software-architect/api-gateway-security` | Auth/TLS layer this config plugs into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the gateway config + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: subgraph audit → directives → router config → limits → auth → CI compose | ~900 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compose-supergraph` | sonnet | Rover compose + breaking-change check per subgraph PR. |
| `draft-router-config` | sonnet | Schema-driven config templating. |
| `audit-cross-subgraph-types` | opus | Cross-service entity ownership analysis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/router.yaml` | Apollo Router config with auth, depth/complexity limits, and SARIF output. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-gateway-graphql.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[api-gateway-patterns]]
- [[api-gateway-security]]
- [[api-gateway-resilience]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
