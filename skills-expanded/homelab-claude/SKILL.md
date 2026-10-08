# Homelab GitOps

## Repo Structure

Each app has its own directory containing `values.yaml` (Helm values),
`sealed-secret.yaml` (encrypted — safe to commit), and raw manifests
(namespace, storage, CRDs, etc.). ArgoCD Application definitions live in
`argocd/apps/*.yaml`.

## ArgoCD Multi-Source Pattern

All apps use a 3-source pattern:

- **Source 1**: Upstream Helm chart. References `$repo` alias for `valueFiles`.
- **Source 2**: This Git repo with `ref: repo` — required so Source 1 can
  resolve `$repo/<app>/values.yaml`.
- **Source 3** (optional): This Git repo at `path: <app>` with a
  `directory.include` glob for raw manifests. Files not in the `include:` list
  are ignored by ArgoCD even if present in the directory.

`targetRevision: '*'` means latest chart release. Immich uses a pinned version
because the chart version must match the `immich-server` image tag in
`values.yaml`.

See `argocd/apps/immich.yaml` for the canonical pinned-version example.

## ArgoCD Is Self-Managed

ArgoCD manages itself via `argocd/apps/argocd.yaml` (3-source pattern).
Chart upgrades go through the normal GitOps flow — merge to `main`, ArgoCD
self-syncs. The Tailscale Ingress for ArgoCD (`argocd/tailscale-ingress.yaml`)
is also managed by this Application.

## Bootstrapping a Fresh Cluster

After running k3s-ansible to bring up the K3s nodes:

```bash
# 1. Install ArgoCD (one-time manual step)
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd -n argocd --create-namespace -f argocd/values.yaml

# 2. Apply the root "App of Apps" — ArgoCD takes over everything else
kubectl apply -f argocd/apps.yaml
```

ArgoCD syncs `argocd/apps/` and creates all child Applications automatically.
Monitor progress with `kubectl get applications -n argocd`.

## Sealed Secrets Workflow

Create a new SealedSecret:

```bash
kubectl create secret generic <name> -n <namespace> \
  --from-literal=KEY=VALUE \
  --dry-run=client -o yaml \
  | kubeseal \
      --controller-name sealed-secrets-controller \
      --controller-namespace kube-system \
      --format yaml > <app>/sealed-secret.yaml
```

The master key backup lives at `sealed-secrets/sealed-secrets-master-keys.yaml`
(gitignored). Regenerate it with:

```bash
kubectl get secrets -n kube-system \
  -l sealedsecrets.bitnami.com/sealed-secrets-key=active \
  -o yaml > sealed-secrets/sealed-secrets-master-keys.yaml
```

Keep it backed up externally — without it, all SealedSecrets are unrecoverable
after a cluster rebuild.

## Tailscale Operator

OAuth credentials are **not** in `tailscale/values.yaml` — they are passed via
`--set-string` at initial install time (see `tailscale/README.md`).

To expose a service via Tailscale, commit a `tailscale-ingress.yaml` in the app
directory and add it to the ArgoCD Application's `include:` glob.

## Handling Chart-Generated Secrets

Charts that generate random values on each render (e.g., Grafana admin
password) cause perpetual OutOfSync. Fix pattern:

1. Add `ignoreDifferences` on the Secret's data fields and any Deployment
   `checksum/secret` annotation.
2. Add `RespectIgnoreDifferences=true` to `syncOptions`.

See `argocd/apps/monitoring.yaml` for the canonical example.

## Renovate Conventions

- Renovate detects chart versions from `argocd/apps/*.yaml` (ArgoCD preset)
  and image tags from `immich/`, `monitoring/`, `home-assistant/` manifests.
- Custom regex managers handle non-standard `tag:` fields in `immich/values.yaml`
  and `kube-vip/values.yaml`.
- Commit format: semantic (`feat:`, `fix:`, `chore:`, `docs:`).
- Update schedules: Immich — immediate; infrastructure, monitoring,
  home-assistant — monthly (first of month, before 6am).
- Immich PRs include a reminder to verify the PostgreSQL backup CronJob ran.

## Adding a New App

1. Create `<app>/` with `values.yaml` and raw manifests.
2. Add `argocd/apps/<app>.yaml` using the 3-source pattern.
3. If secrets are needed, create `<app>/sealed-secret.yaml` via kubeseal.
4. Commit and merge to `main` — the root `apps` Application picks it up automatically.

## Cluster Access

The Kubernetes MCP server is configured in `.mcp.json`. Claude can query the
cluster directly via the `mcp__kubernetes__*` tools without running kubectl.

The Grafana MCP server is also configured in `.mcp.json`. Claude can query
metrics (PromQL), logs (LogQL), and dashboards via `mcp__grafana__*` tools.
The ArgoCD MCP server enables application management via `mcp__argocd__*`
tools. Both servers' tokens are injected from Vaultwarden via mise
(`scripts/env-secrets.sh`). When you `cd` into this repo, mise automatically
sources the script, which unlocks Bitwarden if needed and exports the tokens.
No manual `export` step required — just ensure `bw` is installed and your
vault master password is accessible.

## Parallel Work with Git Worktrees

ArgoCD tracks `main` — all work happens on feature branches via PRs. For
parallel Claude agents, use worktrees so each has an isolated working directory:

```bash
git worktree add ../homelab-<task> -b <type>/<app>-<description>
git worktree remove ../homelab-<task> && git branch -d <type>/<app>-<description>
```

## Cluster Gotchas

Hard-won lessons from operating this cluster are recorded in the auto-memory
system at `~/.claude/projects/-home-benkim0414-workspace-homelab/memory/MEMORY.md`.
Always check "Key Learnings" there before touching: k3s nodes, containerd,
Flannel/CNI, Sealed Secrets, or ArgoCD sync operations.

When a new gotcha is discovered: record it in memory AND propose a rule here
if the same mistake is likely to recur.
