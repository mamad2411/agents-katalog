# Container Image Design, Hardening & Operations

## Purpose
Build small, reproducible container images (Docker, Podman) with multi-stage builds, pinned digests, non-root execution, explicit health checks, minimal attack surface, and verified SBOM provenance.

## Use when
- Authoring or reviewing Dockerfiles and image build pipelines for services, workers, or CLI tools.
- Shrinking image size, cutting CVE counts, or removing root execution from running containers.
- Adding health checks, graceful shutdown, signal handling, or resource limits to containerized workloads.
- Auditing image reproducibility: same context digest in, same image digest out.

## Do not use when
- Designing CI stage ordering, merge gates, or runner caching (use `ci-cd`).
- Cutting versioned releases with changelogs and rollback plans (use `release-engineering`).
- Orchestrating multi-service deployments, Helm charts, or Kubernetes policy (out of scope; this skill stops at the image boundary).
- Tuning application-level caching or eviction (use `caching`).

## Required context
- Base image policy: approved distroless or minimal images with digests (e.g. `gcr.io/distroless/static-debian12@sha256:5f8d1e`), plus the CVE ceiling (zero HIGH/CRITICAL at ship).
- Application runtime needs: language, ports (e.g. 8080), read/write paths, required syscalls, shutdown grace period (30 s).
- Registry and signing setup: registry URL, cosign key or keyless OIDC identity, SBOM generation tool (syft 1.27.0).
- Resource envelope: memory limit (512 MiB), CPU limit (1.0), ephemeral storage ceiling (1 GiB).

## Procedure
1. **Select a minimal pinned base**:
   - Use distroless or `-alpine` bases pinned by digest, never by floating tag; record the digest in the build spec.
   - Prefer static linking (`CGO_ENABLED=0 go build -trimpath -ldflags="-s -w"`) so the final stage carries no toolchain.
2. **Write a multi-stage Dockerfile**:
   - Stage `build`: full toolchain, locked dependencies (`go mod download` from committed `go.sum`), `go vet` and `go test` before compiling.
   - Stage `final`: copy only the binary plus strictly required assets (`COPY --from=build /src/server /server`); no shell, no package manager, no source tree.
   - Confirm final size against budget (e.g. at most 25 MB for a Go API) with `docker images billing-api:2.14.0 --format '{{.Size}}'`.
3. **Drop privileges and harden the runtime**:
   - Create and use a numeric non-root user (`USER 65532:65532`); verify with `docker run --rm image id` showing `uid=65532`.
   - Set `readOnlyRootFilesystem: true` semantics: mount writable `emptyDir` only where the app provably writes (`/tmp`, `/var/run/app`).
   - Drop all Linux capabilities and add none back unless a named syscall need is documented (`--cap-drop=ALL`).
4. **Wire health, signals, and shutdown**:
   - Add `HEALTHCHECK --interval=15s --timeout=3s --retries=3 CMD ["/server", "-health-check"]` backed by a real readiness probe hitting dependencies.
   - Use exec-form `ENTRYPOINT` so PID 1 receives SIGTERM; handle it with a 25-second drain inside the 30-second grace period.
   - Verify with `docker stop -t 30 container` completing without SIGKILL and zero in-flight request drops in the test harness.
5. **Prove reproducibility and provenance**:
   - Rebuild twice from the same context (`docker build --no-cache`) and compare image digests; they must match byte-for-byte modulo timestamps (use `SOURCE_DATE_EPOCH=1726358400`).
   - Scan with `trivy image --severity HIGH,CRITICAL billing-api:2.14.0` (zero findings required) and attach `syft` SBOM plus cosign signature.
   - Run the verification script `scripts/verify.sh` from the repo root; it must exit 0.

## Decision rules
- **Non-Root Is Non-Negotiable**: No image runs as UID 0 in any environment; builds that require root must drop privileges in the final stage.
- **Digest Pinning Is Mandatory**: Floating tags (`latest`, `alpine`, `bookworm-slim`) are prohibited in committed Dockerfiles; digests only.
- **Zero HIGH/CRITICAL at Ship**: Images with unresolved HIGH or CRITICAL CVEs do not ship; exceptions need a dated waiver with owner.
- **Final Stage Carries No Toolchain**: Compilers, shells, curl, and package managers in the final stage are defects, not conveniences.
- **Health Checks Must Be Real**: A health check that returns 200 without touching dependencies is a lie detector that always passes; probe something real.

## Evidence required
- Image specification adhering to `templates/containers-spec.md` with digests, sizes, and scan results.
- Reproducibility proof: two `--no-cache` build digests that match.
- `trivy image` scan log with zero HIGH/CRITICAL findings and the attached SBOM.
- Non-root and shutdown verification logs (`id` output, graceful-stop timing).
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Multi-stage Dockerfile with pinned digests, non-root user, and real health check.
- Build, scan, and sign pipeline steps (or documented commands) producing SBOM and signature.
- Resource envelope: requests/limits for memory, CPU, and ephemeral storage.
- Image report: final size, layer count, CVE count by severity, digest.

## Stop conditions
- Image builds reproducibly (matching digests), runs as non-root, passes health and graceful-shutdown checks.
- Security scan shows zero HIGH/CRITICAL CVEs with SBOM generated and signature attached.
- Image size within budget and layer count justified.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to Security if a base image carries unfixable HIGH/CRITICAL CVEs with no patched upstream within the release window.
- Escalate to Platform Lead if the workload genuinely needs a capability (e.g. `NET_BIND_SERVICE`) or writable root that conflicts with hardening.
- Escalate to the owning team if reproducible builds diverge due to timestamp or network nondeterminism in dependencies.
