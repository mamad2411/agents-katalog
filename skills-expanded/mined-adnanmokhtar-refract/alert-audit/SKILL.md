---
name: alert-audit
description: "Alert behaviour from fire history: dead, noisy, flapping, orphaned and cause-paging alerts; NO-DATA without a backend."
kind: skill
pack: observability
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: alert-audit

## Premise

Alert fatigue and silent alerts are both behaviour: a rule that has not fired in 90 days, a page that fires forty times a week and resolves in under a minute, a page whose owner left, a CPU page that never once matched an incident. None of that is in the rule file. It is in the alerting backend's history and the paging service's incident record, and an agent running beside the code usually cannot reach either. That case has a first-class verdict, `NO-DATA(<source>)`: an estimate is the fabrication this skill exists to prevent (precedents/observability.md § 36).

**This skill is the behavioural, L-tier half of alert quality.** Everything decidable from files — a missing `for`, a page without a runbook, a selector no inventory resolves, a rule file no glob loads, `$value` in labels, a window under the scrape interval, a label set the route tree sends to a null receiver — is `alert-rule-lint`'s (this pack), proved by promtool, pint, amtool or `rule-inventory.py`. This skill **consumes those rows and never re-greps a rule file**. It answers what only history can: did this alert fire, how often, for how long, who acted, and did it matter.

**Every verdict cites the alert name + its rule `file:line` (from the `alert-rule-lint` row) + the history query or export that was read + what came back.** An empty Evidence cell is a fabricated verdict. Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/observability.md`](../../../../snippets/precedents/observability.md); the live oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability (*Live series*, V204).

## Inputs

1. **`alert-rule-lint` rows for the same tree, run today** — the per-rule inventory (name, `file:line`, tier, labels, grounding, problems). Under `/obs-audit` they are already in the run; standalone, run `alert-rule-lint` first. Without them this skill halts: it has no rule list it may trust.
2. **Alert history (L):** the Prometheus `ALERTS` / `ALERTS_FOR_STATE` series over the window, through the HTTP API at a URL the user gave; Grafana alert state history; the Datadog / New Relic monitor event stream. The TSDB retention must cover the window (`--storage.tsdb.retention.time`, a long-term store) or the row is `NO-DATA(history shorter than window)`.
3. **Paging history (L):** a PagerDuty / Opsgenie / Grafana OnCall incident export or API — fire episodes, acknowledgements, responders, incident linkage.
4. **Ownership:** the `team` / `owner` label from the lint row, the route it reaches (lint §8 matrix), the on-call schedule or `CODEOWNERS` for the rule file.
5. **SLOs:** `ai/runtime/slos.md` (written by `slo-audit`) and `slo-rule-scan` rows for burn-rule coverage.

Window default: 90 days for dead, 7 and 30 days for noise. Print the window and each source's reachability in the header.

## Checks

| § | Verdict | Needs | Default severity |
|---|---|---|---|
| 1 | **DEAD** — loaded and grounded, never fired in the window | alert history | M; H when the rule guards a critical SLO and the series it reads is empty |
| 2 | **NOISY** — fires above the page budget; **flapping** — fires and resolves faster than anyone can act | alert + paging history | M |
| 3 | **ORPHAN** — no owner, or an owner no longer on the rotation | paging history, schedule | L–M |
| 4 | **CAUSE-AS-PAGE** — a cause page (lint §7 SY-01) that history shows never matched an incident | paging history, incident linkage | M |
| 5 | **BURN GAP** — an SLO whose burn set is not an accepted set in `THR-OBS-BURN`, or whose slow tier never fired before the budget ran out | `slo-rule-scan` rows; alert history | M; H for an SLO with no burn alert at all |

### 1. Dead alerts

Start from the lint row, never from the rule file. A rule the lint already flagged is **not** a behaviour finding:
- `AL-22` (never loaded) — the rule cannot fire; credit `alert-rule-lint` §4.
- `AL-10` (selector in no inventory) — run the live check it names (`count(<selector>)` at the given URL). Empty → the rule is dead *because the query is broken*: credit lint §4 and promote it from Unconfirmed with this evidence. Non-empty → continue below.
- `AL-12`, `AL-16`, `AL-21` — a rule that cannot fire on this server version; credit lint §5–§6.

For the rest: zero firing samples of `ALERTS{alertname="<name>", alertstate="firing"}` over the window means one of three things, and the verdict names which:
- **Threshold never approached** — the query returns data, and its maximum over the window (the expression without its comparison, as a `max_over_time` subquery) stays far from the threshold. Possibly a deliberate last-line safety net: confirm intent with the owner before proposing removal.
- **Condition obsolete** — the code path or dependency it watches is gone (cite the commit).
- **Cannot tell** — history unreachable or shorter than the window: `NO-DATA(<source>)`, never "probably fine".

Never propose deleting an alert that another alert's runbook, a dashboard link or an incident record references.

### 2. Noisy and flapping alerts

Count **fire episodes**, not samples: from the paging export (incidents per alert), or from Alertmanager's notification log. The `ALERTS` series gives firing time, not episodes. Judge against `THR-OBS-PAGE-BUDGET` (`pages_per_shift ≤ shift_hours / followup_hours_per_page`, defaults 12 h / 6 h — about two pages per shift): a page that alone breaks the budget is NOISY. **Flapping:** median firing duration shorter than the rule's `for` plus one evaluation interval, or resolved before anyone acknowledged. The fix is in the rule (`for`, a longer window, an aggregate instead of per-instance — lint §1, §7) or in the system: a flapping alert may be a real intermittent fault, so read the median duration and the downstream impact before prescribing a `for`. Low-traffic services paging on single errors are a design question (precedents § 15).

### 3. Orphaned alerts

The owner comes from the rule's `team` / `owner` label and the receiver it routes to (lint §8 matrix), never from a guess. ORPHAN when there is no owner label and the route is a catch-all, or the owning team or person is not on the current schedule, or no current member acknowledged its last N pages. The static half (no owner label, a route to `null`) is lint's; this check needs the paging service or the schedule, else `NO-DATA(on-call schedule)`.

### 4. Cause pages, judged by history

Lint §7 flags a page whose expression reads only resource metrics. This check asks what history says: of its N fires in the window, how many were linked to an incident, and how many preceded user impact? A cause page that is definite and imminent — `predict_linear` disk-full within hours, certificate expiry before the next business day, quorum loss — is correct (precedents § 4); CPU over 80 % is never that. A cause signal kept on a dashboard or as a ticket is not a finding.

### 5. Burn-rate coverage

The arithmetic is `slo-rule-scan`'s (§2, `burn-check.py`): a factor is right when `factor = budget_fraction × period / long_window` holds for the declared objective and period, and the short window is `long/12` (`THR-OBS-BURN`). Never judge a literal — Pyrra's 14 / 7 / 2 / 1 on 28d-scaled windows and the Workbook's fourth 3× 24h/2h ticket tier (sloth `google-30d`) are accepted sets (precedents § 12). Per SLO in `ai/runtime/slos.md`, read its `slo-rule-scan` row and record:
- **No burn alert at all** — BURN GAP, H.
- **Page tiers only** — no slow (1×, 3d/6h) ticket: a leak burning at exactly 1× trips neither page tier by construction, so the service has no detector for "we will miss the SLO this period". BURN GAP, M. This is usually the highest-value row here.
- **Behaviour:** did a fast-burn page fire during the last incident that spent budget? Did the slow ticket fire before the budget was exhausted? History, or `NO-DATA(<source>)`.

Without the `slo-rule-scan` row, apply `THR-OBS-BURN` to the burn rules `alert-rule-lint` listed and tag the row `burn arithmetic not verified (slo-rule-scan not run)`.

## Output

```
alert-audit — window 90d (dead) / 7d, 30d (noise) · alert-rule-lint rows: 35 alerts, run 2026-10-10
Alert history: UNREACHABLE (no Prometheus URL given) · Paging history: pagerduty export 2026-07-01..2026-09-30 (pasted)

| Alert | file:line | Verdict | Evidence (query or export → observed) |
|---|---|---|---|
| CheckoutLatency | rules/api.yml:132 | LINT(alert-rule-lint §4 AL-10) | selector in no inventory; live count() not run → stays HIGH Unconfirmed there |
| LegacyImportStalled | rules-extra/legacy.yml:5 | LINT(alert-rule-lint §4 AL-22) | file matched by no rule_files glob — cannot fire |
| NodeCpuHigh | rules/api.yml:142 | CAUSE-AS-PAGE | pagerduty export → 31 incidents/90d, 0 linked to a customer incident, median ack 4m |
| DiskAlmostFull | rules/api.yml:112 | NOISY | pagerduty export → 19 pages/30d on platform; budget 2/shift exceeded on 6 shifts |
| ApiHighErrorRate | rules/api.yml:5 | NO-DATA(alert history) | needs ALERTS over 90d; no Prometheus URL |
| OrdersFailing | rules/api.yml:46 | NO-DATA(alert history) | lint §1 AL-01 open; firing history needed for NOISY |

SLO burn coverage (slo-rule-scan rows, THR-OBS-BURN):
  checkout.success  workbook-3 (14.4 1h/5m, 6 6h/30m page · 1 3d/6h ticket) — covered; behaviour NO-DATA(alert history)
  search.success    workbook-4 (adds 3 24h/2h ticket) — covered
  api.availability  pyrra 14/7/2/1 on 28d — covered; lint §8: severity=critical routes to dev-null (AM-01), so the pages reach no one

Audit status: INCOMPLETE — unmeasured: ApiHighErrorRate, OrdersFailing (+26 rules) — re-run with a Prometheus URL
or paste a 90d ALERTS export.
```

Per-row verdict — exactly one, no synonyms:
- **DEAD / NOISY / ORPHAN / CAUSE-AS-PAGE / BURN GAP** — the check ran on a reachable source and the evidence supports it.
- **LINT(alert-rule-lint §N <code>)** — a decidable defect owned by the lint; credited there, never graded twice.
- **NO-DATA(<source>)** — the history this check needs was unreachable or shorter than the window. It is UNVERIFIED, never a pass, and it makes the run `INCOMPLETE`.

### Closure gate

- **`COMPLETE`** — every alert was checked against a reachable source and every row carries evidence.
- **`INCOMPLETE — unmeasured: <list>`** — the moment any row is `NO-DATA`. Name each alert, what was unreachable, and the one command or export that would close it.

Under `/obs-audit` this skill is the *Alert behaviour* row. At `NO-DATA` that row alone does not force GO-UNVERIFIED (the verdict line prints `behaviour lane NO-DATA(<source>)`), because most repos never reach the backend; a never-fire candidate from the lint still does.

## False positives / precedents

- **A dead alert with a deliberately high threshold** (a last-line safety net) is correct — confirm intent before proposing removal.
- **"The alert has been quiet, so it works"** is the rationalization the dead check exists to reject: an empty query looks exactly like healthy (precedents § Rationalizations; § 16 — a promtool test with mocked series never proves the metric exists).
- **A `for` of hours on batch staleness** (precedents § 3) and **a definite-and-imminent cause page** (§ 4) are not findings.
- **A non-production alert on its own route** is fine unless it pages the production rotation.
- **A cause signal on a dashboard or as a ticket** is not CAUSE-AS-PAGE.
- **Burn factors that differ from 14.4 / 6 / 1** are not a gap when they match an accepted set in `THR-OBS-BURN` (§ 12).

## When to run

- Quarterly alert-hygiene review, with the backend URL or the exports in hand.
- After an incident where the right alert did not fire, or the wrong one paged.
- When on-call reports fatigue; before deleting or demoting an alert.
- On every whole-repo `/obs-audit`, after `alert-rule-lint` (behaviour row, L-tier).

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and keep the rest as Unconfirmed, Hardening or Refuted — never drop them.
- Halt without `alert-rule-lint` rows for the same tree: this skill does not read rule files itself, and a rule list built from a grep is the file-granularity mistake the lint replaced.
- A verdict with an empty Evidence cell is fabricated. No evidence → `NO-DATA(<source>)`, never an estimate, never "probably fine". An adjective where a count belongs ("fires a lot") is not a finding.
- Do not grade a decidable defect here: it is `LINT(…)`, credited to `alert-rule-lint`.
- Do not judge burn factors by a literal; cite `THR-OBS-BURN` and the `slo-rule-scan` row.
- Do not propose deleting an alert that a runbook, dashboard or incident references, or whose intent the owner has not confirmed.

## Related

- `alert-rule-lint` (this pack) — every decidable check; the rule inventory this skill reads.
- `slo-rule-scan` (this pack) — burn arithmetic and generated-rule drift; `slo-audit` (this pack) — attainment and the `ai/runtime/slos.md` registry this skill reads.
- `synthetic-monitoring` (this pack) — blackbox probe pages, held to the same owner and symptom bar.
- `@observability-reviewer` (this pack) — judges these rows; `@sre-engineer` — burn and page-budget policy; `@incident-responder` — consumes alert quality during a page.
- `/obs-audit`, `/alert-design` (this pack) — the audit that dispatches this skill; the command that designs the alerts it judges.
