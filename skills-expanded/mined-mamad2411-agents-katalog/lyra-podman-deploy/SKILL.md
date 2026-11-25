---
name: lyra-podman-deploy
description: "Running and deploying containers with Podman: rootless operation, quadlet systemd units, health-gated startup, auto-update with rollback, pods, networking (pasta), SELinux-aware volumes, file-mounted secrets, and resource limits. Use when deploying services with podman, writing quadlet/.container files, setting up auto-updating containers, or debugging rootless networking, volumes, or startup ordering."
compatibility: "Requires podman 5.x on a systemd Linux host (quadlets, pasta, sdnotify=healthy). Optional: podman-compose or docker compose against the podman socket for dev. Composes with lyra-podman-images, lyra-ci-cd-automation, lyra-security-containers, lyra-security-secrets. Version policy: examples target the latest stable release of every tool; minimum supported is the newest LTS (or last maintained major), and features newer than the minimum are flagged inline."
---

# lyra-podman-deploy

## What it does

Turns built images into supervised production services using what the host already has: systemd. The deployment unit is the **quadlet** — a declarative `.container`/`.pod`/`.volume`/`.network` file that systemd turns into a managed service with dependency ordering, restart policy, journald logging, and boot startup. Rootless by default, health-gated startup, and image-digest-based rollback. No orchestrator to operate for the 95% of deployments that are "run these services on this box, reliably."

## The rules

### 1. Rootless by default — know the three things that change

Containers run in your user namespace: (a) UID 0 in the container maps to your user via `/etc/subuid`/`/etc/subgid`, (b) privileged ports need `sysctl net.ipv4.ip_unprivileged_port_start=80` (or a reverse proxy / systemd socket activation), (c) user services die at logout unless `loginctl enable-linger <user>`. Reach for rootful only when a specific feature demands it, and say why in the unit file.

### 2. Quadlets are the deployment unit — not `podman run` in a shell script

A `.container` file in `~/.config/containers/systemd/` (user) or `/etc/containers/systemd/` (system) generates a full systemd service at daemon-reload — and the same mechanism covers `.pod`, `.volume`, `.network`, `.build` (build an image from a Containerfile on the host), and `.kube` (run a k8s YAML) units, so the whole stack can be declarative. `podman generate systemd` is deprecated; docker-compose-style YAML is for dev. Minimal production unit:

```ini
# app.container
[Unit]
Description=API server
Wants=network-online.target
After=network-online.target

[Container]
# channel tag + AutoUpdate (pull-based deploys) — or pin @sha256 and drop
# AutoUpdate for CI-driven deploys; never both in one unit (a pinned digest can't update)
Image=ghcr.io/org/app:prod
AutoUpdate=registry
# default name would be systemd-app; DNS registers container names (rule 6)
ContainerName=app
PublishPort=127.0.0.1:3000:3000
Environment=NODE_ENV=production
# create before first start: printf '%s' '...' | podman secret create app-db-url -  (rule 8)
Secret=app-db-url,type=mount
HealthCmd=/app/healthcheck
HealthOnFailure=kill
Notify=healthy

[Service]
Restart=always
# pull + startup + health ramp all count against this when Notify=healthy
TimeoutStartSec=900

[Install]
WantedBy=default.target
```

`systemctl --user daemon-reload && systemctl --user start app` — logs in journald, starts at boot (with linger), restarts on failure. More patterns (pods, networks, volumes, dependencies) in [quadlet-patterns.md](./references/quadlet-patterns.md).

### 3. Health is part of the contract, declared at runtime

OCI images don't carry HEALTHCHECK (see lyra-podman-images rule 12) — declare it here: `HealthCmd=` plus `HealthOnFailure=kill` (systemd restarts it), and `Notify=healthy` so systemd only reports the unit started once the container is actually healthy — which makes `After=`/`Wants=` dependency ordering *mean something*. Use startup probes (`HealthStartupCmd=`) for slow-booting services instead of stretching the regular interval.

### 4. Auto-update with rollback: deployment as a pull

`AutoUpdate=registry` on a mutable *channel* tag (`:prod`) + the `podman-auto-update.timer` gives pull-based deploys: push a new image to the registry, the timer pulls it, restarts the unit, and — the part people miss — **rolls back to the previous image if the updated unit fails to start healthy**. With `Notify=healthy`, "fails" includes "never became healthy". CI pushes; hosts converge; failed updates self-revert. For push-style deploys instead, pin `Image=` by digest and let CI rewrite the unit + restart (see lyra-ci-cd-automation) — pick one model **per unit**, never both in the same unit (a digest-pinned image has nothing to auto-update); a host may legitimately run channel-tag services next to CI-pinned ones. Restarts drop traffic for the restart window; where that matters, systemd **socket activation** holds the listening socket open across container restarts and queues connections instead of refusing them (worked example in [quadlet-patterns.md](./references/quadlet-patterns.md)).

### 5. Roll back by digest, keep history

Tags move; digests don't. Deploy digests, keep the last N images (`podman image prune` with care, not `--all`), and rollback is: previous digest into the unit, restart. If you deploy by mutable tag you have no rollback, only "pull whatever is there now".

### 6. Pods for co-located services, networks for isolation

Containers in a pod share a network namespace — an app and its sidecar talk over `localhost`, declared with a `.pod` quadlet plus `Pod=` in each `.container`. Everything else joins explicit named networks (`.network` quadlets); containers on the same network resolve each other by name via DNS. (Rootless traffic to the outside runs through **pasta**, podman 5's default user-mode network backend — the name to know when debugging what an address actually binds to.) Publish to the host only what the outside needs, bound to `127.0.0.1` behind a reverse proxy unless it's the proxy itself. Never `--network=host` for convenience.

### 7. Volumes: named, labeled, backed up

Named volumes (`.volume` quadlets) over bind mounts for data; bind mounts for config. On SELinux hosts use `:Z` (private) or `:z` (shared) instead of disabling labels, and `:U` to chown into the container's user namespace. A volume that isn't in a backup job doesn't exist — `podman volume export` or mount-and-archive on a timer.

### 8. Secrets are files, not environment variables

`podman secret create app-db-url -` then `Secret=app-db-url,type=mount` — the app reads `/run/secrets/app-db-url`. Environment variables leak: `podman inspect`, `/proc/<pid>/environ`, child processes, crash dumps. `type=env` exists for legacy apps; treat it as the compatibility fallback, not the default. Rotation = new secret version + restart unit.

### 9. Resource limits on every production unit

`MemoryMax=` / `CPUQuota=` (systemd-level, preferred in quadlets) or `PodmanArgs=--memory=512m --pids-limit=256`. A container without limits is a noisy neighbor with root-cause potential — memory leaks become OOM kills of *other* services. Limits also make capacity planning honest.

### 10. Logs go to journald; debug with the unit, not the container

Rootless quadlet services log to the user journal: `journalctl --user -u app -f`. Startup failures: `systemctl --user status app` shows the generated command; `podman ps -a` shows the container state; `/usr/lib/systemd/system-generators/podman-system-generator --user --dryrun` shows what the quadlet actually generated — the first tool to reach for when a unit doesn't appear.

Someone must *own* the health signal, because three control loops consume it (restart-on-failure here, auto-update rollback in rule 4, deploy verification in lyra-ci-cd-automation rule 8). Minimum viable ownership on a quadlet host: `HealthOnFailure=` + `Restart=` handle the automatic reactions; `OnFailure=notify@%n.service` (a unit that emails/pings on failure) makes a human aware; `podman events --filter event=health_status` feeds anything external. If nothing watches, "rollback on health-check failure" is a sentence, not a control.

### 11. Compose is for dev; the socket bridges Docker tooling

`docker compose` (or podman-compose) works against `systemctl --user enable --now podman.socket` with `DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock` — fine for local dev parity. Production stays quadlets: supervised, ordered, health-gated, auto-updating. If you need multi-node scheduling, that's Kubernetes — `podman kube play` runs k8s YAML single-node and `podman kube generate` eases the migration path.

---

_Part of the [skill collection](../README.md)._
