---
name: dispatch
description: Activate an Aevum block and launch the unattended orchestrator loop for it in the background.
disable-model-invocation: true
argument-hint: <BLOCK_ID> [--dry-run]
---

Launch block `$ARGUMENTS`. The run is unattended and can take hours.

1. Check each precondition and stop with a clear message if one fails:
   - `docs/blocks/<BLOCK_ID>/block.yaml` and `baseline.json` exist
     (offer `bash scripts/capture-baseline.sh <BLOCK_ID>` if the baseline
     is missing).
   - `git status --porcelain` is empty: workers branch from committed state.

2. If `status: draft`, ask the user to confirm activation. On yes, set
   `status: active`, `activated_at` (UTC now) and `activated_by` (ask for
   the name), refresh `base_sha` to the tip of `base_branch`, and let the
   user commit that change before launching.

   Then `python3 scripts/block-preflight.py <BLOCK_ID>` must exit 0.

3. Start the loop with the Bash tool's `run_in_background`:

   ```bash
   bash .claude/scripts/orchestrate-block-loop.sh $ARGUMENTS
   ```

4. Tell the user, briefly:
   - progress: `tail -f logs/blocks/<BLOCK_ID>/progress.jsonl`
   - early abort: write `logs/blocks/<BLOCK_ID>/signoff/ABORT.md`
   - knobs, set before launch: `AEVUM_EFFORT` (default medium),
     `AEVUM_PERMISSION_MODE` (default auto), `AEVUM_MODEL`,
     `AEVUM_MAX_CONCURRENT_SUBAGENTS` (default 4), `MAX_CONTINUATIONS`
   - when the block is ready, `/signoff <BLOCK_ID>` (`/aevum:signoff` with the plugin) reviews it.

Do not poll the run. You are notified when the background command exits;
then report the loop's exit code and the last ledger events.
