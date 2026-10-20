---
name: argo-workflows-rbac
description: >
  Argo Workflows RBAC and ServiceAccount design for owned clusters: workflow-controller
  and argo-server roles, namespace isolation, SSO/RBAC maps, executor permissions, and
  least-privilege submit/list/log access. Use when locking down who can submit Workflows,
  fixing permission errors on pods/logs/artifacts, or reviewing executor SAs — not for
  abusing Workflows on clusters you do not operate.
---

# Argo Workflows RBAC

## Scope And Authorization

- **In scope:** Argo Workflows installs (controller, server, namespaces) you own or assess with authorization.
- **Out of scope:** Submitting Workflows to third-party clusters; stealing SSO tokens; cluster takeover attempts.
- Workflow executor SAs often need pod create/patch — treat as privileged automation identities.
- Prefer dedicated namespaces per team; avoid cluster-wide `create pods` for all users.
- Pair YAML with `code-quality-standards`; link `argo-events-sensors` when events submit workflows.

## When To Use

- Configuring Argo Server SSO + `workflow-controller-configmap` RBAC (or server RBAC ConfigMap).
- Granting developers submit/get/list/watch/logs without full namespace admin.
- Fixing `cannot get resource "pods/log"` or artifact/archive permission errors.
- Hardening workflow/`workflowtaskresults`/`workflowtasksets` API access on newer versions.
- Separating controller SA, executor SA, and human users.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Argo Events wiring | `argo-events-sensors` |
| Argo CD application RBAC | `argo-cd-rbac-basics` |
| Generic K8s RBAC theory only | cluster RBAC skill |
| Pod security standards / PSA | cluster hardening skill |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Identity | Typical needs |
| --- | --- |
| workflow-controller SA | Watch/manage Workflow CRs, create pods, manage related CRDs |
| argo-server SA | Impersonation/SSO mapping; API aggregation for UI/CLI |
| executor / workflow SA | Pod exec/logs as configured; artifact access; often less than controller |
| Human users / groups | submit, get, list, watch Workflows; logs; not secret write |

## Resource Verbs Cheatsheet

| Resource | Common verbs for submitters |
| --- | --- |
| workflows.argoproj.io | create, get, list, watch, update, delete (limit delete) |
| workflowtemplates / clusterworkflowtemplates | get, list (create for template admins) |
| cronworkflows | get/list/create as needed |
| pods / pods/log | get, list, watch (for log streaming) |
| secrets/configmaps | get only if required; prefer mounted artifacts |
| serviceaccounts | none for normal users |

## Workflow

### 1. Confirm scope and success criteria

1. Record Argo Workflows version, install namespace, multi-tenancy model, SSO type.
2. Success: team A can submit only in ns-a; cannot read secrets cluster-wide; UI lists only allowed workflows; controller healthy.
3. Break-glass: platform admin RoleBinding documented.

### 2. Inventory current RBAC

```bash
kubectl get sa,role,rolebinding,clusterrole,clusterrolebinding -n argo
kubectl get ns | grep -E 'argo|workflow'
kubectl get cm -n argo | grep -i rbac
# Server auth mode
kubectl -n argo get deploy argo-server -o yaml | grep -i auth
# Who can create workflows cluster-wide?
kubectl auth can-i create workflows.argoproj.io --all-namespaces --as=system:serviceaccount:team-a:default
```

1. List Workflow ServiceAccounts referenced in specs (`serviceAccountName`).
2. Check if users run as `default` SA with excess privileges.
3. Note artifact repository credentials (S3 IAM, etc.).

### 3. Baseline

1. Export Roles/RoleBindings for argo and tenant namespaces.
2. Capture failing user operations from UI/CLI errors.
3. Document intended tenancy: namespace-per-team vs single shared ns.

### 4. Apply least-privilege patterns

**Namespace submitter Role (sketch):**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: argo-workflow-submitter
  namespace: team-a
rules:
  - apiGroups: ["argoproj.io"]
    resources: ["workflows", "workflowtaskresults"]
    verbs: ["create", "get", "list", "watch", "update", "patch", "delete"]
  - apiGroups: ["argoproj.io"]
    resources: ["workflowtemplates", "cronworkflows"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["events"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: argo-workflow-submitter
  namespace: team-a
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: argo-workflow-submitter
subjects:
  - kind: Group
    name: org:team-a
    apiGroup: rbac.authorization.k8s.io
```

**Executor ServiceAccount (minimal idea):**

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: workflow-executor
  namespace: team-a
---
# Bind only what executor needs for your executor type (emissary/k8sapi/pns)
# Often: get/patch pods, workflowtaskresults create, secrets get for artifacts if required
```

**Argo Server / SSO**

1. Prefer SSO over static long-lived tokens for humans.
2. Map groups to Roles via server RBAC config (version-specific ConfigMap keys).
3. Disable anonymous UI access in production.

**Controller vs user separation**

1. Do not reuse controller SA as workflow `serviceAccountName`.
2. Pin `workflowDefaults.spec.serviceAccountName` to a weak executor SA.
3. Use `automountServiceAccountToken: false` where executor mode allows.

### 5. Verify with evidence

```bash
# As team user
kubectl auth can-i create workflows.argoproj.io -n team-a --as=user@example.com --as-group=org:team-a
kubectl auth can-i create workflows.argoproj.io -n team-b --as=user@example.com --as-group=org:team-a
# expect yes / no
argo submit -n team-a --serviceaccount workflow-executor hello.yaml
argo logs -n team-a @latest
# Attempt secret list should fail for submitter
kubectl auth can-i list secrets -n team-a --as=user@example.com --as-group=org:team-a
```

1. UI login as SSO group member; confirm namespace visibility.
2. Confirm workflow pods run under intended SA (`kubectl get pod -o jsonpath='{.spec.serviceAccountName}'`).
3. Keep allow/deny matrix in change ticket.

### 6. Observe and harden

1. Audit RoleBindings granting `*` on `argoproj.io` or cluster-admin to humans.
2. Alert on creation of Workflows using privileged SAs or hostPath volumes.
3. Review artifact bucket policies so executor credentials are not world-readable secrets.

### 7. Hand off

1. Document SA catalog: controller, server, per-team executor, CI submitter.
2. GitOps Roles; onboarding guide for new teams (ns + RoleBinding + SA).
3. Cross-link Events sensors that create Workflows so their SAs are also least-privilege.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Tenancy | ns + Role per team | everyone cluster-admin |
| Executor SA | dedicated, minimal | default SA with admin |
| Humans | submit/log only | full secret/controller access |
| Tokens | SSO + short-lived | static admin bearer forever |
| Templates | get/list for users | unrestricted ClusterWorkflowTemplate write |
| Scope | owned install | submitting to foreign clusters |

## Output Checklist

- [ ] Version, namespaces, SSO, authorization recorded
- [ ] Controller/server/executor/human identities inventoried
- [ ] Namespace Roles for submit/list/log applied
- [ ] Executor SA separated and minimal
- [ ] can-i allow/deny matrix verified
- [ ] Anonymous/admin UI paths reviewed
- [ ] Artifact and secret access reviewed
- [ ] Alerts/audit for privileged workflow patterns
- [ ] `code-quality-standards` applied to manifests

## Rules

- Authorized Workflows installs only.
- Workflow automation identities are high risk — least privilege and namespace isolation.
- Never grant humans the controller ServiceAccount.
- Evidence with `kubectl auth can-i` and actual submit/log tests.
- Focus on Workflows RBAC; route Events wiring and Argo CD elsewhere.
