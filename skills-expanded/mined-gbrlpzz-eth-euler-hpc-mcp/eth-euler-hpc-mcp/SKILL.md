---
name: eth-euler-hpc-mcp
description: "Connect Prime Agent to the local eth-euler-hpc-mcp MCP server for Slurm job management on ETH Zurich's Euler HPC cluster (free public share): submit, monitor, cancel and retrieve jobs; check quotas; validate job scripts; transfer data via rsync. Use when the user wants to run heavy compute or large-dataset jobs on Euler, or asks for euler_* MCP tools. Local stdio server — requires the user's SSH config and, off-campus, the ETH VPN."
compatibility: Prime Agent (Python-backed skill; spawns the local eth-euler-hpc-mcp server over stdio)
---

# ETH Euler HPC MCP (Prime Agent integration)

Bridges Prime Agent to the **local, open-source** `eth-euler-hpc-mcp` server
(https://github.com/gbrlpzz/eth-euler-hpc-mcp): the same tools Claude/Cursor
etc. can use, exposed as async methods on the `euler_hpc` singleton.

## Setup (one-time)

1. **Install the server** (the skill only spawns it, it does not bundle it):
   ```bash
   uv tool install eth-euler-hpc-mcp        # or: pipx install eth-euler-hpc-mcp
   ```
   (If the repo is cloned at `~/eth-euler-hpc-mcp` and `uv` is installed, the
   skill can also run it with `uv run --project ~/eth-euler-hpc-mcp` — no
   install needed.)
2. **Configure your account** (`~/.config/eth-hpc/config`):
   ```bash
   USERNAME="your-eth-username"
   SSH_KEY="~/.ssh/euler"      # optional but recommended; never commit real keys
   ```
3. **Off-campus**: connect to the ETH VPN first (https://www.vpn.ethz.ch/).
4. Restart the agent session (or `/reload`) so the skill is picked up.

Overrides: `ETH_EULER_HPC_MCP_CMD` (full command line, e.g.
`"uv run --project /path/to/eth-euler-hpc-mcp eth-euler-hpc-mcp"`) and
`ETH_EULER_HPC_MCP_REPO` (repo dir for the `uv run` fallback).

## Usage (from the agent kernel)

```python
from eth_euler_hpc_mcp import euler_hpc

await euler_hpc.euler_doctor()              # preflight: config, VPN, SSH auth
await euler_hpc.euler_limits()              # public-share limits & storage rules
tpl = await euler_hpc.euler_gen()           # public-share #SBATCH template
await euler_hpc.euler_validate_submit(script_path="job.sbatch")
await euler_hpc.euler_submit(script_path="job.sbatch")                 # dry-run preview
await euler_hpc.euler_submit(script_path="job.sbatch", dry_run=False, confirm=True)  # real submit
await euler_hpc.euler_queue()               # or euler_queue(job_id="12345")
await euler_hpc.euler_cancel(job_id="12345", confirm=True)
await euler_hpc.euler_push(local_path="data/", scratch=True, dry_run=False, confirm=True)
await euler_hpc.euler_pull(remote_path="~/eth-hpc-jobs/slurm-*.out", local_dir="results/", confirm=True)
```

## Operational workflow

1. **Run `euler_doctor` before remote operations.** If it fails, connect to the
   ETH VPN and retry.
2. **Preview every submission** (`euler_submit` defaults to dry-run). Review the
   printed commands, then call again with `dry_run=False, confirm=True`.
3. **Use the validator for every submission.** GPU requests, missing `--time`, and
   requests above the configured CPU or memory limits are rejected. Explain the
   rejection and propose a compliant request when needed.
4. **Treat `PENDING` as a queue state.** Public-share jobs can wait behind
   shareholder jobs. Poll `euler_queue(job_id=...)`; do not resubmit solely
   because a job is pending.
5. **Large-data workflow**: `euler_push(..., scratch=True)` → the job reads
   `$SCRATCH` (or `$TMPDIR` for I/O-heavy steps) → `euler_pull` copies results
   back. Scratch is purged after 15 days and is not backed up.
6. **Keep credentials local.** The server runs on the user's machine and uses
   the user's SSH configuration. Never request keys or tokens in chat.
7. **Clean up completed runs.** Remove temporary remote job files
   (`~/eth-hpc-jobs/`) when a session is complete.
