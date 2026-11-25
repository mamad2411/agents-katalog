---
name: bash-parallelize
description: Identify and exploit parallelization opportunities in bash workflows. Use
  when the user wants to run the same operation on multiple independent datasets,
  mutants, replicas, or files — either by describing the task or by providing an
  existing bash loop/script. Spawns parallel subagents and collects results.
---

# Bash Parallelize

Finds independent work items in a task or script and runs them in parallel using subagents.

## Usage examples

```
/bash-parallelize analyze RMSD for runs/mutA, runs/mutB, runs/mutC using gmx rms
/bash-parallelize  (then paste a bash for-loop)
set up GROMACS equilibration for these 4 mutants and use /bash-parallelize
```

---

## Two modes

### Mode 1 — Task description
User describes work to be done on N independent items (datasets, mutants, replicas, files).
The skill designs the per-item work, identifies the item list, then parallelizes.

### Mode 2 — Script/loop
User provides an existing bash `for`/`while` loop or script.
The skill parses the loop body, verifies independence, then parallelizes.

Detect mode: if the user's input contains a bash loop construct (`for`, `while`, `do`, `done`) or a script path, use Mode 2. Otherwise use Mode 1.

---

## Step 1 — Extract work items

**Mode 1:** Parse the task description to identify:
- The list of independent items (datasets, paths, mutant names, replica IDs, etc.)
- The operation to perform on each item
- Any shared inputs (topology files, parameter files) vs. per-item inputs

**Mode 2:** Parse the loop/script to identify:
- The iterator variable and its value list
- The loop body (the work performed per item)
- Any variables defined outside the loop (shared context)

If items are ambiguous, list what you inferred and ask the user to confirm before proceeding.

---

## Step 2 — Independence check

Before launching any agents, verify that the work items are genuinely independent. Flag and abort if any of the following are detected:

| Dependency type | Example | Action |
|---|---|---|
| Shared output file | Multiple items write to the same path | **Abort** — report collision |
| Ordering dependency | item N reads output of item N-1 | **Abort** — must run serially |
| Shared mutable state | items modify the same topology or index file | **Abort** — report conflict |
| Shared read-only inputs | items read the same .mdp, .top, .itp | **OK** — read-only sharing is safe |

For Mode 2, apply this heuristic: a dependency exists if the same path or variable appears as **both** a read input and a write output across different iterations.

If independence cannot be confirmed, report the concern and ask the user whether to proceed.

---

## Step 3 — Safety check (run before launching agents)

```bash
# Get 1-minute load average and CPU count
LOAD=$(uptime | awk -F'[a-z]:' '{print $2}' | awk -F',' '{print $1}' | tr -d ' ')
NCPU=$(nproc 2>/dev/null || sysctl -n hw.logicalcpu)
echo "Load: ${LOAD}  CPUs: ${NCPU}"
```

Compute `load_fraction = LOAD / NCPU`.

| load_fraction | Action |
|---|---|
| < 0.6 | Proceed normally |
| 0.6 – 0.8 | Warn the user; proceed unless they say stop |
| > 0.8 | **Abort** — system is heavily loaded; ask user before continuing |

**Concurrency cap:**
- Default: `max_parallel = min(N_items, floor(NCPU / 2))`
- User can override: `--max-parallel N` anywhere in the request
- If `N_items > max_parallel`, split into batches and run each batch sequentially, reporting progress between batches

---

## Step 4 — Launch parallel agents

Construct one agent prompt per work item. Each prompt must be **self-contained**: include the specific item, its paths, the full task description, and any shared context (project root, topology paths, force field, etc.).

**Launch all agents for the current batch in a single message** (parallel Agent tool calls). Do not stagger or sequence independent items.

Agent prompt template:
```
Context: [shared project context — paths, tools, force field, etc.]

Your task: [specific operation] for item: [item identifier]
  - Input: [input path(s) for this item]
  - Output: [expected output path(s) for this item]
  - [any item-specific parameters]

Complete the task and report:
1. Whether it succeeded or failed
2. Key output (path, value, or summary)
3. Any warnings or errors encountered
```

---

## Step 5 — Collect and report results

After all agents complete, produce a summary table:

```
Item              Status     Output                    Notes
────────────────  ─────────  ────────────────────────  ──────────────────────
mutant_A          ✓ done     runs/mutA/rmsd.xvg        —
mutant_B          ✓ done     runs/mutB/rmsd.xvg        —
mutant_C          ✗ failed   —                         grompp error: missing itp
```

Also report:
- Total wall-clock time for the parallel batch
- Estimated serial time (sum of individual durations if available)
- Any items that need follow-up

If any item failed, show the error and suggest a fix. Do not silently skip failures.

---

## Constraints and limits

- **Do not use Bash background jobs** (`&`, `wait`) — use the Agent tool exclusively for parallelism
- **Do not launch more agents than `max_parallel`** in a single batch
- **Do not modify shared files** (topology, index, force field) from within a per-item agent
- This skill does not sandbox agents — it trusts them to stay within their assigned item's scope
- If the user's request involves SLURM job submission, each agent submits its own job; the agents do not wait for SLURM jobs to finish (that would require polling)
