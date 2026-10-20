---
name: containerise
description: Produce a hardened multi-stage Dockerfile plus a docker compose file for local development, matched to the stack detected in the repository (Node, Angular static, Java/Spring, Python). Use when a project needs its first container, when an image is oversized or slow to build, when it runs as root, or when SIGTERM handling and local dev parity need fixing.
user-invocable: true
argument-hint: "[--stack node|angular|java|python] [--registry <host>] [--no-compose]"
model: sonnet
effort: medium
metadata:
  foundry.vertical: operations
  foundry.io: "repository -> Dockerfile + .dockerignore + compose.dev.yaml + review.v1"
license: Apache-2.0
---

# Containerise

Produces an image that is small, reproducible, non-root and correct under `SIGTERM`, plus a
compose file that gives developers the same runtime locally.

**Use it when** there is no Dockerfile, or when an existing one fails the checklist in
`references/hardening-checklist.md`.

**Do not use it when** the target is a PaaS with its own buildpack (Vercel, Netlify, and the
buildpack paths of Render/Railway) — a Dockerfile there adds a build you now maintain for no
benefit. Ask `cloud-architect` first if the target is undecided. Do not use it for Windows
containers.

## Step 1 — Detect

```bash
ls -1 package.json angular.json pom.xml build.gradle build.gradle.kts pyproject.toml requirements.txt go.mod 2>/dev/null
ls -1 package-lock.json pnpm-lock.yaml yarn.lock poetry.lock uv.lock 2>/dev/null
test -f package.json && jq -r '.main, .scripts.start, .type' package.json
test -f pom.xml && grep -m1 -o '<packaging>[^<]*' pom.xml
ls -1 Dockerfile* .dockerignore compose*.y*ml docker-compose*.y*ml 2>/dev/null
```

| Signal | Template |
|---|---|
| `angular.json` + a static build | `references/angular-static.Dockerfile` |
| `package.json`, server process | `references/node.Dockerfile` |
| `pom.xml` / `build.gradle*` | `references/java-spring.Dockerfile` |
| `pyproject.toml` / `requirements.txt` | `references/python.Dockerfile` |

Also record the listening port, the writable paths the process needs, and the runtime
(Kubernetes / compose / ECS / Cloud Run) — the runtime decides whether `HEALTHCHECK` is worth
anything (see step 5).

## Step 2 — Resolve base image digests

**Never write a tag or digest from memory.**

```bash
# resolve the current digest for the tag you intend to use
docker buildx imagetools inspect <IMAGE>:<TAG> --format '{{ .Manifest.Digest }}'
# confirm it is multi-arch if you build for arm64 too
docker buildx imagetools inspect <IMAGE>:<TAG> --raw | jq -r '.manifests[]?.platform | "\(.os)/\(.architecture)"'
```

Write it as `FROM <IMAGE>:<TAG>@sha256:<DIGEST>`. If you cannot resolve it (no network, no
daemon), leave the placeholder, add `# TODO(resolve):` with this command, and list it in the
summary.

Pinning by digest without a refresh job means shipping stale, vulnerable base layers forever.
Add a scheduled workflow that re-resolves the digests and opens a pull request, so a human sees
the diff. Weekly is a reasonable cadence.

## Step 3 — Write `.dockerignore` first

This is the highest-value five lines in the whole task. Without it, `node_modules`, `.git`,
`target/`, local `.env` files and test fixtures are uploaded to the daemon and frequently land in
a layer via `COPY . .` — leaking history and credentials as well as bloating the image.

Start from `references/dockerignore.template`, then verify:

```bash
du -sh .                                   # what is on disk
docker build --progress=plain . 2>&1 | grep -i 'transferring context'
```

Target: transferred context **< 10 MB** for a typical application repository.

## Step 4 — Write the Dockerfile

Copy the matching template. The invariants, all enforced by
`references/hardening-checklist.md`:

1. **Multi-stage.** `deps` → `build` → `runtime`. The runtime stage starts from a minimal base,
   never from the build stage.
2. **Layer order:** manifest files → dependency install → source. Copying source first
   invalidates the dependency layer on every edit.
3. **Cache mounts** for package manager caches (`--mount=type=cache`) so they speed up builds
   without entering a layer.
4. **Secret mounts** (`--mount=type=secret`) for private registries. Never `ARG` — build args are
   visible in `docker history` to anyone who pulls the image.
5. **Numeric non-root `USER`.** `USER 10001:10001`, not `USER app`: the kubelet cannot resolve
   names, so `runAsNonRoot` does not work with a named user.
6. **Exec-form `ENTRYPOINT`.** `ENTRYPOINT ["node","server.js"]`. Shell form puts `/bin/sh` at
   PID 1, `SIGTERM` never reaches the application, and every redeploy drops in-flight requests
   after the grace period expires.
7. **One `RUN` per logical unit**, with cleanup inside the same `RUN`. Deleting files in a later
   layer does not shrink the image.
8. **OCI labels** for `source`, `revision` and `licenses`, so a scanner report can be traced back
   to a repository and a commit.
9. Compatible with `readOnlyRootFilesystem: true`: write only to explicitly mounted paths, and
   set `TMPDIR` if the runtime insists on `/tmp`.

## Step 5 — `HEALTHCHECK`: only where it is read

- **Kubernetes ignores `HEALTHCHECK` entirely.** Adding one for a Kubernetes-only image is dead
  weight that creates a false sense of coverage. The image's job there is to *expose* endpoints:
  a cheap liveness endpoint that makes no downstream calls, and a readiness endpoint that
  reflects this pod's ability to serve. Probe configuration belongs to `kubernetes-engineer`.
- **Compose and ECS do read it**, and in compose it is what makes
  `depends_on: { condition: service_healthy }` work — that is its real value here.
- Write the check with tools that exist in the image. Distroless images have no shell and no
  `curl`; either ship a tiny static health-check binary or put the check outside the image.

## Step 6 — Compose for local development

From `references/compose.dev.yaml`. It must give parity where parity matters and convenience
where it does not:

- The application service builds the **same Dockerfile**, targeting a `dev` stage where a
  watch-mode toolchain is acceptable — never a second, divergent Dockerfile.
- Dependencies (database, cache, broker) pinned by digest, with `healthcheck` and
  `depends_on: { condition: service_healthy }` so `up` does not race.
- Named volumes for data; bind mounts only for source. Bind-mounting over `node_modules` is the
  classic breakage — use an anonymous volume to shadow it.
- No secrets in the compose file. `env_file: .env.local`, and `.env.local` is in `.gitignore`.
- `docker compose config` must parse cleanly before you hand it over.

## Step 7 — Verify, with numbers

```bash
docker build -t <IMAGE>:local .
docker image ls --format '{{.Size}}' <IMAGE>:local           # size
docker history <IMAGE>:local --no-trunc | head -20           # layer origins
docker run --rm --entrypoint id <IMAGE>:local                # must not be uid=0
docker run --rm --entrypoint sh <IMAGE>:local -c \
  'command -v apt-get apk yum npm gcc' || echo "no toolchain in final stage (good)"
# SIGTERM handling: must exit well before the 10s default timeout
docker run -d --name sigterm-check <IMAGE>:local && time docker stop sigterm-check
# runtime constraints the cluster will impose
docker run --rm --read-only --cap-drop=ALL --tmpfs /tmp <IMAGE>:local
# scan by digest, fixable only
trivy image --severity HIGH,CRITICAL --ignore-unfixed <IMAGE>:local
```

Record before/after size and build times. Then emit `review.v1` to
`.foundry/blackboard/<wave>/container-engineer.json` via `blackboard_write`, with `metrics`
holding `sizeBytes`, `layers`, `buildSecondsCold`, `buildSecondsWarm`, `fixableCritical`,
`fixableHigh`, and one `finding.v1` per remaining defect citing the CIS Docker Benchmark or
NIST SP 800-190 section it breaks.

If `superpowers` is installed and the container misbehaves at runtime, invoke
`superpowers:systematic-debugging` before editing the Dockerfile — most "container bugs" are
configuration or signal-handling bugs, and random Dockerfile edits hide them.

## Rollback

Images are immutable; this is the cheapest rollback in the system, **provided tags were never
reused**.

1. Tag by git SHA and/or semantic version, never reuse a tag, and enable registry-side tag
   immutability where available.
2. Roll back by **digest**, not by tag:

```bash
kubectl get deploy/<NAME> -o jsonpath='{.spec.template.spec.containers[0].image}'
docker buildx imagetools inspect <REGISTRY>/<IMAGE>:<PREV-TAG> --format '{{ .Manifest.Digest }}'
```

3. Record the previous digest **before** rolling forward.
4. Do not delete a bad image from a shared registry: deletion breaks anything referencing it by
   digest and destroys the audit trail. Mark it deprecated and block its promotion by policy.
5. If the **base image** was compromised, rolling back your image is not enough — rebuild every
   image on that base, rotate every credential ever present in a build, and audit registry pulls.

## References

- `references/node.Dockerfile` — Node service, cache mounts, non-root, exec-form entrypoint.
- `references/angular-static.Dockerfile` — Angular build stage plus a non-root static server.
- `references/java-spring.Dockerfile` — layered Spring Boot extraction, JVM cgroup flags.
- `references/python.Dockerfile` — virtualenv copied between stages, hash-pinned installs.
- `references/dockerignore.template` — the starting point for `.dockerignore`.
- `references/compose.dev.yaml` — local stack with healthchecks and ordered startup.
- `references/hardening-checklist.md` — the full checklist with the reason behind each line and
  the command that verifies it.

## Deliberately not covered

- Runtime security enforcement (seccomp, AppArmor, admission policy, Falco). The image only has
  to be compatible with them.
- Image signing key management and trust-root policy — who may sign is a platform decision.
- Kubernetes manifests, probes and resources — `kubernetes-engineer`.
- Rewriting the application to handle `SIGTERM` or to start faster; this skill reports the defect
  and names the fix.
- Windows containers, and GPU base images.

## Exit criteria

- [ ] `.dockerignore` present; transferred build context **< 10 MB**.
- [ ] Multi-stage; the final stage contains **no package manager and no compiler**.
- [ ] Base pinned by `sha256:` digest, plus a scheduled digest-refresh PR job.
- [ ] `USER` is a **numeric** UID/GID ≠ 0; `docker run --entrypoint id` proves it.
- [ ] Exec-form `ENTRYPOINT`; `docker stop` returns in under the default 10 s grace period.
- [ ] Image runs with `--read-only --cap-drop=ALL`.
- [ ] **Zero fixable** CRITICAL and HIGH findings, or each has a suppression with an owner and an
      expiry date.
- [ ] OCI `source`, `revision`, `licenses` labels present.
- [ ] `HEALTHCHECK` present **only** if the target runtime reads it.
- [ ] `docker compose config` parses; `docker compose up` reaches a healthy state without manual
      ordering; no secrets in the compose file.
- [ ] Warm build **< 90 s**, cold build **< 5 min**, and the before/after size recorded.
- [ ] Every unresolved placeholder listed with the command that resolves it.
