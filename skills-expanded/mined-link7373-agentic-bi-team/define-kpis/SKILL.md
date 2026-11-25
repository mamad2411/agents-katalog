---
name: define-kpis
description: Define or revise the company's metrics and KPIs using industry best practices — build the metric tree (north star, drivers, inputs), write rigorous catalog definitions, set targets and scorecard thresholds, and pair gameable metrics with guardrails.
---

# Define KPIs

Owner: `metrics-steward`. Args may scope it, e.g. `/define-kpis marketing funnel` or bare for the full company set.

## Procedure

1. **Ground in the business.** Read `knowledge/business-context.md` (model, priorities, north star if set). If industry benchmarks would help set targets, run `/research-domain` for current {{INDUSTRY}} benchmarks first — don't quote stale benchmark numbers from memory without checking.

2. **Select the framework for the business model.** SaaS → ARR/NRR/churn/CAC/LTV/activation; e-commerce → conversion/AOV/repeat rate/margin; marketplace → GMV/take rate/liquidity/two-sided retention; media → engagement/retention curves/ARPU; adapt for anything else. Within the framework, choose the *vital few*: 1 north star, 3–6 driver KPIs, supporting input metrics. Resist metric sprawl — every KPI must have a plausible owner and action.

3. **Stress-test each candidate KPI:**
   - Actionable? (someone can move it)
   - Gameable? (then pair it with a counter-metric, mandatory)
   - Computable honestly from available data? (check `knowledge/data-sources.md`; if not, define the honest proxy and note the gap)
   - Leading or lagging? (the set needs both)
   - Ratio metrics: are numerator and denominator individually visible somewhere? (ratios hide volume collapses)

4. **Write catalog entries** in `knowledge/metrics-catalog.md`, full template per entry: name, plain-English definition, exact formula, source table/model, grain, segments where valid, owner, target, scorecard thresholds (🟢/🟡/🔴), counter-metric, limitations, version + date. Definitions must be computable by a stranger from the entry alone. Give every entry a `classification` (`public` / `internal` / `confidential` / `restricted`, as defined in `knowledge/governance-policy.md`) — who may see a number is part of its definition. Where the metric is reported for a standard population ("paying customers", "excluding internal accounts"), define that as a named segment in the entry (`segments:` plus `segment_<name>:`, with a `/*SEGMENT*/` marker in `generic_sql`) so `python scripts/run_metric.py "<metric>" --segment <name>` applies the identical filter everywhere. Confirm with `python scripts/check_metrics.py` and `python scripts/check_governance.py`.

5. **Build/refresh the metric tree** section of the catalog: north star → drivers → inputs, with one line on the causal logic of each link.

6. **Set targets and thresholds.** Base on: history (trailing distribution), trajectory needed for stated priorities, and industry benchmarks. Where the user must make a judgement call (ambition level), present 2–3 options with implications and ask.

7. **Reconcile with existing reporting.** Diff new definitions against what current dashboards/scorecards compute. Any change to an in-use definition is a breaking change: version it, quantify the restatement on the last 3 reported periods, list affected artifacts, and get user sign-off before switching.

8. **Record & propagate.** Log decisions in `knowledge/decision-log.md`. Update the scorecard KPI set. Hand affected dashboards to `dashboard-developer` and affected marts to `analytics-engineer` for alignment.

---

> Created by Colin Beck — https://www.linkedin.com/in/beckcolin/
