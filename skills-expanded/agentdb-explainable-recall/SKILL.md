---
name: agentdb-explainable-recall
description: Search with feature attributions — return WHY each match scored where it did. Use when debugging recall quality, auditing for bias, or explaining results to a user.
---

# Explainable Recall

Standard search returns scores; explainable recall returns *features* — which dimensions of the embedding (or which keywords in hybrid search) drove the match.

## When to use

- Recall quality is off and you need to debug *why*
- Auditing for bias / fairness
- User asks "why this result?" — show the receipts
- Building UIs that surface match rationale

## API

```
agentdb_explainable_recall(
  query:        <embedding | string>
  k:            5
  features:     'embedding-dims' | 'bm25-tokens' | 'hybrid-both' | 'metadata'
)

Returns: [
  {
    id, score,
    explanation: {
      topDims?:       [{ dim: 12, contribution: 0.18 }, ...],
      topTokens?:     [{ token: "jwt", contribution: 0.31 }, ...],
      metadataMatch?: { topic: 'auth', project: 'api' }
    }
  },
  ...
]
```

## Use cases

| Use | Features setting |
|---|---|
| Debug an unexpected high-score | `embedding-dims` — see which dims spiked |
| Verify keyword fall-back works | `bm25-tokens` — see if exact terms were the driver |
| Confirm metadata filters fired | `metadata` — see which filter values matched |
| Build user-facing UI | `hybrid-both` — show both text-level + dim-level signals |

## Don't

- Don't pipe the full feature vector to the user — it's noisy. Pick top 3-5 contributing dims/tokens.
- Don't use explainable recall for normal searches. The feature extraction adds 20-50ms per query.
