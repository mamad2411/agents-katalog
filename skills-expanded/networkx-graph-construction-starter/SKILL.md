# NetworkX Graph Construction Starter

Use this skill to build a deterministic toy biological interaction graph and summarize basic network properties with NetworkX.

## What it does

- Loads a small TSV edge list representing a pathway-like interaction graph.
- Builds a NetworkX graph with edge attributes.
- Summarizes node and edge counts, connected components, degree centrality, and a shortest path example.
- Writes compact JSON that can feed downstream reporting or agent-planning steps.

## When to use it

- You need a local starter for graph-construction workflows in systems biology.
- You want a deterministic network summary before moving on to propagation, enrichment, or causal-network tasks.

## Example

```bash
python3 skills/systems-biology/networkx-graph-construction-starter/scripts/run_networkx_graph_construction.py \
  --input skills/systems-biology/networkx-graph-construction-starter/examples/toy_pathway_edges.tsv \
  --source-node EGFR \
  --target-node STAT3 \
  --out scratch/networkx/graph_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/systems-biology/networkx-graph-construction-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase25_agent_clinical_proteomics_graph_skills -v`
