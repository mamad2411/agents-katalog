---
name: manage-k8s-iam
description: >
  Provision and sync Kubernetes RBAC resources — RoleBindings, ClusterRoleBindings, and
  ServiceAccounts — from a core-iam.yaml and tenant.yaml definition. Maps platform roles
  (`Role("reader")`, `Role("contributor")`, `Role("admin")`, Operator) to Kubernetes built-in ClusterRoles within tenant
  namespaces. Uses the Kubernetes MCP server. Use when applying or updating RBAC after
  running define-core-iam or define-tenant-iam, or when onboarding a new tenant namespace.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "5"
---

# Manage Kubernetes IAM

## Skill Type

Implementation

## System Requirements

- **Kubernetes MCP server** configured and authenticated. The agent will use Kubernetes MCP tools to call the Kubernetes API (`rbac.authorization.k8s.io`, `v1`).
- The executing identity must have sufficient permissions:
  - `rbac.authorization.k8s.io/rolebindings`: create, update, delete, list
  - `rbac.authorization.k8s.io/clusterrolebindings`: create, update, delete, list
  - `v1/serviceaccounts`: create, update, delete, list
  - `v1/namespaces`: get, list (namespace creation is out of scope for this skill)
- The cluster must be integrated with the cloud provider's IAM system (EKS with AWS IAM, AKS with Entra ID, GKE with Google IAM) so that cloud groups can be referenced as Kubernetes subjects. If running on a non-cloud cluster, an OIDC provider must be configured.
- Namespaces for the tenants in scope must already exist (created by the infrastructure provisioning process).

## Your Goal

Apply the RBAC bindings from `core-iam.yaml` and/or one or more `tenants/{name}.yaml` files to one or more Kubernetes clusters. Ensure that:

1. Each tenant's IAM groups are bound to the correct Kubernetes built-in ClusterRoles within the tenant's namespace(s).
2. platform team groups are bound to appropriate cluster-wide roles where needed.
3. `Role("operator")` ServiceAccounts exist per namespace for non-human pipeline access.
4. No direct `ClusterRoleBinding` with cluster-admin exists for tenant groups.

This skill is **idempotent**: running it multiple times produces the same result.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **IAM definition files**: Path(s) to `core-iam.yaml` and/or `tenants/{name}.yaml`. Read these files first.
- **Target cluster(s)**: Which clusters are in scope? A cluster typically corresponds to a `(Sector, Tier, Region)` coordinate. Confirm the kubeconfig context or cluster API endpoint.
- **Namespace naming convention**: How are tenant namespaces named? (e.g., `{tenant}`, `{tenant}-{tier}`, or simply the tenant name if the cluster is already tier-scoped.)
- **Cloud IAM integration type**: EKS (aws-auth ConfigMap or EKS Access Entries), AKS (Entra ID groups via `--aad-admin-group-object-ids` and RoleBindings), GKE (Google Groups RBAC), or standalone OIDC.
- **Cluster-level access needs**: Does the platform team need cluster-level access (e.g., for cluster administration, monitoring agent deployment)? Specify which groups need ClusterRoleBindings vs. namespace-scoped RoleBindings.
- **Scope of this run**: All namespaces, a single tenant, or specific clusters?
- **Dry-run mode**: Recommended for first-time runs.

Read the IAM definition files before proceeding.

## Process

### Step 1 — Read and Parse IAM Definitions

Read the specified files and extract:

- All groups (name, type, role)
- Tenant names and their associated sectors and tiers
- `Role("operator")` Workload Identity definitions (for ServiceAccount annotation)

Validate:
- No human members in `Role("operator")` groups
- Tenant sectors map to known cluster coordinates

Report validation errors and stop before applying changes.

### Step 2 — Map Platform Roles to Kubernetes ClusterRoles

Apply the standard role mapping from the chapter:

| Platform Role | Kubernetes ClusterRole | Scope |
|---------------|----------------------|-------|
| `Role("reader")` | `view` | Namespace (per tenant) |
| `Role("contributor")` | `edit` | Namespace (per tenant) |
| `Role("admin")` | `admin` | Namespace (per tenant) |
| `Role("operator")` | `admin` | Namespace (per tenant) — via ServiceAccount, not human group |

Rules:
- Never bind tenant groups to `cluster-admin`. This is equivalent to giving root access to the entire cluster.
- All tenant bindings are `RoleBinding` (namespace-scoped), never `ClusterRoleBinding`.
- platform team bindings may use `ClusterRoleBinding` for cluster-level administration roles, but only for the `platform-{tier}-admins` group and only with the `cluster-admin` ClusterRole — document these explicitly and keep them minimal.
- The `view` ClusterRole excludes Secrets by default. If developers need to read Secrets for debugging, create a supplemental Role that grants `get` on `secrets` within the namespace and bind it separately — do not elevate the entire binding to `edit` for this purpose alone.

### Step 3 — Resolve Group References per Cloud Provider

The subject in a Kubernetes RoleBinding varies by cloud IAM integration:

**EKS (AWS IAM)**:
- Using EKS Access Entries (preferred): Create an Access Entry for each IAM Identity Center group ARN and associate it with the correct access policy.
- Using aws-auth ConfigMap (legacy): Add a `rolearn` entry mapping the IAM role to a Kubernetes group. Then bind that group in a RoleBinding.

**AKS (Entra ID)**:
- Subject kind is `Group` and name is the Entra ID group Object ID.
- Example: `subjects: [{kind: Group, name: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", apiGroup: rbac.authorization.k8s.io}]`

**GKE (Google Groups RBAC)**:
- Subject kind is `Group` and name is the Cloud Identity group email.
- Example: `subjects: [{kind: Group, name: "payments-live-contributors@mountainlab.io", apiGroup: rbac.authorization.k8s.io}]`

**Standalone OIDC**:
- Subject depends on the OIDC token claims. Use the `groups` claim if the OIDC provider emits group membership. Subject kind is `Group`.

Resolve the correct subject format for the cluster's integration type before creating bindings.

### Step 4 — Create RoleBindings per Tenant Namespace

For each tenant and each target cluster:

1. Determine the namespace(s) for the tenant. If the cluster is tier-scoped (e.g., all workloads in the `ecommerce-live` cluster), the namespace is typically just `{tenant}`. If the cluster spans tiers, namespace may be `{tenant}-{tier}`.
2. Verify the namespace exists. If it does not, report it and skip — namespace creation is outside this skill's scope.
3. For each role (`Role("reader")`, `Role("contributor")`, Admin), check whether a RoleBinding already exists.
4. Create or update the RoleBinding to bind the group to the ClusterRole within the namespace.

RoleBinding naming convention: `{group-name}` or `{role}-{group-name}` — be consistent.

Example RoleBinding (AKS):
``yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: payments-live-contributors
  namespace: payments
subjects:
  - kind: Group
    name: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  # Entra ID group Object ID
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: edit
  apiGroup: rbac.authorization.k8s.io
``

### Step 5 — Create `Role("operator")` ServiceAccounts

For each `Role("operator")` group's non-human identity:

1. Create a Kubernetes ServiceAccount in the tenant's namespace.
2. Annotate it for cloud IAM integration:
   - **EKS**: `eks.amazonaws.com/role-arn: arn:aws:iam::{account}:role/{tenant}-{tier}-operator`
   - **AKS**: `azure.workload.identity/client-id: {managed-identity-client-id}`
   - **GKE**: `iam.gke.io/gcp-service-account: {tenant}-{tier}-operator@{project}.iam.gserviceaccount.com`
3. Create a RoleBinding binding the ServiceAccount to `admin` within the namespace.
4. Do not create a ClusterRoleBinding for the ServiceAccount. `Role("operator")` access must be namespace-scoped.

### Step 6 — Create Platform ClusterRoleBindings

For the platform team's cluster-level access needs:

1. Check whether `ClusterRoleBinding` resources exist for platform groups.
2. For cluster administration:
   - `platform-{tier}-admins` → `cluster-admin` ClusterRole (JIT-only in `Tier("live")` — this binding alone is not sufficient; PIM or equivalent must gate activation)
3. For cluster-wide read access (e.g., monitoring, audit):
   - `platform-{tier}-readers` → `view` ClusterRole at cluster scope

Keep the list of ClusterRoleBindings short. Every new cluster-wide binding increases blast radius. Prefer namespace-scoped RoleBindings wherever possible.

### Step 7 — Validate and Clean Up

After creating all bindings:

1. List all RoleBindings and ClusterRoleBindings in scope.
2. Identify bindings not present in the IAM definition. Report them. Do not remove them without explicit user confirmation.
3. Check for direct user bindings (subjects with `kind: User`). These bypass group-based access management and should be removed — confirm with the user first.
4. Check for any binding referencing `cluster-admin` outside of the platform admin group. Report as a critical finding.

### Step 8 — Report Drift and Changes

Produce a summary after applying:

- RoleBindings created / already existed / updated
- ClusterRoleBindings created / already existed
- ServiceAccounts created / already existed
- Bindings found outside the definition (orphans)
- Security findings (cluster-admin bindings, direct User subjects, missing namespaces)
- Items skipped with reason

In dry-run mode, produce the report without making changes.

## Output Format

Produce a Markdown report named `k8s-iam-report.md`:

``markdown
# Kubernetes RBAC Sync Report

**Date**: [timestamp]
**Cluster(s)**: [cluster names / contexts]
**Scope**: [core / tenant names applied]
**Mode**: [applied / dry-run]

## RoleBindings

| Namespace | Binding Name | ClusterRole | Subject (Group) | Status |
|-----------|-------------|-------------|----------------|--------|
| payments | payments-live-contributors | edit | xxxxxxxx-... (Entra ID) | created |
| payments | payments-live-admins | admin | xxxxxxxx-... (Entra ID) | created |
| payments | payments-readers | view | xxxxxxxx-... (Entra ID) | exists |

## ClusterRoleBindings

| Binding Name | ClusterRole | Subject (Group) | Scope | Status |
|-------------|-------------|----------------|-------|--------|
| platform-live-admins | cluster-admin | platform-live-admins | cluster | exists |

## ServiceAccounts

| Namespace | Name | Cloud Annotation | Status |
|-----------|------|-----------------|--------|
| payments | payments-live-operator | iam.gke.io/gcp-service-account=... | created |

## Orphan Bindings (not in definition)

| Namespace | Binding Name | Note |
|-----------|-------------|------|
| payments | old-payments-deployer | User subject — recommend removal |

## Security Findings

[cluster-admin bindings outside platform group, User subjects, namespaces missing, etc.]

## Open Items

[Namespace creation needed, EKS Access Entry configuration required, etc.]
``

## Principles to Apply

- **Namespace scope for tenants**: All tenant RBAC is `RoleBinding` — never `ClusterRoleBinding`. Tenants do not get cluster-wide access.
- **No direct User subjects**: All bindings reference groups. Direct User subjects bypass group lifecycle management and create orphan permissions when people leave.
- **cluster-admin is exceptional**: The only acceptable `cluster-admin` binding is for the platform admin group, accessed via JIT. Any other binding referencing `cluster-admin` is a critical finding.
- **ServiceAccounts over static tokens**: Operators use ServiceAccounts with cloud IAM annotations (IRSA, Workload Identity) — not manually created tokens or `kubectl` service account secrets.
- **Idempotent by design**: Check before creating. Report orphans but do not delete without confirmation.

## Related Chapter(s)

This skill is grounded in **Chapter 5: Identity and Access Management** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
