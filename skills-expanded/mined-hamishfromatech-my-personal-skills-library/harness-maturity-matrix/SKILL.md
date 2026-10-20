---
name: harness-maturity-matrix
description: Assess and advance an engineering team's AI harness maturity across ten dimensions and five stages — from "No AI Process" through "Chatbot-Assisted" and "Human-in-the-Loop" to "Systematic Harness" and "Agentic Flywheel." Use when diagnosing why agent-assisted work stalls, planning a team's harness investment, auditing brownfield readiness, or deciding what to build next to make delegation safe. NOT for one-off prompt engineering or single-agent debugging.
---

# The Harness Maturity Matrix — AI Engineering Maturity Model

## The Harness Thesis

A convergence is happening across the AI engineering community: **when AI writes the code, the craft shifts to designing the system that controls AI.** The difference between a demo and a production-grade agent is almost entirely the harness — the system of context, constraints, and verification that wraps an agent and turns raw model output into something you can trust.

Multiple practitioners arrived at this insight from different angles:
- **Mitchell Hashimoto** — harness engineering: "anytime an agent makes a mistake, you engineer a solution so it never makes that mistake again."
- **OpenAI** — three engineers used Codex to build a million-line codebase with zero manually written code over five months, via a three-layer harness (context engineering, architectural enforcement via custom linters, garbage-collection agents).
- **Birgitta Boeckeler** — harnesses may become the new service templates (standardized starting points for common topologies); raised the critical brownfield question.
- **Chad Fowler** — when XP replaced phase-gate development, rigor relocated from documents to tests. The new formula: **probabilistic inside, deterministic at the edges.**
- **Kief Morris** — loop progression: outside the loop (vibe coding) → in the loop (review every line) → on the loop (build the harness) → agentic flywheel (direct agents to improve the harness).

The METR 2025 RCT (experienced developers 19% slower with AI while believing they were faster) is exactly what the harness thesis explains: **without the system around the agent, the review-fix-reprompt tax dominates.**

Two principles run through every stage:
1. **Accountability stays with the human.** Maturity is not transferring responsibility to agents; it is humans earning the right to delegate more execution because the system catches what agents get wrong.
2. **Agents are first-class team members.** If information (a backlog item, an architectural decision, a runbook, a metric) is available to humans but not agents, the harness has a hole. "It sits in my slide deck" is the anti-pattern.

## The Five Stages (Dominant Interaction Paradigm)

| Stage | Name | Dominant Pattern |
|---|---|---|
| 1 | No AI Process | Humans execute; standard tools |
| 2 | Chatbot-Assisted | Humans execute with AI suggestions |
| 3 | Human-in-the-Loop | Agents use file/terminal; human reviews every output |
| 4 | Systematic Harness | Repository as system of record; human on the loop |
| 5 | Agentic Flywheel | Agents propose harness improvements; human directs evolution |

Most organizations are at Stage 1 or 2. Stage 4 is aspirational; Stage 5 is informed speculation with no validated production examples yet (Q1 2026).

## The Ten Dimensions (Organized into Four Clusters)

The dimensions form a causal story: **Foundation** (inputs — what agents work with) feeds **Governance** (constraints — what keeps agents safe), which shapes **Delivery** (execution — how work gets done), which produces **Outcomes & Learning** (measurement and evolution).

### Foundation Cluster

**Context Engineering** — How effectively agents receive the right information at inference time. Copy-paste snippets → human-maintained AGENTS.md with manual loading → repository as system of record with progressive disclosure → human designs context structure, agents maintain and evolve it. Key transition: Stage 3 (human curates) → Stage 4 (repo structure IS the context; documentation linters enforce currency). Progressive disclosure: agents start with a repo map and pull detailed documents only when a task needs them, rather than loading an encyclopedia up front.

**Team (Humans + Agents)** — The team as a single composition. Two axes progress together: team shape (large specialist → business-oriented delivery → small generalist per initiative → generalist across multiple initiatives) and agent capability tier (none → suggestion-only → file/terminal → ephemeral full-stack environments with browser automation → agents self-provisioning). The human role evolves: execution → delivery leadership → multi-initiative oversight. Critical nuance: agents provide technical depth on demand but do NOT replace domain depth (unique business rules, customer workflows, market dynamics). In complex-domain businesses, architects must move closer to customers as agents absorb execution, not away.

### Governance Cluster

**Security & Trust** — Zero Trust progression. No AI-specific concerns → human reviews for obvious issues → AI output through existing SAST/DAST → scoped, auditable agent access with AI-specific threat modeling → agents enforce and evolve policies; human governs trust boundaries. Supply chain verification for agent tools becomes critical — treat tool descriptions and AI skills as potential attack vectors.

**Architectural Governance** — How constraints and design taste are enforced. Basic prompt rules → human-enforced boundaries → custom linters with remediation instructions injected into agent context → harnesses as org-wide templates. **Taste invariants as code** — encoding refined judgment about which abstractions age well, which coupling is acceptable, which patterns reduce long-term risk — into linters and structural tests so agents cannot unknowingly violate it. In an AI era where generation is cheap, **taste is the new moat** — an intangible, durable advantage that survives when everyone has the same models. The Stage 3→4 cost: senior engineers must name and codify judgment they have always held implicitly. Teams that skip this stay at Stage 3 forever — agents inside boundaries the humans cannot articulate.

### Delivery Cluster

**Human-Agent Interaction** — Maps to Morris's loop progression (outside → in → on → flywheel). Common Stage 3 failure: teams that review every line become a bottleneck and conclude AI "doesn't save time."

**Workflow & Process** — Occasional AI for specific tasks → daily agent use with parallel work delegation → always-running agents, agent-first delivery, human sets priorities → agents handle full delivery cycle, human steers outcomes. At Stage 4 the question shifts from "should we use AI for this?" to "why would a human do this instead of an agent?"

**Reliability & Operations** — What happens after deployment. Two axes: runbook axis (tribal knowledge → markdown-in-Git → LLM-ready structured runbooks → agent-executable playbooks) and alert-handling axis (manual → AI-drafted queries → auto-analysis on alert → severity-based auto-triage → proactive anomaly detection). The human role shifts from executing incidents to owning only novel failure modes. The Stage 3→4 jump: agents get trusted with low-severity triage end-to-end — a governance decision backed by better runbooks, not blind delegation.

### Outcomes & Learning Cluster

**Verification & Quality** — Human eyes → agent runs tests, human checks → custom linters and structural tests with human review → agent-to-agent review with quality scoring → agents detect and fix regressions. Fowler's principle: **if generation gets easier, judgment must get stricter.** A Stage 4 team has encoded "what good looks like" into tooling, not tribal knowledge.

**Knowledge & Feedback Loops** — Tribal knowledge in wikis → README-level docs → human-structured docs in repo → versioned plans and quality grades in repo; agent failures feed the harness → agents maintain docs and capture learnings. Critical shift: from docs in wikis to versioned artifacts in the repository. Knowledge that lives only in Slack threads or people's heads effectively does not exist for agents.

**Planning & Decision-Making** — Manual boards and experience-driven decisions → AI helps write tickets and research → agent triages issues, human prioritizes, decisions validated via PoCs → decision signals equally reachable by humans and agents, humans validate with cheap prototypes → agents propose initiatives, humans set direction from measured results. The equal-access principle: every signal a human uses to decide what to build next must be equally reachable by agents.

## The Brownfield Reality Check

All source articles lean greenfield. Stages 1–3 apply equally to brownfield and greenfield. Divergence starts at Stage 4.

**Brownfield** here means the common case: a legacy codebase carrying real tech debt, with patchy documentation, weak automation, and processes shaped more by history than design. A well-maintained long-lived codebase is a different beast — its established templates give agents more to imitate. The blocker is not age, but lack of a mature codebase (debt + disorder).

Systematic harness engineering assumes architectural cleanliness that debt-laden legacy rarely has: clear module boundaries, enforceable dependency directions, sufficient test coverage for agents to verify their own work.

### Harness-Readiness Checklist for Brownfield Systems

Before building a harness on legacy code, work through:
1. **Modularization** — Can you name, in a sentence, what each module owns? If ownership is ambiguous, agents will generate code that belongs nowhere and everywhere.
2. **Boundary enforcement** — Are module dependencies explicit and directional? If not, agents will create new coupling faster than humans can untangle it.
3. **Test coverage** — Can agents verify their own changes without human intervention? Gaps in coverage become gaps in agent autonomy.

Teams that skip harness-readiness and jump to agentic workflows typically regress within weeks — agent-generated entropy compounds faster than manual cleanup can address it. As of Q1 2026, Stage 4 remains largely unvalidated for brownfield. AI can accelerate the harness-readiness work itself — like running static analysis on a codebase that has never had one (you will drown in alerts unless you tame the foundation first).

## Mixed Maturity and Regression

**Mixed maturity across dimensions is the norm, not a failure.** One team scored Stage 4 on Context Engineering (structured AGENTS.md, repo-level documentation wired into every prompt) yet sat at Stage 2 on Verification (entirely manual code review). In practice: agents produced architecturally sound code that broke integration tests nobody ran automatically. Once the team prioritized automated verification — wiring CI checks into the agent feedback loop — their context investment finally compounded. **The weaker dimension was the bottleneck, not the stronger one.**

When prioritizing, start with the dimension that creates the most pain or blocks progress in others.

**Regression is real.** Many teams stuck at Stage 2 abandoned AI entirely and regressed to Stage 1. The most common 2026 struggle is overcoming Stage 3 — justified fear of giving control without sufficient verification and governance. The harness is exactly what addresses that fear: you do not hand over control, you build the system that makes delegation safe.

## How to Use the Matrix

The model is a **diagnostic tool, not a certification.** Best used as a team conversation starter, not a solo assessment. Grab a whiteboard, walk through the dimensions, and see where disagreements surface — those disagreements are the signal.

**Practical starting protocol:**
1. Circulate the matrix to senior engineers before the next staff meeting.
2. Ask each person to score one or two dimensions independently.
3. Bring the disagreements to the meeting — you do not need consensus, you need the conversation.
4. Pick one dimension where you feel the most pain. Identify your stage and what the next stage looks like. Build one thing that moves you forward.

**Stage starting points:**
- Greenfield teams: typically start at Stage 3; some Stage 4 characteristics achievable in select dimensions.
- Brownfield teams: getting to Stage 2 is usually straightforward; moving to Stage 3 takes hard work from the whole team; Stage 4 remains aspirational for debt-laden systems.

## A-Tech Applications

### A-Coder
- **Context Engineering:** Repository-as-system-of-record architecture (AGENTS.md auto-generated from repo structure; progressive disclosure via symbol index); documentation linters as a built-in feature.
- **Architectural Governance:** Custom linter framework enabling taste-invariants-as-code (teams encode design judgment into enforceable rules); this is the A-Coder moat — the tool that makes Stage 4 achievable.
- **Verification & Quality:** Agent-to-agent review with quality scoring built into the merge flow; CI checks wired into agent feedback loop so agents self-correct.
- **Team:** Expertise-adaptive autonomy (from `agentic-coding-returns-to-expertise`) maps to the capability-tier progression; A-Coder enables the full-stack ephemeral environment.
- **Brownfield:** Harness-readiness checklist as a built-in diagnostic (modularization audit, boundary enforcement check, coverage gap map); AI-accelerated harness-readiness remediation as a feature.

### Be Practical
- **Curriculum module:** "The Harness Maturity Matrix" — teaches teams to self-assess and plan investment.
- **The loop progression** (outside → in → on → flywheel) as the mental model for adopting AI-assisted development.
- **The brownfield reality check** chapter — why greenfield demos don't transfer and what to do about it.
- **Taste invariants as code** as an advanced module for senior engineers.

### Builder's Club
- **Shared assessment workshop:** teams bring their matrix scores and compare; the disagreements are the learning.
- **Open-source harness templates** (Boeckeler's "harnesses as the new service templates" — community-contributed starting points for common topologies).
- **Brownfield harness-readiness toolkit** as an open-source community project (modularization analyzer, dependency-direction enforcer, coverage-gap mapper).

## Measurement Framework

| Dimension | Stage-4 Indicator | How to Measure |
|---|---|---|
| Context Engineering | Repo IS the context; docs linters enforce currency | % of agent tasks that never need manual context loading |
| Team | Small generalist team per initiative; agents full-stack | Team size vs. delivery throughput; specialist-to-generalist ratio |
| Security & Trust | Scoped, auditable agent access; AI threat modeling | % of agent actions with scoped tokens; threat-model coverage |
| Architectural Governance | Custom linters with remediation; taste as code | % of design rules enforced mechanically vs. tribally |
| Human-Agent Interaction | Human on the loop, not in the loop | % of agent outputs reviewed line-by-line vs. outcome-validated |
| Workflow & Process | Agent-first; human sets priorities | % of work initiated by agents vs. humans |
| Reliability & Ops | Agent auto-triage of low-severity; human owns novel | % of alerts auto-triaged; mean-time-to-context on P1 |
| Verification & Quality | Agent-to-agent review with quality scoring | Verification coverage; false-negative rate; human override rate |
| Knowledge & Feedback | Versioned plans/grades in repo; failures feed harness | % of knowledge in repo vs. Slack/wiki; harness-improvement velocity |
| Planning & Decisions | Signals equally reachable by humans and agents | % of decision signals agent-accessible; prototype-validation rate |

## Anti-Patterns

1. **Stage-skip disease** — jumping to agentic workflows without harness readiness; entropy compounds faster than cleanup.
2. **Strong-dimension illusion** — investing in one dimension (e.g., context) while a weaker one (e.g., verification) is the actual bottleneck.
3. **Taste-atrophy** — relying on senior engineers' implicit judgment instead of codifying it; when they leave, the harness breaks.
4. **Slide-deck knowledge** — information available to humans but not agents; the harness has a hole.
5. **Accountability transfer** — treating maturity as handing responsibility to agents rather than earning the right to delegate.
6. **Domain-depth neglect** — moving architects away from customers as agents absorb execution; agents provide technical depth, not domain depth.
7. **Brownfield-as-greenfield** — applying Stage 4 harness techniques to debt-laden legacy without the readiness checklist.
8. **Greenfield-by-neglect** — letting a greenfield project become brownfield through poor documentation and weak automation.

## Cross-References

- `harness-engineering-ai-agents-2026` (ai-agents-and-workflows) — the five technical layers (model, orchestration, context, verification, telemetry); this skill is the organizational/maturity complement.
- `outer-loop-harness-framework` (ai-agents-and-workflows) — the RPI/BMAD/SPARC outer-loop methodologies that operationalize Stage 3→4 progression.
- `agentic-coding-returns-to-expertise` (developer-experience-and-flow) — the expertise leverage curve that informs the Team dimension.
- `devex-verification-bottleneck-framework` (developer-experience-and-flow) — the verification dimension's measurement stack.
- `coding-agent-decision-fatigue-mitigation` (developer-experience-and-flow) — the human-agent interaction dimension's cognitive-load complement.
- `context-engineering-production-practice` (cognitive-science-and-ux) — the context engineering dimension's technical patterns.
- `agentic-development-security-ads` (ai-agents-and-workflows) — the security & trust dimension's security framework.
- `spec-driven-cognitive-partnership` (cognitive-science-and-ux) — the verification dimension's comprehension safeguards.

## Sources

- HandsOnArchitects (Maciej Laskowski & Tomasz Michalak) — "The Harness Model — AI Engineering Maturity Matrix, Q1 2026" (April 16, 2026). 10-dimension × 5-stage maturity matrix synthesizing the harness engineering community convergence.
- Mitchell Hashimoto — harness engineering practice ("anytime an agent makes a mistake, engineer a solution so it never makes that mistake again").
- OpenAI team — three-engineer, million-line codebase, zero manually written code, three-layer harness (context engineering, architectural enforcement, garbage-collection agents).
- Birgitta Boeckeler — harnesses as the new service templates; brownfield question.
- Chad Fowler — XP→AI rigor relocation; "probabilistic inside, deterministic at the edges."
- Kief Morris — loop progression (outside → in → on → flywheel).
- METR (2025) — RCT: experienced developers 19% slower with AI while believing faster; the harness thesis explains the gap.
- Container Solutions — Cloud Native Maturity Matrix (visual format inspiration).