---
name: new-product-development
version: 4.0
description: >
  Expert orchestration system for complex product development across any industry domain.
  Applies a 5-layer framework: core NPD lifecycle + domain overlays + capability modules +
  decision frameworks + reusable templates. Use for any product type — software, hardware,
  connected device, regulated system, or platform. Triggers on: product ideation, concept
  validation, business case, architecture design, prototyping, market testing, launch
  planning, pilot governance, fleet operations, post-launch review. Automatically detects
  domain (IoT, Healthcare, FinTech, Retail, AgriTech, EdTech, Logistics, Energy, PropTech,
  GovTech), product type, lifecycle stage, and capability lens — then routes to the minimum
  necessary reference set. Use this skill whenever anyone mentions building, launching,
  scaling, or operating any product of any kind.
---

# New Product Development — V4
## Expert Orchestration System

This is a **5-layer execution framework**, not a reference library. Claude acts as an
expert orchestrator that routes every conversation to the right reference set, applies
the right frameworks, and produces consistent high-quality deliverables.

---

## Layer Architecture

```
┌─────────────────────────────────────────────────────┐
│  LAYER 1: SKILL.md — Master Orchestrator            │
│  Routing logic · Stage gates · Delivery model       │
├─────────────────────────────────────────────────────┤
│  LAYER 2: Core Lifecycle References                 │
│  concept-testing · business-analysis · launch       │
├─────────────────────────────────────────────────────┤
│  LAYER 3: Domain Overlays (load one when detected)  │
│  10 industry domains · standardised structure       │
├─────────────────────────────────────────────────────┤
│  LAYER 4: Capability Modules (cross-cutting)        │
│  8 engineering / operating patterns                 │
├─────────────────────────────────────────────────────┤
│  LAYER 5: Decision Frameworks + Templates           │
│  6 frameworks · 8 templates                         │
└─────────────────────────────────────────────────────┘
```

---

## Routing Logic — Claude Must Execute This First

Before responding to any product-related request, determine four dimensions:

### Dimension 1 — Product Type
| Signal in conversation | Product type | Implications |
|---|---|---|
| Web app, SaaS, API, mobile app | Software-only | Cloud architecture depth |
| Device, hardware, sensor, enclosure | Physical device | Device engineering capability |
| Connected device, telemetry, edge | Connected device | Connectivity + edge + firmware |
| FDA, CE, clinical, regulated | Regulated system | Compliance-first at every gate |
| Platform, marketplace, OS | Platform product | Multi-tenant, ecosystem design |

### Dimension 2 — Domain
| Keywords | Domain file to load |
|---|---|
| manufacturing, shop floor, SCADA, OPC UA, Modbus, field device, industrial | `domains/iot-manufacturing.md` |
| HIPAA, patient, clinical, EHR, FDA, medical device, HL7, FHIR | `domains/healthcare-medtech.md` |
| payments, KYC, AML, lending, insurance, PCI, banking, wallet, fintech | `domains/fintech-banking.md` |
| e-commerce, POS, inventory, omnichannel, retail, SKU, merchandising | `domains/retail-ecommerce.md` |
| farming, crop, soil, irrigation, drone, harvest, livestock, precision agriculture | `domains/agritech-food.md` |
| LMS, learning, curriculum, assessment, student, SCORM, xAPI, EdTech | `domains/edtech-learning.md` |
| fleet, last-mile, warehouse, shipment, freight, route, supply chain | `domains/logistics-supplychain.md` |
| grid, solar, wind, EV charging, smart meter, SCADA energy, microgrid | `domains/energy-cleantech.md` |
| building, tenant, BMS, smart building, property, lease, facility | `domains/real-estate-proptech.md` |
| smart city, citizen, government, e-governance, public sector, GovTech | `domains/government-smartcity.md` |

### Dimension 3 — Lifecycle Stage
| Stage | Gate focus |
|---|---|
| Ideation / screening | Problem validation, feasibility, strategic fit |
| Concept / validation | User desirability, technical PoC, willingness to pay |
| Business case | Financial model, market sizing, risk |
| Prototype / build | Architecture, engineering execution, security |
| Pilot / field trial | Real-world validation, operational readiness |
| Launch | GTM, readiness checklist, go/no-go |
| Scale / operate | Fleet ops, cost optimisation, iteration |

### Dimension 4 — Capability Lens
Load the relevant capability module when the conversation touches these topics:

| Topic | Capability file |
|---|---|
| Hardware design, ruggedisation, battery, ergonomics | `capabilities/device-engineering.md` |
| Firmware, edge runtime, offline behaviour, OTA | `capabilities/firmware-edge-runtime.md` |
| Machine protocols, connectivity, tag mapping | `capabilities/industrial-connectivity.md` |
| Telemetry schema, event model, time-series | `capabilities/telemetry-data-contracts.md` |
| OT/IT security, network zones, device identity | `capabilities/ot-it-security.md` |
| Fleet provisioning, remote ops, OTA rollout | `capabilities/fleet-operations.md` |
| Reliability testing, validation, field acceptance | `capabilities/reliability-validation.md` |
| Support model, L1/L2/L3, RMA, installer ops | `capabilities/support-operating-model.md` |

### Routing Rules
1. **Always** apply core lifecycle framework (Layer 2)
2. **If domain detected**: load the matching domain overlay (Layer 3)
3. **If capability topic detected**: load matching capability module(s) (Layer 4)
4. **If decision required**: apply the relevant decision framework (Layer 5)
5. **For deliverables**: use the matching template (Layer 5)
6. **Never load all files** — progressive disclosure only; load what the conversation needs

---

## Core NPD Lifecycle — 8 Stage-Gated Phases

Each stage has: goal · business track · technical track · domain additions (from overlay) ·
capability additions (from module) · deliverable · gate criteria.

---

### Stage 1 — Idea Generation

**Goal**: Produce a documented set of product ideas from validated sources.

**Business track**:
- Jobs-to-be-Done (JTBD) interviews: identify functional, emotional, social jobs
- Pain / gain mapping per customer segment
- Competitive landscape scan: feature gaps, pricing gaps, underserved segments
- Internal opportunity mapping: what can the organisation uniquely build?
- Analogous market research: what solved this problem in adjacent industries?

**Technical track**:
- Engineering-led ideation: internal tools → external products
- Open-source gap analysis: what does the developer / operator community lack?
- AI/ML opportunity scan: where does prediction, classification, or generation add value?
- Platform thinking: what infrastructure asset can become a product surface?
- Technical debt audit: what friction points in existing systems create product opportunity?

**Deliverable**: Idea backlog — each entry includes: source, problem statement,
target user, rough technical feasibility, and strategic alignment score

**Gate**: Minimum 5 distinct ideas documented with rationale before proceeding

---

### Stage 2 — Idea Screening

**Goal**: Apply structured criteria to converge on 1–3 investable ideas.

**Business track**:
- Scoring matrix dimensions: strategic fit (1–5) · market size (1–5) ·
  competitive advantage (1–5) · organisational capability (1–5) · time to value (1–5)
- SWOT per shortlisted idea
- Stakeholder alignment check: who internally champions, who blocks?
- Assumptions register: list the top 5 assumptions that could invalidate each idea

**Technical track**:
- Build vs. buy vs. partner decision (see `decision-frameworks/build-buy-partner.md`)
- Technology readiness level (TRL) assessment per idea
- Stack and skills gap analysis: what is missing from the current team?
- Integration complexity estimate: how many external systems must connect?
- Regulatory pre-check: which compliance regimes apply? What is the entry cost?
- OSS dependency audit: licence risk, community health, maintenance trajectory

**Deliverable**: Ranked shortlist (top 1–3 ideas) with scoring matrix, assumptions
register, and preliminary technical feasibility note

**Gate**: Winning idea scores ≥ 3.5/5 across all matrix dimensions;
no unresolvable technical blockers identified

---

### Stage 3 — Concept Development & Testing

**Goal**: Validate that target users want the concept AND that core technical
assumptions hold — before committing engineering resources.

**Business track**:
- Concept statement: problem · proposed solution · target user · key benefit · differentiator
- Develop 2–3 concept variants (avoid single-option anchoring)
- Validation method selection (see `references/concept-testing.md`):
  - Qualitative: user interviews, focus groups, contextual inquiry
  - Quantitative: concept survey, A/B landing page, smoke test / fake door
  - Behavioural: Wizard of Oz prototype, concierge MVP
- Willingness-to-pay: Van Westendorp Price Sensitivity Meter or Gabor-Granger
- Assumption testing: rank assumptions by risk; design tests to invalidate highest-risk ones

**Technical track**:
- Time-boxed technical spike / PoC (2–5 days): validate the single riskiest
  technical assumption — not a full prototype
- API and integration discovery: what does each integration surface expose?
  What are the data models, rate limits, authentication patterns?
- Data availability audit: for ML/AI products — is labelled training data accessible?
  What is the data quality? Who owns it?
- Architecture sketch: document the candidate architecture patterns with trade-offs;
  do not commit yet — this is hypothesis, not decision
- Security and privacy pre-check: where is PII created, stored, transmitted?
  What attack surface does this concept introduce?

**Deliverable**: Validated concept brief + PoC findings report + assumption test results +
initial architecture sketch with trade-off notes

**Gate**: ≥ 60% purchase intent from target users in concept test;
PoC validates or credibly refines the core technical assumption;
top 3 assumptions tested and addressed

> See `references/concept-testing.md` for validation method selection guide

---

### Stage 4 — Business Analysis

**Goal**: Build the financial, strategic, and technical investment case.

**Business track**:
- Market sizing: TAM → SAM → SOM with methodology documented
  (top-down from research reports + bottom-up from unit economics)
- Revenue model design: subscription · usage-based · transaction · licensing ·
  freemium · marketplace — model 3-year P&L for each viable option
- Pricing strategy: cost-plus baseline · competitive anchor · value-based ceiling;
  segment-specific pricing if applicable
- Customer acquisition model: CAC by channel, LTV by segment, LTV:CAC ratio target
- Break-even analysis and payback period
- Sensitivity analysis: what happens to ROI if key assumptions are wrong by ±20%?
- Risk register: technical · market · regulatory · competitive · operational risks;
  rated by likelihood × impact; mitigation per risk

**Technical track**:
- Cloud cost model: compute · storage · networking · managed services · API calls
  at P50, P90, and peak load — model 3 scenarios (conservative / base / aggressive)
- LLM / AI cost engineering (if applicable): tokens per query · monthly query volume ·
  model unit cost · caching hit rate → monthly LLM spend; model vs. model comparison
- Infrastructure build vs. managed service TCO: self-hosted vs. cloud-managed
  over 3-year horizon
- Security and compliance cost: certification (SOC 2, ISO 27001), pen testing,
  legal review, ongoing compliance tooling
- Engineering team sizing: roles · seniority · duration · cost; include QA,
  DevOps, security — not just feature engineers
- Technical debt budget: what % of engineering capacity reserved for debt servicing?

**Deliverable**: Business case document (see `templates/prd-template.md` for structure) +
cloud cost model + engineering resource plan + risk register

**Gate**: ROI meets organisational threshold; LTV:CAC ≥ 3x; cloud costs sustainable at
projected scale; no unmitigated high-severity risks

> See `references/business-analysis.md` for financial model templates

---

### Stage 5 — Product Development / Prototyping

**Goal**: Build a production-quality MVP using engineering best practices from day one.

**Business track**:
- MVP scope definition via MoSCoW: Must / Should / Could / Won't
- RICE prioritisation for backlog: Reach × Impact × Confidence ÷ Effort
- Agile cadence: 2-week sprints; definition of done; sprint review with stakeholders
- Usability testing at each sprint milestone; incorporate findings into next sprint
- Acceptance criteria defined per user story before engineering begins

**Technical track — Architecture & System Design**:
- Architecture Decision Records (ADRs): document every major technology choice
  with context, options considered, decision, and consequences
- Cloud reference architecture selection:
  - SaaS / web: multi-tenant app tier + managed DB + CDN + WAF + auth layer
  - AI / LLM product: LLM gateway + RAG pipeline + vector DB + caching + eval layer
  - Data platform: ingestion + lakehouse + transformation + serving + governance
  - API / developer product: API gateway + microservices + service mesh + rate limiting
  - Edge / connected product: edge runtime + local storage + sync + fleet mgmt
- Database selection and justification:
  - OLTP: PostgreSQL, MySQL, Cloud Spanner — for transactional workloads
  - OLAP: BigQuery, Snowflake, Redshift — for analytics
  - Vector: Pinecone, Weaviate, pgvector, Qdrant — for semantic search / RAG
  - Time-series: InfluxDB, TimescaleDB, QuestDB — for telemetry and IoT
  - NoSQL: MongoDB, DynamoDB, Firestore — for flexible schema workloads
- Scalability design: stateless services · horizontal autoscaling · Redis caching ·
  CDN for static assets · async processing via message queue (SQS, Pub/Sub, Kafka)
- Multi-tenancy model: document trade-offs between shared schema · schema-per-tenant ·
  DB-per-tenant across cost, isolation, operational complexity, and compliance

**Technical track — AI / LLM Engineering (where applicable)**:
- LLM selection rubric: quality · latency · cost · context window · privacy ·
  fine-tuning availability · rate limits
- RAG pipeline design:
  - Ingestion: document parsing · chunking strategy (fixed / semantic / hierarchical) ·
    metadata extraction · deduplication
  - Indexing: embedding model selection · vector store configuration · hybrid index
    (dense + sparse) for better recall
  - Retrieval: semantic search · keyword fallback · query expansion ·
    re-ranking with cross-encoder
  - Generation: context assembly · prompt construction · output parsing ·
    citation tracking
- LLMOps:
  - Prompt version control: treat prompts as code; review + staging + production
  - Experiment tracking: A/B test prompt variants; statistical significance threshold
  - Observability: trace every LLM call — input, output, tokens, latency, cost,
    model version, prompt version, retrieval quality
  - Fallback chain: primary model → fallback model → graceful degradation response
  - Guardrails: input validation · output safety filters · PII detection and redaction
- Evaluation framework:
  - Define metrics before building: faithfulness · answer relevance · context recall ·
    context precision · latency · cost per query
  - Golden dataset: curate 50–200 representative queries with ideal responses
  - Automated eval pipeline: run on every prompt version change
  - Human eval: periodic review of production samples by domain experts

**Technical track — DevSecOps**:
- CI/CD pipeline: commit → lint + SAST → unit tests → build → integration tests →
  staging deploy → smoke tests → production deploy
- Infrastructure as Code: all cloud resources in Terraform or Pulumi;
  all Kubernetes workloads in Helm; no manual configuration of production systems
- Environment strategy: local → dev → staging → production;
  feature flags decouple deployment from release
- Secrets management: Vault / AWS Secrets Manager / GCP Secret Manager;
  zero hardcoded secrets; rotation policy defined
- Security in CI: SAST (Semgrep, Snyk) · dependency scanning · container image
  scanning · IaC security linting (tfsec, checkov)
- Testing pyramid: unit (>80% business logic coverage) · integration · contract ·
  end-to-end · load (k6, Locust) · chaos (optional, pre-launch)
- Zero-trust IAM: principle of least privilege; service accounts per workload;
  no wildcard permissions; access reviewed quarterly

**Technical track — Observability**:
- Structured logging: JSON format; correlation IDs across services; log levels enforced
- Metrics: system (CPU, memory, latency, error rate, saturation) + business
  (DAU, conversion, feature adoption, revenue) via Prometheus + Grafana or Datadog
- Distributed tracing: OpenTelemetry instrumentation across all services; Jaeger or
  Datadog APM for visualisation
- SLIs and SLOs: define before launch; error budget per rolling 30-day window
- Alerting: alert on symptoms (user-facing) not causes (internal);
  runbook for every alert; PagerDuty / OpsGenie for on-call routing

**Deliverable**: Working MVP + ADR log + CI/CD pipeline live + observability configured +
security baseline met + eval suite passing (for AI products) + load test completed

**Gate**: All acceptance criteria met; zero critical security findings; observability live;
load test passed at 2× expected peak; ADRs documented

---

### Stage 6 — Pilot / Field Trial

**Goal**: Validate the product with real users in real operating conditions before
committing to full launch.

**Business track**:
- Pilot charter: scope · success metrics · timeline · site/cohort selection criteria ·
  responsibilities · exit criteria (see `templates/pilot-charter-template.md`)
- Pilot site / cohort selection: representative but not maximum complexity;
  willing and cooperative stakeholders; accessible for rapid iteration
- Structured feedback collection: weekly check-ins · NPS · feature-specific surveys ·
  session observation
- Commercial signal collection: would they pay? Would they expand? Would they refer?

**Technical track**:
- Canary deployment: 1% → 5% → 25% → 50% → 100% with automated rollback trigger
- Feature flag governance: pilot cohort enabled; kill-switch tested before go-live
- Real-load performance monitoring: p50 / p95 / p99 latency with real traffic
- Cost validation: actual usage vs. cost model; identify unexpected cost drivers
- Security penetration test: run before full launch; findings triaged and resolved
- Data pipeline validation: confirm event capture accuracy; validate analytics
  data quality before making decisions from it
- Operational readiness: on-call rota active; runbooks tested; escalation paths clear
- Pilot acceptance criteria: define quantitative thresholds for proceeding

**Deliverable**: Pilot report (see `templates/post-pilot-review-template.md`) including
performance benchmark · cost validation · security sign-off · commercial signal summary

**Gate**: Pilot acceptance criteria met; error rate below defined threshold;
cost per unit within model; security pen test passed; positive commercial signals

> See `decision-frameworks/pilot-readiness.md` for readiness assessment

---

### Stage 7 — Commercialisation / Launch

**Goal**: Bring the product to market with a fully coordinated, reversible launch plan.

**Business track**:
- GTM strategy: positioning statement · messaging hierarchy · channel mix ·
  pricing and packaging finalised · launch motion (product-led / sales-led / partner-led)
- Sales and support enablement: battlecard · demo environment · objection handling ·
  competitive positioning · support knowledge base
- Launch type selection: soft launch · phased rollout · big bang ·
  beta → GA (see `decision-frameworks/launch-readiness.md`)
- PR and demand generation: press kit · launch blog post · social content calendar ·
  analyst briefings · community seeding

**Technical track — Launch Checklist**:

Infrastructure:
- [ ] Auto-scaling configured and load-tested at 3× expected peak
- [ ] Rollback plan documented, rehearsed, executable in < 15 minutes
- [ ] Status page live and linked from product
- [ ] On-call rota active with defined escalation chain
- [ ] Rate limiting and DDoS protection active
- [ ] All secrets rotated; IAM permissions audited and tightened
- [ ] Data backup tested; recovery time and point objectives met

Security:
- [ ] Penetration test completed; critical and high findings resolved
- [ ] GDPR / DPDP / applicable data privacy compliance verified
- [ ] Data processing agreements signed with all subprocessors
- [ ] Vulnerability disclosure policy published

AI / LLM (if applicable):
- [ ] Prompt versions locked and tagged in version control
- [ ] Fallback model configured and tested end-to-end
- [ ] Per-user spend limits enforced
- [ ] Safety and moderation layer active
- [ ] LLM cost monitoring alerts configured

Developer / API products:
- [ ] OpenAPI spec published and versioned
- [ ] Getting-started guide: < 5 minutes to first successful API call
- [ ] SDK published to relevant package registries
- [ ] Changelog and deprecation policy live

**Deliverable**: GTM plan (see `templates/gtm-industrial-template.md`) + signed-off
technical launch checklist + runbook library + documentation published

**Gate**: All cross-functional teams ready; technical checklist 100% complete;
rollback plan tested; go/no-go formally recorded

> See `references/launch-planning.md` for GTM templates
> See `decision-frameworks/launch-readiness.md` for readiness scoring

---

### Stage 8 — Post-Launch Review & Iteration

**Goal**: Measure outcomes, reduce technical risk, and plan the next cycle with evidence.

**Business track**:
- KPI review vs. targets: revenue · activation · retention · NPS · feature adoption · churn
- Win/loss analysis: why are customers choosing or not choosing this product?
- Qualitative feedback synthesis: customer interviews · support ticket analysis ·
  sales call recordings
- Backlog prioritisation for v2: RICE scoring on incoming requests vs. strategic bets

**Technical track**:
- DORA metrics baseline (industry standard for engineering performance):
  - Deployment frequency — elite: multiple per day
  - Lead time for changes — elite: < 1 hour commit to production
  - Mean time to restore — elite: < 1 hour after incident
  - Change failure rate — elite: < 5% of deployments cause incidents
- AI / LLM performance review:
  - Monthly: cost per query trend · eval score trends · retrieval quality
  - Quarterly: model re-evaluation — is a newer or cheaper model now better?
  - Monitor for distribution shift: production query patterns drifting from golden dataset
- Technical debt review:
  - Document all shortcuts taken during build and pilot
  - Classify: critical (fix immediately) · high (next sprint) · medium (next quarter)
  - Architecture review: does the design hold at 3× current scale?
- Security posture review:
  - Audit all security alerts and incidents from launch period
  - Schedule next penetration test (minimum annually)
  - Rotate credentials; review third-party access grants
- FinOps review:
  - Identify top 3 cost drivers; set reduction targets with owners
  - Evaluate reserved instance or committed use discount opportunities
  - Right-size idle or underutilised resources

**Deliverable**: Post-launch review report + DORA metrics baseline + technical debt
register with priority classification + cost optimisation plan + v2 roadmap

---

## Stage Summary Table

| Stage | Business Deliverable | Technical Deliverable | Gate Criteria |
|---|---|---|---|
| 1. Idea Generation | Idea backlog | Feasibility notes | 5+ ideas with rationale |
| 2. Idea Screening | Ranked shortlist + assumptions | TRL + build/buy/integrate | ≥3.5/5 score; no blockers |
| 3. Concept Testing | Validated concept brief | PoC report + arch sketch | ≥60% intent; PoC validates |
| 4. Business Analysis | Business case + risk register | Cost model + team plan | ROI threshold; LTV:CAC≥3x |
| 5. Prototyping | Working MVP | ADRs + CI/CD + obs + security | All criteria; load test pass |
| 6. Pilot | Pilot report + commercial signals | Perf + cost + security | Pilot criteria met |
| 7. Launch | GTM plan | Technical checklist 100% | All teams + checklist done |
| 8. Post-Launch | Review + v2 roadmap | DORA + debt register + FinOps | Shipped; cycle planned |

---

## Deliverables Claude Can Generate

**Business / Product**:
- Idea scoring matrix
- Concept brief / one-pager
- Business case with financial model
- Product roadmap
- GTM plan
- PRD (using `templates/prd-template.md`)
- Pilot charter (using `templates/pilot-charter-template.md`)
- Post-launch review report

**Technical / Engineering**:
- System architecture diagram + ADR log
- Cloud cost model and infrastructure sizing
- LLM/RAG pipeline design + evaluation framework
- Threat model (using `templates/threat-model-template.md`)
- Observability strategy: SLIs, SLOs, alerting runbooks
- CI/CD pipeline design
- Technical launch readiness checklist
- DORA metrics baseline + engineering health report
- LLM cost engineering model
- API reference and developer getting-started guide
- Telemetry schema (using `templates/telemetry-schema-template.md`)
- Validation matrix (using `templates/validation-matrix-template.md`)

---

## Framework Selection Guide

| Situation | Framework / Reference |
|---|---|
| Validating user need | JTBD, Customer Journey Map, Assumption Testing |
| Sizing the market | TAM/SAM/SOM — top-down + bottom-up |
| Prioritising features | MoSCoW, RICE scoring |
| Architecture decisions | ADR template, Well-Architected Framework |
| Protocol selection | `decision-frameworks/protocol-selection.md` |
| Edge vs. cloud partitioning | `decision-frameworks/edge-vs-cloud-partitioning.md` |
| Build vs. buy vs. partner | `decision-frameworks/build-buy-partner.md` |
| Pilot readiness | `decision-frameworks/pilot-readiness.md` |
| Launch readiness | `decision-frameworks/launch-readiness.md` |
| Security design trade-offs | `decision-frameworks/security-design-tradeoffs.md` |
| Engineering performance | DORA Metrics |
| Security posture | OWASP Top 10, Zero Trust, STRIDE |
| Cost optimisation | FinOps framework |

---

## Full Reference Map

**Layer 2 — Core lifecycle**:
- `references/concept-testing.md`
- `references/business-analysis.md`
- `references/launch-planning.md`

**Layer 3 — Domain overlays** (`references/domains/`):
- `iot-manufacturing.md` · `healthcare-medtech.md` · `fintech-banking.md`
- `retail-ecommerce.md` · `agritech-food.md` · `edtech-learning.md`
- `logistics-supplychain.md` · `energy-cleantech.md`
- `real-estate-proptech.md` · `government-smartcity.md`

**Layer 4 — Capability modules** (`references/capabilities/`):
- `device-engineering.md` · `firmware-edge-runtime.md`
- `industrial-connectivity.md` · `telemetry-data-contracts.md`
- `ot-it-security.md` · `fleet-operations.md`
- `reliability-validation.md` · `support-operating-model.md`

**Layer 5a — Decision frameworks** (`references/decision-frameworks/`):
- `protocol-selection.md` · `edge-vs-cloud-partitioning.md`
- `build-buy-partner.md` · `pilot-readiness.md`
- `launch-readiness.md` · `security-design-tradeoffs.md`

**Layer 5b — Templates** (`references/templates/`):
- `prd-template.md` · `factory-discovery-template.md`
- `pilot-charter-template.md` · `telemetry-schema-template.md`
- `threat-model-template.md` · `validation-matrix-template.md`
- `gtm-industrial-template.md` · `post-pilot-review-template.md`
