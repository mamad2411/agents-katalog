# APIs And RPCs

Use this skill when a TON product must read state, verify a transaction path, or choose between infrastructure access models.

## Inputs

- the product question the data source must answer
- required confidence and latency
- runtime environment and operational constraints
- fallback plan if the primary data path becomes ambiguous

## Process

1. define the exact state question the product is asking
2. classify whether the consumer is UI, backend fulfillment, debugging, or audit
3. choose the simplest access path that can answer the question with the required confidence
4. document what counts as incomplete, delayed, or conflicting data
5. pair the decision with a verification workflow that the team can actually run in production

## Guardrails

- do not select infrastructure by habit alone
- do not expose provider-specific uncertainty as if it were user-facing truth
- do not mix debugging endpoints and production contracts without naming the difference
- do not force a lite-client footprint unless the trust requirement genuinely demands it

## Output

- a chosen access model
- explicit confidence and fallback rules
- a transaction verification path that matches the selected infrastructure
