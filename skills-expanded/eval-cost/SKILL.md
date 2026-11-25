---
name: eval-cost
description: Use when the user asks to make an AI app cheaper or faster, reduce tokens, latency, model/tool/retrieval/rerank/self-check/retry/evaluator cost, or compare cost before/after.
---

# Eval Cost

Use this skill for tokenomics RCA. Cost changes are accepted only when Galileo
quality metrics do not regress.

## Conditional References

- Load `skills/eval-engineer/references/tokenomics-rca.md` when choosing the
  tokenomics workflow or diagnosing why cost moved.
- Run `skills/eval-engineer/scripts/compare_tokenomics_packets.py` when both
  baseline and verification packets exist.
- Load `skills/eval-engineer/assets/cost-diagnosis-template.md`,
  `skills/eval-engineer/assets/tokenomics-fix-plan-template.md`, and
  `skills/eval-engineer/assets/quality-preserving-verification-template.md`
  only when writing those artifacts.

## Do

- Compare cost, latency, tokens, retrieved context, tool calls, retries,
  rerank/self-check spans, model spans, and evaluator cost.
- Run `compare_tokenomics_packets.py` without explicit quality metrics first
  when packets use custom quality names, then inspect the inferred
  `Quality metrics compared` list before accepting the decision.
- Treat behavior counters such as handoff count, tool count, step count,
  retry count, and self-check count as efficiency or workflow evidence, not
  quality gates by default. Promote one to quality only when the metric profile
  states the desired direction for that route or segment.
- Protect named quality metrics and segment gates.
- Reject cheaper candidates when aggregate quality holds but any required
  segment gate regresses.
- Treat lower traffic volume as inconclusive unless per-trace efficiency also
  improves.

## Gotchas

- Cost, latency, wall time, duration, token count, span count, and tool count
  are efficiency evidence, not quality gates by default.
- Quality metrics are not always higher-is-better. Error, toxicity,
  hallucination, policy-violation, and tool-error rates regress when they rise.
- Aggregate quality can hide route, risk-profile, or customer-segment
  regressions.
- For RAG pruning, include hard multi-source or multi-hop cases before keeping
  a top-k reduction.
- For agentic workflows, compare agent steps, planner spans, rerank passes,
  self-check spans, and tool calls so the cheaper loop is explainable.

## Validation Loop

Before keeping a candidate:

1. Compare baseline and verification packets with
   `compare_tokenomics_packets.py`.
2. Inspect inferred quality metrics before accepting the decision.
3. Check segment metrics when available.
4. Confirm metric gaps are recorded as inconclusive or follow-up work.
5. Reject or revise the candidate if quality evidence is missing or regressed.

## Output

State keep/reject/inconclusive first. Explain why the cost moved, which quality
metrics do not regress, and which latency/tool-count tradeoffs remain.
