---
name: kubernetes-skills
description: Kubernetes orchestration patterns, deployments, and best practices
category: stacks/infrastructure/kubernetes
applies_to: kubernetes
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# Kubernetes Skills

Container orchestration platform for automating deployment and scaling.

## Sub-Skills

### Workloads
- [deployments.md](workloads/deployments.md) - Deployment patterns
- [statefulsets.md](workloads/statefulsets.md) - StatefulSet patterns
- [daemonsets.md](workloads/daemonsets.md) - DaemonSet patterns
- [jobs.md](workloads/jobs.md) - Job and CronJob

### Networking
- [services.md](networking/services.md) - Service types
- [ingress.md](networking/ingress.md) - Ingress patterns
- [network-policies.md](networking/network-policies.md) - Network policies

### Configuration
- [configmaps.md](configuration/configmaps.md) - ConfigMap patterns
- [secrets.md](configuration/secrets.md) - Secret management
- [environment.md](configuration/environment.md) - Env variables

### Storage
- [pv-pvc.md](storage/pv-pvc.md) - Persistent volumes
- [storage-classes.md](storage/storage-classes.md) - Storage classes
- [volume-snapshots.md](storage/volume-snapshots.md) - Volume snapshots

### Security
- [rbac.md](security/rbac.md) - RBAC patterns
- [pod-security.md](security/pod-security.md) - Pod security
- [service-accounts.md](security/service-accounts.md) - Service accounts
- [network-policies.md](security/network-policies.md) - Network policies

### Scaling
- [hpa.md](scaling/hpa.md) - Horizontal Pod Autoscaler
- [vpa.md](scaling/vpa.md) - Vertical Pod Autoscaler
- [cluster-autoscaler.md](scaling/cluster-autoscaler.md) - Cluster autoscaling

### Observability
- [logging.md](observability/logging.md) - Logging patterns
- [monitoring.md](observability/monitoring.md) - Prometheus/Grafana
- [tracing.md](observability/tracing.md) - Distributed tracing

### Helm
- [charts.md](helm/charts.md) - Chart development
- [values.md](helm/values.md) - Values patterns
- [hooks.md](helm/hooks.md) - Helm hooks

## Detection
Auto-detected when project contains:
- `*.yaml` or `*.yml` with `apiVersion:`
- `kind: Deployment` or `kind: Service` patterns
