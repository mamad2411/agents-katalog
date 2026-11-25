---
name: eda-stage-checkpoint-golden
description: Create immutable stage checkpoints for Innovus flows. Use when users ask for fixed golden files or restart-from-stage workflows (place/cts/route) with matched DEF+V+SDC and reproducible manifests.
---

# EDA Stage Checkpoint Golden

Use this skill to freeze reusable checkpoints and avoid rerunning all stages.

## Step 1: Build a checkpoint bundle

```bash
ROOT=/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00
cd "$ROOT"

bash scripts/debug/create_stage_golden_checkpoint.sh \
  --design=<design> \
  --tag=<golden_tag> \
  --tech-profile=<tech_profile> \
  --place-run-dir=<run_dir_for_placed_def> \
  --cts-run-dir=<run_dir_for_postcts_def> \
  --route-run-dir=<run_dir_for_routed_def>
```

Output root:
- `regression/stage_checkpoints/<tag>/<design>/`

## Step 2: Verify integrity

Check:
- `manifest.tsv`
- `sha256.tsv`
- `restore_examples.sh`

Do not edit files in an existing tag after creation.

## Step 3: Maintain stable pointer

Update a stable symlink when a new golden is approved:

```bash
ln -sfn <tag> regression/stage_checkpoints/<design>_stagegolden_current
```

## Step 4: Resume from chosen stage

Use generated restore templates in:
- `regression/stage_checkpoints/<tag>/<design>/restore_examples.sh`

Load `references/tagging_policy.md` for tag naming and source policy.
