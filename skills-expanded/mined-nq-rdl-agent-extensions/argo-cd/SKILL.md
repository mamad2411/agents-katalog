---
name: argo-cd
license: CC-BY-4.0
description: >-
  Manage ArgoCD configuration, including applications, projects, repositories,
  clusters, and RBAC. Also used to sync and check the health of ArgoCD apps.
  Use when the user mentions GitOps, Argo, application deployment, Kustomize/Helm
  in ArgoCD context, or asks to install/use the argocd CLI.
compatibility: >-
  Requires the argocd CLI and kubectl access to a cluster running Argo CD.
  Examples checked against Argo CD v3.5.3 docs and CLI on 2026-09-29;
  inline kustomize patches need Argo CD v2.9+ and native OCI sources v3.1+.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# ArgoCD Skill

This skill allows the agent to interact with ArgoCD using the `argocd` CLI tool,
as well as create Declarative GitOps configurations.

Verify against the canonical docs (https://argo-cd.readthedocs.io/en/stable/)
when being wrong would mislead, and check the server version with
`argocd version` before relying on a field or flag.

## Tool Setup

The `argocd` CLI might need to be downloaded if not present. The installation script downloads
the current stable release into the working directory and verifies it against the release's
`cli_checksums.txt`:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/manage/scripts/install-cli.sh"
sudo mv argocd /usr/local/bin/
```

Or you can use Homebrew on macOS:

```bash
brew install argocd
```

## Basic CLI Commands

- Login: `argocd login <SERVER>` (Needs initial password `argocd admin initial-password -n argocd` or other configuration)
- List apps: `argocd app list`
- Get app status: `argocd app get <app-name>`
- Sync an app: `argocd app sync <app-name>`
- Create app (CLI): `argocd app create <name> --repo <repo> --path <path> --dest-server <server> --dest-namespace <namespace>`
- Create project: `argocd proj create <project-name> -d <server>,<namespace> -s <repo>`

## Declarative Setup

ArgoCD configurations are often applied as Custom Resources (CRs) using `kubectl apply`.

### Application Definition

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Tool support: Kustomize

When the source path has a `kustomization.yaml`, ArgoCD detects it as a Kustomize application.
You can set parameters such as inline `patches` (Argo CD v2.9+) in the `Application` spec:

```yaml
  source:
    path: kustomize-guestbook
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: master
    kustomize:
      patches:
        - target:
            kind: Deployment
            name: guestbook-ui
          patch: |-
            - op: replace
              path: /spec/template/spec/containers/0/ports/0/containerPort
              value: 443
```

`kustomize.version: <version>` selects a non-bundled Kustomize. It only works when that binary
is added to the Argo CD image and registered in `argocd-cm` as `kustomize.path.<version>`
(for example `kustomize.path.v3.5.4: /custom-tools/kustomize_3_5_4`). Argo CD v3.5.3 bundles
Kustomize 5.8.1; omit `version` to use it.

### Tool support: Helm

Helm charts can be passed parameters via `helm.parameters` or `helm.values`.

```yaml
  source:
    repoURL: https://charts.jetstack.io
    targetRevision: v1.21.2
    chart: cert-manager
    helm:
      parameters:
      - name: "crds.enabled"
        value: "true"
      values: |
        prometheus:
          enabled: false
```

### Tool support: OCI

Helm charts can also be pulled from OCI registries (e.g. Amazon ECR, Google GCR, Docker Hub).
As a Helm source, the registry goes in `repoURL` without the `oci://` scheme:

```yaml
  source:
    repoURL: registry-1.docker.io/bitnamicharts  # no oci:// prefix
    targetRevision: 15.9.0
    chart: nginx
```

As a native OCI source (Argo CD v3.1+), use the `oci://` scheme with the full artifact path and `path: .`:

```yaml
  source:
    repoURL: oci://registry-1.docker.io/bitnamicharts/nginx
    targetRevision: 15.9.0
    path: .
```

Bitnami's 2025 catalog change (https://github.com/bitnami/charts/issues/35164) stopped updates
for charts outside its free community tier and moved versioned images to `bitnamilegacy`, so
older `bitnamicharts` versions may need image overrides.

### Projects & RBAC

ArgoCD Projects logically group applications. By default, applications use the `default` project.
Projects can restrict allowed source repos, destination clusters, and kinds of resources.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: my-project
  namespace: argocd
spec:
  description: Example Project
  sourceRepos:
  - "https://github.com/my-org/*"
  destinations:
  - namespace: my-namespace
    server: https://kubernetes.default.svc
  clusterResourceWhitelist:
  - group: '*'
    kind: '*'
```

## Private Repositories

If the Git repository is private, credentials must be added to ArgoCD, often as a Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: private-repo-secret
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  url: https://github.com/my-org/private-repo.git
  username: my-username
  password: my-password
```
For project scoped repositories, add `project: <project-name>` to `stringData`.

### Auditing Projects

As a skill, you can use ArgoCD to audit projects. When requested to audit a project, evaluate the following:

- **Source Repositories (`sourceRepos`)**: Are there unexpected or overly permissive wildcards allowing unknown code origins? E.g., `*` vs `https://github.com/my-org/*`.
- **Destinations (`destinations`)**: Where is the project permitted to deploy? Are `kube-system` or root cluster targets appropriately restricted?
- **Resource Kinds**: Are cluster-scoped resources (`clusterResourceWhitelist` or `clusterResourceBlacklist`) restricted appropriately? E.g., is the project allowed to create new Namespaces or CRDs unchecked?
- **Roles & RBAC**: Are roles defined using least privilege? Examine defined `roles` to ensure policies don't grant broader access than necessary (e.g., granting `*` on `applications` unless intended).
