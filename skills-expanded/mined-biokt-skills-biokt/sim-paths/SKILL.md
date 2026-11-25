---
name: sim-paths
description: Validate that simulation files exist on a target machine before launching.
  Use before submitting jobs to rubisco, villin, insulin, calmodulin, agamede, or
  hyperion to catch missing paths early. Spawns a context-free subagent so the check
  does not inherit the current session's token budget.
---

# sim-paths — Simulation Path Validator

## When to invoke

- User says "validate files", "check paths", "verify before launching", or similar.
- After preparing a simulation (gmx-prep, plumed-us, etc.) and before the first job submission.
- Any time a simulation has failed with file-not-found errors and you want to pre-check a revised set.

## How it works

Spawn a `general-purpose` subagent via the `Agent` tool, passing the machine name and
file list **inline in the prompt**. The subagent has no knowledge of the current session;
it only knows what is in that prompt. It SSHes to the target machine, checks each path,
and returns a structured report.

## Step 1 — collect inputs

From the current session, identify:
- **machine**: one of `rubisco`, `villin`, `insulin`, `calmodulin`, `agamede`, `hyperion`
- **files**: the list of absolute paths that must exist on that machine before the job can run

Typical files for a GROMACS run:
- Coordinate file (`.gro`)
- Topology (`.top`) and any included `.itp` files
- MDP parameter files (`.mdp`)
- PLUMED input (`.dat`) if applicable
- SLURM submission script (`.sh`)
- Index file (`.ndx`) if referenced

If the user has not specified paths explicitly, infer them from the simulation setup
that was just prepared (look at the scripts, mdp files, and topology for referenced paths).

## Step 2 — spawn the subagent

Call the Agent tool with `subagent_type="general-purpose"` and the prompt below,
substituting `{machine}` and the file list:

```
You are a file existence checker. Your only task is to verify that a list of files
exists on a remote machine. Do not do anything else.

Machine: {machine}
Files to check:
{- /absolute/path/to/file1}
{- /absolute/path/to/file2}
{...}

For each path, run exactly this command:
  ssh -o BatchMode=yes -o ConnectTimeout=5 {machine} "test -e '/absolute/path' && echo OK || echo MISSING"

If the SSH connection times out or is refused for any path, mark ALL remaining files
as UNREACHABLE and stop checking.

Warn if any path is relative (does not start with /).

Output your report in exactly this format and nothing else:

MACHINE: {machine}
STATUS: PASS | FAIL | ERROR
- OK: /path
- MISSING: /path
- UNREACHABLE: /path  (only if SSH failed)
```

## Step 3 — interpret and act

| STATUS | Meaning | Action |
|--------|---------|--------|
| `PASS` | Every file found | Proceed with job submission |
| `FAIL` | One or more files missing | Report the MISSING paths to the user; do not submit |
| `ERROR` | SSH failed (host unreachable, key issue) | Report connectivity problem; check VPN / SSH config |

If STATUS is FAIL, suggest likely causes (wrong base directory, file not yet copied,
path uses Mac-style `/Users/` instead of Linux `/home/`).
