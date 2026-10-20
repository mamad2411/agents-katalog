---
name: observability-and-monitoring
description: Use this skill to make a running application or service observable — to answer "is it down, why, and for whom." Trigger it on "add logging", "set up structured logs", "set up Sentry / error tracking", "why is prod slow / failing", "we're flying blind", "add tracing / OpenTelemetry", "add metrics / dashboards", "set up alerts / on-call / PagerDuty", "define an SLO / error budget", "instrument this endpoint / job", "add request IDs", "capture Core Web Vitals / RUM / session replay", or any request to see what a deployed app is doing in production. Covers the three pillars — logs, metrics, traces — plus error tracking and frontend RUM, for web apps, APIs, and background jobs (Next.js 15 / Node / edge / serverless, Vercel-first but stack-aware). Cardinal rule: instrument only for questions you will actually ask, and every alert must be actionable or deleted. This skill does NOT cover ML/model monitoring (prediction logging, feature/label drift, model quality) — that is a different concern; hand off to `17-observability`. It also does not fix performance (hand deep CWV / latency work to `performance-optimization`) or audit log-injection vulns (that is `security-and-hardening`); it decides what telemetry to emit and how.
---

# Observability and Monitoring

Makes a deployed app answer three questions fast: **is it down, why, and for whom.** The three pillars — **logs** (what happened), **metrics** (how much / how often), **traces** (where in the request path) — plus **error tracking** and **frontend RUM** exist to serve those questions, nothing more.

**Cardinal rule — instrument for questions you will actually ask; every alert must be actionable or deleted.** Telemetry is not free: it costs money (ingest/retention), latency (spans, exporters), and attention (dashboards nobody reads, alerts everyone mutes). Do not add a log line, metric, or alert unless you can name the question it answers or the action it triggers. A dashboard that answers no question is vanity; an alert nobody acts on is noise that trains the team to ignore the pager.

**Second rule — telemetry must never leak PII or secrets.** Logs, spans, breadcrumbs, and session replays are a data-exfiltration surface. Redaction is mandatory and belongs at the emit layer, not "later." Tokens, passwords, auth headers, card/PII fields get scrubbed before they leave the process. This is a SECURE concern — pair with `security-and-hardening` and `env-secrets-manager`.

This skill is application/service telemetry only. **ML model monitoring (drift, prediction logging, model quality) is a different skill — `17-observability`.** Do not overlap; hand it off.

---

## Sections

```
0. ROUTE    → dispatch on the request
1. ASSESS   → what telemetry already exists; what question can't be answered today
2. LOGS     → structured JSON, levels, correlation IDs, redaction, cost control
3. ERRORS+  → error tracking (Sentry) + distributed tracing (OpenTelemetry)
   TRACES
4. METRICS  → RED/USE, SLIs→SLOs→error budgets, actionable alerts, dashboards
5. FRONTEND → RUM: Core Web Vitals field data, client errors, session replay
6. VERIFY   → prove the telemetry actually fires and answers the question
```

ASSESS is the front door on any existing app — you cannot add the right telemetry without knowing the gap. Move one section at a time; do not bolt on a dashboard before there is signal to put on it.

---

## Section 0 — ROUTE

Dispatch on the request and the state of the app:

- "add logging / request IDs / structured logs" → **LOGS** (`references/logging.md`)
- "set up Sentry / error tracking / why did this throw" → **ERRORS+TRACES** (`references/error-tracking-and-tracing.md`)
- "add tracing / OpenTelemetry / it's slow *somewhere*" → **ERRORS+TRACES**
- "add metrics / dashboards / alerts / SLO / on-call" → **METRICS** (`references/metrics-slos-alerts.md`)
- "Core Web Vitals in the field / client errors / session replay" → **FRONTEND** (`references/frontend-observability.md`)
- "we're flying blind / set up monitoring from scratch" → **ASSESS**, then the pillars in order
- a live incident happening right now → this skill sets up the signal; hand the *investigation* to `systematic-debugging` / `debugging-and-error-recovery` and the `l3-support` agent
- "model is drifting / log predictions / monitor accuracy" → **not this skill** → `17-observability`

---

## Section 1 — ASSESS (the default entry point)

Read what emits signal today before adding more. Inventory across the pillars:

- **Logs** — structured JSON or `console.log` soup? Are levels used? Is there a correlation/request ID threading a request across services and async boundaries? Is anything redacted?
- **Errors** — is there an error tracker at all (Sentry/equivalent), on client *and* server *and* edge? Are releases + source maps wired so a stack trace points at real code?
- **Traces** — can you follow one request from edge → server action → DB → job? Or does the trail die at each boundary?
- **Metrics/SLOs** — is there a single number that says "healthy or not"? Any alert? Is any alert *actionable*, or are they all "CPU > 80%" noise?
- **Frontend** — is there field CWV data (not just lab Lighthouse)? Are client-side errors captured and tied to a backend trace?

Output the **one question you cannot answer today** ("which user hit the 500s at 3am, and what was the slow span") — that question drives which pillar to build first. Grade gaps 🔴 blind (can't answer "is it down") / 🟡 partial. Do not instrument everything; instrument the gap.

---

## Section 2 — LOGS

Read `references/logging.md`. Structured JSON from line one (Pino on Node), a disciplined level ladder (`fatal/error/warn/info/debug/trace`), and **one correlation/request ID propagated across every async boundary** via `AsyncLocalStorage` so a request is greppable end to end. Redaction of PII/secrets/tokens is mandatory and configured at the logger, not sprinkled at call sites. Control cost with sampling of high-volume `info`, not by dropping errors. Know the log-vs-metric-vs-trace decision (a per-request counter is a metric, not a log line) and the edge/serverless caveats (no filesystem, flush-before-freeze, `console` as transport).

---

## Section 3 — ERRORS + TRACES

Read `references/error-tracking-and-tracing.md`. **Sentry for Next.js** wired on all three runtimes (client, server, edge), with release tracking + source map upload so stack traces are readable, and PII scrubbing (`sendDefaultPii: false`, `beforeSend` redaction). **OpenTelemetry** for spans and context propagation — the standard, vendor-neutral, so you are not locked to one backend. Distributed tracing must survive the hops that matter: HTTP → server action → DB query → enqueued job. Sample smartly (head vs tail; keep 100% of errors, sample the boring 200s). A good span is named for an operation, carries a few high-cardinality attributes, and does not log a secret in its tags.

---

## Section 4 — METRICS / SLOs / ALERTS

Read `references/metrics-slos-alerts.md`. Instrument services with **RED** (Rate, Errors, Duration) and resources with **USE** (Utilization, Saturation, Errors). Turn the metrics that matter to users into **SLIs → SLOs → error budgets**, and alert on **symptoms users feel** (error rate, latency, budget burn), never on causes nobody acts on (raw CPU). Every alert links a runbook and names an owner — an alert without an action is deleted. Dashboards answer a specific question ("are we serving requests successfully and fast?"), not a wall of vanity gauges. Prometheus/Grafana(+Loki/Tempo) self-hosted vs hosted (Datadog/Axiom/Grafana Cloud) is a cost/ops trade, decided in the reference.

---

## Section 5 — FRONTEND (RUM)

Read `references/frontend-observability.md`. Real User Monitoring captures **field** Core Web Vitals (LCP/INP/CLS) from actual devices — the p75 that ranking and users care about, not a lab score. Capture unhandled client errors and tie them back to the backend trace (propagate `trace-id`) so a white screen has a server-side story. Session replay is powerful and dangerous: enable **privacy masking by default** (mask all text/inputs, block sensitive nodes) or it becomes a PII firehose. Set budgets/regression alerts on CWV. **Deep CWV *fixing* is not this skill — hand LCP/INP/CLS remediation to `performance-optimization`;** this skill sets up the measurement and the regression alert.

---

## Section 6 — VERIFY

Telemetry that doesn't fire is worse than none — it gives false confidence. Before calling it done: trigger a test error and confirm it lands in Sentry with a readable (source-mapped) stack; make a request and confirm one correlation ID threads the logs and a trace shows the full span tree; confirm a redaction rule actually scrubs a planted fake secret; fire a test alert and confirm it pages the right place with its runbook. Use `verify` (quick confirm) or `qa-tester` (full pass); drive the browser with `browser-testing-with-devtools` to confirm RUM beacons send.

---

## Orchestration

This skill owns *what telemetry to emit and how*; it delegates execution. Route selection through **`decider`** (this repo's standard router — pass it the situation, stage, and tasks; it returns the picks), and slot into the house pipeline `PLAN → EXECUTE → [SECURE/A11Y/PERF] → REVIEW → TEST → VERIFY`. This skill is the natural companion to the **PERF gate (`performance-optimization`)** — observability *finds* the slow path, PERF *fixes* it — and to **`shipping-and-launch`**, which needs monitoring + rollback readiness in place before go-live.

- Skill selection / routing → **`decider`**
- **SECURE**: logs/traces/replays must redact PII & secrets → **`security-and-hardening`** + **`env-secrets-manager`** (DSN and API keys are secrets)
- Slow path found via a trace → **`performance-optimization`** (the PERF gate owns the fix)
- Pre-launch monitoring + rollback wiring → **`shipping-and-launch`**; alerts/dashboards in CI → **`ci-cd-and-automation`**
- A live incident to investigate → **`systematic-debugging`** (root-cause) / **`debugging-and-error-recovery`** (triage) and the **`l3-support`** agent (owns prod monitoring + postmortem); infra/IaC telemetry review → the **`infra-reviewer`** agent; a security-relevant log event or breach signal → the **`cybersec-blue-team`** agent
- Designing the log/metric/event *schema* as a contract → **`api-and-interface-design`**; recording the SLO/alerting decision → **`documentation-and-adrs`**
- Verifying it fires → **`verify`** / **`qa-tester`** / **`browser-testing-with-devtools`**
- **ML model monitoring (drift, prediction logging) → `17-observability`** (out of scope here)

Read a chosen skill's own SKILL.md before running it.

---

## Enforcement over vibes

"Remember to add a request ID" and "please don't log the password" are wishes that drift. Make them structural: a **logger wrapper** as the only sanctioned log path (raw `console.log` fails lint via `no-console`), redaction configured **in the logger** so a new field can't leak by omission, correlation IDs injected by **middleware** not by hand, OpenTelemetry auto-instrumentation so new routes are traced without ceremony, and SLOs/alerts as **code** (Terraform / Grafana-as-code / `alerts.yml`) reviewed in PRs. Telemetry you rely on for incidents belongs in the CI gate, not in a README.

---

## Operating principles

- **Instrument for a question.** No log/metric/span without a question it answers or an action it triggers.
- **Every alert is actionable or deleted.** Symptom-based, owner-named, runbook-linked. Noise trains people to ignore the pager.
- **Redact at the source.** PII/secrets scrubbed at the emit layer, never "cleaned up later." SECURE gate is mandatory.
- **Prefer standards.** OpenTelemetry over proprietary SDKs; you keep the data when you change vendors.
- **Correlate across pillars.** One request ID / trace ID links a log line, a span, and a frontend error. Uncorrelated pillars are three dead ends.
- **Cardinality and cost are real.** High-cardinality labels explode metric bills; sample the boring, keep the errors.
- **Verify it fires.** Untested telemetry is false confidence — trigger it and watch it land.
- **Stay in scope.** App/service telemetry here; model monitoring → `17-observability`; the perf *fix* → `performance-optimization`.
- **Match the user's language** (Russian, Uzbek, English).
- **Web-first, stack-aware.** Defaults tuned to Next.js 15 App Router + RSC + Vercel; Node services, edge runtime, and serverless cold-start caveats handled per-section.

---

## Worked examples (abbreviated)

**"Prod throws 500s at night and we have no idea why — we're flying blind."**
ROUTE → ASSESS: only `console.log`, no error tracker, no request ID. The unanswerable question is "which user, which route, what was slow." Build in order: LOGS (Pino + `AsyncLocalStorage` request ID + redaction) so requests are greppable → ERRORS (Sentry on server+edge+client, releases+source maps) so the throw has a readable stack → one RED dashboard + a single symptom alert on 5xx rate with a runbook. VERIFY by triggering a test error. Hand the actual root-cause dig to `systematic-debugging`.

**"Add an SLO and stop the alert spam."**
ROUTE → METRICS. Define the SLI (successful requests < 500ms / total), set a 99.5% SLO with a 30-day error budget, replace the twelve cause-based CPU/memory alerts with two symptom alerts (fast-burn and slow-burn on budget), each with an owner and runbook. Delete the rest. Record the decision via `documentation-and-adrs`.

**"Users say the app feels slow but Lighthouse is green."**
ROUTE → FRONTEND. Lab ≠ field. Wire RUM to capture p75 INP/LCP/CLS from real devices, tie client errors to backend traces. The field data shows INP p75 = 480ms on the dashboard route. This skill's job ends at "measured + regression alert set"; hand the INP *fix* to `performance-optimization`.
