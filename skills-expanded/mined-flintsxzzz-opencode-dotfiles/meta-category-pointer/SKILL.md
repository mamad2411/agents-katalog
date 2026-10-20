---
name: meta-category-pointer
description: "Pointer to a library of 30 specialized Meta skills. Use when working on meta-related tasks."
risk: none
---

# Meta Capability Library 🎯

This is a **pointer skill**. The 30 specialized Meta skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **analyze-project** — Forensic root cause analyzer for Antigravity sessions. Classifies scope deltas, rework patterns, root causes, hotspots, and auto-improves prompts/health.
- **antigravity-skill-orchestrator** — A meta-skill that understands task requirements, dynamically selects appropriate skills, tracks successful skill combinations using agent-memory-mcp, and prevents skill overuse for simple tasks.
- **audit-context-building** — Enables ultra-granular, line-by-line code analysis to build deep architectural context before vulnerability or bug finding.
- **behavioral-modes** — AI operational modes (brainstorm, implement, debug, review, teach, ship, orchestrate). Use to adapt behavior based on task type.
- **cc-skill-backend-patterns** — Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes.
- **cc-skill-clickhouse-io** — ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads.
- **cc-skill-coding-standards** — Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js development.
- **cc-skill-continuous-learning** — Turn a completed debugging session or repeated user correction into a small, evidence-backed procedure. Use for explicit requests to capture reusable lessons; does not automatically extract or save memories.
- **cc-skill-frontend-patterns** — Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices.
- **cc-skill-project-guidelines-example** — Project Guidelines Skill (Example)
- **cc-skill-security-review** — This skill ensures all code follows security best practices and identifies potential vulnerabilities. Use when implementing authentication or authorization, handling user input or file uploads, or creating new API endpoints.
- **cc-skill-strategic-compact** — Prepare a verified checkpoint before condensing an agent conversation at a phase boundary. Use during long tasks when context is repetitive; preserves constraints, evidence, decisions and the next action.
- **context7-auto-research** — Automatically fetch latest library/framework documentation for Claude Code via Context7 API. Use when you need up-to-date documentation for libraries and frameworks or asking about React, Next.js, Prisma, or any other popular library.
- **diary** — Unified Diary System: A context-preserving automated logger for multi-project development.
- **filesystem-context** — Use for file-based context management, dynamic context discovery, and reducing context window bloat. Offload context to files for just-in-time loading.
- **skill-creator** — To create new CLI skills following Anthropic's official best practices with zero manual configuration. This skill automates brainstorming, template application, validation, and installation processes while maintaining progressive disclosure patterns and writing style standards.
- **skill-creator-ms** — Guide for creating effective skills for AI coding agents working with Azure SDKs and Microsoft Foundry services. Use when creating new skills or updating existing skills.
- **skill-developer** — Comprehensive guide for creating and managing skills in Claude Code with auto-activation system, following Anthropic's official best practices including the 500-line rule and progressive disclosure pattern.
- **skill-improver** — Iteratively improve a Claude Code skill using the skill-reviewer agent until it meets quality standards. Use when improving a skill with multiple quality issues, iterating on a new skill until it meets standards, or automated fix-review cycles instead of manual editing.
- **skill-installer** — Instala, valida, registra e verifica novas skills no ecossistema. 10 checks de seguranca, copia, registro no orchestrator e verificacao pos-instalacao.
- **skill-issue** — Find out why a coding-agent skill won't fire — grade each SKILL.md A–F on activation, simulate which skill a prompt triggers, and flag collisions where one silently shadows another.
- **skill-rails-upgrade** — Analyze Rails apps and provide upgrade assessments
- **skill-router** — Use when the user is unsure which skill to use or where to start. Interviews the user with targeted questions and recommends the best skill(s) from the installed library for their goal.
- **skill-scanner** — Scan agent skills for security issues before adoption. Detects prompt injection, malicious code, excessive permissions, secret exposure, and supply chain risks.
- **skill-seekers** — -Automatically convert documentation websites, GitHub repositories, and PDFs into Claude AI skills in minutes.
- **skill-sentinel** — Auditoria e evolucao do ecossistema de skills. Qualidade de codigo, seguranca, custos, gaps, duplicacoes, dependencias e relatorios de saude.
- **skill-suggester** — Scan prompt history for recurring patterns and unmet needs, then propose new skills or command templates
- **skill-writer** — Create and improve agent skills following the Agent Skills specification. Use when asked to create, write, or update skills.
- **wgm** — Turns a rough request into working software via a governed build loop: align first, plan, then iterate one task at a time with deterministic backpressure and holdout-scenario judging.
- **writing-skills** — Use when creating, updating, or improving agent skills.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/meta/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/meta`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
