---
name: container-build-and-release
description: >
  Builds, tags, scans, and publishes container images with reproducible,
  minimal, multi-stage Dockerfiles and a defensible tagging/release scheme.
  Use when the user asks to "write a Dockerfile," "reduce image size,"
  "set up multi-arch builds," "tag and push a container image," "add image
  scanning to the pipeline," or "publish a release image to a registry."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# Container Build and Release

## Purpose

The container image is the deployable unit for most modern services, and
how it's built determines its size, attack surface, build speed, and
whether "the same image" really is the same thing that was tested. Sloppy
Dockerfiles (single-stage, root user, unpinned base images, `latest` tags)
produce bloated, insecure, and non-reproducible artifacts that undermine
every downstream deployment strategy. This skill covers building small,
reproducible, properly tagged images and publishing them through a
release pipeline with scanning and provenance.

## When to use

- Writing or reviewing a Dockerfile for a new service.
- Reducing image size or build time (slow CI, huge registry storage bill).
- Setting up multi-architecture builds (amd64 + arm64).
- Establishing an image tagging scheme (immutable digests vs. mutable
  tags, `latest` usage policy).
- Adding vulnerability scanning or SBOM generation to the image build
  pipeline.
- Publishing a versioned release image to a registry (GHCR, Docker Hub,
  ECR, ACR, GCR/Artifact Registry).

## Prerequisites & environment

- Docker Engine ≥ 24 or a compatible builder (BuildKit is default in
  Docker ≥ 23; enable explicitly on older versions with
  `DOCKER_BUILDKIT=1`) — BuildKit enables cache mounts and multi-stage
  parallelism used below.
- `docker buildx` for multi-architecture builds (bundled with Docker
  Desktop and modern Docker Engine installs).
- Registry credentials with least-privilege push access, stored as CI
  secrets, not embedded in the Dockerfile or committed config.
- A base image policy decided (distro-based minimal images like
  `debian-slim`/`alpine`, or distroless) — this affects available shell
  tooling for debugging vs. attack surface trade-offs.
- Optional but recommended: `trivy`, `grype`, or the registry's built-in
  scanner for vulnerability scanning; `syft` or `docker buildx imagetools`
  for SBOM generation.

## Step-by-step guidance

1. **Use multi-stage builds** to separate build-time dependencies from the
   runtime image, so compilers, dev headers, and package manager caches
   never ship in the final image:
   ```dockerfile
   # syntax=docker/dockerfile:1.7
   FROM node:20-bookworm-slim AS build
   WORKDIR /app
   COPY package.json package-lock.json ./
   RUN --mount=type=cache,target=/root/.npm \
       npm ci
   COPY . .
   RUN npm run build

   FROM node:20-bookworm-slim AS runtime
   WORKDIR /app
   ENV NODE_ENV=production
   COPY package.json package-lock.json ./
   RUN --mount=type=cache,target=/root/.npm \
       npm ci --omit=dev
   COPY --from=build /app/dist ./dist
   RUN useradd --no-create-home --uid 10001 appuser
   USER appuser
   EXPOSE 3000
   ENTRYPOINT ["node", "dist/server.js"]
   ```

2. **Pin base images by tag and, for release builds, by digest** to make
   builds reproducible and immune to upstream tag mutation:
   ```dockerfile
   FROM node:20.15.1-bookworm-slim@sha256:<digest>
   ```
   Renovate/Dependabot can automate digest bumps so this doesn't become
   manual toil.

3. **Order layers from least to most frequently changing** so Docker's
   layer cache is actually useful: dependency manifests
   (`package.json`/`go.mod`/`requirements.txt`) copied and installed
   *before* application source, so a source-only change doesn't
   invalidate the dependency install layer.

4. **Run as a non-root user** and drop unnecessary capabilities; avoid
   `--privileged` runs and Docker socket mounts in production containers.

5. **Build multi-arch images with buildx** when targeting mixed
   architectures (e.g., amd64 CI runners, arm64 Graviton/Apple Silicon
   production nodes):
   ```bash
   docker buildx create --use --name multiarch-builder
   docker buildx build \
     --platform linux/amd64,linux/arm64 \
     -t ghcr.io/example/payments-api:1.4.2 \
     --push .
   ```

6. **Tag deliberately**: give every built image an immutable, traceable
   tag (commit SHA or semantic version) in addition to any mutable
   convenience tag:
   ```bash
   IMAGE=ghcr.io/example/payments-api
   docker buildx build \
     -t $IMAGE:1.4.2 \
     -t $IMAGE:$(git rev-parse --short HEAD) \
     -t $IMAGE:latest \
     --push .
   ```
   Deploy manifests should reference the immutable tag or, ideally, the
   resolved digest (`$IMAGE@sha256:...`) — never deploy `latest` to a
   real environment, since it gives no guarantee of *which* build is
   actually running. See
   [release-versioning-and-changelog-automation](../release-versioning-and-changelog-automation/SKILL.md)
   for how the version number itself should be derived.

7. **Scan the image before publishing it as a release candidate**:
   ```bash
   trivy image --severity HIGH,CRITICAL --exit-code 1 $IMAGE:1.4.2
   ```
   Fail the pipeline (or require an explicit waiver) on HIGH/CRITICAL
   findings rather than publishing and hoping someone checks later.

8. **Generate and attach an SBOM** for supply-chain traceability:
   ```bash
   syft $IMAGE:1.4.2 -o spdx-json > sbom.spdx.json
   docker buildx imagetools create --tag $IMAGE:1.4.2 --annotation index:sbom=sbom.spdx.json ...
   ```

9. **Push to the registry and record the resulting digest** as a build
   output so downstream deploy steps deploy an exact digest, not a tag
   that could be repointed after the fact:
   ```bash
   DIGEST=$(docker buildx imagetools inspect $IMAGE:1.4.2 --format '{{json .Manifest.Digest}}')
   ```

## Best practices

- Prefer slim/minimal or distroless base images for runtime stages;
  reserve full-featured images for the build stage only.
- Never bake secrets into image layers, even temporarily — a secret
  written in an intermediate layer and removed in a later `RUN` is still
  present in the image history. Use BuildKit secret mounts instead:
  `RUN --mount=type=secret,id=npmrc npm ci` with the secret supplied at
  build time (`--secret id=npmrc,src=.npmrc`), never `ARG`/`ENV` for
  sensitive values.
- Keep `.dockerignore` current (exclude `.git`, `node_modules`, build
  artifacts, local env files) to shrink build context and avoid
  accidentally copying secrets/local config into the image.
- Treat container tags as either fully immutable (digest-pinned releases)
  or explicitly mutable-and-documented (`edge`, `nightly`) — never let
  `latest` silently become "whatever was last pushed" for anything
  customers or production depend on.
- Rebuild and rescan base images periodically even if application code
  hasn't changed, since new CVEs are discovered continuously in upstream
  base images and dependencies.
- Keep image build logic (Dockerfile) reviewed with the same rigor as
  application code — it's part of the production system.

## Common pitfalls

- **Symptom:** Image is several hundred MB larger than expected for a
  simple service.
  **Fix:** Check for a single-stage build carrying build tools/dev
  dependencies into runtime, or a base image that isn't a slim/minimal
  variant; switch to multi-stage and copy only build outputs into the
  runtime stage.

- **Symptom:** A secret used during build (private package registry
  token) is discoverable via `docker history` or by extracting layers,
  even though it's not in the final `ENV`.
  **Fix:** Any value passed via `ARG`/`ENV` or written to a file and later
  deleted in a subsequent `RUN` still persists in that layer's history.
  Use BuildKit `--mount=type=secret` so the secret is never written to a
  committed layer at all.

- **Symptom:** "It worked in staging but broke in prod" despite deploying
  "the same image."
  **Fix:** Check whether prod is actually pulling `latest` (or a tag that
  moved between staging and prod deploy) rather than the exact digest
  that was tested; pin deploys to an immutable tag or digest.

- **Symptom:** Multi-arch build succeeds on CI (amd64) but the arm64
  variant crashes at runtime on Graviton/Apple Silicon nodes.
  **Fix:** The image likely wasn't actually tested on the second
  architecture — run integration tests against both platforms (via QEMU
  emulation or native arm64 runners) before publishing a multi-arch
  manifest as a release.

- **Symptom:** Vulnerability scan flags dozens of CVEs in the base OS
  layer that have nothing to do with the application.
  **Fix:** Confirm the base image is current (rebuild against the latest
  patch tag/digest of the same minor version) before triaging individual
  CVEs — many disappear simply by rebuilding against an up-to-date base.

## Worked example

**Scenario:** Build, scan, and publish a release image for `payments-api`
version `1.4.2` from a GitHub Actions pipeline, targeting both amd64 and
arm64, with a failing gate on critical vulnerabilities.

```yaml
name: release-image
on:
  push:
    tags: ["v*.*.*"]

jobs:
  build-scan-push:
    runs-on: ubuntu-latest
    permissions: { contents: read, packages: write }
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-qemu-action@v3
      - uses: docker/setup-buildx-action@v3

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Derive version
        id: ver
        run: echo "version=${GITHUB_REF_NAME#v}" >> "$GITHUB_OUTPUT"

      - name: Build (local, for scan)
        uses: docker/build-push-action@v6
        with:
          context: .
          load: true
          tags: local/payments-api:scan

      - name: Scan
        run: |
          trivy image --severity HIGH,CRITICAL --exit-code 1 local/payments-api:scan

      - name: Build and push multi-arch
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ghcr.io/example/payments-api:${{ steps.ver.outputs.version }}
            ghcr.io/example/payments-api:${{ github.sha }}
```
A tag push of `v1.4.2` produces
`ghcr.io/example/payments-api:1.4.2` (and a SHA-tagged twin for exact
traceability), only after the scan gate passes — the deploy pipeline
(see [blue-green-canary-deployments](../blue-green-canary-deployments/SKILL.md))
then references that immutable tag, never `latest`.

## Cross-references

- [blue-green-canary-deployments](../blue-green-canary-deployments/SKILL.md)
- [release-versioning-and-changelog-automation](../release-versioning-and-changelog-automation/SKILL.md)
- [artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md)
