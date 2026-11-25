---
name: autoresearch-fix
description: Debug and fix autoresearch train.py crashes or errors. Reads run.log, identifies the issue, and applies a fix. Use when the user reports a crash, OOM error, or training failure.
---

# Autoresearch Crash Debugger

Fix training crashes and errors in the autoresearch loop.

## Common Issues & Fixes

### OOM During Eval
**Symptom**: `RuntimeError: [metal::malloc] Attempting to allocate X bytes which is greater than the maximum allowed buffer size`
**Fix**: Reduce `FINAL_EVAL_BATCH_SIZE` in `train.py`. Try 128, then 64, then 32.

### OOM During Training
**Symptom**: Same metal::malloc error during training steps
**Fix**: Reduce `DEVICE_BATCH_SIZE` (increase `grad_accum_steps` to compensate). Or reduce model size (DEPTH, model_dim).

### Loss Explodes (> 100)
**Symptom**: Script prints "FAIL" and exits
**Fix**: Usually a learning rate issue. Try halving all LRs. Check for NaN in weights.

### Shape Mismatch
**Symptom**: `ValueError` or assertion error about tensor shapes
**Fix**: Check that `n_embd % n_head == 0`, `n_head % n_kv_head == 0`, and batch/sequence dimensions are consistent.

### Import Error
**Symptom**: `ModuleNotFoundError`
**Fix**: Only use packages in `pyproject.toml`. No new dependencies allowed.

### Timeout (> 15 min)
**Symptom**: Run doesn't complete
**Fix**: Model is too large for the hardware. Reduce DEPTH, model_dim, or TOTAL_BATCH_SIZE.

## Debug Steps

1. `tail -n 50 run.log` — read the stack trace
2. Identify which phase failed: data loading, compile, training, eval
3. Apply the appropriate fix above
4. If the fix is trivial (typo, batch size), fix and re-run
5. If the idea is fundamentally broken (architecture doesn't work), log as crash and move on

## Memory Estimation
- Model params (bfloat16): `num_params_M * 2` MB
- Adam state (float32): `num_params_M * 8` MB (m + v)
- Activations scale with `DEVICE_BATCH_SIZE * MAX_SEQ_LEN * n_embd`
- Eval activations scale with `FINAL_EVAL_BATCH_SIZE * MAX_SEQ_LEN * n_embd`
- Rule of thumb: eval batch can be 4-8x device batch on most machines
