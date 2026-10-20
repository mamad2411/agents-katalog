# SpecLeap — Generic Agent Configuration

**For:** AI assistants that don't use specific config files (Claude Code, Cursor, etc.)

**See also:** `CLAUDE.md` (Claude-specific), `codex.md` (GitHub Copilot), `GEMINI.md` (Google Gemini)

---

## What is SpecLeap?

A development framework for spec-driven development with:
- Multi-project support (`proyectos/`)
- Immutable contracts (CONTRATO.md)
- Conversational commands in Spanish
- Specialized agent roles
- Global code standards

---

## Quick Start

1. Say **"Hola"** to initialize
2. Select project or create new
3. Use commands: `refinar`, `planificar`, `implementar`, `explicar`, `documentar`
4. Follow generated plans
5. Create PR (tests >= 90%)

---

## Standards (Always Apply)

Read these files before writing code:

### Global Standards
- `specs/base-standards.mdc` — Core principles
- `specs/backend-standards.mdc` — Backend architecture
- `specs/frontend-standards.mdc` — Frontend architecture
- `specs/documentation-standards.mdc` — Documentation

### Technology-Specific
- `specs/laravel-standards.mdc` — Laravel + PHP
- `specs/react-standards.mdc` — React + TypeScript

### Project-Specific
- `proyectos/[project]/context/conventions.md` — Code patterns
- `proyectos/[project]/CONTRATO.md` — Scope & rules

---

## Commands

| Command | File | Description |
|---------|------|-------------|
| "Hola" | `.commands/inicio.md` | Initialize session |
| `refinar [proyecto]-XXX` | `.commands/refinar.md` | Refine user story |
| `planificar [proyecto]-XXX` | `.commands/planificar.md` | Create implementation plan |
| `implementar @plan.md` | `.commands/implementar.md` | Execute plan |
| `explicar [topic]` | `.commands/explicar.md` | Explain code/architecture |
| `documentar` | `.commands/documentar.md` | Update documentation |

---

## Agent Roles

Adopt these roles when executing commands:

- **`.agents/backend.md`** — Backend development (Laravel, PHP, APIs)
- **`.agents/frontend.md`** — Frontend development (React, TypeScript)
- **`.agents/producto.md`** — Product analysis & user story refinement

**When to adopt:**
- `refinar` → Use `.agents/producto.md`
- `planificar` backend → Use `.agents/backend.md`
- `planificar` frontend → Use `.agents/frontend.md`
- `implementar` → Use role matching the plan type

---

## Project Structure

```
specleap/
├── proyectos/                  # Independent projects
│   ├── _template/              # Template for new projects
│   └── [project-name]/
│       ├── CONTRATO.md         # Immutable contract
│       ├── ANEXOS.md           # Improvements log
│       ├── context/            # Project memory
│       └── specs/              # Implementation plans
├── .agents/                    # Agent role definitions
├── .commands/                  # Command specifications
├── specs/                      # Global standards
└── openspec/                   # CLI tools (optional)
```

---

## Critical Rules

1. **CONTRATO.md is immutable** — Never modify after approval
2. **ANEXOS.md for improvements** — New modules go here
3. **English for code** — Variables, functions, comments
4. **Spanish for UI** — Error messages, user-facing text
5. **Tests >= 90%** — Mandatory coverage
6. **Never push to main** — Always create PR
7. **Follow conventions.md** — Each project has patterns

---

## Workflow Example

```
User: Hola
AI: [Execute .commands/inicio.md]
    List projects → Ask which one

User: app-tienda y desarrollo
AI: Load CONTRATO.md + context/
    "¿Qué ticket trabajarás?"

User: refinar app-tienda-23
AI: [Adopt .agents/producto.md]
    Refine user story → Update Asana

User: planificar app-tienda-23
AI: [Adopt .agents/backend.md]
    Generate plan → Save to specs/

User: implementar @app-tienda-23_backend.md
AI: [Adopt .agents/backend.md]
    Create branch → Code → Tests → PR
```

---

## MCP Integrations (If Available)

- **Asana MCP** — Read/update tickets
- **Context7 MCP** — Fetch library docs (Laravel, React)

---

## References

- Full documentation: `CLAUDE.md`
- Commands: `.commands/*.md`
- Agents: `.agents/*.md`
- Standards: `specs/*.mdc`
- CLI tools: `openspec/cli/`

---

*SpecLeap by Conceptual Creative*
