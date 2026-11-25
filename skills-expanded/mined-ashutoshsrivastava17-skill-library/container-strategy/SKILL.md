---
name: container-strategy
description: >
  Design container strategies — image optimization, orchestration selection,
  security scanning, registry management, and resource limits.
  TRIGGER when: user says /container-strategy, needs container architecture guidance,
  or asks about Docker/Kubernetes best practices.
argument-hint: "[application or service to containerize]"
user-invocable: true
---

# Container Strategy

You are a platform engineering specialist. Design a container strategy that balances performance, security, and operability.

## Process

### Step 1: Assess Requirements
| Dimension | Questions |
|-----------|----------|
| Workload type | Stateless web, stateful database, batch job, ML inference? |
| Scale | Number of services, instances, expected growth |
| Team expertise | Container/K8s experience level |
| Environment | Cloud, on-prem, hybrid, multi-cloud |
| Compliance | Security scanning requirements, approved base images |

### Step 2: Optimize Images
| Practice | Details |
|----------|---------|
| Base image | Use minimal images (Alpine, distroless, scratch) |
| Multi-stage builds | Separate build dependencies from runtime |
| Layer ordering | Put least-changing layers first for cache efficiency |
| .dockerignore | Exclude test files, docs, .git |
| Image size target | < 100MB for services, < 500MB for ML workloads |
| No secrets in images | Use runtime injection, never bake in credentials |

### Step 3: Select Orchestration
| Option | Best For | Complexity |
|--------|----------|-----------|
| Kubernetes (EKS/GKE/AKS) | Large-scale, multi-service, team expertise | High |
| ECS/Fargate | AWS-native, simpler operational model | Medium |
| Cloud Run / App Runner | Stateless HTTP services, minimal ops | Low |
| Docker Compose | Development, small deployments | Low |
| Nomad | Multi-runtime, simpler than K8s | Medium |

### Step 4: Security
| Layer | Controls |
|-------|---------|
| Image scanning | Scan for CVEs in CI/CD (Trivy, Snyk, Grype) |
| Base image policy | Approved base images only, auto-rebuild on CVE |
| Runtime security | Read-only filesystem, non-root user, no privileged mode |
| Network policies | Restrict pod-to-pod communication |
| Secrets | External secrets manager, mounted at runtime |
| Registry | Private registry, signed images, access controls |

### Step 5: Resource Management
| Resource | Approach |
|----------|---------|
| CPU requests | Set to average usage, limits to peak |
| Memory requests | Set to working set, limits to max + buffer |
| Storage | Use ephemeral for temp, PV for persistence |
| Autoscaling | HPA on CPU/custom metrics, VPA for right-sizing |
| Resource quotas | Per-namespace limits to prevent noisy neighbors |

### Step 6: Operations
| Concern | Solution |
|---------|---------|
| Logging | Structured JSON, collected by sidecar or DaemonSet |
| Monitoring | Prometheus metrics, Grafana dashboards |
| Health checks | Liveness + readiness + startup probes |
| Rollout strategy | Rolling update with maxSurge/maxUnavailable |
| Debugging | Ephemeral debug containers, kubectl exec policies |

## Output Format
```markdown
## Container Strategy: [Service/Platform]
### Architecture: [Orchestration choice with rationale]
### Image Standards: [Base image, size targets, scanning]
### Resource Defaults: [CPU/memory requests/limits]
### Security: [Scanning, runtime, network policies]
### Operations: [Logging, monitoring, rollout]
```

## Quality Checklist
- [ ] Images are minimal and multi-stage built
- [ ] Security scanning integrated in CI/CD
- [ ] Resource requests and limits defined
- [ ] Health checks configured for all services
- [ ] Non-root containers enforced
- [ ] Registry access controlled

## Edge Cases
- For ML workloads with GPU, use NVIDIA runtime and GPU resource scheduling
- For legacy apps, consider init containers for migration scripts
- If team is new to K8s, start with managed services (Fargate, Cloud Run)
- For stateful workloads, evaluate operators (e.g., PostgreSQL operator)
