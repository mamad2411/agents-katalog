---
name: gcp-gke-autopilot-limits
description: >
  Work within GKE Autopilot constraints: disallowed pod specs, resource requests,
  system namespaces, networking/load balancer behaviors, and workload identity patterns.
  Use when designing or troubleshooting owned Autopilot clusters and avoiding Standard
  GKE assumptions that break on Autopilot.
---

# GCP GKE Autopilot Limits

## Scope And Authorization

- **In scope:** GKE Autopilot clusters and workloads you own or operate with authorization.
- **Out of scope:** modifying foreign projects’ clusters or bypassing platform security for abuse.
- Prefer staging Autopilot clusters for experiments.
- Pair manifests with `code-quality-standards` and cluster security skills as needed.

## When To Use

- Deploying to **Autopilot** vs Standard GKE.
- Pods stuck Pending due to Autopilot admission constraints.
- Choosing workload patterns (DaemonSets, privileged pods, hostPath) that Autopilot restricts.
- Rightsizing CPU/memory requests under Autopilot billing/compute model.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Binary Authorization | `gcp-binary-authorization` |
| VPC firewall rules | `gcp-firewall-rules` |
| Flux GitOps security | `flux-gitops-security` |
| General Linux node priv-esc | `linux-privilege-escalation` (lab nodes you own) |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Autopilot tendency |
| --- | --- |
| Nodes | Google-managed; no SSH node admin |
| Privileged pods | Restricted / rejected |
| hostPath / hostNetwork | Generally disallowed |
| DaemonSets | Limited vs free-form Standard |
| Resources | Requests required; defaults may be applied |
| Namespaces | System namespaces protected |
| Workload Identity | Preferred for GCP API access |

## Common rejection causes

| Spec | Issue |
| --- | --- |
| `privileged: true` | Blocked |
| `hostPath` volumes | Blocked |
| Missing requests | May fail or get unexpected defaults |
| Forbidden capabilities | Dropped/rejected |
| Node selectors for custom node pools | No custom pools like Standard |
| Some CNI/device plugins | Unsupported |

## Workflow

### 1. Confirm scope and success criteria

1. Cluster version, region, release channel, Standard vs Autopilot confirmed.
2. Success: workloads admitted; resources sane; no reliance on node SSH; WI configured for GCP APIs.
3. Document features requiring Standard instead (honest exit criteria).

### 2. Inventory cluster and failures

```bash
gcloud container clusters describe CLUSTER --region=REGION --format='value(autopilot.enabled)'
kubectl get pods -A | rg -i 'Pending|Evicted|Error'
kubectl describe pod POD -n NS | tail -n 40
```

1. Capture admission error messages (Autopilot webhook).
2. List DaemonSets and privileged workloads from Standard migration.

### 3. Adapt manifests

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      serviceAccountName: app-wi
      containers:
        - name: app
          image: REGION-docker.pkg.dev/PROJECT/REPO/app@sha256:DIGEST
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1"
              memory: "1Gi"
          securityContext:
            runAsNonRoot: true
            allowPrivilegeEscalation: false
            capabilities:
              drop: ["ALL"]
          # no hostPath, no privileged
```

1. Replace node-level agents with Autopilot-supported observability options (managed or allowed DaemonSets only).
2. Use **Workload Identity** instead of node SA keys.
3. Set explicit requests; load-test for throttling.
4. Storage: use supported CSI/preemptible patterns per docs; avoid hostPath.

### 4. Networking and services

1. Prefer GKE Gateway/Ingress patterns supported on Autopilot.
2. NetworkPolicies: confirm dataplane features on your version.
3. Private clusters: align control plane access and Cloud NAT for egress.

### 5. Verify with evidence

| Check | Expect |
| --- | --- |
| Deploy secure pod | Running |
| Privileged test pod | Rejected |
| WI to GCP API | Works without JSON key |
| Scale | New capacity without node SSH |

```bash
kubectl auth can-i list nodes  # limited vs Standard expectations
```

### 6. Observe and harden

1. Monitor pending pods and admission failures.
2. Budget alerts for Autopilot compute.
3. Keep cluster on supported release channel; test upgrades staging first.

### 7. Hand off

1. Constraints checklist for app teams.
2. Explicit list of workloads that need Standard GKE (if any) with justification.
3. Apply `code-quality-standards` for manifests/Helm.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Security context | non-root, no priv | privileged debug DaemonSet |
| Identity | Workload Identity | SA JSON on node |
| Resources | Explicit requests | Guess and thrash Pending |
| Nodes | Accept managed | Demand SSH for prod |
| Migration | Strip hostPath early | Lift-and-shift Standard YAML |
| Evidence | Admission deny proof | “Works on my Standard cluster” |

## Output Checklist

- [ ] Autopilot cluster confirmed
- [ ] Failing admission reasons captured
- [ ] Manifests adapted (no hostPath/privileged)
- [ ] Resources requests set
- [ ] Workload Identity configured for GCP access
- [ ] Networking/Ingress approach validated
- [ ] Unsupported workloads escalated to Standard with rationale
- [ ] Monitoring for Pending/admission errors
- [ ] `code-quality-standards` applied

## Rules

- Owned clusters only.
- Do not weaken Autopilot controls to reintroduce node breakout risks.
- Prefer platform-supported patterns over hacks.
- When Autopilot cannot meet requirements, document Standard exception with security review—not silent privilege.
