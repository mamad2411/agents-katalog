---
name: enterprise-vibe-coding
description: "Knowledge base from \"Enterprise Vibe Coding for Agentic Engineering\" by Valentina Alto (Packt, 2026). Use when applying the author's Hypervelocity Engineering (HVE) frameworks for steered agentic development, the six primitives (instructions, prompts, agents, skills, hooks, MCP), the RPI (Research-Plan-Implement) cadence and Agentic DevOps, governance from stochastic to deterministic (decision boundaries, hooks, policy-as-code, audit trail), multi-agent use cases, loop engineering and Agent Experience (AX) — studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Enterprise Vibe Coding for Agentic Engineering
**Author**: Valentina Alto | **Publisher**: Packt (2026) | **Pages**: ~192 | **Chapters**: 8 | **Generated**: 2026-10-13

## How to Use This Skill

- **Without arguments**: load the core frameworks below
- **With a topic**: ask about `RPI`, `hooks`, `decision boundaries`, `handoff`, `delivery loop`, `AX`; I find and read the relevant chapter
- **With chapter**: ask for `ch05` to load that chapter file
- **Browse**: ask "what chapters do you have?" for the full index
- **Decide fast**: [cheatsheet.md](cheatsheet.md) holds the author's decision rules and thresholds

When you ask about a topic not covered in Core Frameworks below, I read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### 1. Generation is cheap, judgment is not: steer, don't vibe
- Vibe coding (Karpathy, 2025: "forget that the code even exists") is fine for prototypes. It fails once software must be **integrated, audited, secured, or maintained by others**. Four failure modes: **Ownership, Drift, Security, Invisible assumptions**.
- **Vibe-coding flywheel**: velocity spike → consistency erosion → review fatigue → incident acceleration → velocity collapse. The work moves downstream: Faros measured +98% PRs merged but **+91% review time**.
- **Steered agentic development** = humans steer (boundaries, decisions, accountability), agents execute and produce evidence. **Three Shifts**: *Delegation* (bounded task: inputs, tools, allowed actions, definition of done), *Accountability* (a named human approves), *Evidence* (spec, tests, scans, rationale in the PR).
- **Field test before every merge**: *Who decided? What were the constraints? What evidence proves it works?* If any answer is missing, you're still vibe coding, however sophisticated the tooling.

### 2. HVE (Hypervelocity Engineering): capacity scales with the agentic system, not headcount
- Three foundations: **small multidisciplinary teams (4–5)**, **solution accelerators** (start from reference architectures, not a blank repo), **AI across the whole lifecycle**.
- **Maturity spectrum**: 1 Traditional → 2 AI-assisted → 3 Vibe coding (the most dangerous plateau: velocity hides debt) → 4 Structured agentic (agents research and plan before coding) → 5 HVE. Assess it on **seven dimensions** (tool adoption, primitive stack, methodology, governance, business-value measurement, capacity model, human-in-the-loop design). The lowest dimension is the bottleneck.
- **Top 3 risks to triage in 90 days**: review-capacity collapse, security/data drift, invisible architectural drift.

### 3. Agents and the autonomy gradient
- Agent = LLM + **perception, reasoning/planning, tool use, memory**, running in a loop. If one is missing, it's a model call.
- **Autonomy is a gradient, not a switch**: low (a human accepts each step), **bounded** (approval at thresholds like money, prod deploy, customer-facing comms; where mature capability sits today), standing authority (audited, not supervised).
- **Three collaboration phases**: human-first (efficiency play) → agent-led with supervision (unit-economics play) → autonomous with human governance (operating-model play). Don't expect Phase-3 economics from a Phase-1 design.
- **Human-agent working contract**: manager-and-team. The human briefs, scopes, agrees the DoD, reviews, and says "not yet". Connect tools via **MCP**, agents via **A2A**.

### 4. The six primitives: engineer behavior into versioned files
- **Instructions** (always-on rules), **prompts** (*what*: fixed-outline templates), **agents** (*who*: named, least-privilege, explicit escalation), **skills** (*how*: procedures plus failure modes), **hooks** (*enforce*: deterministic, lightweight), **MCP** (*connect*: read-only first, pinned, logged).
- The concept is surface-agnostic, the files are surface-specific: `.github/copilot-instructions.md` ↔ `CLAUDE.md`; `.github/prompts/*.prompt.md` ↔ `.claude/commands/`; `.github/agents/` ↔ `.claude/agents/`; skills in `.github|.claude/skills/<name>/SKILL.md`; hooks in `.github/hooks/` ↔ `.claude/settings.json`.
- Rules: keep the global file short; prefer scoped globs over conditionals; review monthly; no secrets; link, don't paste; name prompts by intent; agent brief ≤ 1 page; start with **3–5 agents, 3–5 skills**; slow checks go to CI, not hooks. Treat every MCP server as a production dependency.
- The runtime is the **macro orchestrator**: one sentence ("implement secure auth") gets six layers of governance composed around it.

### 5. RPI cadence + Agentic DevOps
- **Research** (assumptions note from spec/ADR/code) → **Plan** (diff scope, tests, rollback) → **human approves** → **Implement** (small PRs with test/lint/scan evidence). Enforce it with hooks and policy-as-code.
- **Approval ≠ correctness**: layer independent tests, scans, staged rollout, monitoring and rollback, plus a second reviewer for high-risk changes.
- The SDLC phases stay. Agents automate the *reasoning between* phases, and governed artifacts in the repo replace restated context.
- **Release pipeline as an active safety system**: build → tests + eval harness → staging → smoke agent → **named human approval** → canary → SLO watch → promote/rollback. Agents never decide to release. Test plan per story: **happy + 3 edge + 2 failure + 1 security**.

### 6. Governance: push consequences toward determinism
- **Five bands**: stochastic → stochastic under context constraint → stochastic with deterministic validation → *deterministic procedure invoked by a stochastic decision* → fully deterministic. **The higher the blast radius, the more deterministic the control.** Let creativity stay stochastic and pin down the consequences.
- **Five layers**: (1) instruction hierarchy, *short, imperative, scoped* (Tier-2 `applyTo`/nested `CLAUDE.md` is "the most underused lever"); (2) **hooks**, the only mechanism between decision and action ("anything an instruction recommends, a hook can require"); (3) **policy-as-code** (OPA/Rego, Cedar): deny-by-default, declarative, testable, auditable, versioned, outside the agent; (4) **parallelism only on disjoint scopes**, idempotent shared writes, coordination via files not models; (5) **audit trail**: unbroken causal chain, per-agent identity on behalf of a user, tamper-evident storage.
- **Decision boundaries**: L0 forbidden / L1 human approval / L2 logged and reviewable / L3 autonomous. Every action maps to exactly one level.

### 7. Building products: governance *is* the architecture
- Choose the **MAF orchestration pattern** from the problem's shape: Sequential (real dependencies), Concurrent (fan-out), Group chat (rounds), Magentic (open-ended), **Handoff** (one voice, shifting expertise).
- **Advice / Action / Transaction**: recommend freely; take reversible, in-scope actions validated against the system of record; keep checkout and payment outside the agents. Customer consent does not remove business accountability.
- Ground every fact in a live tool call. Design the **failure path** (idempotency, bounded retries, compensation, escalation with the trace). Layer content gates: deterministic → AI reviewer → human.

### 8. Loop Engineering: design the loop, not the prompt
- Prompt → Context → Harness → **Loop** engineering: each optimizes a different layer, and loops make work *progress*.
- **Five stages, two gates**: Discover (issue → executable contract) → Plan (**Gate 1**; silence ≠ consent) → Execute (small slices) → Verify and Recover (failure becomes the next input) → Complete (**Gate 2**, human merge). A done-condition job fails while any `- [ ]` is unchecked.
- State lives in the issue/PR thread; each tick rebuilds it and advances **one capability**. Bounds: continuation caps, `MAX_STARTS`, idempotent "loop-started" marking, conflict detection, least-privilege MCP, hard gates in sensitive areas. Recovery: **3 attempts** per criterion; in auth/payments/PII/prod, stop on the first failure.

### 9. Agent Experience (AX)
- When agents run for hours, design shifts from interface to **relationship**. Work must stay *understandable, steerable, auditable, accountable*.
- **Five return questions**: goal? what changed? why? what evidence? what decision is needed from me now? Start with one workflow's resumable view. HVE already produces the artifacts.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-vibe-to-steered.md) | The Impact of AI: From Vibe Coding to "Steered" Agentic Development | Three Shifts, field test, vibe-coding flywheel, HVE foundations, maturity spectrum, 7 dimensions, top 3 risks |
| [ch02](chapters/ch02-agentic-ai-new-way-of-work.md) | Agentic AI and the New Way We Work | Four capabilities, 7 building blocks, autonomy gradient, three collaboration phases, MCP/A2A, working contract |
| [ch03](chapters/ch03-primitives.md) | Primitives: The Building Blocks of Agentic Development | Six primitives, anatomy, visibility layers, macro orchestrator, Copilot ↔ Claude Code mapping |
| [ch04](chapters/ch04-sdlc-rpi-cadence.md) | Reshaping the SDLC: Agentic DevOps and the RPI Cadence in Practice | RPI per phase, Agentic DevOps 5 patterns, release safety system, agent scoping, FlowDesk |
| [ch05](chapters/ch05-governance.md) | Governance: From Stochastic to Deterministic Agentic Development | Five bands, five layers, instruction tiers, policy properties, decision boundaries, parallelism rules, audit trail, NIST/ISO/EU AI Act |
| [ch06](chapters/ch06-use-cases.md) | Use Cases: Building Agentic Solutions with the HVE Primitives | MAF patterns, advice/action/transaction, failure path, layered gate, 6-step method, SkyBridge/Luxe/SkillForge |
| [ch07](chapters/ch07-loop-engineering.md) | Loop Engineering | Four disciplines, Osmani's anatomy, five stages + two gates, autonomy modes, recovery boundaries, bounding controls |
| [ch08](chapters/ch08-agent-experience.md) | From Steered Delivery to Agent Experience | HVE journey, converging principles, AX (two senses), five return questions |

## Topic Index

- **A2A protocol** → ch02
- **Accountability / named approver** → ch01, ch04, ch05
- **Advice / action / transaction boundary** → ch06
- **Agent (primitive), least privilege, escalation** → ch03, ch04
- **Agent identity** → ch05
- **Agentic DevOps** → ch04
- **Agentic workflows (gh-aw, claude-code-action)** → ch04, ch05
- **Anti-patterns of loops** → ch07
- **Audit trail** → ch05, ch06
- **Autonomy gradient / Autopilot vs permissions** → ch02, ch07
- **AX (Agent Experience)** → ch08
- **Blast radius / stochastic-to-deterministic spectrum** → ch05
- **Claude Code vs Copilot file locations** → ch03, ch05
- **Collaboration phases (human-first → autonomous)** → ch02
- **Decision boundaries (L0–L3)** → ch05
- **Done-condition / executable contract** → ch07
- **Failure path / idempotency** → ch05, ch06, ch07
- **Field test (who decided / constraints / evidence)** → ch01
- **Handoff and MAF orchestration patterns** → ch06
- **Hooks** → ch03, ch05, ch07
- **HVE foundations / maturity spectrum** → ch01, ch08
- **Instruction hierarchy (global / scoped / memory)** → ch03, ch05
- **Loop engineering / delivery loop / tick** → ch07
- **MCP** → ch02, ch03, ch07
- **NIST AI RMF, ISO/IEC 42001, EU AI Act** → ch05
- **Parallel agents / disjoint scopes** → ch05, ch07
- **Policy-as-code (OPA/Rego, Cedar)** → ch05
- **Primitives (six)** → ch03
- **Release pipeline / canary / human gate** → ch04
- **Review-capacity collapse** → ch01
- **RPI cadence** → ch04, ch06, ch07
- **Skills** → ch03
- **Test strategy (spec-to-test-plan, scenario tests)** → ch04, ch06
- **Vibe coding / vibe-coding flywheel** → ch01, ch08
- **Vibe working** → ch02

## Supporting Files

- [glossary.md](glossary.md): all key terms with definitions
- [patterns.md](patterns.md): techniques and patterns with when/how/trade-offs
- [cheatsheet.md](cheatsheet.md): decision rules, band × decision-level table, pattern picker, thresholds

---

## Scope & Limits

This skill covers the book's content only. Tooling details (Copilot CLI `/loop`, GitHub Agentic Workflows, Microsoft Agent Framework) reflect the book as of 2026 and move fast, so verify them against current docs before relying on exact syntax. For hands-on implementation, combine with project-specific tools. Related skills here: `ai-agents-and-applications`, `huyen-ai-engineering`, `prompt-engineering-generative-ai`.
