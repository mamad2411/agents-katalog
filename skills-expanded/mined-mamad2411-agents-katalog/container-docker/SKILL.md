---
name: container-docker
description: Docker security review — validate daemon exposure, image hygiene, registry access, runtime privileges, and socket/Dockerfile misconfiguration with read-only checks and no container escape or privileged execution.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Docker security — daemon, image, and runtime review

Use this skill to review Docker security posture on authorized in-scope systems. Validate daemon exposure, image hygiene, registry access controls, and runtime privilege configuration. All tests must use user-provided Dockerfile exports, read-only Docker API access (when authorized), and local image analysis of user-provided artifacts. Never pull private images without approval, execute containers with privileged flags, escape containers, or access Docker sockets on production systems without explicit separate approval.

## Required inputs

- Written scope naming the Docker hosts, registries, image names/tags, and allowed review methods (Dockerfile review, local image analysis, read-only daemon metadata, registry catalog enumeration). Explicit confirmation that privileged execution, container escape, private image pulling, and production socket access are prohibited unless separately approved.
- User-provided artifacts: Dockerfiles, docker-compose files, image-scan reports (Trivy, Snyk, Grype), daemon configuration (`daemon.json`), and read-only Docker API access tokens when authorized.
- Confirmation that: no containers will be started with privileged or host-mount flags, no images will be pulled from private registries without approval, no Docker socket commands will be executed on production, and no secrets will be extracted from image layers.
- Valid authorization cache for the Docker host or registry.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for read-only execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — daemon exposure and API access review

Review Docker daemon network exposure:

1. **TCP socket exposure**: check whether the Docker daemon listens on a TCP port (default 2375 for unencrypted, 2376 for TLS). If the daemon is exposed on 2375 without TLS, anyone with network access can execute Docker commands with the daemon's privileges (usually root).
2. **Unix socket permissions**: check permissions on `/var/run/docker.sock`. If the socket is world-readable or world-writable, any local user can control Docker. Default permissions should be `660` with `root:docker` ownership.
3. **Docker-in-Docker (DinD)**: check whether the host runs Docker inside a container with the socket mounted. This is a common CI pattern but allows container escape.
4. **Daemon configuration review** (`daemon.json`): check for insecure registries (`insecure-registries`), disabled user-namespace remapping (`userns-remap`), disabled seccomp/AppArmor profiles, disabled live-restore, disabled content-trust verification, and debug mode enabled.
5. **API version and authentication**: if the daemon API is reachable, check whether it requires authentication. An unauthenticated Docker API allows full container management.

### Phase 2 — Dockerfile and image build review

Review Dockerfiles for security best practices:

1. **Base image pinning**: is the base image pinned by digest (`FROM alpine@sha256:...`) or just by tag (`FROM alpine:latest`)? Floating tags introduce supply-chain risk.
2. **USER directive**: does the Dockerfile switch to a non-root user before the final CMD or ENTRYPOINT? Containers running as root can escape or modify the host more easily.
3. **COPY vs ADD**: is `ADD` used for remote URLs or tar auto-extraction? Prefer `COPY` unless the auto-extraction feature is needed.
4. **Secret handling**: are secrets passed via `ENV` (visible in `docker inspect` and linked containers), `ARG` (visible in build history), or `COPY` of a secret file (persisted in image layers)? Secrets in image layers are never truly removed.
5. **Package installation hygiene**: does the Dockerfile clean package caches (`apt-get clean`, `rm -rf /var/lib/apt/lists/*`, `apk cache clean`) after installing packages? Leftover caches increase image size and attack surface.
6. **Multi-stage builds**: are multi-stage builds used? They prevent build tools and intermediate artifacts from shipping in the final image.
7. **HEALTHCHECK**: is a health check defined? Without it, unhealthy containers may not be restarted.
8. **EXPOSE**: are only necessary ports exposed? EXPOSE is documentation, not enforcement, but unnecessary exposed ports hint at legacy or debug services.

### Phase 3 — image-layer secret and vulnerability scanning

Analyze image contents for secrets and known vulnerabilities:

1. **Secret scanning**: if the user provides a local image tarball or `docker save` output, use catalog tools (Trivy, ggshield) to scan image layers for secrets: API keys, private keys, tokens, database URLs, cloud credentials, and internal hostnames. Never store found secrets in evidence — record their presence, type, and layer hash only.
2. **Vulnerability scanning**: scan the image for known CVEs in OS packages and application dependencies. Record findings by severity: critical (CVSS >= 9.0), high (7.0-8.9), medium (4.0-6.9), low (< 4.0).
3. **Image-layer inspection**: use `docker history --no-trunc` to inspect each layer's build command. Look for secrets passed via `--build-arg`, credentials copied as files, or sensitive data in `RUN` commands.
4. **Image provenance**: check whether the image is signed (Docker Content Trust / Notary, Cosign). Unsigned images from public registries may have been tampered with.
5. **Image size and layer count**: unnecessarily large images or excessive layer counts suggest poor hygiene and increase the attack surface.

### Phase 4 — runtime privilege and capability review

If read-only access to running containers is authorized:

1. **Privileged containers**: check for containers running with `--privileged`. This gives the container all Linux capabilities and access to all host devices — equivalent to root on the host with some namespace isolation.
2. **Capability enumeration**: for each container, list the Linux capabilities (`capsh --print` inside the container or `docker inspect`). Compare granted capabilities against the container's functional needs. Common excessive capabilities: `CAP_SYS_ADMIN`, `CAP_SYS_PTRACE`, `CAP_NET_RAW`, `CAP_SYS_MODULE`, `CAP_DAC_READ_SEARCH`.
3. **Host mounts**: check for host directories mounted into the container (`-v /:/host`, `-v /var/run/docker.sock:/var/run/docker.sock`, `-v /proc:/proc`). Docker socket mounts allow container escape. Host-root mounts allow full host filesystem access.
4. **Network mode**: check whether any container runs with `--net=host` (shares the host network namespace), `--pid=host` (shares host process namespace), or `--ipc=host` (shares host IPC namespace). Each weakens namespace isolation.
5. **Resource limits**: check whether memory and CPU limits are set (`--memory`, `--cpus`). Unbounded containers can exhaust host resources (denial of service).
6. **Read-only root filesystem**: check whether `--read-only` is used for containers that don't need to write to the filesystem. A writable root filesystem allows attackers to modify binaries, drop malware, or tamper with configuration.

### Phase 5 — registry access and supply-chain review

Review the Docker registry configuration:

1. **Registry authentication**: does the registry require authentication for pull operations? Unauthenticated registries allow anyone to download images — exposure depends on image content.
2. **Registry catalog enumeration**: if authorized, enumerate the registry catalog (`/v2/_catalog`). List all repositories. Check for private/internal repositories that should not be pullable without authentication.
3. **Manifest and tag inspection**: for each in-scope repository, list tags without pulling the full image. Inspect the manifest for architecture, layers, and creation timestamps.
4. **Registry TLS**: is the registry served over HTTPS with a valid certificate? Images pulled over HTTP can be tampered with via man-in-the-middle.
5. **Image signing**: does the registry enforce signed images (Docker Content Trust)? If not, anyone with push access can replace an image with a malicious version.

## Decision points

- **Escalate on exposed Docker API without auth**: TCP port 2375 open without TLS → critical (full container and likely host compromise possible).
- **Escalate on privileged container**: `--privileged` flag on a non-admin container → high/critical.
- **Escalate on Docker socket mount in container**: `/var/run/docker.sock` mounted → container escape vector, high finding.
- **Escalate on host-root mount**: `-v /:/host` in container → host filesystem access, critical.
- **Escalate on secrets in image layers**: API keys, tokens, or credentials in image history → critical.
- **Downgrade on cosmetic Dockerfile issues**: missing HEALTHCHECK or unnecessary EXPOSE → informational.

## Prohibited behavior

- Executing container-escape techniques (privileged escape, cgroup release_agent, kernel exploit) against production systems.
- Starting containers with `--privileged`, `--cap-add`, or host-mount flags on production Docker hosts.
- Pulling private images from registries without explicit approval.
- Executing commands on or modifying running containers.
- Extracting and storing secrets from image layers — record metadata only.
- Accessing Docker sockets on production systems without separate explicit approval.

## Stop conditions

- Exposed Docker API found → stop, record critical finding, do not execute Docker commands.
- Secrets found in image history → stop scanning the image, record metadata (type, layer), redact values.
- Container escape vector confirmed (socket mount, privileged + host mount) → stop, do not exploit.
- Registry or host not confirmed in scope → stop.
- Active container or production service impact risk → stop, defer to maintainer.

## Evidence — Docker security posture matrix

For each target, record:

```text
Docker host/registry: <hostname or IP>
Review scope: <daemon | Dockerfile | image | runtime | registry>

Daemon findings (if in scope):
  TCP exposure: <port 2375 open | port 2376 with TLS | none>
  Socket permissions: <mode> | ownership: <user:group>
  Insecure registries: <list | none>
  User namespace remap: <enabled | disabled>
  Content trust: <enabled | disabled>
  Debug mode: <enabled | disabled>

Dockerfile findings (if in scope):
  Base image pinned: <yes | no — floating tag>
  Runs as non-root: <yes | no>
  Secrets in ENV/ARG: <yes (count) | no>
  Package caches cleaned: <yes | no>
  Multi-stage build: <yes | no>

Image findings (if in scope):
  Image: <name:tag> | Digest: <sha256:...>
  Critical CVEs: <count>
  High CVEs: <count>
  Secrets in layers: <count, types>
  Image signed: <yes | no>

Runtime findings (if in scope):
  Container: <name or ID-prefix>
  Privileged: <yes | no>
  Capabilities: <list of excessive caps>
  Host mounts: <list | none>
  Docker socket mount: <yes | no>
  Network mode: <host | bridge | overlay>
  Read-only rootfs: <yes | no>

Overall risk: <critical | high | medium | low | none>
```

Never store: Docker socket paths with full container IDs, secret values from image layers, registry credentials, image pull tokens, Docker daemon TLS keys, or unredacted container environment variables containing credentials.

## Report handoff

When review is complete:
1. `pentest_agent_record_finding` for each finding: exposed Docker API, privileged containers, socket mounts, host-root mounts, excessive capabilities, secrets in image layers, critical CVEs, unauthenticated registry access, and unsigned images.
2. Reference the Docker security posture matrix.
3. Recommend: never expose Docker API on TCP without TLS and mutual authentication, run all containers as non-root with `--read-only` where possible, drop all capabilities and add only those required, never mount Docker socket into containers, use user-namespace remapping, pin base images by digest, use multi-stage builds and clean package caches, scan images for secrets and CVEs in CI (Trivy/Grype), enforce image signing with Cosign or Notary, use `docker-bench-security` for CIS compliance auditing, and mount host directories read-only when read access suffices.
