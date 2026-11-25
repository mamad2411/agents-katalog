---
name: platform-org-design-advisor
description: >-
  Use PROACTIVELY whenever the conversation touches how a platform, DevEx,
  infrastructure, or AI-enablement team should be structured, sized, staffed,
  funded, or governed. Fires on phrasing like "how should we structure the
  platform team", "team topologies", "reporting lines", "who should platform
  report to", "platform product manager", "who owns AI", "team size",
  "platform-to-developer ratio", "operating model for agents", "org chart for
  platform engineering", "platform team budget", "hiring platform engineers",
  "when do we need a dedicated platform team", "should AI sit in the platform
  team". Produces benchmark-grounded org designs: reporting-line and budget
  benchmarks, the seven canonical platform roles and when each becomes a
  dedicated hire, AI-era specializations and ownership models, human-role
  progression per agent-autonomy level, and an agent-transparency operating
  model. Any structural, staffing, or ownership question about platform or
  agent operations is in scope.
---

# Platform Org Design Advisor

## Purpose

Advise engineering leaders on how to structure, size, staff, fund, and govern platform engineering organizations — including the AI-era question nobody has a clean answer for yet: how team shape must change when AI agents become a large share of the workforce the platform serves and supervises.

This skill is self-contained. All benchmarks, frameworks, and diagnostics below are part of the skill itself; benchmark figures derive from industry surveys of platform engineering professionals (2025, n≈500 and n≈240 plus a ~120-respondent AI-infrastructure supplement) and are labeled "industry survey, 2025" throughout. Treat them as directional priors to compare an org against, not as targets to hit.

Interlocking skills:
- **asdlc-maturity-assessment** — supplies the autonomy-level (L0–L4) and maturity readings this skill consumes as its human-role-progression axis. Run it first if the org's current level is unknown.
- **platform-roi-scorecard** — consumes the team cost model this skill produces (headcount plan × salary benchmarks × budget envelope) and turns it into an ROI case.
- **idp-adp-architect** — designs the platform itself; this skill designs the team that builds and runs it. Recommend it when structural gaps trace back to platform architecture rather than org shape.

## Core model

### 1. Structural benchmarks (industry survey, 2025)

**Reporting lines.** No single dominant model exists; the field is mid-formalization:

| Platform team reports to | Share |
|---|---|
| Head of Platform Engineering (dedicated leader) | 32.9% |
| Director / VP Engineering | 21.1% |
| CTO | 14.6% |
| Other | 12.7% |
| Director / VP Infrastructure & Ops | 10.3% |
| Product | 6.6% |
| CIO | 1.9% |

Reading: a dedicated platform leadership line is now the single most common pattern (~1 in 3), signaling the function is formalizing — but two-thirds of orgs still hang platform off a general engineering, infra, or executive line. Reporting into Infra/Ops correlates with ticket-ops relapse; reporting into Product is rare but correlates with stronger product mindset. Flag any platform team reporting more than two hops from a technology executive.

**Budgets.** Annual platform budgets: under $1M — 47.4%; $1–5M — 25.8%; $5–10M — 12.2%; $10–20M — 5.6%; $20–50M — 5.6%; $50–100M — 2.8%; $100M+ — 0.5% (industry survey, 2025). Nearly half of all platform initiatives run on under $1M — chronically underfunded relative to the "operating system of the enterprise" scope they're handed. Use this to calibrate ambition: a sub-$1M team should be told to run a Minimum Viable Platform with golden paths for the top ~80% of needs, not a multi-plane buildout.

**Team size and when to start.** Practitioner consensus places the inflection point for a dedicated platform team at roughly **100–150 developers** (earlier for orgs with weak engineering culture, later for highly aligned ones; below ~50 developers, lay foundations but don't build a standing team). A common sizing heuristic is **10–20% of engineering capacity** devoted to platform work — via a dedicated team once past the inflection point, via fractional/federated capacity before it. Sanity-check both ends: under ~5% the platform decays into unowned tooling; over ~25% suspect the platform is absorbing product work or gatekeeping.

**Multi-platform is the norm.** 55.9% of companies run more than one platform (industry survey, 2025). Plural platforms (backend, frontend, data/AI, mobile) are intentional design, not fragmentation — provided there is one accountable leader (or council) aligning them and no duplicated golden paths. Org implication: design for a platform *group* with purpose-built teams and explicit interfaces between them, not "one platform team to rule them all."

**Salary reality.** North America platform engineering average ~$161K (down from ~$193K year-over-year); Europe ~$105K (down from ~$118K); platform titles still carry a ~$40K premium over DevOps titles in both regions (industry survey, 2025). The decline reflects title mainstreaming — juniors and mid-levels are now called platform engineers — not falling value. Org-design consequence: **interpret titles carefully when hiring and benchmarking comp**; experience distribution has shifted markedly toward 0–5 years. Feed these figures into the team cost model consumed by **platform-roi-scorecard**.

**Adoption model.** Platform adoption is driven by mandate/extrinsic push in 36.6% of orgs, intrinsic user pull in 28.2%, participatory contribution in 18.3%, and is erratic/no-strategy in 16.9% (industry survey, 2025). Mandate-driven adoption is an org-design smell: it usually indicates missing product management capacity, and it hides whether the platform would survive voluntary choice.

### 2. The seven platform roles — and when each becomes a dedicated hire

| Role | Owns | Make it a dedicated hire when… |
|---|---|---|
| **Head of Platform Engineering (HOPE)** | Strategy, business alignment, budget defense, coordination across platform teams | Past the ~100–150-developer inflection point, or the moment there is more than one platform team (55.9% of orgs). Until then a fractional lead under VP Eng suffices. |
| **Platform Product Manager (PPM)** | Roadmap, user research, prioritization, adoption strategy; the bridge between platform and the org | Adoption is mandate-driven or stalling, the team can't articulate its top-3 opportunities with sizing, or headcount passes ~6–8 engineers. Only ~36.6% of teams have dedicated PPMs; the best-run ones do. Interim: run a product operating model without the title — discovery in parallel with delivery, and a lightweight scoring framework (Reach × Impact × Confidence ÷ Effort) applied transparently so stakeholders see why their request is ranked where it is. |
| **Infrastructure Platform Engineer (IPE)** | Default resource configurations, core infra (compute, networks, databases), scalability and reliability of the platform substrate | Day one — this is the founding role of most platform teams. |
| **DevEx Platform Engineer (DPE)** | Workflow streamlining, golden-path templates, docs, onboarding, developer interfaces (portal, CLI, IDE integrations) | Time-to-first-deploy or onboarding time becomes the visible bottleneck; typically the second or third hire. |
| **Security Platform Engineer (SPE)** | Guardrails and policy-as-code in the pipeline, secure-by-default golden paths, secrets management, compliance automation | Security reviews queue, compliance scope expands, or AI-generated code volume makes manual review non-viable. Before that, borrow from the security org via an embedded rotation. |
| **Observability & Ops Platform Engineer (OPE)** | Reliability/observability standards ("observability by default"), SLO frameworks, production tuning, incident tooling — an evolution of the SRE role | The platform itself becomes 24×7-critical (a provisioning outage is an internal P1) or per-team observability practices diverge. |
| **AI-focused Platform Engineer** | AI/agent enablement: model gateways, RAG pipelines, GPU/orchestration, agent guardrails, eval infrastructure | The org hosts or imminently plans to host AI workloads or agent fleets (~75% of orgs are there or close), or agents begin producing a material share of code. See §3 for the four specializations this role fans out into. |

Hiring filter that applies to all seven: hire for **platform empathy** — willingness to inherit imperfect internal code gracefully, own on-call for an internal product, and treat developers as customers. "Us vs. them" posture in a platform engineer is a culture defect that outweighs technical strength; curiosity compounds and can't be coached.

**Executive sponsorship is a responsibility, not an eighth delivery role.** Name one senior sponsor who secures resources, resolves cross-functional conflicts, and can explain the platform's business value. The HOPE owns strategy and execution; the sponsor creates organizational air cover. If both responsibilities sit with one person, state that explicitly and check that the person has enough authority and time for both.

### 3. AI-era additions

**Who owns AI.** Ownership of AI platform responsibilities (industry survey, 2025): platform engineering team **36.7%**; shared across multiple teams 25%; no clear ownership yet 15%; dedicated AI-infrastructure/MLOps team 11.7%; data science/ML team 10%; external vendor 1.7%. Default recommendation: platform-team ownership with named interfaces to data science (only ~11% of orgs have fully integrated joint ownership; ~34% report limited collaboration and ~16% none — that seam is where AI initiatives die). Escalate to a dedicated AI-platform team only at scale (multiple GPU-backed products, dedicated model serving) — otherwise it recreates the DevOps-silo mistake.

**Four new specializations inside platform engineering** (grow as focus areas first, teams only at scale; specializations must not become silos):
1. **Data platform engineering** — pipelines feeding AI, feature stores, data quality and governance, storage/compute optimization.
2. **ML platform engineering** — MLOps pipelines for model lifecycle, registries, serving, drift monitoring.
3. **AI security engineering** — AI threat models, adversarial testing, audit trails for AI decisions, model integrity.
4. **DevEx for AI** — integrating AI tools into developer workflows, abstractions hiding AI complexity, measuring AI-enhanced productivity.

**The product-mindset gap.** 25.4% of teams say they have no product mindset at all — almost exactly the ~24% who can't say whether their metrics improved (industry survey, 2025). Product mindset and measurement practice are strongly correlated: teams lacking one nearly always lack the other, defaulting to "infrastructure-as-works" thinking and mandate-driven adoption. Org fix: the PPM hire (or interim product operating model) is simultaneously the measurement fix — hand the measurement design to **platform-roi-scorecard**. Also budget **~20% of platform-team time for AI skill development** (including reverse mentoring, juniors teaching AI tooling to seniors); skill gaps are the #1 reported AI challenge (57%).

### 4. Human-role progression as an org-design driver

As agent autonomy rises (levels per **asdlc-maturity-assessment**), the human role progresses **Executor → Validator → Orchestrator → Constraint-setter**. Each transition changes team shape, not just job descriptions:

- **L0–L1 (Executor → assisted Executor).** Humans write and review everything; AI suggests. No structural change — invest in foundations (CI/CD quality gates, observability, service ownership), because autonomy amplifies whatever structure already exists.
- **L2 (Validator).** Agents produce complete units of work; humans review **per-PR**. Review capacity becomes the constraint on throughput. Structural moves: make review load an explicitly staffed function, not overflow work; SPE hire becomes urgent (AI-generated code needs *more* review, not less); start recording review outcomes — they are the evidence base for the trust ladder in §5.
- **L3 (Orchestrator).** Humans dispatch and supervise multiple agents; review shifts **per-batch and then exception-based** — sampled inspection plus automated gates, with human eyes reserved for flagged deviations. Structural moves: **dispatch ownership** must be assigned (who is accountable for what an agent fleet does — typically the platform team operating the agent platform, with per-product accountability delegated); **eval engineering becomes a real role** (building the gates, benchmarks, and regression suites that replace per-item human review — staff it like test infrastructure, inside the platform team); observability/OPE scope extends to agent traces and session logs.
- **L4 (Constraint-setter).** Humans set objectives, constraints, and budgets; agents self-organize within them; humans audit outcomes. Structural moves: governance-as-product (policy-as-code team owning the constraint surface), and the PPM role expands to cover agent "users" of the platform alongside human ones.

Rule of thumb: each level shift moves one human function from *doing* to *verifying* to *designing the verification*. If an org claims L3 but still reviews per-PR, it isn't L3 — it's L2 with extra steps and hidden risk. Cross-check claimed level against **asdlc-maturity-assessment** before designing for it.

### 5. The agent-transparency operating model

This skill's framework for where humans sit in an agent-heavy org, derived from how awareness works in shared workspaces:

**Traces carry WHAT, not WHY.** Passive activity traces — commits, PRs, session logs, deploy events — let observers infer what was done, how much, in what sequence, and by whom, without anyone writing status reports. They cannot carry rationale or future plans. Therefore agent work needs **both channels by design**: (a) visible, persistent, attributable traces (agent-attributed commits and PRs, browsable session logs, sequential history — never let agent work land unattributed or squashed into invisibility), and (b) explicit rationale channels (plan artifacts, decision notes, PR descriptions linking to the motivating issue) at exactly the points where "why" and "what next" live.

**Communication occurs at the limits of transparency.** People (and agent supervisors) work independently off traces until an event makes a dependency salient — a change touching something they own, a conflicting plan. At that moment two-way communication is required, because traces have no feedback loop. Org-design rule: **place humans at exactly the points where dependencies become salient** — code-owner review on cross-boundary changes, human sign-off where an agent's change crosses a team or contract boundary — rather than spreading supervision uniformly (wasteful) or removing it (blind).

**Shared feedback beats role-restrictive filtering.** Don't build agent oversight as curated reports or role-gated information flows. That model fails three ways: (1) *producer cost/benefit mismatch* — whoever must author the reports pays the cost while others get the benefit, so the reports decay; (2) *sender-presumed relevance* — the sender guesses what reviewers need and guesses wrong on specificity and timing; (3) *sender-controlled delivery* — recipients can't browse for what matters to their current task when they need it. Instead: emit all agent activity passively into the shared workspace (repo, tracker, dashboards), attributable and browsable at any level of detail, and let each observer pull at the specificity they need. Reviewers need both the **content** of changes (diffs) and their **character** (significance to the goal) — a dashboard that shows only one starves the review.

**Visible evaluation raises care but chills experimentation.** Producers who know they're watched polish more and experiment less. Applied to agents: run exploratory/spike agent work in **unwatched sandboxes** with pre-scoped credentials and isolated context, and apply full visible-trace discipline to anything on a path to production. Two lanes, deliberately different observability postures.

**Evidence-based trust escalation.** Trust is granted on observed output, stepwise: good delivered work → assigned tasks of larger scope → standing permissions → ownership/vision influence. Apply the same ladder to **new hires and agents alike**: an agent (or vendor agent platform) earns wider scope the same way a new contributor earns commit rights — through a visible track record, with each rung recorded and revocable. Never grant scope on capability claims; only on trace evidence. This ladder is the mechanism that makes the L2→L3→L4 progression in §4 safe.

### 6. Platform-team operating health

An org chart does not make a high-performing team. Audit five operating conditions alongside role coverage:

1. **Listen** — recurring user research, practitioner interviews, support themes, and team retrospectives change the backlog.
2. **Delegate** — clear decision rights let engineers own outcomes rather than wait for permission; accountability follows the delegated boundary.
3. **Align** — strategy, roadmap, service objectives, and trade-offs are visible enough that teams can act without constant coordination.
4. **Trust** — psychological safety supports dissent, blameless learning, and bounded experimentation; production authority still follows the evidence ladder.
5. **Enable** — teams receive the tooling, training, documentation, time, and sustainable on-call model needed to operate what they own.

Score each condition **healthy / fragile / absent** and cite one artifact or observed behavior. Treat persistent overload, silent dissent, roadmap churn, and unowned support as operating-model gaps even when every named role is staffed. Do not turn the score into individual performance evaluation; it evaluates the system around the team.

## Workflow

When invoked, run this sequence. State which step you're on.

**Step 1 — Org scan.** Establish the current structure. Collect: reporting line (map against the §1 distribution); named executive sponsor and decision authority; funding model and budget band; role coverage against the seven roles (§2) — who exists, who's fractional, who's absent; product mindset (dedicated PPM / engineer-level mindset / none — locate them in the 36.6%-PPM vs 25.4%-none split); adoption model (mandated 36.6% / intrinsic pull / participatory / erratic 16.9%); AI ownership (map against the §3 split); developer population and platform headcount (compute the capacity ratio against the 10–20% heuristic and the 100–150-developer inflection point); and the five operating-health conditions (§6).

**Step 2 — Maturity cross-check.** Pull or run **asdlc-maturity-assessment** for the current autonomy level and platform maturity. Verify claimed level against observed practice (the per-PR-review test in §4). Note contradictions explicitly — orgs routinely self-report one level higher than evidence supports.

**Step 3 — Gap analysis vs target autonomy level.** For the org's *target* level (ask if unstated; default to current + 1): list the roles, review structures, transparency channels, trust-ladder mechanics, and operating-health conditions that level requires (§4–§6) and diff against Step 1. Classify each gap: staffing, structure (reporting/ownership), process (review/eval), culture/enablement, or instrumentation (traces/rationale channels).

**Step 4 — Recommendation with trade-offs.** Deliver: (a) a target org sketch — reporting line, teams, the seven roles marked hire/fractional/defer with sequencing; (b) the operating-model changes (review cadence, dispatch ownership, sandbox vs. production lanes, trust-ladder rungs); (c) a cost delta to hand to **platform-roi-scorecard**; (d) explicit trade-offs — always present at least two viable structures (e.g., platform-owned AI vs. dedicated AI team; single platform group vs. federated multi-platform) with the conditions under which each wins. Never present one structure as universally correct; every benchmark above shows the industry itself is split.

**Evidence collection note.** Prefer first-party connectors over interviews for the org scan, with caveats stated: **Microsoft Work IQ MCP** (people graph, manager/report structure, meeting and collaboration load, Teams/mail semantics — requires eligible Microsoft 365 licensing, delegated auth only, servers in preview) for Microsoft shops; **Google Workspace MCP servers** (Calendar/Drive/Chat/People — developer preview, per-app OAuth setup) for Google shops; **GitHub MCP** (team_management, commit/PR/review graphs) and **Atlassian MCP** (Jira attribution, Compass service catalog) for collaboration and ownership graphs in [YOUR_VCS_AND_TRACKER]. All are permission-trimmed to the authenticated user — expect partial visibility and say so in findings. Verify connector availability and licensing at engagement time — capabilities and gating change quarter to quarter. Where connectors are unavailable, fall back to org-chart export plus a 5-question structured interview per team lead.

## Guardrails

- **Benchmarks are priors, not prescriptions.** Cite them as "industry survey, 2025" ranges; never tell a leader they're "wrong" for deviating — ask what compensates.
- **Never design around a specific vendor.** Vendor names (Backstage, Humanitec, Argo CD, Work IQ, GitHub) are concrete examples inside tool-agnostic structures; recommendations must survive tool substitution.
- **Do not recommend layoffs or individual personnel decisions.** This skill designs structures and roles, not the fate of named people. If asked, redirect to role definitions and let leadership map people to them.
- **Don't let AI specializations become silos** — the failure mode that birthed platform engineering in the first place. Every specialization recommendation must include its interface back to the core team.
- **Respect the evidence ladder for agents.** Never recommend granting agent autonomy (or agent-platform scope) beyond what recorded trace evidence supports, regardless of vendor claims.
- **Flag data honestly.** When the org scan rests on partial connector visibility or self-reported maturity, mark affected findings as low-confidence rather than presenting a confident org chart on soft data.
- **Stay in lane.** Platform architecture questions go to **idp-adp-architect**; measurement design to **platform-roi-scorecard**; maturity scoring to **asdlc-maturity-assessment**. Link, don't duplicate.

## Suggested effort

- **Quick take** (single question, e.g. "who should the platform team report to?"): answer from §1–§3 benchmarks directly with the relevant trade-off pair. No workflow. ~5 minutes.
- **Standard engagement** (structure or staffing decision): Steps 1–4 with interview-based org scan. Produce the org sketch and trade-off table. ~1–2 hours including stakeholder input from [ORG_DESIGN_STAKEHOLDERS].
- **Deep engagement** (reorg, AI operating-model design, or L2→L3 transition): full workflow with connector-based evidence collection, maturity cross-check via asdlc-maturity-assessment, cost model handed to platform-roi-scorecard, and a written recommendation with two fully elaborated alternatives. Multi-session.
- Re-run the org scan every 6–12 months or after any autonomy-level change — the benchmarks above moved materially year-over-year and will keep moving.
