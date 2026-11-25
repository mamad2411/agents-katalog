---
name: kiri-health
description: "Trigger: docker no funciona, revisa kiri, health check docker, kiri setup, docker context, builder multiarch, restos de orbstack/colima. Diagnose Kiri, Docker context, daemon, builders and leftover runtimes."
metadata:
  author: "alvaroofernaandez"
  version: "2.0"
---

## Activation Contract

Load when Docker fails, the user asks for a Docker/Kiri health check, a build produces the wrong architecture, or there is any suspicion of a second runtime (OrbStack, Colima, Lima, Docker Desktop) on the machine.

## Hard Rules

- Read-only by default: diagnose and report; change nothing without approval, except the recovery commands below once the user agrees.
- Never touch Docker state while diagnosing: no prune, rm, or context changes.
- If OrbStack/Colima/Lima traces are found, NEVER remove them automatically: show the exact removal plan (commands, paths, sizes) and wait for confirmation.
- A sleeping VM (idle > 60 s) is normal; it wakes in ~0.15 s on the next command.
- Report only measured values; a check that was not run is reported as "not run".

## Decision Gates

| Check | Healthy | Recommended action if not |
|---|---|---|
| `docker context show` | `kiri` | `docker context use kiri`; if absent, `kiri setup` |
| `echo $DOCKER_HOST` | empty | remove it from shell rc files (ask) |
| `ls -l ~/.kiri/run/docker.sock /var/run/docker.sock` | socket exists, `/var/run` links to it | `kiri setup` |
| `ls /Library/LaunchDaemons \| rg com.docker` | nothing | Docker Desktop's `com.docker.socket` helper re-links `/var/run/docker.sock` to the dead `~/.docker/run/docker.sock` on every boot, and Kiri's `dev.kiri.docker-socket` only links when the path is absent, so Docker's wins. With the user's sudo: `launchctl bootout system/com.docker.socket`, remove `/Library/LaunchDaemons/com.docker.{socket,vmnetd}.plist` and `/Library/PrivilegedHelperTools/com.docker.*`, then `ln -sfn ~/.kiri/run/docker.sock /var/run/docker.sock` |
| `launchctl list \| rg dev.kiri.daemon` | listed | `kiri setup` (re-creates the agent) |
| `docker info` | succeeds | `kiri diag logs --errors`, then `kiri setup` |
| `kiri diag logs -n 50 --errors` | no recent errors | quote the errors; `kiri diag report` for a bundle |
| `docker buildx ls` | builder `multiarch` present | `docker buildx create --name multiarch --driver docker-container --driver-opt default-load=true --bootstrap kiri` |
| `echo $BUILDX_BUILDER` | `multiarch` | export it in `~/.zprofile` / `~/.zshrc` |
| `command -v kiri` | resolves (`~/.kiri/bin`) | add `~/.kiri/bin` to PATH |
| `command -v colima limactl`, `ls -d /Applications/OrbStack.app` | none | removal plan (ask) |
| OrbStack.app, `~/.orbstack`, `~/.colima`, `~/.lima`, login items | absent | removal plan with `du -sh` sizes (ask) |
| Contexts other than `kiri`/`default` in `docker context ls` | absent | `docker context rm <name>` (ask) |
| `df -h /` free | > 20 GiB | load `docker-space-optimizer` |
| `du -sh ~/Library/Application\ Support/Kiri` | measured and reported | load `docker-space-optimizer` if large |

## Execution Steps

1. Run: `docker context ls`, `docker context show`, `docker info`, `docker buildx ls`, `docker system df`, `kiri --version`, `df -h /`.
2. Run: `ls -l ~/.kiri/run/docker.sock /var/run/docker.sock`, `launchctl list | rg dev.kiri`, `kiri diag logs -n 50 --errors`.
3. Run: `ps aux | rg -i 'colima|lima|orbstack' | rg -v ' rg '`, `command -v colima limactl`, `ls -d /Applications/OrbStack.app`, `rg -n -i 'colima|orbstack|DOCKER_HOST|BUILDX_BUILDER' ~/.zshrc ~/.zprofile ~/.bashrc ~/.profile`.
4. Evaluate every row of the decision table.
5. Recovery, only after approval: `kiri setup` (re-creates context, agent and builder; `kiri setup --uninstall` removes them), then recreate `multiarch` if missing, then prove it with `docker run --rm hello-world` and a native vs `--platform linux/amd64` build checked with `docker image inspect -f '{{.Architecture}}'`.

## Output Contract

Return one table: Check | Status (OK / WARN / FAIL / not run) | Measured value | Recommended action. Then, if any OrbStack/Colima trace exists, the removal plan awaiting confirmation.

## References

- `../kiri-docker/SKILL.md` — daily use and the multiarch build rule.
- `../docker-space-optimizer/SKILL.md` — when space checks fail.
