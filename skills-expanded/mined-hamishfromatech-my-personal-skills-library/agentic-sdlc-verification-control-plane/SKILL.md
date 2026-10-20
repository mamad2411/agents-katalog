---
name: agentic-sdlc-verification-control-plane
description: Applies Bhati's synthesis of the agentic software-development lifecycle (arXiv:2609.04681, Sept 4 2026) — the Agentic SDLC Throughput Paradox, Production-Qualified Change (PQC), the Verification Tax, and the Agentic SDLC Control Plane — as the conceptual map for shifting the engineering question from "how much code can an agent generate" to "how much production-qualified value per dollar, per reviewer-hour, per unit of risk." Use when designing AI agent autonomy policy, budgeting verification/review capacity, planning the transition from per-seat to agentic cost models, or teaching AI-era software-engineering economics. NOT for DevEx measurement surveys (use devex-verification-bottleneck-framework) or for specific sandboxing designs (use ai-coding-agents-sandbox-first).
---

# The Agentic SDLC: Verification Tax and the Control Plane

## Overview
AI coding systems have moved from autocomplete to agents that inspect repositories, edit files, run tools, and open PRs with limited supervision. The consequence is a **structural shift in the bottleneck**: implementation acceleration has pushed the constraint downstream into review, integration, testing, security, deployment, and production operations — while the economics shift from predictable per-seat licensing to variable token/tool/sandbox/CI/rework costs. Bhati's synthesis (drawing on 2024–2026 peer-reviewed SE research, university studies, benchmark audits, production reports, and developer telemetry) proposes four engineering concepts that operationalize this: the **Agentic SDLC Throughput Paradox** (meaningful gains in coding activity that attenuate sharply between writing and shipping), **Production-Qualified Change (PQC)**, the **Verification Tax**, and an **Agentic SDLC Control Plane** that allocates autonomy subject to cost, reliability, and human-attention budgets.

## When to Use
- Designing an autonomy policy for AI coding agents (when to grant, when to gate)
- Planning the transition from per-seat to agentic cost models (token, tool, sandbox, CI, rework)
- Building a measurement system that captures production-qualified value, not code volume
- Briefing leadership on why AI productivity gains shrink between writing and shipping
- NOT for per-developer DevEx surveys (see devex-verification-bottleneck-framework)
- NOT for sandbox/security containment mechanics (see ai-coding-agents-sandbox-first)

## Core Process / Workflow
1. **Adopt PQC as the unit of delivery**: replace "lines of code" and "PRs merged" with Production-Qualified Change — a change that survives integration, testing, security review, deployment, and production operation. The engineering question becomes: *how much PQC per dollar, per reviewer-hour, per unit of operational risk?*
2. **Budget the Verification Tax explicitly**: synthesis evidence shows gains attenuate sharply between writing and shipping — review, integration, testing, security, deployment, and production operations remain constraining stages. Treat verification as a first-class capacity line in the same plan as velocity.
3. **Design the Control Plane**: allocate agent autonomy along three budget axes — (a) cost (token/spend caps per task, per day, per agent), (b) reliability (deterministic gates before human review: static analysis, tests, sandbox), (c) human-attention (reviewer capacity as the scarce resource; deterministic pre-gates protect it). The Control Plane is the operating layer: approved models/data/resources, per-run logs including what was BLOCKED, spend capped at the boundary.
4. **Map the evidence-based horizon**: today's supervised agents → policy-bounded software factories. The synthesis maps the maturity path — autonomy grows only as the gates it passes grow. Use the RAMP maturity matrix (L1–L4) as the staged-ladder companion.
5. **Reprice the cost model**: per-seat licensing assumes stable human headcount; agentic economics are variable (token, tool, sandbox, CI, rework). Cost models built on per-seat assumptions will systematically underestimate agentic spend — use the variable-cost taxonomy from the synthesis.

## Key Evidence
- Recent field studies show meaningful gains in coding activity, but newer evidence shows those gains attenuate sharply between writing code and shipping reliable software
- Review, integration, testing, security, deployment, and production operations remain constraining stages
- Economics shifting from predictable per-seat licensing toward variable token/tool/sandbox/CI/rework costs
- The central research question shifts: how much production-qualified value per dollar, per reviewer-hour, per unit of operational risk
- Four named concepts: Throughput Paradox, PQC, Verification Tax, Control Plane

## Pairs with
`devex-verification-bottleneck-framework` (the developer-side bottleneck this synthesizes), `sonar-state-of-code-2026` and `review-production-gap-observability-2026` (the empirical verification-gap evidence), `spec-quality-bottleneck-agentic-delivery` (the spec-side complement — implementation accelerates, specification is the rate-limiting factor), `ai-coding-agents-sandbox-first` (the containment tier beneath the Control Plane), `coder-agent-relay-regulated-deployment` (the enterprise isolation pattern), `harness-premium-pricing-model` (the harness-vs-model margin layer this cost shift lands on), `ai-dev-cost-measurement-pitfalls` (the measurement pitfalls this concept set complements), `context-engineering-skills-map-2026` (the skill map for the Control Plane operator).

## A-Tech Alignment
- **Open source**: the Control Plane is implementable with open tooling (policy-as-code, OpenTelemetry, static analysis, CI gates) — no proprietary platform required.
- **Privacy**: the Control Plane's least-privilege allocation is the privacy surface — approved data, per-run logs, spend capped at the boundary.
- **Financial freedom**: the variable-cost taxonomy protects solo builders from per-seat pricing assumptions and enables honest agentic ROI accounting.
- **Practical**: PQC + the three-axis budget (cost/reliability/attention) is a directly usable autonomy-policy template.

*Source: Bhati, H., "Beyond Code Generation: Reliability, Verification, and Cost Economics in the Agentic Software Development Lifecycle," arXiv:2609.04681, Sept 4 2026 (cs.SE/cs.AI); 18 pages, 6 figures, 3 tables; synthesis of 2024–2026 SE research and production reports.*