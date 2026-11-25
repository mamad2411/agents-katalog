---
name: containers
description: >-
  Container runtime toolkit, one skill with sub-skills per runtime. (1) podman: reclaim Podman disk
  space on Windows, macOS and Linux (prune unused images, fstrim inside the Podman machine, and on
  Windows compact the WSL ext4.vhdx with diskpart so the space returns to the host). Use WHENEVER
  the work is "podman storage too big", a Podman machine disk or ext4.vhdx that keeps growing, a
  drive filling up with container images, "prune / clean up / shrink / compact podman", or "ดิสก์เต็ม
  เพราะ podman". Read the sub-skill's SKILL.md before acting.
---

# containers: sub-skills

| When the work is… | Read | Scripts |
|---|---|---|
| "podman storage too big", "ext4.vhdx keeps growing", "prune / compact podman", "drive full of images" | [`podman/SKILL.md`](podman/SKILL.md) | `podman/scripts/reclaim.py` (stdlib, `--dry-run`) |

## Rules every sub-skill keeps

- **Measure before and after.** Report the runtime's own numbers (`podman system df`, the host file
  size), never an estimate.
- **Nothing is deleted without a yes.** Show the dry run first. Stopped containers and volumes are
  removed only when the user asks; removing volumes can lose data.
- **Say what else stops.** A step that shuts down WSL stops every distro, not just this runtime.

## Tests

```bash
cd skills/containers && python -m pytest -q     # needs: pytest
python podman/scripts/reclaim.py --help > /dev/null
```
