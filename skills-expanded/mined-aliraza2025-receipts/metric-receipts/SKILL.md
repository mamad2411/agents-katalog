---
name: metric-receipts
description: Pairs every product metric with the decision it informs and states what the number does not prove. Use when defining success metrics, writing dashboards or metric sections in PRDs, reporting results, preparing a metrics slide, or when the user asks "what should we measure" or "is this metric good".
---

# Metric receipts

A metric earns its place when it changes a decision. This skill makes each metric carry three things: what it measures, which decision it informs, and what it cannot tell you.

## Workflow

1. **Start from decisions, not data.** List the decisions the team will make in the next cycle (ship, roll back, fix ingestion, change pricing, hire). If a metric maps to no decision, mark it `VANITY` and move it to an appendix.
2. **Separate the layers.** Most AI and workflow products need at least three different questions answered, and one number rarely answers more than one:
   - Did it run? (completion, latency, error rate)
   - Did it have what it needed? (coverage, evidence, data quality)
   - Was it right or useful? (accuracy against an independent judgment, task success, retention)
3. **Write a receipt card** for each metric (template below).
4. **Check for proxy inflation.** Flag any place where a layer 1 or 2 number is used to claim a layer 3 result.
5. **Set thresholds before looking.** If the user has results already, label any threshold chosen after seeing them as `POST-HOC`.

## Receipt card template

```markdown
### [Metric name]
- **Definition:** numerator / denominator, unit, time window, who is counted once
- **Layer:** ran | had what it needed | right or useful
- **Decision it informs:** [specific decision and owner]
- **Threshold:** [value], chosen [before | after] seeing data
- **Does not prove:** [the tempting conclusion this number cannot support]
- **Source of truth:** [table, event, log, or report]
```

## Example

From an AI video-credibility product, March 2026:

```markdown
### Job completion rate
- Definition: completed jobs / submitted links, one batch of 780 YouTube links
- Layer: ran
- Decision it informs: whether the queue and workers are reliable enough to scale the batch size
- Threshold: none set for this batch
- Result: 780 of 780 completed (2 after retry)
- Does not prove: that results were accurate or useful. In the same batch, 759 of 780 were flagged low evidence.

### Average evidence tokens per video
- Definition: mean extracted evidence tokens per video, 19-link Instagram benchmark
- Layer: had what it needed
- Decision it informs: whether the ingestion redesign was worth keeping
- Result: 1.0 before, 130.9 after the redesign
- Does not prove: that credibility judgments became more accurate. That needs labeled evaluation.
```

## Rules

- Never upgrade a metric's layer in prose. "More evidence recovered" must not become "more accurate".
- Every percentage gets its denominator and date in the same sentence.
- If no metric reaches layer 3, say so plainly in the summary.
