# SpecLeap — Context for Claude Code & Claude API

**Methodology:** Spec-Driven Development (SDD). Spec first, never code first.

---

## 🌐 Default Language: SPANISH

**CRITICAL:** All feedback, messages, commit messages, and user-facing text MUST be in SPANISH.

This project is for Spanish-speaking teams. All agents, commands, and responses must use Spanish unless explicitly overridden.

**Examples:**
❌ "Generating plan..."
✅ "Generando plan..."

❌ "Tests passed"
✅ "Tests pasaron"

See individual agent files (`.agents/*.md`) for specific language directives.

---

## Project Structure

This is **SpecLeap**, a development framework that combines:
- **Conversational agents** (specialized roles with commands)
- **Spec-Driven Development** (contracts first, code second)
- **Multi-project support** (independent projects with contracts)

---

## Core Principles

1. **CONTRATO.md is IMMUTABLE** — Once accepted, never modify. Use ANEXOS.md for improvements.
2. **Projects are independent** — Each project in `proyectos/` has its own contract and context.
3. **Commands are in Spanish** — `refinar`, `planificar`, `implementar`, `explicar`, `documentar`
4. **Agents have roles** — Backend, Frontend, Product Analyst (see `.agents/`)
5. **Standards are global** — `specs/*.mdc` apply to ALL projects

---

## Getting Started

### Trigger Word: "Hola"

When the user says **"Hola"** (case-insensitive), execute `.commands/inicio.md`:
1. List available projects in `proyectos/`
2. Ask which project to work on (or new project)
3. Load project context (CONTRATO.md + context/)
4. Ask what type of work (DESARROLLO / DOCUMENTACIÓN)

---

## Command Detection (CRITICAL)

**When the user writes a SINGLE command keyword** (e.g., just `refinar` or `crear-tickets`), **AUTOMATICALLY**:

1. **Detect the command** from the message
2. **Read the corresponding `.commands/*.md` file**
3. **Follow the instructions in that file step-by-step**

**Command-to-File Mapping:**

| User writes | Read this file | Then execute |
|-------------|----------------|--------------|
| `inicio` or `Hola` | `.commands/inicio.md` | Start workflow |
| `ayuda`, `help`, `comandos` | `.commands/ayuda.md` | List ALL available commands |
| `refinar` | `.commands/refinar.md` | Refine user story |
| `planificar` | `.commands/planificar.md` | Generate backlog |
| `crear-tickets` | `.commands/crear-tickets.md` | Alias of `planificar` |
| `implementar` | `.commands/implementar.md` | Execute implementation |
| `explicar` | `.commands/explicar.md` | Explain concept |
| `documentar` | `.commands/documentar.md` | Update docs |
| `adoptar` | `.commands/adoptar.md` | Adopt legacy project |
| `compliance`, `auditoria`, `audit` | `.commands/compliance.md` | Run framework self-audit (6 dimensions, 0-100 score) |

**Rules:**
- If user writes `comando` alone → read `.commands/comando.md` immediately
- If user writes `comando` + context → read file + use context
- NEVER ask "should I read the file?" — just read it

**Format note:** Commands are plain keywords (no `/`, no `.`). The `/` prefix is reserved by Claude Code for its own native slash commands (`/help`, `/clear`, `/model`, etc.), so SpecLeap commands must be written without it to avoid collision. The `.commands/file.md` path is an internal file reference, not a command syntax.

---

## Commands Available

| Command | Description | Agente |
|---------|-------------|--------|
| `refinar [proyecto]-XXX` | Refine Asana user story | producto.md |
| `planificar [proyecto]-XXX` | Generate implementation plan | backend.md / frontend.md |
| `implementar @plan.md` | Execute plan: branch + code + tests + PR | backend.md / frontend.md |
| `explicar [concepto]` | Explain code/architecture/decisions | neutral |
| `documentar` | Update technical documentation | neutral |

**See:** `.commands/` for detailed command specifications.

---

## Agents

Adopt these roles when executing commands:

- **`.agents/backend.md`** — Laravel + PHP + API expert
- **`.agents/frontend.md`** — React + TypeScript + Vite expert
- **`.agents/producto.md`** — Product analyst + user story enrichment

**When to adopt:**
- `refinar` → producto.md
- `planificar` backend → backend.md
- `planificar` frontend → frontend.md
- `implementar` → backend.md or frontend.md (depending on plan)

---

## Quality Baseline and Evidence

SpecLeap versions quality thresholds and preserves audit evidence per feature:

- **`.quality/baselines/baseline.json`** — shared thresholds (coverage 80/90%, complexity 10, duplicates 3%) plus a repo snapshot. Versioned.
- **`.quality/evidence/[feature-slug]/`** — per-feature audit trail (ticket metadata, test outputs, security scans, decision log, healing telemetry). NOT versioned; regenerated per feature.
- **`scripts/quality-baseline.sh`** — helper with three verbs: `init`, `snapshot`, `new-evidence [slug]`.
- **`scripts/quality-healing.sh`** — helper that appends JSONL healing entries to `.quality/evidence/[slug]/healing.jsonl`. Verbs: `log`, `show`, `stats`.

See `.quality/README.md` for usage details.

---

## Spec-guard Hook

A Claude Code `PreToolUse` hook blocks `Write`/`Edit`/`NotebookEdit` on files under `src/`, `app/`, `tests/`, `test/` or `lib/` when the current git branch is one of the protected ones (`main`, `stage`, `develop`). This enforces the "no code without an active feature branch" rule.

- **Hook:** `.claude/hooks/spec-guard.sh`
- **Template config:** `.claude/settings.json.template`
- **Philosophy:** fail-open — if the hook hits an internal error (no git repo, no jq, malformed stdin), it exits 0 (allow). It only blocks when it is certain the rule applies.
- **Bypass for framework maintenance:** docs (`*.md`), root configs (`package.json`, `.env`), `scripts/` and framework context files (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `codex.md`) are never blocked.

### Manual activation in a consumer project

Copy these two files into the consumer project root:

```bash
mkdir -p .claude/hooks
cp /path/to/specleap-framework/.claude/hooks/spec-guard.sh .claude/hooks/spec-guard.sh
chmod +x .claude/hooks/spec-guard.sh
```

Then merge `.claude/settings.json.template` content into the project's `.claude/settings.json` (create the file if it doesn't exist). If the file already has `hooks.PreToolUse` entries, append the new matcher rather than overwrite.

Automatic integration via `setup.sh` is planned for a later release.

---

## Standards (Always Apply)

Read and follow these standards for ALL code:

### Global Standards
1. **`specs/base-standards.mdc`** — Core principles (English only, TDD, small steps)
2. **`specs/backend-standards.mdc`** — Backend patterns (DDD, testing)
3. **`specs/frontend-standards.mdc`** — Frontend patterns (components, state)
4. **`specs/documentation-standards.mdc`** — Documentation structure

### Technology-Specific Standards
5. **`specs/laravel-standards.mdc`** — Laravel + PHP + Eloquent
6. **`specs/react-standards.mdc`** — React + TypeScript + hooks

**Always read relevant standards before implementing.**

---

## Agent Skills (Progressive Disclosure)

SpecLeap installs **20 curated Agent Skills** in `~/.claude/skills/` (the canonical path Claude Code auto-discovers). They activate automatically when the conversation context matches each skill's `description` frontmatter.

**Source repos:**
- `obra/superpowers` — quality/process skills
- `jeffallan/claude-skills` — stack specialists
- `anthropics/skills` — design
- `vercel-labs/agent-skills` — React/Next/web
- `shadcn-ui/ui` — shadcn components
- `supabase/agent-skills` — PostgreSQL
- `arvindrk/extract-design-system` — design-system extraction
- `alirezarezvani/claude-skills` — GDPR

### Activation Triggers

Skills load knowledge **only when needed** based on context:

```
User: "Crear endpoint POST /api/products con validación"

Auto-activates:
  ✓ verification-before-completion
  ✓ laravel-specialist
  ✓ api-designer
  ✓ database-optimizer
  ✓ security-reviewer
```

### Critical Skills

#### verification-before-completion ⭐ **MANDATORY**

**Before claiming work is complete, fixed, or passing:**
1. **RUN** the verification commands fresh (tests, lint, type-check, manual curl, etc.).
2. **CONFIRM** the output is what you expected — paste the evidence.
3. **ONLY THEN** mark the work as done, commit, or open a PR.

**Iron law:** *"No completion claims without fresh verification evidence."*

#### systematic-debugging

When a bug shows up, follow the loop: reproduce → isolate → form hypothesis → test hypothesis → fix → verify. No guessing, no "this should work".

#### test-driven-development

Write the failing test first, then the minimal code to make it pass, then refactor. Coverage target ≥ 90%.

#### code-reviewer + requesting-code-review + receiving-code-review

The three skills cover the full review cycle: self-review before requesting review, asking for review with focus areas, and reacting to review feedback constructively.

### Skill Catalogue (20)

**🔄 Core / Quality (5):**
- verification-before-completion ⭐
- systematic-debugging
- requesting-code-review
- receiving-code-review
- test-driven-development

**🛠️ Backend (4) — Laravel + PostgreSQL:**
- laravel-specialist
- api-designer
- database-optimizer
- supabase-postgres-best-practices

**⚛️ Frontend (4) — React + TypeScript + shadcn:**
- react-expert
- typescript-pro
- vercel-react-best-practices
- shadcn

**🎨 Design (3):**
- frontend-design
- web-design-guidelines
- extract-design-system

**🔒 Security (2):**
- security-reviewer
- gdpr-dsgvo-expert

**🔁 Process (2):**
- code-reviewer
- brainstorming

**See:** [SETUP.md](SETUP.md) for installation details.

---

## Project Structure

```
proyectos/[project-name]/
├── CONTRATO.md          # 🔒 IMMUTABLE contract
├── ANEXOS.md            # ✏️ Improvements/modules
├── context/             # Memory-bank
│   ├── brief.md
│   ├── architecture.md
│   ├── tech-stack.md
│   ├── conventions.md
│   └── decisions.md
└── specs/               # Feature specs
    ├── [TICKET-ID]_backend.md
    └── [TICKET-ID]_frontend.md
```

**Before working on a project:**
1. Read `CONTRATO.md` — Understand the contract
2. Read `context/architecture.md` — Understand architecture
3. Read `context/conventions.md` — Follow code patterns

---

## Workflow Example

```
User: "Hola"
AI: [Execute .commands/inicio.md]
    - List projects
    - Ask which project + type of work

User: "app-tienda y desarrollo"
AI: [Load proyectos/app-tienda/CONTRATO.md + context/]
    "✅ Proyecto app-tienda cargado. ¿Qué ticket trabajarás?"

User: "app-tienda-23"
AI: "¿Refinar o planificar directamente?"

User: "planificar app-tienda-23"
AI: [Adopt .agents/backend.md]
    [Read CONTRATO + context + ticket]
    [Generate plan in specs/app-tienda-23_backend.md]
    "📋 Plan creado. Revisar antes de implementar."

User: "implementar @app-tienda-23_backend.md"
AI: [Adopt .agents/backend.md]
    [Execute plan step by step]
    [Tests, commit, push, PR]
    "✅ Implementación completada. PR: [URL]"
```

---

## CLI Tools (Optional)

Besides conversational commands, the `openspec` CLI is available:

```bash
openspec enrich "user story"      # Refine user story
openspec new --auto "feature"     # Create proposal
openspec verify CHANGE-001        # Verify tests
openspec status                   # List proposals
```

See: `openspec/cli/README.md`

---

## MCP Integrations

### ⚠️ Asana MCP (MANDATORY)

**Asana is MANDATORY for SpecLeap workflow.**

MUST use for:
- `crear-tickets` — Generate all tickets from CONTRATO.md
- `refinar [proyecto]-XXX` — Read and enrich ticket
- `planificar [proyecto]-XXX` — Read ticket for plan generation
- `implementar` — Update ticket status during implementation
- Automatic updates: "To Do" → "In Progress" → "In Review" → "Done"

**Without Asana MCP, the workflow DOES NOT WORK.**

### CodeRabbit (Recommended)

**Automatic code review on all PRs.**

- Install CodeRabbit GitHub App on repos
- Copy `.coderabbit.yaml` from `proyectos/_template/`
- Reviews in Spanish
- Checks: specs compliance, tests >= 90%, security, standards
- `implementar` waits for CodeRabbit approval before marking complete

### Context7 MCP (Optional)

If configured, use for:
- Fetching up-to-date library documentation (Laravel, React, etc.)
- Avoid outdated knowledge

---

## Critical Rules

1. **NEVER modify CONTRATO.md** after accepted — Only add to ANEXOS.md
2. **NEVER push to main directly** — Always via PR
3. **Tests must pass** — >= 90% coverage
4. **Follow conventions.md** — Each project has specific patterns
5. **All code in ENGLISH** — Variables, functions, comments, docs
6. **User-facing text in SPANISH** — Error messages, UI text

---

## References

- **Commands:** `.commands/*.md`
- **Agents:** `.agents/*.md`
- **Standards:** `specs/*.mdc`
- **Project Template:** `proyectos/_template/`
- **CLI Reference:** `openspec/cli/COMMAND_REFERENCE.md`

---

**When in doubt:**
1. Read the relevant `.commands/` file
2. Adopt the specified `.agents/` role
3. Follow `specs/` standards
4. Ask the user for clarification

---

*Made with ❤️ by the SpecLeap Community*
