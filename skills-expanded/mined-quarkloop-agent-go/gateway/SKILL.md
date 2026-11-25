# service-gateway

Gateway is the single agent-facing boundary for LLM generation, embeddings,
reranking, token counting, provider health, model listing, fallback, and usage
accounting. It embeds Bifrost internally; agents and runtime must not call LLM
providers directly.

## Agent Rules

1. Use normal runtime reasoning for conversational responses. Do not call
   provider adapters directly and do not expose provider-specific HTTP payloads.
2. Use Gateway service functions only when a workflow explicitly needs model,
   embedding, rerank, token, health, or model-list data as a service result.
3. Treat usage as structured accounting data. Never store prompts, raw response
   text, tool arguments, API keys, or provider credentials in usage records.
4. Preserve provider, model, token counts, latency, cost estimate, fallback
   chain, request ID, and finish reason in diagnostics.
5. If fallback happens, report the fallback chain without hiding the original
   provider failure.
6. Services must not call Gateway. The agent/runtime coordinates model calls
   and passes resulting canonical data to other services.

## Service Functions

- `Generate(GenerateRequest) -> GenerateResponse`
  - Generated service function: `gateway_Generate`
  - NATS subject: `svc.gateway.v1.generate`
  - Runs one non-streaming generation and returns text, tool calls, and usage.

- `StreamGenerate(StreamGenerateRequest) -> stream StreamGenerateResponse`
  - Generated service function: `gateway_StreamGenerate`
  - NATS subject: `svc.gateway.v1.stream_generate`
  - Streams deltas/tool calls and emits final structured usage.

- `Embed(EmbedRequest) -> EmbedResponse`
  - Generated service function: `gateway_Embed`
  - NATS subject: `svc.gateway.v1.embed`
  - Creates provider-backed text or supported multimodal embeddings with
    provider/model/dimension metadata. Use runtime content, page, or media
    references for extracted material.

- `Rerank(RerankRequest) -> RerankResponse`
  - Generated service function: `gateway_Rerank`
  - NATS subject: `svc.gateway.v1.rerank`
  - Scores candidate documents for one query.

- `CountTokens(CountTokensRequest) -> CountTokensResponse`
  - Generated service function: `gateway_CountTokens`
  - NATS subject: `svc.gateway.v1.count_tokens`
  - Counts or estimates prompt/tool tokens without generation.

- `ListModels(ListModelsRequest) -> ListModelsResponse`
  - Generated service function: `gateway_ListModels`
  - NATS subject: `svc.gateway.v1.list_models`
  - Lists models exposed by provider policy.

- `ProviderHealth(ProviderHealthRequest) -> ProviderHealthResponse`
  - Generated service function: `gateway_ProviderHealth`
  - NATS subject: `svc.gateway.v1.provider_health`
  - Reports provider adapter readiness.

- `UsageSummary(UsageSummaryRequest) -> UsageSummaryResponse`
  - Generated service function: `gateway_UsageSummary`
  - NATS subject: `svc.gateway.v1.usage_summary`
  - Returns redacted aggregate usage by provider and model.

- `ReloadConfig(ReloadConfigRequest) -> ReloadConfigResponse`
  - Generated service function: `gateway_ReloadConfig`
  - NATS subject: `svc.gateway.v1.reload_config`
  - Reloads provider and fallback policy after explicit approval.

## Boundaries

- Gateway owns provider dispatch, Bifrost lifecycle, fallback ordering, model
  response usage accounting, provider diagnostics, and provider error mapping.
- Embedding requests use the configured Gateway embedding provider and model;
  do not request local or synthetic vectors.
- To query indexed knowledge, pass one non-empty retrieval query in the exposed
  literal `text` parameter. It must faithfully represent the user's request. Do not pass a runtime
  reference or generate separate vectors for individual subquestions.
- For extracted content or media, pass runtime-issued references instead of
  copying binary media into a service call. For canonical knowledge indexing,
  use one bounded `pageRef` for a PDF that exposes page references; do not
  copy PDF text or embed a whole-document `contentRef` as a searchable chunk.
  For a batch of PDFs, call `gateway_Embed` with `pageRefs` containing one
  exact page reference returned by extraction for each source and omit
  `inputs`; runtime restores the source provenance for those references.
  For non-PDF text, a short agent-authored text chunk is permitted. Prepare the
  canonical chunk before embedding: each multi-source batch input represents
  one source and must be reused unchanged in the matching index write after
  embedding succeeds.
  Detailed canonical chunk records are persisted one complete record per
  source; independent records may be issued in the same tool-call batch.
  Gateway only supplies their previously prepared embeddings.
- The OpenRouter-compatible adapter supports mixed text/image embedding
  content. Adapters that cannot represent media inputs reject them explicitly.
- Runtime owns session/run accumulation and persistence through runtime/Core
  activity storage.
- Provider secrets are resolved by deployment or the future Secrets service and
  must be redacted from logs, prompts, service responses, and telemetry.
