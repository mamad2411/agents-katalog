---
name: agent-orchestration-category-pointer
description: "Pointer to a library of 25 specialized Agent Orchestration skills. Use when working on agent-orchestration-related tasks."
risk: none
---

# Agent Orchestration Capability Library 🎯

This is a **pointer skill**. The 25 specialized Agent Orchestration skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **agent-self-scheduling** — Schedule AI agent runs with cron, loops, or external clocks while avoiding unsafe tight autonomous timers.
- **agy-delegate** — Delegate coding tasks to the Google Antigravity CLI (`agy`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **aider-delegate** — Delegate coding tasks to Aider (`aider`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **claude-delegate** — Delegate coding tasks to a separate Claude Code CLI process or Claude session only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **cline-delegate** — Delegate coding tasks to the Cline CLI (`cline`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **codex-delegate** — Delegate coding tasks to the OpenAI Codex CLI only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **codex-subagent** — Launch Codex CLI as an isolated subagent for bounded coding, review, or verification tasks.
- **commandcode-delegate** — Delegate coding tasks to the Command Code CLI (`cmd`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **copilot-delegate** — Delegate coding tasks to the GitHub Copilot CLI (`copilot`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **cursor-delegate** — Delegate coding tasks to the Cursor Agent CLI (`cursor-agent`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **delegate-setup** — Configure approved delegation lanes across installed implementer CLIs, including optional model and effort choices, then write global or project config only after explicit user approval.
- **delegating-to-agents** — Delegate bounded work to other AI agents while preserving context, ownership, and progress checks.
- **goal-loop** — Draft and explain persistent goal-loop prompts for long-running agent work with clear stop conditions.
- **grok-build** — Delegate well-specified implementation tasks to xAI's Grok Build CLI running headlessly while the orchestrating agent plans, writes task specs, reviews every diff, and owns the result.
- **grok-delegate** — Delegate coding tasks to the Grok Build CLI only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **kimi-delegate** — Delegate coding tasks to the Kimi Code CLI (`kimi`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **multi-agent-task-orchestrator** — Route tasks to specialized AI agents with anti-duplication, quality gates, and 30-minute heartbeat monitoring
- **omp-delegate** — Delegate coding tasks to Oh My Pi (`omp`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **opencode-delegate** — Delegate coding tasks to the OpenCode CLI only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **orchestrate** — Coordinate focused subagents on substantial work, keep their ownership non-overlapping, and integrate verified results. Use for large-scope Codex tasks; keep trivial work with the coordinator.
- **pi-delegate** — Delegate coding tasks to the Pi coding agent CLI (`pi`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **qoder-delegate** — Delegate coding tasks to the Qoder CLI (`qodercli`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **vibe-delegate** — Delegate coding tasks to the Mistral Vibe CLI (`vibe`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **warp-delegate** — Delegate coding tasks to the Warp Agent CLI (`oz`) only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.
- **zcode-delegate** — Delegate coding tasks to the Z.AI ZCode CLI only when the user explicitly requests it, while the orchestrator retains review and landing responsibility.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/agent-orchestration/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/agent-orchestration`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
