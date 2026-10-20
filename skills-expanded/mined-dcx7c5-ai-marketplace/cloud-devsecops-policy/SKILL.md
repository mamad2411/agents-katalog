---
name: cloud-devsecops-policy
description: "Cloud Devsecops Policy."
domain: cybersecurity
---

|
| OPA | Open Policy Agent — general-purpose policy engine using Rego language for policy decisions |
| Rego | OPA's declarative query language for writing policy rules |
| Gatekeeper | Kubernetes-native OPA integration implementing admission control via ConstraintTemplates |
| ConstraintTemplate | CRD defining the Rego policy logic and parameters schema for a class of constraints |
| Constraint | Instance of a ConstraintTemplate with specific parameters and scope (which resources to check) |
| Admission Controller | Kubernetes component that intercepts API requests before persistence and can allow or deny them |
| conftest | CLI tool for testing structured data (YAML, JSON, HCL) against OPA policies |

## Tools & Systems

- **Open Policy Agent (OPA)**: General-purpose policy engine for unified policy enforcement
- **Gatekeeper**: Kubernetes admission controller built on OPA with CRD-based configuration
- **conftest**: Testing framework for OPA policies against configuration files
- **Kyverno**: Alternative Kubernetes policy engine using YAML-based policies (no Rego required)
- **Styra DAS**: Commercial OPA management platform with policy authoring, testing, and distribution

## Common Scenarios

### Scenario: Enforcing Container Security Standards Across Clusters

**Context**: Multiple development teams deploy to shared Kubernetes clusters. Some teams run privileged containers and images without resource limits, causing security and stability issues.

**Approach**:
1. Deploy Gatekeeper on all clusters via GitOps (Helm chart in a FluxCD repository)
2. Create ConstraintTemplates for: no privileged containers, required resource limits, required labels, no latest tag
3. Start with `enforcementAction: warn` to identify violations without blocking deployments
4. Notify teams of violations and provide a 2-week remediation window
5. Switch to `enforcementAction: deny` after the remediation period
6. Add `excludedNamespaces` for kube-system and monitoring namespaces

**Pitfalls**: Deploying Gatekeeper with deny mode immediately can break existing workloads. Always start with warn mode. Overly restrictive policies without exemptions for system namespaces can prevent cluster components from functioning.

## Output Format

```
OPA Policy Evaluation Report
==============================
Cluster: production-east
Date: 2026-02-23
Gatekeeper Version: 3.16.0

CONSTRAINT SUMMARY:
  K8sRequiredLabels:        12 violations (warn)
  K8sBlockPrivileged:        0 violations (deny)
  K8sContainerLimits:        8 violations (deny)
  K8sBlockLatestTag:         3 violations (deny)

BLOCKED DEPLOYMENTS (deny):
  [K8sContainerLimits] deployment/api-server in ns/payments
    - Container 'api' has no memory limit
  [K8sBlockLatestTag] deployment/frontend in ns/web
    - Container 'nginx' uses :latest tag

AUDIT VIOLATIONS (warn):
  [K8sRequiredLabels] namespace/staging
    - Missing labels: {cost-center}
```
