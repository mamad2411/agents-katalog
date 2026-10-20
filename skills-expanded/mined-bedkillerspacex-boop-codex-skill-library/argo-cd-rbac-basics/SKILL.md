---
name: argo-cd-rbac-basics
description: >
  Argo CD RBAC for owned or authorized GitOps control planes: global policy.csv in
  argocd-rbac-cm, Casbin p/g rules, SSO group scopes, AppProject roles, default policy,
  and least-privilege sync/delete/admin boundaries. Use when designing or reviewing
  Argo CD roles, mapping OIDC/LDAP groups to policies, debugging permission denied on
  applications/clusters/repos, tightening admin, or separating project-scoped access —
  not for third-party Argo CD abuse or generic Kubernetes cluster-admin outside Argo CD’s
  RBAC model.
---

# Argo CD RBAC Basics

## Scope And Authorization

- **In scope:** Argo CD instances and AppProjects you operate or assess with authorization.
- **Out of scope:** Attacking third-party Argo CD UIs/APIs; stealing SSO tokens; unauthorized cluster access.
- Changes to `argocd-rbac-cm` and AppProject roles can lock out operators — keep break-glass local admin.
- Redact SSO group names only if sensitive; never paste IdP client secrets into tickets.
- Pair manifests/Helm changes with `code-quality-standards`.

## When To Use

- Designing global `policy.csv` and `policy.default` for developers vs platform admins.
- Mapping OIDC/Dex/LDAP groups via `g, <group>, role:<name>` lines.
- Debugging “permission denied” on applications, logs, exec, repos, or clusters.
- Tightening `role:admin` usage and separating AppProject-scoped roles.
- Reviewing whether users can sync/delete only within their project.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| App-of-apps topology | `argocd-app-of-apps` |
| Detailed policy.csv patterns only | `argocd-rbac-csv` |
| Argo Workflows RBAC | `argo-workflows-rbac` |
| Kubernetes RBAC outside Argo CD | cluster RBAC skill |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Global RBAC | ConfigMap `argocd-rbac-cm`: `policy.csv`, `policy.default`, `scopes` |
| Casbin model | `p` permission rules; `g` group/user → role bindings |
| Resources | applications, applicationsets, clusters, repositories, projects, logs, exec, … |
| Actions | get, create, update, delete, sync, override, action, invoke, … |
| Objects | wildcards `*/*` (project/app), or `project/app-name` |
| AppProject roles | Project-scoped policies + JWT/OIDC group bindings in Project CR |

## policy.csv Essentials

```csv
# p, <role>, <resource>, <action>, <object>, <effect optional>
p, role:developer, applications, get, */*, allow
p, role:developer, applications, sync, dev-team/*, allow
p, role:developer, logs, get, dev-team/*, allow
p, role:developer, exec, create, */*, deny

# g, <user or group>, <role>
g, alice@example.com, role:developer
g, my-org:dev-team, role:developer
```

| Field | Meaning |
| --- | --- |
| role | Logical role name (`role:…`) |
| resource | Argo CD API resource type |
| action | Verb (get/sync/delete/…) |
| object | Often `<project>/<app>` or `*` |
| effect | allow/deny (deny wins when modeled) |

## Workflow

### 1. Confirm scope and success criteria

1. Record Argo CD version, SSO type (OIDC/Dex/LDAP/local), projects, environments.
2. Success: group X can sync only project Y apps; cannot delete prod; admin group documented; default policy is read-only or deny.
3. Ensure local admin / emergency access before tightening SSO roles.

### 2. Inventory current RBAC

```bash
kubectl -n argocd get cm argocd-rbac-cm -o yaml
kubectl -n argocd get appprojects -o yaml
# Who am I in UI? Check user info / accounts
argocd account get-user-info
argocd proj role list <project>
```

1. Capture `policy.default` (e.g. `role:readonly` vs empty).
2. List all `role:` definitions and `g,` bindings.
3. Note AppProject `roles[]` that duplicate or override intent.

### 3. Baseline

1. Export current `argocd-rbac-cm` and AppProjects to version control.
2. Sample “permission denied” tickets: which resource/action/object.
3. Map IdP groups → intended duties (viewer, developer, app-admin, platform-admin).

### 4. Apply least-privilege policies

**Global defaults (illustrative):**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.default: role:readonly
  scopes: '[groups, email]'
  policy.csv: |
    p, role:readonly, applications, get, */*, allow
    p, role:readonly, projects, get, *, allow
    p, role:readonly, repositories, get, *, allow
    p, role:dev, applications, get, */*, allow
    p, role:dev, applications, sync, dev/*, allow
    p, role:dev, applications, update, dev/*, allow
    p, role:dev, logs, get, dev/*, allow
    p, role:platform-admin, *, *, */*, allow
    g, org:developers, role:dev
    g, org:platform, role:platform-admin
```

**AppProject-scoped role (preferred for multi-tenant):**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: dev
  namespace: argocd
spec:
  roles:
    - name: syncer
      description: Sync only within this project
      policies:
        - p, proj:dev:syncer, applications, get, dev/*, allow
        - p, proj:dev:syncer, applications, sync, dev/*, allow
      groups:
        - org:dev-team
```

1. Prefer project roles for tenant isolation; keep global admin small.
2. Restrict `exec`, `delete`, and cluster/repo write to platform roles.
3. Align `scopes` with IdP claim names (`groups` vs `group`).

### 5. Verify with evidence

```bash
# As SSO user (or via argocd CLI with that user token)
argocd app list
argocd app sync dev/sample-app   # expect allow
argocd app sync prod/sample-app  # expect deny
argocd cluster list              # expect deny for developers
kubectl -n argocd get cm argocd-rbac-cm -o jsonpath='{.data.policy\.csv}'
```

1. Confirm group claims appear in Argo CD user info (SSO mis-scope is a common failure).
2. UI and CLI both tested — policies apply to API regardless of client.
3. Record denied/allowed matrix in the change ticket.

### 6. Observe and harden

1. Audit who has `role:admin` / `p, …, *, *, *, allow`.
2. Alert on ConfigMap changes to `argocd-rbac-cm` (GitOps the ConfigMap itself).
3. Review AppProject sourceRepos and cluster destinations — RBAC ≠ destination hard limits alone (projects also constrain).

### 7. Hand off

1. Document roles, group mapping, and break-glass admin.
2. Store policy.csv in Git; avoid Console-only edits.
3. Cross-link `argocd-rbac-csv` for large policy files and `argocd-app-of-apps` for topology.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default | readonly or deny | default admin |
| Tenancy | AppProject roles + source/dest limits | one global `*/*` for all devs |
| Admin | tiny platform group | every engineer is admin |
| SSO | groups claim mapped in scopes | email-only with manual user lines forever |
| Exec | disabled for most roles | developers get cluster exec everywhere |
| Change | GitOps + tested matrix | live edit without backup |

## Output Checklist

- [ ] Instance, version, SSO, projects, authorization recorded
- [ ] Baseline rbac-cm and AppProjects exported
- [ ] Roles and group bindings least-privilege
- [ ] policy.default safe; admin path documented
- [ ] Project isolation verified (allow/deny matrix)
- [ ] exec/delete/cluster write restricted
- [ ] scopes match IdP claims
- [ ] Monitoring on RBAC ConfigMap changes
- [ ] `code-quality-standards` applied if manifests shipped

## Rules

- Authorized control planes only.
- Never remove break-glass access without a tested alternate.
- RBAC changes need evidence (user/group matrix), not “looks fine in UI”.
- Prefer project-scoped roles for multi-team GitOps.
- Keep this skill on Argo CD authz; route Workflows and pure K8s RBAC elsewhere.
