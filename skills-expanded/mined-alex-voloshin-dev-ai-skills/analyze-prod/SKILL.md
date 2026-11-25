---
name: analyze-prod
description: Use this skill when investigating a production incident, when an alert fires (latency spike, error rate, pod crashloop), when a customer-reported issue needs prod telemetry, or as the diagnosis step of an incident-response or production-bugfix flow — including when the user describes a prod symptom without asking to "analyze" — to analyze the production environment by collecting Kubernetes pod status, managed database health, logs, metrics, and networking and diagnosing issues, supporting GCP, Azure, and AWS via the `cloud-platforms` skill and applying the SRE or DevOps role.
context: fork
argument-hint: "service name, symptom, or incident description"
allowed-tools: Read Grep Glob Bash
---

# Analyze Production Environment

Systematic production-environment analysis. Collects cluster status, pod health, database metrics, logs, and diagnoses issues. Standalone or as the entry point for production bugfixing.

**Cloud platform detection**: Read `CLAUDE.md` to identify the cloud platform, then load the matching reference module (GCP / Azure / AWS) from `@cloud-platforms`.

**⚠️ SAFETY: READ-ONLY commands only. No mutations (scale, delete, restart, deploy) without explicit user approval at Step 6.**

## 1. Clarify the Scope

Ask the user:

- **Problem / question?** (e.g., "pods crashlooping", "high latency on /api/orders", "DB connections exhausted", "general health check")
- **Affected service(s)?** (deployment name, namespace, or "all")
- **Cloud environment?** (project / subscription / account + cluster name)
- **When did it start?** (deploy, config change, traffic spike, or unknown)
- **Active incident?** (P1–P4 severity, or none)

If invoked as part of a bugfix / incident flow, extract context from the parent conversation instead.

## 2. Apply Appropriate Role

Select role by problem type:

| Problem Type | Primary Role |
|---|---|
| Pod crashes, restarts, health-check failures | `Agent(sre-engineer)` |
| High latency, error-rate spikes, SLO burn | `Agent(sre-engineer)` |
| Managed DB issues (connections, replication, CPU) | `Agent(sre-engineer)` |
| Networking, ingress, DNS, connectivity | `Agent(sre-engineer)` + `Agent(devops-engineer)` |
| Deployment failures, rollback needed | `Agent(devops-engineer)` |
| Terraform / infra drift, resource config | `Agent(devops-engineer)` |
| Application errors in logs | Stack-specific (`Agent(java-engineer)` / `Agent(python-engineer)` / `Agent(frontend-engineer)`) |
| General / unclear | `Agent(sre-engineer)` |

Announce the applied role(s). For P1/P2 incidents, always apply `Agent(sre-engineer)`.

## 3. Establish Context

### 3a. Cloud Platform Context

Detect platform from `CLAUDE.md` and verify authentication via `@cloud-platforms`:
- **GCP**: `gcloud config get-value project` + `gcloud auth list`
- **Azure**: `az account show` + `az aks list`
- **AWS**: `aws sts get-caller-identity` + `aws eks list-clusters`

Confirm the active project / subscription / account matches the user's target.

### 3b. Kubernetes Cluster

```
// turbo
kubectl config current-context
kubectl cluster-info
```

Run the platform-specific cluster list command from `@cloud-platforms` to verify cluster status.

**Record**: Cluster name, location, version, node count, current kubectl context.

## 4. Collect Production Snapshot

Run the following **read-only** diagnostics. Present results as a structured summary.

### 4a. Node Health

```
// turbo
kubectl get nodes -o wide
kubectl top nodes
```

**Flag**: `NotReady` nodes, CPU/memory >80%, version skew.

### 4b. Pod Status

For the affected namespace (or all namespaces if unspecified):

```
// turbo
kubectl get pods -n <namespace> -o wide --sort-by='.status.startTime'
kubectl get pods -n <namespace> --field-selector=status.phase!=Running
```

**Flag**: `CrashLoopBackOff` / `Error` / `Pending` / `ImagePullBackOff`, restart count >3 in last hour, replica count mismatch (`kubectl get deployments`).

### 4c. Pod Details (for problematic pods)

```
kubectl describe pod <pod-name> -n <namespace>
kubectl logs --tail=200 --timestamps <pod-name> -n <namespace>
kubectl logs --previous --tail=50 <pod-name> -n <namespace>
```

**Look for**: OOMKilled (exit 137), app exceptions, connection errors, startup failures, readiness probe failures.

### 4d. Resource Usage

```
// turbo
kubectl top pods -n <namespace> --sort-by=memory
kubectl get hpa -n <namespace>
```

**Flag**: Pods near memory limits, HPA at max replicas, CPU throttling.

### 4e. Managed Database Health

DB diagnostic commands per cloud — see `@cloud-platforms`. **Key metrics**: CPU / memory / disk utilization, active vs max connections, replication lag (HA / read replicas), failed connection count.

### 4f. Networking and Ingress

```
// turbo
kubectl get ingress -n <namespace>
kubectl get svc -n <namespace>
kubectl get endpoints -n <namespace>
```

**Flag**: Services with 0 endpoints (no healthy backends), Ingress with no address, port mismatches.

### 4g. Recent Events

```
// turbo
kubectl get events -n <namespace> --sort-by='.lastTimestamp' --field-selector type!=Normal
```

**Record**: Warning / Error events — especially `FailedScheduling`, `OOMKilled`, `FailedMount`, `Unhealthy`, `BackOff`.

### 4h. Observability Methodology

Observability methodology (Golden Signals / RED / USE / Distributed Tracing) — see `@observability-methods`. Pick a named method per problem class, then cross-reference SLI metrics, error-budget burn, and active alerts against that method's signals.

### 4i. Production Telemetry Surface

Telemetry stack patterns + per-vendor queries — see `@telemetry-stacks`. Identify the stack from `CLAUDE.md`, helm charts, `prometheus-operator` CRDs, or the OTel collector config, then query directly using the vendor patterns documented there.

## 5. Analyze Findings

Using the applied role's expertise:

1. **Correlate** the user's problem with collected data.
2. **Identify root cause** using the role's debugging methodology.
3. **Assess SLO impact** (when `Agent(sre-engineer)` is active): error budget consumed, burn rate.

<common_prod_issues>
- **CrashLoopBackOff**: OOM (check limits), app startup failure, missing config/secret, failed dependency (DB unreachable)
- **High latency**: DB slow queries, connection-pool exhaustion, CPU throttling (requests vs limits), upstream timeout
- **DB connection exhaustion**: too many connections from pods, app leak, pool misconfig, no pooler / proxy
- **Pods Pending**: insufficient cluster resources (autoscaler max), affinity/taint mismatch, PVC not bound
- **5xx errors**: app exception, upstream timeout, readiness probe failing, resource exhaustion
- **Deployment stuck**: image pull error, readiness probe failure, PDB blocking rollout, insufficient quota
- **Network unreachable**: NetworkPolicy block, service selector mismatch, DNS failure, VPC / firewall rule
</common_prod_issues>

## 6. Present Diagnosis

Structure the diagnosis:

```
## Production Environment Summary
- Cloud: [GCP/Azure/AWS] | Project/Sub/Account: [id] | Cluster: [name] ([location])
- Nodes: [count] ([healthy]/[total]) | K8s: [version] | Managed DB: [instance] ([state], [tier])

## SLO Impact (if applicable)
- SLO: [target] | Current: [actual] | Error budget: [remaining]% | Burn rate: [Nx] | Time to exhaustion: [duration]

## Findings
### [Issue 1: title]
- **Symptom / Evidence / Root cause / Severity (P1–P4) / Blast radius**

## Recommendations
1. [Immediate mitigation] — [command] ⚠️ REQUIRES APPROVAL
2. [Root cause fix] — [change description]
3. [Prevention] — [long-term improvement]

## Environment Health: [HEALTHY | DEGRADED | OUTAGE]
```

## 7. Fix or Escalate

**⚠️ All production mutations require explicit user approval.**

- **Immediate mitigation** (rollback, restart, scale): present the exact command, wait for approval, execute, verify.
- **Application code fix**: transition to a stack-specific role. Fix, test locally (optionally `/analyze-local`), deploy via normal CI/CD.
- **Infrastructure fix** (Terraform, Helm, K8s config): apply via PR with `Agent(devops-engineer)` — never direct apply.
- **Root cause unclear**: propose additional diagnostics (increased log verbosity, tracing, profiling, query analysis).

After any fix, re-run relevant Step 4 commands to verify resolution.

## 8. Summary

- **Problem**: original report / incident ID
- **Severity**: P1–P4
- **Role(s) applied**
- **Root cause**
- **SLO impact**: error budget consumed
- **Fix applied** (or "investigation only — no fix applied")
- **Verification**: confirmation the issue is resolved
- **Action items**: postmortem (if P1/P2), prevention, monitoring improvements

## Integration

- **Called by**: `/bugfix` (production environment diagnostics)
- **Roles**: `Agent(sre-engineer)`, `Agent(devops-engineer)`
- **Skills**: `@cloud-platforms` (platform-specific CLI commands, managed service diagnostics), `@observability-methods` (Golden Signals / RED / USE / Tracing), `@telemetry-stacks` (Prometheus / Datadog / Honeycomb / New Relic / Sentry / OTel queries)
