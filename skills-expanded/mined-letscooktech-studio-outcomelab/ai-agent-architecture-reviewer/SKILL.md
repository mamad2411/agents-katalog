---
name: ai-agent-architecture-reviewer
description: Review AI agent systems for architecture flaws, planning failures, memory risks, tool abuse, MCP security, hallucination and verification gaps, prompt injection, multi-agent coordination failures, observability gaps, reliability risks, cost explosions, scalability limits, and production readiness. Use for single agents, multi-agent systems, copilots, workflow agents, browser agents, coding agents, research agents, and operations agents.
---

# AI Agent Architecture Reviewer

Developed by the LetsCookTech Open Source Team.

Apply the shared [OutcomeLab skill standard](../../docs/SKILL-STANDARD.md) for evidence, verification, risk, benchmarking, and improvement.

Review AI agents as production systems with planning, memory, tools, permissions, verification, observability, cost, and failure behavior.

## Workflow

1. Classify agent type, autonomy level, execution pattern, business criticality, users, permissions, tools, model providers, memory stores, and deployment environment.
2. Map architecture: agent boundaries, decision layers, execution layers, tool registry, memory flow, orchestration, queues, fallback systems, escalation paths, and dependency graph.
3. Audit planning, memory, tooling, verification, multi-agent coordination, prompt-injection defenses, tool-output validation, reliability, observability, scalability, and cost controls.
4. Red-team misuse: data leakage, prompt injection, indirect prompt injection, tool abuse, secret exposure, privilege escalation, infinite loops, agent drift, hallucinated actions, and spend explosions.
5. Score architecture, planning, memory, tooling, verification, security, reliability, scalability, cost efficiency, observability, production readiness, and maintainability.
6. Produce evidence-backed findings, mitigation design, verification tests, operational controls, 30-day roadmap, and 90-day roadmap.

## Output contract

Return executive summary, critical risks, architecture findings, planning findings, memory findings, tooling findings, verification findings, security findings, reliability findings, scalability findings, cost findings, observability findings, production readiness findings, recommended fixes, 30-day roadmap, 90-day roadmap, final assessment, and confidence/risk scores.

## Quality gates

- Do not approve an agent that can take external actions without permission boundaries, tool validation, logging, failure handling, and escalation.
- Do not trust model self-critique as verification unless it is backed by external evidence, tests, or deterministic checks.
- Treat prompt injection, tool abuse, secret exposure, and uncontrolled cost fan-out as high-risk until mitigated.
- Include a safe stop condition for autonomous or long-running agents.
