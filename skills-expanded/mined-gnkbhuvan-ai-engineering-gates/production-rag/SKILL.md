---
name: production-rag
description: |
  Retrieval-Augmented Generation (RAG) architecture — designing, scaling, or hardening a
  RAG pipeline for production. Branches: architect a new RAG pipeline, choose a vector
  database, decide a chunking strategy, evaluate retrieval/generation quality, decide RAG
  vs. fine-tuning vs. long-context, pick an advanced pattern (agentic/graph/multimodal
  RAG), or debug a RAG system that's hallucinating or retrieving the wrong thing. This is
  an architecture/design skill — use `fastapi-genai` to implement it.
---

# Production RAG

Architecture methodology for RAG systems: from "do you even need RAG" through pipeline
design, vector database selection, build-vs-buy decisions, evaluation, and production
hardening. Audience includes non-engineers (PMs, architects) as well as AI engineers—stay
at the principles/decision level here; code belongs in `fastapi-genai`.

## First-Principles Foundation

1. **RAG is a fix for three specific problems, not a default**: the knowledge doesn't fit
   in context, it changes too often to bake into a prompt, or different users need different
   access to it. If none of those apply—e.g. a stable knowledge base under roughly 200K
   tokens (~500 pages)—just put it directly in the prompt and skip the entire retrieval
   pipeline's failure surface.
2. **RAG vs. fine-tuning**: RAG keeps facts swappable and filterable per query (permission
   metadata at retrieval time separates what the CEO sees from what's globally visible).
   Fine-tuning bakes facts into one undifferentiated weight blob with no per-user access
   control. Use RAG for facts/freshness; fine-tune for behavior, format, or style (see
   `prompt-engineering`'s fine-tuning decision tree for that side of the choice).
3. **Garbage in, garbage out**: retrieval quality is a hard ceiling on generation quality.
   No amount of prompt engineering fixes a retriever that returns the wrong chunks.
4. **Every retrieved chunk is assumed relevant by the model** (the same "Chekhov's gun"
   effect any included context has on a model — see the `prompt-engineering` skill): a bad
   retriever is worse than no retriever. Filter and rerank before insertion.
5. **Cost scales with chunks and queries, not just documents**: vector DB spend commonly
   runs 1/5 to 1/2 of total model API cost once a system is in production. Budget for
   storage + embedding + query cost explicitly, not just generation tokens.

## Trigger Decision Tree

1. **Is RAG even the right tool?** Check axiom 1 above. If the knowledge base is small and
   stable, recommend skipping RAG entirely before designing anything.
2. **Is this RAG vs. fine-tuning vs. long-context confusion?** Clarify which problem is
   actually being solved (freshness/access-control → RAG; behavior/style → fine-tuning;
   small static corpus → just stuff it in context).
3. **Confirm missing details with the user/PM**—gate below; do not architect past this point until it passes.
4. **Design the pipeline stage by stage** → `references/pipeline-stages.md`.
5. **Pick storage** → `references/vector-db-selection.md`.
6. **Decide build vs. buy** (framework vs. native SDK, turnkey vs. DIY) →
   `references/build-vs-buy.md`.
7. **Plan evaluation before launch, not after** → `references/evaluation.md`.
8. **Only reach for agentic/multimodal/graph RAG if plain RAG demonstrably fails on a
   specific query class** → `references/advanced-patterns.md`.
9. **Harden for production** (cost, security, latency, monitoring) →
   `references/production-hardening.md`.

### When Information Is Missing—Ask Before Architecting

| Missing? | Ask |
|---|---|
| Data freshness | "How often does this knowledge change—daily, never, or somewhere between?" |
| Data volume & format | "Roughly how much content, and what format—PDFs, web pages, a database, tickets?" |
| Access control | "Do different users need to see different subsets of this data?" |
| Existing infrastructure | "What database do you already run—Postgres, MongoDB, something else? (Reuse it before adding a new one.)" |
| Latency/cost budget | "What response time is acceptable, and is there a cost ceiling per query?" |
| Compliance | "Any regulatory requirements—HIPAA, SOC 2, GDPR—that affect where data can live or who can access it?" |
| Success criteria | "How will you know the answers are good enough to ship?" |

**Gate**: this step is done only when every row above that's actually unclear from context has either been answered by the user/PM or stated out loud as an explicit assumption with no objection. Silently assuming and continuing does not satisfy this — stop and ask instead.

## Build vs. Buy — Quick Reference

| Question | Default | Escalate only if |
|---|---|---|
| Framework or native SDK? | Provider SDK (OpenAI Responses/File Search, Claude Agent SDK + your own retrieval) | You need multi-provider portability, complex chain composition, or a large document-loader ecosystem |
| New vector DB or reuse existing? | Reuse the database you already operate (pgvector/Atlas/Supabase) | You exceed its scale ceiling or need a capability it lacks (e.g., sub-5ms p50 latency at huge scale) |
| DIY components or turnkey platform? | DIY for your differentiating logic | Non-differentiating plumbing (extraction, parsing, compliance) where "one throat to choke" beats vendor coordination overhead |

→ Full criteria and current vendor landscape: `references/build-vs-buy.md` and
`references/vector-db-selection.md`

## Evaluation — Quick Reference

Three-part evaluation, not one number:
1. **Retrieval quality**: context precision/recall, NDCG/MAP/MRR if rank order matters.
2. **Generation quality**: faithfulness/hallucination rate, answer relevance.
3. **End-to-end production KPIs**: latency (mean + p95), uptime, cost per query.

Build the eval harness *before* launch—"you can't fix what you can't measure," and query
volume quietly dropping after launch is itself a quality signal (users reverting to their
old workaround).

→ Metrics, tools, and harness design: `references/evaluation.md`

## Deliverables

When delivering a RAG architecture, provide:

1. **Pipeline diagram** (stages + chosen technique per stage, with the reasoning for each)
2. **Storage decision** (which database, and why—reuse vs. new)
3. **Build-vs-buy decision** (framework vs. native SDK, DIY vs. turnkey, and why)
4. **Evaluation plan** (metrics, targets, tooling) before go-live
5. **Known failure modes and mitigations** specific to this design
6. **Cost estimate** (storage + embedding + query + generation, not just generation)

## References

| File | Topic | Load When |
|------|-------|-----------|
| `references/pipeline-stages.md` | Parsing, chunking, embedding, retrieval algorithms, reranking, contextual retrieval | Designing or debugging any pipeline stage |
| `references/vector-db-selection.md` | Vector database comparison and selection framework | Choosing or migrating storage |
| `references/build-vs-buy.md` | Framework vs. native SDK, turnkey vs. DIY | Deciding what to build vs. adopt |
| `references/evaluation.md` | Retrieval/generation metrics, eval harness, tooling | Planning or debugging evaluation |
| `references/advanced-patterns.md` | Agentic RAG, multimodal RAG, RAG with tabular data, graph RAG | Plain RAG fails on a specific query class |
| `references/production-hardening.md` | TCO, security/compliance, latency, monitoring, failure modes | Preparing for or operating in production |
