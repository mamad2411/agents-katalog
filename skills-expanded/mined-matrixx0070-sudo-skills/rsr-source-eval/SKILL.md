---
name: rsr-source-eval
version: 1.0.0
description: Judge one source's credibility, bias, and recency before you rely on it.
author: matrixx0070
tags: [research, credibility, bias, source-evaluation, provenance]
capabilities: []
---

# Source Eval

## When to use
Reach for this when you're about to lean on a single source and need to know how much weight it can bear — a study, an article, a report, a dataset, a post. It produces a trust rating you can attach to any claim you draw from it.

**Not for:** verifying whether a specific claim is true (use rsr-fact-check); comparing many sources across a topic (use rsr-literature-map); merging sources into an answer (use rsr-synthesis). This grades one source, not a claim or a field.

## Method
1. **Identify the source type.** Primary (original data, first-hand), secondary (reporting on primary), or tertiary (summarizing secondary)? *Decision:* prefer primary; if this is tertiary, note you'll want its upstream source before relying on it.
2. **Check provenance.** Who is the author/publisher, what are their credentials, and who funded or benefits from the work?
3. **Scan for bias.** Note stated stance, commercial or political interest, and loaded framing. Bias doesn't disqualify — it tells you which claims to cross-check.
4. **Assess evidence.** Does it cite data and link to primaries, or assert? Is method disclosed? *Decision:* if key claims are uncited, downgrade to "corroborate before use."
5. **Check recency.** Publication date vs. how fast this field moves. A 2019 pricing figure is stale; a 2019 historical account may be fine.
6. **Rate.** Assign High / Medium / Low trust with a one-line reason, and state what it's trustworthy *for*.

## Example
Source: a vendor whitepaper claiming "our tool cuts costs 40%." Type: secondary, self-published. Provenance: authored and funded by the seller — direct commercial interest. Evidence: the 40% comes from one unnamed customer, no method. Recency: current. Verdict: **Low** trust for the cost claim (self-interested, single uncited case); usable only as a statement of what the vendor markets, not as evidence of real savings.

## Pitfalls
- Equating polish or domain authority with accuracy — a clean PDF can still be a marketing asset.
- Treating any bias as fatal; every source has a viewpoint, the question is whether it distorts the specific claim.
- Ignoring the date because the content "feels evergreen."
- Rating trust globally instead of per-use — a source can be strong for context and weak for statistics.

## Output format
```
Source: <title / publisher> — <date>
Type: <primary | secondary | tertiary>
Provenance: <author, funding, interest>
Bias: <stance / interest, or "none evident">
Evidence: <cited & method-disclosed | asserted>
Recency: <current | dated for this topic>

Trust: <High | Medium | Low> — <one-line reason>
Trustworthy for: <what claims this can support>
Corroborate before using for: <what it can't support alone>
```
