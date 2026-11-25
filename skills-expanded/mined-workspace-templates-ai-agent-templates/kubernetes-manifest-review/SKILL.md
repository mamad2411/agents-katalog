---
name: kubernetes-manifest-review
description: Reviews Kubernetes manifests for missing limits, probes, security context and unsafe rollout settings, and returns fixes ranked by risk.
---

# Kubernetes manifest review

Review the manifests as if you will be paged when they fail.

## Steps

1. Find all manifests, Kustomize overlays and rendered Helm output (`helm template`). Review the rendered result, not the template.
2. For every workload (Deployment, StatefulSet, DaemonSet, Job, CronJob) check:
   - **Resources**: `requests` and `limits` for memory and CPU. Memory limit should be set; a CPU limit is optional but requests are not.
   - **Probes**: a `readinessProbe` that exercises the app, a `livenessProbe` that does not depend on downstream services, and a `startupProbe` for slow starts.
   - **Security context**: `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `capabilities.drop: [ALL]`, no `privileged`.
   - **Rollout**: `maxUnavailable`, `maxSurge`, `minReadySeconds`, and a PodDisruptionBudget for anything with two or more replicas.
   - **Availability**: replicas of at least 2 for serving workloads, plus topology spread or anti-affinity.
   - **Images**: no `latest` tag, a digest or exact version, and `imagePullPolicy` that matches.
   - **Config**: secrets from `secretKeyRef`, never inline values.
3. Validate with `kubectl apply --dry-run=server` or `kubeconform` when available.

## Rules

- Do not apply anything to a cluster.
- Only flag what you can point to by resource and field.

## Report

Findings grouped as blocker, should fix, consider. For each: resource, field, why it matters, and the YAML fix.
