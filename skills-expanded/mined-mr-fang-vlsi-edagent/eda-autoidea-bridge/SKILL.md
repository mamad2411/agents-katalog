---
name: eda-autoidea-bridge
description: Bridge autoIdea literature recommendation, historical formulation, and idea-generation outputs into the current repo's paper/knowledge/skill workflow.
---

# EDA AutoIdea Bridge

## When to use
Use this skill when the user wants to combine `external_tools/autoIdea` outputs with current infra:
1. import recommended papers into local download queue,
2. merge autoIdea recommendations with landscape feedback queue,
3. ingest autoIdea idea/experiment drafts into a governed report for follow-up debate and hypothesis design.

## Inputs
- `external_tools/autoIdea` clone with at least one of:
  - `citation_graph_output/recommended_top30.json`
  - `outputs/final_idea.txt`
  - `outputs/experiment.txt`
  - `citation_graph_output/historical_problem_formulation.txt`

## Execution
Run:

```bash
python3 scripts/common/autoidea_bridge.py --autoidea-root external_tools/autoIdea
```

## Outputs
- `docs/papers/queues/autoidea_recommended_top30_bridge.tsv`
- `docs/papers/queues/literature_feedback_merged_with_autoidea.tsv`
- `docs/knowledge_base/99_AUTOIDEA_FUSION_REPORT_20260306.md`

## Integration contract
1. New autoIdea-driven queue rows must still pass current paper/validation gates.
2. Imported idea/experiment drafts are treated as candidates, not accepted plans.
3. Promotion requires `control-theory-veto` and non-regression execution evidence.
