---
name: design-log
description: The _tmp/ working-log convention that lets multi-day, multi-session agent work survive context loss and concurrent sessions -- HANDOFF_*.md, PLAN_*.md, dated session-state sections, "Uncommitted (mine)" vs another session's files, and failure-annotated log names. Use when starting long or multi-session work, handing off, or resuming a task from a previous session.
when_to_use: Beginning a multi-step task expected to span sessions; resuming work described in a prior session; another Claude session is working in the same repo; writing a plan or handoff document; naming a long-run log file.
---

# Working logs for long, multi-session work

These projects survive months of multi-session agent work on this convention. The
artifacts live in gitignored `_tmp/`, or tracked at the repo root when the design
decision is itself a deliverable.

## File naming

| Pattern | Contents |
| --- | --- |
| `_tmp/PLAN_<topic>.md` | the plan before work starts |
| `_tmp/HANDOFF_<topic>.md` | what the next session needs to pick this up |
| `_tmp/ISSUE_<topic>.md` | a defect being investigated |
| `_tmp/REPLY_DRAFT_<topic>.md` | drafted correspondence, for human review |
| `_tmp/verify_*.R`, `smoke_*.R`, `probe_*.R`, `diag_*.R` | throwaway checking scripts, by purpose |
| `_tmp/run_*.sh` | long-run launcher wrappers |

Gitignored by `_tmp*`. `_TODO.md` at the root is a gitignored registry reconciled
against inline `## TODO:` markers.

## Section structure inside a working log

Dated sections, newest last. Each session appends rather than rewrites:

```markdown
## 2026-08-28

### Session state (pick up here)
<the one paragraph a fresh session needs before doing anything>

### Uncommitted (mine)
- R/targets_fire.R  -- severity threshold fix, verified, ready to commit
Other files in the tree belong to the concurrent session.

### Watch
- calibration gen 12/40, log at _tmp/recalibration_canlabs.log
```

**"Uncommitted (mine)" is the load-bearing part.** These repos regularly have two
agent sessions in one worktree. Without it, one session stages another's
half-finished work -- which is exactly how a bad submodule pointer once broke every
node on a cluster.
Before staging anything, check this section; if it does not exist and the tree is
dirty in ways you did not cause, ask rather than assume.

## Record the dead ends, not just the outcome

The single most valuable habit in this corpus. When a hypothesis is falsified,
write the measurement down **next to the setting** and in the working log:

> The parameter is now set explicitly to TRUE with the measurement recorded beside
> it, rather than reverted silently, so the dead end is not retried.

A revert that leaves no trace will be re-proposed by the next session -- possibly
by you.

Also record false alarms. One commit exists purely to correct an AI-flagged hazard
that, on checking, did not exist -- kept *"so the false alarm isn't re-raised."*

## Long runs

Launch through `systemd-run --user`, with a wrapper that frames the log, and check
nothing else is running first -- `hpc-cluster-runs` has the pattern. The working log
records the unit name and the log path under "Watch".

**Rename the log with a failure suffix when a run dies** -- the existing
convention makes the failure mode greppable months later:

```
calibration_severity.log.died_79of80
recalibration_yflip.oom-9gib.log
calibration_fwi.log.gen5_prereboot
```

## Watchdogs

`_tmp/watchdog.sh` is written to be *"Caught by a Monitor on this log"* -- i.e.
the log line format is chosen so a Claude Code `Monitor` can wake a session on it.
When you write a watchdog, emit a single greppable marker line on the condition
you want to be woken for.
