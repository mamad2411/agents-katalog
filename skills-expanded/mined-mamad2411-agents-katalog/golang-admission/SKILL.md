---
name: golang-admission
description: >
  Build and operate Kubernetes admission webhooks and policies in Go: validating
  and mutating admission, fail modes, certs, and policy tests. Use for owned clusters.
---

# Golang Admission

## Research grounding

Runbook for **Kubernetes admission control** implemented in Go (Validating /
Mutating Admission Webhooks, and related policy services). Skill id:
`golang-admission`.

## Scope And Authorization

- **In scope:** clusters you own or are authorized to change.
- **Out of scope:** breaking third-party cluster availability.
- Prefer dry-run / staging cluster; production webhook changes need change windows.
- Redact kubeconfigs and tokens from notes.
- Pair code with `code-quality-standards`.

## When To Use

- Writing a Go admission webhook (controller-runtime, kubebuilder, raw `http`).
- Enforcing image registries, resource limits, labels, or securityContext defaults.
- Debugging webhook timeouts, cert rotation, or fail-open/closed behavior.
- Focus tokens: **golang, admission**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| App-level RBAC | `golang-access-control` |
| Supply-chain attestations verify | `golang-attestations` |
| Generic K8s security program | cluster hardening / PSS skills in catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Types | Validating (allow/deny), Mutating (patch), optional Audit |
| API | `AdmissionReview` v1; respond with `allowed`, `warnings`, JSON patch |
| Frameworks | kubebuilder, controller-runtime webhook, Kyverno/Gatekeeper (policy engines) |
| HA | ≥2 replicas; PDB; watch latency budgets (usually <3s API server timeout) |
| TLS | Serving certs via cert-manager or API service CA bundle |
| Fail policy | `Fail` for security controls; `Ignore` only with strong justification |
| Side effects | Prefer none; if any, document and use dry-run safe code |
| Pitfalls | Webhook selects system namespaces and bricks cluster; infinite mutate loops |

## Workflow

### 1. Confirm scope and success criteria

1. Cluster, namespaces in scope, policy intent, authorization.
2. Success: policy enforces on test objects; system namespaces excluded; latency SLO met.
3. Rollback: delete ValidatingWebhookConfiguration or set failurePolicy carefully.

### 2. Inventory

1. Existing webhooks and policy engines; conflicting rules.
2. Objects to govern (Pod, Deployment, Ingress, CRDs).
3. Privileged namespaces (kube-system) exclusion list.

### 3. Baseline

1. Sample create/update latency before webhook.
2. Capture current noncompliant objects (report-only mode if available).
3. Version manifests and policy tests.

### 4. Implement Go webhook

```go
func (h *PodValidator) Handle(ctx context.Context, req admission.Request) admission.Response {
	pod := &corev1.Pod{}
	if err := h.decoder.Decode(req, pod); err != nil {
		return admission.Errored(http.StatusBadRequest, err)
	}
	if !allowedRegistry(pod) {
		return admission.Denied("image registry not in allowlist")
	}
	return admission.Allowed("")
}
```

1. Register path `/validate-v1-pod` with TLS; set `namespaceSelector` / `objectSelector`.
2. Exclude kube-system and webhook’s own namespace.
3. Support `DryRun` — no external side effects.
4. Mutating: generate JSON patch; ensure idempotent re-invocation.
5. Log decision with uid/name/namespace; no secrets.

### 5. Verify with evidence

```bash
go test ./internal/webhook/... -count=1
go test ./... -race -count=1
go vet ./...
staticcheck ./...

# Staging cluster
kubectl apply -f config/webhook --dry-run=server
kubectl apply -f testdata/pod-denied.yaml   # expect deny
kubectl apply -f testdata/pod-allowed.yaml  # expect allow
```

1. Chaos: kill one webhook pod → still admits (HA).
2. Timeout: inject delay → confirm failurePolicy behavior matches design.
3. Cert expiry drill documented.

### 6. Observe and harden

1. Metrics: `admission_requests_total{allowed}`, latency histogram, error rate.
2. Alert on elevated deny rate (bad rollout) and webhook 5xx.
3. Review match rules quarterly; avoid `*` on all resources without need.

### 7. Hand off

1. Runbook: disable webhook safely; cert rotation owner.
2. Policy catalog linked to ticket system.
3. Apply `code-quality-standards`.

## Config knobs

| Field | Prefer |
| --- | --- |
| failurePolicy | Fail for security; document Ignore |
| timeoutSeconds | 1–5; optimize handler |
| sideEffects | None |
| admissionReviewVersions | v1 |
| matchPolicy | Equivalent |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Explicit resources + namespace exclude | Match everything including kube-system |
| Mode | Dry-run / warn then enforce | Enforce untested on prod day 1 |
| Code | Fast, pure validate | Sync call to flaky external API in hot path |
| TLS | cert-manager rotation | Forever cert, manual copy |
| Topic fidelity | K8s admission webhooks in Go | Generic go test only |

## Output Checklist

- [ ] Cluster scope and policy intent recorded
- [ ] Conflicting webhooks inventoried
- [ ] Go webhook + tests for allow/deny cases
- [ ] namespace/object selectors safe
- [ ] failurePolicy and timeout documented
- [ ] Staging deny/allow evidence captured
- [ ] HA and cert rotation planned
- [ ] Metrics/alerts and runbook updated
- [ ] `code-quality-standards` applied

## Rules

- Authorized clusters only; never brick prod without rollback plan.
- Prefer reversible webhook installs.
- Focus on `golang-admission`; route app authz elsewhere.
- Never paste kubeconfig secrets into notes.
