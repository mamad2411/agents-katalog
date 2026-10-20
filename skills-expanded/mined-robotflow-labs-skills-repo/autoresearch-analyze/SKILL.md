---
name: autoresearch-analyze
description: Analyze autoresearch experiment results. Reads results.tsv, git log, and current train.py to summarize findings, identify patterns, suggest next experiments. Use when the user asks "analyze results", "what worked", "summarize experiments", or "what should we try next".
---

# Autoresearch Results Analyzer

Analyze the experiment history and provide actionable insights.

## Steps

1. **Read results.tsv** — parse all experiments, their val_bpb, memory, status
2. **Read git log** on the autoresearch branch — understand the sequence of changes
3. **Read current train.py** — understand the current best configuration
4. **Compute statistics**:
   - Best val_bpb achieved and which experiment
   - Total improvement from baseline (absolute and percentage)
   - Number of experiments: total, kept, discarded, crashed
   - Memory trend across experiments
   - Throughput (tok/sec) if available in logs
5. **Identify patterns**:
   - Which types of changes consistently help? (architecture, optimizer, schedule, etc.)
   - Which changes consistently hurt or crashed?
   - Diminishing returns — are recent improvements smaller?
   - Unexplored dimensions — what hasn't been tried yet?
6. **Recommend next experiments** ranked by expected impact
7. **Compare to known benchmarks**:
   - Upstream H100 reference: val_bpb ~0.998
   - Our current gap and realistic targets

## Output Format

```
## Experiment Summary
- Total experiments: N (K kept, D discarded, C crashed)
- Baseline val_bpb: X.XXX
- Current best val_bpb: X.XXX (Y% improvement)
- Peak memory range: A-B GB

## What Worked
- [ranked list of successful strategies]

## What Didn't Work
- [ranked list of unsuccessful attempts]

## Recommended Next Experiments
1. [highest expected impact]
2. ...

## Gap Analysis
- Current: X.XXX | H100 reference: 0.998 | Gap: Y.YYY
- Realistic target given Apple Silicon constraints: ~X.XX
```
