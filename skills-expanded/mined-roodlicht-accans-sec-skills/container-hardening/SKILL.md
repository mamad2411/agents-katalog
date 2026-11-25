---
name: container-hardening
description: Docker and OCI image hardening — base-image selection, USER/caps/read-only FS discipline, distroless migration, build-time scanning with trivy/grype, image signing via sigstore, and runtime guardrails (seccomp, AppArmor).
---

# Container Hardening

## When to use

This skill covers the container-image layer: what's inside, how it runs, and how you prove it checks out. It's the foundation `k8s-security` builds on (K8s takes these images and adds cluster-level controls).

Activates on:

- A request like "review our Dockerfile", "migrate to distroless", "why does our container run as root", "trivy scan triage", "sign images with cosign".
- A new or modified `Dockerfile`, `Containerfile`, `docker-compose.yml`, `.dockerignore`, multi-stage build script.
- An image-scan output (trivy/grype/snyk container) that needs triaging.
- A handoff from `security-review` phase 3 (container in scope) or from `k8s-security` (PodSecurityContext points to an image-level issue).
- A supply-chain moment: image needs to be signed, attestation published. Together with `supply-chain`.

### When NOT to use (handoff)

- Kubernetes workload spec (PodSecurityContext, NetworkPolicy, RBAC) → `k8s-security`. The image is the ingredient; K8s is the cook.
- SBOM format and signing-keys setup → `supply-chain`. This skill calls sigstore; that one explains it.
- Vulnerabilities in packages *inside* the image → scanner output goes to `cve-triage` for triage.
- Secrets in image layers → `secrets-scanner` on image history.
- CI pipeline that runs the build → `cicd-hardening`.
- Pure code question that just happens to run in a container → `secure-coding` or the framework skill.

## Approach

Six phases. Phases 1–3 are image content, phase 4 is signing, phase 5 is runtime, phase 6 is verification.

### 1. Base-image choice

The base image is 80% of your attack surface. Choose deliberately.

**Options, smallest to largest**:

- **scratch** (0 layers). Only for statically-linked binaries. Go, Rust, sometimes C. Smallest attack surface, no shell, no debug tools. Default for statically linked artifacts.
- **Distroless** (Google). Minimal runtime for a language (Java, Python, Node), no shell, no package manager. `gcr.io/distroless/java21-debian12`, `gcr.io/distroless/python3-debian12`, etc. With a `:debug` variant for troubleshooting.
- **Chainguard Images** / **Wolfi**. Glibc-free, continually rebuilt, SLSA-L3-signed. Comparable to distroless, with a demonstrably smaller CVE window thanks to daily builds.
- **Alpine** (musl-libc). Small (~5 MB), package manager (apk) present. Caveat: musl can produce subtle differences vs glibc (DNS resolution, thread-locals).
- **Debian slim** / **Ubuntu minimal**. Larger footprint but broader compatibility.
- **`<language>:latest`** (e.g. `node:latest`, `python:latest`). **Don't use.** `latest` is unreproducible, and these tags carry far more than needed.

Rules:

- **Pin on digest, not on tag.** `FROM gcr.io/distroless/python3-debian12@sha256:<digest>`. A tag can mutate under your feet.
- **Document update cadence.** Base images get CVEs; you have to rebuild regularly. Renovate or Dependabot for Dockerfile dep bumps.
- **One image = one responsibility.** Not one mega-image with app + migration + CLI tools; separate images with a shared base.

### 2. Dockerfile hygiene

The instructions that shape image content. Each of these is a classic foot-gun.

- **USER non-root.** The default Docker user is root (UID 0). Explicit `USER app` or `USER 10001` on a dedicated UID. Without USER: every process in the container is root in the container, and on container escape it's root on the host.
- **Read-only filesystem where possible.** Via `docker run --read-only` or Kubernetes `readOnlyRootFilesystem: true`. Limit write needs to explicit `tmpfs` or `volume` mounts. Exposure: if an attacker gets execution, they can't drop malware.
- **Drop capabilities.** Default Docker caps (NET_ADMIN, SYS_ADMIN selectively) are too broad. `--cap-drop=ALL` plus explicit additions for what you need (e.g. `--cap-add=NET_BIND_SERVICE` for ports < 1024). In Kubernetes: `securityContext.capabilities`.
- **Multi-stage builds.** Build stage with compilers and dep installers, runtime stage minimal. Prevents `gcc`, `make`, `git` from ending up in the production image. See Docker docs for syntax.
- **.dockerignore.** Prevents `.env`, `.git`, `node_modules`, test fixtures from landing in the image via `COPY . .`. Without `.dockerignore` your container has the whole source plus any local secrets.
- **No secrets in layers.** `ENV PASSWORD=...`, `ARG SECRET=...`, or `COPY .env .` commits secrets into image history. Even after a later layer-delete the secret is still there. Use BuildKit secrets (`RUN --mount=type=secret,id=...`) or runtime injection via K8s secret / Vault.
- **Layer order for caching and security.** Install dependencies first (rarely change), copy code later (frequently changes). Cache efficiency plus forced rebuild on dep change.
- **Apt/apk install cleanup.** `apt-get install --no-install-recommends` plus `rm -rf /var/lib/apt/lists/*` in the same RUN. Otherwise package lists stay in the layer.
- **Add a HEALTHCHECK** (when not via K8s liveness/readiness). Lets the orchestrator know the container is hung.
- **Document EXPOSE, don't publish.** `EXPOSE 8080` is documentation. Publishing happens at `docker run -p` or via a K8s Service.

**Anti-pattern**:

```dockerfile
FROM node:latest                    # latest tag, unreproducible
COPY . /app                         # including .env, .git, tests
RUN npm install --unsafe-perm       # suggests root permission need
USER root                           # explicitly root
CMD ["npm", "start"]
```

**Better variant**:

```dockerfile
FROM node:20-bookworm-slim@sha256:<digest> AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY src ./src

FROM gcr.io/distroless/nodejs20-debian12@sha256:<digest>
WORKDIR /app
COPY --from=build /app /app
USER 10001
CMD ["src/index.js"]
```

### 3. Build-time scanning

Before the image hits the registry:

- **Trivy** (Aqua, Apache-2). Scans images for OS and app dep-vulns, secrets, misconfigs. Fastest in adoption.
  ```bash
  trivy image --severity HIGH,CRITICAL --exit-code 1 <image>:<tag>
  ```
- **Grype** (Anchore, Apache-2). Vuln scanner combined with Syft for SBOM. Detailed per-package CVEs.
- **Clair** (Red Hat OSS). Server-side scanning, integrates with Harbor.
- **Snyk container** / **Sysdig Secure** (commercial). Enterprise options with broader feed sources and UI.
- **Docker Scout** (Docker Inc). Default in Docker Desktop since 2023; comparable to Trivy for the use case.

Tie output to `cve-triage`. All high-severity findings face that skill's blocker criteria (KEV, reachable, exposed). Don't auto-block on every HIGH; you drown in low-impact base-image noise.

Scan configurations too: Trivy has `--scanners misconfig` for Dockerfile linting (overlapping with phase 2's rules).

### 4. Image signing and provenance

See `supply-chain` for the full explanation; here are the container-specific calls.

- **Sign at build** (not after). Sigstore + cosign, keyless via OIDC.
  ```bash
  cosign sign --yes <registry>/<image>@sha256:<digest>
  ```
- **Attest the SBOM** on the same image.
  ```bash
  syft <image>:<tag> -o cyclonedx-json > sbom.json
  cosign attest --yes --predicate sbom.json --type cyclonedx <image>@sha256:<digest>
  ```
- **SLSA provenance** via `slsa-framework/slsa-github-generator` for GitHub Actions builds.
- **Verify on pull**, not just on push. A Kubernetes admission controller (Kyverno, Sigstore policy-controller) that rejects unsigned images. Reference: `k8s-security` phase 1.

Registry choice:

- **Harbor** (OSS) supports signing, vuln scanning, image replication.
- **Cloud registries** (ECR, GAR, ACR) with built-in scanning.
- **GHCR** for GitHub-attached builds.

### 5. Runtime hardening

The image is only half. Runtime policy decides what the container is allowed to do once it runs.

- **Seccomp** — filter system calls. Docker's default profile is a good starting point; custom profiles for specific workloads (nginx, PostgreSQL) can be sourced from the `moby/moby` repo or via tools like `dockerd-rootless-setuptool`.
- **AppArmor / SELinux** — mandatory access control. Default AppArmor profiles on Ubuntu/Debian, SELinux on RHEL/Fedora. Custom profiles via `--security-opt apparmor=profile-name`.
- **Rootless Docker / Podman** — daemon runs as a non-root user; a container escape doesn't reach host-root. Default in Podman, opt-in in Docker.
- **No new privileges** — `--security-opt=no-new-privileges:true` prevents setuid escalation inside the container.
- **gVisor / Kata Containers** — kernel isolation for higher trust levels. Overhead ~5–20%; pays off for multi-tenant workloads or sensitive data.

Ephemeral runtime: containers are stateless. State in volumes, not in writable layers. `--rm` for one-off runs, `emptyDir` or persistent-volume in K8s.

### 6. Verification-loop

Layer 1: scope (every Dockerfile in the repo covered? base images pinned by digest? USER non-root in every stage?), assumptions ("distroless so safe" only with the concrete image hash verified), gaps (both build-time and runtime controls present?), consistency (trivy severity threshold consistent across images?).

Layer 2: image-tag and digest syntax correct, CVE references in scan triage verified against NVD, SLSA-level claim backed by the concrete builder config, no fabricated seccomp-profile names.

## Output

```
Container hardening review — <image(s)>
Dockerfiles in scope: <list>
Base images: <used, pinned by digest: yes/no>

Image content:
  USER non-root:            <yes/no per image>
  Multi-stage build:        <yes/no>
  Read-only compatible:     <yes/no, and which write paths>
  .dockerignore present:    <yes/no>
  Secrets in layers:        <none | found: ...>

Scan output (trivy/grype):
  Blockers (HIGH/CRITICAL): <N, with cve-triage handoff>
  Medium:                   <N>
  Misconfigs:               <list>

Signing + provenance:
  Signed:                   <yes/no, cosign identity>
  SBOM attested:            <yes/no, format>
  SLSA level effective:     <L0–L3>

Runtime policy:
  Seccomp:                  <default | custom | none>
  AppArmor/SELinux:         <profile | none>
  Capabilities dropped:     <ALL + adds | default>
  Rootless runtime:         <yes/no>

Findings (severity-sorted)

Verification-loop: ...
```

## References

- Docker security docs — [https://docs.docker.com/engine/security/](https://docs.docker.com/engine/security/).
- OCI Image Spec — [https://github.com/opencontainers/image-spec](https://github.com/opencontainers/image-spec). Primary image-format spec.
- NIST SP 800-190 — [https://csrc.nist.gov/pubs/sp/800/190/final](https://csrc.nist.gov/pubs/sp/800/190/final). Application Container Security Guide.
- CIS Docker Benchmark — [https://www.cisecurity.org/benchmark/docker](https://www.cisecurity.org/benchmark/docker). Checklist form, good for audits.
- Docker Bench for Security — [https://github.com/docker/docker-bench-security](https://github.com/docker/docker-bench-security). Scripted CIS-Docker check.
- Distroless images — [https://github.com/GoogleContainerTools/distroless](https://github.com/GoogleContainerTools/distroless).
- Chainguard / Wolfi — [https://edu.chainguard.dev/chainguard/chainguard-images/](https://edu.chainguard.dev/chainguard/chainguard-images/). Continually rebuilt minimal images.
- Trivy — [https://trivy.dev/](https://trivy.dev/). Multi-purpose scanner.
- Grype + Syft — [https://github.com/anchore/grype](https://github.com/anchore/grype). Vuln scanner plus SBOM.
- Sigstore cosign — [https://docs.sigstore.dev/cosign/overview/](https://docs.sigstore.dev/cosign/overview/). Image signing without long-lived keys.
- Seccomp profiles — [https://docs.docker.com/engine/security/seccomp/](https://docs.docker.com/engine/security/seccomp/).
- OWASP Docker Security Cheat Sheet — [https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html).

## Categories

- appsec
