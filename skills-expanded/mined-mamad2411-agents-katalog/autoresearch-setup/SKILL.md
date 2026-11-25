---
name: autoresearch-setup
description: Set up a new autoresearch experiment run from scratch. Handles branch creation, data verification, baseline run, and results.tsv initialization. Use when starting fresh or on a new machine.
---

# Autoresearch Setup Skill

Initialize a new autoresearch experiment run.

## Steps

1. **Check prerequisites**:
   - Apple Silicon Mac (verify with `uname -m` → arm64)
   - Python 3.10+ (verify with `python3 --version`)
   - uv installed (verify with `which uv`)

2. **Verify data**:
   ```bash
   ls ~/.cache/autoresearch/data/ | head -5       # data shards exist?
   ls ~/.cache/autoresearch/tokenizer/             # tokenizer exists?
   ```
   If missing, tell user to run: `uv run prepare.py`

3. **Check machine memory**:
   ```bash
   sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}'
   ```
   - < 16GB: Use `FINAL_EVAL_BATCH_SIZE=32`, `DEVICE_BATCH_SIZE=8`
   - 16-32GB: Use `FINAL_EVAL_BATCH_SIZE=64`, `DEVICE_BATCH_SIZE=16`
   - 32-64GB: Use `FINAL_EVAL_BATCH_SIZE=128`, `DEVICE_BATCH_SIZE=16`
   - 64GB+: Use `FINAL_EVAL_BATCH_SIZE=256`, `DEVICE_BATCH_SIZE=16`

4. **Propose run tag**: Based on date (e.g., `mar10`) or purpose (e.g., `mar10-muon`)

5. **Create branch**: `git checkout -b autoresearch/<tag>`

6. **Adjust train.py** for machine (especially `FINAL_EVAL_BATCH_SIZE`)

7. **Run baseline**: `uv run train.py > run.log 2>&1`

8. **Initialize results.tsv**:
   ```
   commit	val_bpb	memory_gb	status	description
   <hash>	<val_bpb>	<mem>	keep	baseline
   ```

9. **Confirm setup** with user, then hand off to `autoresearch-loop`
