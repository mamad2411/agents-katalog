# SpecLeap — Context for Google Gemini

**Methodology:** Spec-Driven Development (SDD)

---

## Overview

SpecLeap is a development framework that ensures:
- Contract-first development (CONTRATO.md defines scope)
- Conversational commands in Spanish
- Specialized AI agents for backend/frontend/product
- Global standards for code quality

---

## Getting Started

### Step 1: Trigger Initialization

Say **"Hola"** to start the onboarding flow.

### Step 2: Select Project

Choose from existing projects or create new one.

### Step 3: Execute Commands

Available commands:
- `refinar [proyecto]-XXX` → Refine Asana ticket
- `planificar [proyecto]-XXX` → Create implementation plan
- `implementar @plan.md` → Execute plan
- `explicar [topic]` → Explain code/architecture
- `documentar` → Update documentation

---

## Project Structure

Each project has:

**CONTRATO.md** (immutable)
- Scope definition
- Tech stack
- Modules & features
- Business rules

**context/** (updatable)
- brief.md — Executive summary
- architecture.md — Architecture decisions
- tech-stack.md — Technologies & versions
- conventions.md — Code patterns
- decisions.md — Technical decisions log

**specs/** (feature plans)
- Implementation plans per ticket
- Test specifications
- API documentation

---

## Standards

Read these before coding:

| File | Purpose |
|------|---------|
| `specs/base-standards.mdc` | Core principles (English only, TDD) |
| `specs/laravel-standards.mdc` | Laravel + PHP patterns |
| `specs/react-standards.mdc` | React + TypeScript patterns |
| `specs/backend-standards.mdc` | Backend architecture |
| `specs/frontend-standards.mdc` | Frontend architecture |

---

## Agent Roles

Adopt these personas when executing commands:

- **Backend Developer** (`.agents/backend.md`) — Laravel expert
- **Frontend Developer** (`.agents/frontend.md`) — React expert
- **Product Analyst** (`.agents/producto.md`) — User story refinement

---

## Workflow Example

```
User: Hola
AI: [List projects] "¿Qué proyecto?"

User: app-tienda y desarrollo
AI: [Load context] "Proyecto cargado. ¿Qué ticket?"

User: planificar app-tienda-23
AI: [Generate plan] "Plan creado en specs/app-tienda-23_backend.md"

User: implementar @app-tienda-23_backend.md
AI: [Execute] "Código implementado. PR creado."
```

---

## Critical Rules

1. CONTRATO.md never changes after approval
2. Use ANEXOS.md for new modules
3. Code in English, UI text in Spanish
4. Tests >= 90% coverage mandatory
5. Never push to main (always PR)
6. Follow project conventions.md

---

See `CLAUDE.md` for complete documentation.
