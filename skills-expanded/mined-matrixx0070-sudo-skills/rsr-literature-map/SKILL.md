---
name: rsr-literature-map
version: 1.0.0
description: Map the landscape of work and opinions on a topic into labeled clusters with representative sources.
author: matrixx0070
tags: [research, landscape, clustering, literature-review, positions]
capabilities: []
---

# Literature Map

## When to use
Reach for this when you need the shape of a field before you have an answer — "who's working on X and how do they group", "what are the main camps on Y", "what's the range of approaches to Z". Output is a clustered map of positions/approaches, each with representative sources and points of disagreement.

**Not for:** answering a specific question (use rsr-deep-dive); merging sources into one cited answer (use rsr-synthesis); grading one source (use rsr-source-eval). A map orients you; it does not resolve.

## Method
1. **Define the axis.** Decide what you're clustering by: methodology, conclusion/position, discipline, or time period. *Decision:* if the topic is contested, cluster by position; if it's technical, cluster by approach.
2. **Gather broadly.** Pull a wide, diverse set of sources — deliberately seek dissent and outliers, not just the top results, which tend to echo one view.
3. **Cluster.** Group sources along your axis into 3-6 named clusters. Name each by its defining stance or method, not by author.
4. **Characterize each cluster.** One line on what it claims, its strongest evidence, and 1-2 representative sources with dates.
5. **Map the tensions.** *Decision:* where two clusters directly disagree, note the crux — the specific point they split on — not just "they differ."
6. **Note the frontier.** Flag what's emerging, what's fading, and where the field is silent.

## Example
Topic: "approaches to reducing LLM hallucination." Clusters: (1) *Retrieval grounding* — inject sources at inference (RAG papers, 2023-24); (2) *Training-time* — RLHF/fine-tuning on factuality (2022-23); (3) *Decoding-time* — self-consistency, verification passes (2023-25); (4) *Abstention* — teach refusal under uncertainty. Tension: retrieval camp vs. training camp split on whether the fix belongs at inference or in weights. Frontier: decoding-time verification is rising; pure prompt-tricks are fading.

## Pitfalls
- Sampling only the top results, so every cluster echoes the dominant view and dissent vanishes.
- Clustering by author or venue instead of by idea, producing a bibliography not a map.
- Forcing everything into two camps when the field actually has a spectrum.
- Stating clusters "differ" without naming the specific crux they disagree on.

## Output format
```
Topic: <one sentence>
Clustered by: <methodology | position | discipline | period>

Clusters:
1. <name> — <what it claims / does>; evidence: <strongest>; reps: <src, date; src, date>
2. ...

Key tensions:
- <cluster A> vs <cluster B>: crux is <specific point>

Frontier: rising <..> | fading <..> | silent on <..>
```
