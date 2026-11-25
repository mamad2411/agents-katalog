---
compatibility: macOS, codex-native, opencode
name: eth-euler-hpc
description: "Delegate ETH Zurich Euler HPC (Slurm) job management to an AI agent. Submit, monitor, retrieve, and cancel jobs from a laptop with the free public-share limits (max 48 CPU cores, 128 GiB of memory, no GPUs). Use when the user wants to run heavy computation, large-dataset processing, or long-running jobs on ETH HPC; check storage quotas; transfer data to/from Euler; generate public-share job scripts; or debug Slurm jobs. Off-campus use requires the ETH VPN first. CLI: `eth-hpc` (doctor, ssh, quota, queue, submit, gen, interactive, cancel, push, pull, tunnel, limits)."
---

# ETH Euler HPC (Slurm)

Local, structured access to ETH Zurich's **Euler** cluster for research jobs.
The user has a standard student account → the **free "public share"**. The
workflow follows the public-share resource, storage, and access constraints
documented below.

## When to use

- Heavy compute, long-running jobs, or large-dataset processing that a MacBook Air cannot do.
- Data transfer to/from Euler (`push` / `pull`).
- Checking quotas, queue status, or job results.
- Interactive compute sessions for debugging (`eth-hpc interactive`).

## Acknowledgments — Citing Euler in Publications

Verified on docs.hpc.ethz.ch/publications (2026-08):

- **No obligation** for ETH members (incl. student accounts): Euler does **not**
  require you to cite/acknowledge it in journal papers, conference papers, or
  theses.
- **Guest users are kindly asked** to acknowledge Euler in the acknowledgment
  section — the public share is financed by SIS's limited budget.
- If you do mention Euler, email the publication reference to the HPC group
  (cluster-support@id.ethz.ch) — they add it to their public list.
- No standard sentence. Examples: "The numerical simulations were performed on
  the Euler cluster operated by the High Performance Computing group at ETH
  Zurich." / "All simulations were performed on the ETH Zurich Euler cluster."

## Resource and access constraints

1. **Set `--time` on every job.** The workflow requires an explicit time limit.
2. **Public-share limits: ≤ 48 CPU cores and ≤ 128 GiB of memory per job; no GPUs.**
   `eth-hpc submit` rejects requests above these limits.
3. **Run compute through Slurm, not on login nodes.** Use login nodes for light tasks
   such as editing, compiling, and submitting; use `sbatch` or `srun --pty` for compute.
4. **Use one personal account.** Do not share credentials or SSH keys.
5. **Follow the storage model** (see below). `$SCRATCH` is purged after 15 days,
   is not backed up, and file timestamps must not be modified to avoid purging.
6. **Use `eth_proxy` only when required.** Compute nodes have no internet by default,
   and the proxy has limited capacity.
7. **Install software in `$HOME` or through modules/conda.** Euler does not provide
   `sudo` access.

## Storage model

| Path | Capacity | Backup | Purge | Use for |
|---|---|---|---|---|
| `$HOME` (`/cluster/home/<user>`) | 50 GB, 500k files | nightly + snapshots | on account deletion | code, results, small important files |
| `$SCRATCH` (`/cluster/scratch/<user>`) | 2.5 TB, 1M files | **none** | **after 15 days** | large datasets, intermediate data |
| `$TMPDIR` (node-local) | node-dependent | none | at job end | fast I/O during a job (request with `--tmp`) |
| Project/Work | shareholder-only | — | — | not available on the public share |

Data workflow: large datasets go to `$SCRATCH`; **rsync final results back to
`$HOME` or `$SLURM_SUBMIT_DIR` before the job ends**; archive many-small-file
transfers; contact cluster support for transfers larger than 1 TB.

## Quickstart

```bash
# 0. (off-campus) connect to ETH VPN: https://www.vpn.ethz.ch/
# 1. one-time config — create ~/.config/eth-hpc/config:
#      USERNAME="your-eth-username"
#      SSH_KEY="~/.ssh/euler"      # any filename works; never commit real keys
# 2. preflight check (config, network, SSH auth, first-login hints)
eth-hpc doctor
# 3. log in (first time: accept usage rules + enter email verification code)
eth-hpc ssh
# 4. generate and edit a public-share job script
eth-hpc gen job.sbatch
# 5. validate + submit (dry-run first)
eth-hpc submit job.sbatch --dry-run
eth-hpc submit job.sbatch
# 6. monitor and retrieve
eth-hpc queue
eth-hpc pull '~/eth-hpc-jobs/slurm-*.out' results/
```

First-login note: SSH will ask you to accept the ETH "Benutzungsordnung für
Telematik (BOT)" rules, then sends a verification code to your ETH email. If no
prompt appears, use `eth-hpc ssh --first-login`
(`-o PreferredAuthentications=keyboard-interactive -o PubkeyAuthentication=no`).

## CLI reference

| Command | Purpose |
|---|---|
| `eth-hpc doctor` | Preflight: config, VPN/network reachability, SSH auth |
| `eth-hpc ssh [--first-login]` | Interactive shell on a login node |
| `eth-hpc quota` | Storage quotas (`lquota`) |
| `eth-hpc queue [jobid]` | Jobs (`myjobs`, `squeue` fallback) |
| `eth-hpc gen [file]` | Generate public-share job template |
| `eth-hpc submit <file>` | Validate against public-share limits, then submit |
| `eth-hpc interactive [--cpus N --time H:MM:SS --mem-per-cpu G]` | Small `srun --pty` compute session |
| `eth-hpc cancel <jobid>` | Cancel (confirmation required) |
| `eth-hpc push <local> [remote-dir]` / `--scratch` | Upload via rsync |
| `eth-hpc pull <remote> [local-dir]` | Download via rsync |
| `eth-hpc tunnel start/status/stop` | euler-tunnel (VS Code Remote into a batch job) |
| `eth-hpc limits` | Print researched public-share limits |

Global: `--dry-run` (print, don't execute), `-y/--yes`, `--config FILE`.

## Job script rules

- `--time` **required**; parsed and capped (default cap `24:00:00`, configurable).
- Total cores `--ntasks × --cpus-per-task` must be ≤ 48.
- Total memory (`--mem` or `--mem-per-cpu × cores`) must be ≤ 128 GiB.
- `--gpus` / `--gres` → **rejected** (public share has no GPUs).
- Multi-node (`--nodes > 1`) → warning.
- `$SCRATCH` usage → warning to rsync results back (15-day purge).
- Request resources as specific as required, as loose as possible; don't specify
  partitions, CPU/GPU types, or exact nodes — Slurm handles that (faster start).

## Research workflow

- **Interactive dev**: `eth-hpc interactive --cpus 8 --time 02:00:00` for
  debugging; `euler-tunnel` (see below) for VS Code connected into a batch job.
- **Large datasets**: push to `$SCRATCH` (`eth-hpc push data/ --scratch`), process in
  batch jobs reading from `$SCRATCH` (or copy to `$TMPDIR` for I/O-heavy steps),
  then pull results.
- **Web alternatives** (interactive only, not for long jobs): JupyterHub at
  https://jupyter.euler.hpc.ethz.ch, RStudio, Code Server, and the Slurm web GUI
  at https://slurm-jobs-webgui.euler.hpc.ethz.ch.
- **Troubleshooting**: `ReqNodeNotAvail` = job is just queued (be patient);
  "Too many authentication failures" = use `-o IdentitiesOnly=yes` (the CLI does
  this when `SSH_KEY` is set); timeouts = VPN not connected; no `sudo` = install
  in `$HOME`; `module avail`/`module spider` to find software.

## euler-tunnel (configured on this machine)

`euler-tunnel` SSH-tunnels into a **running batch job** — for VS Code Remote,
Jupyter/TensorBoard, or long-lived `tmux`/`screen` inside a compute node.

- Enabled locally: `~/.ssh/config` has a `Host euler-tunnel` block (User
  `your-eth-username`, `IdentityFile ~/.ssh/euler`, `IdentitiesOnly yes`,
  `ProxyCommand ssh -i ~/.ssh/euler ... euler-tunnel connect`), and
  the tunnel host key is in `~/.ssh/known_hosts`. Remote config was generated
  with `euler-tunnel config` on Euler.
- Lifecycle (all through the toolkit):
  ```bash
  eth-hpc tunnel start --time=04:00:00 --cpus-per-task=2 --mem-per-cpu=2G
  eth-hpc tunnel status          # wait until RUNNING (public share queues)
  ssh euler-tunnel 'hostname'    # run commands inside the compute-node job
  # VS Code: Remote-SSH -> "euler-tunnel"
  eth-hpc tunnel stop
  ```
- Only works with the configured key (passwordless). Re-run `euler-tunnel
  config` on Euler if the host key changes.

## Agent workflow

1. **Run `eth-hpc doctor` before remote operations.** It verifies VPN reachability
   and SSH authentication. If it fails, connect to the ETH VPN and retry.
2. **Preview every submission**: run `eth-hpc submit <file> --dry-run`, review the
   printed commands, then submit.
3. **Use the validator for every submission.** GPU requests, missing `--time`, and
   requests above the configured CPU or memory limits are rejected.
4. **Submit compute through Slurm.** Use login nodes for editing, compiling, and
   submitting; use `eth-hpc interactive` or batch jobs for computation.
5. **Large-data workflow**: `eth-hpc push data/ --scratch` → the job reads
   `$SCRATCH`/`$TMPDIR` → `eth-hpc pull` copies results back. Scratch is purged
   after 15 days and is not backed up.
6. **Treat `PENDING` as a queue state.** Public-share jobs can wait behind
   shareholder jobs. Poll `eth-hpc queue <jobid>`; do not resubmit solely because
   a job is pending.
7. **Credentials never enter the repo or conversation**: config lives in
   `~/.config/eth-hpc/config`, keys in `~/.ssh/`. Never echo or commit them.
8. **Clean up after yourself**: remove test/remote job files
   (`~/eth-hpc-jobs/`) when a session is done; stop tunnel jobs with
   `eth-hpc tunnel stop`.

## Sources

All limits were researched from https://docs.hpc.ethz.ch/ (2026-08). Full facts
with page URLs: `references/limits.md`. Re-verify live once logged in with
`lquota`, `myjobs`, and `sacctmgr show qos` — limits can change.
