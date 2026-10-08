---
name: pairwise_de
description: Reference template — pairwise differential expression between two named groups.
---

## When to use

The curated `run_de` tool does per-cluster one-vs-rest DE; this template covers an arbitrary
A-vs-B comparison (e.g. disease vs control) via scanpy `rank_genes_groups` with an explicit
`reference`. ADAPT GROUP_KEY / GROUP_A / GROUP_B to a column that exists in adata.obs.

## Run
Fetch the template with `read_skill_reference("pairwise_de", file="reference.py")`, adapt the CONFIG / marker / threshold values to THIS dataset, then execute it via `run_code` (reads checkpoints from `BIOAGENT_WORK`, writes under `BIOAGENT_ARTIFACTS`). If a purpose-built tool already covers the step, use the tool instead.
