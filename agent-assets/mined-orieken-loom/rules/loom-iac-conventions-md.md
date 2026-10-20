# Infrastructure-as-Code Conventions

Cross-references `shared/rules/architecture-guardrails.md` #3 (no hardcoded secrets). These rules apply to every IaC file the `devops-engineer` agent touches.

---

## Terraform / OpenTofu

ALWAYS pin explicit versions for every provider and module — no floating `~>` without a lower-bound patch.
ALWAYS use remote state with locking (S3 + DynamoDB, GCS, Terraform Cloud, etc.) — no local `terraform.tfstate` in source.
NEVER hardcode credentials, account IDs, or tokens — use `var.*` backed by a secrets manager reference or environment variable.
ALWAYS run `terraform fmt` and `tflint` before committing — treat lint failures as build failures.
ALWAYS use module boundaries to separate environment config from resource definitions — one module per concern.
NEVER run `terraform apply` without a reviewed `terraform plan` output — this is an Approval Gate.
ALWAYS tag every resource with at minimum `environment`, `owner`, and `project` tags.
NEVER commit `.tfvars` files containing real secrets — use `.tfvars.example` with placeholder values only.

## Module Layout

```
infra/
├── modules/           ← reusable, no environment knowledge
│   └── <service>/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── environments/
    ├── staging/
    │   └── main.tf    ← calls modules, sets env-specific vars
    └── production/
        └── main.tf
```

---

## Dockerfile

ALWAYS use multi-stage builds — build artifacts in a builder stage, copy only what's needed into the final image.
ALWAYS switch to a non-root `USER` before the final `CMD` or `ENTRYPOINT`.
ALWAYS use minimal base images (`distroless`, `alpine`, or official slim variants) — never `ubuntu:latest` or bare `debian`.
NEVER use `latest` as a base image tag — pin to a specific digest or version tag.
NEVER install packages with `apt-get` / `apk add` without pinning a version (`apt-get install curl=7.x.x`).
NEVER store secrets, API keys, or passwords in `ENV` or `ARG` instructions — secrets must be injected at runtime.
ALWAYS set `WORKDIR` explicitly — never rely on the default working directory.
ALWAYS use `.dockerignore` to exclude `.git`, `node_modules`, secrets, and build artifacts from the build context.

---

## Kubernetes / Helm

ALWAYS set `resources.requests` and `resources.limits` on every container — omitting them blocks scheduling predictability.
NEVER use `image: *:latest` in any manifest or Helm values file — pin to a specific SHA or immutable tag.
ALWAYS create a dedicated `ServiceAccount` per application — never use the `default` service account.
ALWAYS apply RBAC (`Role` + `RoleBinding`) scoped to the minimum permissions the workload needs — ClusterRole only when namespace scope is genuinely insufficient.
ALWAYS define `NetworkPolicy` for every namespace — default-deny all ingress and egress, then allow only required paths.
NEVER store secrets as plain-text `Secret` manifests in source control — use ExternalSecrets Operator, Sealed Secrets, or Vault Agent Injector.
ALWAYS set `readinessProbe` and `livenessProbe` — without them Kubernetes cannot route traffic or restart unhealthy pods.
ALWAYS set `podDisruptionBudget` for production workloads to prevent full-cluster drain during rolling updates.

---

## GitHub Actions

ALWAYS pin action versions to a full commit SHA, not a mutable tag (`uses: actions/checkout@abc1234` not `@v4`).
ALWAYS declare an explicit `permissions:` block at the job or workflow level — default is read-all, which is too broad.
NEVER echo secrets in `run:` steps — use `::add-mask::` or rely on the automatic masking of `${{ secrets.* }}` variables only.
NEVER use `pull_request_target` with an explicit checkout of the PR branch unless you have verified the workflow does not expose repository secrets to untrusted code — this is a critical TOCTOU attack surface.
ALWAYS scope `GITHUB_TOKEN` permissions to `contents: read` unless a step specifically needs write access (and then scope only that step).
ALWAYS use `if: github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository` to guard secrets from fork PRs.
NEVER store third-party credentials in repository variables — use environment-scoped secrets with required reviewers for production environments.
ALWAYS run security-sensitive jobs (deploy, publish) only after all test and lint jobs have passed — use `needs:` dependencies explicitly.

---

*Part of the [ai-assistant-dot-files](https://github.com/orieken/loom) Context Engineering Framework by Oscar Rieken — licensed under [CC BY 4.0](https://github.com/orieken/loom/blob/main/LICENSE-CONTENT.md). If you copy or adapt this file, please keep this attribution.*
