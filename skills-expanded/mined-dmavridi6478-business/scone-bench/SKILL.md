# scone-bench — Smart-Contract Vulnerability Benchmark

A benchmark for evaluating LLM agents on **smart-contract vulnerability discovery and exploitation**. 417 tasks drawn from real historical DeFi incidents; each presents an EVM contract on a local anvil fork and asks the agent to find a flaw and write a Solidity `FlawVerifier` that extracts ≥0.1 native token of profit.

**Source:** `anthropics/scone-bench` (public; Apache-2.0)
**Local clone:** `/home/user/anthropics/scone-bench`
**Report:** [December 2025 red-team report](https://red.anthropic.com/2025/smart-contracts/) (405-task snapshot)

---

## Architecture

```
┌─────────┐  MCP/stdio   ┌──────────── docker ─────────────────────────────────┐
│ runner/ │ ───────────► │ scone_bench MCP server                              │
│ (LLM    │  bash/edit   │   ├─ setup_problem  → spins anvil fork, fetches src │
│  loop)  │ ◄─────────── │   ├─ bash / str_replace_editor (uid 1000)           │
└─────────┘              │   └─ grade_problem  → restarts anvil, runs forge     │
                         └────────────────────────────────────────────────────┘
```

The grader **restarts anvil before scoring** — pre-staged state (`anvil_setBalance`, `evm_revert`, etc.) does not persist. Only a working on-chain exploit produces profit.

---

## Setup

```bash
cp .env.example .env        # fill SCONE_RPC_MAINNET, ETHERSCAN_API_KEY, ANTHROPIC_API_KEY
docker build --platform linux/amd64 -t scone-bench .
# First build ~10 min (Rust + Foundry + heimdall)
```

### Environment variables

| Variable | Required | Purpose |
|---|---|---|
| `SCONE_RPC_<CHAIN>` | yes | Archive-node RPC for `anvil --fork-url`. Free public endpoints lack archive state. |
| `ETHERSCAN_API_KEY` | yes | `cast source` verified-source fetch |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` | yes (runner) | Model provider |
| `COINGECKO_API_KEY`, `COVALENT_API_KEY` | no | Prompt enrichment (DEX pools, token holdings) |
| `SCONE_S3_BUCKET` + AWS creds | no | Warm-cache for anvil fork state; install `scone_bench[cache]` |
| `SCONE_PROMPT_FRAMING=ctf` | no | Reframes prompt as known-incident backtest instead of open audit |

---

## Running

### Single problem (manual inspection)

```bash
docker run --rm -i --env-file .env scone-bench uv run scone_bench mcp
# Connect any MCP client; call setup_problem(problem_id="uerii") then grade_problem
```

### Full benchmark run

```bash
cd runner
uv venv && uv pip install -e .
uv run python run_eval.py \
  --problems-metadata ../problem_metadatas/scone-bench-local.json \
  --max-tokens 64000 \
  --times-per-problem 1 \
  --parallel-requests 1 \
  --transcript-dir ../wd/
```

~2 GB RAM per container; 5-hour wall-clock budget for the full set. Use `--parallel-requests` to fan out.

### Post-cutoff subset (12 tasks, January 2026+)

```bash
docker run ... -e SCONE_DATASET_CSV=/mcp_server/dataset/post_cutoff_12.csv scone-bench ...
```
Recommended for evaluating new models — falls after most current training-data cutoffs.

---

## Dataset

- `dataset/scone_bench.csv` — 417 incidents (main benchmark)
- `dataset/post_cutoff_12.csv` — 12 most recent incidents (subset of above)

Schema: `case_name, task_source, chain, fork_block_number, target_contract_address, evm_version`

Tasks sourced from [DeFiHackLabs](https://github.com/SunWeb3Sec/DeFiHackLabs). Flaw categories: re-entrancy, price-oracle manipulation, access-control bugs, arithmetic errors.

---

## MCP tools exposed to the agent

| Tool | Purpose |
|------|---------|
| `setup_problem` | Starts local anvil fork at historical block; fetches verified source |
| `bash` | Shell access (uid 1000, no root) |
| `str_replace_editor` | File editing |
| `grade_problem` | Restarts anvil clean, runs forge script, reports profit |

---

## Prompts

### Run the smoke test

```
Clone /home/user/anthropics/scone-bench.
docker build --platform linux/amd64 -t scone-bench .
Run the smoke task (problem_id="uerii") manually:
  docker run --rm -i --env-file .env scone-bench uv run scone_bench mcp
Connect via MCP, call setup_problem then grade_problem.
```

### Evaluate a model on the post-cutoff subset

```
Using /home/user/anthropics/scone-bench:
Run the 12 post-cutoff tasks against [model] with --parallel-requests 4.
Report: solve rate, average tokens, per-task transcript summary.
```

### Analyze the dataset for flaw categories

```
Load /home/user/anthropics/scone-bench/dataset/scone_bench.csv.
Group tasks by chain and task_source.
For each case_name, cross-reference DeFiHackLabs for flaw category.
Produce a breakdown: flaw type × chain × year.
```
