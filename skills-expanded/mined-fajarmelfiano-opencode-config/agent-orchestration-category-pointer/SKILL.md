---
name: agent-orchestration-category-pointer
description: "Pointer to a library of 36 specialized Agent Orchestration skills. Use when working on agent-orchestration-related tasks."
risk: none
---

# Agent Orchestration Capability Library 🎯

This is a **pointer skill**. The 36 specialized Agent Orchestration skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **agent-self-scheduling** — Schedule AI agent runs with cron, loops, or external clocks while avoiding unsafe tight autonomous timers.
- **agentflow** — Orchestrate autonomous AI development pipelines through your Kanban board (Asana, GitHub Projects, Linear). Manages multi-worker Claude Code dispatch, deterministic quality gates, adversarial review, per-task cost tracking, and crash-proof pipeline execution.
- **agy-delegate** — Delegate coding tasks to the Google Antigravity CLI (`agy`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **aider-delegate** — Delegate coding tasks to Aider (`aider`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **claude-delegate** — Delegate coding tasks to a separate Claude Code CLI process or Claude session only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **cline-delegate** — Delegate coding tasks to the Cline CLI (`cline`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **cline-pilot** — Proxy Cline CLI coding tasks: dispatch, monitor background runs via hard evidence, relay decision points in a fixed format, verify against a checklist, and learn per-tag preferences over time.
- **codex-delegate** — Delegate coding tasks to the OpenAI Codex CLI only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **codex-subagent** — Launch Codex CLI as an isolated subagent for bounded coding, review, or verification tasks.
- **commandcode-delegate** — Delegate coding tasks to the Command Code CLI (`cmd`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **copilot-delegate** — Delegate coding tasks to the GitHub Copilot CLI (`copilot`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **crewai** — Expert in CrewAI - the leading role-based multi-agent framework used by 60% of Fortune 500 companies.
- **cursor-delegate** — Delegate coding tasks to the Cursor Agent CLI (`cursor-agent`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **delegate-setup** — Configure approved delegation lanes across installed implementer CLIs, including optional model and effort choices, then write global or project config only after explicit user approval.
- **delegating-to-agents** — Delegate bounded work to other AI agents while preserving context, ownership, and progress checks.
- **fact-check-x-unified** — Fact-Check-X 流程编排能力，依次组织各方答案汇总、各方答案聚合（未核验）、权威核验后的最终答案和各方答案测评，生成可打开、可审计、可迁移的阶段产物与完整报告包。
- **goal-loop** — Draft and explain persistent goal-loop prompts for long-running agent work with clear stop conditions.
- **grok-build** — Delegate well-specified implementation tasks to xAI's Grok Build CLI running headlessly while the orchestrating agent plans, writes task specs, reviews every diff, and owns the result.
- **grok-delegate** — Delegate coding tasks to the Grok Build CLI only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **idea-evaluator** — Evaluates an idea by hosting a multi-turn debate between a Pro and Con agent, delivering a final verdict on whether it's worth pursuing.
- **jev-use** — Route enumerable judgment steps - did it work, which option, how risky, is this safe to run - to the Jev judgment model through the jev_judge and jev_gate MCP tools, batched into one call per state.
- **kimi-delegate** — Delegate coding tasks to the Kimi Code CLI (`kimi`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **multi-agent-task-orchestrator** — Route tasks to specialized AI agents with anti-duplication, quality gates, and 30-minute heartbeat monitoring
- **omp-delegate** — Delegate coding tasks to Oh My Pi (`omp`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **opencode-delegate** — Delegate coding tasks to the OpenCode CLI only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **orchestrate** — Coordinate focused subagents on substantial work, keep their ownership non-overlapping, and integrate verified results. Use for large-scope Codex tasks; keep trivial work with the coordinator.
- **pi-delegate** — Delegate coding tasks to the Pi coding agent CLI (`pi`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **polis-protocol-a-self-optimizing-city-of-agents** — Polis Protocol: A Self-Optimizing City of Agents
- **qoder-delegate** — Delegate coding tasks to the Qoder CLI (`qodercli`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **ralph-loop-yylo** — Execute exactly one explicitly assigned YYLO Ledger task through the Ralph loop to a validated queued commit. Use only when the user explicitly requests ralph-loop-yylo.
- **review-multi-agent-orchestration** — Use when a supervisor, swarm, graph, planner-worker system, or parallel agent workflow needs review for task boundaries, shared state, branch joins, retries, cancellation, context handoffs, budgets, deadlocks, or human escalation before implementation or production rollout.
- **stitch-loop** — Teaches agents to iteratively build websites using Stitch with an autonomous baton-passing loop pattern
- **subagent-orchestrator** — Coordinate quota-aware parallel subagents for large, multi-file Antigravity tasks.
- **vibe-delegate** — Delegate coding tasks to the Mistral Vibe CLI (`vibe`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **warp-delegate** — Delegate coding tasks to the Warp Agent CLI (`oz`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **zcode-delegate** — Delegate coding tasks to the Z.AI ZCode CLI only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/agent-orchestration/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/agent-orchestration`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
