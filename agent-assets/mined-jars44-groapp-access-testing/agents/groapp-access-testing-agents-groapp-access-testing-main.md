# AGENTS.md — Cross-Tool Discovery

> This file is discovered by OpenCode, Claude Code, OpenClaw, Antigravity, and other AI coding tools.

## Entry Sequence (All Tools)

```text
0. READ .agent/SYSTEM_PROMPT.md  — master agent protocol (THIS WINS OVER EVERYTHING)
1. READ AGENTS.md            — this file, orchestration entry point
2. READ CLAUDE.md            — AI behavior & output rules
3. READ .agent/README.md     — agent metadata center
4. READ task-specific docs   — constitution, workflows, personas, skills
5. EXECUTE task              — following SOP in docs/workflows/
6. WRITE result              — update .agent/state.json
7. RUN quality gate          — docs/constitution/004-quality-gate.md
```

## Multi-Agent Orchestration

This project implements **Mode C: Maximum Parallelism** for reducing wall-clock time.

Read `docs/workflows/002-multi-agent-orchestration.md` for full pipeline.

## Tool Discovery Map

| Tool            | Config File                      | How to Load                       |
| --------------- | -------------------------------- | --------------------------------- |
| **OpenCode**    | `opencode.json` + `.opencode/`   | Auto-discovered from project root |
| **Claude Code** | `CLAUDE.md` + `.claude/`         | Read from project root            |
| **OpenClaw**    | `AGENTS.md`                      | Read from project root            |
| **Antigravity** | `antigravity.json` + `AGENTS.md` | Read from project root            |
| **Hermes**      | `AGENTS.md`                      | Read from project root            |

## Directory Architecture

```text
project/
├── AGENTS.md                    ← Entry point for all tools
├── CLAUDE.md                    ← AI behavior rules (Claude Code, others)
├── opencode.json               ← OpenCode config (agents, commands, permissions)
├── antigravity.json            ← Antigravity config (agents, goals)
├── .opencode/                  ← OpenCode custom agents + commands
│   ├── agents/
│   │   ├── lead.md             ← Orchestrator (primary agent)
│   │   ├── researcher.md       ← Code explorer (subagent)
│   │   ├── builder.md          ← Test implementor (subagent)
│   │   ├── reflector.md        ← Self-critique (subagent)
│   │   ├── qa-gatekeeper.md    ← Test runner (subagent)
│   │   ├── reviewer.md         ← Code auditor (subagent)
│   │   └── senior-qa-engineer.md ← Default persona (primary)
│   ├── commands/
│   └── skills/
├── .claude/                    ← Claude Code custom agents + commands + skills
│   ├── agents/
│   │   ├── lead.md
│   │   ├── researcher.md
│   │   ├── builder.md
│   │   ├── reflector.md
│   │   ├── qa-gatekeeper.md
│   │   ├── reviewer.md
│   │   └── senior-qa-engineer.md
│   ├── commands/
│   └── skills/
├── .agent/                     ← Universal metadata center
│   ├── SYSTEM_PROMPT.md        ← Master agent protocol (THIS WINS OVER EVERYTHING)
│   ├── README.md               ← Agent metadata center entrypoint
│   ├── state.json              ← Pipeline state machine
│   ├── settings.json           ← Runtime config, persona tool restrictions
│   ├── mcp.json                ← MCP tool schema
│   ├── memory/                 ← Cross-session knowledge graph
│   │   ├── schema.md           ← Entity/relation schemas
│   │   └── entities/           ← Per-entity JSON files
│   ├── plans/                  ← Test plans + per-TC todos
│   │   └── todos/              ← Per-TC todo files
│   ├── tasks/                  ← Per-agent output files
│   ├── reports/                ← Implementation summaries
│   ├── templates/              ← Dispatch prompts + implementation-plan template
│   └── hooks/                  ← Pre/post validation scripts
├── docs/
│   ├── constitution/           ← Non-negotiable rules (001-005)
│   ├── workflows/              ← SOPs (000-003)
│   ├── personas/               ← Agent role definitions
│   └── reference/              ← Tech stack, directory, test data
└── skills/                     ← Specialized skills
    ├── dispatching-e2e-tests/
    ├── auditing-selector-quality/
    └── memory-management/
```

## Agent Personas

| Persona            | File                                  | Role                            |
| ------------------ | ------------------------------------- | ------------------------------- |
| Lead Orchestrator  | `docs/personas/orchestrator-lead.md`  | Planning, delegation, teardown  |
| Researcher         | `docs/personas/researcher.md`         | Read-only code exploration      |
| Builder            | `docs/personas/builder.md`            | POM + spec implementation       |
| Reflector          | `docs/personas/reflector.md`          | Self-critique before QA         |
| QA Gatekeeper      | `docs/personas/qa-gatekeeper.md`      | Test execution, flakiness check |
| Reviewer           | `docs/personas/reviewer.md`           | Code audit (Stage 1 + Stage 2)  |
| Senior QA Engineer | `docs/personas/senior-qa-engineer.md` | Default persona, test strategy  |

## Templates

| Template            | File                                               | Purpose                                                |
| ------------------- | -------------------------------------------------- | ------------------------------------------------------ |
| Per-TC Todo         | `.agent/templates/tc-template.md`                  | One test case — ownership, status, selectors, evidence |
| Implementation Plan | `.agent/templates/implementation-plan-template.md` | Feature-level plan with TC matrix                      |
| Summary             | `.agent/templates/summary-template.md`             | Teardown report with pipeline log                      |
| Lead Dispatch       | `.agent/templates/lead-dispatch.md`                | Orchestrator workflow                                  |
| Researcher Dispatch | `.agent/templates/researcher-dispatch.md`          | Code exploration workflow                              |
| Builder Dispatch    | `.agent/templates/builder-dispatch.md`             | POM/spec implementation                                |
| Reflector Dispatch  | `.agent/templates/reflector-dispatch.md`           | Self-critique workflow                                 |
| QA Dispatch         | `.agent/templates/qa-gatekeeper-dispatch.md`       | Test execution workflow                                |
| Reviewer Dispatch   | `.agent/templates/reviewer-dispatch.md`            | Code audit workflow                                    |

## Commands

| Command           | Agent                   | Purpose                                              |
| ----------------- | ----------------------- | ---------------------------------------------------- |
| `/triage`         | Lead                    | Phase 0: classify request → hotfix/mode-c/epic       |
| `/hotfix`         | Lead → Builder          | Level 1: fast-track single file fix (< 3 TCs)        |
| `/mode-c`         | Lead (orchestrator)     | Level 2: full Mode C pipeline (3-50 TCs)             |
| `/researcher-a`   | researcher-routes       | Routes & navigation discovery                        |
| `/researcher-b`   | researcher-components   | Components & selectors discovery                     |
| `/researcher-c`   | researcher-validators   | Validators & error states discovery                  |
| `/researcher-d`   | researcher-pom-patterns | POM patterns discovery in test framework             |
| `/builder-pom`    | builder-pom             | Create/update Page Object Model files                |
| `/builder-spec`   | builder-spec            | Create/update Playwright test specs                  |
| `/reflector-pom`  | reflector-pom           | Critique POM structure (selector priority, BasePage) |
| `/reflector-spec` | reflector-spec          | Critique spec quality (no timeouts, AAA pattern)     |
| `/qa-gatekeeper`  | qa-gatekeeper           | Run tests, apply flakiness protocol, verdict         |
| `/review`         | reviewer                | Full audit (Stage 1 compliance + Stage 2 quality)    |
| `/test`           | —                       | Run full test suite and generate report              |

## Conflict Prevention

| File                                   | Strategy             | Why                                     |
| -------------------------------------- | -------------------- | --------------------------------------- |
| `.agent/plans/todos/tc-*.md`           | Per-TC files         | One agent per TC = no concurrent writes |
| `.agent/memory/entities/{entity}.json` | Per-entity files     | One agent owns entity = no corruption   |
| `.agent/state.json`                    | Single writer (Lead) | Written once at teardown                |
| `.agent/tasks/{agent}-*.json`          | One file per agent   | Isolated outputs                        |

## Design Patterns

This project implements all 7 industry-standard agent patterns:

1. **Reflection** → `docs/personas/reflector.md`
2. **ReAct** → `docs/personas/researcher.md`
3. **Plan-and-Execute** → `docs/workflows/001-test-task-sop.md`
4. **Tool Use** → `.agent/mcp.json` + `.agent/settings.json`
5. **Multi-Agent Collaboration** → `docs/workflows/002-multi-agent-orchestration.md` Mode C
6. **Memory Management** → `.agent/memory/` + `skills/memory-management/SKILL.md`
7. **Human-in-the-Loop** → `docs/personas/qa-gatekeeper.md`

Read `docs/constitution/005-design-patterns.md` for full mapping.
