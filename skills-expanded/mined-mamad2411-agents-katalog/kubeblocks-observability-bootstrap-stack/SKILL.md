---
name: kubeblocks-observability-bootstrap-stack
version: "0.1.0"
description: Bootstrap a Prometheus / Grafana monitoring stack for KubeBlocks database metrics when no usable observability base exists yet.
---

# KubeBlocks Observability: Bootstrap Stack

Use this path only when the environment does **not** already have a usable Prometheus / Grafana base.

If the cluster already has monitoring infrastructure, route to [kubeblocks-observability-existing-stack](../kubeblocks-observability-existing-stack/SKILL.md) instead.

## Workflow

```text
- [ ] Step 1: Confirm no existing stack should be reused
- [ ] Step 2: Install kube-prometheus-stack
- [ ] Step 3: Add scrape config for KubeBlocks clusters
- [ ] Step 4: Confirm readiness level
```

## Step 1: Confirm No Existing Stack Should Be Reused

```bash
kubectl get pods -A | grep -E 'prometheus|grafana' || true
```

If Prometheus / Grafana already exists and is the team's system of record, stop and use the existing-stack path instead.

## Step 2: Install kube-prometheus-stack

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

Wait for operator, Prometheus, and Grafana pods to become ready.

## Step 3: Add Scrape Config

After the stack exists, add `PodMonitor` / `ServiceMonitor` for KubeBlocks-managed database pods.

See the compatibility shim [kubeblocks-setup-monitoring](../kubeblocks-setup-monitoring/SKILL.md) and the original reference file at [../kubeblocks-setup-monitoring/references/reference.md](../kubeblocks-setup-monitoring/references/reference.md) for addon-specific exporter notes.

## Step 4: Confirm Readiness Level

At minimum, state whether the result is:

- `metrics-ready`
- `scrape-ready`
- `dashboard-ready`
- `alerting-ready`

Do not collapse all of these into "monitoring is ready".
