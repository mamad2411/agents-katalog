---
name: data-quality-auditor
description: >
  Audit data quality across pipelines, warehouses, and operational stores. Use
  when designing a DQ program from scratch, defining DQ dimensions (completeness,
  accuracy, consistency, timeliness, validity, uniqueness) for a dataset,
  building rule-based checks (Great Expectations / dbt tests / Soda / custom),
  detecting schema drift, monitoring freshness SLAs, responding to a DQ incident,
  or auditing an existing pipeline for missing DQ coverage. Complements our
  `senior-data-engineer` skill (which covers pipeline design / ETL / Spark) by
  going deep on audit-grade quality, not throughput.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  author: borghei
  category: engineering
  domain: engineering
  updated: 2026-05-27
  tags: [data-quality, dq, freshness, schema-drift, great-expectations, dbt-tests, soda, data-observability, data-engineering]
---

# Data Quality Auditor

End-to-end data quality (DQ) practice: define DQ dimensions, write rule-based checks, detect schema drift, monitor freshness SLAs, respond to DQ incidents, build a maturity-graded program. Tool-agnostic — works whether you use Great Expectations, dbt tests, Soda Core, Monte Carlo, custom SQL, or hand-rolled scripts.

This skill is audit-focused, not pipeline-focused. For pipeline design, ETL, Spark/dbt, see `engineering/senior-data-engineer`.

---

## When to use this skill

| Situation | Skill applies |
|-----------|---------------|
| Setting up DQ from scratch on a new pipeline | Yes — start with **DQ dimensions** + **check catalog** |
| Auditing existing pipelines for missing DQ | Yes — `scripts/dq_check_runner.py` against datasets |
| Detecting schema drift in upstream sources | Yes — `scripts/schema_drift_detector.py` |
| Monitoring freshness / SLA on data assets | Yes — `scripts/freshness_monitor.py` |
| Responding to a DQ incident (bad data in prod) | Yes — use **incident response playbook** |
| Designing a DQ governance model | Yes — see **DQ maturity model** |
| Compliance evidence (data quality for SOC 2 PI1, GDPR, ISO 27001) | Yes — DQ checks produce auditable artifacts |
| Building data pipelines for the first time | Use `engineering/senior-data-engineer` first |

---

## The six DQ dimensions (and why they're not optional)

Industry-standard taxonomy. Every dataset should have at least one check per dimension when at production stage.

| Dimension | Question | Example check |
|-----------|----------|---------------|
| **Completeness** | Are required fields populated? | `users.email IS NOT NULL` — fail if > 0.1% nulls |
| **Accuracy** | Do values match reality? | Reconciliation against source-of-truth system; sample-based human review |
| **Consistency** | Do values agree across systems / time? | `users.email` in DB matches Salesforce; row count today within 5% of yesterday |
| **Timeliness / Freshness** | Is data current to expectation? | `events_table.max(event_time)` is < 1h old; pipeline runs SLA |
| **Validity** | Do values conform to format / schema / business rules? | Email regex matches; country code in ISO 3166-1; status in known enum |
| **Uniqueness** | Are entities not duplicated? | `users.user_id` is unique; no two rows with same `(user_id, day)` |

Some teams add: **Integrity** (referential — FKs resolve), **Conformity** (matches a published standard), **Reasonableness** (passes basic sanity checks beyond strict validity).

See [references/data-quality-dimensions.md](references/data-quality-dimensions.md) for per-dimension depth: how to measure, what threshold to set, what to alert on, common pitfalls per dimension.

---

## The DQ check catalog

Five categories of checks, applied per dataset:

| Category | Examples | When |
|----------|----------|------|
| **Volume** | Row count is between min/max; row count is within ±N% of yesterday | Always for batch tables |
| **Freshness** | `MAX(updated_at)` ≤ N minutes ago; pipeline ran in last N minutes | All tables with refresh SLA |
| **Schema** | Column exists; column type matches; column ordinal; column nullable matches | All tables; especially upstream-sourced |
| **Values** | NOT NULL; UNIQUE; in enum; matches regex; min/max; reference exists | Per-column based on semantic role |
| **Distribution** | Mean / median / p99 within expected band; histogram doesn't shift; cardinality stable | Tables where data shape matters (ML features, analytics dimensions) |

See [references/dq-check-catalog.md](references/dq-check-catalog.md) for the full catalog: ~50 specific check patterns with detection heuristics, tool snippets (Great Expectations / dbt / Soda / SQL), and tuning notes.

---

## DQ maturity model

Five levels. Most teams should target Level 3-4.

| Level | What | Effort |
|-------|------|--------|
| **L0 — Reactive** | "We find DQ issues when users complain." No automated checks. | None (until incidents pile up) |
| **L1 — Ad-hoc** | Some checks exist on critical tables; engineers write them as needed; no centralized framework. | Low |
| **L2 — Scheduled** | Checks run on every pipeline run; failures alert via Slack / pager. Catalog of checks lives in version control. | Medium |
| **L3 — Comprehensive** | Per-dataset SLAs; checks cover all 6 DQ dimensions; freshness + volume + schema monitoring is automatic for every table; data team owns DQ. | High |
| **L4 — Data-as-product** | DQ is part of every dataset's contract. Producers responsible for quality of what they emit. Consumers can subscribe to DQ events for upstream data. | Very high; org-wide investment |

L0 / L1 teams: read this skill, pick the most-painful 3 datasets, add L2-level checks first.
L3 teams: invest in observability tooling; consider data observability vendor or build internal.
L4 teams: think about data contracts and data mesh.

---

## DQ incident response playbook

When DQ alerts fire, treat it like a production incident.

### Severity classification

| Severity | What | Response time |
|----------|------|---------------|
| **Sev1 — Customer-facing** | Bad data is visible to customers OR feeding ML production OR driving billing | < 15 min ack, < 4h fix |
| **Sev2 — Internal critical** | Bad data is feeding executive dashboards, finance close, regulatory reporting | < 1h ack, < 24h fix |
| **Sev3 — Internal degraded** | Bad data is in analytical tables; doesn't immediately affect decisions | < 1 day ack, fix in next release |
| **Sev4 — Cosmetic / non-critical** | Edge case; doesn't affect known consumers | Backlog |

### Standard playbook

1. **Acknowledge** the alert (within ack-SLA).
2. **Quarantine** affected data — block downstream pipelines, alert consumers via channel/email.
3. **Triage** — is this a real DQ issue or false positive? Root cause: upstream change? schema drift? bug in transformation? source data corruption?
4. **Contain** — stop the bleeding. Pause the pipeline; route around the bad data; serve cached known-good data; revert to last known good state.
5. **Fix forward** — apply the fix in code + reprocess affected data.
6. **Notify** — affected downstream consumers; update status page if customer-impacting.
7. **Post-incident** — write up timeline, root cause, action items.

### Recovery patterns

- **Backfill** — re-run pipelines for the affected partition / time range
- **Quarantine pattern** — keep bad data in a `_quarantine` schema; clear when reprocessed
- **Dead-letter queue (DLQ)** — for streaming data, send unprocessable records to DLQ for manual review
- **Idempotent reprocessing** — every pipeline should be re-runnable for any date range without side effects

See [references/dq-incident-response.md](references/dq-incident-response.md) for full incident playbook including templates for incident channels, post-incident writeup, and consumer notification.

---

## End-to-end workflows

### Workflow: Add DQ to a new dataset

1. **Profile** the data — `scripts/dq_check_runner.py --profile --table mydb.mytable` runs statistics: row count, null rates per column, distinct count, min/max for numerics, histogram for categoricals.
2. **Pick check thresholds** based on the profile and product knowledge.
3. **Write the checks** (in your tool of choice — Great Expectations / dbt tests / Soda / custom SQL).
4. **Wire into pipeline** — checks run on every load. Failures fail the pipeline (with alerting), don't silently produce bad data downstream.
5. **Document the DQ contract** in the data catalog: what does this table guarantee?

### Workflow: Detect and respond to schema drift

1. **Snapshot baseline schema** — `scripts/schema_drift_detector.py --baseline mydb.mytable > baseline.json`.
2. **Schedule the detector** to run before every consumer pipeline (or hourly).
3. **On drift detection** — alert + block pipeline; investigate whether the change was intentional (upstream renamed a column) or accidental (data corruption).
4. **If intentional**: update consumer pipelines + baseline. If accidental: roll back upstream or fix.

### Workflow: Monitor freshness SLAs

1. **Define SLA per table** — e.g., `events_table` must be updated within 1 hour; `daily_revenue` within 24 hours.
2. **Wire freshness checks** — `scripts/freshness_monitor.py --table events_table --max-age-min 60`.
3. **Alert on SLA breach** — via pager/Slack.
4. **Triage** — pipeline failure? upstream delay? logic bug?

### Workflow: Audit existing pipelines

1. **Inventory** all production tables (typically from data catalog).
2. **Score per table** — for each, what % of dimensions have at least one check? `scripts/dq_check_runner.py --audit --catalog`.
3. **Prioritize** — start with customer-facing + Sev1-impact tables.
4. **Schedule remediation** — add missing checks per priority.

### Workflow: Post-incident DQ improvement

1. After a DQ incident, ask: would an automated check have caught this?
2. If yes: add it. The check becomes regression prevention.
3. Document the incident → check mapping. Over time, DQ check inventory reflects organizational pain history.

---

## Anti-patterns

- **DQ as afterthought.** Checks added "when we have time." Almost never added; bad data accumulates.
- **All-or-nothing DQ.** "If we can't have 100% coverage, why bother?" Some coverage on critical tables is enormously valuable.
- **Checks without thresholds.** "Alert on any nulls." Real data has noise; tune thresholds; alert on meaningful changes.
- **Alert fatigue.** Too many noisy alerts → real ones ignored. Tune; aggregate; route by severity.
- **No owner for the data.** "Who do I ping about bad data in `orders_aggregated`?" Every prod table needs an owner.
- **DQ tool sprawl.** dbt tests + Great Expectations + Soda + custom SQL + ad-hoc Slack rules. Pick one (or two) and standardize.
- **Reactive only.** DQ team only fixes incidents; never proactively profiles or improves. Stuck at L1.
- **Checks but no enforcement.** Checks run, fail, alert — but nothing blocks the pipeline. Bad data goes downstream anyway.
- **No DQ in CI.** Production has checks; dev/staging doesn't. Bugs make it to prod, then caught.
- **Same check on a table 50 columns wide.** "Not null on every column." Drowning in noise. Focus on semantically-required.

---

## Tooling outputs

| Script | Input | Output |
|--------|-------|--------|
| `scripts/dq_check_runner.py` | Connection config + table list + check definitions | Per-table check results: pass/fail/warning, value, threshold. Markdown + JSON. |
| `scripts/schema_drift_detector.py` | Baseline schema snapshot + current schema | Diff: added/removed/changed columns; type changes; ordinal changes; severity per change. |
| `scripts/freshness_monitor.py` | Connection config + table + freshness column + SLA | Pass/fail; current age; SLA budget; alerting-ready output. |

All scripts: stdlib only, argparse CLI, JSON or human-readable output.

**Note:** scripts read schemas from JSON inputs or simulate. For live DB queries, integrate with your DB driver of choice (psycopg / mysqlclient / google-cloud-bigquery / etc.) — out of scope for stdlib-only design.

---

## References

- [data-quality-dimensions.md](references/data-quality-dimensions.md) — the 6 dimensions in depth + measurement patterns + threshold guidance
- [dq-check-catalog.md](references/dq-check-catalog.md) — ~50 specific check patterns with tool snippets
- [dq-incident-response.md](references/dq-incident-response.md) — incident playbook + recovery patterns + writeup templates

---

## Related skills

- `engineering/senior-data-engineer` — pipeline design, ETL, dbt, Spark
- `engineering/observability-designer` — observability for data infrastructure (different from DQ but adjacent)
- `engineering/chaos-engineering` — DQ checks themselves benefit from chaos testing
- `ra-qm-team/gdpr-dsgvo-expert` — data quality is part of GDPR Art. 5(1)(d) "accuracy" principle
- `ra-qm-team/soc2-compliance-expert` — SOC 2 PI1 (Processing Integrity) requires DQ controls
