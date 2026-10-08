# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

Always use the `deepgate` conda environment:
```bash
conda activate deepgate
```

DeepGate (the GNN embedding model) is loaded dynamically from `/home/local1/vicky/python-deepgate` via `sys.path`. This dependency is required for embedding extraction but falls back gracefully where dummy embeddings suffice.

## Code Quality

Always ensure the agent edits are compatible with the ruff linter guidelines. run linter by yourself to verify when needed. Keep line length below 100 chars.

## Communication Style

Always reply in terse caveman lingo to save tokens, e.g.
"why lot word when few word do trick". Keep technical facts correct.
Do not apply caveman lingo to code, filenames, commands, academic prose,
generated docs, or quoted text.

## Common Commands

**Lint:**
```bash
ruff check .
ruff format .
```

**Run all tests:**
```bash
python -m pytest tests/
```

**Run a single test file:**
```bash
python -m pytest tests/test_ai_podem.py -v
```

**Data preparation (build shards from raw pickle dataset):**
```bash
python -m src.ml.core.dataset \
    --input /home/local1/cache-cw/reconv_dataset.pkl \
    --out /home/local1/cache-cw/processed_reconv/ \
    --max_len 50
```

**Supervised training:**
```bash
python -m src.ml.train train \
    --dataset /home/local1/cache-cw/reconv_dataset.pkl \
    --processed-dir /home/local1/cache-cw/processed_reconv/ \
    --output checkpoints/run_name \
    --epochs 50 --batch-size 3000 --max-paths 256 \
    --amp --checkpointing --num-workers 4
```

**RL experience collection:**
```bash
python -m scripts.collect_experience \
    --bench_dirs data/bench/ISCAS85 data/bench/iscas89 \
    --model checkpoints/unlinked_candidate/best_model.pth \
    --max_faults 50 --exploration 5
```

**RL fine-tuning:**
```bash
python -m scripts.train_rl \
    --model checkpoints/unlinked_candidate/best_model.pth \
    --output checkpoints/reconv_rl_model.pt \
    --epochs 10 --batch_size 256 --max_paths 200 --amp
```

**Full RL pipeline (collect → train → benchmark):**
```bash
python scripts/run_rl_pipeline.py --all \
    --bench_dirs data/bench/ISCAS85 data/bench/iscas89 \
    --max_faults 100 --exploration 5 --epochs 20
```

**Debug a single fault:**
```bash
python -m scripts.debug_ai_podem_execution \
    data/bench/ISCAS85/c17.bench "10-1" \
    --model checkpoints/reconv_model/best_model.pth
```

## Architecture Overview

### Core Problem
The project solves **back implication in reconvergent fan-out structures** for ATPG (Automatic Test Pattern Generation). Given a target logic value at a reconvergence node, the model predicts consistent logic assignments across all diverging paths that share a common stem.

### Logic Representation
- Five-valued logic: `ZERO=0`, `ONE=1`, `XD=2` (don't care/unknown), `D=3` (good=1,faulty=0), `DB=4` (good=0,faulty=1)
- Defined in `src/util/struct.py` alongside `Gate`, `GateType`, and `Fault` dataclasses
- Circuit inputs are `.bench` format files; parsed by `src/util/io.py:parse_bench_file`

### ATPG Core (`src/atpg/`)
- **`podem.py`**: Base PODEM algorithm. Uses global state (`rl_agent`, `backtrace_function`, etc.) to support pluggable backtrace strategies. Returns `SUCCESS`, `UNTESTABLE`, `TIMEOUT`, or `BACKTRACK_LIMIT`.
- **`logic_sim_three.py`**: 3-valued (and 5-valued) logic simulation; provides `d_frontier`, `fault_is_at_po`, `reset_gates`.
- **`scoap.py`**: Calculates SCOAP controllability/observability measures used in PODEM heuristics.
- **`reconv_podem.py`**: Identifies reconvergent path pairs via BFS/beam-search (`pick_reconv_pair`). `PathConsistencySolver` checks whether a target value is logically achievable using Maamari LRR (Local Reconvergent Region) analysis and exit-line tracking.
- **`recursive_reconv_solver.py`**: `HierarchicalReconvSolver` drives the AI justification loop. Solves pairs from shortest to longest. `ReconvPairPredictor` is the abstract interface for pluggable prediction backends.
- **`ai_podem.py`**: `AIBacktracer` wraps `HierarchicalReconvSolver` as a drop-in replacement for PODEM's `simple_backtrace`. Falls back to `simple_backtrace` when no reconvergent structure exists.
- **`reconv_cache.py`**: Disk-persisted pickle cache for reconvergent pair topology (stored in `.reconv_cache/` alongside each `.bench` file). Pairs are topology-only and never change between runs.

### ML Model (`src/ml/core/model.py`)
`MultiPathTransformer` processes a batch of reconvergent path sets:
- Input shape: `[B, P, L, D]` — batch, paths, sequence length, feature dim
- Augments input with a learnable gate-type embedding (12 types → 64 dims), then projects to `model_dim`
- **Shared Path Encoder**: Transformer encoder processes each path independently (local sequential logic features)
- **Path Interaction Layer**: Transformer over path-summary tokens (terminal node of each path) — lets paths "communicate"
- **Cross-Attention**: Each node attends to all interaction-aware path summaries (global structure context)
- **Prediction Heads**: Per-node logits `(B, P, L, 2)` + global solvability logits `(B, 2)`

### Loss Function (`src/ml/core/loss.py`)
`reinforce_loss` uses Gumbel-Softmax to allow gradient flow through discrete logic assignments:
- **Soft/Full Edge Loss**: Penalizes gate-logic violations (NOT/BUFF violations weighted 2×)
- **Reconvergence Consistency Loss**: MSE on reconvergence node logits across paths
- **Anchor Supervision**: Cross-entropy on pre-verified anchor values (SAT samples only)
- **Solvability Loss**: Weighted cross-entropy (UNSAT:SAT = 10:1) for the solvability head
- **Entropy Regularization**: Prevents overconfident distributions

### Dataset & Training (`src/ml/`)
- `src/ml/core/dataset.py`: `ReconvergentPathsDataset` loads `.pkl` files or preprocessed tensor shards. Supports anchor injection, constraint curriculum, and LRU shard caching.
- `src/ml/train.py`: Main training loop with AMP, gradient clipping (max norm 1.0), Gumbel temperature annealing (`τ_t = τ₀ × 0.99^(epoch-1)`, min 0.1), and constrained curriculum (first 25% epochs unconstrained, then linearly ramps).
- `src/ml/data/embedding.py`: `bench_to_embed()` — extracts DeepGate GNN embeddings (128-dim structural `hs` and functional `hf`). Caches results in `.deepgate_cache/` per circuit.

### RL Pipeline (`scripts/`, `src/ml/rl/`)
- `scripts/collect_experience.py`: Runs AI-PODEM across benchmark circuits, records steps via `ExperienceRecorder`
- `src/ml/rl/rl_recorder.py`: `ExperienceRecorder` / `ExperienceStep` — buffers and persists REINFORCE episodes to disk
- `scripts/train_rl.py`: Offline REINFORCE fine-tuning on collected episodes
- `scripts/run_rl_pipeline.py`: Orchestrates the full collect → train → benchmark cycle; parallelizes collection across GPUs (capped by available RAM, ~5 GB/process)

### Code Style
- Ruff with `line-length = 100`, target Python 3.10, rules `E`, `F`, `I`
- Double quotes, space indentation
