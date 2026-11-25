# NetworkX Network Propagation Starter

Use this skill to propagate signal from one or more seed nodes over a small weighted interaction graph with personalized PageRank.

## What it does

- Loads a deterministic weighted edge list and a small seed-node set.
- Runs NetworkX personalized PageRank as a lightweight propagation surrogate.
- Emits ranked node scores, top non-seed hits, and basic graph statistics in JSON.

## When to use it

- You need a verified local starter for `network propagation`.
- You want a deterministic way to score neighbors around seed genes before using larger pathway or interaction resources.

## Example

```bash
python3 skills/systems-biology/networkx-network-propagation-starter/scripts/run_networkx_network_propagation.py \
  --input skills/systems-biology/networkx-network-propagation-starter/examples/toy_network.tsv \
  --seeds skills/systems-biology/networkx-network-propagation-starter/examples/toy_seeds.txt \
  --top-k 5 \
  --out scratch/networkx-propagation/summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/systems-biology/networkx-network-propagation-starter/tests -p 'test_*.py'`
- Repository smoke target: `make smoke-network-propagation`
