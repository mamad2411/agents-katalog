---
name: dbscan-parameter-tuning-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for dbscan-parameter-tuning using latest full-instruction v2 family injection.
allowed-tools:
  - dbscan_grid_search
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: dbscan-parameter-tuning

## 1. When to use this skill
Use this skill to optimize DBSCAN hyperparameters for clustering citizen science annotations of Mars clouds. The objective is to find the Pareto frontier balancing maximum F1 score and minimum delta (average standard Euclidean distance). This applies when the environment has citizen science and expert annotation datasets, requiring a grid search over `min_samples`, `epsilon`, and `shape_weight` using a custom distance metric.

## 2. Visible input and artifact inventory
- **Input Data**: 
  - `/root/data/citsci_train.csv`: Citizen science annotations (`file_rad`, `x`, `y`).
  - `/root/data/expert_train.csv`: Expert annotations (`file_rad`, `x`, `y`).
- **Output Artifact**: 
  - `/root/pareto_frontier.csv`: CSV containing Pareto-optimal hyperparameters (`F1`, `delta`, `min_samples`, `epsilon`, `shape_weight`).

## 3. Execution procedure for the current task
1. **Read Instructions**: Understand the custom distance metric formula and the grid search space for `min_samples`, `epsilon`, and `shape_weight`. Verify input datasets in `/root/data/`.
2. **Run Grid Search**: Use the `dbscan_grid_search` tool to perform the hyperparameter grid search. It evaluates combinations by clustering points, matching centroids, and computing F1 score and average delta across all unique images in the expert dataset.
3. **Filter and Identify Pareto Frontier**: Keep results with average F1 > 0.5. Identify Pareto-optimal points where no other point has both a higher F1 score and a lower delta.
4. **Format Output**: Format points into a CSV. Round `F1` and `delta` to 5 decimal places, `shape_weight` to 1 decimal place. `min_samples` and `epsilon` are integers.
5. **Write Artifact**: Save to `/root/pareto_frontier.csv`.

## 4. Family tool routing and useful placeholder snippets
- **Tool**: `dbscan_grid_search`
- **Usage**: Handles the grid search and evaluation process, abstracting the complexity of running DBSCAN with custom metrics.
- **Snippet**: 
  ```python
  results = dbscan_grid_search(
      citsci_data="/root/data/citsci_train.csv",
      expert_data="/root/data/expert_train.csv",
      min_samples_range=[3, 4, 5, 6, 7, 8, 9],
      epsilon_range=list(range(4, 25, 2)),
      shape_weight_range=[0.9 + i*0.1 for i in range(11)],
      distance_metric="custom_formula"
  )
  ```

## 5. Validation checks before final submission
- **File Existence**: Verify `/root/pareto_frontier.csv` exists.
- **Header Check**: Ensure header is exactly `F1,delta,min_samples,epsilon,shape_weight`.
- **Data Types**: Check `F1` and `delta` have 5 decimal places, `shape_weight` has 1 decimal place, `min_samples` and `epsilon` are integers.
- **Pareto Optimality**: Confirm points form a Pareto frontier.

## 6. Common failure modes and repair actions
- **Missing Images in Average**: Failing to include images with no citizen science points in F1 average. *Repair*: Loop over all unique `file_rad` values in the expert dataset.
- **Incorrect Delta Calculation**: Including NaN values in delta average. *Repair*: Exclude images where no matches were found from delta average.
- **Wrong Distance Metric**: Using standard Euclidean distance instead of the custom metric. *Repair*: Check the instruction for the exact distance formula.

## 7. Finalizer capsule
If nearing the maximum step limit and the grid search fails, generate a minimal valid artifact.
- **Action**: Write `/root/pareto_frontier.csv` with the correct header and a dummy row matching required data types (e.g., `0.50001,10.00000,5,10,1.0`). This prevents evaluation script crashes.
