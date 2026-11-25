---
name: platform-roi-scorecard
description: Build a developer-productivity and platform-ROI scorecard for a platform engineering team — combining DORA, SPACE, MVP-stage, and AI-workload metrics with a full dollar-value ROI calculation, survey + system-data measurement design, industry benchmark calibration, credibility/measurement audit, and adoption tracking. Use whenever the user needs to prove platform value to leadership, build a platform business case, justify AI infrastructure ROI, design a metrics program, design a developer survey, estimate the cost of a platform team, measure developer productivity, calculate ROI, or figure out why platform adoption or credibility is stalling. For industry/vertical benchmark positioning and peer patterns, use the sibling platform-industry-brief skill; for structuring and sizing the platform team itself, use platform-org-design-advisor.
---

# Platform ROI Scorecard

## Purpose
Produce a defensible, dollar-denominated case for a platform team's value — not vibes, not lines of code. Also diagnose (and fix) the "measurement paradox" where teams report improvement without ever having measured a baseline. Siblings: `asdlc-maturity-assessment` supplies the agent-maturity read that segments the measurement layer; `platform-org-design-advisor` produces the team cost model (headcount × salary benchmarks) this scorecard consumes; `platform-industry-brief` carries the full industry benchmark databank behind the calibration table.

## Core model to hold in your head

### Why traditional metrics fail here
Lines of code, story points, and commit counts were built for individual output tracking. They miss what platforms actually create: reduced friction (e.g., deploy time cut from hours to minutes), knowledge sharing (faster onboarding via standardized workflows), error prevention (guardrails catching issues pre-production), and cross-team efficiency (shared tools eliminating duplicate work). Don't let a stakeholder anchor the conversation on these metrics — redirect to the frameworks below.

### The three measurement frameworks, and when to use each
1. **DORA metrics** — system-level delivery health: deployment frequency, lead time for changes, mean time to recovery, change failure rate. Best for showing systemic improvement, especially to technical stakeholders and once a platform is past MVP.
2. **SPACE framework** — developer experience, five dimensions:
   - **S**atisfaction — surveys, NPS
   - **P**erformance — code quality, system reliability
   - **A**ctivity — reviews, deployments (concrete actions)
   - **C**ommunication — knowledge sharing, collaboration
   - **E**fficiency — workflow smoothness, reduced context switching
   Ties technical change to business outcome: higher satisfaction correlates with retention, which is a real dollar figure (see below).
3. **MVP-stage metrics** — for platforms too early for DORA/SPACE to be meaningful:
   - **Complexity Index** = 1 − (unique configurations ÷ total resources). Higher = more standardized.
   - **Onboarding Time** — time to a new developer's first meaningful PR.
   - **Service Creation Time** — end-to-end time to get a new service production-ready.

**Sequencing rule:** early-stage platforms should prioritize onboarding time, satisfaction, and service creation time (adoption/usability signals). As the platform matures, DORA metrics become the stronger signal of systemic engineering improvement. Don't demand DORA-level metrics from a 6-week-old platform.

### Measurement doctrine: survey data and system data are complementary — you need both
Every metric in the scorecard comes from one of two sources, and neither is sufficient alone:
- **System data** (CI/CD, version control, ticketing, deploy toolchain) gives a *continuous*, precise, granular view — but only of what is automatically collected and correlated. Grade every system-derived metric on the **three C's**: **completeness** (enough history in this system of record to support the claim — e.g., a real trend line, not two data points), **comprehensiveness** (captured across ALL relevant systems — time-to-market for a customer request may span the support tracker + requirements tool + agile board + deploy toolchain), and **correctness** (correlated without double-counting — the same item logged as a support ticket and a defect must be reconciled, not counted twice). System data also misses whatever happens outside the tools (un-checked-in config scripts, manual workarounds) and silently drifts stale when the stack changes but the collectors don't.
- **Survey data** gives a *periodic*, holistic view: respondents synthesize automation + process + culture in one pass, catch behavior that bypasses the tooling, and capture culture, job satisfaction, and burnout — which are **leading indicators** of delivery performance and retention. HR attrition data is a lagging proxy: by the time it moves, people have already left.

**Survey design rules** (bake these into any survey you produce):
- Survey the **doers** — people hands-on with the delivery system. Don't survey executives: they systematically overestimate maturity relative to practitioners.
- **20–25 minutes maximum** to protect participation and completion; run it **every 4–6 months** — more often burns respondents out.
- For frequency questions (deploys, releases), offer **log-scale response options** (on demand / weekly / monthly / quarterly / yearly) — practitioners answer reliably at that granularity, not at exact counts.
- Use tested, statistically valid question wording where possible; survey design is a discipline, not a form.

**Triangulation rule:** when survey and system data diverge sharply, that is a *debugging signal, not noise*. If engineers consistently report long build times while dashboards say builds are fast, suspect partial capture or a misconfigured collector before you suspect the engineers — if everyone close to the system says the same thing, treat their experience as a true data point. Investigate every large divergence; it usually exposes a gap in the system data.

### The five dimensions for selecting which metrics matter
Don't try to measure everything. Pick metrics across **velocity, security, quality, people, and cost**, and let business strategy decide the weighting (e.g., a go-to-market strategy demanding high release frequency selects velocity + quality first). Accept that this is a trade-off — document what you are choosing not to prioritize and why.

### Capability-to-outcome chain

Do not jump from “we launched a portal” to “the platform created revenue.” Build an auditable chain for each funded capability:

**Capability shipped → user behavior changed → delivery/operational outcome changed → business outcome changed.**

Example shape: a production-ready service golden path → teams voluntarily use it and complete it without tickets → onboarding and lead time fall while change-failure rate stays within bounds → features reach customers sooner and engineering capacity shifts from plumbing to product work. Every arrow needs evidence; if one is missing, report the value as a hypothesis rather than realized ROI.

Maintain a capability scorecard with:

- owner, target users, baseline and adoption/retention;
- time-to-first-success and completion/bypass rate;
- service SLI/SLO, support demand, reliability and security outcomes;
- cost-to-serve and unit cost per successful completion;
- downstream product or business KPI, attribution method, and confidence tier.

This prevents local optimization: faster provisioning is not a win if ticket volume, failure rate, cognitive load, or cost moves elsewhere. Pair developer-experience evidence with operational evidence, then connect both to the business metric.

### AI-workload extension: when the platform serves AI/ML workloads
Platforms increasingly serve data scientists and ML engineers alongside app developers. Treat models, datasets, and inference endpoints as **versioned, deployable artifacts moving through build/test/production behind golden paths** — the same rigor as microservices — and extend the scorecard with a 6-metric AI velocity set:
1. **Time to first inference** — project kickoff to first production inference request.
2. **Template adoption rate** — % of AI projects using platform-provided templates/golden paths.
3. **GPU utilization** — are clusters efficiently used or sitting idle? (Scale-to-zero on idle inference clusters is the big cost lever.)
4. **Cost per inference** — the unit economics of AI workloads.
5. **Deployment frequency for models** — how often teams ship new model versions through CI/CD.
6. **Governance coverage** — % of AI workloads with complete audit trails (which data trained which model for which application).

Useful sanity-check questions: can a developer stand up a complete AI stack within ~48 hours? Deploy operational AI in weeks rather than months?

**Value-narrative framing — AI-enabled vs. AI-native:** *AI-enabled* means AI tools bolted into existing workflows (coding assistants, chat interfaces, occasional external API calls); *AI-native* means models and inference run as first-class, governed platform services embedded in business processes. The platform's AI ROI story is the measurable move from enabled to native — told with the six metrics above, not with tool-adoption counts.

**Skepticism flag:** treat vendor productivity and revenue claims about AI platforms skeptically — much of what circulates comes from illustrative scenarios, not measured customers. Apply the same discipline as everywhere else in this skill: no before/after baseline, no ROI claim.

### The ROI calculation
**ROI = (Total Value Generated − Total Cost) ÷ Total Cost**

**Costs** (often undercounted — audit for all of these):
- Initial implementation (engineering time, PoC, onboarding)
- Tooling (licenses, cloud usage, subscriptions)
- Enablement (training, docs, internal comms)
- Maintenance overhead (updates, monitoring, compliance, patching)
- Opportunity cost (what didn't get built because the platform did)
- Salary allocation — if engineers spend 50% of time on platform work, count 50% of their comp as platform cost. Calibrate the comp assumption against market reality: North America platform engineers average ~$161K, down year-over-year as the title mainstreams (industry survey, 2025).

**Value** (convert every technical win to a dollar figure):
- *Developer time saved* = hours saved/week × number of developers × hourly rate × 52
- *Faster feature delivery* = estimated revenue impact of shipping X weeks sooner
- *Reduced downtime* = hours of prevented outages × cost per hour of downtime
- *Tool consolidation* = eliminated license/support/maintenance spend

**Worked reference patterns** (use as sanity checks / illustrative benchmarks, not universal targets):
- A small team (~25 developers, 2-person platform team) can plausibly see ~180%+ ROI within ~6 weeks by combining developer-time savings with faster lead time — driven mostly by autonomy and lead-time gains, at fairly low annual cost (order of $200K).
- A larger org (~200 developers, 8-person platform team) can plausibly see ~200%+ ROI mixing cloud-cost savings from standardized provisioning with productivity gains — at meaningfully higher annual cost (order of $1M+), where a large chunk of the value shows up as direct infra savings, not just developer time.
- Treat these as illustrative shapes for how value breaks down (time savings + delivery speed vs. infra savings + productivity), not as numbers to promise a specific org.

### Timeline expectations
Set stakeholder expectations honestly: productivity improvements typically show up within 6–12 weeks of MVP deployment; comprehensive ROI measurement needs 6–12 months of adoption data. Industry pattern: mature orgs allocate roughly 10–20% of engineering capacity to platform work — use this as a sanity check on resourcing, not a target to hit.

### Benchmark calibration table (industry survey, 2025 — context-setting, not targets)
Ground the scorecard's expectations in where the industry actually is:

| Benchmark | Value |
| --- | --- |
| Annual platform budget under $1M | 47.4% of orgs |
| Orgs using DORA metrics to prove success | 40.8% |
| Orgs using time-to-market | 31.0% |
| Orgs using SPACE | 14.1% |
| Orgs that do not measure success at all | 29.6% (down from 45% the prior year) |
| Orgs running more than one platform | 55.9% |
| North America platform engineer salary | ~$161K average (down year-over-year) |
| Platform capacity in mature orgs | ~10–20% of engineering capacity |

How to use these: the salary figure anchors the cost model's salary-allocation line; the budget figure tells you whether the org's ask is in the industry mainstream (nearly half of platform initiatives run under $1M — often underfunded relative to expectations); the "29.6% don't measure" figure is your opener when diagnosing the measurement paradox — not measuring is common, and rapid improvement on it is achievable industry-wide; and multi-platform prevalence (55.9%) means the scorecard may need to cover several platforms, not one.

### The credibility/measurement audit (do this before building the scorecard)
A large share of platform teams report improvement without a real baseline — self-reported "vibes" outrun what's actually been measured. Before producing a scorecard, check for this gap explicitly:
- Ask: "What was the metric before, and what is it now?" If there's no before/after, you don't have an ROI claim yet — you have an anecdote.
- Push for a real experimental setup: baseline observation → statistical comparison → triangulation across at least two frameworks (e.g., DORA + SPACE), not a single number in isolation.
- If no measurement exists yet, don't skip to "let's calculate ROI" — first run a 2–4 week observation phase: pull existing data from CI/CD, ticketing, PR-merge rates, and onboarding metrics, cross-reference them, and find the low-hanging-fruit bottleneck before instrumenting anything new. Spreadsheets are a fine starting tool; don't let tooling be the blocker.

### Adoption as its own signal
Track adoption on an S-curve: slow initial uptake → rapid ramp → saturation. Measure users, voluntary usage (not just mandated usage), features delivered, services migrated. If adoption deviates from the expected S-curve, intervene with workshops/docs/onboarding — and if trust still doesn't follow after intervention, that's a legitimate signal to consider sunsetting the platform rather than forcing adoption. Voluntary usage is a stronger credibility signal than mandate-driven usage — call this out explicitly if the org's adoption is >30% mandate-driven.

## Workflow

1. **Audit measurement maturity first.** Determine if a real baseline exists at [YOUR ORGANIZATION / CLIENT]. If not, scope the deliverable down to "observation plan" rather than "ROI scorecard" and say so.
2. **Map capability-to-outcome chains.** For each funded capability, name the target user behavior, delivery/operational outcome, business outcome, attribution method, and confidence tier. Mark broken arrows as hypotheses.
3. **Select metrics** across the five dimensions (velocity, security, quality, people, cost), explicitly tied to the org's stated business strategy — ask what the business is optimizing for if not stated. Pair every system-derived metric with a survey counterpart per the measurement doctrine — the scorecard needs both views.
4. **Choose the right framework mix** by platform stage: MVP metrics if <3 months old, SPACE + emerging DORA if establishing, full DORA + SPACE if mature — plus the 6-metric AI velocity set if the platform serves AI/ML workloads.
5. **Design the data collection**: a practitioner survey built to the design rules (survey doers not executives, 20–25 minutes max, every 4–6 months, log-scale frequency options) paired with system data pulled via first-party connectors (see below), graded on the three C's. Plan up front to investigate any survey-vs-system divergence as a debugging signal.
6. **Build the ROI calculation**: enumerate every cost category above (don't let the user skip salary allocation or opportunity cost), then convert each value driver to dollars with the formulas above, showing the math. Include capability cost-to-serve and unit economics; sanity-check budget and salary assumptions against the benchmark calibration table.
7. **Add the adoption view**: current position on the S-curve, voluntary vs. mandated %, and an intervention recommendation if off-curve.
8. **Tailor the write-up to audience**: for executives, lead with the dollar ROI number, use external benchmarks, tie to strategic goals (time-to-market, retention), keep it visual and concise. For dev teams, lead with workflow/pain-point improvements and concrete before/after numbers, not dollars.
9. **Output.** A scorecard with: measurement-maturity finding, capability-to-outcome chains, selected metrics + why, the survey + system-data collection plan, the ROI calculation with full cost/value breakdown, adoption S-curve position, and two versions of the summary (exec framing / dev-team framing).

### System-data collection via first-party connectors
When pulling system data, prefer vendor-owned (first-party) MCP servers over hand-built exports — they inherit the org's existing auth and permission trimming. Map scorecard inputs to connectors (examples; the structure is tool-agnostic):
- **PR / commit / deploy metrics** (deployment frequency, lead time, review latency) → GitHub MCP server (repos, pull requests, Actions, deployments), Azure DevOps MCP (repos, PRs, builds), or GitLab MCP (MRs, pipelines — beta, gated behind Premium/Ultimate + Duo licensing).
- **Work-item lead time / backlog health** → Atlassian Remote MCP (Jira, plus Compass service catalog for attribution), Azure DevOps boards, or GitHub issues/projects.
- **Cloud cost** (for the cost side of the ROI model) → managed AWS MCP Server (Cost Explorer and Budgets reachable via call_aws — the strongest first-party cost surface), Azure MCP Server (resource + monitor queries; dedicated cost surface is partial), GCP via BigQuery billing export queried through the Google Cloud MCP servers (indirect).
- **Collaboration / onboarding signals** (meeting load, knowledge silos, who-works-with-whom) → Microsoft Work IQ MCP servers (people graph, Teams/mail semantics — preview, requires eligible Microsoft 365 licensing) or Google Workspace MCP servers (Calendar/Drive/Chat/Gmail — developer preview).

Caveats to state in the scorecard's methodology notes: several of these connectors are preview or license-gated; usage dashboards often lag (~2 days is common), so don't read yesterday's adoption dip as real; users with telemetry disabled are invisible to system data (one more reason surveys are mandatory); and connector availability changes fast — verify at engagement time rather than assuming this list still holds.

## Guardrails
- Never produce a polished ROI number without first checking whether a real baseline exists — surface the measurement gap instead of papering over it.
- Don't let "lines of code" or story points into the scorecard as a legitimate productivity metric.
- Be explicit when illustrative benchmark numbers are being used for shape/pattern rather than as a promised outcome for this specific org.
- Never build the case on system data alone or surveys alone — the measurement doctrine requires both; investigate divergence between them instead of averaging it away.
- Don't survey executives as a proxy for practitioner reality, and don't import vendor case-study or AI-productivity claims as evidence — require a measured before/after baseline.
- Never claim business value from a platform activity metric alone; show the complete capability-to-outcome chain and its attribution confidence.

## Suggested effort
Max — this is a full business-case document, not a single number.
