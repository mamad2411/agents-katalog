---
name: containerization-and-iac
description: Use this skill for any decision about how an app is packaged, provisioned, and deployed to a runtime — Docker images, local dev parity, and infrastructure-as-code. Trigger it on "write a Dockerfile", "containerize this", "dockerize", "docker-compose for local", "spin up Postgres/Redis locally", "my image is huge/slow to build", "deploy this somewhere", "deploy to Fly/Railway/Render/Cloud Run/ECS/Fargate/Kubernetes", "put this on a server", "set up infra", "provision a database/redis/bucket", "Terraform this", "Pulumi", "write IaC", "spin up the cloud resources", "least-privilege IAM for this service", "where should this app run". Strongly prefer this skill over improvising a Dockerfile or clicking around a cloud console, even when the user never says "Docker", "container", or "infra". Cardinal rule: use the highest-level platform that fits (managed > container > orchestrator), keep images minimal and non-root, and make every infra change planned, reviewed, and reversible. It does NOT write app code, design DB schemas, build CI pipelines, or run runtime monitoring — it hands those to the right skills. It has a STRONG bias against premature containerization and premature Kubernetes: if Vercel fits, don't containerize; if a container fits, don't reach for K8s.
---

# Containerization & IaC

This skill decides **how an app is packaged, provisioned, and shipped to a runtime** — and keeps that decision honest across sessions. It is the deploy-substrate companion to `ci-cd-and-automation` (which wires the pipeline) and `shipping-and-launch` (which runs the launch). Those decide *how code moves*; this decides *what it runs on*.

**Cardinal rule — climb the platform ladder only as far as you must.** The default target is a managed platform (Vercel for the Next.js house stack). A container is the *escape hatch* you reach for when a managed platform genuinely doesn't fit — not the starting point. Kubernetes is the escape hatch from the escape hatch, justified only by real multi-service scale. **Over-provisioning is as much a failure as under-provisioning — premature K8s is a red flag, flag it as loudly as an insecure image.**

**Second rule — minimal, non-root, reproducible images; planned, reversible infra.** Every image is multi-stage, runs as a non-root user, pins its base, and gets scanned. Every infra change goes `plan → review → apply` and has a rollback path. No manual console clicks as the source of truth — the console is for reading, not for provisioning.

---

## Sections

```
0. ROUTE            → read what's there, then dispatch on the request
1. CHOOSE TARGET    → managed vs container-PaaS vs managed-container vs K8s
2. CONTAINERIZE     → the Dockerfile (multi-stage, slim, non-root, scanned)
3. COMPOSE          → local dev parity (app + Postgres + Redis + queue)
4. PROVISION        → IaC (Terraform / Pulumi / platform CLI) — or not yet
5. SECURE + SHIP    → SECURE gate, then hand to ci-cd / shipping
6. VERIFY           → image builds & runs, plan is clean, deploy is reversible
```

CHOOSE TARGET is the front door. Almost every real invocation starts there — you cannot write a Dockerfile or a Terraform module for a target you haven't chosen. Do not skip to CONTAINERIZE because the user said "write a Dockerfile"; confirm a container is even the right answer first (often it is not).

---

## Section 0 — ROUTE

Read what already exists before recommending anything: any `Dockerfile`, `docker-compose.yml`, `fly.toml`/`railway.json`/`render.yaml`, `*.tf`/`Pulumi.yaml`, `vercel.json`, and `next.config.js` (is `output: 'standalone'` set?). Then dispatch:

- "Where should this run?" / "deploy this" → **CHOOSE TARGET** (the default entry).
- "Write/fix a Dockerfile", "my image is huge" → confirm target, then **CONTAINERIZE** (`references/docker.md`).
- "Local setup with a DB/Redis" → **COMPOSE** (`references/compose-and-local.md`).
- "Terraform/Pulumi this", "provision X" → **PROVISION** (`references/iac.md`).
- Anything touching IAM / secrets / public-facing resources → the **SECURE gate is mandatory** (see Orchestration).
- Ambiguous → run **CHOOSE TARGET**; it is read-only and always safe.

---

## Section 1 — CHOOSE TARGET (the decision that dominates the rest)

Read `references/deploy-targets.md`. Classify the workload (framework, statefulness, number of services, traffic, team ops capacity, budget), then pick the **lowest platform tier that fits** — climbing later is a config change; unwinding a Kubernetes cluster you never needed is a project. The ladder:

1. **Managed platform** (Vercel / Netlify) — the default for Next.js and static/edge-first apps. No container, no Dockerfile.
2. **Container PaaS** (Fly.io / Railway / Render) — when you need a long-running server, a container, background workers, or a bundled DB, but not orchestration.
3. **Managed containers** (Google Cloud Run / AWS ECS-Fargate) — when you're already in a cloud, need scale-to-zero or fine IAM, still no cluster to babysit.
4. **Kubernetes / Helm** — only at real scale: many services, multi-team, sophisticated traffic/rollout needs. Justify it against the tier below, in writing.

Name the tier above and the concrete trigger to climb. **If Vercel fits, say so and stop** — don't write a Dockerfile nobody needs.

---

## Section 2 — CONTAINERIZE (only once a container is the chosen target)

Read `references/docker.md`. Produce a **multi-stage** Dockerfile: a build stage and a minimal runtime stage. For the Next.js house stack, use `output: 'standalone'` and copy only `.next/standalone` + `.next/static` + `public` — this is the single biggest image-size win. Non-negotiables: pin the base (`node:22-slim` or distroless, never bare `:latest`), run as a **non-root user**, add a `.dockerignore`, order layers for cache hits (deps before source), add a `HEALTHCHECK`, and scan the image. Go binaries and Python services containerize differently — the reference covers both.

---

## Section 3 — COMPOSE (local dev parity)

Read `references/compose-and-local.md`. `docker-compose.yml` gives the team one command for app + Postgres + Redis + queue, with healthcheck-gated `depends_on`, named volumes for data, a shared network, and an `.env` file that carries **dev-only** secrets (never prod credentials). Compose is for *local parity*, not production. When compose covers local dev and the target is a managed platform, you're done — don't invent an orchestrator you won't run.

---

## Section 4 — PROVISION (IaC — or explicitly not yet)

Read `references/iac.md`. For a solo prototype on a managed platform, the platform CLI/dashboard *is* fine — IaC before you have infra worth versioning is ceremony. The moment infra becomes real (multiple resources, more than one environment, more than one person), commit it to code: **Terraform** (the default; huge provider ecosystem, mature state tooling) or **Pulumi** (real languages, when you want types/loops over HCL). Non-negotiables: remote state backend with locking, small reviewable modules, **least-privilege IAM**, `plan` reviewed in CI with policy checks (tfsec/checkov/OPA), and drift detection. Destructive changes get the discipline below.

---

## Orchestration

This skill owns the substrate decision and its artifacts; it delegates everything else. Route skill selection through **`decider`** (this repo's standard router) and slot into the default pipeline `PLAN → EXECUTE → [SECURE/A11Y/PERF] → REVIEW → TEST → VERIFY` — this skill owns PLAN/EXECUTE for *deploy substrate*, then feeds the closing gates:

- **SECURE (mandatory here)** — any change touching IAM/least-privilege, secrets, or public-facing resources runs the SECURE gate: pair with **`security-and-hardening`** and **`env-secrets-manager`**, and get the **infra-reviewer** agent to sign off before apply. Image/dependency scanning goes to **`tob-supply-chain`** + **`cybersec-vuln-scanner`**. This gate is never skipped for infra with a public surface or a privilege grant.
- **Destructive / irreversible infra** (deleting a stateful resource, replacing a DB, a `terraform apply` that shows `-/+`) → insert **`doubt-driven-development`** *before* applying. A wrong apply here is not a revert, it's data loss.
- **File placement / where infra files live** → **`arch`**. **Runtime telemetry, logs, dashboards, alerts** → **`observability-and-monitoring`**. **DB provisioning + migration coordination** → **`database-schema-designer`** and the **db-migration-reviewer** agent (a migration inside a deploy is its own risk surface).
- **CI wiring** (build/push image, run `terraform plan` in CI, deploy step) → **`ci-cd-and-automation`**. **Launch execution** (rollout, canary, rollback plan, monitoring on) → **`shipping-and-launch`**. **Backend/runtime code** → **`backend-engineering`**.
- **REVIEW → TEST → VERIFY** always close the loop: **`code-review`** / **`simplify`** on the config, **`verify`** / **`run`** to actually build and boot the image, **`verification-before-completion`** before calling it done. A failed apply for a non-obvious reason → **`systematic-debugging`** (or **`debugging-and-error-recovery`** for CI-only failures). Record the substrate decision with **`documentation-and-adrs`**; **`git-workflow-and-versioning`** for the commit.

Reviewer agents to invoke by name when the surface matches: the **infra-reviewer** agent (IaC safety, IAM, public-resource blocking, rollback), the **devops** agent (the actual deploy), the **db-migration-reviewer** agent (migrations), the **security-officer** and **cmmc-reviewer** agents (regulated/gov surfaces). Read a chosen skill's own `SKILL.md` before running it.

---

## Enforcement over vibes

A Dockerfile that "should be" small and an infra change that "should be" safe are worthless — enforce it. Emit the machinery that makes violations **fail**: image scanning in CI (Trivy/Grype/Docker Scout) with a severity gate, a `.dockerignore` that actually excludes secrets and `node_modules`, a non-root `USER` line, `terraform plan` posted to the PR with `tfsec`/`checkov`/OPA policy as a required check, remote state with locking so two applies can't race, and drift detection on a schedule. An unscanned image and an unreviewed `apply` are the two most common ways infra goes wrong — close both with automation, not prose.

---

## Operating principles

- **Highest platform that fits.** Managed > container > orchestrator. Vercel-first for the house stack; a container is the escape hatch; K8s is the escape hatch from the escape hatch.
- **Don't containerize by reflex.** "Write a Dockerfile" often has the correct answer "you don't need one — deploy to Vercel." Say it.
- **Premature K8s is a defect.** Flag over-provisioning as loudly as under-provisioning. Justify every cluster against Cloud Run/ECS in writing.
- **Minimal, non-root, pinned, scanned.** Every image, every time. Multi-stage by default; distroless/slim over full; `USER` is not optional.
- **Infra is code, not clicks.** The console reads; code provisions. `plan → review → apply`, reversible, with remote state.
- **Destructive changes get doubt.** A DB deletion or resource replacement is irreversible — route through `doubt-driven-development` before apply.
- **SECURE gate is mandatory** for IAM, secrets, and public resources. Never ship a public bucket or a wildcard IAM role.
- **Delegate.** This skill picks the substrate and writes its config; `decider` routes; `security-and-hardening`/`env-secrets-manager` harden; `ci-cd-and-automation`/`shipping-and-launch` move the code; `database-schema-designer` owns migrations.
- **Match the user's language** (Russian, Uzbek, English).
- **Stack-aware.** Defaults tuned to Next.js 15 (`output: 'standalone'`) + Node services on Vercel-first; Go binaries → scratch/distroless static images; Python → slim + venv/uv layering (see `references/docker.md`).

---

## Worked examples (abbreviated)

**"Containerize my Next.js app and deploy it."**
ROUTE → CHOOSE TARGET *first*. It's a standard Next.js 15 App Router app, no long-running workers, no exotic runtime. **Recommendation: don't containerize — deploy to Vercel**, which fits the house stack natively and beats a hand-rolled container on DX, edge, and Lighthouse. Only if the user has a hard constraint (must run on their own AWS, needs a persistent socket) do we drop to a container PaaS. If so: multi-stage Dockerfile with `output: 'standalone'`, non-root, Fly.io as the target, image scan in CI. No Dockerfile written until the target is confirmed.

**"Set up local dev with Postgres and Redis, and my image is 1.2 GB."**
Two things. COMPOSE: a `docker-compose.yml` with app + `postgres:16` + `redis:7`, healthcheck-gated `depends_on`, named volumes, `.env` with dev-only creds. CONTAINERIZE: the 1.2 GB is almost certainly a single-stage build shipping `node_modules` + source + the full `node` image. Fix = multi-stage + `output: 'standalone'` + distroless runtime → typically ~150 MB. Verify by building and booting; scan before it's "done".

**"Terraform our infra — a Cloud Run service, a Postgres, a bucket."**
PROVISION, but SECURE gate is mandatory (IAM + a public-capable bucket). Terraform with a remote GCS/S3 state backend + locking, split into small modules, least-privilege service account (no `roles/owner`), bucket **not** public with `tfsec` proving it. `plan` posted to the PR, `security-and-hardening` + the infra-reviewer agent sign off, DB creation coordinated with `database-schema-designer` and the db-migration-reviewer agent. The bucket-delete in the plan → `doubt-driven-development` before apply. Reversible, reviewed, then hand the deploy step to `ci-cd-and-automation`.
