---
name: audit-rbac-grants
description: Audit RBAC roles and bindings — find overbroad verbs (*), cluster-wide grants that should be namespaced, stale ServiceAccounts, anonymous access.
---

# audit-rbac-grants

> Read a set of RBAC manifests and flag the grants that are wider than they need to be.

## When to use

- A periodic RBAC review.
- A new operator/controller's manifest is being merged.
- A workflow needs an authz check before deploy.

## Inputs

- The cluster's `Role`, `ClusterRole`, `RoleBinding`, `ClusterRoleBinding` manifests (or a YAML dump from `kubectl get … -o yaml`).
- The list of namespaces in the cluster (so cluster-wide grants stand out).

## Procedure

1. **Cluster-wide vs namespaced**:
   - `ClusterRoleBinding` to a workload's ServiceAccount → flag unless that workload genuinely needs cluster-wide read/write.
   - Prefer `RoleBinding` referencing a `ClusterRole` so the role definition is shared but the grant is namespaced.
2. **Verbs**:
   - `verbs: ["*"]` → flag every time. Always.
   - `verbs: ["create","update","patch","delete"]` on Secrets / ServiceAccounts / RoleBindings → flag.
   - `verbs: ["impersonate"]` or `["escalate"]` → flag with high severity.
3. **Resources**:
   - `resources: ["*"]` → flag.
   - `nonResourceURLs: ["*"]` → flag.
   - Secrets / ServiceAccounts / RoleBindings / ClusterRoleBindings as resources for create/update verbs → privilege escalation risk; flag.
4. **Subjects**:
   - `system:anonymous` or `system:unauthenticated` → flag immediately.
   - `kind: Group` referencing OIDC groups → confirm group membership is documented.
   - `kind: User` with an email → people move; prefer Group-based subjects.
5. **Stale**: any RoleBinding pointing to a ServiceAccount or User that no longer exists is dead grant; flag.

## Output

```text
RBAC audit: <cluster or namespace>

HIGH severity:
  - ClusterRoleBinding refund-admin → ServiceAccount payments/refund
    Verbs: ["*"] on resources ["*"]. Namespaced scope is sufficient.
    Fix: replace with RoleBinding in payments namespace; tighten verbs.

  - ClusterRoleBinding lets system:anonymous list endpoints.
    Fix: delete; default-deny anonymous.

MEDIUM:
  - RoleBinding refund-ops grants verbs ["create","patch"] on secrets in
    payments. Only "get" + "list" are needed for the workload's reads.

LOW (stale):
  - RoleBinding old-job-runner → ServiceAccount that no longer exists.
```

## Quality bar

- Every finding cites the binding name + namespace.
- Severity ordering: anonymous > impersonate/escalate > "*" verbs > secret-write > cluster-wide read > stale.
- "Fix" is a concrete change (binding type, narrower verbs), not "review with security team".

## Anti-patterns to avoid

- Approving a `ClusterRole` with `["*"]` because "it's an operator" without checking what the operator actually uses.
- Granting `impersonate` to humans for "convenience".
- Leaving stale bindings; they make future audits noisier.
