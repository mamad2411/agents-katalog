---
name: data-and-ai-pipelines
description: >
  Build data and AI infrastructure. Use for data pipelines (ingest, transform,
  serve), batch vs stream processing, data warehouses/lakes, key data terms,
  AI agents, LLM serving, the open-source AI stack, and data merging/analysis.
  Triggers: "data pipeline", "ETL/ELT", "data warehouse", "AI agent", "LLM
  serving", "open source AI", "ChatGPT architecture".
---

# Data and AI Pipelines

Move data from source to insight/model reliably, and serve AI workloads.

## When to use
- Designing ingestion, transformation, or serving layers.
- Choosing batch vs stream processing.
- Building or integrating AI/LLM features.
- Data modeling and terminology alignment.

## Pipeline stages
1. **Ingest** — batch (scheduled pulls), stream (events, CDC), or APIs.
2. **Store** — data lake (raw, cheap, schema-on-read) vs warehouse (modeled,
   schema-on-write) vs lakehouse.
3. **Transform** — clean, join, aggregate (ELT with SQL, or Spark/Flink).
4. **Serve** — BI, dashboards, feature store, model training, APIs.

## Batch vs stream
- **Batch:** high throughput, latency tolerated, easy reprocessing, cheaper.
  Example: daily billing, nightly aggregates.
- **Stream:** low latency, continuous, harder exactly-once, event-time/windowing
  complexity. Example: fraud detection, live metrics.
- Unified pipelines (Lambda/Kappa) trade complexity for freshness.

## Data modeling
- OLTP (transactions) vs OLAP (analytics) vs lake vs TSDB vs search.
- Schema-on-write vs schema-on-read; schema evolution (Avro/Protobuf).
- Partitioning, compaction, and file formats (Parquet/ORC) for scan efficiency.
- Key data terms: cardinality, grain, dimension vs fact, idempotent loads.

## AI / LLM systems
- **AI agent:** LLM + tools + memory + planning loop; autonomy vs control.
- LLM serving: tokenization, batching, KV-cache, GPU memory, latency vs
  throughput, streaming responses, RAG for grounding.
- **Open-source AI stack:** model runtimes (Ollama/vLLM), orchestration,
  vector DBs, embeddings, evaluation.
- Cost drivers: GPU time, tokens, retries, vector store, egress.

## Checklist
- [ ] Batch/stream chosen per source with rationale.
- [ ] Storage layer chosen (lake/warehouse/lakehouse).
- [ ] Schema + evolution + contracts defined.
- [ ] Idempotent, replayable transformations.
- [ ] Data quality checks + lineage + freshness SLAs.
- [ ] PII classification and access control.
- [ ] For AI: eval, grounding (RAG), cost/latency budget, fallbacks.
- [ ] Observability on pipeline lag/failures.

## Common pitfalls
- Stream processing when batch would do (unneeded complexity).
- Non-idempotent transforms → duplicate/incorrect data.
- Schema drift breaking downstream silently.
- Lake without governance → data swamp.
- LLM features without evaluation or grounding → hallucinations.
- Ignoring token/GPU cost at scale.

## References
- `...\data-pipelines-overview.md`, `...\key-data-terms.md`
- `...\what-is-an-ai-agent.md`, `...\how-does-chatgpt-work.md`, `...\the-open-source-ai-stack.md`, `...\chatgpt-timeline.md`, `...\deepseek-1-pager.md`
- `...\5-functions-to-merge-data-with-pandas.md`
- `...\big-data-pipeline-cheatsheet-for-aws-azure-and-google-cloud.md`
- `...\change-data-capture-key-to-leverage-real-time-data.md`
- `...\choose-the-right-database-for-metric-collecting-system.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`database-design`, `messaging-and-streaming`, `cloud-and-infrastructure`,
`scalability-and-performance`.
