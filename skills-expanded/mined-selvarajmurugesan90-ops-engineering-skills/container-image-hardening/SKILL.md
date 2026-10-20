---
name: container-image-hardening
description: >
  Guides building minimal, non-root, hardened container images —
  multi-stage builds, distroless/minimal base images, non-root users,
  read-only root filesystems, dropped Linux capabilities, and pinned/
  digest-referenced base images. Use when the user asks to "harden this
  Dockerfile", "reduce container image attack surface/size", "make our
  container run as non-root", "switch to a distroless base image",
  "fix a container security scan finding about running as root or having
  a shell", or "set Kubernetes securityContext restrictions for a pod".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devsecops
  maturity: stable
---

# Container Image Hardening

## Purpose

A container image built from a full general-purpose base image (e.g. a
default Ubuntu or Debian image with a shell, package manager, and dozens
of unrelated utilities) running as root gives an attacker who compromises
the application inside it a much larger toolkit and a much easier path to
container breakout or lateral movement than a minimal, non-root image
with no shell and only the application's actual runtime dependencies.
Container image hardening is about shrinking that attack surface at
build time: using multi-stage builds so build tooling never ships in the
final image, choosing minimal or distroless base images, running as a
non-root user, making the root filesystem read-only, dropping unnecessary
Linux capabilities, and pinning base images by digest so "the same image"
can't silently change out from under you. None of this replaces
vulnerability scanning of what *is* in the image — it reduces what's
there to scan and what's exploitable if a vulnerability is found.

## When to use

- The user asks to "harden this Dockerfile" or "reduce the attack surface"
  of a container image.
- A container/SCA scan flags a base image with dozens of OS-level
  vulnerabilities and the user wants to address the base image itself,
  not just individual CVEs.
- The user wants to fix a "runs as root" finding from a security scanner,
  admission-policy rejection, or manual review.
- The user is deciding between a distroless, Alpine, minimal, or
  full-distribution base image for a given language/runtime.
- The user wants to set Kubernetes `securityContext` fields (`runAsNonRoot`,
  `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, dropped
  `capabilities`) consistently across workloads.
- The user is troubleshooting a hardened image that fails at runtime
  (permission errors, missing shell for debugging, missing writable
  temp directory) and needs to understand the trade-offs.

## Prerequisites & environment

- Docker or another OCI-compatible builder (Buildah, Podman, BuildKit)
  supporting multi-stage builds (standard in Docker since `18.09`+, and
  in essentially all current tooling).
- Familiarity with the target application's actual runtime dependencies
  — hardening requires knowing what the app truly needs at runtime versus
  what's only needed to build it, which usually means reading the
  existing Dockerfile and build process rather than guessing.
- Base image choices to evaluate:
  - **Distroless** (`gcr.io/distroless/*`) — no shell, no package
    manager, only the language runtime and its direct OS-level
    dependencies; smallest attack surface, but harder to debug (no
    `exec`-into-shell) and requires a compatible language runtime image
    per stack (`distroless/java`, `distroless/nodejs`, `distroless/cc`
    for compiled binaries with a C library, `distroless/static` for
    fully static binaries e.g. Go with CGO disabled).
  - **Alpine** — small (musl libc, `apk` package manager), widely used,
    but musl's subtle differences from glibc occasionally break
    compiled dependencies (e.g. some Python/Node native modules); still
    ships a shell and package manager unless explicitly stripped.
  - **`-slim` variants** (e.g. `python:3.12-slim`, `node:20-slim`) — a
    reasonable middle ground: much smaller than the full image, glibc-based
    (fewer compatibility surprises than Alpine), still has a shell.
  - Full-distribution images (`ubuntu`, `debian`, default `python:3.12`)
    — largest attack surface and image size; rarely justified for a
    final runtime image, sometimes needed as a build stage.
- Kubernetes cluster (if hardening deploy-time `securityContext`) with
  admission-policy enforcement optional but recommended — see
  [policy-as-code-guardrails](../policy-as-code-guardrails/SKILL.md) to
  make these properties mandatory rather than best-effort.

## Step-by-step guidance

1. **Split the build into stages**, so build-only tooling (compilers,
   `dev` package variants, source code not needed at runtime) never
   reaches the final image:
   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM golang:1.22 AS builder
   WORKDIR /src
   COPY go.mod go.sum ./
   RUN go mod download
   COPY . .
   RUN CGO_ENABLED=0 GOOS=linux go build -o /out/app ./cmd/app

   FROM gcr.io/distroless/static-debian12:nonroot
   COPY --from=builder /out/app /app
   USER nonroot:nonroot
   ENTRYPOINT ["/app"]
   ```

2. **Pin the base image by digest**, not just tag, for anything you
   consider "the same" across rebuilds — tags are mutable and can be
   repointed by the upstream maintainer:
   ```dockerfile
   FROM python:3.12-slim@sha256:<digest> AS base
   ```
   Balance this against staying current on security patches: pinning by
   digest requires an explicit, deliberate bump process (e.g. a
   Renovate/Dependabot rule that tracks base-image digests) rather than
   silently freezing on a vulnerable base forever.

3. **Run as a non-root user explicitly** — don't rely on a base image's
   default (`distroless/*-nonroot` variants set this for you; for others,
   create and switch to a dedicated user):
   ```dockerfile
   RUN addgroup --system app && adduser --system --ingroup app app
   USER app:app
   ```

4. **Set a read-only root filesystem** at deploy time, with an explicit
   writable volume only where genuinely needed (temp files, cache):
   ```yaml
   # Kubernetes pod securityContext
   securityContext:
     runAsNonRoot: true
     readOnlyRootFilesystem: true
     allowPrivilegeEscalation: false
     capabilities:
       drop: ["ALL"]
   volumes:
     - name: tmp
       emptyDir: {}
   volumeMounts:
     - name: tmp
       mountPath: /tmp
   ```

5. **Drop all Linux capabilities and add back only what's required** —
   most application containers need none of the default capability set:
   ```yaml
   securityContext:
     capabilities:
       drop: ["ALL"]
       # add: ["NET_BIND_SERVICE"]  # only if binding to a port < 1024
   ```

6. **Remove build-time secrets and unnecessary files** from the final
   image — use BuildKit secret mounts for anything credential-like during
   build (see [secrets-management](../secrets-management/SKILL.md)), and
   a `.dockerignore` to keep `.git`, local env files, and test fixtures
   out of the build context entirely:
   ```
   # .dockerignore
   .git
   .env*
   **/__pycache__
   node_modules
   *.md
   ```

7. **Scan the built image**, not just the Dockerfile, since the final
   image is what actually ships:
   ```bash
   trivy image --severity CRITICAL,HIGH myorg/myapp:1.4.2
   ```
   See [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md)
   for the full scanning workflow.

8. **Verify hardening holds at runtime**, not just at build time — a
   Dockerfile with `USER app` can still be overridden by a Kubernetes pod
   spec with `runAsUser: 0`; enforce the deploy-time properties via an
   admission policy (see
   [policy-as-code-guardrails](../policy-as-code-guardrails/SKILL.md))
   so the Dockerfile's intent can't be silently undone at deploy time.

## Best practices

- Treat multi-stage builds as the default, not an optimization — any
  Dockerfile with a compiler, dev headers, or source checkout that also
  runs the application in the same final stage is very likely shipping
  unnecessary attack surface.
- Choose the smallest base image the application can actually run
  reliably on: distroless/static for statically-linked binaries (Go,
  Rust with musl target), a `-slim` glibc-based image for interpreted
  languages with native extensions where Alpine's musl libc causes
  friction, Alpine where compatibility is confirmed and size matters
  most.
- Set non-root, read-only-root, dropped-capabilities, and
  no-privilege-escalation together as a bundle — these four properties
  compound: a non-root user with a writable root filesystem is still
  meaningfully weaker than the same user with a read-only filesystem.
- Pin base images by digest for reproducibility, but pair it with an
  automated process to bump that digest regularly (Renovate/Dependabot
  digest-update rules) — an unpinned `:latest` drifts unpredictably, but
  a digest pinned once and never revisited silently accumulates
  unpatched base-image CVEs, which is not obviously better.
- Enforce hardening properties at the Kubernetes admission layer in
  addition to the Dockerfile — a well-hardened image can still be run
  insecurely (`runAsUser: 0`, capabilities added back, writable root
  filesystem) by pod spec alone, and only cluster-side enforcement
  guarantees the properties actually hold at runtime.
- Keep a debug story for distroless/no-shell images before you need it in
  an incident — e.g. a separate debug image variant with a shell built
  from the same application layer, or `kubectl debug` with an ephemeral
  container attached to the running pod — rather than discovering during
  an incident that you can't `exec` in at all.

## Common pitfalls

- **Symptom:** Switching to a distroless base image breaks the ability to
  `kubectl exec -it` into the container to debug an issue.
  **Fix:** This is expected — distroless images have no shell by design.
  Use `kubectl debug <pod> -it --image=busybox --target=<container>` to
  attach an ephemeral debug container with a shell to the running pod's
  namespaces instead of relying on exec-into-the-app-container, or
  maintain a separate `-debug` image tag with a shell for troubleshooting
  builds specifically.

- **Symptom:** An Alpine-based image works in local Docker Desktop testing
  but a compiled Python/Node native dependency fails or behaves
  differently in the CI/production Alpine build.
  **Fix:** This is usually musl libc vs. glibc incompatibility in a
  native extension; either switch that stage to a glibc-based `-slim`
  image, or confirm the specific native dependency has verified musl
  support before committing to Alpine for that service.

- **Symptom:** Setting `readOnlyRootFilesystem: true` causes the
  application to crash on startup with a permission or "read-only file
  system" error.
  **Fix:** The app is writing somewhere in the root filesystem at runtime
  (temp files, a cache directory, a PID file) — identify the path (check
  the crash log/strace) and mount a dedicated `emptyDir` (or persistent
  volume, if it must survive restarts) at exactly that path rather than
  reverting the read-only setting entirely.

- **Symptom:** A Dockerfile sets `USER app` but the running pod in
  Kubernetes still shows the process running as root (UID 0).
  **Fix:** Something in the deploy path (`runAsUser: 0` in the pod spec,
  or a Helm chart default) is overriding the image's default user;
  Kubernetes pod spec takes precedence over the Dockerfile `USER`
  instruction. Set and enforce `runAsNonRoot: true` in the pod
  `securityContext` and consider an admission policy to prevent this
  override cluster-wide (see
  [policy-as-code-guardrails](../policy-as-code-guardrails/SKILL.md)).

- **Symptom:** Image size and vulnerability count barely improve after
  switching base images, and the SCA scan still shows the same dozens of
  CRITICAL findings.
  **Fix:** Check whether build-stage tooling or dev dependencies are
  still leaking into the final stage (missing `COPY --from=builder`
  scoping, or installing dev packages in the final stage instead of only
  the builder stage) — the base image swap alone doesn't help if the
  Dockerfile still installs a compiler or full package set in the
  runtime stage.

## Worked example

A Go HTTP service is rewritten from a single-stage, root, full-Debian
Dockerfile to a hardened multi-stage, distroless, non-root build, with
matching Kubernetes `securityContext`.

Before:
```dockerfile
FROM golang:1.22
WORKDIR /app
COPY . .
RUN go build -o server ./cmd/server
CMD ["./server"]
```
(Runs as root, ships the full Go toolchain and source tree, ~900MB image,
default Debian base with a shell and package manager.)

After:
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22 AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -o /out/server ./cmd/server

FROM gcr.io/distroless/static-debian12:nonroot@sha256:<digest>
COPY --from=builder /out/server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]
```
Corresponding Kubernetes pod hardening:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: myapp
      image: myorg/myapp:1.4.2@sha256:<image-digest>
      securityContext:
        runAsNonRoot: true
        readOnlyRootFilesystem: true
        allowPrivilegeEscalation: false
        capabilities:
          drop: ["ALL"]
      volumeMounts:
        - name: tmp
          mountPath: /tmp
  volumes:
    - name: tmp
      emptyDir: {}
```
Result: image size drops from ~900MB to under 20MB (statically-linked Go
binary plus a near-empty distroless base), the final image ships no
shell/package manager/source tree for an attacker to leverage after a
compromise, a `trivy image` scan on the new image shows a dramatically
smaller finding count because there's no OS package layer to accumulate
CVEs, and the pod-level `securityContext` guarantees the container can't
be started as root or with a writable filesystem even if someone edits
the deployment manifest later — assuming an admission policy is in place
to keep that guarantee from being quietly overridden.

## Cross-references

- [software-composition-analysis-sca](../software-composition-analysis-sca/SKILL.md) —
  scanning the resulting image for known vulnerabilities in whatever
  base-image packages and dependencies remain.
- [supply-chain-security-slsa-sbom](../supply-chain-security-slsa-sbom/SKILL.md) —
  generating an SBOM and signing the hardened image so its provenance
  can be verified downstream.
- [policy-as-code-guardrails](../policy-as-code-guardrails/SKILL.md) —
  enforcing non-root/read-only/dropped-capabilities requirements at
  Kubernetes admission time so a hardened Dockerfile's properties can't
  be silently overridden by a pod spec.
