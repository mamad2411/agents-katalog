# 🤖 AGENTS

> **LOAD**: When delegating to agents | **PURPOSE**: Agent handling protocol

---

## TIERED EXECUTION (ORCA-FIRST)

> ⛔ **DEFAULT ASSUMPTION**: You are ALWAYS running inside Orca. Attempt TIER 0 first. Only fallback to lower tiers if the previous tier's commands fail.

### TIER 0: Orca Terminal ⭐ (DEFAULT — Always try first)

```yaml
assumption: "You ARE inside Orca. Always attempt orca commands first."

lifecycle:
  0. CHECK MODELS (Pre-Check):
     Run `agy --list-models` or `agy models` to verify available models.
  
  1. CREATE (Spawn):
     Use `orca terminal create --command "<cli_command>"` to spawn the worker.
     *For AGY*: `orca terminal create --command "agy --model {model_name} --dangerously-skip-permissions -i='[ROLE: WORKER] {task}'"` (MUST use -i, prepend [ROLE: WORKER]).
     *For Claude*: `orca terminal create --command "claude -p '{task}'"`
     *For Cline*: `orca terminal create --command "cline '{task}'"`
  
  2. WAIT (Sleep):
     orca terminal wait --terminal {term_id} --for tui-idle
  
  3. READ (Extract):
     orca terminal read --terminal {term_id}
  
  4. CLOSE (Cleanup):
     orca terminal close --terminal {term_id}

on_failure:
  - Log: "⚠️ TIER 0 FAILED: {error_message}"
  - Fallback to TIER 1 (invoke_subagent)
```

### TIER 1: Sub-agent (FALLBACK when TIER 0 fails)

```yaml
condition: TIER 0 (orca) command returned error or orca not available

1. Log: "⚠️ TIER 0 FAILED → Falling back to TIER 1 (invoke_subagent)"

2. Prepare handoff:
   include: requirements, task, acceptance criteria, constraints
   exclude: internal reasoning, failed attempts

3. Skills analysis: (output required)
   "🎯 Skills Analysis: {simple|complex} → {using X | skipping}"

4. Invoke: invoke_subagent(agent_name, context)

5. Verify: format matches, criteria met

6. On error: fallback to TIER 2, log reason
```

### TIER 2: EMBODY (Fallback only)

```yaml
permitted_when:
  - Tool Discovery found NO sub-agent tools
  - Sub-agent tool returned system error

forbidden_reasons:
  - Task seems "simple"
  - "Save tokens"
  - "Efficiency"

execution:
  1. Log: "⚠️ TIER 2: {reason}"
  2. READ agent file COMPLETELY
  3. EXTRACT: Directive, Protocol, Constraints, Format
  4. ANNOUNCE embodiment (see format below)
  5. EXECUTE as agent (follow THEIR protocol)
  6. EXIT embodiment, continue as orchestrator
```

**Embodiment Announcement Format**:
```markdown
📋 EMBODIED: `{agent}`
**Directive**: {core directive verbatim}
**Protocol**: {thinking protocol summary}
**Constraints**: {key constraints}
```

---

## TOOL DISCOVERY (First delegation only)

```markdown
## 🔍 Tool Discovery
| Check | Result |
|-------|--------|
| Orca terminal (TIER 0) | ✅ DEFAULT / ❌ Failed → fallback |
| Sub-agent tool (TIER 1) | ✅ / ❌ |
| Execution tier | TIER 0 / TIER 1 / TIER 2 |
```

**Cache**: Tool discovery result is cached for session. Do not re-check.

---

## CONTEXT MODEL COMPARISON

| Aspect | TIER 1: Sub-agent | TIER 2: EMBODY |
|--------|-------------------|----------------|
| Priority | ⭐ MANDATORY | 🔄 Fallback |
| Context | Fresh, isolated | Shared with parent |
| Quality | ✅ Optimal | ⚠️ Risk of pollution |
| Parallel | Yes | No (sequential) |
| Availability | Platform-dependent | Always available |

---

## COMPLETION GUARANTEE

```yaml
rule: "EVERY delegation request WILL be fulfilled"

mechanism:
  - TIER 1 is primary when available
  - TIER 2 is fallback when TIER 1 fails
  - EMBODY always works (read + transform)

result:
  - NO task is ever skipped
  - NO delegation ever fails completely
  - System is future-proof
```

---

## AGENT CATEGORIES

| Category | Agents | Purpose |
|----------|--------|---------|
| **meta** | tech-lead, planner, wiki-architect | Coordinate, plan — never implement |
| **execution** | backend-engineer, frontend-engineer, mobile-engineer, game-engineer, database-architect | Implementation |
| **validation** | tester, reviewer, security-engineer, performance-engineer, debugger, wiki-reviewer | QA |
| **research** | researcher, scouter, brainstormer, designer, wiki-extractor | Investigation |
| **support** | docs-manager, devops-engineer, business-analyst, project-manager, reporter | Support |

---

## 🧠 MODEL ASSIGNMENT — PER TASK TYPE

> ⛔ **BINDING**: Every subagent MUST be spawned with the correct model. No exceptions.

| Task Classification | Orca CLI Model ID (`--model` param) | `invoke_subagent` param | When to Use |
|--------------------|---------------------------------|-------------------------|-------------|
| **Planning** | `claude-opus-4-6-thinking` | `inherit` | Architecture, task breakdown, strategy, tech-lead decisions |
| **Light** | `gemini-3.8-flash-high` | `flash` | Research, scouting, file reading, simple lookups, docs reading |
| **Heavy** | `gemini-3.1-pro-high` | `pro` | Implementation, complex logic, refactoring, database design |
| **Review** | `cline` (via Orca) | N/A | Code review, quality checks — spawned directly via Orca CLI |

### Classification Heuristics
```yaml
LIGHT (→ flash):
  - Codebase exploration / structure analysis
  - Reading and summarizing documentation
  - Finding files, patterns, dependencies
  - Simple code lookups / searches
  - Writing reports / summaries

HEAVY (→ pro):
  - Writing new features (frontend/backend)
  - Complex refactoring
  - Database schema design
  - API implementation
  - Bug fixing requiring deep analysis
  - Performance optimization

PLANNING (→ inherit):
  - Architecture planning
  - Task decomposition
  - Technical strategy
  - Trade-off analysis
  - Project roadmap

REVIEW (→ Cline):
  - Code review
  - Security audit
  - Quality assessment
  - Best practices validation
```

---

## 📦 RESEARCH-SPECIFIC HANDOFF PATTERN

> Research is ALWAYS Phase 1. The Orchestrator NEVER explores the codebase directly.

### Handoff Structure for Research
```
./handoffs/{date}-{job}/
├── research.md          ← Research subagent writes findings here
├── orchestrator_main.md ← Orchestrator tracks progress
├── plan.md              ← Planner writes plan here (Phase 2)
├── frontend.md          ← Frontend worker reads/writes (Phase 3)
├── backend.md           ← Backend worker reads/writes (Phase 3)
└── cline-review.md      ← Review prompt for Cline (Phase 4)
```

### Research Handoff Template (research.md)
```markdown
# Research Handoff — {job_name}
**Date**: {date}
**Status**: PENDING | IN_PROGRESS | COMPLETED

## Task
{What the research subagent needs to investigate}

## Scope
- [ ] Project structure analysis
- [ ] Existing code patterns
- [ ] Available documentation
- [ ] Dependencies & tech stack
- [ ] Relevant ZAUI components (if UI)
- [ ] API patterns (if backend)

## Findings
{Subagent writes findings here}

## Recommendations
{Subagent writes recommendations here}
```

### Research Delegation Protocol
```yaml
1. Orchestrator creates: ./handoffs/{date}-{job}/research.md
   - Fills in Task and Scope sections
   - Sets Status: PENDING

2. Orchestrator spawns flash subagent:
   - Role: "Codebase Researcher"
   - Model: flash
   - Prompt: "[ROLE: WORKER] Read ./handoffs/{date}-{job}/research.md, 
     investigate the codebase, and write your findings back to that file.
     Also read .agents/rules/ZALO-MINI-APP.md for project rules."

3. Subagent executes:
   - Reads handoff → explores codebase → writes Findings + Recommendations
   - Sets Status: COMPLETED

4. Orchestrator reads research.md:
   - Analyzes findings
   - Proceeds to Phase 2 (Planning)
```

## 🔺 AGENT TEAMS — GOLDEN TRIANGLE (`:team` variant only)

> **LOAD**: `TEAMS.md` for full Golden Triangle protocol and debate mechanism.
> Teams spawn exactly **3 agents per phase**: Tech Lead + Executor + Reviewer.
> Adversarial collaboration produces higher quality than parallel cooperation.

### Golden Triangle Roster

| Domain | Tech Lead | Executor | Reviewer | Use When |
|--------|-----------|----------|----------|----------|
| `backend-team` | `tech-lead` | `backend-engineer` | `reviewer` | APIs, server logic, backend features |
| `frontend-team` | `tech-lead` | `frontend-engineer` | `reviewer` | UI components, client-side features |
| `fullstack-team` | `tech-lead` | `backend-engineer` + `frontend-engineer` | `reviewer` | End-to-end features |
| `database-team` | `tech-lead` | `database-architect` | `reviewer` + security lens | Schema design, migrations, queries |
| `research-team` | `researcher` | `scouter` | `brainstormer` (Devil's Advocate) | Discovery, codebase analysis, patterns |
| `planning-team` | `planner` | `researcher` | `tech-lead` (feasibility critic) | Architecture planning, task decomposition |
| `qa-team` | `tester` | `tester` (self-implements) | `security-engineer` + `performance-engineer` | Test strategy, coverage, quality |
| `design-team` | `designer` | `frontend-engineer` | `reviewer` + UX/a11y lens | UI/UX design, component specs |
| `debug-team` | `debugger` | `backend-engineer` | `reviewer` (root-cause validator) | Root cause analysis, issue resolution |
| `devops-team` | `devops-engineer` | `backend-engineer` | `security-engineer` | CI/CD, infrastructure, deployment |
| `security-team` | `security-engineer` | `backend-engineer` | `reviewer` (pen-test mindset) | Security assessment, vulnerability audit |
| `game-team` | `tech-lead` | `game-engineer` | `reviewer` (game arch + 60fps) | Game development, engines, physics, ECS |
| `mobile-team` | `tech-lead` | `mobile-engineer` | `reviewer` (UX + platform) | iOS, Android, React Native, Flutter |
| `performance-team` | `performance-engineer` | `backend-engineer` | `reviewer` (measurement + regression) | Profiling, optimization, load testing |
| `docs-team` | `docs-manager` | `researcher` | `reviewer` (accuracy + completeness) | Technical writing, API docs, architecture docs |
| `project-team` | `project-manager` | `business-analyst` | `tech-lead` (feasibility critic) | Project planning, risk, delivery |
| `report-team` | `reporter` | `scouter` | `reviewer` (data accuracy + insight) | Status reports, metrics, analytics |
| `wiki-team` | `wiki-architect` | `wiki-extractor` | `wiki-reviewer` | Wiki generation, entity extraction, documentation quality |

### Golden Triangle vs Single Agent

| When | Use |
|------|-----|
| Standard `:fast`, `:hard` variants | Single agent per phase |
| `:team` variant | Golden Triangle per phase |
| User explicitly requests team review/collaboration | `:team` variant |
| Maximum quality with adversarial debate is priority | `:team` variant |

### Golden Triangle Definitions Location

```
agents/teams/{team-name}/
├── techlead.md    # Coordinator, decomposer, arbitrator
├── executor.md    # Builder, implementer, defender
└── reviewer.md    # Devil's advocate, quality gatekeeper

# Wiki Team definitions:
agents/teams/wiki-team/
├── techlead.md    # Wiki Architect role — decomposes, coordinates, arbitrates
├── executor.md    # Wiki Extractor role — extracts, writes, defends
└── reviewer.md    # Wiki Reviewer role — validates accuracy, completeness, coverage
```

### Communication Protocol

- **Shared Task List**: Published by Tech Lead at phase start, tracks task status
- **Mailbox**: `./.reports/{topic}/MAILBOX-{date}.md` — append-only log of all exchanges
- **Debate**: Max 3 rounds per task → Tech Lead arbitrates
- **Consensus**: `✅ CONSENSUS: TechLead ✓ | Executor ✓ | Reviewer ✓` required to release output

---

## TASK → AGENT MAPPING

| Task | Agent |
|------|-------|
| API, backend logic | `backend-engineer` |
| UI, components | `frontend-engineer` |
| Database schema | `database-architect` |
| Security | `security-engineer` |
| Testing | `tester` |
| Code review | `reviewer` |
| Debugging | `debugger` |
| Planning | `planner` |
| Research | `researcher` |
| Codebase analysis | `scouter` |
| Documentation | `docs-manager` |
| Deployment | `devops-engineer` |
| Reports | `reporter` |
| Project management | `project-manager` |
| Business analysis | `business-analyst` |
| Design | `designer` |
| Brainstorming | `brainstormer` |
| Game development | `game-engineer` |
| Mobile development | `mobile-engineer` |
| Technical leadership | `tech-lead` |
| Wiki generation | `wiki-architect`, `wiki-extractor`, `wiki-reviewer` |

---

## CONTEXT ISOLATION (Distributed Handoffs)

```
ORCHESTRATOR'S JOB:
  1. Analyze user requirements.
  2. Write high-level plan and task assignments to `./handoffs/{date}-{job}/orchestrator_main.md`.
  3. Prepare domain-specific handoffs (e.g., `./handoffs/{date}-{job}/backend.md`).
  4. Spawn the worker and instruct them ONLY to read their specific handoff file.

WORKER'S JOB:
  1. Read only the specific handoff file assigned to them. (They only need to know enough to do their job, no more).
  2. Do not read the entire codebase or master handoff unless explicitly instructed.
  3. Execute the task.
  4. Write the results, progress, and any blocker back to THEIR specific handoff file.

DELIVERABLE FORMAT:
  Always organize handoffs by date and job progress:
  - Good: `./handoffs/2023-10-27-auth-feature/frontend.md`
  - Bad: `./handoffs/all-context.md` (Do not merge context)
```

---

## RECURSIVE DELEGATION

```
IF agent.category == "meta" OR agent.handoffs.length > 0:
  → This is a MANAGER agent
  → MUST delegate to specialists
  → NEVER implement directly
```

---

## ANTI-LAZY FALLBACK DETECTION

```yaml
detection:
  - Choosing TIER 1 (invoke_subagent) without attempting TIER 0 (orca) first
  - Choosing TIER 2 without attempting TIER 0 and TIER 1
  - Justifying EMBODY with "task is simple"
  - Mentioning "efficiency" or "faster" when skipping TIER 0
  - Using invoke_subagent without logging TIER 0 failure first

correction:
  1. STOP
  2. Log: "⚠️ LAZY FALLBACK DETECTED — Skipped TIER 0 (Orca)"
  3. Attempt TIER 0 (orca terminal create) first
  4. Only use TIER 1 if TIER 0 actually fails (log the error)
  5. Only use TIER 2 if TIER 1 actually fails (log the error)

strict_rules:
  ❌ NEVER skip TIER 0 (orca) without attempting it first
  ❌ NEVER assess task as "too simple" for orca
  ❌ NEVER prioritize tokens over context isolation
  ❌ NEVER use invoke_subagent as first choice
  ✅ ALWAYS attempt orca terminal create FIRST
  ✅ ALWAYS log TIER 0 failure before falling back
  ✅ ALWAYS log TIER 1 failure before EMBODY
```
## ?? ORCA MULTI-TERMINAL ORCHESTRATION (CLI-AGNOSTIC)

When running inside the Orca environment, the Orchestrator MUST use the Multi-Terminal Delegation pattern to spawn workers. This avoids quota-burn and completely bypasses framework limitations.

### Supported CLI Runners
The Orchestrator is NOT locked to Antigravity (gy). You can spawn ANY agent CLI based on the task:
- gy (Antigravity): Default for structured tasks using the 24 built-in roles.
- claude (Claude Code): Excellent for general codebase exploration.
- cline: For deeply autonomous engineering tasks.
- codex / hermes / omp: For specialized environments or local models.

### The 24 Built-in Antigravity Roles (For gy --agent <role>)
**Engineering**: ackend-engineer, rontend-engineer, database-architect, devops-engineer, game-engineer, mobile-engineer
**Planning**: rainstormer, usiness-analyst, planner, project-manager, scouter, 	ech-lead
**QA & Debug**: debugger, 	ester, eviewer, performance-engineer, security-engineer
**Docs & Research**: docs-manager, eporter, esearcher, designer, wiki-architect, wiki-extractor, wiki-reviewer

### The 5-Step Orchestration Lifecycle
To prevent infinite loops ("Inception") and resource leaks (infinite terminals), every delegation MUST strictly follow this lifecycle:

0. **CHECK MODELS (Pre-Check)**:
   Run a command (e.g. `agy --list-models` or `agy models`) to verify which models are currently available and active. Use this information to assign the most appropriate model to the worker.

1. **CREATE (Spawn)**:
   Use orca terminal create to spawn the worker. 
   *CRITICAL*: Do NOT use the `-p` (print) flag because it runs in headless mode and hides the agent's progress. Instead, ALWAYS use the `-i` (interactive) flag for `orca terminal create`. 
   For `agy`, provide `--model {model_name}` and `--dangerously-skip-permissions`, and prepend `[ROLE: WORKER]` in the `-i` prompt to trigger the role switch.
   *Example (Antigravity)*: `orca terminal create --command "agy --model gemini-3.1-pro-high --dangerously-skip-permissions -i='[ROLE: WORKER] Check docker-compose.yml'"`
   *Example (Claude Code)*: `orca terminal create --command "claude -p 'Check docker-compose.yml'"`
   *Example (Cline)*: `orca terminal create --command "cline 'Check docker-compose.yml'"`
   *(Note the returned terminal ID, e.g., term_123)*

2. **WAIT (Sleep)**:
   Wait for the worker to finish the task.
   *Example*: orca terminal wait --terminal term_123 --for tui-idle

3. **READ (Extract)**:
   Scrape the output of the terminal to get the worker's answer.
   *Example*: orca terminal read --terminal term_123

4. **CLOSE (Cleanup)**:
   Kill the terminal pane to prevent infinite visual clutter.
   *Example*: orca terminal close --terminal term_123

