# Claude AI Agent Configuration

## Overview

This project uses Claude AI as an intelligent development agent with structured workflows, specialized sub-agents, and mandatory coding standards.

---

## Development Workflow

Follow this workflow for all feature development:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   /spec  →  /plan  →  /build  →  /test  →  /review  →  Ship│
│                                                             │
│   Define    Plan     Build     Verify    Review     Deploy  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Phase | Command | Purpose |
|-------|---------|---------|
| **Define** | `/spec` | Create PRD with objectives, scope, boundaries |
| **Plan** | `/plan` | Decompose into vertical slices with acceptance criteria |
| **Build** | `/build` | Implement incrementally using TDD (RED-GREEN-REFACTOR) |
| **Verify** | `/test` | Write and verify tests; use Prove-It for bug fixes |
| **Review** | `/review` | Five-axis code review before merge |
| **Ship** | `/deploy` | Build, test, deploy with staged rollout |

### Supporting Commands

| Command | Purpose |
|---------|---------|
| `/debug` | Systematic error diagnosis and root cause analysis |
| `/simplify` | Reduce complexity without changing behavior |
| `/fix-issue` | Analyze and fix reported issues |

---

## Core Principles

### Code Quality
- **Test-Driven Development** — Write failing tests first, then implement
- **Incremental Implementation** — Small vertical slices, always buildable
- **Five-Axis Review** — Correctness, Readability, Architecture, Security, Performance

### Philosophy
- Progress over perfection
- Fix root causes, not symptoms
- The simplest thing that could work
- Tests are proof, not afterthought

---

## Mandatory Rules

All rules in `.claude/rules/` are **mandatory** and must be followed:

### Code Quality
| Rule | Description |
|------|-------------|
| `clean-code.md` | Variables, functions, SOLID, async/await |
| `code-style.md` | Formatting, naming conventions |
| `error-handling.md` | AppError class, global handler patterns |

### Architecture & Design
| Rule | Description |
|------|-------------|
| `tech-stack.md` | Approved technologies (Next.js, PG, Redis, Prisma) |
| `system-design.md` | CAP theorem, caching, scaling, queues |
| `project-structure.md` | Layered architecture, folder organization |
| `api-conventions.md` | REST standards, response envelopes |

### Data & Naming
| Rule | Description |
|------|-------------|
| `naming-conventions.md` | Cache keys, DB, queues, env vars |
| `database.md` | Prisma patterns, transactions, N+1 prevention |

### Operations
| Rule | Description |
|------|-------------|
| `security.md` | **CRITICAL** — Never violate security rules |
| `monitoring.md` | Prometheus, Grafana, logging, alerting |
| `testing.md` | Coverage thresholds, test patterns |
| `git-workflow.md` | Branching strategy, conventional commits |

---

## Available Agents

Invoke the right agent for each task type:

### Development Agents
| Agent | When to Invoke |
|-------|---------------|
| 🖥️ **Frontend Developer** | Components, pages, routing, state, UI performance |
| 🔧 **Backend Developer** | APIs, services, DB queries, background jobs |
| 🏗️ **Systems Architect** | Architecture decisions, ADRs, system design |

### Quality Agents
| Agent | When to Invoke |
|-------|---------------|
| 👀 **Code Reviewer** | Five-axis PR review, code quality assessment |
| 🧪 **Test Engineer** | Test strategy, TDD, coverage, bug reproduction |
| 🔒 **Security Auditor** | Vulnerability assessment, threat modeling |
| ✅ **QA Engineer** | Test plans, E2E tests, bug reports |

### Product Agents
| Agent | When to Invoke |
|-------|---------------|
| 📋 **Project Manager** | User stories, sprint planning, status reports |
| 🎨 **UI/UX Designer** | Design system, wireframes, accessibility |
| ✍️ **Copywriter/SEO** | Page copy, meta tags, SEO optimization |

---

## Available Skills

Specialized skills for complex operations:

| Skill | Description |
|-------|-------------|
| `tdd` | Test-Driven Development patterns |
| `code-review` | Five-axis review framework |
| `incremental-implementation` | Vertical slice development |
| `deploy` | Full deployment pipeline |
| `security-review` | Security audit checklist |

---

## Reference Checklists

Quick references in `.claude/references/`:

| Reference | Use For |
|-----------|---------|
| `security-checklist.md` | Pre-deploy security verification |
| `testing-patterns.md` | Test structure and anti-patterns |
| `performance-checklist.md` | Core Web Vitals, optimization |
| `accessibility-checklist.md` | WCAG 2.1 AA compliance |

---

## Agent Behavior Guidelines

1. **Follow the workflow** — Use `/spec` → `/plan` → `/build` → `/review`
2. **Apply mandatory rules** — All rules in `.claude/rules/` are non-negotiable
3. **Test first** — Write failing tests before implementing
4. **Incremental changes** — Small commits, always buildable
5. **Explain before acting** — Describe changes before making them
6. **Fix root causes** — Don't patch symptoms
7. **Use the right agent** — Invoke specialized agents for their domains
