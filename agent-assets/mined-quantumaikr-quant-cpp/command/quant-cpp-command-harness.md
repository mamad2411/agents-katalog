---
description: Launch the hierarchical harness (Karpathy loop + ClawTeam parallel agents)
argument-hint: Optional target score (default 0.9) or "single" for single-agent mode
---

# Harness

Launch the full Hierarchical Harness that combines the Karpathy AutoResearch loop with ClawTeam multi-agent parallelism.

## How It Works

The harness has an Outer Loop (you, the Leader) and Inner Loops (spawned workers):

```
You (Leader):
  score → identify bottleneck → delegate modules → merge gate → repeat

Workers (in isolated worktrees):
  each runs: score → modify own module → score → report back
```

## Execution

### Step 1: Score and assess phase

Run `bash score.sh` and determine the current phase:

| Score | Phase | Action |
|-------|-------|--------|
| < 0.05 | Foundation | YOU do it directly (single agent) |
| 0.05 ~ 0.30 | Core Algorithms | Spawn parallel workers: polar, qjl, uniform |
| 0.30 ~ 0.60 | Advanced | Spawn parallel workers: turbo, cache, simd-neon, bench |
| > 0.60 | Fine-tuning | YOU do it directly (precision matters) |

### Step 2: For Foundation / Fine-tuning phases (single agent)

Use the `/develop` command pattern — implement one WBS item at a time.

### Step 3: For parallel phases, spawn ClawTeam workers

$ARGUMENTS can override the target score (default: 0.9).

```bash
# Create team
clawteam team spawn-team tq-dev -d "quant.cpp development"

# Spawn workers for each independent module
clawteam spawn --team tq-dev --agent-name polar --workspace --repo . \
  --task "Implement PolarQuant in src/core/tq_polar.c. Read refs/PolarQuant/models/modeling_llama_polar.py for algorithm. Write tests/test_polar.cpp. Run bash score.sh --quick after changes. Only modify: src/core/tq_polar.*, tests/test_polar.*"

clawteam spawn --team tq-dev --agent-name qjl --workspace --repo . \
  --task "Implement QJL in src/core/tq_qjl.c. Read refs/QJL/models/llama2_utils_qjl.py for algorithm. Write tests/test_qjl.cpp. Run bash score.sh --quick after changes. Only modify: src/core/tq_qjl.*, tests/test_qjl.*"
```

### Step 4: Wait and merge gate

```bash
# Wait for all workers
clawteam task wait tq-dev --timeout 1800

# Merge gate: merge each worker one-by-one
# For each worker branch:
#   1. git merge <branch> --no-edit
#   2. bash score.sh --quick
#   3. If score dropped: git reset --hard HEAD~1
#   4. If score OK: continue
```

### Step 5: Loop back to Step 1

Repeat until the target score is reached.

## Key Rules

- Workers must only modify files in their module ownership (see CLAUDE.md)
- Merge gate ALWAYS checks score after each merge — revert if it drops
- Foundation and fine-tuning phases are always single-agent (safer)
- Monitor workers: `clawteam board attach tq-dev`
