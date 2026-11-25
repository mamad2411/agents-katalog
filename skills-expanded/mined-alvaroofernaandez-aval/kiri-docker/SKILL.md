---
name: kiri-docker
description: "Trigger: docker, docker compose, buildx, contenedor, imagen, levantar servicios, docker run/exec, kiri, dominio .kiri.local, k8s local, kiri share. Run all Docker work against Kiri, the only runtime."
metadata:
  author: "alvaroofernaandez"
  version: "2.0"
---

## Activation Contract

Load for any Docker task on this Mac: running or building images, containers, Compose stacks, Buildx, `docker exec`, logs, local domains, Kubernetes, sharing a port, or repairing the Docker environment.

## Hard Rules

- Kiri (0.2.x, beta) is the ONLY permitted runtime. Never use, install or recommend OrbStack, Colima, Lima, Docker Desktop or Podman.
- Check `docker context show` before operating; it must be `kiri` (socket `~/.kiri/run/docker.sock`; `/var/run/docker.sock` links to it). If not, run `docker context use kiri`, and if the context is missing, load `kiri-health`.
- Never set `DOCKER_HOST`; the context is the single source of truth.
- BUILDS: always run with `BUILDX_BUILDER=multiarch` (exported in `~/.zprofile` and `~/.zshrc`). Kiri's own builder `kiri` resolves docker.io/quay.io through a mirror of its single-arch local store, so `--platform linux/amd64` silently yields an ARM64 image when the base exists locally (warning `InvalidBaseImagePlatform`). Never build deploy images on the `kiri` builder.
- Verify every image you will push or deploy as amd64: `docker image inspect -f '{{.Architecture}}' <image>` must print `amd64`.
- `buildx build --add-host x:host-gateway` fails on docker-container builders; use `198.19.248.254` (host gateway on this Mac).
- Stopping containers is safe; `docker compose down -v`, `docker rm -v` or deleting volumes needs explicit confirmation.
- Kubernetes stays stopped unless the user asks (`kiri k8s start`).
- Never run `kiri ui` (not even `--help`) unasked: it opens the window and the window installs pending Kiri updates.
- Slow builds, `compose up` with long boot, image pushes: run them in a Herdr terminal (`hc run --bg --name <x> -- zsh -ic '<cmd>'`, see `herdr`) so you stay reachable.
- The VM sleeps after 60 s idle and wakes in ~0.15 s: a sleeping VM is normal, not a fault.

## Decision Gates

| Situation | Command |
|---|---|
| Start a stack | `docker compose up -d` (add `--build` after code changes) |
| Stop a stack, keep data | `docker compose down` |
| Build for this Mac | `docker build -t <app>:local .` (builder `multiarch`, native arm64) |
| Build amd64 for deploy | `docker build --platform linux/amd64 -t <app>:<tag> .` then verify `Architecture` |
| Run an amd64 image | `docker run --platform linux/amd64 ...` (Rosetta) |
| Docker not answering, wrong context, `multiarch` builder missing | `aval kiri up` (idempotent; creates the builder with a bounded BuildKit cache, 20 GB max) |
| Local domain for a container | `http(s)://<container>.kiri.local`; compose: `<service>.<project>.kiri.local`; custom: label `dev.kiri.domain=api.myapp`; `*.kiri.localhost` needs no setup |
| Reach the host from a container | `host.docker.internal` (gateway IP `198.19.248.254`) |
| Public link to a port/container | `kiri share <PORT\|CONTAINER>` (exposes it publicly: confirm first) |
| Local Kubernetes | `kiri k8s start\|stop\|status\|delete` (k3s, kubectl context `kiri`) |
| Linux machine | `kiri machine create NAME --distro ubuntu` |
| Import from another runtime | `kiri import [orbstack\|desktop-linux] [--list]` (imports ALL images, not selective) |
| Shell into a container | `docker exec -it <name> sh` |
| VM resources | `~/.kiri/vm.json` `{"cpus": 6, "memory_mib": 8192}` (this Mac: M4, 10 cores, 16 GB); CPUs are only used while containers are busy; applied on next VM start (`launchctl kickstart -k gui/$(id -u)/dev.kiri.daemon`, stops running containers: ask first) |
| Update Kiri | `kiri update --check` |
| Docker misbehaves | `kiri-health` |
| Low disk space | `docker-space-optimizer` |

## Execution Steps

1. Run `aval kiri up` (starts Kiri if needed, fixes the context and builder, flags a foreign `/var/run/docker.sock`).
2. For builds, `echo $BUILDX_BUILDER` → must be `multiarch`; export it for the session if empty.
3. Run the task with `docker`, `docker compose` or `docker buildx`.
4. For deploy images, run the amd64 verification before pushing.
5. After configuring or repairing the environment, prove it with `docker run --rm hello-world`.

## Output Contract

Return the commands run, their relevant output, the active context and builder, the verified image architecture when a build was involved, and the state of affected containers (`docker compose ps` or `docker ps`).

## References

- `../kiri-health/SKILL.md` — diagnosis and recovery.
- `../docker-build-optimized/SKILL.md` — builds.
- `../docker-space-optimizer/SKILL.md` — disk space.
