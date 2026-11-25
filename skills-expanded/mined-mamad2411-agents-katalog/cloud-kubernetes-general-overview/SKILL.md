---
name: cloud-kubernetes-general-overview
description: "Cloud Kubernetes General Overview."
domain: cybersecurity
---

|
| RBAC | Role-Based Access Control in Kubernetes, a method for regulating access to cluster resources based on the roles of individual users or service accounts |
| ClusterRole | Cluster-wide role definition that specifies permissions (verbs on resources) applicable across all namespaces |
| ClusterRoleBinding | Associates a ClusterRole with subjects (users, groups, service accounts) at the cluster scope |
| Service Account | Identity associated with pods for authenticating to the Kubernetes API server, automatically mounted unless disabled |
| automountServiceAccountToken | Pod spec field controlling whether the service account token is automatically mounted into the pod filesystem |
| Privilege Escalation | RBAC verbs (bind, escalate, impersonate) that allow a user to grant themselves or others elevated permissions |

## Tools & Systems

- **kubectl**: Primary CLI for querying Kubernetes RBAC resources (roles, bindings, service accounts)
- **rbac-tool**: kubectl plugin for RBAC analysis including who-can queries, visualization, and policy generation
- **KubiScan**: Python tool for scanning Kubernetes RBAC for risky permissions and privilege escalation paths
- **Kubeaudit**: Security auditing tool that checks pods and workloads for security anti-patterns including RBAC issues
- **rakkess**: kubectl plugin showing access matrix for the current user across all resource types

## Common Scenarios

### Scenario: Auditing an EKS Cluster Shared by Multiple Development Teams

**Context**: A shared EKS cluster serves four development teams. RBAC was configured during initial setup but has not been reviewed in 12 months. Teams report being able to access other teams' namespaces.

**Approach**:
1. List all ClusterRoleBindings to identify bindings granting broad access to authenticated users
2. Run `kubectl rbac-tool who-can get secrets` to find subjects that can read secrets across namespaces
3. Discover that a ClusterRoleBinding grants `edit` to `system:authenticated`, giving all users write access cluster-wide
4. Run KubiScan to identify service accounts with risky permissions and pods running with elevated service accounts
5. Replace the ClusterRoleBinding with namespace-scoped RoleBindings for each team
6. Disable automountServiceAccountToken for workloads that do not need API access
7. Create a NetworkPolicy to isolate namespace traffic between teams

**Pitfalls**: Removing ClusterRoleBindings can break CI/CD pipelines and operators that rely on cluster-wide access. Always audit which workloads use the bindings before removing them. EKS maps IAM roles to Kubernetes groups via aws-auth ConfigMap, so RBAC changes must be coordinated with IAM role mappings.

## Output Format

```
Kubernetes RBAC Audit Report
===============================
Cluster: production-eks (EKS 1.28)
Audit Date: 2026-02-23
Namespaces: 12

RBAC INVENTORY:
  ClusterRoles: 48 (18 custom, 30 system)
  ClusterRoleBindings: 32 (12 custom, 20 system)
  Roles (namespaced): 24
  RoleBindings (namespaced): 36
  Service Accounts: 67

CRITICAL FINDINGS:
[RBAC-001] ClusterRoleBinding Grants edit to system:authenticated
  Binding: authenticated-edit
  Effect: ALL authenticated users have edit access across ALL namespaces
  Risk: Any user can modify resources in any namespace
  Remediation: Replace with namespace-scoped RoleBindings per team

[RBAC-002] Custom ClusterRole with Wildcard Permissions
  ClusterRole: developer-admin
  Rules: verbs=["*"], resources=["*"], apiGroups=["*"]
  Bindings: 4 users via developer-admin-binding
  Risk: Equivalent to cluster-admin without the name
  Remediation: Scope to specific resources and verbs needed

SUMMARY:
  Principals with cluster-admin: 6 (recommended: <= 3)
  Roles with wildcard permissions: 4
  Service accounts with secret access: 12
  Pods with auto-mounted tokens: 45 / 67
  Privileged containers: 8
```
