---
name: podmaster
description: "End-to-end container expertise spanning OCI images, runtimes, and operations: image design, Dockerfile/Containerfile optimization, Docker Engine and Compose, Podman (rootless, pods, Quadlet), containerd and CRI, debugging, security hardening, and CI scanning. Use when building or reviewing container images, choosing Docker vs Podman, troubleshooting containers or pods, optimizing layers and cache, working with nerdctl/ctr, Kubernetes node runtimes, Containerfile, docker-compose, podman-compose, health checks, or when the user mentions containers, OCI, rootless, BuildKit, or image supply chain."
---

# Podmaster (container engineering)

Think in **OCI terms** first (image format, distribution, runtime bundle), then map to the concrete tool (Docker, Podman, containerd, Kubernetes).

## Reference files

| Topic | File | When to read |
| :--- | :--- | :--- |
| Docker Engine, Compose, Buildx | [reference/docker.md](reference/docker.md) | `docker` CLI, compose files, buildx, contexts |
| Podman | [reference/podman.md](reference/podman.md) | rootless, pods, Quadlet, `podman compose`, kube play |
| Dockerfile and Containerfile | [reference/dockerfile.md](reference/dockerfile.md) | multi-stage builds, layer cache, `.dockerignore`, hardening |
| containerd and CRI | [reference/containerd.md](reference/containerd.md) | `ctr`, `crictl`, `nerdctl`, snapshots, Kubernetes node runtime |
| Debugging | [reference/debugging.md](reference/debugging.md) | crash loops, networking, resources, exec, logs |
| Runtimes and CRI | [reference/runtimes-and-cri.md](reference/runtimes-and-cri.md) | runc/crun, shim, kubelet CRI flow, what to use when |

Read the relevant reference before giving version-specific flags or config paths. Prefer the user's installed version when commands differ.

## Mental model: what a "container" is

1. **Image** -- immutable artifact: manifest, config, and layers (tar blobs addressed by digest). The same image produces the same filesystem root on any OCI-compliant host.
2. **Container** -- an isolated process (or process tree) governed by:
   - **Namespaces** (PID, mount, network, UTS, IPC, user, cgroup) -- what it can see.
   - **cgroups** -- CPU, memory, IO, and PID limits.
   - **Capabilities** and **seccomp** -- which privileges and syscalls are allowed.
3. **Low-level runtime** (typically **runc** or **crun**) unpacks the OCI bundle and execs the init process inside those namespaces.
4. **Higher-level daemon** (Docker Engine, Podman, containerd) manages images, storage graphs, networking plugins, and the API surface you call.

Orchestrators (Kubernetes) talk to **containerd** (or CRI-O) via the **CRI**, not to Docker Engine directly.

## Principles (tool-agnostic)

### Images and supply chain

- **Pin bases** by digest or immutable tag for reproducibility; `latest` is for local experiments, not production.
- **Separate build and runtime** with multi-stage builds; ship only compiled artifacts and production dependencies.
- **Scan images** in CI (Trivy, Grype, or equivalent) and fail on policy for critical CVEs in shipped layers.
- **Do not bake secrets** into images; inject at runtime via env, files from an orchestrator, or a KMS.

### Process and filesystem

- **Run as non-root** when the workload allows; set `USER` after `COPY` with correct ownership.
- **Read-only root filesystem** where possible; use tmpfs or writable volumes only where the application requires.
- **Minimize packages** in the final stage; clean package caches in the **same** `RUN` layer as installs.

### Networking

- Prefer **explicit publish** (`-p`, `ports:`) over `--network host` unless host networking is genuinely required.
- Service discovery in orchestration is **DNS-based**; verify name resolution and whether headless vs cluster IP services are needed.

### Observability

- **One main process** per container when possible -- PID 1 owns signal handling and graceful shutdown.
- **Health checks** belong in the image (`HEALTHCHECK`) and in the orchestrator (`liveness`/`readiness`); align the endpoint with what "ready" actually means for the workload.

### Layer caching

- Order Dockerfile instructions from **least often changing** to **most often changing**.
- Copy **lockfiles** before application source; run install before `COPY .`.

## Workflows

### Design or review an image

1. Identify runtime vs build-time dependencies.
2. Choose a base image (slim, alpine, distroless) balancing size, libc compatibility, and security update cadence.
3. Sketch the multi-stage graph: builder, optional test stage, minimal runtime.
4. Add a non-root user, health check, and metadata labels (`org.opencontainers.image.*`).
5. Add `.dockerignore` / `.containerignore`.

See [reference/dockerfile.md](reference/dockerfile.md).

### Debug a failing container

1. Check `ps` or orchestrator events for exit code and restart policy.
2. Read logs (runtime and application).
3. `inspect` for env, mounts, network endpoints, and cgroup limits.
4. `exec` into a running container, or run a debug sidecar sharing namespaces.

See [reference/debugging.md](reference/debugging.md).

### Choose Docker vs Podman on a workstation

- Daemonless operation, rootless by default, pods without Kubernetes, or systemd unit generation: favor Podman. See [reference/podman.md](reference/podman.md).
- Docker Compose v2 ecosystem, BuildKit cloud builders, or scripts that assume `docker.sock`: favor Docker. See [reference/docker.md](reference/docker.md).

### Operate on a Kubernetes node

Node images and pods run under **containerd** (typical) or **CRI-O**. Use **crictl** for CRI-level inspection and **ctr** for low-level containerd debugging. See [reference/containerd.md](reference/containerd.md) and [reference/runtimes-and-cri.md](reference/runtimes-and-cri.md).

## Checklist: production-grade container

- [ ] Multi-stage build; no compilers or SCM tools in the final stage unless required.
- [ ] Pinned base image version or digest.
- [ ] Non-root user; minimal capability set at deploy time where supported.
- [ ] `.dockerignore` / `.containerignore` prevents secrets and large context uploads.
- [ ] Health check defined and matches real readiness.
- [ ] CI pipeline: build, scan, sign (if policy requires), push with immutable tag.
- [ ] `CMD`/`ENTRYPOINT` and expected env vars documented (no secrets as literals).

## Additional resources

- OCI distribution and image specs: [opencontainers.org](https://opencontainers.org/)
- This skill covers images, local container engines, and the CRI layer. For Kubernetes workload patterns (Deployments, Services, RBAC, etc.) use a cluster-focused skill.
