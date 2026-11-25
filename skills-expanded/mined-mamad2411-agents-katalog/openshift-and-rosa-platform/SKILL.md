---
name: openshift-and-rosa-platform
description: >
  Guides working with OpenShift-specific Kubernetes concepts — Routes,
  Security Context Constraints (SCCs), Projects, and Operator Lifecycle
  Manager (OLM) — plus Red Hat OpenShift Service on AWS (ROSA)
  provisioning and the AWS/Red Hat shared responsibility split. Use
  when a user asks to "expose a service with an OpenShift Route,"
  "fix a pod blocked by SCC," "install an operator via OLM," "create
  an OpenShift Project," "provision a ROSA cluster," or "understand
  what Red Hat vs. our team manages in ROSA."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# OpenShift and ROSA Platform

## Purpose

OpenShift is a Kubernetes distribution that layers additional
opinionated primitives — Routes instead of bare Ingress, Security
Context Constraints instead of raw Pod Security admission alone,
Projects as a wrapper around Namespaces, and OLM for Operator lifecycle
— on top of vanilla Kubernetes. These differences are exactly where
Kubernetes-general knowledge silently fails on OpenShift: a manifest
that works on EKS/GKE can be rejected outright by SCCs, and "just expose
it with an Ingress" isn't quite how OpenShift users typically expose
services. ROSA adds a further layer: Red Hat manages the control plane
and much of the infrastructure inside an AWS account the customer still
owns, with a specific shared-responsibility split that changes incident
response and access assumptions. This skill covers both.

## When to use

- Exposing a Service externally on OpenShift (Routes vs. Ingress, and
  when each is actually used).
- Debugging a pod that fails to schedule/start with an SCC-related
  permission error (`unable to validate against any security context
  constraint`).
- Creating and scoping a Project (OpenShift's Namespace wrapper) with
  appropriate quotas and default network isolation.
- Installing or troubleshooting an Operator distributed via OLM
  (CatalogSource, Subscription, InstallPlan, ClusterServiceVersion).
- Provisioning a new ROSA cluster and understanding what Red Hat
  operates versus what the customer is responsible for.
- Migrating manifests written for vanilla Kubernetes (EKS/AKS/GKE) to
  run on OpenShift/ROSA without being blocked by SCCs or missing Routes.

## Prerequisites & environment

- `oc` CLI (OpenShift's `kubectl` superset) matched to the target
  cluster's OpenShift version — OpenShift versions track upstream
  Kubernetes on a roughly 3-releases-behind cadence (e.g. OpenShift 4.16
  ships Kubernetes 1.29), so confirm compatibility before assuming a
  Kubernetes feature/API version is available.
- `rosa` CLI ≥ 1.2 for ROSA-specific provisioning
  (`rosa create cluster`), plus an AWS account meeting ROSA's
  prerequisites (VPC, IAM roles created via `rosa create account-roles`,
  or STS-mode OIDC provider setup for the newer, recommended STS
  deployment mode over the legacy IAM-user mode).
- Cluster-admin or project-admin `oc` role bindings appropriate to the
  task (creating Projects/OLM subscriptions typically needs elevated
  cluster roles; deploying into an existing Project needs only
  namespace-scoped `edit`/`admin`).
- Familiarity with vanilla Kubernetes concepts this skill builds on —
  for CNI/networking specifics on OpenShift's default SDN/OVN-Kubernetes
  see [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md)
  for the general Calico/Flannel concepts (OpenShift itself defaults to
  OVN-Kubernetes, a separate CNI from either).

## Step-by-step guidance

1. **Expose a Service with a Route** rather than (or in addition to) an
   Ingress — Routes are OpenShift-native and integrate with the
   platform's built-in router (HAProxy-based) without requiring a
   separately installed Ingress controller:
   ```yaml
   apiVersion: route.openshift.io/v1
   kind: Route
   metadata:
     name: payments-api
     namespace: payments
   spec:
     host: payments.apps.cluster.example.com
     to:
       kind: Service
       name: payments-api
     tls:
       termination: edge
       insecureEdgeTerminationPolicy: Redirect
   ```
   OpenShift also supports standard Kubernetes `Ingress` objects (the
   platform's Ingress Operator translates them to Routes automatically),
   so existing Ingress manifests generally still work, but native Route
   fields (weighted multi-service routing, path-based Route merging
   rules) aren't expressible through the Ingress object.

2. **Create a Project** (OpenShift's Namespace wrapper, adding
   self-service provisioning and default RBAC/quota hooks):
   ```bash
   oc new-project payments --description="Payments platform" --display-name="Payments"
   ```
   A Project *is* a Namespace with additional OpenShift-managed
   annotations — `kubectl get namespace payments` shows the same object.

3. **Diagnose SCC rejections** when a pod fails to start:
   ```bash
   oc get events -n payments --field-selector reason=FailedCreate
   # "unable to validate against any security context constraint" is the tell
   ```
   Check what the pod's spec requires (running as a specific UID,
   `hostNetwork`, added Linux capabilities) against the SCCs available
   to its ServiceAccount:
   ```bash
   oc get scc
   oc describe scc restricted-v2
   oc get serviceaccount payments-api -n payments -o yaml
   ```
   The default `restricted-v2` SCC (OpenShift ≥ 4.11) forbids running as
   a fixed root/specific UID, privilege escalation, and most added
   capabilities — the common fix is adjusting the *application* to run
   as an arbitrary, non-root UID (the platform assigns one from the
   Project's allocated UID range) rather than granting a broader SCC:
   ```yaml
   spec:
     containers:
       - name: payments-api
         securityContext:
           allowPrivilegeEscalation: false
           runAsNonRoot: true
           capabilities: { drop: ["ALL"] }
   ```
   > **Warning:** granting a broader SCC (`anyuid`, `privileged`) to
   > unblock a pod is a security-posture regression, not a routine fix —
   > treat it as an exception requiring review, and prefer fixing the
   > container image/app to run under an arbitrary non-root UID instead.

4. **Install an Operator via OLM** rather than raw manifests, for any
   Operator distributed through Red Hat's or a community catalog:
   ```bash
   oc get packagemanifests -n openshift-marketplace | grep cert-manager
   ```
   ```yaml
   apiVersion: operators.coreos.com/v1alpha1
   kind: Subscription
   metadata:
     name: cert-manager-operator
     namespace: openshift-operators
   spec:
     channel: stable-v1
     name: openshift-cert-manager-operator
     source: redhat-operators
     sourceNamespace: openshift-marketplace
     installPlanApproval: Automatic
   ```
   ```bash
   oc apply -f cert-manager-subscription.yaml
   oc get csv -n openshift-operators   # confirm Succeeded phase
   ```
   Set `installPlanApproval: Manual` for production clusters where
   Operator upgrades should be reviewed before applying, rather than
   `Automatic`, which applies new `InstallPlan`s as soon as the catalog
   publishes them.

5. **Provision a ROSA cluster** (STS mode — the recommended,
   keyless-role deployment model over the legacy IAM-user mode):
   ```bash
   rosa create account-roles --mode auto --yes
   rosa create cluster --cluster-name payments-prod --sts \
     --region us-east-1 --version 4.16 \
     --machine-cidr 10.0.0.0/16 --compute-nodes 3
   rosa create operator-roles --cluster payments-prod --mode auto --yes
   rosa create oidc-provider --cluster payments-prod --mode auto --yes
   ```
   ```bash
   rosa describe cluster --cluster payments-prod
   rosa create admin --cluster payments-prod   # break-glass cluster-admin user
   ```

6. **Understand the ROSA shared-responsibility split** before treating
   any incident as fully self-serviceable:
   - **Red Hat operates**: the control plane (API server, etcd,
     scheduler), control-plane node patching/upgrades, and
     infrastructure nodes (router, registry, monitoring stack)
     — with SRE on-call and an SLA.
   - **Customer owns**: the AWS account and its cost/quota, worker node
     scaling decisions (within Red Hat's managed node lifecycle),
     workload configuration (Projects, RBAC beyond cluster-admin
     defaults, Operators installed, application security), and
     day-2 operations of anything deployed *onto* the cluster.
   - **Shared/coordinated**: cluster version upgrades (customer
     schedules within Red Hat's supported window; Red Hat executes),
     and networking that touches the customer's own VPC/route tables
     outside what ROSA provisions automatically.
   Confirm which category an incident falls into before opening either
   an internal ticket or a Red Hat support case — misrouting a
   control-plane issue to internal on-call (or vice versa) delays
   resolution.

7. **Validate before promoting a manifest written for vanilla
   Kubernetes** to run on OpenShift/ROSA:
   ```bash
   oc apply --dry-run=server -f deployment.yaml
   oc adm policy scc-subject-review -f deployment.yaml
   ```
   `scc-subject-review` reports which SCC (if any) would admit the pod
   spec as written, surfacing SCC issues before a real apply attempt.

## Best practices

- Prefer fixing container images to run as an arbitrary non-root UID
  (compatible with `restricted-v2`) over granting broader SCCs — this
  keeps the same image portable to non-OpenShift Kubernetes too.
- Use OLM `Subscription`s with `installPlanApproval: Manual` in
  production namespaces so Operator upgrades are a reviewed,
  deliberate action, not an automatic side effect of the catalog
  publishing a new version.
- Scope Projects with `ResourceQuota` and `LimitRange` from creation,
  not as an afterthought — Project self-service creation without quotas
  is a common path to one team's workload starving node capacity for
  others.
- Treat `rosa create admin`'s break-glass cluster-admin credential like
  any other break-glass credential: time-box its use, and prefer
  federated identity-provider-based cluster access (`rosa create
  idp`) for day-to-day admin access instead.
- When comparing OpenShift/ROSA to vanilla managed Kubernetes options,
  weigh the SCC/OLM/Route learning curve and Red Hat subscription cost
  against genuine requirements (regulated-industry support contracts,
  existing OpenShift investment) rather than defaulting to it as "the
  enterprise choice" without a specific driver — see
  [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md)
  for the vanilla-cloud-managed alternative comparison.
- Keep track of which OpenShift version maps to which upstream
  Kubernetes minor version when consulting general Kubernetes
  documentation/CVE advisories — the version numbers do not match
  1:1.

## Common pitfalls

- **Symptom:** A Deployment that runs fine on EKS/GKE fails to schedule
  on OpenShift with `unable to validate against any security context
  constraint`.
  **Fix:** The pod spec requests something `restricted-v2` (the
  default SCC most ServiceAccounts get) forbids — commonly a fixed
  non-arbitrary UID, added capabilities, or `hostNetwork`. Adjust the
  container to run as an arbitrary non-root UID rather than granting a
  broader SCC as the default fix.

- **Symptom:** An Ingress object applied on OpenShift doesn't produce
  the expected external hostname/behavior seen on other clouds.
  **Fix:** Confirm whether the cluster's Ingress Operator actually
  translated it into a Route (`oc get route`) and whether OpenShift-
  specific fields the team expected (weighted routing, custom
  `insecureEdgeTerminationPolicy`) need to be set directly on a native
  Route object instead, since the Ingress-to-Route translation only
  covers the common subset of fields.

- **Symptom:** An OLM `Subscription` shows `InstallPlan` stuck in
  `RequiresApproval` and the Operator never actually installs/upgrades.
  **Fix:** This is expected behavior under
  `installPlanApproval: Manual` — approve the pending `InstallPlan`
  explicitly (`oc get installplan -n <ns>` then `oc patch installplan
  <name> -p '{"spec":{"approved":true}}' --type merge`) rather than
  assuming `Manual` mode is broken; it's working as configured.

- **Symptom:** A ROSA cluster incident (e.g. slow API server responses)
  gets escalated internally for hours before anyone realizes the
  control plane is Red-Hat-managed.
  **Fix:** Confirm which shared-responsibility bucket the symptom falls
  into before spending internal on-call time on it — control-plane
  health/performance issues on ROSA are Red Hat's operational
  responsibility and should go through Red Hat support channels
  (`rosa` cluster ID and support case) in parallel with, not instead
  of, internal triage of anything workload-side.

- **Symptom:** `rosa create cluster --sts` fails partway through with a
  missing-role error.
  **Fix:** STS-mode ROSA requires `rosa create account-roles` and later
  `rosa create operator-roles`/`rosa create oidc-provider` to be run in
  the correct order relative to cluster creation — re-run `rosa create
  account-roles --mode auto` and confirm `rosa list account-roles`
  shows the expected roles before retrying cluster creation, rather
  than assuming the CLI's `--mode auto` handles every prerequisite
  automatically in one pass.

## Worked example

**Scenario:** Provision a ROSA STS cluster, create a Project with
quota, deploy an app that needs SCC adjustment to run non-root, and
expose it via Route.

```bash
rosa create account-roles --mode auto --yes
rosa create cluster --cluster-name payments-prod --sts \
  --region us-east-1 --version 4.16 --compute-nodes 3
rosa create operator-roles --cluster payments-prod --mode auto --yes
rosa create oidc-provider --cluster payments-prod --mode auto --yes
rosa create idp --cluster payments-prod --type github \
  --client-id <CLIENT_ID> --client-secret <CLIENT_SECRET_PLACEHOLDER>
```

```bash
oc new-project payments --display-name="Payments"
```

```yaml
apiVersion: v1
kind: ResourceQuota
metadata: { name: payments-quota, namespace: payments }
spec:
  hard: { "requests.cpu": "8", "requests.memory": 16Gi, pods: "40" }
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: payments-api, namespace: payments }
spec:
  replicas: 3
  selector: { matchLabels: { app: payments-api } }
  template:
    metadata: { labels: { app: payments-api } }
    spec:
      containers:
        - name: payments-api
          image: ghcr.io/example/payments-api:1.4.2
          securityContext:
            allowPrivilegeEscalation: false
            runAsNonRoot: true
            capabilities: { drop: ["ALL"] }
          ports: [{ containerPort: 8080 }]
---
apiVersion: v1
kind: Service
metadata: { name: payments-api, namespace: payments }
spec:
  selector: { app: payments-api }
  ports: [{ port: 8080, targetPort: 8080 }]
---
apiVersion: route.openshift.io/v1
kind: Route
metadata: { name: payments-api, namespace: payments }
spec:
  host: payments.apps.payments-prod.example.com
  to: { kind: Service, name: payments-api }
  tls: { termination: edge, insecureEdgeTerminationPolicy: Redirect }
```

```bash
oc apply -f quota.yaml -f deployment.yaml -f service.yaml -f route.yaml
oc get route payments-api -n payments
```

The pod schedules successfully under `restricted-v2` because it runs
non-root with no added capabilities, and `oc get route` shows the
externally reachable HTTPS host served by OpenShift's built-in router —
with cluster-control-plane health and node OS patching handled by Red
Hat's SRE team per the ROSA shared-responsibility model, not by the
cluster's own operators.

## Cross-references

- [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md) — comparison point for vanilla cloud-managed Kubernetes; ROSA runs inside a customer AWS account alongside these options.
- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — contrast with OpenShift's native Route/router model when a workload needs to be portable across both.
- [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md) — automating Route/Ingress TLS certificates on OpenShift via the OLM-distributed cert-manager Operator shown above.
