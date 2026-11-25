---
name: aem-oak-index
description: Oak index review and creation — index type selection, property coverage, evaluatePathRestrictions, async configuration
allowed-tools: Read, Grep, Glob
argument-hint: "[index XML file path, or query to create an index for]"
---

Review or create an Oak index for: `$ARGUMENTS`

## If reviewing an existing index

Check each of the following. Report as **Blocking** / **Warning** / **Suggestion**.

**Type and async**
- `type` is `lucene` or `property` — never `traversal` — Blocking
- `async` is set to `async` or `async,nrt` — synchronous indexing blocks writes — Blocking
- Index type matches the query pattern — `property` for simple equality, `lucene` for full-text or multi-property — Warning

**Coverage**
- All properties referenced in the corresponding query are indexed — Blocking
- `evaluatePathRestrictions=true` when the query uses `ISDESCENDANTNODE` or path restrictions — Blocking
- `nodeTypes` is scoped to the types the query targets — not indexing all node types — Warning
- `nodeScopeIndex` is not enabled unless full-text search across node content is genuinely needed — Warning

**Naming and placement**
- Index is in `ui.apps` under `oak:index` and embedded in `all/` — Warning
- Index name follows project convention (e.g. `<project>-<purpose>-lucene`) — Suggestion

## If creating a new index

1. Identify the query (JCR-SQL2 or XPath) that needs the index
2. Identify the node types, properties, and path restrictions in the query
3. Choose the index type:
   - Multi-property or full-text → `lucene`
   - Single property, exact match, low cardinality → `property`
4. Generate the index definition XML:
   - Set `jcr:primaryType=oak:QueryIndexDefinition`
   - Set `type`, `async=async`, `evaluatePathRestrictions=true` (if path-restricted)
   - Add `indexRules` with the correct node type and property definitions
5. Place the file under `ui.apps/src/main/content/jcr_root/oak:index/`
6. Confirm it is embedded in `all/pom.xml`
7. Provide the `EXPLAIN` statement to validate the index is selected at runtime
