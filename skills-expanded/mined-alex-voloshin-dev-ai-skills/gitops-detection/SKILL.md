---
name: gitops-detection
description: Use this skill when the agent is starting any Terraform or Helm change and needs to determine whether the apply flow is owned by a controller (in which case the change is a git PR, not a local imperative command) — for GitOps and orchestrator detection covering marker patterns and routing rules for Argo CD, Flux, Atlantis, HCP Terraform / Terraform Cloud, Spacelift, and env0. Loaded by `/infra-change` and related infrastructure workflows; not a workflow itself.
disable-model-invocation: true
---

# GitOps Detection — Route the apply before running it

Knowledge reference for detecting GitOps controllers and managed-apply layers in an infrastructure repository. Before running `terraform apply` or `helm upgrade` directly, check whether the repo's infra changes flow through a controller. If so, the change is a git PR, not an imperative command.

## Detection matrix

| Marker | System | Implication |
|---|---|---|
| `argocd/` directory or `Application` / `ApplicationSet` CRDs in Git | [Argo CD](https://argo-cd.readthedocs.io) (GitOps) | Push manifest changes to git; Argo CD reconciles. Do NOT `helm upgrade` directly — it will be reverted on next sync. Use `argocd app sync` or `kubectl argo rollouts promote` only when intentionally bypassing the loop. |
| `kustomization.yaml` + Flux `HelmRelease` / `Kustomization` CRDs | [Flux](https://fluxcd.io) (GitOps) | Push to git; Flux reconciles. Manual override: `flux reconcile kustomization <name>`. |
| `atlantis.yaml` (root) | [Atlantis](https://www.runatlantis.io) | Plans run in PR comments via `atlantis plan` / `atlantis apply`. Do NOT run `terraform apply` locally — Atlantis is the apply gate. |
| `terraform { cloud { ... } }` block in `.tf` files | [Terraform Cloud / HCP Terraform](https://cloud.hashicorp.com/products/terraform) | Plans/applies run in HCP Terraform UI/API. Local `terraform apply` is disabled by the cloud backend. |
| `.spacelift/` directory | [Spacelift](https://spacelift.io) | Stacks orchestrate plans/applies. Local apply forbidden. |
| `.env0/` or env0 stack tags | [env0](https://www.env0.com) | Same as Spacelift — managed apply layer. |

## What to check, in order

1. Look at the repo root for top-level files: `atlantis.yaml`, `.spacelift/`, `.env0/`, `argocd/`.
2. Grep `.tf` files for the `cloud { ... }` block inside a `terraform {}` configuration block.
3. Check Kubernetes manifests for Argo CD `Application` / `ApplicationSet` CRDs (apiVersion `argoproj.io/v1alpha1`) or Flux CRDs (apiVersion `helm.toolkit.fluxcd.io` / `kustomize.toolkit.fluxcd.io`).
4. Look for `kustomization.yaml` files paired with Flux CRDs — Kustomize alone is not GitOps; the Flux CRDs are the signal.

If multiple markers match (e.g., Argo CD for app manifests + Atlantis for Terraform), each domain routes independently to its controller.

## Routing rules

If a GitOps controller or managed-apply layer is detected:

1. **Plan the change as a git PR** against the manifest repo. Do not run local imperative commands.
2. **After PR approval and merge**, the controller reconciles automatically (GitOps) or runs the apply (Atlantis / HCP Terraform / Spacelift / env0).
3. **Skip the local `terraform apply` / `helm upgrade` steps** in the parent workflow.
4. **Verify reconciliation via the controller's status**:
   - Argo CD: `argocd app get <name>` (look for `SYNCED` + `HEALTHY`)
   - Flux: `flux get kustomizations` / `flux get helmreleases`
   - Atlantis: the PR comment thread (`atlantis apply` output)
   - HCP Terraform: the run page in the HCP UI / API
   - Spacelift / env0: the stack page in the vendor UI

## When local override is acceptable

Manual overrides exist for incident response but should be used sparingly and documented in the change record:

- Argo CD: `argocd app sync <name>` (force immediate reconcile)
- Flux: `flux reconcile kustomization <name>` / `flux reconcile helmrelease <name>`
- HCP Terraform / Spacelift / env0: trigger a run from the vendor UI

For long-term changes, always merge to the git source of truth — controllers will revert out-of-band changes on the next reconcile.

## When this applies

| Phase | Apply this knowledge |
|---|---|
| Step 0a — Detect orchestration / GitOps controllers | Run the detection matrix above before any plan or apply |
| Step 5 — Plan review | If controller detected, "plan" = the PR diff in the manifest repo |
| Step 6 — Apply | If controller detected, "apply" = PR merge + controller reconcile |
| Step 7 — Verify | Use the controller's status command to confirm reconciliation |

## Integration

- **Used by**: `/infra-change` (Step 0a — pre-flight routing decision)
- **Companion knowledge**: `@terraform-procedures` (commands deferred when HCP/Atlantis/Spacelift/env0 owns the apply), `@helm-procedures` (commands deferred when Argo CD/Flux owns the apply)
- **External references**: [Argo CD docs](https://argo-cd.readthedocs.io), [Flux docs](https://fluxcd.io/docs/), [Atlantis docs](https://www.runatlantis.io/docs/), [HCP Terraform docs](https://developer.hashicorp.com/terraform/cloud-docs), [Spacelift docs](https://docs.spacelift.io), [env0 docs](https://docs.env0.com)
