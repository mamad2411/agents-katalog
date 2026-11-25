---
name: hpc-cluster-runs
description: "Running long jobs and heavy work on shared machines and clusters: what counts as heavy on a control node (including package tests, checks, source builds and data probes), launching runs that survive IDE memory kills (systemd-run, not screen or nohup), stopping a run and reaping what it leaves behind, keeping node checkouts in sync, sizing parallel workers against memory, and never touching a process you did not start."
when_to_use: Launching a long or multi-day run; stopping one; syncing code or packages across cluster nodes; a run is stuck or orphaned; deciding where to execute something on a shared machine; sizing parallel workers for a node.
paths:
  - "**/_hosts.R"
  - "**/_hosts.R.example"
  - "**/scripts/**"
---

# Long runs on shared machines

## Where work runs

The control node schedules work and hosts the user's interactive session. **Do not
run heavy work on it.** This is the most repeated correction in the session record
-- dozens of turns, several in capitals -- and the incidents behind it include
multi-day runs killed mid-flight and the user's IDE killed along with every session
inside it.

"Heavy" is broader than it looks. Each of these has taken a control node down:

- running a pipeline, a simulation or a model engine on real inputs, and renders
  (`quarto render`, `rmarkdown::render`);
- **package work**: `devtools::test()`, `devtools::check()`, `R CMD check`, source
  builds from `renv::install` or `pak`;
- **data probing**: an unfiltered `sf::st_read()` of a multi-GB layer, `fread()` of a
  large CSV, a full-table `ogrinfo` scan, `terra::rasterize()`, concurrent large
  downloads -- "just a quick look" at a new data source is not exempt;
- ad-hoc scratch scripts. One line with the wrong units in a probe
  (`terra::densify(..., flat = FALSE)` on lon/lat reads the interval in metres)
  built 30 million vertices and peaked at 27 GB.

Light orchestration is fine on the control node: git, status queries against a
pipeline's metadata, reading small results, and the node-sync script. When in doubt,
it is heavy.

**Preflight before the first heavy thing in a session:**

```sh
hostname -s                                         # where am I? sessions open on any node
free -g
ps -eo pid,rss,etime,cmd --sort=-rss | head         # what is already resident?
```

Detect the role by capability, not by hostname string:

```r
if (file.exists("_hosts.R")) { ... }   ## robust to the cluster being renamed
```

Set `controllerHosts` in `.claude/r-project-policy.json` and the guard in this
plugin will refuse heavy commands there.

**Dispatch instead.** Home directories are often local per node, so a compute node
has its own clone: bring it up to date, or stage the working tree on shared storage,
then run the work there:

```sh
ssh <compute-node> 'bash -s' < _tmp/job.sh
```

**If something genuinely must run on the control node, cap it**, so a runaway dies
alone instead of taking the IDE with it:

```sh
systemd-run --user --scope -p MemoryMax=4G -p MemorySwapMax=0 Rscript-4.6.1 -e '...'
```

## Why `nohup`, `setsid` and `screen` do not protect a run

`systemd-oomd` kills **cgroups**, not process trees. Anything launched from an IDE
terminal or from an agent's shell lives in the IDE's cgroup scope, and `nohup`,
`setsid`, `disown` and `screen` only detach it from the terminal -- they do not move
it out of that scope. When memory pressure crosses the threshold, oomd kills the
whole scope: the user's R sessions, every agent session, and every "detached" run
launched from them. In one incident a 5-day calibration died this way while a
sibling run survived, because only the survivor had been launched into its own unit.

Check where a process lives:

```sh
sed 's|.*/||' /proc/<pid>/cgroup     # must NOT be the IDE's app-*.scope
```

Agent background tasks die with the IDE too, so they cannot be the durable monitor
for a multi-day run. Use a systemd user timer for anything that must outlive the
session.

## Never touch a process you did not start

These are shared machines and several projects run on them at once. An agent once
killed another project's multi-day calibration, and a separate "cleanup" in one
project killed a sibling project's run with a global `docker rm -f $(docker ps -aq)`.
Before signalling anything:

```sh
ps -o pid,user,lstart,etime,cmd -p <pid>
docker ps --format '{{.ID}}\t{{.Names}}\t{{.Status}}'
```

If it is not yours, report it and stop. Scope any cleanup to your own project's
containers by name or pool id. The `SessionStart` hook lists what was already
running when your session began, precisely so you can tell the difference.

## Launching a long run

```sh
pgrep -af "<the project's long-run patterns>"   ## preflight: is anything already running?
systemd-run --user --unit=<name> --collect \
  --working-directory="$PWD" bash _tmp/run_<name>.sh
systemctl --user status <name>
journalctl --user -u <name> -f        ## or tail the log the wrapper writes
```

The wrapper frames the run so the log is self-describing:

```bash
{ echo "=== <name> launch $(date -Is) ==="
  Rscript-4.6.1 scripts/run_<name>.R
  echo "=== EXIT=$? $(date -Is) ==="
} > "$LOG" 2>&1
```

Use `screen` only when you need to attach interactively, and launch the screen
itself through `systemd-run --user` if the run must survive memory pressure.

**Rename the log with a failure suffix when a run dies** -- it makes the failure
mode greppable months later: `.died_79of80`, `.oom-9gib`, `.gen5_prereboot`.

## Stopping a run

**Launched as a systemd unit:** `systemctl --user stop <name>` signals every process
in the unit's cgroup, including child R processes. Confirm nothing survived:

```sh
ps -u "$USER" -o pid,etime,cmd | grep -E 'exec/R' | grep -v grep
```

**Launched under `screen`:** ending the screen does not necessarily stop the run. A
child R process started by the run (through `callr`, or a worker pool) does not
receive SIGHUP, survives, and keeps whatever lock or file handle it held.

```sh
## 1. kill any retry loop FIRST, or it treats the dead R process as a crash
##    and relaunches everything
## 2. end the screen
screen -X -S <name> quit
## 3. find and kill the surviving child R processes -- yours only
ps -u "$USER" -o pid,etime,cmd | grep -E 'exec/R' | grep -v grep
kill -TERM <pid>
```

**Either way, then reap containers on every compute host** the run used. Neither SSH
nor a worker scheduler reaps a worker's container children, and orphaned
per-container workers **restart** their containers. Kill the workers before the
containers, or `docker stop` is whack-a-mole. Rebooting the control node has the
same effect as killing the controller: remote workers keep running with nothing to
report to.

## Keeping nodes in sync

The most common cluster footgun is mismatched code across nodes.

```sh
## 1. locally
git add <paths> && git commit && git push
## 2. on EACH worker node
ssh nodeN 'cd <project> && git pull && git submodule update --init --recursive'
## 3. only if the lockfile changed
ssh nodeN 'cd <project> && Rscript-4.6.1 -e "renv::restore(prompt = FALSE)"'
```

Three constraints worth automating into a `sync-nodes.R`:

- **Worker checkouts must stay clean.** A dirty tree blocks the `git merge --ff-only`
  that the sync relies on, so nothing a run does on a worker may write a git-tracked
  path.
- **Group hosts by OS codename and warm one per group first.** The package cache is
  keyed by codename, so parallel cold restores across nodes sharing a network cache
  cause redundant compilation and cache contention.
- **Check version *and* commit.** A node reporting the right package version can
  still be on a different commit; compare the recorded SHA against the lockfile, not
  just the version string.

**Never sync or install while a run of the same project is live** -- it swaps the
library out from under the active workers, and a lazy-load failure surfaces hours into
a job with an error pointing at the package rather than the cause. A hook in this
plugin blocks this. A run in another project loads its own renv library and is not at
risk, except from `renv::purge()` and `renv::rebuild()`, which delete or replace shared
cache entries in place; for those, and for installs into a repo without renv, the hook
checks runs in every project. If the renv cache is shared between machines, note the
asymmetry: **installing** on one machine only writes a new cache entry, which is safe
for the others; the dangerous step is the **restore** that re-points a library. To
prepare an updated library while a run is live, stage it in a second clone with
`renv::isolate()` or `options(renv.config.cache.symlinks = FALSE)`.

## Know what is shared between machines

Check rather than assume, with `ls -ld` and `df`. A common layout: home directories --
code, the renv library, sometimes run state -- are **local disk on every host**, and only
data directories are shared network mounts. Two consequences:

- **Code reaches a host only through commit, push, pull.** Editing locally and launching
  elsewhere silently runs the old code.
- **A result file written to a host-local directory exists on one machine.** Shared
  state that records its path is then wrong on every other host. If such a file must be
  regenerated elsewhere, make the write **deterministic** -- byte-identical on every
  host -- by checking it for embedded timestamps, absolute paths and process IDs.

## Sizing parallel workers

- **Memory settings are per process.** A `terra` memory fraction applies to each
  worker, so N workers can collectively exceed RAM. Cap it at
  `memfrac * node_RAM / n_workers`.
- Some backends need hard caps for reasons unrelated to RAM -- a Java-backed
  service capped at 6 workers because more caused socket errors, and it must be
  process-based rather than forked because forking corrupts its sockets.

## Do not co-run two heavy projects on the same nodes

Documented after a control node hard-locked doing exactly that, and again after
four compute nodes went down in one night. The second mechanism is worth knowing:
two projects declared identical per-node worker caps sized for light workers, and a
report-render stage whose workers each needed 75-130 GB fanned out across them.
Worker caps must be sized to the heaviest stage that will use the pool, and a node
running one project's long calibration must be kept out of every other project's
pool. Check what is already running before launching, and say what you found.
