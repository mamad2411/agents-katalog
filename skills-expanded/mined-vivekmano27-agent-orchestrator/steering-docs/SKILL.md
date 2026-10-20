---
name: steering-docs
description: Generate persistent project context files — product.md, tech.md, structure.md — that guide every coding session. Use when setting up a new project, creating project context, or when the user mentions "steering documents", "project context", "product vision", or "tech stack documentation".
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Steering Documents Skill

Create three persistent context files in `.claude/steering/` that the agent reads at the start of every session.

## 1. product.md — Product Context

```markdown
# Product Context

## Vision
[One paragraph: what this product will become]

## Problem Statement
[What pain point does this solve?]

## Target Users
- Primary: [Who, demographics, tech proficiency]
- Secondary: [Who else uses it]

## Success Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| [KPI]  | [Goal] | [How to measure] |

## Competitive Landscape
| Competitor | Strengths | Our Differentiation |
|-----------|-----------|-------------------|
| [Name]   | [What they do well] | [Why we're different] |
```

## 2. tech.md — Technical Context

```markdown
# Technical Context

## Stack
- Language: [e.g., TypeScript 6+]
- Framework: [e.g., Next.js 16+ App Router]
- Database: [e.g., PostgreSQL 18+ via Prisma]
- Auth: [e.g., NextAuth.js v5]
- Hosting: [e.g., Vercel + Supabase]
- CI/CD: [e.g., GitHub Actions]

## Architecture Pattern
[e.g., "Modular monolith with clean architecture layers"]

## Key Libraries
| Library | Purpose | Version |
|---------|---------|---------|
| [name]  | [what it does] | [version] |

## Performance Targets
- Page load: < [X]s
- API response: < [X]ms
- Lighthouse score: > [X]

## Third-Party Services
| Service | Purpose | Env Var |
|---------|---------|---------|
| [name]  | [use]   | [VAR_NAME] |
```

## 3. structure.md — Project Structure

```markdown
# Project Structure

## Directory Layout
```
src/
├── app/           → Next.js routes and pages
├── components/    → Reusable UI components
│   ├── ui/        → Primitive components (Button, Input)
│   └── features/  → Feature-specific components
├── lib/           → Shared utilities and helpers
├── services/      → Business logic and API calls
├── models/        → Data models and types
├── hooks/         → Custom React hooks
└── config/        → App configuration
```

## Naming Conventions
- Files: kebab-case (user-profile.tsx)
- Components: PascalCase (UserProfile)
- Functions: camelCase (getUserProfile)
- Constants: SCREAMING_SNAKE (MAX_RETRIES)
- Types: PascalCase with suffix (UserProfileProps)

## Module Rules
- Components NEVER import from services directly — use hooks
- Services NEVER import from components
- Models are shared across all layers
- Config is read-only at runtime
```

## Anti-Patterns

- **Stale steering docs** — writing them once and never updating; docs must evolve with the project or they mislead
- **Too much detail** — writing 500+ lines of rules that nobody reads; keep each doc focused and scannable
- **Duplicating CLAUDE.md** — steering docs complement CLAUDE.md, not duplicate it; CLAUDE.md has repo rules, steering docs have product/tech/structure context
- **No product context** — only documenting technical decisions without explaining what the product does and why; agents need business context to make good decisions
- **Missing structure.md** — documenting product and tech without documenting how the code is organized; agents waste time exploring instead of navigating directly

## Checklist

- [ ] product.md created (what the product does, who uses it, key workflows)
- [ ] tech.md created (stack decisions, patterns, external services, environment setup)
- [ ] structure.md created (directory layout, module responsibilities, import rules)
- [ ] All three docs use project-config.md values (not hardcoded stack assumptions)
- [ ] Docs are concise (each under 200 lines)
- [ ] Docs saved to project root or `.claude/` directory
- [ ] Updated when significant architecture or product changes occur
