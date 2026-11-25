---
name: docker-space-optimizer
description: "Trigger: docker ocupa mucho, liberar espacio docker, build cache, prune, docker disk usage. Diagnose and reclaim Kiri Docker space safely."
metadata:
  author: "alvaroofernaandez"
  version: "2.0"
---

## Activation Contract

Load when Docker images, build cache, volumes or Kiri's disk use too much space, after large builds, or when free space on `/` is low.

## Hard Rules

- Kiri is the only runtime. Act only when `docker context show` is `kiri`; refuse any other context (the script exits non-zero).
- Measure BEFORE and AFTER, and report the difference.
- Safe cleanup needs no confirmation: `docker container prune -f`, `docker image prune -f`, `docker builder prune -af`, `docker buildx prune --builder multiarch -af`.
- Destructive cleanup (`docker system prune -af --volumes`, `docker volume rm/prune`, `docker image prune -a`, `docker rmi`) runs ONLY after listing exactly what will be removed, with sizes, and getting explicit approval.
- Measure Kiri's real usage with `du -sh ~/Library/Application\ Support/Kiri` before and after, and report the measured number.
- Kiri's `vm/data.img` does NOT shrink by itself after deletes. `aval docker cleanup` ends with `fstrim` on the VM's ext4 through a throwaway volume (`kiri-fstrim-probe`), which returns freed blocks to macOS (verified 2026-11-19: 49.4 → 25.2 GB real). Never mount `/dev/vda` directly. Report the measured `du -h vm/data.img` before/after, never an assumed number.
- Manual trim without pruning: `docker volume create kiri-fstrim-probe && docker run --rm --privileged -v kiri-fstrim-probe:/v alpine:3 fstrim -v /v; docker volume rm kiri-fstrim-probe`.

## Decision Gates

| Finding | Action |
|---|---|
| Build cache large | Safe cleanup (script) |
| Dangling images / stopped containers | Safe cleanup (script) |
| Unused tagged images | List `repo:tag`, size, age → ask |
| Unused volumes | List name, size, owning compose project → ask; never prune DB volumes silently |
| Context ≠ kiri | Stop; load `kiri-health` |

## Execution Steps

1. Diagnose: `df -h /`, `docker system df`, `docker system df -v`, `du -sh ~/Library/Application\ Support/Kiri`.
2. Run `aval docker cleanup` (add `--dry-run` to only list the commands; checks context, safe prunes incl. the `multiarch` builder cache, before/after report).
3. If more space is needed, present destructive candidates as a table and wait for approval.
4. Re-measure with step 1 commands.

## Output Contract

Return a table: free space on `/` before/after, Kiri data size before/after (measured), total reclaimed, what was removed, what was kept and why.

## References

- `aval docker cleanup` — safe cleanup with before/after report.
