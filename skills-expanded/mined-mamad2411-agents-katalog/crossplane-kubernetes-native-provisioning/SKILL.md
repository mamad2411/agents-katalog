---
name: crossplane-kubernetes-native-provisioning
description: >
  Provisions cloud infrastructure through Crossplane's Kubernetes-native
  control plane model — Providers, `Composition`/`CompositeResourceDefinition`
  (XRD), and namespaced Claims — as an alternative to Terraform for teams
  that want infrastructure requests to look like any other Kubernetes API
  object, reconciled continuously rather than applied on demand. Use when
  a user asks to "set up Crossplane," "define a Composition/XRD," "let
  application teams self-service provision infra via a Claim," "compare
  Crossplane to Terraform," "build a platform API for infrastructure on
  Kubernetes," or "continuously reconcile cloud resources instead of
  running apply on a schedule."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Crossplane: Kubernetes-Native Infrastructure Provisioning

## Purpose

Crossplane provisions and manages real cloud infrastructure — VPCs,
managed databases, IAM roles, storage buckets — but does it as a
Kubernetes control-plane extension rather than as a standalone CLI tool
run against a state file: cloud resources are represented as
Kubernetes custom resources, and Crossplane's providers continuously
reconcile them toward desired state the same way a Deployment
controller reconciles Pods, indefinitely, not just at `apply` time. This
is a genuinely different paradigm from
[infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md)'s
plan-then-apply, state-file-tracked model — not a Kubernetes wrapper
around Terraform — and the tradeoff is real: continuous reconciliation
and drift correction come for free, a `Composition` lets a platform team
expose a curated, higher-level self-service API (a `DatabaseClaim`
instead of raw `RDSInstance` fields) to application teams, but the
provider ecosystem and HCL-equivalent expressiveness are less mature
than Terraform's for some clouds/resources, and every provisioned
resource now lives inside the same Kubernetes API server that runs
workloads. This skill covers the Composition/XRD/Claim model and
day-to-day provisioning; validating Compositions and Claims before
applying (catching schema mismatches) is
[crossplane-configuration-validation](../crossplane-configuration-validation/SKILL.md)'s
job.

## When to use

- Building a self-service infrastructure API for application teams
  (e.g. "request a `DatabaseClaim`" instead of "file a ticket" or
  "write your own Terraform module") on a platform already built around
  Kubernetes.
- Deciding whether Crossplane or Terraform is the better fit for a new
  infra-provisioning workflow, especially when the surrounding platform
  is already Kubernetes-centric (an internal developer platform, a
  GitOps-managed fleet).
- Defining a `CompositeResourceDefinition` (XRD) and `Composition` so a
  namespaced `Claim` can provision a multi-resource cloud stack (a
  database plus its network access plus its IAM role) as one request.
- Provisioning cloud infrastructure that should reconcile continuously
  (self-heal from drift) rather than only on a scheduled `apply`.
- Migrating a subset of Terraform-managed infrastructure that would
  benefit from a Kubernetes-native, self-service front end, without
  necessarily replacing Terraform everywhere.

## Prerequisites & environment

- A Kubernetes cluster ≥ 1.26 with Crossplane ≥ v1.16 installed (via
  Helm), plus cluster-admin (or sufficiently scoped) access to install
  Providers and define XRDs/Compositions — these are cluster-scoped,
  platform-team-owned resources, distinct from the namespaced Claims
  application teams create.
- Cloud provider credentials scoped per Crossplane `Provider`
  (`provider-aws`, `provider-azure`, `provider-gcp`, or the newer
  `provider-family` split providers) stored as a Kubernetes `Secret`
  and referenced by a `ProviderConfig` — never embedded directly in a
  `Provider`/`ProviderConfig` manifest.
- Familiarity with
  [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md)'s
  module/variable/output concepts is useful context (an XRD's schema
  plays a similar role to a Terraform module's `variables.tf`/
  `outputs.tf`), but this skill does not assume or repeat Terraform
  workflow details.
- A decision on how deep the self-service abstraction should go —
  Crossplane's value is largest when a platform team genuinely curates
  a `Composition` (hiding cloud-specific complexity behind a small
  Claim schema); using it as a thin one-to-one passthrough to a single
  managed resource captures less of that benefit.
- If also running Argo CD or Flux, decide how Crossplane's continuous
  reconciliation interacts with GitOps-managed manifests that create
  Claims — see
  [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md);
  the two are complementary (GitOps manages the Claim manifest, Crossplane
  reconciles the actual cloud resources it describes), not competing.

## Step-by-step guidance

1. **Install Crossplane and a provider**:
   ```bash
   helm repo add crossplane-stable https://charts.crossplane.io/stable
   helm install crossplane crossplane-stable/crossplane --namespace crossplane-system --create-namespace
   ```
   ```yaml
   apiVersion: pkg.crossplane.io/v1
   kind: Provider
   metadata:
     name: provider-aws-rds
   spec:
     package: xpkg.upbound.io/upbound/provider-aws-rds:v1.19.0
   ```
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: aws-creds
     namespace: crossplane-system
   type: Opaque
   stringData:
     creds: |
       [default]
       aws_access_key_id = ${AWS_ACCESS_KEY_ID}
       aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}
   ---
   apiVersion: aws.upbound.io/v1beta1
   kind: ProviderConfig
   metadata:
     name: default
   spec:
     credentials:
       source: Secret
       secretRef: { namespace: crossplane-system, name: aws-creds, key: creds }
   ```
   Source the actual credential values from your organization's
   secrets manager at apply time (never commit them), per
   [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md)
   — the `${...}` placeholders above are not literal syntax to commit.

2. **Provision a single managed resource directly** first, to confirm
   the provider/credentials work, before building a `Composition` on
   top:
   ```yaml
   apiVersion: rds.aws.upbound.io/v1beta2
   kind: Instance
   metadata:
     name: test-db
   spec:
     forProvider:
       region: us-east-1
       engine: postgres
       instanceClass: db.t3.medium
       allocatedStorage: 20
       username: appuser
       passwordSecretRef:
         namespace: crossplane-system
         name: test-db-password
         key: password
     providerConfigRef: { name: default }
   ```
   ```bash
   kubectl get instance.rds.aws.upbound.io test-db -o jsonpath='{.status.conditions}'
   ```
   A `Ready: True`/`Synced: True` condition pair confirms the resource
   was actually created in AWS, not just accepted by the Kubernetes API
   server.

3. **Define a `CompositeResourceDefinition` (XRD)** — the schema for
   the self-service API application teams will actually use, deliberately
   narrower than the underlying provider resource's full field set:
   ```yaml
   apiVersion: apiextensions.crossplane.io/v1
   kind: CompositeResourceDefinition
   metadata:
     name: xdatabaseinstances.platform.example.org
   spec:
     group: platform.example.org
     names: { kind: XDatabaseInstance, plural: xdatabaseinstances }
     claimNames: { kind: DatabaseClaim, plural: databaseclaims }
     versions:
       - name: v1alpha1
         served: true
         referenceable: true
         schema:
           openAPIV3Schema:
             type: object
             properties:
               spec:
                 type: object
                 properties:
                   parameters:
                     type: object
                     properties:
                       storageGB: { type: integer, default: 20 }
                       tier: { type: string, enum: ["small", "medium", "large"] }
                     required: ["tier"]
                 required: ["parameters"]
   ```
   The XRD's schema is the contract application teams see — deliberately
   simpler than every AWS RDS field (`tier` maps internally to an
   instance class the platform team chooses, not something the
   requester picks directly).

4. **Define the `Composition`** that maps the XRD's simple schema onto
   one or more real provider resources:
   ```yaml
   apiVersion: apiextensions.crossplane.io/v1
   kind: Composition
   metadata:
     name: xdatabaseinstances.aws
   spec:
     compositeTypeRef:
       apiVersion: platform.example.org/v1alpha1
       kind: XDatabaseInstance
     resources:
       - name: rds-instance
         base:
           apiVersion: rds.aws.upbound.io/v1beta2
           kind: Instance
           spec:
             forProvider:
               region: us-east-1
               engine: postgres
               username: appuser
             providerConfigRef: { name: default }
         patches:
           - fromFieldPath: spec.parameters.storageGB
             toFieldPath: spec.forProvider.allocatedStorage
           - fromFieldPath: spec.parameters.tier
             toFieldPath: spec.forProvider.instanceClass
             transforms:
               - type: map
                 map: { small: db.t3.small, medium: db.t3.medium, large: db.t3.large }
         connectionDetails:
           - fromConnectionSecretKey: endpoint
           - fromConnectionSecretKey: port
   ```
   The `transforms.map` patch is exactly the abstraction point: the
   requester says `tier: medium`; the platform team, not the requester,
   decides that maps to `db.t3.medium` today and can change that mapping
   later without any Claim needing to change.

5. **Application teams provision via a namespaced `Claim`**, not by
   touching the XRD/Composition/provider resources directly:
   ```yaml
   apiVersion: platform.example.org/v1alpha1
   kind: DatabaseClaim
   metadata:
     name: payments-db
     namespace: payments
   spec:
     parameters:
       tier: medium
       storageGB: 100
     writeConnectionSecretToRef:
       name: payments-db-conn
   ```
   ```bash
   kubectl get databaseclaim payments-db -n payments -o jsonpath='{.status.conditions}'
   kubectl get secret payments-db-conn -n payments   # connection details Crossplane populated
   ```
   The application team never sees or edits `Instance`/`ProviderConfig`
   directly — their entire surface is the `DatabaseClaim`'s narrow
   schema, and the resulting connection Secret.

6. **Let Crossplane's continuous reconciliation handle drift** —
   unlike a scheduled `terraform plan`/`apply`, Crossplane's controllers
   watch the managed resource continuously and correct drift as soon as
   it's detected, without a separate invocation:
   ```bash
   kubectl get managed   # aggregate view across all managed resource kinds
   ```
   Confirm `SYNCED` and `READY` columns are both `True` for anything
   provisioned — a resource that's `READY` but not `SYNCED` (or the
   reverse) indicates the desired spec and actual cloud state have
   diverged and Crossplane is actively working to reconcile it, similar
   in spirit to distinguishing Argo CD's `sync`/`health` signals in
   [argocd-sync-failure-and-drift-investigation](../../../gitops-argo-ecosystem/skills/argocd-sync-failure-and-drift-investigation/SKILL.md).

7. **Manage Composition/XRD changes like any platform API change** —
   version the XRD (`v1alpha1` → `v1beta1` → `v1`) rather than
   breaking existing Claims in place, and use Crossplane's
   `CompositionRevision`s if pinning specific Claims to a known-good
   Composition version during a platform-side change is needed.

8. **Decommission a Claim deliberately.**
   > **Warning:** Deleting a `Claim` (or the underlying `Composite`
   > resource it created) triggers deletion of the real cloud
   > infrastructure it provisioned, unless the Composition's resources
   > are configured with a `deletionPolicy: Orphan` — this is
   > equivalent in consequence to `terraform destroy` and deserves the
   > same caution (see
   > [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md)).
   ```bash
   kubectl get databaseclaim payments-db -n payments -o jsonpath='{.spec.compositeDeletePolicy}'
   kubectl delete databaseclaim payments-db -n payments   # only after confirming backups/intent
   ```

## Best practices

- Keep the XRD's schema deliberately narrower than the underlying
  provider resource's full field set — the value of Crossplane's
  Composition model is the abstraction; exposing every raw cloud field
  through the Claim just recreates Terraform's flexibility with more
  moving parts and less maturity.
- Version XRDs explicitly and evolve schemas additively where possible
  (new optional fields, not renamed/removed required ones) so existing
  Claims don't break when the platform team improves a Composition.
- Scope each `ProviderConfig`'s credentials to the minimum cloud IAM
  permissions the Compositions built on it actually need — the same
  least-privilege principle as
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md),
  applied to the identity Crossplane itself assumes.
- Set `deletionPolicy`/`compositeDeletePolicy` deliberately per resource
  class — `Delete` (the default) for genuinely ephemeral/reproducible
  infrastructure, `Orphan` for anything where accidental Claim deletion
  should not also delete real, hard-to-recreate cloud state (a
  production database) without a separate explicit action.
- Treat `kubectl get managed`'s `SYNCED`/`READY` columns as two
  independent signals worth checking separately, the same discipline
  applied to Argo CD's `sync`/`health` split in
  [argocd-sync-failure-and-drift-investigation](../../../gitops-argo-ecosystem/skills/argocd-sync-failure-and-drift-investigation/SKILL.md).
- Pair Crossplane Claims with GitOps (Flux or Argo CD) so Claim
  manifests themselves are version-controlled and reviewed the same way
  any other Kubernetes manifest is, rather than created ad hoc via
  `kubectl apply` — see
  [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md) and
  [flux-cd-configuration-and-reconciliation](../flux-cd-configuration-and-reconciliation/SKILL.md).
- Don't reach for Crossplane just because a team is Kubernetes-native —
  if application teams don't need self-service infra requests and the
  org already has mature Terraform tooling/reviews, introducing a
  second provisioning paradigm has a real adoption/maintenance cost
  that should be weighed against the self-service benefit.

## Common pitfalls

- **Symptom:** A `Claim` is created and never becomes `Ready`, with no
  obvious error in `kubectl describe databaseclaim`.
  **Fix:** Check the underlying `Composite` resource and managed
  resource directly (`kubectl get composite`, `kubectl get managed`) —
  the Claim's own status often just reflects "waiting on the composite,"
  and the real error (a provider credential rejected by the cloud API,
  a schema validation failure in a patch) is one or two levels down in
  the actual provider-managed resource's `status.conditions`.

- **Symptom:** A `Composition` patch (`fromFieldPath`/`toFieldPath`)
  silently doesn't apply — the target field stays at the `base`
  manifest's default value regardless of what the Claim specifies.
  **Fix:** Field path typos in patches fail silently rather than
  erroring loudly in many Crossplane versions — double-check
  `fromFieldPath`/`toFieldPath` strings exactly match the XRD's schema
  and the target provider resource's actual field structure
  respectively; validate with
  [crossplane-configuration-validation](../crossplane-configuration-validation/SKILL.md)'s
  dry-run workflow before assuming the Composition logic itself is
  broken.

- **Symptom:** `kubectl get managed` shows a resource `READY: True` but
  `SYNCED: False` persistently, not just transiently during a normal
  reconcile cycle.
  **Fix:** Persistent `SYNCED: False` means Crossplane's provider
  controller cannot reconcile the resource toward its desired spec
  (often a permissions issue on the `ProviderConfig`'s credentials, or
  a cloud-side constraint like an immutable field the patch is trying
  to change post-creation) — check the managed resource's
  `status.conditions` message directly rather than assuming `READY: True`
  means everything is fine.

- **Symptom:** Deleting a `DatabaseClaim` during cleanup unexpectedly
  deletes a production RDS instance with real customer data and no
  separate confirmation step.
  **Fix:** This is the destructive default behavior working as
  configured, not a bug — `deletionPolicy: Delete` (Crossplane's
  default) means Claim deletion cascades to real infrastructure
  deletion. Set `deletionPolicy: Orphan` on Compositions backing
  anything genuinely important, and treat any Claim deletion request
  against production-tier resources with the same review rigor as a
  `terraform destroy` plan review.

- **Symptom:** Two different teams' Claims, built from Compositions
  that both reference the same `ProviderConfig`, interfere with each
  other (one team's IAM changes affect another's resources).
  **Fix:** A shared `ProviderConfig` means a shared cloud credential
  and its IAM scope — if isolation between teams/environments matters,
  provision separate `ProviderConfig`s (backed by separate,
  narrowly-scoped credentials/roles) per team or environment rather
  than one shared provider identity for the whole cluster.

## Worked example

**Scenario:** A platform team wants application teams to self-service
provision PostgreSQL databases via a `DatabaseClaim`, without any team
needing to know AWS RDS's actual API surface, and with production
databases protected from accidental deletion.

```bash
helm install crossplane crossplane-stable/crossplane --namespace crossplane-system --create-namespace
```

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata: { name: provider-aws-rds }
spec: { package: xpkg.upbound.io/upbound/provider-aws-rds:v1.19.0 }
```

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata: { name: xdatabaseinstances.platform.example.org }
spec:
  group: platform.example.org
  names: { kind: XDatabaseInstance, plural: xdatabaseinstances }
  claimNames: { kind: DatabaseClaim, plural: databaseclaims }
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                parameters:
                  type: object
                  properties:
                    tier: { type: string, enum: ["small", "medium", "large"] }
                    storageGB: { type: integer, default: 20 }
                    environment: { type: string, enum: ["dev", "staging", "prod"] }
                  required: ["tier", "environment"]
```

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata: { name: xdatabaseinstances.aws }
spec:
  compositeTypeRef: { apiVersion: platform.example.org/v1alpha1, kind: XDatabaseInstance }
  resources:
    - name: rds-instance
      base:
        apiVersion: rds.aws.upbound.io/v1beta2
        kind: Instance
        spec:
          forProvider: { region: us-east-1, engine: postgres, username: appuser }
          providerConfigRef: { name: default }
          deletionPolicy: Orphan
      patches:
        - { fromFieldPath: spec.parameters.storageGB, toFieldPath: spec.forProvider.allocatedStorage }
        - fromFieldPath: spec.parameters.tier
          toFieldPath: spec.forProvider.instanceClass
          transforms:
            - type: map
              map: { small: db.t3.small, medium: db.t3.medium, large: db.r6g.xlarge }
```

`deletionPolicy: Orphan` is set unconditionally here rather than only
for prod, deliberately — an application team's `DatabaseClaim` deletion
detaches Crossplane's management but never auto-deletes the real RDS
instance; actual decommissioning requires a separate, explicit AWS-side
action, which the platform team treats as an acceptable tradeoff for
this Composition given how costly an accidental database deletion would
be.

```yaml
apiVersion: platform.example.org/v1alpha1
kind: DatabaseClaim
metadata: { name: payments-db, namespace: payments }
spec:
  parameters: { tier: medium, storageGB: 100, environment: prod }
  writeConnectionSecretToRef: { name: payments-db-conn }
```

```bash
kubectl get databaseclaim payments-db -n payments -o jsonpath='{.status.conditions}'
kubectl get secret payments-db-conn -n payments -o jsonpath='{.data.endpoint}' | base64 -d
```

The `payments` team never touched an `Instance` or `ProviderConfig`
directly — their entire interaction was the `DatabaseClaim`, and the
resulting `payments-db-conn` Secret gives their application everything
it needs to connect.

## Cross-references

- [crossplane-configuration-validation](../crossplane-configuration-validation/SKILL.md) — dry-running Compositions/Claims and catching XRD schema mismatches before they reach a live cluster.
- [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md) — the plan-then-apply, state-file-tracked alternative paradigm this skill's continuous-reconciliation model differs from; read for contrast, not duplicated here.
- [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md) — how Claim manifests themselves should be version-controlled and reviewed via GitOps rather than applied ad hoc.
- [flux-cd-configuration-and-reconciliation](../flux-cd-configuration-and-reconciliation/SKILL.md) — pairing Flux-managed Claim manifests with Crossplane's own reconciliation of the infrastructure they describe.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege design for the cloud credentials backing each `ProviderConfig`.
- [argocd-sync-failure-and-drift-investigation](../../../gitops-argo-ecosystem/skills/argocd-sync-failure-and-drift-investigation/SKILL.md) — the analogous "two independent status signals" investigative pattern, referenced here for Crossplane's `SYNCED`/`READY` conditions.
