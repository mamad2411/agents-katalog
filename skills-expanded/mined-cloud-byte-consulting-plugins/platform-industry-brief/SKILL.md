---
name: platform-industry-brief
description: >-
  ALWAYS use this skill when the user asks how platform engineering looks in a
  specific industry or vertical — automotive, mobility, gaming, healthcare,
  logistics, freight, finance, real estate, classifieds, retail, or any other
  sector — or asks for industry benchmarks, "what are peers doing", "state of
  platform engineering", adoption stats, maturity benchmarks, "how do we
  compare to the industry", or a vertical-specific platform or market brief on
  IDPs or AI adoption in engineering orgs. Also fires when a company or
  vertical is named alongside platform strategy questions ("platform
  engineering in automotive", "what does gaming do differently"). Do NOT
  answer these from general knowledge: this skill carries the benchmark
  databank and vertical pattern library needed for a credible,
  industry-contextualized brief. For an org's own metrics/ROI scorecard use
  sibling platform-roi-scorecard; for a scored single-org maturity assessment
  use asdlc-maturity-assessment.
---

# Platform Industry Brief

## Purpose

Produce industry-contextualized platform-engineering briefs. Given a vertical (or a company you can map to a vertical), assemble: (1) the relevant cross-industry benchmarks, (2) the vertical-specific constraints and peer patterns, (3) a maturity/adoption read, and (4) concrete next steps — packaged in a short, decision-ready brief.

This skill is self-contained: the benchmark databank and the vertical pattern library below are the source of truth. Do not go hunting for external reports; do not cite report titles. Attribute numbers generically ("industry survey, 2025" / "industry survey, 2026").

Sibling skills to cross-reference:
- **asdlc-maturity-assessment** — for a structured maturity-level read of the target org.
- **platform-roi-scorecard** — for calibrating metrics/ROI claims against the benchmarks here.
- **platform-security-playbook** — mandatory routing for regulated verticals (healthcare, finance, government).

## Core model

A credible industry brief has three ingredients, and this skill carries all three:

1. **Benchmark databank** — where the industry as a whole actually is (adoption, maturity, budgets, metrics). Use it to anchor claims and to position the target org relative to peers.
2. **Vertical pattern library** — what peer organizations in the target vertical actually did: context, constraint, approach, outcome, transferable lesson. Patterns transfer; company anecdotes alone do not.
3. **AI-native trajectory framing** — where demand is heading (AI-enabled → AI-native, agent swarms), so the brief reads forward, not just backward.

### 1. Benchmark databank

All figures below are from industry surveys of platform engineering practitioners (2025, n≈240–520 depending on question; AI-infrastructure sub-survey n≈110–120). Always note the survey year when citing — benchmarks age fast.

**AI adoption and usage (industry survey, 2025)**
- **89%** of platform practitioners report daily AI usage.
- What AI is used for (multi-select): code generation **74.9%**, documentation **69.7%**, email/messages 55.5%, error analysis 43.6%, infrastructure file generation 42.2%, data analysis 41.7%, ChatOps 22.3%.
- Hype check: **47.3% say AI is over-hyped**, 44.5% appropriately hyped, 8.2% under-hyped. Adoption is near-universal but sentiment is split — quote both sides.
- Timing of major impact: 52% "already happening"; ~71% expect major impact within 12 months.
- **~75%** are hosting or preparing to host AI workloads (39.2% "coming soon", 25.6% "a few", 10.1% "a lot").
- Who owns AI platform responsibilities: platform engineering team **36.7%**, shared across teams 25%, no clear ownership 15%, dedicated AI-infra/MLOps team 11.7%, data science 10%.
- CI/CD for AI artifacts: **41.5% have made no changes yet**; 28.5% extending pipelines for models; 23.1% offering AI blueprints/templates. Implication: model handoffs are largely manual and inference endpoints often sit outside standard governance.
- Top challenges: skill gaps 57.2%, hallucination 55.7%, integration with existing systems 50.7%, data privacy 49.8%, cost 38.3%.
- Governance reality: 69.7% of orgs have AI policies; 16.9% report security teams actively blocking AI. Note the policy–practice gap versus 89% daily usage.

**Maturity distributions (five-dimension platform maturity model, industry survey 2025; YoY = 2024→2025 where available)**
- Investment: dedicated team but primarily reactive **45.5%**; treated as a product with data-driven investment **28.2%**; voluntary/temporary staffing **13.1%**; optimized ecosystem **13.1%** (up from 12.2%).
- Adoption: **extrinsic push/mandate 36.6%** (up from 35.8%); intrinsic user pull 28.2%; participatory (users contribute back) 18.3% (up from 17.3%); **erratic, no coherent strategy 16.9%**.
- Interfaces: standard tooling 43.2%; self-service with high autonomy 31.5%; custom/manual processes 15.0%; seamlessly integrated services 10.3% (up from 9.1%).
- Operations: centrally enabled, user-need-focused 35.7%; centrally tracked 31.9%; ad hoc/by request 18.8%; proactive managed services 13.6% (up from 10.7%).
- Measurement: ad hoc and inconsistent **35.2%** (down from 42.5% — the biggest YoY improvement); insights-driven 25.8%; consistent collection, limited analysis 20.2%; fully integrated quant+qual **18.8%** (up from 10.4%).
- Read: steady incremental progress across all dimensions; measurement improved most; the industry remains far from ecosystem-level maturity. Most orgs land in the middle tiers — position the target org against these modes.

**Metrics and value (industry survey, 2025)**
- Metrics used to prove success: DORA **40.8%**; time to market 31.0%; SPACE 14.1%; **29.6% do not measure at all — down from 45% the prior year**.
- Reported impact: ~61.5% report improvement (35.2% slight + 26.3% significant); 24.2% don't know.
- Time to measurable value: 35.2% within 6 months; **40.9% cannot demonstrate measurable value within 12 months** — a funding-risk benchmark worth flagging in every brief.

**Budgets and structure (industry survey, 2025)**
- Annual platform budget: **47.4% under $1M**; 25.8% $1–5M; 12.2% $5–10M; ~14.5% above $10M. Nearly half of initiatives are underfunded relative to expectations.
- **55.9% of companies run more than one platform** (backend, data/AI, frontend, mobile). Multi-platform is now the norm — frame plurality as intentional design, not fragmentation.
- Reporting lines: Head of Platform Engineering 32.9%; VP/Director Engineering 21.1%; CTO 14.6% — leadership is formalizing but no dominant model exists.
- Product management: ~36.6% have dedicated platform PMs; 25.4% admit to no product mindset at all.

**Governance four-stage model (use to place an org's AI governance)**
1. **Enable experimentation** — sandboxes, clear experiment/production boundaries.
2. **Establish guidelines** — derived from actual usage patterns; principles over rules.
3. **Automate enforcement** — policy-as-code, AI observability, feedback loops.
4. **Continuous evolution** — governance treated as a product with regular reviews.
Contextual distribution: 69.7% have policies (mostly stages 1–2), 16.9% are stuck pre-stage-1 (security blocking), and automated enforcement (stage 3) is rare — the 41.5% "CI/CD untouched by AI" figure is the tell.

### 2. Vertical pattern library

One compact entry per vertical. Each is a **pattern, exemplified by a public case** — present the pattern as the transferable unit, the company as evidence. Never present a single case as the industry norm. New pattern entries are produced from practitioner interviews via the sibling **interview-case-study-writer** skill.

**Automotive / mobility — pattern: platform maturity as strategic-pivot insurance, exemplified by SIXT**
- *Context:* ~800-person product/engineering org building 95%+ of software in-house; decade-long platform investment.
- *Constraint:* legacy monolith deploys took 2–3 weeks; fragmentation across engineering, ops, product; pressure to expand the platform audience from hundreds of developers to thousands of citizen developers and, eventually, agents.
- *Approach:* centralize common foundations (observability, build, deployment, app frameworks) while extending team ownership; for AI: "deterministic harnesses around probabilistic systems" — standards injected at the source, a platform agent reviewing code at deploy time, multi-model verification (one model catches what another misses), and shared context exposing all apps/APIs/async flows so models can reason about system-wide impact.
- *Outcome:* 120,000–130,000 deployments/month across thousands of applications; launched an entirely new subscription business in a couple of months during a market shock — estimated 2–3x faster than without the platform.
- *Transferable lesson:* platform maturity compounds into strategic agility; design for three audiences (developers, citizen developers, agents) on shared security/observability foundations.

**Gaming — pattern: capacity contingency plus data-driven work categorization, exemplified by Demonware (Activision Blizzard)**
- *Context:* online services for 60M+ players; hybrid estate of private data centers, public cloud, dedicated game servers; petabytes of telemetry.
- *Constraint:* launch traffic can miss forecasts by orders of magnitude; constant DDoS attacks; zero downtime tolerance; failure is immediately public.
- *Approach:* rigorous capacity and contingency planning ("plan 80%, the 20% execution should be the easy part") built from incident history; systematic work categorization (KTLO vs feature vs tech debt); internal developer portal treated as a data platform first, interface second, with AI summarization layered on validated data.
- *Outcome:* one team measured at 80–90% KTLO was rebalanced to ~40% within months through process fixes — not headcount.
- *Transferable lesson:* measure work types before hiring ("it's rarely a headcount issue"); an IDP is only as useful as the accuracy of its underlying data.

**Real estate / classifieds — pattern: valuation-aligned platform strategy in M&A-heavy groups, exemplified by Aviv Group**
- *Context:* group of similar-sized classifieds brands across markets, formed by repeated acquisitions; leadership experience spanning comparable group environments.
- *Constraint:* no dominant technical standard to converge on; acquisitions and divestments can happen within the same two-year window; a divested brand must become independent in 12–24 months.
- *Approach:* align architecture with the business valuation model — growth-valued companies optimize for integration speed and accept duplication; EBITDA-valued companies can consolidate but must price in future decoupling. Build platform services as potentially licensable products; accept strategic redundancy; separate infrastructure from code ownership for two-step separations; maintain a connected data graph linking source code, infra, and cloud cost to revenue and EBITDA.
- *Outcome:* divestment readiness by design rather than crisis; over-investment avoided by starting from business goals ("the most influential architecture decisions were deciding not to do something").
- *Transferable lesson:* platform strategy is a function of corporate strategy — revisit the valuation alignment every 6–12 months.

**Healthcare — pattern: platform as the escape from walled-garden compliance (practitioner interview; vendor-affiliated perspective — weigh accordingly)**
- *Context:* the most regulated, data-heavy vertical; decades of "secure by design" culture; hard regulatory deadlines (e.g., 72-hour prior-authorization processing rules).
- *Constraint:* security implemented as siloed control gates ("throwing things over the wall department to department") rather than integrated workflows; deep vendor lock-in to EHR/claims suites erodes sovereignty; keeping the lights on consumes nearly all capacity.
- *Approach:* platform engineering as the prescription for integrated secure-by-design workflows; GenAI targeted first at back-office data toil (format translation, ETL, legacy data extraction) rather than clinical front lines; modular pipelines of small specialized agents with adversarial/verification agents checking output quality; sovereignty preserved by demanding opt-outs from vendor-bundled AI ("make sure we can turn it off") and hybrid/portable infrastructure.
- *Outcome:* pockets of innovation concentrated where data toil is worst; human-in-the-loop retained for clinical decisions.
- *Transferable lesson:* in regulated verticals the unglamorous data layer is the AI beachhead, and sovereignty (exit-ability, data control) is a first-class platform requirement. Route any healthcare brief through **platform-security-playbook**.

**Freight / logistics — pattern: AI agents as the workforce that finally makes process excellence real, exemplified by practitioners from Forto (now building Zauber)**
- *Context:* freight forwarding moves ~80% of physical goods (~9–10% of GDP) yet runs on email, Excel, and heroic exception handling; fragmented multi-party chains where no forwarder owns the full asset chain.
- *Constraint:* uniquely hostile to rigid automation — constant exceptions (rerouted vessels, customs inspections, schedule changes); legacy transport systems with API gatekeeping (per-call pricing that kills integration); processes documented on paper but executed idiosyncratically per clerk.
- *Approach:* human-orchestrator "control tower" model — agents autonomously handle discrete high-volume steps (quoting, order validation, document checks, data entry) and escalate exceptions to humans; GenAI as the on-ramp to clean operational data (AI enters/cleans data from emails, replacing rule-based ETL).
- *Outcome:* on small-to-mid tasks, agent error margins reported ~5–10x lower than human; humans shift to judgment-heavy exception handling and customer relationships.
- *Transferable lesson:* once AI is the workforce, the process definition becomes load-bearing — organizations with real process excellence transform fastest; API-hostile incumbency is now an existential liability.

**Regulated finance — pattern: golden paths as compliance artifacts (composite pattern — synthesized from regulated-vertical principles, not a single named case)**
- *Context:* banking/insurance share healthcare's guardrail culture: model risk management, auditability, data residency, regulator-facing explainability.
- *Constraint:* every AI artifact (model, dataset, inference endpoint) must be traceable — which data trained which model for which application; security teams default to blocking (the 16.9% benchmark skews higher here).
- *Approach:* encode compliance into the paved road: policy-as-code scanning AI-generated code, context isolation (AI experimentation inside scoped environments with pre-approved credentials and data), versioned datasets with lineage metadata, audit trails as a platform service, and the four-stage governance model to move from blanket prohibition to automated enforcement.
- *Outcome/lesson:* the safest path must be the easiest path; finance briefs should always pair benchmark positioning with a governance-stage read and route to **platform-security-playbook**.

### 3. AI-native trajectory framing

Use this to give every brief a forward-looking arc.

- **AI-enabled vs AI-native.** AI-enabled = AI tools inside existing workflows (coding copilots, chat interfaces) — where ~89% of orgs are today. AI-native = models, datasets, and inference endpoints treated as versioned, containerized platform services deployed through CI/CD with full lineage; governance, data, and compute as first-class concerns from day one. The difference is architectural, not tool adoption. Benchmark the gap: 89% daily usage vs 41.5% with CI/CD untouched by AI.
- **Agent-swarm taxonomy (demand-forecasting lens for platform capacity).** AI-native experiences are powered by swarms of specialized agents, not one model. Four interaction classes: **brand-to-agent** (the business defines agent behavior, permissions, optimization targets), **agent-to-agent** (agents composing — one summarizes history, another optimizes the offer), **agent-to-employee** (generated staff guidance/talk tracks), **agent-to-customer** (direct customer-facing interaction). Use the taxonomy to forecast platform demand: each class multiplies inference traffic, identity/permission permutations, and observability surface. Capacity planning should count agent classes and interaction volume, not just human seats.
- **Illustrative case — flag as hypothetical.** A widely circulated hospitality vignette (late check-in, agents upselling dinner, car service, and wine to double a night's room revenue from $400 to $800) is a **hypothetical illustration from vendor-commissioned material, not measured data** — usable to explain the swarm taxonomy, never as an outcome claim. A related velocity claim (40+ agentic workflows built in 3 weeks of hackathons on a pre-built composable stack) is directional evidence for "platform first, agents fast," similarly to be flagged as vendor-reported.
- **Infrastructure implications:** governed data foundation (versioned, lineage-tagged datasets), accelerated compute with scale-to-zero economics (don't pay for idle GPUs at 3 AM), and production orchestration (models as deployable artifacts on golden paths). Avoid the "mainframe anti-pattern": one centralized GPU cluster with global teams queueing for time.

## Workflow

1. **Intake.** Establish: vertical (or map the named company to one), company size/engineering headcount, regulatory exposure (none / moderate / heavy), current platform status (none / early / established), and what decision the brief should support. Ask only for what's missing; make stated assumptions explicit. Default target org: [YOUR ORGANIZATION / CLIENT].
2. **Select benchmarks.** Pull only the databank rows relevant to the question (adoption stats for an AI brief; maturity + budget rows for an investment brief). Always attach the survey year. Position the target org against the modal answer, not the best-in-class tail.
3. **Match vertical patterns.** Lead with the target vertical's pattern entry. Add 1–2 adjacent patterns when they transfer (e.g., gaming's capacity discipline for any spiky-traffic business; classifieds' valuation alignment for any M&A-active group). State each as pattern-first: "peer pattern: X, exemplified by Y."
4. **Maturity/adoption read.** Place the org on the five maturity dimensions and the four-stage governance model using the distributions above. For a rigorous assessment, invoke **asdlc-maturity-assessment**; for benchmark-calibrated ROI/metrics claims, invoke **platform-roi-scorecard**.
5. **Risks and watchouts.** Standard set: measurement gap (29.6% don't measure — is this org one of them?), funding risk (40.9% can't show value in 12 months), mandate-driven adoption fragility (36.6%), governance stage mismatch, and vertical-specific constraints from the pattern entry. Regulated verticals: route to **platform-security-playbook**.
6. **Write the brief** using the output template:
   - **TL;DR** — 3–5 bullets: where the industry is, where this org sits, the one move that matters most.
   - **Where the industry is** — benchmark positioning with survey years.
   - **What peers do** — vertical pattern(s), context → constraint → approach → outcome → lesson.
   - **What to do next** — 3–5 prioritized, org-specific actions tied to the maturity read.
   - **Benchmark appendix** — the exact figures cited, each with "industry survey, 2025/2026" attribution.

## Guardrails

- **Mark hypothetical and vendor-sponsored material as such.** The hospitality vignette is hypothetical; the healthcare perspective is vendor-affiliated; velocity claims from commissioned material are vendor-reported. Say so inline.
- **Never present a single case as an industry norm.** One company is an existence proof, not a distribution. Pattern first, exemplar second.
- **Benchmarks age.** Every figure carries its survey year; when a brief is written more than ~18 months after the survey, say the numbers are dated and directional.
- **No source-report name-dropping.** Attribution is always generic ("industry survey, 2025"). Named companies in the pattern library are fine — they are public case studies.
- **Regulated verticals route to platform-security-playbook.** Healthcare, finance, government: the brief is incomplete without the security/compliance overlay.
- **Don't invent vertical data.** If the target vertical has no pattern entry, say so, use the nearest adjacent pattern with an explicit transfer argument, and rely more heavily on cross-industry benchmarks.

## Suggested effort

- **Quick positioning answer** ("how does our vertical compare?"): benchmarks + one pattern entry, ~300 words, no intake beyond the vertical.
- **Standard brief** (default): full workflow, 1–2 pages, 30–60 minutes equivalent effort, template structure above.
- **Deep brief** (board/investment decision): full workflow plus sibling-skill invocations (maturity assessment + ROI scorecard), risks quantified against benchmarks, 3–5 pages.
- When in doubt, ship the standard brief and offer the deep version as a follow-up.
