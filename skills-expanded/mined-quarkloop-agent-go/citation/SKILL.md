# service-citation

The citation service resolves source spans and verifies grounding. It is a
mechanical evidence service, not an answer generator.

## Agent Workflows

1. After the LLM selects facts, claims, and candidate evidence, call
   `citation_ResolveSpans` to normalize source spans and offsets.
2. Use `citation_CreateCitation` when a single selected evidence phrase needs a
   normalized citation record.
3. Before answering or indexing high-value claims, call
   `citation_VerifyGrounding` when grounding needs mechanical verification.
4. Use `citation_ScoreCoverage` to summarize grounding coverage across a set
   of claims before a final answer or index write.
5. Use `citation_RenderReferences` to render source references for user-facing
   answers and manual verification artifacts.
6. Pass resolved citations to `indexer_UpsertChunk.citations`,
   `indexer_UpsertFact.fact.citations`, and `provenance`.

## RPCs

- `ResolveSpans(ResolveSpansRequest) -> ResolveSpansResponse`
  - Generated service function: `citation_ResolveSpans`
- `CreateCitation(CreateCitationRequest) -> CitationSpan`
  - Generated service function: `citation_CreateCitation`
- `VerifyGrounding(VerifyGroundingRequest) -> VerifyGroundingResponse`
  - Generated service function: `citation_VerifyGrounding`
- `ScoreCoverage(ScoreCoverageRequest) -> ScoreCoverageResponse`
  - Generated service function: `citation_ScoreCoverage`
- `RenderReferences(RenderReferencesRequest) -> RenderReferencesResponse`
  - Generated service function: `citation_RenderReferences`

## Contract Notes

- The agent chooses claims and evidence candidates.
- `citation_VerifyGrounding.claims` and `citation_ScoreCoverage.claims` are
  JSON arrays of claim objects, not strings containing serialized JSON. Each
  claim includes `id`, `claim`, and a `citations` array.
- `CitationSpan` objects use exactly `id`, `sourceUri`, `textSpan`,
  `startOffset`, `endOffset`, and `confidence`. Do not send `chunkId`,
  `filename`, `source`, `sourceText`, or arbitrary metadata inside a citation
  span.
- Mechanical verification requires a non-empty `textSpan` obtained from
  evidence; if retrieved context supplies only source references, use
  `citation_RenderReferences` instead of inventing spans.
- `citation_ResolveSpans` requires exact `sourceText`. Use it while source
  text is available during extraction/indexing; for retrieved index context,
  prefer `citation_VerifyGrounding` or `citation_RenderReferences` with
  citation spans from the retrieved chunks.
- This service does not call LLMs, query the indexer, or generate final
  answers.
- Verification results are evidence diagnostics; the agent decides how to use
  them in final reasoning.
