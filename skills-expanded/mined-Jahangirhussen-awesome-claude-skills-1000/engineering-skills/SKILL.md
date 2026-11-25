---
name: "engineering-skills"
description: "Index of the engineering-team skills bundle for Claude Code, Codex, Gemini CLI, Cursor, OpenClaw, and 6 more tools. Architecture, frontend, backend, QA, DevOps, security, AI/ML, data engineering, Playwright, Stripe, AWS, MS365 (stdlib-only Python tools). Use when browsing or choosing among engineering-team role skills — load only the one specialist SKILL.md you need, never bulk-load the bundle."
version: 2.9.0
author: Alireza Rezvani
license: MIT
tags:
  - engineering
  - frontend
  - backend
  - devops
  - security
  - ai-ml
  - data-engineering
agents:
  - claude-code
  - codex-cli
  - openclaw
---

# Engineering Team Skills

32 production-ready engineering skills organized into core engineering, security, AI/ML/Data, and specialized tools.

## Quick Start

### Claude Code
```
/read engineering-team/skills/senior-fullstack/SKILL.md
```

### Codex CLI
```bash
npx agent-skills-cli add alirezarezvani/claude-skills/engineering-team
```

## Skills Overview

### Core Engineering (13 skills)

| Skill | Folder | Focus |
|-------|--------|-------|
| Senior Architect | `senior-architect/` | System design, architecture patterns |
| Senior Frontend | `senior-frontend/` | React, Next.js, TypeScript, Tailwind |
| Senior Backend | `senior-backend/` | API design, database optimization |
| Senior Fullstack | `senior-fullstack/` | Project scaffolding, code quality |
| Senior QA | `senior-qa/` | Test generation, coverage analysis |
| Senior DevOps | `senior-devops/` | CI/CD, infrastructure, containers |
| Senior SecOps | `senior-secops/` | Security operations, vulnerability management |
| Code Reviewer | `code-reviewer/` | PR review, code quality analysis |
| Senior Security | `senior-security/` | Threat modeling, STRIDE, penetration testing |
| AWS Solution Architect | `aws-solution-architect/` | Serverless, CloudFormation, cost optimization |
| MS365 Tenant Manager | `ms365-tenant-manager/` | Microsoft 365 administration |
| TDD Guide | `tdd-guide/` | Test-driven development workflows |
| Tech Stack Evaluator | `tech-stack-evaluator/` | Technology comparison, TCO analysis |

### AI/ML/Data (5 skills)

| Skill | Folder | Focus |
|-------|--------|-------|
| Senior Data Scientist | `senior-data-scientist/` | Statistical modeling, experimentation |
| Senior Data Engineer | `senior-data-engineer/` | Pipelines, ETL, data quality |
| Senior ML Engineer | `senior-ml-engineer/` | Model deployment, MLOps, LLM integration |
| Senior Prompt Engineer | `senior-prompt-engineer/` | Prompt optimization, RAG, agents |
| Senior Computer Vision | `senior-computer-vision/` | Object detection, segmentation |

### Specialized Tools (5 skills)

| Skill | Folder | Focus |
|-------|--------|-------|
| Playwright Pro | `playwright-pro/` | E2E testing (9 sub-skills) |
| Self-Improving Agent | `self-improving-agent/` | Memory curation (5 sub-skills) |
| Stripe Integration | `stripe-integration-expert/` | Payment integration, webhooks |
| Incident Commander | `incident-commander/` | Incident response workflows |
| Email Template Builder | `email-template-builder/` | HTML email generation |

## Python Tools

30+ scripts, all stdlib-only. Run directly:

```bash
python3 <skill>/scripts/<tool>.py --help
```

No pip install needed. Scripts include embedded samples for demo mode.

## Rules

- Load only the specific skill SKILL.md you need — don't bulk-load all 32
- Use Python tools for analysis and scaffolding, not manual judgment
- Check CLAUDE.md for tool usage examples and workflows

## When to use
Browsing or choosing among the 32 engineering-team skills (architecture, frontend, backend, QA, DevOps, security, AI/ML, data, tools).

## When NOT to use
- A specific engineering skill is already known (open it directly).
- Non-engineering requests.

## Inputs
The engineering task and stack.

## Edge cases and failure handling
- No skill fits -> use general engineering capability and say so.
- Several fit -> start with the architecture skill, then specialists.

## Validation
- The chosen skill's focus matches the task; its SKILL.md was opened before acting.

## Related skills
engineering-advanced-skills, senior-architect, senior-fullstack
