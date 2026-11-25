---
name: kubernetes-patterns
description: Pod design patterns, sidecar containers, init containers, config management, rolling updates, and resource limits for reliable Kubernetes workloads. Grok-native with Production Contract.
when-to-use: When building or reviewing containerized services on K8s (EKS/GKE/AKS or self-managed), especially in swarms with platform or backend tracks.
---

# Kubernetes Patterns Skill

Battle-tested, production-grade patterns for running workloads on Kubernetes without the 3am surprises.

## When to Use
- Designing Deployments, StatefulSets, Jobs, CronJobs.
- Platform or application teams adopting K8s.
- Before any significant container platform work in a swarm.

## Core Patterns

### 1. Pod Design & Probes
- Always liveness + readiness + startup probes with sensible timing.
- Graceful shutdown: preStop hook + SIGTERM handling + drain.
- Resource requests/limits on every container (no "unbounded").

### 2. Sidecar & Init Containers
- Sidecar for logging, metrics, proxy (Envoy/Istio), secrets (vault-agent).
- Init containers for DB migrations, config generation, wait-for-dependencies.

### 3. Config & Secrets
- ConfigMap + Secret mounted as volume or env.
- Never put secrets in image or env in plain text in Git.
- Use External Secrets Operator or Sealed Secrets for GitOps.

### 4. Rolling Updates & Resilience
- RollingUpdate strategy with maxSurge/maxUnavailable.
- PodDisruptionBudget for user-facing workloads.
- Topology spread constraints + anti-affinity for high availability.

### 5. Observability & Cost
- Prometheus + Grafana + OpenTelemetry from day one.
- Vertical + Horizontal Pod Autoscaler together.
- Resource quotas + limit ranges per namespace.

## Integration with Grok System
- Pair with kubernetes-expert agent.
- on_infra_change hook for major manifest or policy changes.
- Record friction when a pattern caused outage or cost spike.
- Pre-flight: "Have we defined probes, PDB, resource limits, and observability?"

## Production Contract
- Pre-Flight: audit existing manifests, utilization, incidents.
- Ledger for multi-phase platform work.
- Handoff includes exact resource model, scaling behavior, and rollback plan.
- Friction + compound for every "we forgot the PDB again".

These patterns exist because people died (figuratively) learning them the hard way. Use the contract.