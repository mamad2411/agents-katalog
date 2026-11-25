---
name: remote-compute
description: "Run work on SSH-reachable Unix-like machines: connect/diagnose, inspect, prepare environments, stage code/data, launch/monitor jobs, retrieve outputs, and clean up. Use for remote servers, clusters, workstations, GPU hosts, long jobs, environment setup, or result retrieval. Examples assume GNU/Linux with Bash; Windows/PowerShell is out of scope."
---

# Remote compute

Command examples assume a GNU/Linux remote with Bash and OpenSSH. On another
Unix-like host, use a native equivalent only after verifying its semantics.

Running work on an SSH-reachable machine is a loop: orient, prepare, move,
run, monitor, retrieve, clean up. The expensive failures are rarely exotic:
re-discovering the same host every session, launching before the environment
is proven, and losing outputs or jobs to a dropped connection. Each section
below prevents one of them.

## Establish the machine

Address hosts by an alias in `~/.ssh/config` (host, user, key, port,
`ProxyJump` for bastions), never by repeated ad-hoc flags; the alias keeps every
later `ssh`/`scp`/`rsync` command short and reproducible. If the alias is
missing, inspect existing config for conflicts and create it only from
user-supplied connection facts. Verify a new host-key fingerprint through a
trusted source; never disable host-key checking. For a session of repeated
commands, connection multiplexing (`ControlMaster auto`, `ControlPersist`)
removes the per-command handshake.

On failure, diagnose the part under local control first: inspect `ssh -G
<alias>`, key path and permissions, agent state, `ProxyJump`, DNS, and the exact
SSH error. Repair reversible user-owned config when the evidence is clear.
Missing credentials or authorization, a required VPN, firewall policy, DNS
outside local config, and an unavailable host require the user or operator;
report the exact blocker and stop. Do not retry in a loop.

## Orient before acting

Keep one durable note per host: what scheduler it runs, which
partitions/accounts work, activation commands that succeeded, storage layout
(home quota, scratch path, purge policy), and gotchas. Keep it project-local
when the host serves one project, otherwise somewhere stable such as
`~/.config/remote-compute/<alias>.md`. Read it before probing. Afterward,
append only facts true of the host, tagged with how you know them
(`verified <date>`, `per user`, `inferred`); project results and per-job
state do not belong there. If the session taught nothing new about the host,
write nothing.

On first contact, one batched probe answers most of it:

```sh
ssh <alias> 'uname -a; id; df -h ~ /tmp; nvidia-smi -L 2>/dev/null; command -v sbatch qsub bsub docker apptainer conda module 2>/dev/null; conda env list 2>/dev/null'
```

Recognize the host's shape rather than choosing one: a plain host (direct
execution, possibly yours to administer), a scheduler cluster (login node
plus `sbatch`/`qsub`/`bsub`, no root, compute nodes possibly without
internet, scratch with a purge policy), or a container-capable host
(docker/apptainer). The shape decides what "install", "run", and "background"
mean below.

When a system-level change is actually in scope on a machine the user
administers, `sudo -n true` establishes noninteractive sudo without prompting.
Do not probe or use sudo on a shared login node without explicit authorization.
Without authorized sudo, everything installs user-space: venv/conda under home
or scratch, `pip --user`, `~/.local`, `systemctl --user`. Even when sudo works,
confirm before a system-level change on any machine other people share.

## Prepare or reuse an environment

Reuse first. Before concluding a tool is missing, use the few cheap probes that
fit the host: `command -v <tool>`, `conda env list`, `module avail <tool>`, likely
install directories, and `python -c 'import <pkg>'`. If they come back empty,
ask before installing unless the user already authorized remote environment
setup and the proposed install is user-space, reversible, and within the stated
budget. Dependency choice, shared/system changes, or large downloads still
require a decision.

Provisioning is its own task with its own validation, never folded inline
into the real run: build the environment, prove it, then launch. Install
user-space by default. When install order matters — a package that would
drag in the wrong build of a dependency, such as a CPU-only torch — install
the pinned dependency in its own earlier `pip install` invocation; pip
leaves an already-satisfied requirement alone.

Large assets (model weights, reference databases) download once to
persistent storage, with the tool's cache variable pointed there. Use the
tool's own downloader, not hand-fetched files: layouts often include marker
files the tool checks. Verify from the tool's perspective by running the
real entrypoint once against the staged data.

Validation is a ladder, and only the top rung proves the invocation shape:

1. Import or `--version` exits 0 — cheap, catches almost nothing.
2. A tiny end-to-end run on toy input — catches GPU/library/cache
   mismatches.
3. The intended entrypoint, config, and key flags on a small or bounded input
   writing to an isolated output path — catches wrong flags, config files that
   override the command line, and paths that exist but lack what the tool
   checks for, without duplicating a multi-hour job or clobbering outputs.

Run rung 3 before building real work on the environment, and again after any
rebuild. Checks that only full input can exercise (full-scale memory, walltime,
long-run checkpointing) run on the first real execution, whose outputs are kept.

## Move code and data

Record `git rev-parse HEAD` and `git status --short` before staging code. When
the intended code is a committed revision and the host can reach the repository,
clone or fetch that exact revision so the remote copy has provenance. Otherwise
stage an explicit file set: review tracked and required untracked files, run an
`rsync` dry run, and exclude `.git`, credentials and secret files, environments,
caches, prior outputs, sockets, and unrelated large files. Add ignored files
only when the task explicitly needs them; never use an unreviewed `rsync -a` of
the whole working tree.

Data moves separately by `rsync -a --partial` so interrupted transfers resume.
Data already on the host is referenced in place, never round-tripped through
your machine, and host-to-host transfers go direct between the hosts. Budget
transfer time before starting: at typical link rates, gigabytes are minutes to
tens of minutes, and a large recurring dataset deserves a persistent remote
copy rather than per-run staging.

## Run

Give each run its own working directory on the host
(`.../runs/<name>-<timestamp>`): inputs staged in, outputs and logs written
under it. That directory is the unit of monitoring, retrieval, and cleanup.

Write the job as a script file, transfer it, and run `bash job.sh`. Never
build multi-layer quoting into an inline `ssh host "..."` command; escaping
bugs are the most common self-inflicted remote failure. In the script:

- `set -eo pipefail`; write activation explicitly (`source .../activate`,
  `module load ...`) rather than assuming the login shell provides it.
- Redirect output to files in the run dir and record the exit code (for
  example `trap 'echo $? > exit_code' EXIT`) so status stays inspectable
  after the fact.
- If you background children, record every PID and wait for all of them without
  letting `set -e` abort the loop. Accumulate a nonzero status, then exit only
  after every child has been reaped:

  ```bash
  status=0
  for pid in "${pids[@]}"; do
    wait "$pid" || status=$?
  done
  exit "$status"
  ```

  A bare `wait` can hide child failures.
- Bound the run with `timeout <budget>` or the scheduler's walltime, and
  make long jobs checkpoint periodically so a deadline or preemption costs
  one interval, not the run.
- Export thread caps matching your allocation (`OMP_NUM_THREADS`,
  `MKL_NUM_THREADS`); `nproc` sees the whole machine, not your share.

Anything longer than a few minutes must survive your SSH session dying: run
it under the scheduler if there is one, otherwise
`tmux new -d -s <name> 'bash job.sh'` or `nohup setsid bash job.sh &`. Never
leave a long job attached to your terminal.

Before spending a shared allocation or billed resource, state in one line
what you are about to run — tool, input, scale, expected duration. Honor any
budget the user gave (N jobs at a time, M GPUs) structurally: cap the loop
that launches, do not merely remember the number.

## Monitor

Poll, don't babysit: `ssh <alias> tail -n 50 <rundir>/run.log` and
`ssh <alias> cat <rundir>/exit_code` (scheduler: `squeue`/`qstat`/`bjobs`)
at intervals matched to the job's expected duration. A job silent in its log
for far longer than expected is worth inspecting (`ps`, GPU utilization)
before waiting more.

## Retrieve

`rsync -a` the run dir's outputs and logs back, on failure as well as
success; the log is the diagnosis. Retrieve selectively: pull deliverables
and logs, leave bulky intermediates remote, and record their remote path.
Verify the bytes arrived (sizes, or a checksum for anything critical) before
deleting anything remote.

## Clean up

Leaving is part of the run: kill tmux/screen sessions you started, close
tunnels, cancel orphaned scheduler jobs, and remove the run dir's scratch
once outputs are confirmed local (keep the run dir itself if resuming is
plausible, and say which you did). On billed or shared machines, idle jobs or
sessions left running cost money or goodwill; end the task with nothing of yours
running that the user did not ask to keep. Then update the host note if the
session taught something durable.

## When a run fails

Read the exit code and log tail first; they usually identify the failure class. An infrastructure failure (wrong partition or account, environment not
activated, missing module, out-of-memory, walltime, disk quota) is yours to
fix: adjust, record the fix in the host note, relaunch. A tool failure (the
tool ran and errored on its inputs or flags) needs the invocation or the
data fixed, not the host. Network errors from an offline or fenced compute
node (connection reset, cannot resolve host) mean there is no route out:
fetch where the network exists — the login node or your machine — and stage
the result in; retrying in place cannot succeed. Retries are cheap on a
smoke test and expensive on a long allocation: after two failed launches of
the same job, stop and reassess (or ask) rather than launch a third variant
blind.

## Conditional patterns

Apply only when the host actually has them.

**Scheduler (Slurm/PBS/LSF).** Detect the scheduler and use its own directive
and lifecycle commands; never write one scheduler's directives into another's
job file.

| Scheduler | Directive | Submit | Inspect | Cancel |
|---|---|---|---|---|
| Slurm | `#SBATCH` | `sbatch` | `squeue` | `scancel` |
| PBS | `#PBS` | `qsub` | `qstat` | `qdel` |
| LSF | `#BSUB` | `bsub` | `bjobs` | `bkill` |

Queue/partition, account/project, walltime, memory, GPU, and log directives are
site policy: derive them from verified host notes, site documentation, or a
known-good job, not generic assumptions. Use a scheduler array with an explicit
concurrency cap for many homogeneous tasks; use separate jobs when tasks differ
or need distinct recovery. Compute nodes often lack internet, so pre-stage
downloads from the login node. Scratch is usually purge-on-idle; record the
verified purge window in the host note.

**GPU.** `nvidia-smi` shows what is there; match the framework's CUDA build
to the driver. Validate with rung 2 of the ladder — a tiny forward pass that
prints the device name — because a clean import says nothing about kernels
matching the hardware.

**Long-running service** (a model server, a database, a notebook). Bind to
`127.0.0.1` and reach it through an SSH tunnel
(`ssh -L <port>:127.0.0.1:<port> <alias>`), never a publicly exposed port.
Make start idempotent (succeed if already running), define readiness as
answering a real request (not merely a live PID), and verify stop by confirming
the port is free. Secrets reach the service via
environment variables or tight-mode files, never argv (world-readable in
`ps`), and caches are never world-writable on a shared host. Run it under a
supervisor that survives logout: the scheduler, a `systemctl --user` unit,
or a tmux session named after the service.

**Sudo/admin.** Follow the authorization rules in Orient: default to
user-space even when sudo works, and reserve sudo for tasks that genuinely
require it (drivers, system packages, ports below 1024).
