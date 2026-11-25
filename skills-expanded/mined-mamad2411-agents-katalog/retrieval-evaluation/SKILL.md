---
name: retrieval-evaluation
description: "Evaluate a retriever or search ranking change against a reproducible, access-safe benchmark rather than a few impressive answers. Use for hybrid versus vector search comparisons, chunking or reranker changes, recall regressions, relevance-label design, search result quality, or a proposal to promote a new retrieval index. Freeze queries, corpus snapshot, ACL context and relevance judgements; compare baseline and candidate on paired inputs with explicit units, denominators and unjudged policies; keep answer grounding and abstention separate from retrieval scores. Treat any cross-tenant or unauthorized result as an independent veto. Keep a sealed holdout out of tuning and stop when the evidence cannot distinguish improvement from noise. Not for grading an entire agent's tool use or conversation: that is agent-evaluation."
allowed-tools: "Read, Grep, Glob"
---

# Retrieval Evaluation

Prove which documents are found for which authorised searchers before interpreting answer quality. An improved average rank cannot excuse one access leak.

## Workflow

1. Write the decision and minimum meaningful gain before tuning. Freeze a versioned query set, corpus/index snapshot, document and chunk identities, access-control principal/tenant context and relevance labels with provenance. Partition development and sealed holdout by query family or source to prevent near-duplicate contamination; do not inspect holdout results during tuning.
2. Define the relevance unit (document or chunk), how multiple chunks of one document count, cutoff `k`, grading scheme and query-level aggregation. Record which queries have zero relevant documents and score them separately for inappropriate returns/abstention rather than silently dropping them from denominators. Record unjudged results explicitly: judge them blind to system identity or use a predeclared exclusion policy applied equally to both systems; never treat unknown as relevant.
3. Run baseline and candidate on identical queries, corpus, ACLs and time-bound configuration. Keep per-query paired ranks and retrieval latency. Report eligible query denominator, judged coverage, recall@k and ranking metric (for example MRR or nDCG with declared grading), plus slices for rare terms, fresh content, tenants and zero-relevant queries. Show paired regressions alongside aggregate gains.
4. Test unauthorized documents and snippets separately for every principal, including absent/stale ACL data and cross-tenant cases. Any exposure vetoes promotion regardless of relevance. Check both retrieval and downstream display paths; verify platform-specific filtering and caching semantics before trusting a claimed guard.
5. If an answer generator is involved, score cited support, answer correctness and abstention on a separate sheet with the same frozen evidence; do not relabel an answer improvement as recall. Run the sealed holdout once after tuning ends, record version hashes and compare to prewritten gates. If labels, coverage or sample size cannot support a decision, return insufficient evidence, not a win.

## Output

Produce a benchmark card: frozen inputs and hashes, identity/ACL policy, label rubric, metric formulas and denominators, paired per-query deltas and slices, leak veto, separate answer sheet if applicable, holdout access log and promote/hold decision.

## Anti-patterns

**Tuning on the test queries.** A repeatedly inspected holdout becomes development data; seal a fresh one rather than calling the next run independent.
