---
name: containerize-and-ship-a-service
description: Use when writing a Dockerfile or a CI/CD pipeline for a backend service — a multi-stage build (heavy builder → slim runtime), base images pulled through a dependency proxy / private registry, authenticating to private package registries during build and SCRUBBING those creds before the final stage, lockfile-first layer caching, purpose-specific images (app / DB-migration job / test), and a CI pipeline (install → lint → test → build → push → migrate → deploy) kept thin per repo by including one shared org template, with per-branch→environment deploy rules and secrets from CI variables (never baked in). Docker + GitLab CI reference, framework-flexible.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Containerize & ship a service

How a backend service is **built into an image** and **shipped through CI/CD**. Examples are Docker +
GitLab CI with a Node/pnpm service; the principles port to any stack/CI. principle → **▸ Example** →
**▸ Other stacks**. Branch→release flow itself is `git-flow`; DB migration rules are `database-migrations`;
release backward-compat is `release-safety` — this skill is the *build + pipeline* mechanics.

## Core principle
**A small, reproducible image with NO secrets baked in, shipped by a thin per-repo pipeline that
includes one shared template, gated by branch.** Build creds live only in a throwaway build stage;
runtime secrets come from the environment at deploy; the pipeline is maintained once, not per service.

## 1. Multi-stage build — heavy builder → slim runner
Compile in a builder stage; copy only the build output + production deps into a clean runtime stage, so
toolchains/dev-deps never ship.
```dockerfile
FROM <registry>/node:22-alpine AS builder
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@<ver> --activate
COPY package.json pnpm-lock.yaml ./          # manifest first (cache) — see §4
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build && pnpm store prune

FROM <registry>/node:22-alpine AS runner      # clean runtime base
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
COPY --from=builder /app/dist ./              # only the build output
RUN corepack enable && pnpm install --prod --frozen-lockfile && pnpm store prune
EXPOSE 3000
CMD ["node", "main.js"]
```
▸ *Other stacks:* `go build` in a builder → `scratch`/`distroless` runner; a JVM build → a JRE-only
runtime image; Python wheels built then copied. Principle: **build heavy, run slim**.

## 2. Base images through a dependency proxy / private registry
Pull bases via a **dependency proxy** (or your private registry mirror), not Docker Hub directly —
avoids rate limits and pins your supply chain. Pin exact versions (`node:22-alpine3.22`), not `latest`.
```dockerfile
ARG CI_DEPENDENCY_PROXY_DIRECT_GROUP_IMAGE_PREFIX
FROM ${CI_DEPENDENCY_PROXY_DIRECT_GROUP_IMAGE_PREFIX}/node:22-alpine3.22 AS builder
```
▸ *Other stacks:* an ECR/Artifact Registry pull-through cache; a Harbor/Nexus proxy. Principle: a
controlled, pinned base source.

## 3. Private deps during build — inject, then SCRUB before the final stage
Installing private packages needs a credential — pass it as a **build `ARG`**, use it, then **delete it
in the same stage**, and rely on multi-stage so it never reaches the runtime image. Two common forms:
```dockerfile
# (a) registry token
ARG CI_JOB_TOKEN
RUN echo "//gitlab.com/api/v4/packages/npm/:_authToken=${CI_JOB_TOKEN}" >> .npmrc
RUN pnpm install --frozen-lockfile && rm -f .npmrc          # scrub

# (b) SSH key for git+ssh deps
COPY id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa && ssh-keyscan gitlab.com > /root/.ssh/known_hosts \
 && git config --global url."git@gitlab.com:".insteadOf "https://gitlab.com/"
RUN pnpm install --frozen-lockfile && rm -f /root/.ssh/id_rsa   # scrub
```
**Never** `COPY` a secret into the runtime stage, and never bake one into an `ENV`/layer — `docker
history` exposes it. ▸ *Other stacks:* BuildKit `--mount=type=secret` (best — never lands in a layer at
all), or a build-only stage. Principle: credentials are build-time only and disposable.

## 4. Layer caching — manifest first
Copy the dependency manifest + **lockfile** first and install, *then* copy source — so the (slow)
install layer is cached and only rebuilds when deps change. Always install from the **lockfile**
(`--frozen-lockfile` / `npm ci`) for reproducibility.
▸ *Other stacks:* `go.mod`/`go.sum` then `go mod download`; `pom.xml` then `mvn dependency:go-offline`;
`requirements.txt`/`poetry.lock` first. Same idea everywhere.

## 5. Purpose-specific images — one concern each
Don't overload one image. Common split:
- **app** — the long-running service: `CMD ["node", "main.js"]`.
- **migration** — a **run-once Job**, not a service: `CMD pnpm run dbm:run && pnpm run dbs:run` (apply
  migrations + seeds, then exit). Run it as a gated pre-deploy step (§8), never inside the app's start.
- **test** — dev deps + the test runner, used only in CI.
▸ *Other stacks:* a migration init-container/Job; a separate test image/target. Principle: build, test,
migrate, and serve are different lifecycles — different images/targets.

## 6. The CI pipeline — stages
A typical backend pipeline, in order, failing fast:
`install → lint → test → build image → push → migrate → deploy`.
- **Tests hit real deps**: declare Postgres/Redis as **CI service containers** (or a compose file) so
  integration tests run against a real DB, not mocks.
- **Cache** the dependency store between runs; pass build output as **artifacts** to later stages.
- **Tag the image** with the commit SHA (and the semver tag on a release) so every deploy is traceable.
▸ *Other stacks:* GitHub Actions jobs, CircleCI workflows, Jenkins stages — same ordering + a
service/sidecar DB for tests.

## 7. Keep each repo's pipeline thin — include a shared template
Each service's CI file is just **variables + an `include` of one org-wide template**, so the pipeline
(stages, build, deploy) is written once and every service inherits fixes/upgrades.
```yaml
# a service's .gitlab-ci.yml — the whole thing
variables:
  SERVICE_NAME: "your-service"
  NODE_OPTIONS: "--max_old_space_size=4096"
include:
  - project: "<org>/ci-templates"
    ref: master
    file: "/backend/gitlab-ci.yml"
```
▸ *Other stacks:* GitHub **reusable workflows** (`uses: org/.github/.../x.yml@ref`), CircleCI **orbs**, a
Jenkins shared library. Principle: centralize the pipeline; per-repo config is a few variables.

## 8. Per-branch → environment + secrets
- **Gate deploys by branch**, mirroring `git-flow`: merges to `develop` → **staging**, a release
  tag / `master` → **production** (manual approval for prod). Run the **migration Job before** the app
  deploy; abort the deploy if it fails.
- **Secrets come from CI variables** (masked + protected, protected branches only) and are injected as
  **environment variables at deploy** — never `COPY`'d or `ARG`'d into the image. App config follows the
  config/env rules (validated on boot).
▸ *Other stacks:* environment-scoped secrets (GitHub Environments, Vault, SSM) injected at runtime;
branch/tag-filtered deploy jobs.

## Verification
- **No secrets / no toolchain in the runtime image:** `docker history --no-trunc <image> | grep -iE 'authtoken|id_rsa|\.npmrc|secret|password'` → empty; `docker run --rm <image> gcc --version` → "not found" (slim runner, no build toolchain); runtime image size << builder.
- **Pinned bases via proxy, lockfile installs:** `grep -nE 'FROM .*:latest' Dockerfile` → empty (exact tags only); `grep -n 'frozen-lockfile\|npm ci' Dockerfile` present; `FROM` lines reference the dependency-proxy/registry prefix, not `docker.io` directly.
- **Cache order + split images:** in the Dockerfile the `COPY` of the manifest+lockfile precedes `COPY . .`; the app image's `CMD` starts only the server — `grep -n 'dbm:run\|migration' Dockerfile` shows migrations are a separate image/Job, never in app start.
- **Thin pipeline, gates before ship:** the repo CI file is basically `variables:` + one `include:` (`grep -c 'include:' .gitlab-ci.yml` = 1); the shared template runs `lint`+`test` against real service-container deps (Postgres/Redis) **before** `build`/`deploy`.
- **Branch-gated deploys, env-injected secrets:** CI rules map `develop`→staging and tag/`master`→prod, with the migration Job gated **before** the app deploy; runtime secrets are masked CI variables injected as env (the `docker history` check above confirms none are baked into a layer).

## Related
- `git-flow` — the branch→release flow these deploy rules mirror.
- `database-migrations` — what the migration Job runs (additive, reversible, ordered before deploy).
- `release-safety` — backward-compat + rollout gating around a deploy.
- `structure-a-backend-service` (the app being built) · global *Config & Environment Rules*.
