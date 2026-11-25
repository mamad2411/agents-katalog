---
name: domain-recommender
description: "Use for recommendation and ranking systems: product or content recommendation, collaborative filtering, candidate retrieval, learning to rank, next-item or sequential recommendation, and cold start. Picks retrieve-then-rank architecture, the right model, honest temporal splits, and ranking metrics. Triggers on 'recommendation', 'recommender', 'collaborative filtering', 'ranking', 'personalization', 'next item', 'user-item', 'what to show users'."
---

# Recommendation - Method Selection

For large catalogs use two stages: retrieve candidates, then rank them. Always keep a simple, strong baseline.

## Decision table
| Sub-task | Recommended | Notes |
|---|---|---|
| Strong baseline | matrix factorization (ALS, BPR) or item k-NN | cheap and hard to beat. Always include it. |
| Candidate retrieval (large catalog) | two-tower model (user tower and item tower) + approximate nearest neighbor index | scalable first stage. |
| Ranking | gradient-boosted trees on features, or DeepFM or DLRM | optimizes the top of the list. |
| Sequential or next-item | SASRec (causal) or BERT4Rec (bidirectional, cloze objective) | captures order. The bidirectional cloze can leak the target if not masked correctly. |
| Cold start | content-based features inside a two-tower model | for new users or items with no history. |

## Cross-cutting practice
- Leakage (critical): split by TIME (train on the past, evaluate on the future) or leave-one-last-interaction-out per user. Never use a random interaction split. Never let the model see the target interaction.
- Handle implicit feedback with BPR or sampled softmax; address popularity bias and the cold-start case.
- Metrics: Recall@K, NDCG@K, MAP, MRR, HitRate@K. Do not use plain accuracy or ROC-AUC as the headline. Always compare against a popularity baseline.
- Explainability: nearest items, "because you interacted with X", and SHAP on the ranker features.
- Recent direction (2024-2025): LLM-based generative recommenders and generative retrieval. SASRec and BERT4Rec remain strong, still-standard baselines; reported gains over them are frequently overstated, so always compare fairly.
- Improve accuracy: use `accuracy-improvement-loop` (hard-negative mining, a sequential model, or a stronger two-stage pipeline).
