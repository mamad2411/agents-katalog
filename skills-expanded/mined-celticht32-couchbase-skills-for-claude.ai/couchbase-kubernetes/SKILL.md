---
name: couchbase-kubernetes
description: "Deploy and operate Couchbase on Kubernetes using the Couchbase Autonomous Operator (CAO). Use whenever the user asks about Couchbase Autonomous Operator, CAO, CouchbaseCluster CRD, Couchbase on Kubernetes, Couchbase on EKS, Couchbase on GKE, Couchbase on AKS, Couchbase on OpenShift, Helm chart for Couchbase, CouchbaseBucket CRD, CouchbaseUser CRD, CouchbaseBackup CRD, CouchbaseReplicationRepresentation, server groups in Kubernetes, rack awareness in Kubernetes, persistent volumes for Couchbase, Couchbase pod resources, rolling upgrades via operator, Couchbase operator RBAC, Prometheus with CAO, or 'how do I run Couchbase on Kubernetes.' Distinct from couchbase-capella (managed Capella — no Kubernetes involved) and couchbase-upgrade (server binary upgrades outside Kubernetes). Use proactively when the user has a Kubernetes or OpenShift deployment requirement."
license: MIT
---

# Couchbase on Kubernetes (Autonomous Operator)

A skill for *deploying and operating* Couchbase on Kubernetes using the Couchbase Autonomous Operator (CAO). CAO is a Level 5 Kubernetes Operator — it manages the full lifecycle of a Couchbase cluster as a set of Kubernetes custom resources.

Distinct from:
- `couchbase-capella` — fully managed Capella (no Kubernetes to manage)
- `couchbase-upgrade` — upgrading the Couchbase binary outside Kubernetes (or the planning layer for k8s upgrades)
- `couchbase-sizing` — the capacity math applies equally; this skill covers the k8s-specific mechanics

## When this skill applies

- "How do I deploy Couchbase on Kubernetes?"
- "How do I install the Couchbase Autonomous Operator?"
- "How do I configure a CouchbaseCluster resource?"
- "How do I configure rack awareness / AZ-awareness in Kubernetes?"
- "How do I size persistent volumes for Couchbase pods?"
- "How do I do a rolling upgrade via the operator?"
- "How do I configure Prometheus monitoring with CAO?"
- "How does the operator manage buckets, users, and backups?"
- "How do I use the CAO Helm chart?"

## Pick the right reference

| Question | Read |
|---|---|
| "Installing CAO — Helm chart, namespaces, RBAC, admission controller" | `references/installation.md` |
| "CouchbaseCluster CRD — node topology, services, server groups, resources, storage" | `references/cluster-crd.md` |
| "Buckets, users, backups, XDCR as Kubernetes resources" | `references/supporting-crds.md` |
| "Operations — rolling upgrades, scaling, AZ awareness, Prometheus" | `references/operations.md` |

## Three core principles

**Principle 1 — The operator reconciles, not you.**
Don't edit Couchbase directly through the UI or REST API when CAO is managing the cluster. CAO continuously reconciles the desired state (your CRDs) against the actual cluster state. Manual changes made outside the operator will be reverted on the next reconciliation cycle. All changes go through the CRD.

**Principle 2 — Persistent volumes are the most important sizing decision.**
Data, Index, and Analytics nodes need persistent volumes that survive pod restarts. Size them generously — you can expand a PV online (if your storage class supports it) but you cannot shrink it. Use storage classes with `allowVolumeExpansion: true` and `volumeBindingMode: WaitForFirstConsumer` for AZ-aware scheduling.

**Principle 3 — Server groups map to availability zones.**
Configure server groups that align with your Kubernetes node labels (topology zones, rack labels). CAO distributes pods across server groups using pod anti-affinity rules. Without server groups configured correctly, all Couchbase pods could land on nodes in the same AZ — defeating high availability.

## Quick reference: CAO Custom Resource types

| CRD | What it manages |
|---|---|
| `CouchbaseCluster` | The cluster itself — nodes, services, networking, TLS, server groups |
| `CouchbaseBucket` | Bucket lifecycle — creation, quota, type, replicas, TTL |
| `CouchbaseScope` | Scope within a bucket |
| `CouchbaseCollection` | Collection within a scope |
| `CouchbaseUser` | Local Couchbase users and their roles |
| `CouchbaseGroup` | User groups and role assignments |
| `CouchbaseRoleBinding` | Bind users to groups |
| `CouchbaseBackup` | Backup schedules and repositories |
| `CouchbaseBackupRestore` | Restore operations |
| `CouchbaseReplicationRepresentation` | XDCR remote cluster references and replications |
| `CouchbaseMemcachedBucket` | Memcached-type buckets |
| `CouchbaseEphemeralBucket` | Ephemeral (non-persistent) buckets |

## Supported Kubernetes distributions

CAO 2.9 (current) is certified for:
- AWS EKS
- Google GKE
- Azure AKS
- Red Hat OpenShift
- Rancher (SUSE)
- Vanilla upstream Kubernetes 1.27+

## Version matrix

| CAO version | Couchbase Server versions supported |
|---|---|
| 2.9 (Dec 2025) | 7.2, 7.6, 8.0 |
| 2.8 | 7.1, 7.2, 7.6 |
| 2.7 | 7.1, 7.2 |

Always match the CAO version to your Couchbase Server version. Check `docs.couchbase.com/operator` for the current support matrix.

## Related skills

- `couchbase-sizing` — node count, RAM, disk math before writing the CRD
- `couchbase-upgrade` — upgrade planning, breaking changes, version path
- `couchbase-observability` — Prometheus integration details (metrics endpoint, scrape config)
- `couchbase-security-hardening` — TLS and RBAC patterns translate directly to CRD configuration
- `couchbase-backup-restore` — backup strategy; CAO adds `CouchbaseBackup` CRD on top
