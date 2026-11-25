# Container Security

Monitor Kubernetes clusters, ECS clusters, and container workload security using Trend Micro Vision One. This skill provides visibility into container environments, their security posture, and runtime protection status.

## Instructions

1. When the user asks about container security, Kubernetes, ECS, or containerized workloads, use this skill to query container infrastructure.

2. **List Kubernetes clusters**: Start with `list_kubernetes_clusters` to get an overview of all monitored K8s environments.

3. **Check ECS clusters**: Use `list_ecs_clusters` to review AWS ECS container infrastructure.

4. **Get cluster details**: Use cluster-specific detail tools to retrieve comprehensive security and configuration information.

5. **Review namespaces**: For Kubernetes, examine namespaces to understand workload organization and security policies.

6. **Assess runtime protection**: Verify that container runtime security features are enabled and functioning.

7. **Correlate with vulnerabilities**: Cross-reference container findings with CVE data for image vulnerabilities.

## Tools

This skill uses the following Vision One MCP tools (all read-only):

### Kubernetes Clusters
| Tool | Purpose |
|------|---------|
| `container_security_k8_clusters_list` | List monitored Kubernetes clusters |
| `container_security_k8_cluster_get` | Get detailed K8s cluster information |
| `container_security_k8_images_list` | List Kubernetes images running across clusters |

### AWS ECS Clusters
| Tool | Purpose |
|------|---------|
| `container_security_ecs_clusters_list` | List monitored AWS ECS clusters |

### Container Vulnerabilities
| Tool | Purpose |
|------|---------|
| `container_security_image_vulnerabilities_list` | List container image vulnerabilities detected in K8s and ECS |

## Common Workflows

### Container Environment Inventory
1. List all Kubernetes clusters
2. List all ECS clusters
3. For each cluster, get detailed configuration
4. Summarize protection coverage across environments
5. Identify any unprotected container workloads

### Kubernetes Security Assessment
1. List Kubernetes clusters
2. Get cluster details for each
3. List namespaces and workloads
4. Check runtime protection status
5. Identify security policy gaps

### ECS Security Review
1. List ECS clusters
2. Get cluster details
3. Review task definitions and services
4. Verify container insights and protection
5. Document findings and recommendations

### Container Compliance Check
1. Inventory all container clusters
2. Verify protection agent deployment
3. Check security policy configurations
4. Identify non-compliant workloads
5. Generate compliance report

### Container Image Vulnerability Assessment
1. List container image vulnerabilities across all clusters
2. Filter by risk level (high/medium/low)
3. Identify most vulnerable images
4. List affected clusters and workloads
5. Prioritize patching by exposure and severity

### Container Image Inventory
1. List all Kubernetes images running in clusters
2. Identify image sources (registries)
3. Check image digests for integrity
4. Correlate with vulnerability data
5. Document image usage across namespaces

## Output Format

### Container Environment Summary
```
## Container Security Overview

### Kubernetes Clusters
| Cluster | Provider | Nodes | Namespaces | Protection |
|---------|----------|-------|------------|------------|
| [Name] | [EKS/AKS/GKE/On-prem] | [count] | [count] | [Enabled/Partial/Disabled] |

### ECS Clusters
| Cluster | Region | Services | Tasks | Protection |
|---------|--------|----------|-------|------------|
| [Name] | [Region] | [count] | [count] | [Enabled/Disabled] |

### Protection Summary
- Total clusters: [count]
- Fully protected: [count]
- Partially protected: [count]
- Unprotected: [count]
```

### Kubernetes Cluster Details
```
## Kubernetes Cluster: [Name]

**Provider**: [EKS/AKS/GKE/On-prem]
**Version**: [K8s version]
**Nodes**: [count]

### Protection Status
- Runtime protection: [Enabled/Disabled]
- Admission control: [Enabled/Disabled]
- Image scanning: [Enabled/Disabled]

### Namespaces
| Namespace | Pods | Protection Status |
|-----------|------|-------------------|
| [Name] | [count] | [Protected/Unprotected] |

### Security Findings
- Critical: [count]
- High: [count]
- Medium: [count]
- Low: [count]
```

### ECS Cluster Details
```
## ECS Cluster: [Name]

**Region**: [AWS Region]
**Status**: [Active/Inactive]

### Services
| Service | Tasks | Status |
|---------|-------|--------|
| [Name] | [count] | [Active/Draining] |

### Protection Status
- Container protection: [Enabled/Disabled]
- Image scanning: [Enabled/Disabled]

### Resource Utilization
- CPU reservation: [%]
- Memory reservation: [%]
```

## Security Considerations

- This skill provides read-only access to container security data
- Cluster names, namespaces, and configurations are sensitive infrastructure details
- Container vulnerabilities may expose critical application components
- Unprotected containers represent significant security risk
- Coordinate with platform teams for protection deployment
- Runtime protection gaps should be addressed urgently for production workloads
