---
name: argocd-rbac-csv
description: >
  Authoring and reviewing Argo CD policy.csv Casbin lines for owned control planes:
  p/g syntax, resource/action/object wildcards, deny effects, group bindings, and
  validation of large multi-role files. Use when policy.csv grows beyond basics or
  permission matrix tests fail — not for generic Kubernetes RBAC or attacking Argo CD.
---

# Argo CD RBAC CSV

## Scope And Authorization

- **In scope:** Editing `argocd-rbac-cm` `policy.csv` / related policy files on Argo CD you operate with authorization.
- **Out of scope:** Third-party Argo CD instances; social-engineering SSO groups.
- Bad CSV can deny everyone or grant admin — always keep local admin break-glass.
- Version-control the CSV; review diffs like IAM policy.
- Pair with `argo-cd-rbac-basics` for overall model; this skill is the CSV deep-dive.

## When To Use

- Writing multi-role `policy.csv` with fine-grained project/app objects.
- Debugging why a group can sync one app but not another.
- Adding deny rules (e.g. block `delete`/`exec` for developers).
- Migrating email user lines to IdP group `g,` bindings.
- Validating CSV after merge conflicts or bulk edits.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Overall Argo CD RBAC design | `argo-cd-rbac-basics` |
| App-of-apps structure | `argocd-app-of-apps` |
| Workflows RBAC | `argo-workflows-rbac` |
| Kubernetes Role/RoleBinding | cluster RBAC skill |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| CSV form | Syntax |
| --- | --- |
| Permission | `p, <sub>, <res>, <act>, <obj>, <eft>` |
| Role binding | `g, <user-or-group>, <role>` |
| Built-in roles | `role:admin`, `role:readonly` (distribution may ship defaults) |
| Objects | `*/*`, `<project>/*`, `<project>/<app>` |
| Effects | `allow`, `deny` |

## Resource And Action Reference (common)

| Resource | Typical actions |
| --- | --- |
| applications | get, create, update, delete, sync, override, action, invoke |
| applicationsets | get, create, update, delete |
| projects | get, create, update, delete |
| repositories | get, create, update, delete |
| clusters | get, create, update, delete |
| logs | get |
| exec | create |
| certificates | get, create, update, delete |
| accounts | get, update (admin) |
| gpgkeys | get, create, delete |
| extensions | invoke (version-dependent) |

Confirm exact resources for your Argo CD version in upstream RBAC docs.

## Workflow

### 1. Confirm scope and success criteria

1. Record Argo CD version, IdP groups claim, projects/apps inventory.
2. Success: matrix of (group × app × action) matches design; CSV parses without lockout.
3. Snapshot current ConfigMap before edit.

### 2. Inventory and export

```bash
kubectl -n argocd get cm argocd-rbac-cm -o jsonpath='{.data.policy\.csv}' > policy.csv
kubectl -n argocd get cm argocd-rbac-cm -o jsonpath='{.data.policy\.default}'
kubectl -n argocd get cm argocd-rbac-cm -o jsonpath='{.data.scopes}'
# Optional: policy.matchMode if present (glob vs regex) — version specific
```

1. Split roles mentally: readonly, dev, release, platform.
2. List all `g,` subjects (users vs groups).
3. Find overly broad lines: `p, role:x, *, *, */*, allow`.

### 3. Baseline

1. Store `policy.csv` hash in ticket.
2. Collect failing cases: user, attempted action, object, error text.
3. Confirm `scopes` includes the claim that carries groups.

### 4. Author CSV carefully

**Structured example:**

```csv
# ----- roles: permissions -----
p, role:readonly, applications, get, */*, allow
p, role:readonly, projects, get, *, allow
p, role:readonly, repositories, get, *, allow
p, role:readonly, clusters, get, *, allow

p, role:app-dev, applications, get, */*, allow
p, role:app-dev, applications, sync, dev/*, allow
p, role:app-dev, applications, update, dev/*, allow
p, role:app-dev, logs, get, dev/*, allow
p, role:app-dev, exec, create, */*, deny
p, role:app-dev, applications, delete, */*, deny

p, role:app-release, applications, get, */*, allow
p, role:app-release, applications, sync, prod/*, allow
p, role:app-release, applications, delete, prod/*, deny
p, role:app-release, logs, get, prod/*, allow

p, role:repo-admin, repositories, *, *, allow
p, role:cluster-admin-lite, clusters, get, *, allow

# ----- bindings -----
g, org:viewers, role:readonly
g, org:dev-team, role:app-dev
g, org:release-managers, role:app-release
g, org:platform, role:admin
```

**Object matching tips**

1. `dev/*` = all apps in AppProject `dev`.
2. `dev/payment-api` = single app.
3. `*` for projects/repos/clusters resources often means all objects of that type (confirm version).
4. Prefer explicit project prefixes over global `*/*` for mutating actions.

**Editing process**

```bash
# Apply via kubectl edit or GitOps
kubectl -n argocd create cm argocd-rbac-cm \
  --from-file=policy.csv=./policy.csv \
  --dry-run=client -o yaml | kubectl apply -f -
# Ensure other keys (policy.default, scopes) preserved — prefer full render from Git
```

1. Preserve `policy.default` (e.g. `role:readonly`) when rebuilding ConfigMap.
2. Avoid Windows CRLF if parser is picky; use LF.
3. Comment lines with `#` supported in policy.csv.

### 5. Verify with evidence

```bash
# Reload: Argo CD watches CM; if needed restart server components per version docs
kubectl -n argocd rollout restart deploy/argocd-server
# Test identities (SSO user or --as if impersonation available in your setup)
argocd account can-i sync applications 'dev/foo'  # if CLI supports can-i in your version
# Practical tests:
argocd app sync dev/foo      # as dev group user → allow
argocd app sync prod/foo     # as dev group user → deny
argocd app delete prod/foo   # deny
```

| Subject | Action | Object | Expected |
| --- | --- | --- | --- |
| org:dev-team | sync | dev/* | allow |
| org:dev-team | sync | prod/* | deny |
| org:dev-team | exec | any | deny |
| org:platform | * | * | allow (admin) |

1. Confirm groups appear in user info after login.
2. Regression: readonly still works for unauthenticated-to-role default users.

### 6. Observe and harden

1. Lint PRs: forbid new `*, *, */*, allow` except platform role.
2. Alert on ConfigMap changes.
3. Periodically remove stale `g, user@…` lines after SSO migration.

### 7. Hand off

1. Keep CSV in Git with CODEOWNERS = platform security.
2. Document role catalog and matrix.
3. Link AppProject roles when CSV should stay small (`proj:<project>:<role>` policies).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Mutating verbs | Scoped to project | `applications, *, */*, allow` for all devs |
| Deny | explicit deny for exec/delete | hope UI hides buttons |
| Bindings | IdP groups | long email lists only |
| Default | readonly | empty default + accidental admin |
| Edits | Git PR + matrix test | kubectl edit without backup |
| Objects | `proj/app` precision | wrong project name silently denying |

## Output Checklist

- [ ] Version, scopes, policy.default recorded
- [ ] Baseline CSV exported and hashed
- [ ] Roles structured; broad admin minimized
- [ ] Group bindings use IdP groups
- [ ] Deny rules for exec/delete as required
- [ ] Allow/deny matrix tested with real users/groups
- [ ] ConfigMap keys preserved; LF/format valid
- [ ] Git ownership and alerts set
- [ ] `code-quality-standards` applied if automation ships

## Rules

- Authorized Argo CD only; keep break-glass admin.
- Treat CSV like production IAM — review every line.
- Prefer project-scoped objects for sync/update/delete.
- Validate with real group claims, not only YAML syntax.
- Deep CSV focus here; overall RBAC product design stays in `argo-cd-rbac-basics`.
