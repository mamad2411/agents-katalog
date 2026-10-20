# Answer Module

Cited-answer seam on top of cross-store recall. One natural-language query
returns a short composed answer plus typed citations resolving to the exact
`RecallHit`s used for synthesis.

## Ownership

- `AnswerProviderImpl` implements the public `AnswerClient`. It delegates scope
  selection to the shared daemon selector and owns recall-to-answer classification, citation validation, answer
  assembly, persistence, history listing, and history not-found results.
- Routes decode requests, delegate, and map the typed unknown-scope error to
  HTTP. Generated routine bindings own daemon transport; the local client
  late-binds the same registered domain provider.
- Chat command request policy and plain-text outcomes live in `commands.ts`.
  Channels supply a scope-selected client and parsed body, then own output limits
  and delivery. Client errors propagate to their existing error paths.
- The CLI and tool validate their public inputs and render the direct domain
  result. Failure wording is owned by `render.ts`, not copied per surface.
- The answer module registers its answer-history recall contributor through
  the typed recall provider token. Recall never imports answer code.

## Citation contract

The synthesizer emits `[source:id]` markers whose source is a `RecallSource`
and whose id resolves against the exact hit pile supplied to the model. The
provider preserves markers in the answer, de-duplicates citations in original
order, caps them at `ANSWER_MAX_CITATIONS`, and returns only referenced hits.

Unknown or absent markers cause one synthesis retry with restricted-marker
guidance. A second invalid response becomes `synthesis_failed`. A recall
`semantic_unavailable` result propagates directly; an empty successful recall
becomes `no_hits`. There are at most two model calls.

## Persisted answer history

Every answer attempt appends one versioned record through `AnswerHistoryStore`.
An append failure is warned but does not alter the operator-visible result.
The store owns retention, decoding, legacy migration, atomic replacement,
listing, lookup, and keyword search for the recall contributor.

`AnswerFailure` is the single failure union used by live results and persisted
history. Recall projections summarize prior records and never copy that result
matrix. Scope-scoped reads and writes use `AnswerScopeContext`; there is no
parallel persistence or retrieval path. The initial history store stays bound to
its construction workspace; supplied host lookups never use an ambient host.

## Boundaries

- Reuse recall's typed hits and contributor registry; do not add an embedding
  cache, second retrieval path, or provider globals.
- Synthesis prompt tuning stays internal to `synthesis-prompt.ts`.
- Do not surface cost into autonomy or add a second answer envelope.
