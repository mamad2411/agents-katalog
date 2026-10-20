# Recall Module

Cross-store recall seam. One natural-language query returns ranked,
source-tagged hits across every registered contributor: `knowledge`, `memory`,
`history`, `tasks`, and the answer-history corpus contributed by the answer
module.

## Ownership

- `RecallProvider` validates source filters, resolves scope context, classifies
  semantic availability, queries contributors, normalizes scores, and returns
  the public `RecallResult` directly.
- `RecallContributor` is the typed registration protocol for store owners.
- `query.ts` is the shared untrusted-wire decoder for `POST /recall` and
  `POST /api/recall`. Routes only decode, delegate, and map the typed
  unknown-scope error to HTTP.
- The generated routine client binding owns daemon transport. The local client
  late-binds the registered provider and returns the same domain result without
  rebuilding its union.
- The CLI and tool validate their own public inputs and render the domain
  result. They do not inspect contributor state or reclassify availability.
- `render.ts` owns the plain-text hit projection. The cross-client fixture in
  `clients/conformance/` pins the shared rendering contract.

## Contributor registration

A new store extends the source and hit unions in `client.ts`, adds its raw arm
in `recall-types.ts`, and implements `RecallContributor` beside the owning
store. Its module registers and unregisters that contributor through the typed
recall provider token and declares a runtime dependency on `recall`.

The first-party raw-store contributors live in `contributors.ts`. The answer
contributor lives in `src/modules/answer/recall-contributor.ts`; registration
flows one way through the public provider API, so recall does not depend on the
answer module.

## Ranking and degradation

Contributors return native scores. Recall normalizes once per source into
`[0, 1]`, merges the batches, sorts by normalized score, and tie-breaks by
`RECALL_SOURCE_ORDER` then id.

A contributor without a semantic backend uses its store's keyword fallback. A
contributor that throws logs once and contributes an empty batch. With no
registered contributors, the provider returns `semantic_unavailable`; routes,
clients, tools, and CLIs consume that classification rather than duplicating
it.

## Boundaries

- Contributors use the supplied scope context. Do not introduce global
  provider getters or a second contributor registry.
- Per-store query paths and semantic indexes remain owned by their store
  modules; recall adds no embedding cache or index format.
- Answer-history hits carry the prior query, preview, citation count, and
  timestamp needed for ranking and rendering. They do not embed a copied
  `AnswerResult`; the answer-history store remains the provenance owner.
