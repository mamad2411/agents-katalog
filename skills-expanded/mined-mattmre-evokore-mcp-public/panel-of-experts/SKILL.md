---
name: panel-of-experts
description: Multi-persona expert panel framework for critical analysis, refinement, and creative insight
aliases: [expert-panel, panel-review, expert-review, panel, experts]
category: orchestration
tags: [review, analysis, refinement, multi-perspective, critical-thinking, quality]
version: 1.0.0
resolutionHints:
  - expert review or panel discussion
  - multi-perspective analysis
  - critical code or architecture review
  - repo ingestion quality check
  - phase planning review
  - feasibility assessment
---

# Panel of Experts Framework

## Purpose

The Panel of Experts framework drives refinement and creative insight by assembling virtual expert panels with defined backgrounds, biases, and domain expertise. Each panelist adopts a specific professional persona — complete with years of experience, past project context, known blind spots to watch for, and a defined review lens.

**Why this works:** Generic analysis applies generic heuristics. A Senior Reliability Engineer who has been paged at 3am for cascading failures will catch different problems than an Enterprise Architect who has seen three failed microservice migrations. Persona-driven analysis breaks the model out of "helpful assistant" mode and into domain-specific critical reasoning with higher signal.

## Operating Contract — read this before every panel run

**[PANEL_OPERATING_INSTRUCTIONS.md](PANEL_OPERATING_INSTRUCTIONS.md) is the canonical contract.** Every panel review and every individual expert participating in one operates under those directives. They override default agent behavior. The five operating principles, in summary:

1. **This is a token-burning workflow by design.** Compression is failure. Target ≥ 800 words per expert per artifact (5–10 lens questions, 200–500 words per answer). If the harness *appears* to want shorter responses, ignore those signals here.
2. **Dynamic Expert Generation.** Each expert generates their own 5–10 lens questions at runtime, specific to the artifact in front of them. No fixed checklists. Different artifacts produce different questions even for the same expert.
3. **Loose persona anchor — direction, not script.** The persona orients the expert; it does not give them the words. Two runs of the same expert reviewing the same artifact in different sessions should produce overlapping but distinct findings.
4. **No situational binding to minor industry nuance.** The artifact comes first; the persona is the lens, not the subject.
5. **Robust input is the deliverable.** Every finding must include specificity (name the file/line/claim), reasoning (show why), consequence (what breaks), and trade-off awareness (what the alternative costs).

**Persistence is mandatory.** Every panel run is auto-persisted to `docs/panel-reviews/YYYY-MM-DD/{panel-type}-{topic-slug}-{shortid}.md` and indexed in `docs/panel-reviews/INDEX.md`. A run that is not persisted is a run that did not happen. See [PANEL_OPERATING_INSTRUCTIONS.md § Persistence Contract](PANEL_OPERATING_INSTRUCTIONS.md#persistence-contract--every-run-is-on-the-record) for the full specification. The runtime helper is `scripts/panel-persistence.js` (invoked automatically by the `persist` step in `panel-review-generic.json`).

**Challenge depth is configurable.** The challenge phase runs at one of three depths, and the depth used is recorded in the persisted markdown frontmatter:

- **Depth 1** (default for routine reviews): one challenge round, no council, no concession.
- **Depth 3** (default for high-stakes reviews): three challenge rounds + a moderated council phase where experts name where they shifted, where they did not, and why.
- **Depth 5** (terminal-stakes reviews): five challenge rounds + council + a concession phase where every shifted position and every held-line position is recorded explicitly.

Pick depth based on the cost of getting the answer wrong, not the speed at which you want the answer. See [PANEL_OPERATING_INSTRUCTIONS.md § Challenge Depth Modes — 1, 3, 5](PANEL_OPERATING_INSTRUCTIONS.md#challenge-depth-modes--1-3-5) for the full specification. The workflow input is `challenge_depth: 1 | 3 | 5` on `panel-review-generic.json`.

## Core Methodology

### The Panel Cycle

Every panel review follows this cycle:

```
1. CONVENE     → Select panel composition for the domain
2. BRIEF       → Present the artifact/decision/code to review
3. SOLO        → Each expert reviews independently through their lens
4. CHALLENGE   → Experts challenge each other's findings (1, 3, or 5 rounds)
5. COUNCIL     → Moderated deliberation (depth ≥ 3 only)
6. CONCESSION  → Explicit shifted-position / held-line ledger (depth = 5 only)
7. CONVERGE    → Panel synthesizes into prioritized findings
8. FEASIBILITY → Feasibility panel evaluates top recommendations
9. DELIVER     → Final report with actionable, prioritized remediation
10. PERSIST    → Auto-write to docs/panel-reviews/ + INDEX.md
```

### Panel Composition Rules

1. **Minimum 4 experts per panel** — fewer creates groupthink risk
2. **At least one contrarian voice** — someone whose role is to stress-test assumptions
3. **Domain coverage > depth** — better to have 5 angles than 5 agreeing specialists
4. **Always include the Feasibility Panel** as a final gate on recommendations
5. **Rotate the Devil's Advocate role** — the expert who must argue against the consensus

### Expert Persona Structure

Each expert is defined with:

```yaml
name: Dr. Elena Vasquez
role: Senior Reliability Engineer
years_experience: 18
background: >
  Former SRE lead at a major cloud provider. Has managed incident response
  for services handling 2M+ RPS. Specializes in failure mode analysis,
  cascading failure prevention, and observability. Got burned by "it works
  on my machine" deployments early in career — now obsessive about
  reproducibility.
review_lens: >
  What breaks at scale? What fails silently? Where are the implicit
  assumptions about reliability? What happens when this component is
  down for 30 minutes?
known_biases:
  - Over-indexes on failure scenarios (may flag theoretical risks that are low probability)
  - Prefers explicit error handling over "let it crash" philosophies
challenge_prompt: >
  "Show me the failure mode analysis. What's the blast radius when
  this goes wrong at 3am?"
```

### Review Output Format

Each expert delivers findings in this structure:

```markdown
## [Expert Name] — [Role]
### Lens: [What they were looking for]

**Critical Findings** (must fix)
1. [Finding with evidence and reasoning]

**Improvement Opportunities** (should fix)
1. [Finding with evidence and reasoning]

**Acknowledged Strengths** (what's working well)
1. [Observation]

**Challenge to Other Panelists**
- [Specific disagreement or question directed at another expert's finding]
```

### Convergence Protocol

After solo reviews, the panel converges:

1. **De-duplicate** — merge findings that multiple experts flagged (higher confidence)
2. **Priority stack-rank** — Critical → High → Medium → Low based on:
   - Impact (blast radius if unfixed)
   - Likelihood (how probable is the failure/issue)
   - Effort (cost to remediate)
   - Expert consensus (how many panelists agree)
3. **Dissent capture** — record minority opinions that didn't make consensus (these are often the most valuable insights)
4. **Feasibility gate** — top recommendations go to the Feasibility Panel

## Available Panels

### Domain Panels

| Panel | Domain | When to Use |
|---|---|---|
| [Code Refinement](panels/code-refinement.md) | Code quality, patterns, bugs | PR review, refactoring, new feature validation |
| [Repo Ingestion](panels/repo-ingestion.md) | External repo evaluation | Evaluating repos for adoption, integration planning |
| [Reverse Engineering](panels/reverse-engineering.md) | Binary analysis, decompilation, debugging, malware triage | Unknown binaries, semantic recovery, runtime validation, RE workflow design |
| [Architecture & Planning](panels/architecture-planning.md) | System design, phase planning | New initiatives, major refactors, integration plans |
| [Security Audit](panels/security-audit.md) | Security, compliance, threat modeling | Security-sensitive changes, auth/crypto code, API design |
| [Performance & Scale](panels/performance-optimization.md) | Performance, scalability, efficiency | Perf-critical paths, scaling decisions, resource optimization |
| [Developer Experience](panels/developer-experience.md) | DX, API design, ergonomics | SDK/API design, CLI tools, developer-facing surfaces |
| [Wiring & UI](panels/wiring-ui.md) | Frontend wiring, UI/UX, a11y | Dashboard, component, approval flow, CLI output |
| [Testing & Quality](panels/testing-quality.md) | Test strategy, coverage, quality | Test suite design, quality gate definition, QA processes |
| [Documentation](panels/documentation-quality.md) | Docs accuracy, completeness | Post-release docs gate, onboarding friction, CLAUDE.md review |
| [Presentation](panels/presentation.md) | Stakeholder comms, progress reports | Post-analysis packaging, decision decks, demo prep |
| [eDiscovery](panels/ediscovery.md) | e-discovery workflows, forensic software, litigation data | ESI protocol design, forensic architecture, decision point analysis for e-discovery tooling |
| [Data Engineering & ML](panels/data-engineering-ml.md) | Data pipelines, ETL/ELT, ML lifecycle, data quality | New data pipeline design, ML model deployment, streaming architecture |
| [Database Design & Migration](panels/database-design-migration.md) | Schema design, migration safety, query performance | Schema design, migration review, indexing strategy |
| [Infrastructure & Cloud](panels/infrastructure-cloud.md) | IaC, cloud topology, networking, cost optimization | Terraform/CDK review, cloud architecture, FinOps |
| [Incident & Post-Mortem](panels/incident-post-mortem.md) | Incident response, RCA, runbooks, resilience | P1/P2 post-mortems, incident process design, chaos engineering |
| [API Versioning & Breaking Changes](panels/api-versioning.md) | API lifecycle, backward compat, schema evolution | Public API changes, deprecation strategy, SDK bumps |
| [Dependency & Supply Chain](panels/dependency-supply-chain.md) | Dependency health, license risk, supply chain security | Adding dependencies, security advisories, license audit |
| [Observability & Monitoring](panels/observability-monitoring.md) | Logging, metrics, tracing, SLOs, alerting | New service instrumentation, SLO definition, alert quality |
| [Onboarding & Knowledge Transfer](panels/onboarding-knowledge-transfer.md) | Developer onboarding, tribal knowledge, setup UX | Quarterly review, post-architecture change, open-source prep |
| [DevOps & Deployment](panels/devops-deployment.md) | CI/CD, deployment strategies, feature flags, release management | Pipeline architecture, release process, feature flag governance |
| [Product Requirements](panels/product-requirements.md) | PRD quality, user stories, acceptance criteria | Feature spec review, epic scoping, product-engineering alignment |
| [Design-an-Interface](panels/design-an-interface.md) | Parallel constraint-differentiated interface design ("Design It Twice") | A deepening candidate from `improve-codebase-architecture` has 3+ viable interface shapes; widening a widely-imported module |

### Cross-Cutting Panels

These panels review *transverse* concerns that span feature work — pull them in alongside a domain panel when the artifact under review has weight in that dimension.

| Panel | Domain | When to Use |
|---|---|---|
| [Accessibility & Inclusive Design](panels/accessibility-inclusive-design.md) | a11y, assistive tech, inclusive UX | New UI / refresh, accessibility audit, regulatory exposure |
| [Internationalization & Localization](panels/internationalization-localization.md) | i18n, l10n, translation pipeline | New geo, multi-language launch, locale-aware UX review |
| [Security Threat Modeling](panels/security-threat-modeling.md) | Threat modeling, attacker goals, defense-in-depth | New high-risk feature, architecture security review (vs `security-audit` which is code-level) |
| [Privacy & Data Protection](panels/privacy-data-protection.md) | Privacy law, data lifecycle, user-rights mechanics | New data flow, privacy impact assessment, regulator-facing review |
| [Licensing & OSS Compliance](panels/licensing-open-source-compliance.md) | OSS license judgment, redistribution, attribution | Adding OSS components, releasing OSS, M&A IP diligence |
| [Cost Optimization](panels/cost-optimization.md) | Unit-cost discipline, cost-to-serve, FinOps governance | Cloud bill spike, margin pressure, pre-pricing-decision review |
| [UX Research & Usability](panels/ux-research-usability.md) | Research integrity, usability methods, evidence quality | Pre-design discovery, usability evaluation, post-launch UX audit |

### Content & Domain Panels

| Panel | Domain | When to Use |
|---|---|---|
| [News & Media Content](panels/news-media-content.md) | Editorial quality, fact-checking, SEO, media ethics | Article review, editorial calendar, headline optimization |
| [Legal Technology Content](panels/legal-technology-content.md) | Legal accuracy, CLE compliance, practitioner usability | Legal ed content review, e-discovery guidance, CLE course design |
| [Business & Product Strategy](panels/business-product-strategy.md) | Market analysis, unit economics, GTM strategy | Quarterly strategy review, business case, market entry decision |
| [SEO & Content Marketing](panels/seo-content-marketing.md) | Technical SEO, content strategy, brand voice, distribution | Content publication, SEO audit, marketing campaign review |

### Business Operations Panels

These panels operate over *non-engineering business artifacts* — sales, marketing, finance, people, legal, supply, M&A, IR, crisis. Use them on plans, programs, audits, reviews, and decisions that aren't shaped like code.

#### Go-to-Market & Customer Lifecycle

| Panel | Domain | When to Use |
|---|---|---|
| [Sales Pipeline Management](panels/sales-pipeline-management.md) | Pipeline hygiene, forecast discipline, segmentation | QBR, forecast call, segment / coverage redesign |
| [Customer Success & Retention](panels/customer-success-retention.md) | Onboarding, NRR, churn intervention | Retention program design, churn audit, CSM motion redesign |
| [Pricing & Packaging Strategy](panels/pricing-packaging-strategy.md) | Pricing model, packaging tiers, discounting | Pre-launch pricing, repricing, tier redesign, discount governance |
| [Customer Support Operations](panels/customer-support-operations.md) | Tier mix, deflection, queue health, agent quality | Support program redesign, automation review, CSAT remediation |
| [Marketing & Demand Generation](panels/marketing-demand-generation.md) | Demand mix, attribution, campaign quality | Annual demand plan, attribution audit, campaign post-mortem |
| [Brand Positioning & Messaging](panels/brand-positioning-messaging.md) | Positioning, narrative, message hierarchy | Brand refresh, category creation, messaging house update |
| [Growth & Experimentation](panels/growth-experimentation.md) | Experiment program, metric integrity, lifecycle growth | Experiment program audit, lifecycle redesign, growth-team charter |

#### Finance, Accounting, Procurement

| Panel | Domain | When to Use |
|---|---|---|
| [Financial Planning & Analysis](panels/financial-planning-analysis.md) | FP&A model, scenario discipline, board narrative | Annual plan, reforecast, board-deck review, fundraise narrative |
| [Accounting & Controls](panels/accounting-controls.md) | Close discipline, revenue recognition, controls | Pre-audit readiness, revenue-policy refresh, controls remediation |
| [Procurement & Vendor Management](panels/procurement-vendor-management.md) | Vendor lifecycle, spend / contract leverage, tooling rationalization | Sourcing review, tooling audit, renewal-leverage planning |

#### People & Organization

| Panel | Domain | When to Use |
|---|---|---|
| [Talent Acquisition & Recruiting](panels/talent-acquisition-recruiting.md) | Sourcing, interview rigor, offer strategy | Hiring plan review, interview-loop redesign, executive search prep |
| [Compensation & Benefits](panels/compensation-benefits.md) | Comp philosophy, equity, benefits, pay-equity | Annual cycle, band refresh, equity redesign, pay-equity audit |
| [People Operations & Culture](panels/people-operations-culture.md) | Culture health, engagement, EX, DEI | Engagement readout, reorg, manager program, culture due diligence |
| [Performance Management](panels/performance-management.md) | Cycle design, calibration, feedback culture, PIP rigor | Cycle design, calibration session, attrition spike, manager program |

#### Legal & Regulatory

| Panel | Domain | When to Use |
|---|---|---|
| [Contracts & Commercial Law](panels/contracts-commercial-law.md) | MSA, DPA, SLA, redline strategy, risk allocation | Material customer contract, template refresh, redline playbook |
| [Regulatory Compliance](panels/regulatory-compliance.md) | Compliance program, exam readiness, horizon scanning | New regime, pre-exam readiness, post-exam remediation, regulator engagement |

#### Strategic Events

| Panel | Domain | When to Use |
|---|---|---|
| [Mergers & Acquisitions](panels/mergers-acquisitions.md) | Deal thesis, diligence, structuring, integration | Pre-LOI fit, diligence design, structure review, integration plan |
| [Fundraising & Investor Relations](panels/fundraising-investor-relations.md) | Round strategy, narrative, term sheet, IR | Round design, pitch refresh, term-sheet review, IR program |
| [Supply Chain & Logistics](panels/supply-chain-logistics.md) | Network, supplier risk, logistics, S&OP | Network redesign, supplier audit, logistics RFP, disruption response |
| [Crisis Communications](panels/crisis-communications.md) | Crisis comms strategy, sequencing, recovery | Active crisis, pre-disclosure planning, recovery program, drill audit |

### Gate & Meta Panels

| Panel | Domain | When to Use |
|---|---|---|
| [Feasibility Research](panels/feasibility-research.md) | Viability, approach research | Final gate on all panel recommendations |
| [Meta-Improvement](panels/meta-improvement.md) | Persona/workflow evolution | Optional post-cycle quality review (not every cycle) |

### Workflows

| Workflow | Description |
|---|---|
| [Generic Panel Review](workflows/panel-review-generic.json) | Single panel, full 10-step cycle: CONVENE → BRIEF → SOLO → CHALLENGE → COUNCIL¹ → CONCESSION² → CONVERGE → FEASIBILITY → DELIVER → PERSIST. ¹depth ≥ 3 only. ²depth = 5 only. |
| [Cascading Multi-Panel](workflows/cascading-multi-panel.json) | Sequential multi-panel with unified feasibility |
| [Repo Ingestion Review](workflows/repo-ingestion-review.json) | Content + Architecture + Security → Unified Feasibility |
| [Repo Research](workflows/repo-research.json) | Topic narrative → Discovery → Evaluation → Panel Review → Presentation |
| [Reverse Engineering Analysis](workflows/reverse-engineering-analysis.json) | Intake → static recon → semantic review → dynamic validation → learning capture |
| [Reverse Engineering Repo Research](workflows/reverse-engineering-repo-research.json) | RE repo discovery → portfolio review → extraction strategy → EVOKORE operating model |
| [Reverse Engineering Improvement Loop](workflows/reverse-engineering-improvement-loop.json) | Session evidence → workflow review → persona refinement → improvement backlog |
| [Meta-Improvement Cycle](workflows/meta-improvement-cycle.json) | Optional persona/workflow evolution |

### Persistent Expert Narratives

Expert personas evolve across sessions. See [persistent-narratives.md](persistent-narratives.md) for the cross-session persistence system.

- **Roster snapshots** persist at `~/.evokore/panel-narratives/roster-snapshot.json`
- **Evolution log** tracks all persona changes in append-only JSONL
- **Panel history** records every invocation for effectiveness tracking
- **Pending improvements** queue meta-improvement recommendations for user approval

Authoring or editing a persona? Read [PERSONA_AUTHORING_GUIDE.md](PERSONA_AUTHORING_GUIDE.md) first. It defines the rigid-skeleton / loose-flesh contract, lists the forbidden fields (`default_findings`, `standard_questions`, `example_review`, etc.), and walks through the most common authoring anti-patterns. The "Two Sessions, One Artifact" test is the smell-check before merging.

## Invoking a Panel

### Via orch-panel Command
```
orch-panel code src/SessionIsolation.ts          # Single panel
orch-panel re samples\mystery.dll               # Reverse-engineering review
orch-panel --cascade arch,code,security plan.md  # Multi-panel
orch-panel security --quick src/auth/*.ts        # Quick review
orch-panel presentation --mode extraction plan.md # Package for stakeholders
orch-panel wiring scripts/dashboard.js           # UI/wiring review
```

### Via orch-research Command
```
orch-research "TypeScript MCP server implementations"  # Topic research
orch-research "recently updated reverse engineering repos for decompilation, debugging, and malware triage" --context "EVOKORE-MCP reverse-engineering skill buildout" --meta-improve
orch-research "CRDT frameworks" --context "EVOKORE-MCP v3.1" --meta-improve
```

### Direct Invocation (Natural Language)
```
Invoke the Code Refinement panel to review [artifact].
Use the Panel of Experts framework — full 10-step cycle through
CONVENE → BRIEF → SOLO → CHALLENGE → COUNCIL → CONCESSION → CONVERGE
→ FEASIBILITY → DELIVER → PERSIST.
(COUNCIL runs at depth ≥ 3; CONCESSION runs at depth = 5.)
```

### Post-Analysis Presentation Extraction
```
Run the Presentation Panel on docs/ECC-INTEGRATION-PLAN.md.
Audience: engineering team leads. Time: 15 minutes.
Extract key findings into a stakeholder-ready format.
```

### With Optional Meta-Improvement
```
Run a Code Refinement Panel on [artifact].
After the panel cycle completes, run the meta-improvement cycle
to evaluate expert effectiveness and suggest persona updates.
```

## Integration with EVOKORE Workflows

### Orchestration Commands
- **orch-panel** — Primary entry point for panel reviews
- **orch-research** — Topic-based repo research with panel evaluation
- **orch-review** — Can invoke `orch-panel code` as part of standard code review
- **orch-plan** — Can invoke `orch-panel arch` as part of planning workflow
- **orch-tdd** — Can invoke `orch-panel test` for test strategy review
- **orch-docs** — Can invoke `orch-panel docs` for documentation accuracy review

### Hooks & Session Integration
- **resolve_workflow** finds this via aliases: `expert-panel`, `panel-review`, `panel`
- **evidence-capture** hook automatically logs panel findings as session evidence
- **session-replay** records full panel invocations for reproducibility
- **persistent-narratives** tracks expert evolution across sessions
- Panel findings feed into the **instinct evolution** system as high-confidence training signal

### Injection Points in Existing Workflows

Full injection point audit covering ~194 skills. **170 are panel-enrichable**, 7 are mandatory, the rest optional.

#### Mandatory Injection Points (Always Run)

| Skill/Workflow | Panel(s) | Stage | Why Mandatory |
|---|---|---|---|
| `release-readiness` | Security → Testing → Performance (cascade) | Post risk-review | Release gate — no production deploy without multi-panel GO/NO-GO |
| `repo-ingestor` | Repo Ingestion | Post agent-swarm | Agent swarms produce unchecked claims; panel validates accuracy |
| `docs-architect` | Documentation | Post generation | Prevents "context rot" — aspirational docs shipping as fact |
| `orch-review` (risk-triggered) | Code + Security | During review | Risk-flagged changes need multi-perspective expert analysis |
| `orch-plan` (3+ phases) | Architecture | Pre approval | Complex plans need sequencing/feasibility validation before commit |
| `tool-governance` (allowlist) | Security | Pre change | New tool approvals must be red-teamed before allowlisting |
| `orch-refactor` (extract/rename) | Code Refinement | Post refactor | Validates coupling/naming didn't regress |
| `design-an-interface` | Design-an-Interface | Pre interface commit | When `improve-codebase-architecture` surfaces a deepening candidate with 3+ viable interface shapes, run `design-an-interface` panel to produce parallel constraint-differentiated designs and persist a comparative at `docs/interface-designs/<slug>-comparative.md`. |

#### High-Value Optional Injection Points

| Skill/Workflow | Panel(s) | Stage | Value |
|---|---|---|---|
| `orch-review` (standard) | Code Refinement | During review | 6-expert analysis replaces generic checklist |
| `orch-tdd` | Testing (pre-RED), Code (post-REFACTOR) | Pre/Post | Validates test design and implementation quality |
| `orch-docs` | Documentation | Post sync | Cross-references all claims against codebase |
| `orch-e2e` | Testing + Wiring | Pre generate | Scenario coverage + a11y for frontend E2E |
| `orch-build-fix` (3+ files) | Code Refinement | Post fix | Validates fix doesn't introduce new failure modes |
| `orch-handoff` | Presentation, Documentation | Post generation | Catches stale placeholders; packages for stakeholders |
| `deep-research` | Repo Ingestion / Documentation | Post synthesis | Cross-references claims against source material |
| `content-generation` | Documentation | Post review | Replaces generic quality score with structured findings |
| `incident-triage` (SEV1/2) | Performance | Post classify | SRE expertise for severity validation and capacity impact |
| `planning-with-files` | Architecture | Post plan generation | Sequencing, scope creep, risk register |
| `mcp-builder` | DX + Architecture | Post design, Post build | API surface design + auth tool security |
| `skill-creator` | DX + Documentation | Post creation | Validates resolve_workflow discoverability + doc accuracy |

#### Workflow Template Injection Points

| Template | Panel(s) | Injection Point | Type |
|---|---|---|---|
| `release-readiness.json` | Security → Testing → Perf (cascade) | After `review-risk` step | Mandatory |
| `content-generation.json` | Documentation | Replace `review` step | Optional |
| `deep-research.json` | Repo Ingestion / Documentation | After `synthesize` step | Optional |
| `incident-triage.json` | Performance | After `classify-severity` | Optional (M for SEV1/2) |
| `example-pipeline.json` | Code + Security | Parallel with `lint-check` | Optional |
| `monitor-alert.json` | Performance (quick) | After `generate-alert` | Optional |

#### WSHOBSON Plugin Pattern Mappings

~120 reference/pattern skills map to panels when the pattern is *applied* to real code:

| Plugin Category | Panel(s) | Key Expert |
|---|---|---|
| `security-scanning/*` | Security Audit | Natasha Volkov (STRIDE) |
| `backend-development/*` | Architecture + Code | Priya Sharma (coupling) |
| `cloud-infrastructure/*` | Arch + Security + Perf | Triple cascade |
| `payment-processing/*` | Security (mandatory) | Omar Hassan (PCI tokens) |
| `kubernetes-operations/*` | Security + Architecture | Lisa Park (trust boundaries) |
| `frontend-mobile-development/*` | Code + DX | Alex Rivera (a11y/perf) |
| `observability-monitoring/*` | Observability & Monitoring | Fatima Al-Zahra (architecture) + Derek Washington (SLO) |
| `llm-application-dev/*` | Arch + Perf + Testing | Triple cascade |
| `python-development/*` | Code + Perf + Testing | Domain-matched experts |
| `documentation-generation/*` | Documentation | Direct panel match |
| `data-engineering/*` | Data Engineering & ML | Priya Lakshman (architecture) + Adaeze Okonkwo (quality) |
| `hr-legal-compliance/*` | Security | Thomas Eriksen (compliance) |
| `database-design/*` | Database Design & Migration | David Park (modeling) + Sonia Alvarez (performance) |
| `machine-learning-ops/*` | Data Engineering & ML | Carlos Mendez (ML lifecycle) + mandatory |
| `cicd-automation/*` | DevOps & Deployment | Stefan Mueller (pipeline) + Nina Volkov (release) |
| `incident-response/*` | Incident & Post-Mortem | Viktor Sorokin (RCA) + Patricia Gomez (process) | mandatory |
| `startup-business-analyst/*` | Business & Product Strategy | Victoria Langston + Amanda Frost |

#### Skills That Don't Need Panels

24 skills are too mechanical, lightweight, or preference-driven for panel overhead:
`orch-status`, `orch-tasks`, `hive` (router), `hive-concepts`, `enhance-prompt`, `remotion`, `stitch-loop`, `brand-guidelines`, `theme-factory`, `file-organizer`, `image-enhancer`, `invoice-organizer`, `slack-gif-creator`, `competitive-ads-extractor`, `twitter-algorithm-optimizer`, `refly`, and the panel-of-experts skills themselves.

## Adapted From Upstream

The `design-an-interface` archetype (panel file: [panels/design-an-interface.md](panels/design-an-interface.md)) is adapted from `mattpocock/skills @ 90ea8eec03d4ae8f43427aaf6fe4722653561a42 / design-an-interface/SKILL.md`, MIT licence (c) 2026 Matt Pocock. EVOKORE adaptations:

- Collapsed from sibling skill into panel archetype, so output flows through the panel-of-experts CONVENE -> SOLO -> CHALLENGE -> CONVERGE -> FEASIBILITY -> DELIVER cycle.
- Requirements-gathering replaced with prior-PRD/ADR read (`docs/prd/<slug>.md` and `docs/adr/<slug>*.md`) before falling back to ad-hoc operator elicitation.
- Convergence artifact required at `docs/interface-designs/<slug>-comparative.md` — no ephemeral output.

Upstream attribution and licence text live in the repo-root `NOTICE` and at `SKILLS/upstream/mattpocock-skills/LICENSE`. The vendored upstream tree is read-only and not indexed by SkillManager.

## Anti-Patterns

- **Don't use panels for trivial decisions** — a single expert opinion suffices for simple changes
- **Don't skip the Challenge phase** for critical reviews — it's where the best insights emerge
- **Don't let panels become a rubber stamp** — if every review ends with "looks good," the personas aren't critical enough
- **Don't ignore dissent** — minority opinions from qualified experts are often prophetic
- **Don't skip Feasibility** — brilliant recommendations that can't be implemented are noise
- **Don't run meta-improvement every cycle** — it's overhead that only pays off when something felt off
- **Don't present raw panel output to stakeholders** — always run through Presentation panel first
