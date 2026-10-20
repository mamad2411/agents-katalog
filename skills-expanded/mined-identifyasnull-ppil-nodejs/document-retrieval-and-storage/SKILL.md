# document-retrieval-and-storage

Purpose
- Explain correct patterns for retrieving documents (Mango-style selectors and utility helpers) and for persisting/updating documents via service client `synchroniseDocument`.

When to use
- Any compute flow, task, or job that needs to assemble composite documents from multiple source document types and save or update derived documents (for example: building `search` documents from primary/ad/serviceProvider records).

Key concepts (summary)
- Retrieval
  - Site `cfg` clients are mandatory: use `await cfg.getClient(serviceName)` or `await cfg.getClientByDocumentType(type)` to obtain service clients.
  - Use inline filter vars to create filters unless the pattern is highly repetitive to fetch many documents by a key list. This is more efficient than repeated single-document reads.
  - For ad-hoc queries, use `client.getDocumentByFilter('type', { selector: { ... }, limit, suppressMessages: true })` where `selector` is a Mango-style object (keys + operators). Always include a `limit` when expecting small results.

- Selection shapes (Mango selector)
  - Selector is a plain object: e.g. `{ documentType: 'search', searchIdField: primaryId }` or more complex nested conditions.
  - When constructing selectors from external input, validate/normalize values (trim strings, ensure IDs are present) to avoid broad scans.

- Persisting / synchroniseDocument
  - Use `client.synchroniseDocument(documentType, null, documentsArray)` to push batched adds/updates/deletes. The third arg may be:
    - an array of full document objects to be created/updated/deleted (deleted items include `_deleted: true`), or
    - a single object for single-operation deletes/updates.
  - The returned `syncResult` typically includes `adds`, `updates`, `deletes`, and `skippedUpdates` arrays. Inspect each to determine which primary items succeeded.
  - Map returned items back to source primary IDs (e.g. the repo uses `searchIdField = `${primaryKey}Id``) and convert those to batchIds for downstream completion/failure tracking.

Best practices
- Idempotency and deduplication
  - Always construct stable `id` for derived documents when possible (use existing `id` or generate a GUID on first creation then derive a short hash for `idHash`) so repeated runs do not create duplicates.

- Batching
  - Batch fetch and batch write. `fetchDocumentsByValues` and `synchroniseDocument` accept arrays and are far more efficient than per-document network calls.

- Error handling
  - On synchronise failure, mark the entire batch items as failed and log the error with stack. When partial success is returned, use `skippedUpdates` to mark specific items failed.
  - Wrap per-primary processing in try/catch; accumulate `failedBatchIds` and `completedBatchIds` for a compact result object that callers expect.

- Mapping & indexing
  - Keep a stable mapping between primary ids and derived document fields (e.g. `searchIdField`) so sync results can be correlated back to originals.

- Performance
  - Avoid rebuilding large Maps repeatedly in tight loops. Build maps once and reuse them during the run.

- Logging & diagnostics
  - Use `cfg.logDiag.log` for fine-grained diagnostic messages and `cfg.log.info/warn/error` for operational events.

- Client APIs & cfg
  - Use `cfg.getImport('search-engine')` or `cfg.getClient(...)` as shown in `generateSearchObject.mjs` to resolve providers and clients. Use `global.configProvider.get(argv.cfg)` in CLI/task contexts.

Common pitfalls
- Assuming all returned `adds`/`updates` contain source-id fields — always check and guard.
- Rebuilding selectors on the listing side: prefer saved derived state and explicit `_deleted` flags rather than relying on recomputation.

Example snippets (derived from generateSearchObject.mjs)
- Bulk fetch primary docs
```js
const primaryDocs = await util.fetchDocumentsByValues(primaryClient, primaryType, primaryIdField, documentIds, null, true);
```

- Preferred: Single-filter Mango query (ensure `limit`)
```js
const docs = await primaryClient.getDocumentByFilter('search', {
  selector: { documentType: 'search', [searchIdField]: primaryId },
  limit: 1,
  suppressMessages: true
}) ?? [];
```

- Batch synchronise
```js
const syncResult = await primaryClient.synchroniseDocument('search', null, searchObjectsToSync);
// syncResult.adds, syncResult.updates, syncResult.deletes, syncResult.skippedUpdates
```

Integration notes for Author JAL agent
- This skill documents the recommended implementation and should be included in the Author JAL Site Agent knowledge set so site authors follow the same retrieval/storage contract used by `generateSearchObject.mjs`.

Operational checklist for implementers
- Use `fetchDocumentsByValues` for bulk fetches by value, i.e. by a primary key field.
- Build Maps keyed by id for O(1) lookups for larger scale processing.
- Keep `searchIdField` and mapping to primary ids consistent across runs.
- Use `synchroniseDocument` for batched persistence and inspect `syncResult` for partial failures.
- On failure, mark batch ids failed; on success, mark completed.

End.
# document-retrieval-and-storage

Purpose
- Explain correct patterns for retrieving documents (Mango-style selectors and utility helpers) and for persisting/updating documents via service client `synchroniseDocument`.

When to use
- Any compute flow, task, or job that needs to assemble composite documents from multiple source document types and save or update derived documents (for example: building `search` documents from primary/ad/serviceProvider records).

Key concepts (summary)
- Retrieval
  - Site `cfg` clients are mandatory: use `await cfg.getClient(serviceName)` or `await cfg.getClientByDocumentType(type)` to obtain service clients.
  - Use inline filter vars to create filters unless the pattern is highly repetitive to fetch many documents by a key list. This is more efficient than repeated single-document reads.
  - For ad-hoc queries, use `client.getDocumentByFilter('type', { selector: { ... }, limit, suppressMessages: true })` where `selector` is a Mango-style object (keys + operators). Always include a `limit` when expecting small results.

- Selection shapes (Mango selector)
  - Selector is a plain object: e.g. `{ documentType: 'search', searchIdField: primaryId }` or more complex nested conditions.
  - When constructing selectors from external input, validate/normalize values (trim strings, ensure IDs are present) to avoid broad scans.

- Persisting / synchroniseDocument
  - Use `client.synchroniseDocument(documentType, null, documentsArray)` to push batched adds/updates/deletes. The third arg may be:
    - an array of full document objects to be created/updated/deleted (deleted items include `_deleted: true`), or
    - a single object for single-operation deletes/updates.
  - The returned `syncResult` typically includes `adds`, `updates`, `deletes`, and `skippedUpdates` arrays. Inspect each to determine which primary items succeeded.
  - Map returned items back to source primary IDs (e.g. the repo uses `searchIdField = `${primaryKey}Id``) and convert those to batchIds for downstream completion/failure tracking.

Best practices
- Idempotency and deduplication
  - Always construct stable `id` for derived documents when possible (use existing `id` or generate a GUID on first creation then derive a short hash for `idHash`) so repeated runs do not create duplicates.

- Batching
  - Batch fetch and batch write. `fetchDocumentsByValues` and `synchroniseDocument` accept arrays and are far more efficient than per-document network calls.

- Error handling
  - On synchronise failure, mark the entire batch items as failed and log the error with stack. When partial success is returned, use `skippedUpdates` to mark specific items failed.
  - Wrap per-primary processing in try/catch; accumulate `failedBatchIds` and `completedBatchIds` for a compact result object that callers expect.

- Mapping & indexing
  - Keep a stable mapping between primary ids and derived document fields (e.g. `searchIdField`) so sync results can be correlated back to originals.

- Performance
  - Avoid rebuilding large Maps repeatedly in tight loops. Build maps once and reuse them during the run.

- Logging & diagnostics
  - Use `cfg.logDiag.log` for fine-grained diagnostic messages and `cfg.log.info/warn/error` for operational events.

- Client APIs & cfg
  - Use `cfg.getImport('search-engine')` or `cfg.getClient(...)` as shown in `generateSearchObject.mjs` to resolve providers and clients. Use `global.configProvider.get(argv.cfg)` in CLI/task contexts.

Common pitfalls
- Assuming all returned `adds`/`updates` contain source-id fields — always check and guard.
- Rebuilding selectors on the listing side: prefer saved derived state and explicit `_deleted` flags rather than relying on recomputation.

Example snippets (derived from generateSearchObject.mjs)
- Bulk fetch primary docs
```js
const primaryDocs = await util.fetchDocumentsByValues(primaryClient, primaryType, primaryIdField, documentIds, null, true);
```

- Preferred: Single-filter Mango query (ensure `limit`)
```js
const docs = await primaryClient.getDocumentByFilter('search', {
  selector: { documentType: 'search', [searchIdField]: primaryId },
  limit: 1,
  suppressMessages: true
}) ?? [];
```

- Batch synchronise
```js
const syncResult = await primaryClient.synchroniseDocument('search', null, searchObjectsToSync);
// syncResult.adds, syncResult.updates, syncResult.deletes, syncResult.skippedUpdates
```

Integration notes for Author JAL agent
- This skill documents the recommended implementation and should be included in the Author JAL Site Agent knowledge set so site authors follow the same retrieval/storage contract used by `generateSearchObject.mjs`.

Operational checklist for implementers
- Use `fetchDocumentsByValues` for bulk fetches by value, i.e. by a primary key field.
- Build Maps keyed by id for O(1) lookups for larger scale processing.
- Keep `searchIdField` and mapping to primary ids consistent across runs.
- Use `synchroniseDocument` for batched persistence and inspect `syncResult` for partial failures.
- On failure, mark batch ids failed; on success, mark completed.

End.
