---
name: kubernetes-guidance
description: Guidance for working with Kubernetes resources in this homelab Flux repository. Use when navigating, modifying, or deploying K8s apps, Flux Kustomizations, CNPG databases, Helm charts, or SOPS secrets.
---

# Homelab Kubernetes Structure Guide

This document provides a routing map of the Kubernetes directory structure for agents and developers to quickly understand the organization and find relevant components.

## Directory Overview

```
kubernetes/
├── apps/           # Application deployments (15 apps, each self-contained)
├── cluster/        # Flux bootstrap entry point + namespace definitions
└── components/     # Shared Kustomize Components (clustersettings)
```

## Architecture Pattern

This repo uses **Flux-native Kustomization CRDs** at three tiers:

1. **Cluster tier** (`cluster/`) — Flux bootstrap, namespace definitions, and per-app Flux Kustomization CRDs
2. **App tier** (`apps/<app>/`) — Top-level Flux Kustomization CRDs that point to sub-app directories
3. **Sub-app tier** (`apps/<app>/<sub>/`) — Actual Kubernetes manifests (HelmReleases, secrets, etc.)

Flux reconciles from `cluster/flux-system/gotk-sync.yaml` → `cluster/apps.yaml` → `cluster/apps/*.yaml` → `apps/<app>/*.yaml` → `apps/<app>/<sub>/`

## Detailed Structure

### 1. `apps/` - Application Layer

Each app is self-contained with its own Flux Kustomization CRDs, Helm charts, secrets, and repos.

```
apps/
├── kustomization.yaml          # Aggregates all app-level kustomizations
│
├── authentik/                  # Authentik SSO + PostgreSQL (CNPG)
│   ├── authentik.yaml          # Flux Kustomization → authentik/authentik/
│   ├── cnpg.yaml               # Flux Kustomization → authentik/cnpg/
│   ├── kustomization.yaml      # Kustomize: sets namespace, includes sub-apps + repos
│   ├── authentik-clustersettings.secret.sops.yaml
│   ├── authentik/              # HelmRelease, httproute, values, kustomizeconfig
│   ├── cnpg/                   # CNPG cluster, scheduledbackup, objectstore, secrets
│   └── repos/                  # HelmRepository (authentik.helm.yaml)
│
├── cert-manager/               # cert-manager + Cloudflare/Local issuers
│   ├── cert-manager.yaml       # Flux Kustomization → cert-manager/cert-manager/
│   ├── kustomization.yaml
│   ├── cert-manager/           # HelmRelease, certificates, clusterissuers, secrets
│   └── repos/                  # HelmRepository (jetstack.helm.yaml)
│
├── cloudflare-ddns/            # Dynamic DNS controller
│   ├── cloudflare-ddns.yaml    # Flux Kustomization → cloudflare-ddns/cloudflare-ddns/
│   ├── kustomization.yaml
│   └── cloudflare-ddns/        # Deployment + SOPS secret
│
├── cnpg-system/                # CloudNativePG operator + Barman plugin
│   ├── cnpg.yaml               # Flux Kustomization → cnpg-system/cnpg/
│   ├── artifacts.yaml          # Flux Kustomization → cnpg-system/artifacts/
│   ├── plugin-barman-cloud.yaml # Flux Kustomization → cnpg-system/plugin-barman-cloud/
│   ├── kustomization.yaml
│   ├── cnpg/                   # HelmRelease
│   ├── artifacts/              # ImageCatalog
│   ├── plugin-barman-cloud/    # HelmRelease
│   └── repos/                  # HelmRepository (cnpg.oci, artifacts.git, plugin-barman-cloud.oci)
│
├── dbgate/                     # Database management GUI
│   ├── dbgate.yaml             # Flux Kustomization → dbgate/dbgate/
│   ├── kustomization.yaml
│   └── dbgate/                 # Deployment, Service, PVC, httproute
│
├── default/                    # Gateway API CRDs
│   ├── gatewayapi.yaml         # Flux Kustomization → default/gateway/
│   ├── kustomization.yaml
│   └── gateway/                # Gateway API experimental-install.yaml
│
├── glance/                     # Glance dashboard
│   ├── glance.yaml             # Flux Kustomization → glance/glance/
│   ├── kustomization.yaml
│   └── glance/                 # Deployment, Service, PVC, httproute, config, SOPS secret
│
├── grafana-operator/           # Grafana Operator (manages Grafana instances)
│   ├── grafana-operator.yaml   # Flux Kustomization → grafana-operator/grafana-operator/
│   ├── kustomization.yaml
│   ├── grafana-operator/       # HelmRelease, values, kustomizeconfig
│   └── repos/                  # HelmRepository (grafana-operator.oci)
│
├── istio-system/               # Istio service mesh (base, cni, istiod, ztunnel, gateway, certs)
│   ├── base.yaml               # Flux Kustomization → istio-system/base/
│   ├── cert-manager.yaml       # Flux Kustomization → istio-system/cert-manager/
│   ├── cni.yaml                # Flux Kustomization → istio-system/cni/
│   ├── gateway.yaml            # Flux Kustomization → istio-system/gateway/
│   ├── istiod.yaml             # Flux Kustomization → istio-system/istiod/
│   ├── ztunnel.yaml            # Flux Kustomization → istio-system/ztunnel/
│   ├── kustomization.yaml
│   ├── base/                   # HelmRelease (istio-base)
│   ├── cert-manager/           # Certificates for istio
│   ├── cni/                    # HelmRelease (istio-cni)
│   ├── gateway/                # Gateway resource + ReferenceGrant
│   ├── istiod/                 # HelmRelease (istiod), values, kustomizeconfig
│   ├── ztunnel/                # HelmRelease (ztunnel), values, kustomizeconfig
│   └── repos/                  # HelmRepository (base.oci, cni.oci, istiod.oci, ztunnel.oci)
│
├── kite/                       # Kite app + PostgreSQL (CNPG)
│   ├── kite.yaml               # Flux Kustomization → kite/kite/
│   ├── cnpg.yaml               # Flux Kustomization → kite/cnpg/
│   ├── kustomization.yaml
│   ├── kite/                   # HelmRelease, httproute, SOPS secret, values
│   ├── cnpg/                   # CNPG cluster, scheduledbackup, objectstore, secrets
│   └── repos/                  # HelmRepository (kite.oci)
│
├── monitoring/                 # Full observability stack
│   ├── alloy.yaml              # Flux Kustomization → monitoring/alloy/
│   ├── grafana.yaml            # Flux Kustomization → monitoring/grafana/
│   ├── kube-prometheus-stack.yaml # Flux Kustomization → monitoring/kube-prometheus-stack/
│   ├── loki.yaml               # Flux Kustomization → monitoring/loki/
│   ├── tempo.yaml              # Flux Kustomization → monitoring/tempo/
│   ├── prometheus-operator-crds.yaml # Flux Kustomization → monitoring/prometheus-operator-crds/
│   ├── kustomization.yaml
│   ├── alloy/                  # Grafana Alloy (metrics/logs collection), httproute
│   ├── grafana/                # Grafana instance + PostgreSQL (CNPG) + dashboards/datasources/folders
│   │   ├── cnpg/               # CNPG cluster for Grafana
│   │   ├── dashboard/          # Grafana Dashboard CRDs (14 dashboards)
│   │   ├── datasource/         # GrafanaDatasource CRDs (prometheus, loki, tempo, alertmanager)
│   │   ├── folder/             # GrafanaFolder CRDs (kubernetes, logging, monitoring, programming, storage)
│   │   └── grafana/            # Grafana CRD, httproute, admin-creds secret
│   ├── kube-prometheus-stack/  # Prometheus + Alertmanager + node-exporter
│   ├── loki/                   # Log aggregation
│   ├── tempo/                  # Distributed tracing
│   └── repos/                  # HelmRepositories (grafana.helm, kube-prometheus-stack.oci, loki.oci, tempo.oci, prometheus-operator-crds.oci)
│
├── redpanda/                   # Redpanda streaming platform
│   ├── redpanda.yaml           # Flux Kustomization → redpanda/redpanda/
│   ├── kustomization.yaml
│   ├── redpanda/               # HelmRelease, httproute, values
│   └── repos/                  # HelmRepository (redpanda.helm)
│
├── reloader/                   # Reloader (auto-restart on secret/configmap changes)
│   ├── reloader.yaml           # Flux Kustomization → reloader/reloader/
│   ├── kustomization.yaml
│   ├── reloader/               # HelmRelease
│   └── repos/                  # HelmRepository (reloader.helm)
│
└── rustfs/                     # RustFS (S3-compatible storage)
    ├── rustfs.yaml             # Flux Kustomization → rustfs/rustfs/
    ├── kustomization.yaml
    ├── rustfs-clustersettings.secret.sops.yaml
    ├── rustfs/                 # HelmRelease, httproute, values
    └── repos/                  # HelmRepository (rustfs.helm)
```

### 2. `cluster/` - Flux Bootstrap Entry Point

```
cluster/
├── apps.yaml                 # Flux Kustomization: points to kubernetes/apps/ with SOPS decryption
├── namespaces.yaml           # All namespace definitions (single file)
├── apps/                     # Per-app Flux Kustomization CRDs
│   ├── authentik.yaml        # Flux Kustomization CRD with decryption + substituteFrom
│   ├── cert-manager.yaml
│   ├── cloudflare-ddns.yaml
│   ├── cnpg-system.yaml
│   ├── dbgate.yaml
│   ├── flux-system.yaml
│   ├── gatewayapi.yaml
│   ├── glance.yaml
│   ├── grafana-operator.yaml
│   ├── istio-system.yaml
│   ├── kite.yaml
│   ├── monitoring.yaml
│   ├── redpanda.yaml
│   ├── reloader.yaml
│   └── rustfs.yaml
└── flux-system/              # Flux bootstrap manifests
    ├── gotk-components.yaml
    ├── gotk-sync.yaml        # Root: points to kubernetes/cluster/
    └── kustomization.yaml
```

**Key Concepts:**

- `cluster/flux-system/gotk-sync.yaml` is the **Flux root** — points to `kubernetes/cluster/`
- `cluster/apps.yaml` (Flux Kustomization) → builds `kubernetes/apps/` with SOPS decryption
- `cluster/apps/*.yaml` are Flux Kustomization CRDs that define dependencies and decryption per app
- `cluster/namespaces.yaml` centralizes all namespace definitions

### 3. `components/` - Shared Kustomize Components

```
components/
└── clustersettings/
    ├── kustomization.yaml    # Component type (not Kustomization)
    ├── configmap.yaml        # Shared ConfigMap for variable substitution
    └── secret.sops.yaml      # Shared SOPS-encrypted Secret for variable substitution
```

**Usage:** Apps include this via `components: [../../components/clustersettings/]` in their kustomization.yaml. This injects shared ConfigMap/Secret into the rendered manifests for Flux `postBuild.substituteFrom`.

## Flux Kustomization CRD Fields

Each Flux Kustomization CRD should have these fields:

| Field | Purpose | Required |
|-------|---------|----------|
| `decryption` | SOPS decryption provider + secretRef | Yes (if app has .sops.yaml files) |
| `postBuild.substituteFrom` | Variable substitution from ConfigMap/Secret | Yes (if app uses `${VARIABLE}` syntax) |
| `dependsOn` | Flux dependency ordering | Yes (if app depends on another) |
| `namespace` | Target namespace | No (set in kustomization.yaml instead) |

**Standard substituteFrom chain:**
```yaml
postBuild:
  substituteFrom:
    - kind: Secret
      name: clustersetting
    - kind: ConfigMap
      name: clustersetting
```

Some apps also include app-specific clustersettings (e.g., `authentik-clustersettings`, `rustfs-clustersettings`).

## CNPG Backup Configuration

All databases use the **plugin method** with Barman Cloud:

- **Method**: `plugin` (not `barmanObjectStore`)
- **Plugin**: `barman-cloud.cloudnative-pg.io`
- **Configuration Location**: `apps/<app>/cnpg/<app>.cluster.yaml`

### Current Databases with CNPG:

| Database | Location | Cluster Name |
|----------|----------|--------------|
| `authentik` | `apps/authentik/cnpg/` | `authentik-authentik` |
| `kite` | `apps/kite/cnpg/` | `kite-kite` |
| `grafana` | `apps/monitoring/grafana/cnpg/` | `grafana-cnpg-grafana` |

## Dependency Chain

```
gatewayapi
├── istio-system
│   ├── istio-system-base → cni, istiod, ztunnel
│   ├── istio-system-gateway
│   └── istio-system-cert-manager
├── dbgate
├── glance
├── redpanda
├── rustfs
├── monitoring-alloy
├── monitoring-grafana (also depends on grafana-operator)
├── monitoring-kube-prometheus-stack (also depends on prometheus-operator-crds)
└── app-kite (also depends on istio-system, cnpg-system)

cert-manager
└── cnpg-system
    └── cnpg-system-cnpg → cnpg-system-plugin-barman-cloud
        └── authentik-cnpg → authentik-authentik
        └── kite-cnpg → kite-kite
```

## Navigation Guide

### Finding Configuration

| Task | Location |
|------|----------|
| Add/modify an app | `apps/<app>/kustomization.yaml` + create Flux Kustomization CRD |
| Add sub-app | Create `apps/<app>/<sub>/` with manifests, add Flux Kustomization CRD in parent |
| Configure database backup | `apps/<app>/cnpg/<app>.cluster.yaml` (CNPG cluster spec) |
| Add Helm chart | Create `apps/<app>/repos/<chart>.yaml` (HelmRepository) |
| Add Grafana dashboard | `apps/monitoring/grafana/dashboard/<name>.yaml` |
| Add Grafana datasource | `apps/monitoring/grafana/datasource/<name>.yaml` |
| Add shared variables | `components/clustersettings/configmap.yaml` or `secret.sops.yaml` |
| Deploy to production | Ensure `cluster/apps/<app>.yaml` Flux Kustomization CRD exists and is listed |

### Adding a New App

1. Create `apps/<app>/kustomization.yaml` with `namespace:` set
2. Create `apps/<app>/<sub>/` with HelmRelease, values, kustomizeconfig
3. Create `apps/<app>/<sub>/kustomization.yaml` with resources + configMapGenerator
4. Create `apps/<app>/repos/<chart>.yaml` if using Helm charts
5. Create Flux Kustomization CRD at `apps/<app>/<app>.yaml` with `decryption`, `postBuild`, `dependsOn`
6. Add to `apps/kustomization.yaml` resources list
7. Create `cluster/apps/<app>.yaml` (Flux Kustomization CRD for cluster-level)
8. Add namespace to `cluster/namespaces.yaml`
9. Include `components: [../../components/clustersettings/]` in kustomization.yaml if app needs shared config

## SOPS Encryption/Decryption

This repo uses `sops` with age encryption (key: `age1ytym...f2sy4`). The `.sops.yaml` config has two relevant rules:

- `kubernetes/.*\.sops\.ya?ml` — encrypts `^(data|stringData)$` (K8s secrets with `stringData` or `data`)
- `kubernetes/.*values\.sops\.ya?ml` — encrypts `^(.*)$` (Helm values files, everything)

**Commands:**

```bash
# Encrypt a new secret (in-place)
sops encrypt -i kubernetes/apps/<app>/<sub>/<file>.sops.yaml

# Decrypt to view contents (stdout)
sops decrypt kubernetes/apps/<app>/<sub>/<file>.sops.yaml

# Edit a SOPS file in-place (decrypts, opens $EDITOR, re-encrypts)
sops kubernetes/apps/<app>/<sub>/<file>.sops.yaml
```

**Workflow:**
1. Create the plain `secret.yaml` (or `values.yaml`) with `stringData`/`data` as normal
2. Rename to `<name>.secret.sops.yaml` or `<name>.sops.yaml` (must match `.sops.yaml` regex)
3. Run `sops encrypt -i <file>`
4. Update the sub-app kustomization.yaml to reference `./<file>.sops.yaml`
5. The app-level Flux Kustomization CRD must have `decryption: provider: sops` + `secretRef: sops-age`

## Environment Variables & Secrets

- Shared config: `components/clustersettings/configmap.yaml` + `secret.sops.yaml`
- App-specific: `apps/<app>/<app>-clustersettings.secret.sops.yaml` (SOPS-encrypted)
- Flux substitutes variables via `postBuild.substituteFrom` at reconcile time
- SOPS secrets are decrypted by Flux using the `sops-age` Secret

## Quick Lookup

| Question | Answer |
|----------|--------|
| "Where is Kite configured?" | `apps/kite/kite/` (HelmRelease + values) |
| "Where are Kite backups defined?" | `apps/kite/cnpg/scheduledbackup.yaml` |
| "How do I add a new app?" | See "Adding a New App" above |
| "What gets deployed?" | `cluster/apps.yaml` → `cluster/apps/*.yaml` → `apps/` |
| "Where are namespaces defined?" | `cluster/namespaces.yaml` |
| "Where are shared variables?" | `components/clustersettings/` |
| "Where is the Grafana database?" | `apps/monitoring/grafana/cnpg/grafana.cluster.yaml` |
| "Which apps use SOPS?" | Apps with `.secret.sops.yaml` files need `decryption` in their Flux Kustomization |
