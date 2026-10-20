---
name: golang-blue-green
description: >
  Execute blue/green deployments for Go services: dual environments, traffic
  switch, health validation, rollback, and DB compatibility. Use for owned
  systems under change control.
---

# Golang Blue Green

## Research grounding

Runbook for **blue/green deployment** of Go services—two production environments
with atomic (or near-atomic) traffic cutover and fast rollback. Skill id:
`golang-blue-green`.

## Scope And Authorization

- **In scope:** environments you operate; authorized production changes.
- **Out of scope:** unauthorized traffic manipulation on third-party systems.
- Prefer change windows for first cutovers; automate later.
- Pair with `golang-active-passive`, `database-migration-safety`, `golang-alerting`.

## When To Use

- Zero/near-zero downtime releases for Go APIs.
- Risky releases needing instant rollback without re-build.
- Platform support for two stacks (two ASGs, two k8s Deployments + service selector, two slots).
- Focus tokens: **golang, blue, green**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Leader election HA | `golang-active-passive` |
| Canary analysis deep dive | progressive delivery skills if present |
| Schema expand/contract | `database-migration-safety` / `golang-backfill` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Element | Guidance |
| --- | --- |
| Blue | Currently live environment |
| Green | New version idle until switch |
| Switch | LB weight, DNS, k8s Service selector, gateway route |
| Health | Ready checks must include dependency pings |
| Data | Backward/forward compatible schema before switch |
| Sticky | Sessions/cache invalidation strategy |
| Rollback | Switch traffic back; keep blue warm |
| Pitfalls | Incompatible migrations; long DNS TTL; both writing incompatible schemas |

## Workflow

### 1. Confirm scope and success criteria

1. Service, environments, traffic switch mechanism, authorization.
2. Success: cutover < target minutes; error rate stable; rollback tested.
3. DB migration plan classified (expand-only pre-switch).

### 2. Inventory

1. LB/Ingress/API gateway capabilities.
2. Stateful parts (websockets, background workers)—need dual-consumer plan.
3. Config/secret differences blue vs green.

### 3. Baseline

1. Current version, metrics SLOs, error budget.
2. Snapshot configs and image digests.

### 4. Deploy green and validate

```bash
# Build attested image
CGO_ENABLED=0 go build -trimpath -o app ./cmd/app
go test ./... -count=1
govulncheck ./...
# deploy green with same capacity as blue; no traffic yet
```

```go
// Readiness should fail if cannot reach critical deps
func ready(w http.ResponseWriter, r *http.Request) {
	if err := db.PingContext(r.Context()); err != nil {
		http.Error(w, "db", http.StatusServiceUnavailable)
		return
	}
	w.WriteHeader(http.StatusOK)
}
```

1. Run smoke against green internal URL (not public).
2. Warm caches/connections if needed.
3. Pre-switch migration: expandable only; no destructive contract yet.
4. Switch traffic (weighted 100% or atomic).
5. Watch golden signals for N minutes.
6. If bad: switch back to blue immediately.
7. After soak: decommission or recycle old blue; apply contract migrations safely.

### 5. Verify with evidence

1. Synthetic transactions before/after switch.
2. Rollback drill in staging full path.
3. Version metric/`build_info` shows expected fleet.

```bash
go test ./internal/smoke/... -count=1
# curl health on green; load test staging cutover
```

### 6. Observe and harden

1. Automate switch with guards (auto-rollback on SLO burn).
2. Ensure workers not double-processing (consumer group design).
3. Document DNS TTL if used (prefer low or non-DNS switch).

### 7. Hand off

1. Runbook: cutover checklist + rollback.
2. On-call knows which color is live (label/metric).
3. Apply `code-quality-standards` to deploy scripts.

## Compatibility matrix

| Change type | Before switch |
| --- | --- |
| Additive API field | OK |
| Remove field | Wait until old blue gone |
| DB drop column | After all green + no blue |
| New required field | Expand with default first |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollback | Instant traffic flip | Rebuild old version from scratch under fire |
| Schema | Expand/contract | Breaking migration mid-switch |
| Health | Dependency-aware ready | Only process up |
| Topic fidelity | Blue/green for Go | Generic go test only |

## Output Checklist

- [ ] Switch mechanism and owners defined
- [ ] Green deployed and smoked
- [ ] Schema compatibility confirmed
- [ ] Cutover executed with metric watch
- [ ] Rollback path proven
- [ ] Post-soak cleanup done
- [ ] Runbook updated
- [ ] `code-quality-standards` applied

## Rules

- Always have rollback before cutover.
- Focus on `golang-blue-green`.
- Authorized production changes only.
- Never run incompatible dual-writers without a plan.
