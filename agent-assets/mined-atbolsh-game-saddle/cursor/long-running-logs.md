---
description: Long-running jobs must leave diagnosable files, not a live tty
alwaysApply: true
---

# Long-running jobs — exhaustive on-disk logs

A train / distill / weekend / datagen run that lasts hours is a
**hands-off** job. If it dies and the only record was a tty, the run
is wasted. `dmesg` will not show a CUDA OOM (userspace, exit 1).
`nohup` is a SIGHUP shield, not a logging strategy.

When you write or change an orchestrator or a GPU loop:

- **Parent file log** (`data_game/<label>_orchestrator.log` or
  equivalent). `logging.basicConfig` to stderr is not enough.
- **Tee every child** stdout+stderr to
  `data_game/<label>_stages/<stage>.log`. Set `PYTHONUNBUFFERED=1`.
- **Write the wait status** to `<stage>.exit.json`: exit code,
  `signaled`, `signal_name`. Negative subprocess rc is `-signal`.
- **VRAM** like `run_weekend.VramMonitor`: 1/min `nvidia-smi`
  `memory.used` → `data_game/<label>_vram.jsonl`, tagged with stage,
  fsynced. Reuse the class; do not invent a second sampler.
- **In-process heartbeat** before each expensive forward: sources,
  token lengths, packed B×T, GPU MiB. Overwrite `heartbeat.json`
  atomically. A SIGKILL must still leave the last successful write
  (`flush` + `fsync`).
- **Every optimizer step** to `last_step.json` (not only every
  `log_steps`). Non-finite loss / `grad_norm` **abort** with a
  `nonfinite_*` event — never continue.
- **Exceptions** → `crash.txt` + a `crash` event, then re-raise.
  Do not rely on the tty for the traceback.

```python
# BAD — child dies, parent has no file, dmesg is empty
subprocess.run(cmd)

# GOOD — tee + exit record + VramMonitor.set_stage(stage)
_run_stage(cmd, stage)  # see training/context_distill.py
```
