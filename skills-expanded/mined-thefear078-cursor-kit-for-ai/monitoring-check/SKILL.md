---
name: monitoring-check
description: MUST USE to audit Prometheus/Grafana (or vendor) stacks — scrape targets, alert rules, cardinality, runbooks, on-call noise. Triggers on alert fatigue, missing metrics during incident, or new monitoring deploy.
---

# Monitoring Check

Monitoring proves **user-impacting symptoms** early. Audit the stack for coverage, cardinality discipline, and alert quality — pair with `observability` for traces/SLOs and logs correlation.

## When This Skill Applies

- New Prometheus/Grafana/Alertmanager deploy
- On-call complains about noise or silence
- Post-incident: "we had no alert"
- Migrating exporters or kube-prometheus-stack upgrade
- LLM/queue/worker metrics missing

## Severity Model

| Level | Signal | Gate |
|-------|--------|------|
| **M0** | No alerts on golden path; scrapes down; AM routes to /dev/null | Block prod reliance |
| **M1** | High-cardinality labels crashing TSDB; no runbook links | Fix urgently |
| **M2** | Dashboard gaps; suboptimal thresholds | Sprint |
| **M3** | Cosmetic panel tweaks | Backlog |

## Phase 0 — Stack Inventory

```bash
kubectl get servicemonitor,prometheusrule -A 2>/dev/null | head -30
curl -s http://prometheus:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'
curl -s http://prometheus:9090/api/v1/status/runtimeinfo | jq '.data'
```

Record: retention, scrape interval, external labels, remote write if any.

## Phase 1 — Scrape & Target Health

- [ ] All intended jobs **UP**; `up==0` alert exists
- [ ] Service discovery matches current pod labels (common break after rename)
- [ ] Blackbox/cron probes for external dependencies
- [ ] Exporters version-pinned; no duplicate metric names from sidecars

```promql
# Targets down
up == 0

# Scrape failures
scrape_samples_scraped == 0 and up == 1
```

## Phase 2 — Alert Rule Quality

For each firing or critical rule:

- [ ] Symptom-based (errors, latency, saturation) not cause-only (CPU>90 forever)
- [ ] `for:` duration prevents flapping
- [ ] Severity label: page vs ticket
- [ ] Annotation: `runbook_url`, `dashboard`, `summary`
- [ ] Inhibit rules: don't page on dependency cascade 50 times

```bash
promtool check rules /path/to/rules/*.yaml
amtool check-config alertmanager.yml
```

Cross-ref: `observability` for SLO burn alerts.

## Phase 3 — Cardinality & Cost

- [ ] No unbounded labels (`user_id`, `request_id` on histograms)
- [ ] Recording rules for expensive queries on dashboards
- [ ] Retention matches budget (`cost-optimize`)

```promql
# Top cardinality offenders (Prometheus 2.x)
topk(20, count by (__name__)({__name__=~".+"}))
```

## Phase 4 — Dashboards

- [ ] Golden path dashboard exists and loads <5s
- [ ] Variables for env/service
- [ ] Links to traces/logs (if OTel deployed)
- [ ] Owner team on folder

## Phase 5 — On-Call Drill

Simulate: mute one exporter, inject 5xx — verify page reaches correct rotation within SLA.

## Output Template

```markdown
## Monitoring Check: [cluster/stack]

**Verdict:** ✅ / 🔶 / ❌

### Target health
| Job | UP | Notes |

### Alert audit
| Alert | OK? | Issue | Fix |

### Cardinality / perf
| Issue | Impact | Fix |

### Dashboard gaps
- ...

### Actions
1. ...
```

## Anti-Patterns

- **Alert on CPU only** — miss DB lock incidents
- **100 rules copy-pasted** without `for:` — wake people nightly
- **Grafana without datasource versioning** — broken after upgrade
- **Monitoring monitoring missing** — TSDB full silent failure

## Cross-References

| Skill | Use when |
|-------|----------|
| `observability` | OTel + SLO layer |
| `k8s-review` | ServiceMonitor manifests |
| `incident-response` | Active outage |
| `llm-integration` | Token/latency metrics |

## Cursor Kit Templates

- `monitoring` — kube-prometheus, Grafana provisioning

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

