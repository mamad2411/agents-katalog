---
name: gke
description: "Deploy and manage Kubernetes workloads on Google Kubernetes Engine (GKE). Covers Autopilot and Standard modes, Workload Identity, node pool management, networking, security, and gcloud/kubectl CLI patterns. Warns before cluster creation (billable). Use when the user mentions: kubernetes on GCP, create GKE cluster, GKE autopilot, kubectl GCP, GKE networking, GKE security."
license: MIT
metadata:
  "googlecloud-plugin/version": "0.1"
  "googlecloud-plugin/triggers": "GKE, kubernetes on GCP, google kubernetes engine, create GKE cluster, workload identity, node pool, GKE autopilot, kubectl GCP, GKE networking, GKE security"
  "googlecloud-plugin/required-scopes": "container.clusters.create, container.clusters.delete, container.clusters.get, container.clusters.list, container.clusters.update, container.nodes.list"
  "googlecloud-plugin/mcp-servers": "google-gke"
---

# GKE — Google Kubernetes Engine

Run Kubernetes workloads with Google's managed control plane. Choose Autopilot (fully managed nodes) or Standard (you manage node pools).

## Mode Selection

| | Autopilot | Standard |
|---|---|---|
| Node management | Google | You |
| Billing | Per pod resource | Per node |
| Best for | Ops-light teams, variable load | Fine-grained node control |

## Core Patterns

### Create an Autopilot cluster (recommended)

```bash
# Billable action — GKE charges per cluster + node resources
gcloud container clusters create-auto CLUSTER_NAME \
  --region REGION \
  --project PROJECT_ID
```

### Get credentials

```bash
gcloud container clusters get-credentials CLUSTER_NAME \
  --region REGION \
  --project PROJECT_ID
```

### Workload Identity (never use SA key files in pods)

```bash
# Annotate the Kubernetes SA to impersonate a GCP SA
kubectl annotate serviceaccount KSA_NAME \
  iam.gke.io/gcp-service-account=GSA_EMAIL

# Bind the GCP SA
gcloud iam service-accounts add-iam-policy-binding GSA_EMAIL \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:PROJECT_ID.svc.id.goog[NAMESPACE/KSA_NAME]"
```

## Safety Rules

- Always use Workload Identity — never mount SA key files into pods
- Enable Binary Authorization for production clusters
- Cost warning: GKE clusters incur cluster management fee + node costs

## References

- [GKE Overview](https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview)
- [GKE Autopilot](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview)
- [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)
- [GKE Security Overview](https://cloud.google.com/kubernetes-engine/docs/concepts/security-overview)
- [GKE Best Practices Index](https://cloud.google.com/kubernetes-engine/docs/best-practices)
- [GKE IAM](https://cloud.google.com/kubernetes-engine/docs/how-to/iam)
- [GKE Release Notes](https://cloud.google.com/kubernetes-engine/docs/release-notes)
