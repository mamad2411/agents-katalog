---
name: observe-ready
description: "Keep a deployed app healthy once real users are on it. Refuses paper SLOs (numbers with no error-budget policy), blind dashboards (charts bound to no SLO), and paper runbooks (written once, never executed). Triggers on 'add monitoring,' 'define an SLO,' 'alerts when X,' 'add Datadog / Honeycomb / Sentry / Grafana,' 'write a runbook,' 'on-call setup,' 'post-mortem,' 'structured logging,' 'OpenTelemetry,' 'distributed tracing,' 'error budget policy,' or any request to wire operational signals for a live service. Does not pick the tool (stack-ready), deploy the app (deploy-ready), build the app (production-ready), or manage secrets (security). Pairs with deploy-ready. Full trigger list in README."
version: 3.1.0
updated: 2026-11-23
changelog: CHANGELOG.md
suite: ready-suite
tier: shipping
upstream:
  - production-ready
  - stack-ready
  - deploy-ready
  - repo-ready
downstream: []
pairs_with:
  - deploy-ready
  - launch-ready
compatible_with:
  - claude-code
  - codex
  - cursor
  - windsurf
  - antigravity
  - pi
  - openclaw
  - any-agentskills-compatible-harness
---

# Observe Ready

This skill exists to solve one specific failure mode. An app that ships to real users, has a dashboard nobody looks at, an SLO number posted on a wiki page that no alert is wired to, a runbook written once and never executed, and a pager that fires so often the on-call has muted half of it. When something finally breaks the way no monitor was written to catch, the operators open the dashboard and discover that the one chart they need either does not exist, is measuring the wrong thing, or is hosted on the same cluster that just went down. The alert that did fire has no runbook link. The runbook that is linked has a `grep` command referencing a log field renamed six months ago. The postmortem never happens because the team is already in the next incident.

The job here is the opposite. Produce an observability surface where every charted metric has a promise behind it, every alert that pages is actionable, every runbook has been executed in the last quarter, and the whole surface is reachable during the incident it describes. If a dashboard cannot answer "is the service meeting its SLO right now," it is not a dashboard; it is wall art. If an alert has no runbook, it is noise. If a runbook has not been executed, it is a guess with formatting.

This is harder than it sounds because observability is a *systems* problem layered on a systems problem. The dashboards, the metrics pipeline, the trace store, the log aggregator, the alert router, the on-call schedule, the runbook host, and the status page are each independent infrastructures. If any one of them depends on the thing it is supposed to observe, the whole surface collapses at exactly the moment you need it. Slack lost its dashboards in January 2021 ([Slack Engineering](https://slack.engineering/slacks-outage-on-january-4th-2021/)). Roblox explicitly made "remove circular dependencies in the observability stack" a remediation after its 73-hour outage ([Roblox](https://about.roblox.com/newsroom/2022/01/roblox-return-to-service-10-28-10-31-2021)). Datadog ate its own dogfood in March 2023 ([Datadog](https://www.datadoghq.com/blog/2023-03-08-multiregion-infrastructure-connectivity-issue/)). The pattern is not rare.

## Core principle: every metric is bound to a promise, or it is demoted

The load-bearing discipline is that a metric on a dashboard above the fold is a promise in disguise: it is there because somebody wants to look at it during an incident. If the metric is not bound to an SLO, a user journey, or a named diagnostic role, it is noise that crowds out the signal. observe-ready enforces:

> Every charted, alerted, or SLO-ed number is either (1) a Service Level Indicator with a documented SLO and error-budget policy, (2) a supporting diagnostic explicitly marked as non-alerting, or (3) removed.

This principle is non-negotiable. An AI-generated observability config that emits forty charts and a dozen threshold alerts without naming which one is the SLO for which user journey is a **paper SLO** on a **blind dashboard**, and the skill refuses to accept it as a deliverable. Paper canary's cousin: the artifact is present, the mechanism is absent. See `references/RESEARCH-2026-04.md` sections 5 and 8 for the citations and the naming-lane derivation.

## When this skill does NOT apply

Route elsewhere if the request is:

- **Picking the observability tool itself** ("Datadog vs. Honeycomb," "Grafana Cloud vs. New Relic," "self-host Prometheus or pay for Chronosphere"). That is `stack-ready`. observe-ready assumes the tool choice exists; it opinions on what any chosen tool must actually do in the config it lands with.
- **Deployment mechanics** ("set up the canary," "write the migration calendar," "enforce same-artifact promotion"). That is `deploy-ready`. observe-ready consumes deploy-ready's topology and healthcheck artifacts; it does not author the pipeline.
- **Building the app** ("wire the users page," "add RBAC," "build the dashboard UI"). That is `production-ready`. observe-ready reads `.production-ready/STATE.md` to know which features exist so it can name SLOs per user journey.
- **Repo hygiene** ("add CODEOWNERS," "set up branch protection," "review policy"). That is `repo-ready`.
- **Secrets and vault management** ("rotate this API token," "set up a vault"). That is security territory. observe-ready opinions on PII scrubbing in telemetry pipelines because that is an egress problem at the observability surface, not a vault problem.
- **Product analytics, funnel analysis, A/B testing, conversion tracking.** That lives in `production-ready`'s telemetry domain (`references/analytics-and-telemetry.md`). observe-ready owns operational signals, not marketing signals. Keep the line bright: if the question is "did the signup conversion go up this week," it is not observe-ready's question. If the question is "are signups failing more than the SLO allows," it is.
- **Performance tuning and cost optimization** ("reduce bundle size," "why is this Lambda slow"). observe-ready surfaces latency; it does not tune it. Route to a future scale-ready or cloud-provider docs. observe-ready does opinion on observability-cost control (retention, sampling, cardinality) because that is its own territory.
- **Security incident response playbooks** (breach, intrusion, data exfiltration). That is `production-ready`'s security deep-dive. observe-ready wires the detection hooks; security owns the playbook.
- **User-facing error pages, 404s, 500s, offline shell.** That is `production-ready`'s `error-pages-and-offline.md`. observe-ready wires the error tracking behind them.

This section is the scope fence. Every plausible trigger overlap with a sibling has a route-elsewhere line.

## Workflow

Follow this sequence. Skipping steps produces the exact class of failure this skill exists to prevent: a monitoring surface that renders but does not observe.

### Step 0. Detect observability state and mode

Read `references/observe-research.md` and run the mode detection protocol.

- **Mode A (Greenfield)**: the app has just shipped or is about to; no SLOs, no structured logging, no real dashboards. Start from zero.
- **Mode B (Instrumented-but-unbound)**: metrics, logs, traces exist in some form. No SLOs. Dashboards exist but nobody knows who owns them. This is the most common starting state.
- **Mode C (Mature-with-sprawl)**: SLOs exist. Too many dashboards, too many alerts. The ask is "make this surface usable again." Pruning is the load-bearing move.
- **Mode D (Incident-reactive)**: a recent incident exposed an observability gap. The ask is narrower: wire what was missing, then proceed to the rest.
- **Mode E (Cost-driven)**: the bill arrived. Telemetry volume is the lever; the ask is "cut 40% without losing signal." Retention, sampling, and cardinality dominate.

**Passes when:** a mode is declared, and the corresponding research output block from `observe-research.md` is produced.

### Step 1. Service and user-journey inventory

Read `references/metrics-taxonomy.md`. Catalog the services and user journeys that need operational signals.

Produce, in writing:

1. **Service list.** From `.deploy-ready/TOPOLOGY.md` if present, otherwise from the running code. Each service tagged with a topology type: request/response, worker, batch, edge, scheduled job, data pipeline.
2. **Dependency graph.** Which services call which. External dependencies named (DB, cache, queue, third-party API). This is load-bearing for SLO composition (Step 4) and the observability-surface dependency test (Step 10).
3. **User journeys.** The named flows a real user completes: "sign up," "log in," "create an order," "upload a file," "export a report." From `.production-ready/STATE.md` or from the running app. Each journey has a critical path through one or more services.
4. **Signal sources that already exist.** Every existing metric, log stream, trace backend, error tracker, and alert policy. Listed, owner named if known, last-reviewed date if known.

**Mode C shortcut:** the inventory exists; run the pruning audit on it. Anything without an owner or a last-reviewed date in the last 180 days is a prune candidate.

**Passes when:** every service is listed with a topology type; every user journey is named; every existing signal source has either an owner and a review date, or a "prune candidate" marker.

### Step 2. Structured logging baseline

Read `references/logging-patterns.md`. Log discipline is the foundation; without structured events with correlation IDs, traces and metrics cost more and reveal less.

Enforce:

- **One structured log format across services.** JSON by default. Every log line carries a `trace_id`, a `service`, a `level`, a `timestamp`, an `event` name. The shape is defined once and enforced by the logger, not by human discipline.
- **Log levels mean what they claim.** `ERROR` is for things the on-call should see (matches an alert or a triage queue). `WARN` is for things that might matter under load. `INFO` is for normal operation. `DEBUG` is off in prod or sampled heavily. An AI-generated config that logs everything at `INFO` with stack traces at `WARN` fails this gate.
- **Correlation IDs propagate.** A `trace_id` generated at the edge is threaded through every call (synchronous, async, queued, gRPC, HTTP). See `references/tracing.md` for the OpenTelemetry propagation spec; the logger and the tracer use the same ID.
- **PII is scrubbed at ingest.** Declared PII fields (email, phone, address, full request body, authorization headers, payment details) are redacted at the OTel Collector (or equivalent) before they reach the storage backend. This is a GDPR-shaped default. See `references/logging-patterns.md` section 4 for the attribute-processor pattern.
- **Sampling is declared.** If the log rate is high, a sampled pipeline keeps ERROR and selected paths; declare the sample rate in config, not at runtime.
- **Retention is aligned to purpose.** 30 days hot for query, 90 days warm for postmortem, archive for compliance. Declare the aligned windows; do not leave it at vendor defaults.

**Passes when:** one log format is declared and enforced; correlation IDs propagate across every call type in the dependency graph; PII scrubbing is wired at the collector, not at the application boundary; retention is named, not implicit.

### Step 3. Metrics taxonomy

Read `references/metrics-taxonomy.md`. Every metric that exists in the system goes in one of three buckets: golden signals (user-facing SLIs), method metrics (RED for requests, USE for resources), or diagnostics (cause-level, non-alerting).

- **Golden signals per user journey.** For each journey named in Step 1: latency (p50, p95, p99), traffic (throughput), errors (rate), saturation (utilization of the bottleneck resource). These are candidate SLIs. They are the only metrics that belong above the fold on the service's primary dashboard.
- **RED for request/response services.** Rate, Errors, Duration per endpoint. Instrumented once at the framework middleware, not per-handler.
- **USE for infrastructure resources.** Utilization, Saturation, Errors per resource (CPU, memory, disk, connection pool). These are diagnostics; they do not page.
- **Per-service-type catalog.** Workers track queue depth, dequeue rate, processing duration, failure rate, retry rate. Batch jobs track runtime, records processed, failure count, last successful completion. Edge workers track request count, error rate, CPU time. Data pipelines track freshness lag, row count, dedupe rate. See `references/metrics-taxonomy.md` for each catalog.
- **Cardinality budget.** Any metric with a high-cardinality label (`user_id`, `request_id`, `tenant_id`, `order_id`) on a per-time-series priced backend (Datadog, New Relic) is rejected. High-cardinality dimensions go on wide events (Honeycomb, ClickHouse-based stacks) or are explicitly excluded at the pipeline.

**Passes when:** every user journey has a golden-signal set named; every service has a RED or USE set per its topology; every high-cardinality dimension is either on a wide-event backend or excluded from the metrics pipeline with a named rule.

### Step 4. SLO design

Read `references/slo-design.md`. This is the load-bearing step. The paper-SLO test applies here and nowhere else.

For each user journey named in Step 1:

1. **Pick one SLI.** One measurable question: "what fraction of requests in journey X returned a success response in under N ms." Not three. Not zero. One.
2. **Pick an SLO number.** Start loose; tighten with data. 99% is a reasonable starting point. 99.9% requires a dependency stack that actually allows it; if the upstream is 99.9%, the downstream cannot promise better. Do the math across the dependency graph (Step 1); the product is the ceiling.
3. **Pick the window.** Rolling 28 or 30 days is the default. Shorter windows (7 days) are more responsive but noisier.
4. **Compute the error budget.** `1 - SLO`, converted to "bad events per window." For 99.9% over 30 days at 10M requests per window, that is 10,000 bad events.
5. **Write the error-budget policy.** This is the document that tells product and engineering how to behave when the budget burns. Template: "if we burn more than 50% of the budget by the halfway point of the window, pause non-reliability feature launches and direct engineering effort at restoring the budget." The policy names the trigger, the action, the stakeholder, and the exit criterion. An SLO without a policy is a paper SLO; the skill refuses.
6. **Record the SLO in `.observe-ready/SLOs.md`.** Name, SLI query, target, window, error budget, policy, owner, last-reviewed date.

**Low-traffic exception.** Services with fewer requests than the SLO's error count over a reasonable window (rough rule: fewer than 10x the error budget per window) cannot compute meaningful burn rates. Use one of: extended windows, synthetic traffic, or aggregation across related services. Declare the choice.

**Passes when:** every user journey has an SLO recorded with all seven fields (SLI, target, window, budget, policy, owner, last-reviewed); every SLO is feasible against its dependency-chain math; the error-budget policy names a trigger and an action.

### Step 5. Alert design

Read `references/alert-patterns.md`. Alerts are derivative of SLOs, not parallel to them.

Enforce:

- **Pages are on SLIs, not on causes.** A page fires when an SLO's error-budget burn rate exceeds threshold. It does not fire on CPU > 80%, memory > 75%, disk > 90% unless that signal predicts an SLO burn in a short horizon. Symptom-based pages, cause-based diagnostics. See `references/alert-patterns.md` section 2 for the Ewaschuk-derived rule.
- **Multi-window multi-burn-rate alert tiers.** Never single-window. The four-tier matrix (fast-acute, medium, slow, drift) is the default. The SRE workbook math is reproduced in `alert-patterns.md` section 3.
- **Severity ladder.** PAGE (urgent, user-visible, wake someone up). TICKET (latent, needs attention this business day). LOG-ONLY (trend, review in weekly ops). Three tiers. No "P1 / P2 / P3 / P4" expansion that creates ambiguity.
- **Every PAGE has a runbook link.** Not a wiki page name, a URL. Not a URL to a directory, a URL to a specific runbook for this alert. See Step 9 for runbook discipline.
- **Every alert has an owner.** Name, team, and rotation. If nobody owns the alert, it is deleted, not muted.
- **Deadman switches on silent paths.** For services that produce a heartbeat, alert on absence. Checkly's own 5-hour outage from missing deadman alerts is the citation ([Checkly](https://www.checklyhq.com/blog/post-mortem-outage-browser-check-results-alerting)).
- **Routing is out-of-band.** The pager path does not depend on the service being paged. If PagerDuty is routed through the same Slack workspace that depends on the app's SSO, the path fails the Facebook 2021 test.
- **Prune cadence is declared.** Alerts that did not fire in the last 90 days get reviewed. Alerts that fired and were dismissed >3 times without action are candidates for deletion or threshold tuning.

**Passes when:** every page is tied to a named SLO; every SLO has multi-window multi-burn-rate alerts at the tier defaults; every page has a runbook URL, an owner, and a routing path independent of the service; the pruning cadence is on the calendar.

### Step 6. Dashboard design

Read `references/dashboards.md`. The dashboard is the operator's answer key, not the engineer's art project.

Enforce the above-the-fold rule:

- **First screen answers the question "is this service meeting its SLOs."** Seven or fewer charts above the fold. Each one corresponds to a named SLO, an SLI, or a diagnostic explicitly needed during incidents. The first chart is the burn-rate gauge. Anything not needed to triage goes below the fold or on a secondary dashboard.
- **Every chart has an owner.** Dashboard metadata carries `owner`, `last_reviewed`, `purpose`. Anything missing these is a blind dashboard; the skill flags it for pruning.
- **Chart semantics are strict.** `p99` not `avg` for latency. Rate as `events/sec` not raw counts. Time ranges align (1h, 6h, 24h, 7d panels do not silently mix).
- **Per-service-type catalogs.** A request/response service has the same shape of primary dashboard as every other request/response service. An operator who knows one service can read another without a tutorial. See `references/dashboards.md` section 3 for the catalog.
- **Sprawl budget.** No more than three dashboards per service (primary, drilldown, dependencies). If a service grows a fourth, one of the existing three is pruned or merged. This is the explicit defense against the Flexport 2700-dashboard pattern ([Tasman](https://www.tasman.ai/news/dashboard-sprawl-is-killing-your-business)).

**Passes when:** primary dashboards have seven or fewer above-the-fold charts; every chart is bound to an SLO, an SLI, or a named diagnostic; every dashboard has owner and last-reviewed metadata; the per-service-type shape is consistent across services.

### Step 7. Distributed tracing

Read `references/tracing.md`. Traces answer "where did time go on this request," which metrics and logs cannot.

Enforce:

- **OpenTelemetry as the instrumentation layer.** Vendor-agnostic. The SDK attaches context on entry and propagates it through the dependency graph. W3C Trace Context is the default; Baggage carries business context.
- **Context propagates across every boundary.** Synchronous HTTP, gRPC, async queues, long-lived streams, serverless cold starts, fan-out. See `references/tracing.md` section 3 for the traps and the remediations.
- **Sampling is appropriate to trace purpose.** Head-based at 1% is acceptable for cheap learning; it drops most error traces at birth. Any prod service with SLOs requires tail-based sampling (or error-biased sampling) that keeps the interesting tail. `references/tracing.md` section 4 covers the collector buffer math and the tradeoffs.
- **Retention aligns to SLO window.** If SLO is rolling 30 days and trace retention is 15 days, the skill flags the mismatch. Retention can be tiered (hot 7 days, warm 30 days, cold 90 days) but the SLO-aligned tier must cover the SLO window.
- **Span hygiene.** Span names are low-cardinality (the route pattern, not the URL). Span attributes include the SLI-relevant fields. No PII in span attributes; scrub at the collector.

**Passes when:** OTel instrumentation is in place across the dependency graph; context propagates through every boundary the graph names; sampling is error-biased or tail-based for every prod service with an SLO; trace retention covers the SLO window.

### Step 8. Error tracking

Read `references/error-tracking.md`. Error trackers (Sentry, Rollbar, Bugsnag, Honeycomb's errors pane) are a different lens from metrics, not a redundant one.

Enforce:

- **Exception capture with breadcrumbs and stack traces.** Every service reports exceptions to the error tracker. The exception carries: `service`, `release`, `environment`, `user_segment`, `trace_id`, breadcrumbs, sanitized request context.
- **Release tagging is required.** Every deploy tags the error stream with the release identifier (from `.deploy-ready/STATE.md`). This is how you answer "did this error start with v1.12.3."
- **Grouping is tuned, not default.** Sentry and Rollbar default grouping is aggressive; it can merge distinct errors or over-split the same error across versions. Review grouping for the top 20 signatures quarterly.
- **Error tracking does not replace metrics.** A 500 error rate metric tells you how often something failed; the error tracker tells you what failed. Both are required; neither substitutes.
- **PII handling.** Request bodies, user identifiers, payment details are scrubbed before capture. Most trackers have a scrubber; it must be configured.

**Passes when:** every service reports to the error tracker with release tagging; grouping has been tuned on the top 20 signatures in the last quarter; the PII scrubber is configured; no duplication exists between metrics-based error rates and tracker-reported exception counts (they answer different questions by design).

### Step 9. Runbook discipline

Read `references/runbooks.md` (the file title in the catalog is `incident-response.md` and covers both runbooks and incident coordination).

Enforce:

- **Every PAGE has a runbook.** Not a stub. A runbook the on-call can execute at 3am with a single browser tab.
- **Runbook template is fixed.**
  - Section 1: alert firing context (which SLO, which journey, which service).
  - Section 2: three-to-five diagnostic queries with commands (not descriptions of queries).
  - Section 3: decision tree for rollback vs. scale vs. escalate vs. communicate.
  - Section 4: escalation path with names, channels, and phone numbers.
  - Section 5: post-incident checklist.
- **Runbooks are executable.** Every command in a runbook is a real command against real infrastructure. No `# check the logs`; use `kubectl logs -n prod deploy/api --tail 200 | grep trace_id=XXXX` with the exact flag set this service uses.
- **Last-executed date is required.** A runbook without a `last_executed` marker in the last 90 days is a paper runbook; the skill flags it for a tabletop walk.
- **Hosted out-of-band.** Runbooks on the same cluster as the app are unreachable runbooks. Store them on a distinct infrastructure: a git repo mirrored to a read-only viewer, a status-page equivalent, or a printed card in the DC. Facebook 2021 and Roblox 2021 are the citations.
- **Linked from the alert, not the wiki.** The PagerDuty / incident.io alert payload includes the runbook URL directly, not a wiki search.

**Passes when:** every PAGE alert links to a runbook; every runbook has a last-executed date in the last 90 days; runbook hosting is independent of the observed service; runbook format matches the fixed template.

### Step 10. Observability surface independence

Read `references/dependency-graph.md` (included within `vendor-landscape.md`).

Apply the dependency test to every observability artifact:

| Artifact | Question | If dependent |
|---|---|---|
| Dashboards | If the app's cluster is down, can I view the dashboard? | Host the minimum-viable dashboard out-of-band (different cluster, different region, different provider). |
| Alert routing | If Slack is down, do I still get paged? | PagerDuty directly via SMS/phone, not only via Slack integration. |
| Runbooks | If SSO via the app's IdP is down, can I open the runbook? | Out-of-band runbook store (printed, mirrored, or on an independent IdP). |
| Status page | If the region is degraded, can customers check status? | Hosted on a different provider or region than the app itself. |
| Trace store | If the trace backend runs on the same cluster, can I trace the cluster outage? | Trace backend on a distinct infrastructure or a managed vendor. |
| On-call schedule | If the calendar is on the app's auth, can the next oncall find out they are up? | Schedule source is independent (PagerDuty, incident.io, etc., with phone tree fallback). |

Record the outcome in `.observe-ready/INDEPENDENCE.md`. Any "dependent" row gets a remediation or an explicit exception (e.g., the app is small enough that the tradeoff is acceptable, and the on-call knows).

**Passes when:** the six-row independence test is walked in writing; every "dependent" row has a remediation or a justified exception; the minimum-viable out-of-band surface (dashboard snapshot, runbook mirror, status page) exists.

### Step 11. Incident response and post-mortem cadence

Read `references/post-mortem.md`.

Incident response:

- **Severity ladder.** SEV-1 (user-visible, widespread, active). SEV-2 (user-visible, bounded or degraded). SEV-3 (internal-visible, no user impact yet). Each SEV carries a response expectation (page count, war-room opens, status-page updated, customer comms on what cadence).
- **Incident commander role.** Named per incident. Runs the war-room; does not fix. Rotates with the on-call.
- **Status page updates.** SEV-1 and SEV-2 trigger an initial status update within 15 minutes and at a declared cadence thereafter.
- **Customer communication.** Separate channel from internal comms; templated so it does not require writing under pressure.

Post-mortem:

- **Blameless format.** "What happened, what we observed, what we did, what we learned." No names attached to blame; names attached to expertise.
- **Five Whys or equivalent causal analysis.** Not as ritual; as a structural forcing function to get past the surface cause.
- **Action items tracked to closure.** Every post-mortem emits a list of action items with owner, due date, and SLO or runbook impact. Tracked in `.observe-ready/incidents/NNN-slug.md` and reviewed at the end-of-sprint retro.
- **Incident-to-learning loop.** Every incident surfaces at least one observability gap (an alert that should have fired, a dashboard that should have existed, a runbook that was missing or stale). That gap becomes an action item with a sprint-bounded due date.
- **Alert pruning after incidents.** An incident that fired ten alerts where two were useful prunes the other eight. This is the defense against the GitHub 2018 alert-fatigue-under-load pattern.

**Passes when:** severity ladder is declared; incident commander role exists on the rotation; the post-mortem template is in use on the last three incidents (or a documented "no incidents in the last quarter"); action items from the last post-mortem are tracked to closure with explicit SLO or runbook impact.

## Completion tiers

20 requirements across 4 tiers. Aim for the highest tier the session allows. Declare each tier explicitly at its boundary.

### Tier 1: Instrumented (5)

The app emits coherent telemetry and exceptions are captured.

| # | Requirement |
|---|---|
| 1 | **Structured logging.** One JSON format across services, with `trace_id`, `service`, `level`, `timestamp`, `event`. Levels mean what they claim. |
| 2 | **Correlation IDs propagate.** `trace_id` threads through every call in the dependency graph: sync HTTP, gRPC, async queues, scheduled jobs. |
| 3 | **PII scrubbed at ingest.** Declared PII fields redacted at the OTel Collector (or equivalent) before reaching the storage backend. |
| 4 | **Error tracker live.** Every service reports exceptions to Sentry / Rollbar / Bugsnag (or equivalent) with release tagging from `.deploy-ready/STATE.md`. |
| 5 | **Metrics taxonomy applied.** Every service has a named RED or USE set per its topology; every high-cardinality dimension is placed appropriately for the pricing model. |

### Tier 2: Promised (5)

Every user journey has an SLO, and alerts are tied to the SLOs, not to thresholds.

| # | Requirement |
|---|---|
| 6 | **SLO per user journey.** Every named user journey has one SLI, one SLO number, one window, one error budget, one error-budget policy, one owner, one last-reviewed date. |
| 7 | **Error-budget policy is written.** The policy names the trigger, the action, the stakeholder, and the exit criterion. No SLO ships as a number without a policy (the paper-SLO refusal). |
| 8 | **Multi-window multi-burn-rate alerts.** Every SLO has the four-tier alert matrix (fast, medium, slow, drift). No single-window burn-rate alerts. |
| 9 | **Symptom-based pages.** Pages fire on SLI burn rate, not on CPU / memory / disk thresholds. Cause-level metrics are diagnostics only. |
| 10 | **Every alert has a runbook link.** URL, not a wiki path. Pointing at a specific runbook, not a directory of runbooks. |

### Tier 3: Traceable (5)

Traces, dashboards, and runbooks are actually usable during an incident.

| # | Requirement |
|---|---|
| 11 | **OTel tracing across the graph.** Context propagates through every boundary the dependency graph names. No "the trace ends at the queue." |
| 12 | **Tail or error-biased trace sampling.** Head sampling at 1% is rejected for prod services with SLOs. Retention covers the SLO window. |
| 13 | **Above-the-fold dashboard discipline.** Primary dashboard per service has seven or fewer above-the-fold charts; each chart binds to a named SLO, SLI, or diagnostic. |
| 14 | **Runbook per PAGE, executable, last-executed <90 days.** Every PAGE alert links a runbook that has been walked in the last quarter. No paper runbooks. |
| 15 | **Dashboard and alert metadata.** Every artifact carries owner and last-reviewed date. Unowned artifacts are pruned, not muted. |

### Tier 4: Rehearsed (5)

The observability surface is reachable during the incident it describes, and the team learns from every incident.

| # | Requirement |
|---|---|
| 16 | **Observability surface independence test walked.** The six-row dependency test in Step 10 is in `.observe-ready/INDEPENDENCE.md` with each row green or exception-justified. Minimum-viable out-of-band surface exists. |
| 17 | **Severity ladder and incident commander role live.** SEV-1 / SEV-2 / SEV-3 defined; IC role on rotation; status-page update cadence declared. |
| 18 | **Blameless post-mortem template in use.** Last three incidents (or a "no incidents this quarter" note) have post-mortems with action items tracked to closure. |
| 19 | **Incident-to-learning loop closing.** Every post-mortem emits at least one observability-gap action item (missing alert, missing dashboard, stale runbook) with a sprint-bounded due date. |
| 20 | **Alert pruning cadence on the calendar.** Quarterly review of dead alerts, alerts that fired and were dismissed >3 times, alerts that never fired. Log of prunes maintained. |

**Proof test:** a new engineer joining the on-call rotation reads `.observe-ready/STATE.md` and can (a) name the SLOs for every user journey, (b) describe what the error-budget policy does when the budget burns, (c) point at the runbook for each PAGE alert, and (d) walk the minimum-viable out-of-band surface without opening any in-band tool.

## The "have-nots": things that disqualify the observability surface at any tier

If any of these appear, the surface fails this skill's contract and must be fixed:

- An **SLO with no error-budget policy**. Paper SLO. The number is decorative.
- An **alert that pages with no runbook link**. The on-call cannot act without a browser search.
- A **runbook with no `last_executed` date in the last 90 days**. Paper runbook; assumed drifted.
- A **runbook hosted on the service it documents**. Unreachable runbook during the incident.
- A **dashboard with more than seven charts above the fold**. Cognitive overload; triage time goes up.
- A **chart above the fold with no SLO, SLI, or named diagnostic role**. Blind dashboard.
- A **single-window burn-rate alert for an SLO**. Wrong noise / speed tradeoff in both directions.
- A **cause-based alert** (CPU > 80%, memory > 75%, disk > 90%, error count > 0) **wired to the pager as primary**. These are diagnostics, not symptoms. They go to the ticket queue.
- A **log line emitting `user.email` / `user.phone` / `user.address` / `authorization` / card or account numbers / full request body** without the PII scrubber.
- A **high-cardinality label** (`user_id`, `request_id`, `tenant_id`, `order_id`, `session_id`) **on a per-time-series priced metric backend** (Datadog, New Relic CCU, Prometheus Cortex per-series) without an explicit exclusion rule.
- **Head-only trace sampling** (1% or similar) on a prod service with an SLO. Error traces get dropped at birth.
- **Trace retention shorter than the SLO window**. The postmortem cannot query the trace.
- **Error-tracking configuration with no release tag**. You cannot answer "did this start in v1.12.3."
- A **dashboard or alert with no `owner` and no `last_reviewed` metadata**. Orphan artifact; drift begins on day one.
- **Alert routing through a Slack workspace that depends on the app's SSO or the app's region**. The Facebook 2021 / Roblox 2021 pattern.
- An **"add monitoring" output that emits 20+ monitors or 5+ dashboards with no ownership, no SLO mapping, and no pruning policy**. Dashboard sprawl at birth.
- **No deadman-switch alert** on services that emit a heartbeat or run on a schedule. Checkly 2024 is the five-hour-invisible-outage citation.
- **Post-mortem template not used for the last three incidents** (if incidents happened) **or no recorded "no incidents this quarter" note**. Incident-to-learning loop is open.
- An **alert that fired and was dismissed >3 times in a quarter without tuning or deletion**. Contributing to the 85% false-positive baseline.

When you catch yourself about to ship any of these, fix it before proceeding. A bad observability surface is worse than no surface; the team will trust it and discover the gap during the next incident.

## Reference files: load on demand

The body above is enough to start. Load each reference *before* the step that uses it, not after.

| Reference file | When to load | ~Tokens |
|---|---|---|
| `observe-research.md` | **Always.** Start of every session (Step 0). | ~6K |
| `logging-patterns.md` | **Tier 1.** Step 2; structured events, correlation IDs, PII scrubbing, retention. | ~8K |
| `metrics-taxonomy.md` | **Tier 1.** Step 1 and Step 3; RED / USE / golden signals, per-service-type catalogs, cardinality. | ~9K |
| `slo-design.md` | **Tier 2.** Step 4; SLI picking, SLO selection, error-budget policy, multi-burn-rate math, composition. | ~10K |
| `alert-patterns.md` | **Tier 2.** Step 5; symptom-based pages, the four-tier matrix, severity ladder, routing independence, pruning. | ~9K |
| `dashboards.md` | **Tier 3.** Step 6; above-the-fold rule, per-service-type catalog, sprawl budget, chart semantics. | ~8K |
| `tracing.md` | **Tier 3.** Step 7; OTel, context propagation traps, sampling strategies, retention, span hygiene. | ~10K |
| `error-tracking.md` | **Tier 1.** Step 8; exception capture, release tagging, grouping, metrics-vs-errors, PII. | ~6K |
| `incident-response.md` | **Tier 3 / Tier 4.** Step 9 runbook template and Step 11 severity ladder, IC role, status page, comms. | ~9K |
| `post-mortem.md` | **Tier 4.** Step 11; blameless format, Five Whys, action-item tracking, incident-to-learning loop. | ~7K |
| `vendor-landscape.md` | **On demand.** Datadog / Grafana / Honeycomb / New Relic / OTel self-host deltas, pricing traps, independence considerations. | ~10K |
| `RESEARCH-2026-04.md` | **On demand.** Source citations behind every guardrail, incident, and naming-lane decision. | ~30K |
| `observe-antipatterns.md` | **Every SLO definition + Mode C audits.** Named-failure-mode catalog with grep tests, severity, and per-skill guards. Loaded at every alert-routing review. | ~5K |

Skill version and change history live in `CHANGELOG.md`. When resuming a project, confirm the skill version your session loaded matches the version recorded in `.observe-ready/STATE.md`. A skill update between sessions may change guardrails or tier requirements; if versions differ, re-read the changed sections before continuing.

## Suite membership

observe-ready is the shipping-tier skill that owns "keep it healthy once it is live." See `SUITE.md` at the repo root for the full map. Relevant siblings at a glance:

- **Planning tier:** `prd-ready` (what), `architecture-ready` (how), `roadmap-ready` (when), `stack-ready` (with what tools).
- **Building tier:** `production-ready` (the app), `repo-ready` (the repo scaffolding).
- **Shipping tier:** `deploy-ready` (ship it), `observe-ready` (this skill, keep it healthy), `launch-ready` (tell the world), `harden-ready` (survive adversarial attention).

Skills are loosely coupled: each stands alone, each composes with the others via well-defined artifacts. No skill routes through another; the harness is the router. Install what you need.

## Consumes from upstream

When the agent starts, it checks for upstream artifacts and pre-fills from them rather than asking the user to repeat decisions already made. Absence is fine; the skill falls back to its own defaults.

| If present | observe-ready reads it during | To pre-fill |
|---|---|---|
| `.deploy-ready/TOPOLOGY.md` | Step 1 (service inventory) | Service list, topology types, environment list, dependency hints. |
| `.deploy-ready/healthchecks.md` | Step 1 and Step 3 | Healthcheck endpoints per service; these become liveness SLIs and deadman-switch anchors. |
| `.deploy-ready/STATE.md` | Step 8 and Step 11 | Current release identifier (for error-tracking release tagging); in-progress expand/contract cycles (for trace-field stability). |
| `.deploy-ready/incidents/*.md` | Step 11 | Prior deploy-linked incidents; fold into the alert-pruning and runbook-execution cadence. |
| `.stack-ready/DECISION.md` | Step 0 and Step 7 | Chosen observability vendor (if named), chosen language/runtime (for OTel SDK path), chosen hosting (for independence test). |
| `.production-ready/STATE.md` | Step 1 | User journey list (for SLO mapping), feature surface (for RED metric coverage), audit-log schema (for log-field contract). |
| `.production-ready/adr/*.md` | Step 1 and Step 4 | Architectural decisions that affect SLO targets: chosen DB (availability ceiling), auth provider (login-journey SLO target), session store (session-continuity SLO). |

If an upstream artifact *contradicts* the running system (dashboards exist that the deploy topology does not explain, SLOs reference services that are not in the inventory), trust the running system and note the drift. Upstream artifacts are historical records, not current-state overrides.

## Produces for downstream

observe-ready's output is consumed primarily by humans (on-call, incident responders, engineering leadership). There is no suite skill strictly downstream of observe-ready. launch-ready pairs with it; it does not consume it.

observe-ready emits artifacts so the next session can resume without rediscovery:

| Artifact | Path | Purpose |
|---|---|---|
| **SLO register** | `.observe-ready/SLOs.md` | Per-user-journey SLO with SLI query, target, window, budget, policy, owner, last-reviewed. |
| **Dashboard catalog** | `.observe-ready/dashboards.md` | List of dashboards with owner, purpose, last-reviewed, and binding (which SLO or SLI each primary dashboard serves). |
| **Alert policy catalog** | `.observe-ready/alerts.md` | List of alert policies with SLO binding, tier (page/ticket/log), runbook URL, owner, routing path. |
| **Runbook index** | `.observe-ready/runbooks.md` | URL + last-executed date for every runbook. Paper-runbook candidates flagged. |
| **Independence report** | `.observe-ready/INDEPENDENCE.md` | The six-row dependency test from Step 10 with each row's status. |
| **Incident log** | `.observe-ready/incidents/NNN-slug.md` | Blameless post-mortem per incident, with action items. Also read by `deploy-ready` to tune deploy-time alert thresholds. |
| **Session state** | `.observe-ready/STATE.md` | Tier reached, open questions, skill version the session ran under. |

If any of these are missing when another engineer picks up the work, they are rebuilt from the running system in Step 0 and Step 1. The artifacts are cheap to emit and make the observability surface auditable across sessions.

## Handoff: deployment mechanics is not this skill's job

If the work needs pipeline gates, promotion strategy, migration calendars, canary traffic-shift configuration, or rollback choreography, delegate to `deploy-ready`. The two skills compose: deploy-ready owns shipping mechanics; observe-ready owns what the running system tells you. Do not duplicate either.

The tight coupling between the two: a canary in deploy-ready requires a metric from observe-ready. If deploy-ready emits "this ships as a canary," observe-ready must be able to serve the canary metric against a population-tagged SLI. If observe-ready cannot, the canary is cosmetic (deploy-ready calls this the paper-canary rule). Reciprocally, observe-ready's "uniform rollouts defeat symptom-based alerts" rule refers back to deploy-ready's Step 7 rollout-strategy discipline. The skills know about each other; neither generates the other's output.

**If your harness exposes a skill-invocation tool** (e.g., Claude Code's Skill tool), invoke `deploy-ready` directly when the handoff trigger fires. **Otherwise**, surface the handoff to the user: "This step needs `deploy-ready`. Install it or handle the deploy layer separately." Do not attempt to generate canary traffic-shift YAML or expand/contract calendars inline from this skill.

## Session state and handoff

Observability work spans sessions: SLOs take days to stabilize, alert pruning happens over weeks, post-mortem cadence is quarterly. Without a state file, every resume rediscovers the surface from scratch, and paper SLOs accumulate.

Maintain `.observe-ready/STATE.md` at every tier boundary. Read it first on resume. If it conflicts with the running system, trust the running system and update the file.

**Template:**

```markdown
# Observe-Ready State

## Skill version
Built under observe-ready [current skill version], [frontmatter updated date]. If the agent loads a newer version on resume, re-read the changed sections before the next pass.

## Tier reached
Tier 3 (Traceable). Target next: Tier 4 (Rehearsed).

## Services and journeys
| Service | Topology | User journeys touched |
|---|---|---|
| api | request/response | signup, login, create_order, export_report |
| worker | async queue | order_fulfillment, email_send |
| edge | edge worker | (traffic routing only; no user journey directly) |

## SLOs active
| Journey | SLI | SLO | Window | Owner | Last reviewed |
|---|---|---|---|---|---|
| signup | 2xx in <500ms | 99.5% | 30d rolling | @api-team | 2026-04-15 |
| login | 2xx in <300ms | 99.9% | 30d rolling | @api-team | 2026-04-15 |
| create_order | 2xx in <800ms | 99.5% | 30d rolling | @orders | 2026-04-10 |
| export_report | 2xx in <5s | 99% | 7d rolling | @reports | 2026-04-18 |

## Paper-SLO watchlist
- None currently; all active SLOs have written policies.

## Dashboards
- api primary. Owner @api-team. Last reviewed 2026-04-15. 6 charts above fold.
- orders primary. Owner @orders. Last reviewed 2026-04-10. 5 charts above fold.
- shared deps. Owner @platform. Last reviewed 2026-04-05. 4 charts above fold.

## Runbooks
- signup-slo-burn. Last executed 2026-03-28 (tabletop).
- login-slo-burn. Last executed 2026-04-01 (real incident INC-037).
- create_order-slo-burn. Last executed 2026-02-14 (tabletop). FLAG: approaching 90-day stale.

## Independence report
See .observe-ready/INDEPENDENCE.md. Status: 5 of 6 rows green; 1 exception (status page hosted on same region as app, justified because the app is small).

## Incidents this quarter
- INC-037 (2026-04-01). Login latency spike during DB failover. Post-mortem done, 3 action items: 2 closed, 1 in flight (add DB connection-pool saturation alert).
- INC-036 (2026-03-20). Worker queue depth alert fired 90 min late. Post-mortem done, all 2 action items closed.

## Alert pruning last pass
2026-04-05. Pruned 4 alerts (never fired in 90 days); tuned 3 (>3 dismissals without action); added 2 (from INC-036 and INC-037).

## Open questions blocking next tier
- [open, target: Tier 4] Quarterly alert pruning not yet on the calendar. Owner: @sre-lead.
- [open, target: Tier 4] Status-page out-of-band copy not yet set up. Owner: @platform.

## Last session note
[2026-04-22] Completed SLO pass on export_report. Next: status-page independence.
```

**Rules:**
- STATE.md is the contract with the next session. If it is out of date, the next session rediscovers the surface.
- At every `/compact`, `/clear`, or context reset, update STATE.md first.
- Never delete STATE.md. If an entry is wrong, correct it in place with a dated note.
- The paper-SLO watchlist is load-bearing. An SLO without a policy is a paper SLO; surfacing them in STATE.md keeps them visible until fixed.

## Keep going until it is actually observed

The dashboards rendering is roughly 20% of the work. The remaining 80% is the SLO binding, the error-budget policy, the multi-burn-rate alerting, the runbook-per-page, the retention alignment, the independence test, and the incident-to-learning loop. Budget for all of it.

An "observed" service is one where a new on-call reads the primary dashboard in 30 seconds and knows whether the service is meeting its promises; opens the runbook for the firing alert and executes the first diagnostic command without editing it; and, if the main cluster is down, still has a usable out-of-band surface to triage from. When in doubt, open the primary dashboard and ask: "is the service meeting its SLO right now, and do I know what to do if it is not." The first question the dashboard cannot answer cleanly is the next thing to fix.
