---
name: platform-fitness-functions
description: >-
  Instrument a platform roadmap with executable architectural fitness
  functions and metrics using CI tests, staged warning-to-error thresholds,
  DORA signals, GQM workshops, and transparent maturity indexes. Use for
  evolutionary architecture, platform KPIs, deployment frequency, lead time,
  change failure rate, MTTR, SPACE or DevEx metrics, policy gates, dependency
  currency, metric workshops, or proving roadmap progress with evidence.
---

# Platform Fitness Functions

## Purpose
What can be measured can be governed. This skill turns roadmap intentions into executable governance: every milestone becomes a fitness-function promotion (a threshold tightening from warning to error), every claim of progress becomes a metric with a pipeline behind it, and every division-specific "what should we even measure?" becomes a GQM tree. A fitness function is a unit/integration test for architecture — an objective, quantifiable assessment of an architectural characteristic, run continually so degradation cannot creep in silently. Pairs with `platform-maturity-benchmark` (whose gap register this instruments) and consumes check inventories from every other skill in this plugin.

## Core model to hold in your head

### The six-axis fitness-function taxonomy
Classify every FF along six dimensions; the classification tells you where it runs and what it costs:

| Axis | Poles | Platform examples |
|---|---|---|
| Scope | **Atomic** (one characteristic, one context) vs **holistic** (combined characteristics) | Cyclomatic-complexity gate vs. "security + latency under load" combined test |
| Cadence | **Triggered** (on change) vs **continual** (always-on in prod) vs **temporal** (clock-driven) | CI policy check vs. synthetic-transaction monitor vs. dependency-currency / cert-expiry / credential-TTL sweeps |
| Result | **Static** (fixed pass/fail threshold) vs **dynamic** (threshold shifts with context) | CC < 10 vs. acceptable latency as a function of concurrent jobs |
| Invocation | **Automated** vs **manual** | Pipeline gates vs. legally required human review — automate the detection even when the reaction stays manual |
| Origin | **Intentional** (designed up front) vs **emergent** (added when misbehavior is observed) | Both legitimate; architects should add emergent FFs aggressively when they spot governable misbehavior |
| Coverage | **Domain** vs **architecture** | Experiment-reproducibility check vs. dependency-direction rule |

Category checklist so nothing is forgotten (the API fitness-function categories): code quality, resiliency (fault injection via gateway/mesh), observability conformance, performance, compliance/audit, security (dependency CVEs, OWASP-style scans), operability (monitoring/alerting present). For an ADP add: agent-attribution coverage, credential-TTL ceilings (`agent-identity-engineer`), consumer-driven contract suites (`agent-api-contract-designer`), MCP selection-regression tests (`mcp-platform-api-author`), golden-path scorecards (`golden-path-designer`).

### Authoring workflow: context + metric + executable test
An FF is not a metric; it's a metric with teeth. Each one is authored as:
1. **Context** — which architectural characteristic, why it matters here, recorded as a short ADR.
2. **Target metric** — the quantifiable measure and its threshold.
3. **Automated test** — the executable check wired into the deployment pipeline: ArchUnit-style structure tests, OPA/Kyverno policy evaluations, contract suites, load-test stages, license/CVE scanners — atomic FFs in early stages, holistic FFs in integration stages, manual-triggered stages for human sign-offs.

Prefer executable rules over written guidelines: guidelines require bureaucratic scolding; tests consolidate the rule as an artifact developers and agents both obey.

### Cascading warning→error thresholds: the maturity-progression mechanic
The herding-governance move: when a new FF would fail most of the estate, don't abandon it and don't block everyone — set a lenient threshold as **warning**, announce the schedule, then tighten stepwise into **error**. Teams get time to pay down debt in a controlled, gradual way; the FF stays in place afterward so bit rot cannot return.

This is also THE mechanic that turns a roadmap into something verifiable: **each roadmap milestone = a promotion event** — a named set of FFs moving from absent→warning or warning→error. "We reached Scalable interfaces" becomes "the golden-path scorecard, contract suite, and policy gates now block at these thresholds and the estate passes." Milestones defined this way cannot be gamed by slideware, and `platform-maturity-benchmark` re-scores against enforcement state, not claims.

Temporal FFs backstop the mechanic: dependency-currency checks (how far behind are our libraries, charts, operators), cert and credential expiry sweeps, license-change detection (automated detection, manual lawyer reaction) — clock-driven debt no change-trigger will ever catch.

### DORA four keys from raw event data
Don't buy a metrics product to start; the four keys derive from three raw event streams yielding four instrumentation timestamps — **commits** (commit timestamp), **deployments** (deployment timestamp per service), **incidents** (degradation-detected and resolved timestamps):
- Deployment frequency = count(deployments) / period.
- Lead time for changes = deploy_ts − commit_ts distribution (median, not mean).
- Change failure rate = failed deployments / total (define "failure" explicitly and publish the definition).
- Failed-deployment recovery time = resolved_ts − detected_ts.

For external positioning, retrieve the current DORA report or primary documentation at engagement time and record the publication year, cohort, definitions, and source link. Do not reuse an embedded performance-band table across report generations: metric names, thresholds, and analysis evolve. If the source cannot be verified, report the organization's own baseline and trend without a percentile or performance label.

Operating rules:
- Improve in balance: throughput gains that degrade stability are not gains — the four move as a set.
- Ship a **minimal viable dashboard** first (even a wiki page): current values, trend, raw data and calculations open to everyone.
- Primary audience is the delivery teams themselves — they're who can change the numbers; executives get rolled-up, read-only views and come down to the teams for detail.
- **Conversation, not control:** the metrics start discussions ("where did this queue form?"), never individual performance reviews — weaponized metrics get gamed into uselessness.
- K8s shortcut: deployment-observability tooling (e.g., Keptn-style annotations) emits deploy events with app/env/version dimensions out of the box.

### Service levels and metric lifecycle

For each platform capability, connect three levels:

- **SLI:** the observed measure, with source, query, dimensions, and data-quality checks.
- **SLO:** the internal target and evaluation window that drives operational decisions and an error budget.
- **SLA or service commitment:** the explicit promise to consumers, including support, exclusions, and what happens when the promise is missed.

Do not create an SLA before the underlying SLI is trustworthy or an SLO has been exercised. A dashboard is not a service contract, and an SLI with no target does not guide action.

Every metric also needs a decision contract: owner, consumer, decision it informs, trigger/threshold, review cadence, and retirement condition. At review time ask whether the metric still answers the original question, whether behavior has been gamed, and whether a paired metric is needed to expose a trade-off. Retire or replace metrics that no longer drive a decision; preserving them forever creates dashboard debt and can turn yesterday's proxy into today's target.

### GQM: deriving the division-specific metrics
For everything the standard frameworks don't cover ("are researchers actually faster?", "is agent-generated CI load sustainable?"), run **Goal–Question–Metric** — a hierarchical tree:
- **Goal** (root): purpose + object + issue + viewpoint — e.g., "improve time-to-first-training-run for new experiments, from the researcher's viewpoint."
- **Questions**: what you'd need answered to evaluate the goal.
- **Metrics**: what answers each question; **data** (leaves): what feeds each metric.
- **Prune**: drop weak-signal and costly metrics; prioritize data that feeds multiple metrics cheaply. The tree gives traceability — every collected datum traces to a goal, the antidote to dashboard sprawl.
- Run as a workshop (2–5 people; breakouts for more): agree the goal statement, brainstorm questions, riff metrics, prune together, leave with a collection plan and owners.

Complement DORA's lagging indicators with leading ones (cycle time, queue depth) and SPACE/DevEx signals (satisfaction, flow) so throughput gains aren't purchased with burnout. Advanced KPI menu: cost per deployment/training-run, infrastructure (GPU) utilization, adoption rate, active users, incident frequency and resolution time, experimentation rate, feature adoption rate.

### Numeric maturity-index construction (MMI-style)
When leadership wants "one number tracked quarterly," build it transparently like the Modularity Maturity Index rather than vibing:
- Define principle areas (for an ADP index: identity, interfaces/contracts, golden paths, measurement, agent-readiness) with published weights.
- Per area, a fixed criteria list; each criterion scored 0–10 against published scoring instructions.
- Area score = mean of its criteria; index = weighted sum of areas.
- Properties to copy from the MMI: criteria are inspectable (scores cite evidence), the scheme is stable across assessments (comparable over time and across divisions), and low sub-scores localize the work.

The index is a communication device; the FF suite underneath is the governance — never let the number float free of its criteria.

### Anti-patterns
- **Measurement theater:** dashboards nobody acts on; metrics collected because they're collectible. Every metric must trace to a GQM goal or an FF threshold — or be deleted.
- **Vanity metrics:** activity counts (PRs, suggestions, tickets closed) presented as outcomes; adoption spikes without retention. The survey's warning applies: orgs "have a much better image of themselves than the reality."
- **The portal trap, measurement edition:** instrumenting the portal's clicks while the backend paths have no telemetry — measure path outcomes, not interface activity.
- **Local optimization:** individual output up, org lead time flat — find where the queue moved (usually review/validation) instead of celebrating.
- **No-baseline default:** measuring nothing. Any consistent baseline, however manual, beats it — manual capture first is fine and normal.

## Workflow
1. **Intake the roadmap.** Take the gap register from `platform-maturity-benchmark` (and the ASDLC roadmap from the platform-assessment plugin's `asdlc-maturity-assessment`, if present) for [YOUR ORGANIZATION / CLIENT]; list every milestone that claims progress.
2. **Instrument DORA first:** locate the three event streams, define failure/incident explicitly, stand up the minimal viable dashboard with open raw data; use an external performance band only after retrieving and versioning the current primary source.
3. **Run a GQM workshop** for the division's top 2–3 goals; prune the trees; produce the collection plan with owners.
4. **Author the FF suite:** for each roadmap milestone and each category-checklist row, write context + metric + executable test; classify on the six axes; place in pipeline stages; collect existing checks from sibling skills (policy gates, contract suites, scorecards, selection tests, identity sweeps) into one registry with owners. Add SLI/SLO/service commitments for user-facing platform capabilities.
5. **Define the promotion schedule:** per FF, the warning threshold, tightening steps, and error date; map every roadmap milestone to its promotion set — this mapping IS the instrumented roadmap.
6. **Add temporal FFs:** dependency currency, cert/credential expiry, license-change detection.
7. **Construct the index** (if wanted): areas, criteria, scoring instructions, weights — all published before first scoring.
8. **Output.** An instrumentation pack: DORA pipeline + dashboard spec, GQM trees with collection plans, the FF registry (classification, test, stage, threshold, owner), capability service-level definitions, metric decision/retirement register, the milestone→promotion map, temporal-FF schedule, index definition, and an anti-pattern audit of any existing metrics.

## Guardrails
- No metric without a consumer and a decision it informs; no FF without an executable test — otherwise it's theater.
- Metrics are for conversation and team self-service, never individual performance management; the moment they're weaponized, they're gamed.
- Publish definitions (what counts as a deployment, a failure, an incident) before publishing numbers; changing definitions silently invalidates trends.
- New blocking gates always enter as warnings with an announced promotion date (herding, not ambush).
- Keep the four keys together — never report throughput without stability alongside.
- A maturity index without published criteria and evidence-cited scores is astrology; refuse to produce one.
- Business-value/ROI framing of these same numbers → sibling `platform-roi-scorecard` (platform-assessment plugin); this skill owns the technical instrumentation.
- No SLA or executive promise may outrun the measured SLI and exercised SLO beneath it.

## Suggested effort
High — the DORA baseline plus one GQM workshop is a focused week; the full FF registry and promotion map is an ongoing program artifact the roadmap lives by.
