---
name: golang-board-reporting
description: >
  Build and operate board-level security metrics from Go services and platforms:
  KRIs/KPIs (MTTD/MTTR, vuln backlog, authn failures, patch lag, control coverage),
  Prometheus/OpenTelemetry aggregation, monthly board packs, and evidence trails.
  Use for owned systems, labs, or authorized executive reporting work.
---

# Golang Board Reporting

## Research grounding

Runbook for **board security metrics** emitted and aggregated by **Go** services.
Covers metric design, exporters, rollups, redaction, and board-pack assembly—not
generic Go lint. Skill id: `golang-board-reporting`.

## Scope And Authorization

- **In scope:** owned platforms, authorized internal metrics pipelines, lab demos of board packs.
- **Out of scope:** scraping competitor metrics, exfiltrating customer data for slides, unauthorized access to SIEM/finance systems.
- Prefer aggregated, non-PII figures; redact account IDs, emails, and secrets from packs.
- Production metric changes need owner + change window; pair code with `code-quality-standards`.

## When To Use

- You need a **board / exec security scorecard** fed by Go microservices or platform jobs.
- Defining KRIs (key risk indicators) and KPIs with owners, targets, and data sources.
- Wiring Prometheus / OTel / BigQuery rollups into monthly PDF/Notion/Google-Slides packs.
- Explaining security posture trends (vuln aging, MFA coverage, break-glass usage) with evidence.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| App metrics / RED / USE dashboards only | `observability-metrics-tracing` |
| Implementation quality baseline | `code-quality-standards` |
| Vulnerability scanning pipeline | `golang-codeql-ops` / `govulncheck` workflows |
| Compliance control mapping | `golang-compliance-map` |
| Incident narrative for postmortems | `recon-and-methodology` + IR runbooks |
| Secrets inventory program | `secrets-management-hygiene` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Board KRIs | Critical open CVEs age, MFA %, privileged access events, break-glass count, patch SLA breach rate |
| Go exporters | `prometheus/client_golang`, OTel metrics SDK, labeled counters/histograms (no high-cardinality user IDs) |
| Rollup | Nightly Go jobs or scheduled queries: service → domain → org; store snapshots for month-over-month |
| Evidence | Query SQL/PromQL + export timestamp + data owner; link tickets for exceptions |
| Pitfalls | Vanity metrics, unowned series, PII labels, silent scrape gaps, “100% compliant” without sampling |

### Example KRI set (security board)

| KRI | Definition | Source sketch | Target example |
| --- | --- | --- | --- |
| Crit vuln aging | % critical findings open > 30d | SCA/SAST + ticket system | < 5% |
| Authn failure rate | 5xx/invalid token spikes | Go auth middleware counters | Alert + trend |
| MFA coverage | Human accounts with MFA | IdP export job | ≥ 98% |
| Break-glass uses | Count + mean duration | PAM / `golang-break-glass` logs | Zero unreviewed |
| Patch lag | Mean days image/base behind | Registry + SBOM | ≤ SLA |

## Workflow

### 1. Confirm audience and success criteria

1. Record board cycle (monthly/quarterly), owner (CISO/platform), environments feeding data.
2. Success: stable pack with **defined KRIs**, MoM deltas, exception list with owners/expiry.
3. Agree redaction rules (no customer names, no raw IPs if policy requires).

### 2. Inventory metric sources

1. List Go services exposing `/metrics` or OTel; note missing labels (`service`, `env`, `team`).
2. Inventory external sources: vuln scanners, IdP, cloud CSPM, ticket SLAs.
3. Map each board row → one primary source + owner; mark gaps.

### 3. Baseline current board pack

1. Save last pack + underlying queries; note stale or manual spreadsheet steps.
2. Capture scrape success rate and last successful rollup time.
3. Record known lies (hard-coded 100%, missing services).

### 4. Instrument and aggregate in Go

1. Add low-cardinality metrics in middleware / workers:

```go
var (
    authnFail = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "sec_authn_failures_total",
        Help: "Authn failures by reason (coarse)",
    }, []string{"service", "reason"})
    breakGlass = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "sec_break_glass_total",
        Help: "Break-glass activations",
    }, []string{"service", "env"})
)
// Never label with user_id, email, or full path.
```

2. Nightly rollup job (Go): pull Prom remote-read / warehouse; write `board_kpis` snapshot table.
3. Keep secrets in Vault/KMS; board job uses short-lived SA tokens.

### 5. Verify with evidence

```text
# Local metrics smoke
go test ./internal/metrics/...
curl -sS localhost:8080/metrics | rg 'sec_(authn_failures|break_glass)_total'

# PromQL examples (adjust names)
# sum(increase(sec_authn_failures_total[30d])) by (service)
# sum(increase(sec_break_glass_total[30d])) by (env)

# Rollup job
go test ./cmd/board-rollup/...
go run ./cmd/board-rollup -as-of=$(date -u +%Y-%m-01) -out=./out/board-snapshot.json
```

1. Diff this month vs last; investigate >20% swings before publishing.
2. Sample 3 services: metric present in prod scrape, not only local.
3. Redact export before attaching to board deck.

### 6. Assemble pack and observe

1. Template: cover → KRI table → trends → top risks → exceptions → asks.
2. Alert on rollup job failure and scrape-target drop (missing data is a board risk).
3. Quarterly: retire unused series; re-validate label cardinality.

### 7. Hand off

1. Owners table in runbook; link catalog (`observability-metrics-tracing`, break-glass skills).
2. Schedule automatic pack generation T-5 business days before board.
3. Apply `code-quality-standards` to exporter/rollup code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Labels | `service`, `env`, `team` | `user_id`, raw URL, email |
| KRI | Owned, timed, with data lineage | “Security score 97” with no formula |
| Change | Additive metrics + dual-write | Delete series board still uses |
| Evidence | PromQL + snapshot hash | Screenshot of local Grafana only |
| Exceptions | Ticket + expiry on SLA breach | Hide aging vulns to “look green” |

## Output Checklist

- [ ] Audience, cycle, authorization for data use recorded
- [ ] KRI definitions with owners and sources documented
- [ ] Go exporters use low-cardinality labels only
- [ ] Rollup job produces versioned snapshots
- [ ] MoM verification run; anomalies explained
- [ ] Board pack redacted; no secrets/PII
- [ ] Scrape/rollup failure alerts exist
- [ ] Exceptions have owners + expiry
- [ ] `code-quality-standards` applied to shipped code
- [ ] Next board date and data freeze noted

## Rules

- Authorized internal reporting only; no unauthorized data mining.
- Prefer evidence (queries, snapshots) over narrative slides alone.
- Do not invent compliance percentages; show sampling method.
- Keep focus on `golang-board-reporting`; route deep observability or IR elsewhere.
- Never paste live tokens, customer lists, or unredacted incident details into the pack repo.
