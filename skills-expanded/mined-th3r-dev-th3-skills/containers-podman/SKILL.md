---
name: containers-podman
description: Use this skill when Podman eats too much disk on Windows, macOS, or Linux. Triggers include "podman storage too big", a Podman machine disk or ext4.vhdx that keeps growing, a drive filling up, too many container images, or any request to prune, clean up, shrink, or compact Podman. One cross-platform Python script prunes unused images (stopped containers and volumes only on request), runs fstrim inside the Podman machine, and on Windows compacts the WSL vhdx with diskpart so the space actually returns to the host. Pruning alone does NOT shrink a WSL vhdx; this skill handles every step.
---

# Podman: disk reclaim

`scripts/reclaim.py` uses only the Python standard library (3.9+). What it does depends on the OS:

| OS | Where Podman storage lives | Steps the script runs |
|---|---|---|
| Linux | Host filesystem, native Podman | prune |
| macOS | Podman machine, sparse raw disk | prune, `fstrim` in the machine |
| Windows | Podman machine, WSL2 `ext4.vhdx` | prune, `fstrim`, stop, `wsl --shutdown`, diskpart compact, start |

On Windows, the WSL vhdx grows but never shrinks. `podman system prune` frees space inside the VM, but the host file stays the same size until it is compacted.

## Workflow

### 1. Measure first (always)

```sh
python scripts/reclaim.py --dry-run
```

This prints `podman system df`, the vhdx size on the host (Windows only), and the planned steps. It changes nothing. Read the output:

- **The vhdx is much bigger than the in-use SIZE.** Compaction alone recovers most of the space. Suggest `--skip-prune` if the user wants to keep every image.
- **RECLAIMABLE is high on Images.** A default run is the right call.

### 2. Confirm before deleting

Pruning images is destructive. Public images are cheap to pull again, but locally built ones are not. Before a real run, show the user what will be removed and get a yes. Ask separately before using either of these flags:

- `--containers` removes **stopped** containers along with their writable layers. A stopped dev database is one example of what this deletes.
- `--volumes` removes volumes that no container references. If you combine it with `--containers`, it also removes the volumes of the containers that were just pruned. That is **data loss**.

### 3. Windows: run elevated

`diskpart` needs Administrator rights. If the current shell is not elevated, give the user the exact command to run in an Administrator terminal:

```powershell
python <repo>\skills\containers\podman\scripts\reclaim.py
```

Warn the user that the script calls `wsl --shutdown`. That **stops every WSL distro** (Ubuntu, Docker Desktop, and others), not just Podman. If they do not want that, `--skip-compact` prunes without admin rights, but the host file stays the same size.

### 4. Report

Report the before and after output of `podman system df`. On Windows, also report the final line: `VHDX on host: X GB -> Y GB (freed Z GB)`.

## Flags

| Flag | Effect |
|---|---|
| `--dry-run` | Show sizes and the plan, change nothing |
| `--skip-prune` | Reclaim only, delete nothing |
| `--skip-compact` | Prune only. No admin rights needed, no `wsl --shutdown` |
| `--containers` | Also prune stopped containers |
| `--volumes` | Also prune unused volumes |
| `--machine <name>` | Target a machine other than `podman-machine-default` |

## Notes

- **Do not** recreate the machine with a smaller `--disk-size` to save space. The disk size is a cap, not space that is already allocated.
- Windows support covers the WSL machine provider only. A Hyper-V provider machine fails with "WSL distro not found".
- On Windows Home, `Optimize-VHD` is missing because there is no Hyper-V module. `diskpart` ships with every edition, which is why the script uses it.
- Test: `python tests/test_reclaim.py` or `pytest tests`.
