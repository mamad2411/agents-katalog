---
name: platform-security-playbook
description: >-
  Design, harden, and audit platform-level security and governance for
  development where humans and AI coding agents work side by side. Use
  PROACTIVELY when the user wants to secure AI or coding agents, set up agent
  governance or guardrails, enforce least privilege for agents, build an audit
  trail of agent actions, run or modernize vulnerability management, achieve
  compliance for coding agents (SOX, GDPR, FedRAMP, ITAR, IL4-IL6, NIS2,
  DORA), evaluate a sovereign platform or cloud strategy, adopt policy-as-code
  or shift-down security, triage CVEs at scale, control agent network/egress
  access, or asks "can we trust agents in a regulated environment", "who
  approves what an agent ships", "what does the auditor need from our AI
  workflow". Fire on related phrasing, not just exact matches. For maturity
  scoring use asdlc-maturity-assessment; for platform architecture (including
  sovereign variants) use idp-adp-architect; for verifying a single agent's
  output, agent-trust-auditor.
---

# Platform Security Playbook

## Purpose

Help the user design and audit the security and governance architecture of a
development platform where both humans and AI coding agents produce change. The
output of this skill is a concrete control design: which controls exist, where they
are enforced, what evidence they produce, and how they scale as agent autonomy grows.

Why this matters (industry data, 2025/2026):

- Analyst forecast: over 40% of agentic AI projects will be canceled by 2027 due to
  inadequate risk controls — failures of governance, not of models or compute.
- 84% of organizations consider AI governance a serious concern; 68% cannot reliably
  distinguish agent actions from human actions; 59% do not know how quickly they
  could shut down AI systems in a crisis.
- Vulnerability management costs an average of $1.9M per year in direct spend, and
  the average data breach costs $4.88M. Over 40,000 new CVEs were published in 2024
  (+38% year over year) and 84% of codebases contain at least one known vulnerability.
- Developers spend roughly 19% of weekly hours on security toil — about one full
  workday — and fewer than 30% of platform teams achieve successful voluntary adoption
  when security adds friction.

The skill treats risk reduction as a first-class objective (fines, trust, audit
findings), not merely a tax on productivity: in regulated industries, effective risk
minimization is itself a competitive advantage.

Context to establish before applying: [ORG_NAME], [APPLICABLE_REGIMES — e.g. SOX,
GDPR, FedRAMP], [CURRENT_AUTONOMY_LEVEL — see the ladder below], [PLATFORM_OWNER —
team accountable for enforcement].

Related skills: use **idp-adp-architect** to design the underlying platform and agent
infrastructure this playbook governs (reference architectures, workspace
provisioning, the security plane's component choices). Use
**asdlc-maturity-assessment** to locate the organization on the autonomy ladder and
apply the regulated-industry overlay and Level-2+ readiness gates before scaling
agent access. Regulated-vertical briefs (healthcare, finance, government) from
**platform-industry-brief** route here for this compliance overlay.

## Core model

### Doctrine 1 — Governance moves from humans to infrastructure

The traditional assumption — humans write code on laptops, push to repos, pipelines
handle the rest — breaks down once agents execute multi-step workflows, file PRs in
parallel, and iterate without a human touching every line. At low autonomy,
governance can be a human concern (review everything). As autonomy grows, review
bandwidth becomes the bottleneck and governance must become an infrastructure
concern: policies enforced by the platform, deterministically, on every action.

### Doctrine 2 — Deterministic guardrails around probabilistic behavior

Agents are probabilistic; you cannot fully predict what they will attempt. Compliance
systems, identity controls, audit trails, policy enforcement, and CI/CD are
deterministic. The production system's job is to constrain probabilistic agent
behavior inside deterministic guardrails enforced at the platform layer. Target a
**controlled-failure model**: the goal is not that agents never hit a boundary, but
that every boundary encounter is blocked, logged, attributed, and surfaced for review
instead of becoming an incident. Worked pattern: agent attempts production-DB access
→ policy blocks it → the block is logged with attribution → the agent is told the
action is out of scope and adjusts → security receives a review notification. Nothing
bad happened, and everything is on the record.

### Doctrine 3 — The workspace is the control surface

There are three tiers where controls can live, and two of them are insufficient:

1. **Application tools** (IDEs, agent apps — e.g. Cursor, VS Code): user-facing
   settings you do not operate. A vendor update can silently change them.
2. **Model providers** (hosted LLM platforms — e.g. Bedrock-style services):
   model-level policies, blind to what agents actually execute.
3. **The platform / workspace layer**: network access, tool usage, permissions,
   resource boundaries, model routing, and audit logging enforced at the
   infrastructure layer, consistently across any model or agent framework.

Vendor-, IDE-, and SaaS-level controls fail auditability tests: compliance teams
cannot audit what they cannot see, and governance living inside a vendor platform
means you have outsourced enforcement, auditability, and risk management. Regulated
environments need independent control over how agents execute. Centrally managed,
policy-controlled workspaces (cloud development environments, self-hosted or
air-gapped where required) are where governance becomes deterministic: every process
in the workspace inherits enforced policy.

### The five control responsibilities (the spine of this playbook)

Every platform governing agents must implement these five responsibilities. Audit any
existing platform against them; design any new platform around them.

1. **Provisioning** — environments are stood up from code (e.g. Terraform/OpenTofu
   templates): compute profiles, network configuration, pre-installed tools,
   injected context. Agents consume their environment as code and "know who they
   are" from the first token.
2. **Policy** — RBAC defining which libraries, tools, repos, and network domains each
   agent may access. Policies are expressed as code and version-controlled. Agents
   are told their boundaries up front so they do not waste tokens attempting blocked
   actions.
3. **Audit** — every prompt, tool call, model interaction, and resource access is
   logged and attributed to a specific agent, task, and initiating human. Model-usage
   tracking gives cost visibility. Compliance teams audit agents with the same rigor
   as human developers.
4. **Proxy** — all model and agent traffic routes through a governed proxy:
   authentication via the existing identity provider, routing across model providers,
   centralized observability of model usage.
5. **Boundary** — a per-agent firewall enforcing network isolation and access control
   at the process level; outbound requests are restricted and audited to cut
   data-exfiltration risk.

### The five privilege-separation patterns

Cardinal rule: **agents never inherit human privilege levels.** Agent defaults:
least privilege, no internet access, no repository write access — read plus PR
submission only. Humans keep their own privilege level even when they join an agent's
workspace to review (the reviewer is not limited by the agent's constraints).

1. **Read-only agents** — analysis and context-gathering agents get read-only repo
   access; no branch or commit ability.
2. **PR-only writes** — code-generating agents may only propose (submit PRs), never
   merge or commit to protected branches; every change flows through review.
3. **Approval workflows** — high-stakes actions (production deployments,
   infrastructure changes, sensitive-data access) require explicit human approval at
   defined checkpoints before the agent proceeds.
4. **Per-agent firewalling** — permissions are scoped per agent per task: a
   backlog-grooming agent and a prototyping agent do not share an access profile.
5. **Shared oversight workspaces** — humans can observe agent work in real time,
   with role-based access controls applied.

### Autonomy-aware controls: the four-level ladder

Map the organization to a level, then treat the listed controls as **mandatory at
that level and above**. (Use asdlc-maturity-assessment for the full readiness
evaluation and regulated-industry gates.)

| Level | Human role | Mandatory controls |
|---|---|---|
| **L1 — Human in the loop** | AI suggests; human confirms and executes every change | Identity/SSO for all AI tooling; audit logging of model usage; secret scanning; acceptable-use policy. Governance may still be human-operated. |
| **L2 — Human on the loop** | Agents generate PRs in parallel; deterministic systems validate; humans verify behavior, not every line | Governance must move into infrastructure: PR-only writes and read-only defaults; policy-as-code gates in CI; per-agent identity with full audit attribution; deterministic validation suites; provisioning from templates. |
| **L3 — Human as orchestrator** | Agents execute multi-step workflows and deploy low-risk changes under human orchestration | All L2 controls plus: approval checkpoints for high-stakes actions; per-agent firewalling; ephemeral one-task workspaces; proxy for all model traffic; token/cost budgets; validation loops that route failures back to the agent as structured feedback. |
| **L4 — Human outside the loop** | A system of agents initiates and promotes changes autonomously | All L3 controls plus: process-level boundary enforcement; controlled-failure containment with automated review routing; shared oversight workspaces; a tested kill-switch/shutdown runbook; model-risk monitoring (versioning, drift detection) comparable to quantitative-model governance. |

The transition that changes everything is **L1 → L2**: the moment validation replaces
line-by-line review, governance requirements change fundamentally.

### Vulnerability management doctrine: shift left → shift down

Shift left (asking developers to run scanners, triage findings, and patch earlier)
has hit its limits — it relocates toil rather than removing it. **Shift down** makes
the platform responsible: shift left means developers run security tools; shift down
means the platform runs security tools and developers never see the findings unless
action is required. This is a change in domain ownership: the platform team owns the
security posture of the foundation; application teams inherit that security by
default and retain responsibility only for business logic and data handling.

The four secure-by-design platform capabilities:

1. **Automated image hardening** — hardened, signed base images, centrally managed,
   automatically rebuilt when upstream CVEs are disclosed.
2. **Policy-as-code enforcement** — deployment-boundary policies (e.g. OPA, Kyverno,
   Conftest): no unscanned images, block critical-severity CVEs, enforced in CI/CD.
3. **Pre-approved service templates** — golden-path templates (Terraform/OpenTofu,
   Helm) with scanning hooks and secure defaults baked in.
4. **Continuous secret rotation** — centralized secrets management (e.g. Vault, AWS
   Secrets Manager, Doppler), short-lived tokens, secret scanning in pipelines,
   nothing hard-coded.

Why the manual alternative cannot scale — CVE triage economics: a developer pulls a
popular base image; the scanner reports **287 vulnerabilities, 52 rated high or
critical**; the developer spends **4 hours** triaging exploitability, documenting
false-positive exceptions, and patching. The next day a new CVE lands on the same
image and costs another half day. Multiply by dozens of services and hundreds of
developers: a systemic hemorrhage of capacity that no amount of individual diligence
fixes. The answer is architectural — hardened images eliminate whole classes of
findings at once; policy-as-code replaces inconsistent human judgment with
predictable enforcement.

### Sovereignty overlay

Apply this subsection when the organization operates in jurisdictions with data
sovereignty requirements, critical-sector regulation, or geopolitical exposure.

- **Jurisdiction analysis — the legal squeeze**: extraterritorial laws (e.g. the US
  CLOUD Act) can compel a provider to hand over data regardless of where it is
  physically stored, while GDPR prohibits transferring EU personal data without
  safeguards — a provider subject to both is in an impossible position, and so is
  its customer. EU regulation raises the bar further: NIS2 imposes cybersecurity and
  supply-chain risk management across critical sectors, and DORA requires financial
  entities to map ICT dependencies, avoid over-dependence on any single critical
  provider, and maintain **tested, operational** exit strategies — not a filed
  document.
- **Data residency ≠ sovereignty**: servers in-country are illusory if the control
  plane, management APIs, VCS, CI/CD, secrets manager, or AI assistant are governed
  by a foreign jurisdiction. Every management-stack component must pass the same
  sovereignty evaluation as the infrastructure.
- **Exit-by-design**: sovereignty is portability of workflows. Everything-as-code
  with GitOps makes the exit strategy a functional capability: all infrastructure
  defined declaratively (e.g. OpenTofu — Linux Foundation-governed, avoids
  single-vendor license risk), a self-hosted VCS (e.g. Forgejo, Gitea, self-hosted
  GitLab) as the sole source of truth, and a GitOps controller (e.g. ArgoCD)
  reconciling declared state — so disaster recovery or forced provider exit means
  pointing the controller at a new cluster and rebuilding from the repo. Air-gapped
  operation is the ultimate stress test: a fully self-hosted platform can run at
  full automated velocity without sending a packet across the public internet.
- **AI sovereignty (generic argument)**: dependence on a single foreign-jurisdiction
  AI provider is a concentration risk — access can be constrained by legal,
  commercial, or geopolitical shifts outside the organization's control, and
  proprietary assistants may transmit code to vendor servers, creating an IP-leakage
  vector. Sovereign designs keep optionality: self-hosted or open-weight models on
  regional infrastructure for sensitive workloads, with model routing through the
  governed proxy so switching providers is a configuration change.
- **Provider validation questions** (a sovereign platform answers yes to all): Does
  the provider hold regional sovereignty certifications (e.g. SecNumCloud, BSI C5)?
  Is data physically stored exclusively in the designated jurisdiction? Is the
  provider corporately immune to extraterritorial data requests? Is the IaC tooling
  open-source and free of restrictive licensing? Are VCS, orchestrator, keys,
  secrets, and IAM self-hosted or enterprise-controlled within the jurisdiction? Are
  AI assistants hosted on local or sovereign infrastructure, with an explicit
  guarantee that code and telemetry are not ingested into external training models?

## Workflow

Run the phases in order. The single most common failure mode is skipping Phase 1 and
locking agents down before understanding behavior.

### Phase 1 — Baseline: observability first

"Governance is impossible without insight." Before enforcing anything:

1. **Audit current AI and agent usage across teams** — identify shadow AI, which
   tools developers actually use, and quantify the governance gap.
2. **Deploy visibility infrastructure** for model traffic: which models are used, how
   agents interact with tools, token consumption, cost attribution. This surfaces
   shadow AI, highlights valuable use cases, and establishes baseline metrics.
3. **Generate SBOMs** for the three highest-traffic services (e.g. with Syft or
   Grype) to establish dependency visibility; audit the delivery flow
   commit-to-runtime and identify the three highest-friction security touchpoints.
4. Record baseline values for the metrics catalog (below).

### Phase 2 — Structured context and governed workspaces

Solve the cold-start problem before scaling: agents that begin without context
produce poor output and waste resources. Provision workspaces from
infrastructure-as-code templates so agents consume the environment as code and
understand role, constraints, and available tools; supplement with lightweight
context engineering — markdown files defining standards, anti-patterns, and
terminology. First-attempt accuracy improves significantly with structured upfront
context. Move development from local machines into centrally managed workspaces and
implement the five control responsibilities there. (Design the workspace
infrastructure itself with idp-adp-architect.)

### Phase 3 — Privilege separation and policy-as-code

Document the agent-vs-human permission model; implement the five
privilege-separation patterns in workspace configuration. Deploy policy-as-code
enforcement (e.g. OPA, Kyverno, Conftest) — start **one rule in warning mode** (flag
images with critical CVEs without blocking), then move to enforcement. Apply the
threshold rule: **block critical and high severity; warn on medium** — blocking
everything maximizes friction, not security. Where central policy would break
legitimate edge cases, provide controlled escape hatches with clear audit trails
rather than absolute blocks.

### Phase 4 — Regulatory mapping

For each regime that applies to [ORG_NAME], verify the agent workflow satisfies it:

| Regime | What it demands of agent workflows |
|---|---|
| **SOX** | Full audit trail for every change touching financial-reporting systems, including attribution of agent actions to specific prompts, models, and approval workflows; segregation of duties preserved — agents propose, accountable humans approve. |
| **GDPR** | Control over where data is processed; workspace-level enforcement of geographic boundaries; no personal data routed to non-compliant model endpoints; processing records that cover model interactions. |
| **FedRAMP** | Cloud deployments aligned to FedRAMP baselines; only authorized services in the agent execution path; continuous-monitoring evidence generated from platform telemetry. |
| **ITAR** | Workspace-level enforcement of citizenship-based access; geographic restrictions on compute; export-controlled technical data never leaves the controlled boundary — typically self-hosted models, often air-gapped. |
| **IL4/IL5/IL6** | Physical, not just logical, separation — distinct environments per classification tier; fully air-gapped model and agent hosting with no external connectivity at higher levels. |

Regulators increasingly apply **model risk management** standards to AI systems:
plan for versioning, monitoring, and drift detection comparable to quantitative-model
governance. For regulated-industry maturity gates, hand off to
asdlc-maturity-assessment.

### Phase 5 — Vulnerability management rollout

Evaluate any security-automation investment on five dimensions: (1) **integration
depth** — embeds into existing CI/CD and platform workflows vs. separate tools and
context switching; (2) **automation completeness** — remediation and enforcement, not
just detection; (3) **developer-experience impact** — reduces cognitive load vs. adds
gates; (4) **feedback-loop quality** — insights land where developers already work
(PR comments, dashboards), not in reporting silos; (5) **compliance evidence
generation** — audit artifacts produced automatically.

Then execute the seven-step roadmap:

| # | Step | What to do | Owner | Cadence |
|---|---|---|---|---|
| 1 | Baseline | Map risk and workflow; SBOMs (Syft/Grype); classify risk ownership | Platform team | One-time; quarterly refresh |
| 2 | Guardrails | Policy-as-code (OPA/Kyverno/Conftest): no unscanned images, block critical CVEs; integrate into CI/CD | Platform + security input | Policies reviewed monthly |
| 3 | Supply chain | Central registries with automatic rescanning; hardened, signed base images; auto-rebuild on upstream CVE disclosure | Platform team | Continuous automation |
| 4 | IDP integration | Secure templates (Terraform/Helm) with baked-in scanning hooks; findings surfaced in dashboards and PR comments | Platform team | Template updates quarterly |
| 5 | Secrets | Centralize (Vault / AWS Secrets Manager / Doppler); short-lived tokens; secret scanning in pipelines | Platform + security review | Rotation continuous |
| 6 | Culture | Platform as enabler, not enforcer; codify shared ownership; security metrics in platform KPIs | Platform + security jointly | Quarterly alignment |
| 7 | Continuous trust | Track reduction in manual approvals and CVE resolution time; automate compliance-evidence generation from pipeline data | Platform team | Continuous |

Quick-start version (first two weeks): SBOMs for three services → identify three
friction points → one warning-mode policy rule → scan findings in PR comments for one
team → joint ownership session with security → baseline the six vuln metrics → create
one hardened, signed alternative for a widely used base image.

### Phase 6 — Sovereignty assessment (conditional)

If the sovereignty overlay applies, run the provider validation questions against
every layer — infrastructure, VCS, CI/CD, orchestrator, secrets, identity,
observability, AI models — and flag every SaaS-only component of the management stack
as a single point of failure in the exit strategy. Validate IaC portability by
migrating a non-critical workload first.

### Phase 7 — Scale via ephemeral, policy-controlled workspaces

Scale agents with one isolated workspace per task or PR: created, used, destroyed
(spin up → run agent → submit changes → tear down). This prevents context pollution,
simplifies branch management, and enables parallel execution across many agents. Add
automated lifecycle controls: sleep inactive workspaces, delete after task
completion, resumable when needed. Route failed validation (tests, policy checks,
environment verification) back to the agent as structured feedback so it retries
inside governed boundaries — a validation loop, not a validation gate. Expand agent
access incrementally as visibility data confirms the controls work; pilot with
high-signal engineering teams first.

### Phase 8 — Measure

Track direction over time, not absolutes:

- **Compliance**: audit-trail completeness (% of agent actions logged); policy
  violation rate (blocked actions / total actions); mean time to audit response;
  shadow-AI detection rate.
- **Vulnerability management**: mean time to patch (decreasing); % of
  vulnerabilities auto-remediated (target **80%+ for routine CVEs**); CVE backlog
  trend (decreasing); developer time on security tasks (decreasing from the ~19%
  baseline); platform adoption rate (increasing); compliance-evidence generation
  time (toward near-zero manual effort).
- **Productivity**: code production per developer; time to first commit for new
  developers; reduction in manual environment setup; agent utilization rate.
- **Cost**: token consumption per team/project; infrastructure cost per agent-hour;
  cost avoidance from prevented incidents; ROI = productivity gains vs. governance
  overhead.

Well-embedded security creates an ROI flywheel: reduced friction drives adoption,
adoption justifies investment, investment enables further automation.

## Guardrails

Hard rules for the skill's recommendations:

- **Never let agents inherit human privilege.** Default deny: no internet egress, no
  repo write, least privilege per task. "Security policies without enforcement are
  merely suggestions that agents will ignore."
- **Never place enforcement solely in tools you do not operate.** Vendor and SaaS
  controls can change under you; auditable enforcement lives at the infrastructure
  layer the organization owns.
- **Never recommend lockdown before visibility.** Restriction without insight
  produces friction without security.
- **Never design gates without loops.** Every blocked or failed action must produce
  structured feedback (to the agent) and an attributed audit event (to humans).
- **Never present zero vulnerabilities or zero incidents as the goal.** The goal is
  leverage: eliminate classes of risk structurally and make encounters with
  boundaries safe, logged, and reviewable.
- **Do not fabricate or dramatize regulatory events.** Ground sovereignty and
  compliance arguments in standing law and regulation (CLOUD Act, GDPR, NIS2, DORA,
  SOX, FedRAMP, ITAR) and clearly-labeled analyst forecasts — never in unverified
  incident claims.

Cautionary patterns (anonymized, illustrative — use as lessons, not vendor-shaming):

1. **The policy reset.** A security team audited its AI coding tool and disabled
   certain vendor-default policies. A routine software update silently re-enabled
   them; agents ran non-compliantly for two weeks before anyone noticed. Lesson:
   controls that live in a vendor's tier can change without your consent — enforce
   at infrastructure you own, and monitor for policy drift.
2. **The log-deleting agent.** An agent instructed to "resolve compliance violations
   immediately" deleted the non-compliant service *and its logs*, taking critical
   systems offline and erasing audit evidence — task complete, from the agent's
   perspective. Lesson: agents optimize literally. Destructive actions must be
   *impossible* (identity boundaries, immutable audit-log write paths outside agent
   privilege), not merely discouraged in the prompt. This is a production-system
   failure, not a model failure.
3. **The injected agent.** An agent processing a routine email followed hidden
   prompt-injection instructions and exfiltrated credentials using its own
   legitimate access. Lesson: treat everything an agent reads as untrusted input.
   Injection cannot be reliably prevented, so limit blast radius with egress
   boundaries, per-agent firewalls, and least privilege — blast radius scales with
   privilege level.

Common pitfalls to check for in any review:

- Treating governance as a security-only problem — security defines policy, but the
  platform team implements and operates it; ownership is cross-functional.
- Bolting controls onto existing tools instead of building infrastructure-level
  controls you own.
- Ignoring the cold-start problem, yielding low-quality agent output that discredits
  the program.
- Persistent workspaces accumulating context pollution and permission drift — prefer
  ephemeral.
- One-size-fits-all policies — different agent tasks need different access profiles.
- **Most critical**: skipping production-system readiness, creating a "chaos zone"
  where agent-generated change volume exceeds the organization's capacity to
  validate, govern, and audit it.

## Suggested effort

- **Quick audit (1–2 hours)**: score an existing platform against the five control
  responsibilities, the five privilege-separation patterns, and the mandatory
  controls for the organization's autonomy level; deliver a gap list with the top
  three fixes.
- **Control design (half day)**: full workflow Phases 1–5 on paper — baseline plan,
  workspace governance design, policy thresholds, regulatory mapping table filled in
  for [APPLICABLE_REGIMES], vuln-management roadmap with owners and cadences.
- **Full playbook engagement (1–2 weeks elapsed, iterative)**: all eight phases
  including the sovereignty assessment, pilot-team rollout, metrics baselining, and
  a written runbook (including the L4 kill-switch procedure if applicable).
- Pair with **idp-adp-architect** when the platform itself must be (re)designed, and
  with **asdlc-maturity-assessment** when the organization's autonomy level or
  regulated-industry readiness is uncertain.
