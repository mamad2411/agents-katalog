---
name: openchoreo-platform-engineer-gitops
description: Platform-engineer GitOps work for OpenChoreo — scaffolding a fresh GitOps repo or migrating an existing cluster, wiring Flux CD, and authoring platform resources (ComponentTypes, Traits, Workflows, Environments, DeploymentPipelines, SecretReferences, AuthzRoles, planes) via Git. Use when the user says 'scaffold an OpenChoreo GitOps repo', 'set up GitOps for this cluster', 'move this cluster to GitOps', 'wire Flux for OpenChoreo', 'add a ComponentType via Git', 'commit a new trait/workflow/environment to the GitOps repo', or operates a PE-side change from inside a scaffolded GitOps repo.
metadata:
  version: "1.0.0"
---

# OpenChoreo Platform-Engineer GitOps Guide

Git is the source of truth; the cluster is its reflection. This skill writes OpenChoreo **platform** resources to Git, lets a CD tool (Flux CD today) reconcile them, and reads cluster state with `occ` to verify. Authoritative reading: <https://openchoreo.dev/docs/platform-engineer-guide/gitops/>.

This skill is scoped to platform-engineer GitOps work — scaffolding the repo, wiring Flux, and authoring platform CRDs via Git. Application-level GitOps (Project / Component / Workload / ComponentRelease / ReleaseBinding) and non-GitOps cluster operations (Helm install, direct CRD edits against the API server) are out of scope; tell the user when a task crosses that boundary.

## Step 0 — Detect the mode

Two modes; pick before doing anything.

```bash
# Cwd indicators a scaffolded OpenChoreo GitOps repo
ls flux 2>/dev/null && ls platform-shared 2>/dev/null && ls namespaces 2>/dev/null
```

- **Scaffolding mode** — cwd is empty or not yet a GitOps repo. Go to [`references/setup.md`](./references/setup.md). Includes both *fresh scaffold* and *migrate an existing cluster*.
- **Operating mode** — cwd is a scaffolded repo (has at least `flux/` or equivalent CD-tool dir, `platform-shared/`, `namespaces/`). Skip setup; jump to the relevant recipe under [`references/recipes/`](./references/recipes/).

If unsure, ask the user.

## Step 1 — Verify `occ` and the current context (always)

`occ` is the **only** tool this skill uses against OpenChoreo. Before any action that touches the cluster or reads cluster state to seed a repo:

```bash
command -v occ                   # installed?
occ config context list          # current context, control plane, namespace
occ namespace list               # smoke test the connection
```

If `occ` isn't installed or no context is set, follow [`references/setup.md`](./references/setup.md) §1.

**Always confirm the active context with the user before any destructive or seeding action.** Scaffolding-from-cluster and Flux wiring reach into a live cluster — point them at the wrong control plane and the wrong cluster's resources end up in Git, or Flux starts reconciling the wrong source against the wrong target. Use `AskUserQuestion` with the current context name prefilled. Don't proceed on assumption.

## Step 2 — Load concepts and authoring

Read once per session before authoring anything:

- [`references/concepts.md`](./references/concepts.md) — resource hierarchy, sync ordering, immutability, verification ladder, drift recovery.
- [`references/authoring.md`](./references/authoring.md) — `occ` file-mode generators, `llms.txt` API-reference approach, repo path conventions, git workflow, DCO.

For CEL inside ComponentType / Trait / Workflow templates, load [`references/cel.md`](./references/cel.md) only when you're actually writing or reviewing CEL.

## What this skill can do

- **Scaffold a fresh GitOps repo and wire Flux** → [`recipes/scaffold-fresh.md`](./references/recipes/scaffold-fresh.md)
- **Migrate an existing cluster to GitOps** — inventory via `occ`, capture the resources the user picks, wire Flux → [`recipes/scaffold-from-cluster.md`](./references/recipes/scaffold-from-cluster.md)
- **Install the build-and-release workflow bundle** from [`sample-gitops`](https://github.com/openchoreo/sample-gitops) — Workflow CRs + the Argo `ClusterWorkflowTemplate`s they reference, plus the git-token / gitops-token secrets they read → [`recipes/install-build-release-workflows.md`](./references/recipes/install-build-release-workflows.md)
- **Author a (Cluster)ComponentType** → [`recipes/author-componenttype.md`](./references/recipes/author-componenttype.md)
- **Author a (Cluster)Trait** → [`recipes/author-trait.md`](./references/recipes/author-trait.md)
- **Author a (Cluster)Workflow** (build template or generic automation) → [`recipes/author-workflow.md`](./references/recipes/author-workflow.md)
- **Author Environments + DeploymentPipeline + default Project** → [`recipes/author-environment-pipeline.md`](./references/recipes/author-environment-pipeline.md)
- **Author a SecretReference** (consumes a `ClusterSecretStore`) → [`recipes/author-secret-reference.md`](./references/recipes/author-secret-reference.md)
- **Author AuthzRoles and bindings** (cluster- or namespace-scoped) → [`recipes/author-authz.md`](./references/recipes/author-authz.md)
- **Author other PE-side resources** — DataPlane / WorkflowPlane / ObservabilityPlane (and Cluster variants), ObservabilityAlertRule, NotificationChannel → [`recipes/author-other-resources.md`](./references/recipes/author-other-resources.md)
- **Verify reconciliation; recover from drift** → [`recipes/verify-and-recover-drift.md`](./references/recipes/verify-and-recover-drift.md)

## What this skill cannot do

- **Application-level GitOps** — `Project`, `Component`, `Workload`, `ComponentRelease`, `ReleaseBinding`, workload descriptor authoring. Out of scope; tell the user when the task crosses into application territory.
- **Helm install of OpenChoreo control plane / planes.** Assumes a running control plane. Refer to the docs at <https://openchoreo.dev/docs/getting-started/>.
- **Imperative ops** — triggering a `WorkflowRun`, `kubectl exec`, runtime log tail, direct CRD edits against the API server. `WorkflowRun` does **not** belong in Git (per `gitops/overview.md`); trigger via the UI, webhook, or `occ component workflow run`.
- **External-system admin** — Git provider webhook config, IdP / SSO, Vault / AWS Secrets Manager / OpenBao backend setup. The skill wires only the OpenChoreo-side `SecretReference` / `ClusterSecretStore` resources, not the upstream store.
- **CD tools other than Flux CD.**

## Tool surface

| Tool                              | Purpose                                                                                                                              |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `occ`                             | Reads cluster state (`<kind> get`, `<kind> list`), authenticates (`login`, `config`), pre-Flux bootstrap (`apply -f` — single file). |
| `git` + host CLI (`gh` / `glab` / `bb` / …) | Branch, `commit -s`, push, PR + wait-for-merge.                                                                            |
| `flux` (preferred) or `kubectl`   | Verify Flux `GitRepository` / `Kustomization` status; bootstrap Flux's view of the repo.                                             |
| WebFetch                          | `llms.txt` and the API-reference pages it indexes (for CRD shapes `occ` doesn't generate).                                           |
| `AskUserQuestion` (or equivalent) | Confirm context, repo pattern, remote, before-Flux-wiring decisions.                                                                 |

## Working style

- **Git is the source of truth.** GitOps-managed resources change only through Git. `occ apply -f` is reserved for pre-Flux one-shot bootstrap.
- **Pin every CRD shape** to either an `occ` generator or the API reference on `llms.txt` for the running `occ` minor. See [`authoring.md`](./references/authoring.md).
- **Always `git commit -s`** (DCO is required upstream). Default flow is PR + wait-for-merge; direct push only when the repo profile says so.
- **Verify, don't assume.** Reconciliation is interval-based (documented `GitRepository: 1m`, `Kustomization: 5m`); read the result back with `occ <kind> get` after the merge.
- **Ask, don't assume the cluster identity.** Confirm the `occ` context every session, especially before seeding from cluster or wiring Flux.
- **Don't open a PR or push without explicit user confirmation.** Local commits are reversible; remote-visible actions are not.

## Stable guardrails

- **Sync ordering** — `platform-shared/` before `namespaces/<ns>/platform/` before `namespaces/<ns>/projects/`, via Flux `dependsOn`. Documented in `gitops/using-flux-cd.mdx`.
- **No plaintext secrets in Git** — use `SecretReference` (per `gitops/overview.md` *Secrets Management*).
- **Protect `platform-shared/` with CODEOWNERS** — cluster-scoped changes affect every namespace. Sample at [`assets/codeowners-platform-shared`](./assets/codeowners-platform-shared).
- **`update_*` semantics differ from `kubectl apply` on some CRDs** — but in GitOps mode Flux re-applies the full file every reconcile, so YAML-side edits are full-spec by definition. Don't hand-edit half a spec and expect a partial patch.

## Anti-patterns

- Scaffolding without confirming the `occ` context — silently seeding the wrong cluster's resources into Git.
- Wiring Flux before the user has confirmed the remote URL — Flux will start pulling from somewhere unexpected.
- Pushing or opening a PR before the user has reviewed the commit list.
- Hand-authoring large CRDs (ComponentTypes / Workflows) from memory instead of templating from `occ <kind> get` or pulling shape from `llms.txt`.
- Treating cluster reads as authoritative *after* GitOps is wired — once Flux is reconciling, Git is the source of truth; `occ <kind> get` is now the verification primitive, not the authoring primitive.
- Inventing tooling the user didn't ask for (kustomize overlays, custom controllers, helper scripts). Stay on the documented Flux Kustomization chain.
