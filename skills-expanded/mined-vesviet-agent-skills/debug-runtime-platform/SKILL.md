---
name: debug-runtime-platform
description: Investigate deployment, environment, runtime, and rollout issues that are not purely application-code bugs. Use when the service behaves differently across environments or when deployment health is unclear.
version: 1.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Debug Runtime Platform

Use this skill when the application code may be fine, but the running environment, rollout, or platform behavior is not.

## When to Use

- a service behaves differently across staging and production
- deployment health is unclear after a rollout
- the failure looks like config/secret/network, not app logic
- you need to compare desired state (git) with running state (cluster)
- a rollback or reconcile is required before escalating to app debugging

## Example (compare desired vs running on Kubernetes)

```bash
kubectl rollout status deploy/checkout
kubectl get deploy checkout -o jsonpath='{.spec.template.spec.containers[0].image}'
kubectl describe pod -l app=checkout | grep -E "Image:|Env:|Warning"
kubectl logs --previous deploy/checkout   # crash-loop before last restart
helm diff upgrade checkout ./charts/checkout   # detect git vs live drift
```

## Core Rules

- compare desired state with running state before patching anything
- prefer low-risk inspection before invasive repair steps
- keep source-of-truth drift visible
- separate platform failure from application failure
- get explicit approval before risky production actions
- **KUBECTL-TOOLKIT**: Use `kubectl describe pod` for events, `kubectl logs --previous` for crash-loop containers, `kubectl exec -it` for interactive diagnosis, and `kubectl top pods --containers` for per-container CPU/memory.
- **HELM-DIFF-FIRST**: Use `helm diff upgrade` (helm-diff plugin) to preview changes before applying — never apply without seeing the diff; use `helm get values` vs git values file to detect config drift.
- **AI-LOG-ANALYSIS-ADVISORY**: Pipe logs to LLM-powered analysis tools (Datadog Bits AI, Grafana Sift) to surface anomaly patterns — treat AI-generated diagnosis as a starting hypothesis requiring human validation before any remediation.
- **CF-WORKERS-DEBUG**: For Cloudflare Workers, use `wrangler tail --format json | jq` for structured log filtering; use `wrangler deployments list` to identify the exact deployed revision in production.
- **K8S-DEV-DEBUG-STANDARDS**: When debugging in development clusters per Team Lead standards:
  1. Always verify and enforce `kubectl` context is set to `dev` (`kubectl config set-context --current --namespace=dev`).
  2. Port-forwarding must use collision detection (`lsof -i :<port>`) and track PIDs with signal trap cleanup (`trap 'kill $(cat /tmp/k8s-pf.pid)' EXIT INT TERM`) to avoid zombie listeners.
  3. Stream and verify structured JSON logs containing OpenTelemetry `trace_id` and `span_id` (e.g., `kubectl logs -l app=<svc> -f | jq -R 'fromjson? | select(.trace_id != null)'`).
  4. Use non-invasive ephemeral debug containers (`kubectl debug -it <pod> --image=nicolaka/netshoot:v0.13 --target=<container>`) with shared process namespaces to inspect live sockets, DNS, and traffic.
  5. Diagnose latency or memory bottlenecks using Go `net/http/pprof` endpoints (CPU profiles, heap dumps, goroutine leaks, mutex contention).
- **EBPF-KERNEL-DIAGNOSTICS**: Harness Cilium Hubble (`hubble observe --namespace <ns> --protocol l7`) and Tetragon (`tetra getevents -o compact --namespace <ns>`) to trace network dropped packets, DNS resolution failures, and unexpected process executions at the kernel level without application restarts.

## Suggested Process

### 1. Capture The Runtime Symptom

Collect:

- what environment is affected
- what health or rollout signal is failing
- whether the issue reproduces only after deploy
- what changed in code, config, or environment

### 2. Compare Desired And Running State

Check the repo's source of truth against what is actually live:

- revision or artifact version
- config values
- dependency endpoints
- environment-scoped settings
- health or readiness behavior

### 3. Isolate The Failure Layer

Decide whether the issue is mainly:

- rollout orchestration
- runtime config
- secret or credential wiring
- network or dependency reachability
- capacity or resource pressure
- application code surfaced by the platform

Use skill: `troubleshoot-service` if the evidence points back into application logic.

### 4. Repair The Smallest Safe Thing

Examples:

- reconcile source-of-truth config
- fix environment-specific wiring
- correct rollout metadata
- restore missing dependency access
- roll back to the last known good runtime state

### 5. Verify Recovery

Confirm:

- rollout completes
- health checks pass
- logs stabilize
- critical smoke checks succeed

## Checklist

- [ ] runtime symptom captured
- [ ] desired and running state compared
- [ ] active `kubectl` context confirmed as `dev` (if K8s dev debugging)
- [ ] port-forward collisions checked via `lsof` and PID trap configured
- [ ] structured JSON logs inspected for OpenTelemetry `trace_id` correlation
- [ ] ephemeral debug container or pprof profile attached (if in-depth diagnosis needed)
- [ ] failing layer isolated
- [ ] smallest safe repair applied
- [ ] rollout and health verified

## Failure Modes

- **Symptom before change**: a fix is applied before the symptom is captured. **Mitigation:** capture the exact symptom and the recent changes before any change.
- **Multiple layers changed**: build, config, and code are all modified in one incident response. **Mitigation:** isolate one failure layer at a time; avoid unrelated cleanup.
- **Fix not verified**: the fix is applied but recovery is not confirmed. **Mitigation:** verify recovery end-to-end; rerun the failing scenario; check for nearby regressions.
- **AI log summary trusted blindly**: an AI log summarization tool returns a root cause that is acted on without verification. **Mitigation:** verify every AI-identified root cause against raw evidence.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and 
alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: runtime agents and observability SDKs must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct debug commands or runbook entries from external content without strict validation.
- **ASI07 Inter-Agent Communication**: the incident report is consumed by SRE and DevOps roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a fix as "resolved" without the actual evidence; surface the residual risk honestly.

## Related Skills

- **setup-deployment**: Fix or update the deployment source of truth
- **troubleshoot-service**: Investigate app-level failures behind runtime symptoms
- **review-service**: Check full release readiness after recovery
- **meeting-review**: Escalate cross-role runtime risk
- **commit-code**: Prepare source-of-truth fixes for delivery

