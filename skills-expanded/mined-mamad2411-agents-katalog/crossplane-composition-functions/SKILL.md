---
name: crossplane-composition-functions
description: >
  Author and operate Crossplane Composition Functions (pipeline mode) for owned
  control planes: function-patch-and-transform, Go/Python/Templating functions,
  CompositionRevision safety, and render testing. Use when building XRDs/Compositions
  that generate managed resources with function pipelines rather than only legacy
  patch-and-transform in the Composition spec.
---

# Crossplane Composition Functions

## Scope And Authorization

- **In scope:** Crossplane control planes, XRDs, Compositions, and Providers in clusters you administer.
- **Out of scope:** Pointing Compositions at cloud accounts you do not own; privilege escalation via ProviderConfigs without approval.
- Prefer `crossplane render` / dev clusters before promoting CompositionRevisions to prod.
- Redact cloud credentials in ProviderConfigs; prefer IRSA/Workload Identity.
- Pair YAML/Go function code with `code-quality-standards`.

## When To Use

- Migrating Compositions to **pipeline** mode with Composition Functions.
- Complex desired-state logic beyond simple patches (conditionals, loops, external calls).
- Reusing function-patch-and-transform or org-written functions across Compositions.
- Debugging Observation vs desired diffs, function IO, or broken pipelines.
- Versioning CompositionRevisions for safe rollout.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General K8s app deploy (Helm/Deployments only) | workload deploy skills |
| Terraform modules without Crossplane | `terraform-security-basics` / Terraform ops |
| Cloud IAM design alone | cloud IAM skills |
| GitOps promotion mechanics only | GitOps skills |
| Implementation quality baseline | `code-quality-standards` |

## Concepts

| Term | Role |
| --- | --- |
| XRD | Defines claim/composite API (kind, parameters schema) |
| Composition | Maps XR to composed resources |
| pipeline mode | Steps invoke Functions with `input` resources |
| Function | OCI-packaged gRPC function mutating pipeline state |
| CompositionRevision | Immutable snapshot when Composition changes |
| Provider | Talks to cloud APIs for managed resources |

## Workflow

### 1. Confirm scope and success criteria

1. Control plane version (`crossplane version`), providers, and target cloud accounts.
2. Success: claim creates expected managed resources; updates are predictable; failed functions surface useful conditions; rollback via revision works.

### 2. Inventory

```bash
kubectl get xrd,composition,function,provider,providerconfig
kubectl get compositionrevisions
crossplane version
```

Note whether Compositions use `spec.mode: Pipeline` or legacy resources/patches only.

### 3. Design XRD + pipeline

1. Keep XRD parameter schema small and validated (OpenAPI).
2. Pipeline steps: validate → patch-and-transform → custom function → readiness.
3. Prefer pure functions; minimize network calls from functions (latency, failure modes).

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xbuckets.example.org
spec:
  compositeTypeRef:
    apiVersion: example.org/v1alpha1
    kind: XBucket
  mode: Pipeline
  pipeline:
    - step: patch-and-transform
      functionRef:
        name: function-patch-and-transform
      input:
        apiVersion: pt.fn.crossplane.io/v1beta1
        kind: Resources
        resources:
          - name: bucket
            base:
              apiVersion: s3.aws.upbound.io/v1beta1
              kind: Bucket
              spec:
                forProvider:
                  region: us-east-1
            patches:
              - type: FromCompositeFieldPath
                fromFieldPath: spec.parameters.region
                toFieldPath: spec.forProvider.region
```

### 4. Develop custom functions (when needed)

1. Use official function SDK (Go/Python) templates.
2. Contract: read `RunFunctionRequest` resources/observed; return desired composed resources.
3. Unit-test transforms offline; avoid embedding secrets in function images.
4. Publish function package to registry you control; pin by digest in Function CR.

```yaml
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-example
spec:
  package: xpkg.example.com/org/function-example:v1.2.3
```

### 5. Render and test before apply

```bash
# Validate render of composite YAML against Composition
crossplane render xr.yaml composition.yaml functions.yaml
# Apply to dev cluster
kubectl apply -f xrd.yaml -f composition.yaml
kubectl apply -f claim.yaml
kubectl describe claim/NAME
kubectl get managed
```

Check status conditions on composite and composed resources for function errors.

### 6. Rollout safely

1. Composition changes create new **CompositionRevision**; select via label/update policy.
2. Canary: new claims on new revision; existing claims upgrade strategy documented.
3. Provider permission least privilege for managed resource types only.
4. GitOps: PR review required for XRD breaking changes (field removal).

### 7. Operate

1. Alert on stuck composites (`Synced=False`, `Ready=False`).
2. Log/metrics for function runtime pods if self-hosted.
3. Pause reconciliation only with break-glass procedure.
4. Document how to delete claims without orphaning cloud resources (policy: orphan vs delete).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Logic | Tested pipeline functions | Unreadable nested patches only copy-pasted |
| Secrets | Inject via ProviderConfig identity | Cloud keys in Composition YAML |
| Versioning | Pinned function packages | `:latest` functions in prod |
| Changes | Revision + canary claims | Edit live Composition without render test |
| XRD | Stable API, versioned | Breaking params without migration |

## Output Checklist

- [ ] Crossplane/provider versions recorded
- [ ] XRD schema reviewed
- [ ] Pipeline steps and function pins defined
- [ ] `crossplane render` or dev apply succeeded
- [ ] Claim → managed resource path verified
- [ ] IAM/ProviderConfig least privilege checked
- [ ] CompositionRevision rollout plan
- [ ] Failure conditions observable
- [ ] Deletion policy documented
- [ ] Residual risk (function supply chain) noted

## Rules

- Treat Composition Functions as production code (tests, pins, reviews).
- Never embed long-lived cloud keys in XRDs/Compositions.
- Authorized control planes and cloud accounts only.
- Focus on **function pipelines and composition authoring**, not general app K8s deploys.
