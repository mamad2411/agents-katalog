# LangChain Basics

## Summary

**One-sentence:** Composes LCEL pipelines (prompt | model | parser) with `with_structured_output()` for reliable parsing, pinned package versions, LangSmith tracing, and built-in retry/fallback chains, providing the building blocks every LangChain-based agent depends on.

**One-paragraph:** Core LangChain concepts, installation, chain patterns, prompt engineering, output parsing, and streaming for sequential AI pipelines. LCEL (the pipe operator `|`) declaratively composes components. `with_structured_output()` is the reliable parser; `JsonOutputParser` is unreliable with smaller models. Pin every package version; turn on LangSmith in development; use `chain.with_retry()` for transient errors; use `with_fallbacks()` for resilience.

**Ефективно для:** простих послідовних LLM-пайплайнів, prompt engineering, structured extraction — там, де LangGraph надмірний, а пряма Anthropic-SDK не дає observability "з коробки".

## Applies If (ALL must hold)

- Building sequential LLM pipelines (output of one step feeds the next).
- Need `with_structured_output()` for reliable Pydantic-validated parsing.
- Task is prompt engineering + chain composition, not stateful agent loops.
- Streaming output to UI matters OR LangSmith observability is required.

## Skip If (ANY kills it)

- Need stateful multi-step agents with branching — use LangGraph.
- Pure RAG with indexing as primary concern — LlamaIndex handles it better.
- No LLM calls — plain Python is simpler.
- Latency critical and abstraction overhead matters — call Anthropic SDK directly.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| API keys | env vars | Provider config |
| LangSmith key (optional but recommended) | env var | LangSmith account |
| Pinned package versions | `requirements.txt` | Application config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `field-descriptions-as-prompts` | `with_structured_output()` schemas need precise descriptions. |
| `gateway-fallback-chain` | `with_fallbacks()` is the LangChain-native version of the gateway pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Six rules: prefer structured_output, pin versions, LangSmith in dev, retry on external calls, stream for UX, module-level chains | ~1100 |
| `content/02-output-contract.xml` | essential | Structured extraction schema example + chain config envelope | ~900 |
| `content/03-failure-modes.xml` | essential | JsonOutputParser unreliability, version drift, sync RunnableParallel, MemoryCache | ~800 |
| `content/06-decision-tree.xml` | essential | LangChain (LCEL) vs LangGraph vs raw SDK | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Wire a sequential chain | haiku | Mechanical composition |
| Design structured extraction schema | sonnet | Field design + descriptions |
| Pick LangChain vs LangGraph for new feature | opus | Architectural tradeoff |

## Templates

| File | Purpose |
|------|---------|
| `templates/structured-extraction.py` | Inline chain using `with_structured_output()` for extraction |
| `templates/_smoke-test.json` | Minimum valid extraction output for self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-langchain-basics.py` | Validates an extraction output against the schema | Pre-commit on chain changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[langchain-chains]]
- [[langchain-agents-architectures]]
- [[field-descriptions-as-prompts]]

## Decision tree

See `content/06-decision-tree.xml`. Root question is whether the workflow needs stateful branching. Branches route to LangGraph (stateful), LangChain LCEL (sequential), or raw vendor SDK (latency-critical).
