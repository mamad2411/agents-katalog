---
name: idp-adp-architect
description: Design, evolve, or audit an Internal Developer Platform and its human-facing Internal Developer Portal into an Agentic Developer Portal (ADP) that lets AI coding agents consume organizational context and platform capabilities safely alongside engineers. Use to design or review platform reference architecture, cloud tool stacks, portal experiences, golden paths, abstraction layers, AI/ML or data platforms, Kubernetes fleets, platform observability, sovereign or exit-ready platforms, or agent identity, sandboxing, evaluation, and guardrails. Also fires on "Internal Developer Portal," "Internal Developer Platform," "ADP," "Agentic Developer Portal," "platform engineering," "platform orchestrator," "golden path design," "reference architecture," "fleet management," "digital sovereignty," or "platform architecture for AI agents."
---

# Platform → ADP Architect

## Purpose
Take the evidence catalog from `platform-maturity-discovery` and produce a concrete architecture: what to build, in what order, to let both human developers and AI coding agents work safely and productively through an Agentic Developer Portal over shared platform capabilities. Covers generic service platforms, portal interfaces, AI/ML extensions, cluster-fleet operations, observability design, and sovereign/exit-ready variants. For security and governance control design, pair with `platform-security-playbook`.

## Core model to hold in your head

### Portal, platform, and ADP

- An **Internal Developer Portal** is a human-facing interface for discovery and consumption: catalog, search, documentation, scorecards, templates, and self-service entry points. It is a subset of the experience, not the backend platform.
- An **Internal Developer Platform** standardizes the repeatable parts of software delivery through APIs, orchestration, infrastructure, policy, identity, observability, and support. It owns coordination, compliance, and repeatability — never the creative work itself.
- An **Agentic Developer Portal (ADP)** expands the portal into a governed human-and-agent interaction surface over the platform. Agents need machine-consumable context and capabilities plus identity, execution boundaries, evaluation, audit, and feedback.

Avoid using “IDP” alone because it is commonly expanded as either portal or platform. Write the intended term in full. Note the multi-platform reality: large enterprises may run separate service, data/AI, mobile, and frontend platforms; align their interfaces rather than pretending one backend serves all workloads.

### The five-plane reference model
An Internal Developer Platform is organized around five planes. Think planes, not layers: layers imply strict hierarchy and sequential dependencies; planes are parallel concerns that intersect and can each be evolved or swapped independently.

1. **Developer control plane** — how developers declare intent: IDE/CDE, copilots/agents/LLM interfaces, portal, CLI. Rule: code as truth, interface as enabler — portals, chat, and CLIs are access layers, but every change is logged and versioned as code; Git is the single source of truth and complete system record.
2. **Integration & delivery plane** — version control, workload spec, IaC, CI, image registry, platform orchestrator, CD. The orchestrator models the estate as a graph (which app connects to what resource in which environment), owns central RBAC, and consumes CI metadata to trigger and manage deployments.
3. **Resource plane** — compute, data stores, networking, storage, messaging; provisioning of infra and environments.
4. **Security plane** — code analysis, secrets, identity, policy control, network security, security suites; spans the whole architecture as its foundation.
5. **Observability plane** — monitoring/logging, observability, FinOps, incident management; spans all other planes.

Per-cloud tool mapping (vendors are EXAMPLES filling category slots):

| Category slot | AWS example | Azure example | GCP example |
| --- | --- | --- | --- |
| Portal | Backstage | Backstage | Backstage |
| Coding agent | Claude Code | GitHub Copilot | Claude Code |
| VCS + CI | GitHub + GitHub Actions | GitHub + GitHub Actions | GitHub + GitHub Actions |
| Workload spec | Score | Score | Score |
| Platform IaC | Terraform / OpenTofu | Terraform / OpenTofu | Terraform / OpenTofu |
| Platform orchestrator | Humanitec | Humanitec | Humanitec |
| CD (GitOps operator) | Argo CD | Flux CD | Argo CD |
| Image registry | Amazon ECR | Azure Container Registry | Google Artifact Registry |
| Compute (K8s) | Amazon EKS | AKS | GKE |
| Database | Amazon RDS | Azure SQL | Cloud SQL |
| DNS / networking | Route 53 | Azure DNS | Cloud DNS |
| Messaging | Amazon SQS | Azure Service Bus | Pub/Sub |
| Secrets | HCP Vault | Azure Key Vault | Google Secret Manager |
| Identity | AWS IAM | Okta | Google Cloud IAM |
| Policy control | OPA | OPA | OPA |
| Code analysis | Sourcegraph | Codacy | SonarQube |
| Network security | Prisma Cloud | Cilium | Cilium |
| Monitoring / logging | CloudWatch | Azure Monitor | Cloud Monitoring |
| Observability | Datadog | Prometheus + Grafana | Honeycomb |
| FinOps | Kubecost | CloudZero | Flexera |
| Incident mgmt | Rootly | PagerDuty | PagerDuty |

**The cross-cloud lesson: the category slots ARE the architecture; the vendors are pluggable.** Argo CD and Flux CD swap freely; AWS IAM and Okta swap freely; Datadog and Prometheus+Grafana swap freely — nothing else in the design changes. Only the resource-plane picks and a few native services (registry, monitoring, IAM, DNS) are cloud-specific. The portable invariants across every cloud: Backstage, GitHub + Actions, Score, Terraform/OpenTofu, a graph-based platform orchestrator (e.g., Humanitec), and OPA. When designing a stack, name the category slot first, then pick a vendor for it — never the reverse. And keep each cloud's stack internally consistent: never put one cloud's native service in another cloud's stack.

### Five design principles
1. **GitOps first** — every edit action in the platform is represented as a code change; the full state of all systems (service, infra, tool config) is versioned as code; any modification, whether UI-initiated or agent-initiated, triggers a git pull request. This guarantees DR/backup readiness and is the ideal audit log at scale.
2. **Backend first** — a platform is only as good as its backend. The orchestrator (or well-tuned pipelines) is the brain: it owns role/access management and stores a graph-based representation of how services and resources fit together, versioned by deployment; API-first and documented. Without it, linear on-off pipelines accumulate tech debt fast.
3. **Secure by default** — least privilege, encryption in transit and at rest, secret RETRIEVAL not distribution, public exposure denied unless explicitly allowed, all changes validated via policy-as-code. When secure practices are built into every golden path, the safest way becomes the easiest way.
4. **Observability by default** — every component emits metrics/logs/traces by default, in standardized formats, centrally aggregated; SLOs per platform capability with alerts tied to error budgets.
5. **AI-augmented, CLI-first** — copilots/LLMs/agents in IDEs, CLIs, and portals automate config writing, pipeline debugging, and doc generation, and analyze telemetry to predict issues. Hard rule: when an LLM goes beyond code assistance to trigger infra/environment changes, the action must execute through a trusted CLI or the orchestrator API — never direct console or raw cloud-API mutation — so every AI-driven action stays governed, RBAC-enforced, and auditable.

### Capability portfolio and sourcing discipline
Treat the platform as a portfolio of internal products, not one giant implementation project. Each capability — service scaffolding, environment creation, deployment, secrets, observability, data access, model serving — needs a named user segment, owner, value hypothesis, consumption interface, reliability target, cost-to-serve, and lifecycle state. A portal entry without an owned backend capability is catalog theater.

For every capability, make the **reuse / buy / assemble / build** decision explicitly:

| Choice | Prefer when | Evidence required |
|---|---|---|
| Reuse an existing enterprise service | It already meets the user need and control boundary | Fit-gap, integration cost, service owner and SLO |
| Buy a managed product | The capability is commodity and operating it is not differentiating | Total cost, portability/exit path, security and data-boundary review |
| Assemble open components | The interfaces are stable but local integration creates value | Integration ownership, upgrade plan, compatibility tests |
| Build custom | The workflow is materially differentiating or no option meets a hard constraint | User evidence, full lifecycle cost, staffing, support and deprecation plan |

Default to the least custom option that satisfies the requirement. “We can build it” is not a reason; custom code creates a permanent product, support, upgrade, and security obligation. Record decisions in a capability register with: user/problem, selected option, rejected alternatives, owner, API/interface, SLI/SLO, dependencies, unit cost, adoption signal, version policy, exit plan, and review date.

Every production capability also needs an internal service contract. At minimum define the measured indicator, target objective, support and incident path, maintenance expectations, compatibility window, and exception process. The contract turns self-service from an interface promise into an operable service.

### Abstraction layers & golden paths (how humans/agents actually consume the platform)
A **golden path** is the intended, low-friction way to accomplish a task — a paved road codifying tribal knowledge into repeatable self-service, with security, compliance, and observability built in, plus "break-out" flexibility for novel cases. Abstraction layers make golden paths possible:

- **Front-end abstractions** — for usability: portals (Backstage/Cortex/Port-style), CLIs, declarative config (Score/Radius/Kubevela-style), natural-language interfaces, exec dashboards. Prefer visual/low-code interfaces with sane defaults, and let one persona's interface surface data another persona cares about (e.g., show cost to the developer requesting infra). For an opinionated Azure implementation profile of this architecture (Radius + Dapr + Azure Verified Modules + Flux + central Managed Grafana), hand off to the companion `azure-platform-engineering` plugin — this skill stays cloud-neutral.
- **Back-end abstractions** — for automation & standardization: unified platform APIs, orchestrators that fill in missing config, an abstraction over IaC itself so requesters never touch raw modules. Golden rule: **self-service fails without standardization, and standardization is worthless without automation built on top of it.**

A good abstraction generalizes away detail that doesn't matter; a bad one (an "illusion") hides detail that does matter and misleads the user. Only abstract when the "why" is clear and the impact is real.

Two canonical golden-path walkthroughs to design against:

- **Developer self-service resource request** (day-2, developer-initiated): dev states intent in natural language → LLM translates it to a precise CLI command → GitOps workflow opens an auto-generated PR against the workload spec (e.g., adding a storage resource to `score.yaml`) → merge triggers CI build → security-plane code analysis scans → image lands in the registry → orchestrator reads metadata + app context, selects the matching infra template → checks identity management for the developer's permission → sign-off (senior/security approvals as needed) → orchestrator executes the template's IaC against the cloud API → secrets manager retrieves the new credentials and injects them into the container environment (never exposed) → resource becomes a node in the platform graph, monitored by default, surfaced in the portal. The chained interplay — LLM → CLI → Git → CI → security → orchestrator → IAM → IaC → secrets → observability → portal — is the test of whether the planes are actually wired together.
- **Platform-engineer fleet update** (fleet-initiated): (1) engineer edits the shared resource template in the IDE while a policy engine analyzes the change in real time against security/compliance rules, flagging misconfigurations before they're introduced; (2) the portal shows every affected resource with version history per environment, and a SIMULATION models the impact on existing configs to catch conflicts pre-apply; (3) the orchestrator rolls out progressively — a small subset of dev resources first, then a larger percentage, then staging — minimizing blast radius with fast rollback; (4) observability collects metrics/logs throughout with anomaly alerts and a live rollout view.

### Resource-plane depth: cluster lifecycle & fleet management
Kubernetes is the de facto resource plane, and the enterprise reality is a fleet — a **"nation of cities"** (one cluster = a city of workloads; the fleet = a nation), driven by isolation/blast-radius control, diverse environments (clouds, DCs, edge, sovereign/air-gapped), and specialized workloads (GPU/AI). Manage every cluster on a planned journey:

- **Day 0 — blueprint**: define the complete production-ready cluster as a reusable declarative template covering every layer, not just the distro: OS choice (Ubuntu/RHEL/micro-OS), K8s distribution per use case (e.g., K3s for lightweight, RKE2 for FIPS), CNI and CSI choices, and core services baked in (observability stack, ingress + TLS, secrets management, policy agents like OPA Gatekeeper or Kyverno). Maintain distinct blueprints per cluster class (web, data, GPU/AI, edge).
- **Day 1 — provisioning & placement**: instantiate from the blueprint via automation (commonly Cluster API) across clouds, on-prem, edge, and sovereign locations; watch consistency assumptions (cloud clusters assume elastic resources; edge clusters are memory-constrained).
- **Day 2 — the relentless operation**: three major K8s releases a year mean multiple upgrades per cluster annually, plus OS patches, constant certificate rotation (missed expiries cause outages), autoscaler tuning (HPA/VPA/KEDA/Karpenter), CVE hotfixes, DR testing, and continuous policy enforcement.

Survival principles: automation is survival (an unautomated cluster activity "must be considered unreal"); cattle, not pets (clusters rebuilt from templates, not endlessly patched); guard against drift (GitOps reconciliation loops continuously detect and remediate deviation from the declared state — drift is how "snowflake" clusters are born).

At fleet scale, add a fleet-level control plane and five disciplines: fleet-wide observability, progressive rollouts, standardized blueprints, policy propagation as versioned code, and exception workflows (temporary deviations with ownership, expiry, and automatic reconciliation). Measure fleet maturity with data, not instinct: **percentage of clusters at N-1 version, average drift remediation time, CVE time-to-patch, and fleet error budgets.**

### Observability-plane depth
Core distinction: **monitoring** is the practical act of collecting telemetry (tells you something is wrong); **observability** is a property of the system — the ability to determine any internal state by asking questions from outside (explains why it's broken). Platform teams carry a **dual mandate**: (1) observe their own infrastructure (K8s, CI/CD, shared services, databases, brokers), and (2) provide observability-as-a-service to application teams — a paved path to visibility with instrumentation by default.

Judge every telemetry stream against the four-part quality rubric:
1. **Semantics** — is what the data represents clearly defined?
2. **Context** — does it capture where/under what conditions it was generated (service version, region)?
3. **Relations** — is it linked to related signals (a log pointing to its trace)?
4. **Accuracy** — is it correct and reliable?

Backbone: OpenTelemetry semantic conventions (shared vocabulary and resource attributes like `service.name`, `cloud.region` — without them, conflicting labels break queries and dashboards) + the OTel Collector as the platform's telemetry router and policy engine (sample high-volume traces, redact sensitive fields, drop debug logs — all without touching application code) + the OTel Operator for auto-instrumentation. Cross-signal correlation is the payoff: metric alert → the specific slow trace → the correlated log lines naming the deployment at fault. Treat dashboards and alert rules as code (YAML in Git, PR-reviewed, deployed via CI — e.g., with Perses), never hand-edited in a UI. Design telemetry to answer specific failure-mode questions, not "instrument everything."

### AI/ML platform extension: the sixth plane
A generic services platform will not cover data/AI/ML workloads: they add specialized infrastructure (GPUs), a distinct tool landscape, and a broader user base (data scientists, ML engineers, data engineers, BI analysts). Extend the model:

- **Sixth plane — Data & Model Management**: metadata store capturing lineage and artifacts from every pipeline run; feature store providing consistent feature definitions for batch training AND real-time inference (kills train-serve skew); model registry with versioning, aliasing (staging/production), and **model cards** (purpose, performance, training data, ethical considerations, usage guidelines) for governance and reproducibility.
- **Dual-orchestrator pattern**: the platform orchestrator (e.g., Humanitec) handles platform-level configuration and environments; a specialized ML workflow orchestrator (e.g., Kubeflow Pipelines) manages the multi-step graphs of training, evaluation, and validation. Both consume from the same artifact registry. Add CT (continuous testing) to CI/CD.
- **Developer control plane** adds a notebook workspace category (e.g., Jupyter) — self-service, GPU-enabled, compliant notebooks provisioned in minutes from templates, no tickets.
- **Resource plane** adds streaming systems (e.g., Kafka), GPU-aware scheduling and node pools, and a dedicated model-serving layer (e.g., NVIDIA Triton for multi-framework inference, backed by a low-latency cache for feature lookups).
- **Observability plane** adds model observability (drift and hallucination detection — e.g., Arize), data validation/quality monitoring (e.g., Monte Carlo), and a lineage & metadata catalogue linking execution logs to source models and data for full auditability.
- **Security plane** adds **model scanning** (automated gates checking model artifacts for licensing compliance, bias, PII leakage, and vulnerabilities before production — e.g., Protect AI) and treats **model weights as secrets** (stored in the secrets manager, injected at runtime, never hardcoded). New threat class: adversarial attacks.

Adoption order: start with one or two high-impact golden paths (secure notebooks, automated training pipelines), expand gradually (training → serving → sophisticated pipelines), make security and observability Day-1 priorities, and align early on what constitutes a "workload" (training job, inference endpoint, data pipeline) so interfaces, policy, and cost attribution stay consistent.

### Sovereign variant (exit-by-design)
When jurisdiction risk or regulation (GDPR, NIS2, DORA) is in scope, treat **jurisdiction analysis as an architecture input**: the US CLOUD Act compels US providers to hand over data regardless of where it is physically stored, while GDPR prohibits such transfers — so **data residency ≠ data sovereignty**; a compliant data center under a foreign-jurisdiction control plane is only partial sovereignty. DORA additionally demands a *tested*, operational exit capability, not a filed document. Design moves:

- **Open-source-first, self-hosted slots**: every management-stack component (VCS, CI, orchestrator, secrets, IAM, observability) must be self-hostable under the org's legal control — e.g., Gitea/Forgejo for VCS, Keycloak for identity, Vault/OpenBao for secrets, Harbor for registry, Prometheus+Grafana for observability, OPA for policy. Locally hosted open-weight models for AI assistance where proprietary copilots would leak IP into foreign training pipelines.
- **GitOps + OpenTofu as the exit mechanism**: everything-as-code in a self-hosted repo means the org possesses its entire business state as code; disaster recovery or forced provider exit = point the GitOps controller at a new cluster on a different provider and reconstruct from scratch. Prefer OpenTofu over restrictively licensed IaC to remove single-vendor license risk. Air-gapped operation is the ultimate stress test: the whole platform should be able to run in an isolated DC.
- **Validate provider claims** with hard questions: does the provider hold regional sovereignty certifications (e.g., SecNumCloud, BSI C5)? Is data physically stored exclusively in the designated jurisdiction? Is the provider corporately immune to extraterritorial data requests? Is the orchestrator framework-agnostic (deploys to sovereign AND global providers without vendor-specific plugins)? Are keys, secrets, and IAM self-hosted rather than cloud-native managed? Are AI assistants hosted on local/sovereign infra with explicit no-training guarantees? Segment workloads: sensitive/regulated → sovereign providers; non-sensitive elastic → hyperscalers treated as pure commodity behind abstract IaC.

### What changes when agents join
Coding agents are not autocomplete — they become actors across the lifecycle: retrieving context, writing code, opening PRs, validating output, responding to signals. That breaks the assumptions a human-only portal and platform were built on (one human per step, human-speed pacing, human judgment at every gate). Agents act fast, in parallel, don't tire, and don't exercise judgment — so a platform that isn't ready will amplify chaos, not throughput. **A shaky platform does not get better when you add agents — it gets worse, faster.** Do not build an ADP over an immature platform; fix the foundation first.

### What an ADP is
An Agentic Developer Portal is the evolved interaction and orchestration surface over the Internal Developer Platform: it lets agents consume organizational context and the same governed capabilities humans use, at whatever autonomy level the organization permits. Where a conventional Internal Developer Portal assumes a human navigates and triggers every path, the ADP supports both human and machine entry points across a spectrum of supervised execution.

The ADP has three layers:

1. **Tooling layer (top)** — the same five (or six) planes above, now under much higher load (agents call tools repeatedly, in parallel, at volumes no human workflow anticipated).
2. **Path definitions (middle)** — the operational backbone. A "path" is how any actor (human or agent) invokes work. Every path is one of three types:
   - **Deterministic** — pipeline-driven, gated, repeatable (the CI/CD lineage that already exists; unchanged by agents).
   - **Probabilistic** — agent-driven work verified by evals and humans (drafting a spec, reviewing a PR, generating release notes).
   - **Hybrid** — a loop: probabilistic step → deterministic gate → retry with enriched context until it passes. **This loop is where the actual productivity gains live** — treat a first-pass agent failure as expected, not as a defect, and design the retry loop rather than trying to make agents right on the first try.
3. **Agent infrastructure (bottom)** — the constant substrate under everything, made of seven components: **identity** (who is acting), **context** (what it knows), **capability** (what it's allowed to do), **execution** (where it runs — sandboxed, ephemeral workspaces), **evaluation** (is the output acceptable), **security** (guardrails against misuse), **observability** (what happened, auditable after the fact).

Deterministic paths can run on the tooling layer alone and don't need agent infrastructure — that's intentional. Apply autonomy where judgment creates value, and keep determinism where it already wins. The ADP's agent needs land on the platform's existing principles: GitOps-first gives every agent action a PR-shaped audit trail, and the CLI-first rule gives agents a governed execution channel — an organization that built those in already has the ADP's spine.

## Workflow

1. **Intake.** Consume the discovery charter, evidence catalog, maturity readings, and ADP readiness gates from `platform-maturity-discovery`. If they do not exist, run that discovery first. Then establish:
   - What exists today: which Internal Developer Portal interfaces and Internal Developer Platform capabilities exist? Which of the five planes are mature vs. missing?
   - Systems of record: work tracker (GitHub Issues/Projects, Jira, Azure Boards), repo host (GitHub, Azure Repos) and its branch protections/rulesets, and CI/CD (GitHub Actions; Azure DevOps Pipelines — note YAML vs. Classic mix, since Classic UI-defined pipelines are not version-controlled and are a governance liability for the deterministic gates agents depend on). For a full audit checklist of these sources, use the `asdlc-maturity-assessment` skill's "Evidence sources & audit playbook."
   - Cloud/infra context: hyperscaler(s), Kubernetes or not, cluster count and fleet shape (single cluster? tens? edge/sovereign locations?), regulated industry or not.
   - Workload mix: standard services only, or data/AI/ML workloads too (training, serving, notebooks, GPUs)? If AI/ML, plan the sixth plane and dual orchestrators.
   - Sovereignty exposure: EU-regulated sector (NIS2/DORA), public sector, defense, or jurisdiction-sensitive IP? If yes, apply the sovereign variant.
   - Current AI agent usage: none / autocomplete only / agents opening PRs / agents running unsupervised.
   - Team size and platform team size/maturity.
   - What's motivating this now (cost, incidents, developer complaints, a mandate to "adopt AI agents").
   - Capability portfolio: which platform services exist, who owns and supports each, how users consume them, what they cost, and which are duplicated or ownerless.
2. **Diagnose.** State plainly which of these is true and why:
   - *No real Internal Developer Platform yet* → build the platform foundation first (five planes, golden paths for the top recurring developer requests). A portal UI does not close this gap.
   - *Solid platform and conventional portal, no/limited agent usage* → this is the ADP greenfield case. Proceed to step 3.
   - *Agents already in use ad hoc* → flag the gap explicitly: the organization has agentic behavior without an ADP control surface (identity, sandboxing, evaluation, and audit), even if it looks like just "better autocomplete."
   - Also diagnose the resource plane: if >30–50% of clusters are hand-managed snowflakes with no declarative blueprints, fleet lifecycle work belongs in phase one.
3. **Design the platform**, plane by plane and layer by layer:
   - Map every plane's category slots to concrete tools using the per-cloud table — category first, vendor as example; keep the stack internally consistent per cloud; verify the five design principles are structurally enforced (GitOps trail, orchestrator brain, policy-as-code defaults, telemetry by default, CLI-first AI actions).
   - Tooling: which planes need to scale/harden for agent-volume traffic (rate limits, cost controls per identity, parallel environment provisioning).
   - Paths: enumerate the 3–5 highest-value paths (e.g., "PR review," "dependency bump," "self-service resource request," "fleet template update," "incident remediation") and classify each as deterministic / probabilistic / hybrid. For every hybrid path, specify the gate and the retry/context-enrichment mechanism. Model the two canonical walkthroughs above.
   - Agent infrastructure: for each of the seven components, name the concrete implementation choice (e.g., identity = short-lived scoped service accounts per agent session; execution = ephemeral sandboxed workspace per session; observability = agent action log distinct from human audit log).
   - If AI/ML is in scope: add the Data & Model Management plane, the ML workflow orchestrator, notebook golden paths, model scanning gates, and drift/data-quality observability.
   - If sovereignty is in scope: run the validation questions, mark which slots must be self-hosted, and specify the exit test (can the platform be reconstructed on a different provider from Git alone?).
   - For each proposed capability, record the reuse/buy/assemble/build decision, lifecycle owner, service contract, unit-cost measure, compatibility policy, and exit/deprecation plan before selecting a product.
4. **Sequence it.** Never propose everything at once — sequence by the four levels of agentic maturity (see the `asdlc-maturity-assessment` skill for the full rubric): most orgs should build for Level 2 next (dispatch path + validation loop + agent identity + sandboxing) regardless of long-term ambition, because that's the hardest and highest-leverage jump. For platform-side work: golden paths for the top recurring requests first, then fleet/lifecycle automation, then AI/ML extension — security and observability as Day-1 properties of each phase, never retrofits.
5. **Output.** Produce an architecture brief with: current-state diagnosis, target design plane-by-plane (with the tool-mapping table filled in for their cloud(s)), a capability register and sourcing decision log, internal service contracts, the golden paths and abstraction layers needed, ADP layers if in scope, a phased build sequence with fleet/observability maturity metrics to track, and explicit call-outs of what NOT to build yet.

## Guardrails
- Never recommend agent autonomy features (auto-merge, unsupervised background execution) without the identity/sandboxing/evaluation infrastructure underneath them being explicit in the plan.
- If the organization lacks a working Internal Developer Platform, say so directly and scope down — an ADP interface is not a fix for missing platform capabilities.
- Keep the abstraction-layer guidance honest: flag if a proposed "portal" would be an illusion (hiding detail that still matters) rather than a real abstraction.
- Hold the CLI-first line: any LLM- or agent-triggered infra/environment change must route through a trusted CLI or the orchestrator API with RBAC and audit. If a design lets a conversational interface mutate infrastructure directly, call it out as a defect.
- Architecture is category slots, not vendors: when recommending a stack, name the category first and present vendors as swappable examples; double-check that every pick is native to the target cloud (no cross-cloud service leakage into a stack).
- Don't bolt AI/ML workloads onto a generic services platform — if training, serving, or notebooks are in scope, the sixth plane and the ML workflow orchestrator are structural requirements, not add-ons.
- On sovereignty claims, distinguish data residency from data sovereignty; a foreign-jurisdiction control plane over local data centers is only partial sovereignty, and an exit strategy that has never been tested is a document, not a capability.
- Never approve custom build work without a differentiated user need, full lifecycle owner, operating cost, and exit/deprecation plan.
- Never call a capability self-service until its reliability, support, compatibility, and exception expectations are explicit.

## Suggested effort
Medium–high — this produces a multi-section architecture document, not a quick answer.
