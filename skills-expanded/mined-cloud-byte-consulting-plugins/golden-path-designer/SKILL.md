---
name: golden-path-designer
description: >-
  Design golden paths as versioned products for human and AI-agent users,
  using maturity levels, Thinnest Viable Platform scoping, Backstage
  templates, Crossplane abstractions, CI gates, and adoption metrics. Use for
  paved roads, self-service workflows, service or experiment scaffolds,
  platform MVP/TVP work, OPA/Kyverno/KubeLinter controls, template drift,
  clone-and-forget problems, or machine-executable onboarding paths.
---

# Golden Path Designer

## Purpose
A golden path is the intended, low-friction way to accomplish a task — tribal knowledge codified into repeatable self-service with security, compliance, and observability built in, plus break-out flexibility for novel cases. This skill designs golden paths as **products**, not templates: scoped by hypothesis, implemented as versioned abstractions, gated in CI, measured by lifecycle-phase KPIs — and, for the ADP end-state, executable by agents through APIs, because in an Agentic Developer Portal the paths built for human researchers are the same paths agents run. Self-service fails without standardization, and standardization is worthless without automation on top — hold that chain through every design.

## Core model to hold in your head

### The 3-level golden-path maturity model (with per-level implementation moves)
| Level | State | Failure mode | Implementation focus at this level |
|---|---|---|---|
| 1. **No golden path** | Teams run their own DevOps practices; inconsistent CI/CD, observability, deploys | Wheel reinvention, unbounded drift | Design a baseline path with minimal standardization for the most common task; lead with the WHY (target outcome), let teams implement toward it |
| 2. **Clone-and-forget** | Central templates exist; teams clone, adapt, then diverge forever | The trap level: day-1 speed, day-2 abandonment — no upgrade channel, fixes never propagate | Expand coverage across more workflows with flexibility, but start building the product spine: version templates, track who cloned what, publish changelogs |
| 3. **Golden paths as products** | Paths deeply integrated into the IDP: versioned, upgradable, instrumented, owned | Over-rigidity if break-out routes are missing | Full integration: advanced capabilities in the path (canary, rollback, parallel builds), upgrade propagation to existing consumers, feedback loops, adoption telemetry |

The level-2→3 jump is the one that matters: the difference between a template and a product is that a product can be *upgraded after adoption*. If a security fix to the path can't reach the fifty services already scaffolded from it, you have clone-and-forget with better marketing. This model is also the sharpest probe for the Interfaces aspect in `platform-maturity-benchmark`.

### TVP scoping: hypothesis → validate → expand
Never design the path catalog first. Apply Thinnest Viable Platform discipline:
1. **Pick the use case** by scoring candidates (frequency × pain × implementation ease) — for a GPU research division: onboard a new experiment, submit a training job, get an inference endpoint, access observability data, onboard a dataset.
2. **Write the product hypothesis** — a falsifiable value statement per use case ("a paved experiment-onboarding path cuts lead time from first commit to first training run by 20%"). The hypothesis doubles as the internal pitch to the leadership funding the platform.
3. **Build the thinnest implementation** that can validate it with early adopters; good enough to ship beats feature-complete.
4. **Build–measure–learn:** once the hypothesis is proven with early adopters, open it to the org and let the early adopters do the promotion. Only then expand to the next path.

Competition is real even internally — it's every team hand-rolling their own tooling; the TVP must beat that alternative on day one for its narrow use case.

### Implementation pattern: Backstage Software Templates + Crossplane abstractions
The productized path has a front and a back:
- **Front: Backstage Software Templates** (scaffolder) — the parameterized entry point. The researcher (or agent) supplies name, team, GPU tier, framework; the template generates the repo from a skeleton (source layout, CI workflows, scorecard config, `catalog-info.yaml`), registers the component in the catalog, and wires ownership metadata. The template's parameter schema is the path's contract.
- **Back: Crossplane composite abstractions** — the platform team defines composite resource types (XRDs) like `GPUTrainingEnvironment` or `ExperimentWorkspace` that encapsulate the real infrastructure (namespace, quota, storage, node-pool/GPU class, network policy, service accounts); consumers claim the abstraction, never the raw resources.
- The abstraction test: a good abstraction generalizes away detail that doesn't matter; a bad one (an "illusion") hides detail that does. Expose the knobs researchers genuinely vary (GPU count/type, storage size), bury the rest under secure defaults.
- The pairing end-to-end: template scaffolds the claim + repo → GitOps applies it → the composition provisions → the catalog shows the result. Every step is a PR-shaped, auditable code change.

**Alternative back-end substrate: Radius Resource Types + Recipes** (Azure-leaning stacks). Instead of Crossplane XRDs, the platform team defines abstract Resource Types (YAML/OpenAPI contracts) and implements them with Bicep or Terraform Recipes bound per environment — the same app definition deploys to dev, Azure Container Apps, or AKS because the environment's recipe binding decides the infrastructure, and Radius maintains a live application graph. Choose Crossplane when you want multi-cloud CRD-native abstractions with a mature ecosystem; choose Radius when the estate is Azure-first, recipes should reuse existing Bicep/Terraform (including Azure Verified Modules), and per-environment swap of compute/data backends is the product requirement — accepting its CNCF Sandbox maturity. The Azure implementation lives in the companion `azure-platform-engineering:radius-golden-path-builder` skill; this skill stays substrate-neutral.

### CI-enforced onboarding scorecards and maturity gates
Standards that live in wikis don't survive contact with deadlines — enforce the path's bar in the pipeline the path itself scaffolds:
- **KubeLinter** (or equivalent static analysis) validating manifests against cloud-native best practice, with platform-tuned check sets and custom checks, run via the scaffolded CI workflow on every PR.
- **OPA / Kyverno** policy-as-code gates: mandatory ownership metadata, resource limits, no privileged pods, registry allowlists, GPU-quota annotations — evaluated on PR, not post-deploy.
- **Scorecards as maturity gates:** aggregate the checks into a per-service scorecard (metadata completeness, security posture, observability wiring, dependency health) with graduated tiers — a service must clear tier N to unlock tier-N capabilities (production deploy rights, higher GPU quota).
- Roll out new checks warn-only first, then promote to blocking — the cascading warning→error mechanic from `platform-fitness-functions`, which owns the instrumentation of these gates.

### Machine-consumable golden paths (the ADP requirement)
Agents execute the same paths humans do — which forces properties that also make paths better for humans:
- **Structured, not prose:** every path step is an API call, CLI invocation, or template execution with typed inputs/outputs — never "then ask in #platform-help." A path an agent can't execute end-to-end has a hidden manual step; find it and automate it or explicitly gate it.
- **API-driven:** the path is invokable via the platform API/orchestrator, with the portal and the MCP tool surface (`mcp-platform-api-author`) as equivalent front doors. Graph-based platform backends already model handover points for stakeholders "whether human or machine" — that's the substrate to target.
- **Definition of done per path:** explicit, checkable completion criteria (repo exists, CI green, claim bound, endpoint healthy) so an agent — or a human — knows the path finished. This is the same definition-of-done discipline the ASDLC demands for every path agents touch (`asdlc-maturity-assessment`, platform-assessment plugin).
- **Identity-aware:** path execution requires the caller's scoped identity (`agent-identity-engineer`); an agent scaffolding an experiment does so as a named session, within quota, on the audit plane.

### Path service contract and lifecycle

A golden path is an internal product backed by an operable service, not a template handed over once. Before launch, publish a compact contract:

- **Users and outcome:** target cohort, job to be done, value hypothesis, and explicit non-goals.
- **Interface contract:** typed inputs/outputs, compatibility window, versioning policy, and definition of done for human and agent callers.
- **Service contract:** owner/on-call route, SLI and SLO, support response expectation, maintenance windows, dependency status, and escalation path.
- **Economics:** cost shown to the requester where actionable, plus platform cost-to-serve per successful path completion.
- **Change policy:** upgrade channel, migration assistance, deprecation notice, rollback, and an observable exception/break-out route.

Review the contract with early adopters before promoting the path. Reassess it on a fixed cadence using completion failures, support themes, bypass reasons, satisfaction, and unit cost. Expand when demand and outcomes justify it; repair when users struggle; deprecate when a better path replaces it or maintained usage no longer justifies the cost.

### Adoption KPIs by lifecycle phase
KPIs only mean something against the platform's declared lifecycle phase — declare the phase, then read the numbers:

| Phase | Expected signal | Healthy | Red flag |
|---|---|---|---|
| **First adoption** | Support requests and cost-per-change RISE while few teams migrate | Rising engagement from early adopters | Zero support requests (nobody's trying) |
| **Ramp-up** | New apps/experiments onboard fast; support requests climb; cost-per-change stagnates | Migration velocity | Onboarding without retention (clone-and-forget) |
| **Optimization** | Support requests and cost-per-change drop steeply; onboarding peaks then tapers (market saturated); time-per-release flattens low | Steady KPIs independent of growth | Interpreting the taper as failure and cutting investment — flat cost with rising value is the product working |

Core adoption set: adoption rate (% of target users on the path), active users, time-to-first-success (signup → first training run), support requests per path, % of new services/experiments via path vs. bypass, and path completion rate (started vs. finished — agents surface this beautifully because their failures are logged). Interpret with context: falling support requests mean great docs OR abandonment; always pair a usage metric with an outcome metric.

## Workflow
1. **Locate the org** on the 3-level model per workflow area (scaffolding, CI/CD, observability, deploy) for [YOUR ORGANIZATION / CLIENT]; feed the reading to `platform-maturity-benchmark`.
2. **Score candidate paths** (frequency × pain × ease) against the research division's real workflows; pick ONE for the TVP.
3. **Write the hypothesis** with a measurable target and a named validation cohort of early adopters.
4. **Design the path and contract:** user journey (human AND agent variants), Backstage template parameter schema, Crossplane XRD/composition boundary (exposed knobs vs. secure defaults), the break-out route for novel cases, owner, service objective, compatibility window, unit-cost measure, and deprecation policy.
5. **Design the gates:** KubeLinter/OPA/Kyverno check set, scorecard tiers, warn→block promotion schedule.
6. **Make it machine-consumable:** API surface per step, definition of done, identity/scope requirements; hand the tool-card design to `mcp-platform-api-author`.
7. **Instrument** the lifecycle-phase KPI set before launch (baseline included); register path-health fitness functions with `platform-fitness-functions`.
8. **Validate, then expand:** run the cohort, test the hypothesis honestly, productize (versioning, upgrade channel, ownership) before starting path #2.
9. **Output.** A path product spec: maturity reading, scored candidate table, hypothesis, journey maps, template + composition design, service contract, gate definitions, KPI plan with phase segmentation, lifecycle review cadence, and the expansion sequence.

## Guardrails
- One TVP path validated before any catalog is designed; a platform announced as a catalog of unbuilt paths is the portal trap's cousin.
- Never ship a path without an upgrade channel — that's manufacturing clone-and-forget at scale.
- Every abstraction decision passes the illusion test: does it hide detail that still matters to the researcher (GPU class, cost)? Surface cost to the requester even when defaults are chosen.
- No hidden manual steps: if the agent variant of the path can't run, the human variant has friction you haven't measured.
- Gates start as warnings with a published promotion date; springing blocking gates on existing teams burns the adoption the path exists to earn.
- Declare the lifecycle phase before reporting KPIs; numbers without phase context mislead in both directions.
- Break-out routes stay open and observable — a golden path is the easiest way, never the only way.
- A template without an owner, service objective, compatibility policy, support route, and deprecation plan is not a productized golden path.

## Suggested effort
High — a full path product spec spans discovery, design, gating, and measurement; the TVP slice alone is a focused multi-session effort.
