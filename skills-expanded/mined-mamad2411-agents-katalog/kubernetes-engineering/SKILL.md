---
name: kubernetes-engineering
description: Operate Kubernetes workloads. Use when designing deployments,
  services, and cluster resources.
metadata:
  tags: kubernetes, engineering
---

# Kubernetes Engineering

## Use this skill when
- Defining Deployments, Services, Ingress, ConfigMaps
- Autoscaling, resources, and scheduling
- Debugging running pods and rollout issues

## Do not use this skill when
- Manifest generation boilerplate (use k8s-manifest-generator)
- Cluster architecture at scale (use kubernetes-architect)

## Instructions
1. Declare resources and limits; set request==limit for critical services.
2. Use liveness vs readiness probes correctly and tune initial delays.
3. Prefer managed controllers; avoid bare pods.
4. Handle configuration via ConfigMaps/Secrets, not baked images.
5. Set securityContext: non-root, drop capabilities, read-only rootfs.
6. Plan for node failure: replica counts and PodDisruptionBudget.
7. Use topologySpreadConstraints for multi-zone resilience where needed.
8. Pin image tags/digests and use Recreate or RollingUpdate intentionally.

## Checklist
- Probes tuned
- Resources set on every container
- Security context applied

## Output Format
- Workload | probes | resources | scheduling strategy | failure tolerance

## Common Mistakes
- No resource limits (noisy neighbors)
- Probes copied generically
- Mutating live state instead of YAML
