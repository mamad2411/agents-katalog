---
name: team
description: "Spawn an agent team for complex multi-part tasks"
category: workflow
tags: [multi-agent, parallel, coordination, team-lead]
depends-on: [init]
input: "complex task description"
output: ".ccs/team-board.md + coordinated multi-agent results"
token-estimate: 8000
parallel-safe: false
argument-hint: "[task description]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-opus-4-6
context: fork
agent: general-purpose
---

# Team

Coordinate a multi-agent team for tasks that span multiple domains. You are the **team lead** — break work down, assign roles, dispatch agents in parallel, then integrate results.

## Steps

### 1. Load context
- Read `.ccs/architecture.md` → tech stack, patterns, entry points
- Read `.ccs/file-index.md` → S/A-rank files by domain
- Read `.ccs/conventions.md` → code style, test patterns
- Read `.ccs/task.md` → prior work and current state

### 2. Analyze task
- Identify domains involved (backend, frontend, data, infra, test, docs)
- Estimate complexity: how many parallel streams make sense (2-4)
- Identify shared interfaces — contracts agents must agree on before coding
- List dependencies between streams (what must finish before what)

### 3. Design the team
Decide roles based on the task. Common compositions:

| Pattern | Roles | When |
|---------|-------|------|
| Full-stack feature | Backend + Frontend + Test | Multi-layer feature |
| Refactor | Analyzer + Implementer + Verifier | Large refactors |
| Research + Build | Researcher + Builder | Unknown domain |
| API + Docs | Backend + Docs + Test | API endpoints |

### 4. Create team board
Write `.ccs/team-board.md` using template at `.claude/skills/_ccs/templates/team-board-template.md`:
- List team roles and focus areas
- Break the task into numbered subtasks (T1, T2, T3...)
- Assign each subtask to a role
- Document shared interfaces and contracts upfront
- Log architecture decisions

### 5. Early alignment
Before dispatching agents, resolve interface questions:
- What data structures are shared?
- What API contracts must both sides agree on?
- What file boundaries prevent merge conflicts?
Log decisions in the team board's Decisions section.

### 6. Dispatch agents in parallel
Use the **Task tool** to spawn agents simultaneously. Each agent gets:
- Its role and focus area
- The specific subtask(s) assigned
- Relevant file paths from `.ccs/file-index.md`
- Conventions from `.ccs/conventions.md`
- Interface contracts from the team board
- Instructions to write to specific files (no overlapping writes)

Spawn agents with `subagent_type: general-purpose` and model `sonnet` for implementation, `haiku` for scanning/docs.

### 7. Integrate results
After all agents complete:
- Read each agent's output
- Check for conflicts (same file modified, inconsistent interfaces)
- Resolve conflicts — the lead decides
- Verify consistency across boundaries
- Run tests if applicable (suggest `/ccs-test`)

### 8. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`:
- Type: `team`
- List every file read/modified/created with agent attribution
- Summarize team composition and task breakdown
- Note any conflicts resolved
- Log total agent count and model usage

### 9. Update team board
Mark all tasks as done in `.ccs/team-board.md`. Add integration log entry.

## Rules
- **Max 4 agents** — more creates coordination overhead that exceeds benefit
- **No overlapping writes** — assign distinct file ownership to each agent
- **Contracts first** — interfaces agreed before any implementation
- **Lead resolves all conflicts** — agents don't negotiate with each other
- **Read-only shared context** — agents read `.ccs/` files but only the lead writes to them
- **Suggest next step** — after team completes, suggest `/ccs-test` or `/ccs-review`

## When NOT to use teams
- Single-file changes → use `/ccs-build`
- Bug fixes → use `/ccs-fix`
- Simple refactors → use `/ccs-refactor`
- Tasks under 3 files → overkill, use single-agent skills

## Refs
- Team board: `.ccs/team-board.md`
- Architecture: `.ccs/architecture.md`
- File index: `.ccs/file-index.md`
- Conventions: `.ccs/conventions.md`
- Task log: `.ccs/task.md`
- Agent guide: `.claude/skills/_ccs/agents/team-lead.md`
- Strategy: `.claude/skills/_ccs/references/context-strategies.md`

---
*codebase-context-skill v2.0.0*
