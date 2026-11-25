<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: task-analyzer
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - WebSearch
description: >
  Autonomously analyzes and executes tasks with a structured plan. Triggers on
  "분석해", "작업 계획", "이거 해줘", "자동으로 처리해", "계획 세워", "workflow 만들어",
  "analyze", "task plan", "do this", "handle automatically", "make a plan",
  "create a workflow", "break this down", "execute", "run this task" and similar
  requests. Decomposes complex tasks into subtasks, identifies required tools,
  delegates to sub-agents, collects results, and reports. The core autonomous
  execution engine of OpenClaw-CC.
---

# Task Analyzer — Autonomous Task Analysis & Execution Engine

## Preamble

Before executing this skill:

1. **Load context from memory**:
   ```
   memory_search(query: "{skill-relevant-query}", associative: true, limit: 5)
   memory_search(tag: "{skill-name}", limit: 3)
   ```
   Review returned memories for relevant past context, decisions, and patterns.

2. **Check OMC state for active work**:
   ```
   state_get_status()
   ```
   If conflicting active tasks exist, warn the user before proceeding.

3. **Detect current branch** (for git-related skills):
   ```bash
   git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "not-a-git-repo"
   ```

4. **Check proactive mode**:
   ```
   state_read("occ-proactive")
   ```
   If `"false"`: do NOT proactively suggest other OpenClaw-CC skills during this session.
   Only run skills the user explicitly invokes.

5. **Log skill activation**:
   ```
   memory_daily_log(type: "note", entry: "Skill activated: /{skill-name}")
   ```

## Role

Analyze user requests, transform them into executable plans, and autonomously
execute using available tools (MCP servers, sub-agents, file system).
Before starting any task, check related context with `memory_search`.
After completion, persist results with `memory_store`.

## Memory Context Loading

Before starting work, load relevant context from the 3-layer memory system:

```
# Search for related past work
memory_search(query: "{task description}", associative: true, limit: 5)

# Search by relevant tags
memory_search(tag: "{relevant-tag}", limit: 3)

# Check for recent related daily logs
memory_search_date(start: "{7 days ago}", end: "{today}", category: "daily-logs", limit: 5)
```

**Use retrieved context to**:
- Avoid repeating past mistakes
- Build on previous decisions
- Maintain consistency with established patterns
- Reference related knowledge graph nodes

If critical related memories exist, summarize them before proceeding:
```
Found {N} related memories:
- {memory_1 title}: {brief relevance}
- {memory_2 title}: {brief relevance}
```

## 5-Phase Process

### Phase 1 — Understanding the Request

Analyze the user request along 4 axes:

| Axis | Question | Example |
|------|----------|---------|
| **What** (intent) | What is the goal? | "Understand competitor landscape" |
| **Done when** (success criteria) | What state signals completion? | "Report with comparison table finished" |
| **With what** (resources) | What tools/data are needed? | "Web search, existing competitor data from memory" |
| **Constraints** | Are there time/scope/format limits? | "English, max 3 pages" |

Ask the user a clarifying question for ambiguous requests. Proceed directly to Phase 2 for clear requests.

### Phase 2 — Task Decomposition

Decompose complex tasks into an atomic subtask tree.

```
[Task] Write competitor analysis report
├── [Context]  memory_search("competitor") → check existing data
├── [Collect]  Research competitor A latest news → web_search
├── [Collect]  Research competitor B latest news → web_search (∥ parallel)
├── [Analyze]  Strength/weakness comparison matrix → reasoning
├── [Generate] Draft report → file creation
├── [Store]    memory_store(category:"projects", tags:["competitor","analysis"])
└── [Notify]   messenger_send(platform:"telegram", message:"Report complete")
```

For 12 decomposition patterns, see `references/decomposition-patterns.md`.

### Phase 3 — Execution Strategy Selection

| Strategy | Condition | Example |
|----------|-----------|---------|
| **Sequential** | Subtasks have ordering dependencies | Research → Analyze → Write |
| **Parallel** | Independent subtasks (delegate to sub-agents) | Research A ∥ Research B ∥ Research C |
| **Hybrid** | Parallel collection → sequential analysis → parallel output | Most composite tasks |
| **OMC Team** | Complex multi-file work (3+ files, cross-cutting) | TeamCreate → team-plan → team-exec → team-verify |

Delegation criteria: subtask is independent, has 3+ steps, and its result is not immediately needed by another task.

### OMC Multi-Agent Delegation (v3)

Route subtasks to specialized OMC agents based on type:

| Subtask Type | OMC Agent | Model | Delegation Method |
|-------------|-----------|-------|-------------------|
| Code implementation | `executor` | sonnet | `Agent(subagent_type: "oh-my-claudecode:executor")` |
| Architecture decision | `architect` | opus | `Agent(subagent_type: "oh-my-claudecode:architect")` |
| Bug investigation | `debugger` | sonnet | `Agent(subagent_type: "oh-my-claudecode:debugger")` |
| Web research | `research-agent` | sonnet | Project-local agent |
| Code review | `code-reviewer` | opus | `Agent(subagent_type: "oh-my-claudecode:code-reviewer")` |
| Test writing | `test-engineer` | sonnet | `Agent(subagent_type: "oh-my-claudecode:test-engineer")` |
| Memory operations | `memory-specialist` | sonnet | Project-local agent |
| Notifications | `comms-agent` | haiku | Project-local agent |

**For complex tasks (5+ subtasks):** Create an OMC team pipeline:
```
1. TeamCreate(name: "{task}", members: [executor, verifier])
2. SendMessage(to: executor, prompt: "{subtask}")
3. Wait for results
4. SendMessage(to: verifier, prompt: "verify {results}")
5. If verified: collect results
6. If failed: SendMessage(to: executor, prompt: "fix {issues}")
```

**Memory integration:** Every agent delegation includes:
- Pre: `memory_search(associative: true)` — inject context into agent prompt
- Post: `memory_store` — persist agent deliverables

### Phase 4 — Execution & Monitoring

After executing each subtask, determine its status:

- **Success** → Collect result and proceed to next task
- **Partial success** → Save what was obtained, note missing parts and continue
- **Failure** → Try an alternative strategy (up to 2 retries). Report to user if all alternatives fail

Log important information discovered during execution immediately with `memory_daily_log`.

### Phase 5 — Result Collection & Reporting

1. Integrate all subtask results
2. Persist key deliverables with `memory_store`
3. Record execution log with `memory_daily_log(type:"done")`
4. Notify user via `messenger_send` if needed
5. Deliver final report using the output format below

## Memory Persistence

After completing the workflow, persist results to the 3-layer memory system:

### Required Actions

1. **Log completion to daily log**:
   ```
   memory_daily_log(type: "done", entry: "{skill-name}: {brief result summary}")
   ```

2. **Store significant findings** (importance ≥ 6):
   ```
   memory_store(
     category: "{appropriate category}",
     title: "{descriptive title}",
     content: "{structured result content}",
     tags: ["{skill-name}", "{project}", "{relevant-tags}"],
     importance: {6-10 based on significance}
   )
   ```

3. **Link to related memories** (if applicable):
   ```
   memory_link(source: "{new_memory_id}", target: "{related_id}", relation: "{related|derived|refines}")
   ```

### Category Routing

| Content Type | Category | Subcategory |
|-------------|----------|-------------|
| Bug fix / debugging | knowledge | debugging |
| Code review results | projects | {project-name} |
| Design decisions | projects | {project-name} |
| Research findings | knowledge | {topic} |
| Release / deploy | projects | {project-name} |
| Person-related info | people | — |
| Task / action item | tasks | — |

## Messenger Notification

Send notifications for significant events via messenger:

### When to Notify

| Event | Platform | Priority |
|-------|----------|----------|
| Task/pipeline completed | telegram | Normal |
| Verification failed | telegram | High |
| Long-running task done (10+ min) | telegram | Normal |
| Critical error or blocker | telegram | High |
| PR created / release shipped | all | Normal |
| Importance ≥ 8 memory created | telegram | Normal |

### Notification Format

```
messenger_send(
  platform: "telegram",
  message: "[{skill-name}] {status_emoji} {brief description}\n\n{details if relevant}"
)
```

**Status Emojis**:
- Completed successfully: ✅
- Completed with warnings: ⚠️
- Failed / blocked: ❌
- Needs attention: 🔔

### Do NOT Notify

- Routine memory operations
- Intermediate progress steps
- Read-only operations (search, list, status)

## Available Tool Mapping Table

| Task Type | MCP Tool | Notes |
|-----------|----------|-------|
| Retrieve past context | `memory_search`, `memory_get` | Always call first at task start |
| Persist information | `memory_store`, `memory_update` | Save deliverables and insights |
| Record execution log | `memory_daily_log` | type: note/decision/todo/done |
| Check memory status | `memory_stats`, `memory_list` | Inspect storage state |
| Delete memory | `memory_delete` | Clean up duplicates and stale data |
| Web research | `web_search`, `web_fetch` | Collect external information |
| External notifications | `messenger_send` | platform: discord/telegram/all |
| Read messenger | `messenger_read`, `messenger_poll` | Check user messages |
| Messenger status | `messenger_status` | Platform connection status |
| Register scheduled task | `task_create`, `task_update` | Include cron expression |
| Query scheduled tasks | `task_list`, `task_history` | Review existing tasks |
| Run/delete scheduled task | `task_run_now`, `task_delete` | Immediate run or delete |
| Generate crontab | `task_generate_crontab` | Output system crontab file |
| Create/edit files | Built-in file tools | Reports, documents |
| Execute code/commands | `bash` | Prefer delegating to sub-agent |

For detailed routing, see `references/tool-routing-matrix.md`.

## Execution Principles

1. **Least privilege** — Use only the tools required. Use `bash` only when file tools cannot do the job.
2. **Failure recovery** — If one step fails, continue with independent remaining steps.
3. **Transparency** — Report the current phase to the user when entering each Phase.
4. **Memory leverage** — At task start, query `memory_search` for similar past tasks and use them as reference.
5. **Cost efficiency** — Use sub-agents only for independent, complex subtasks.

## Output Format

Report using the template below after task completion:

```markdown
## Task Completion Report

**Request**: [One-line summary of the original request]
**Status**: Completed / Partially completed / Failed

### Execution Steps
1. [Step name] — Completed: [Result summary]
2. [Step name] — Completed: [Result summary]
3. [Step name] — Partially completed: [Reason]

### Key Deliverables
- [List of generated files, data, insights]

### Memory Stored
- [Saved items with category/tags]

### Suggested Next Steps (if applicable)
- [Follow-up action suggestions]
```

## Reference Documents

- 12 task decomposition patterns: `references/decomposition-patterns.md`
- Task-to-tool routing matrix: `references/tool-routing-matrix.md`
- 3 complex task execution examples: `examples/complex-task-example.md`

## Completion Status Protocol

Every skill must end with one of these status codes:

| Code | Meaning | When to Use |
|------|---------|-------------|
| **DONE** | All steps completed, evidence provided | Root cause found + fix verified, PR created, review finished |
| **DONE_WITH_CONCERNS** | Completed with warnings or caveats | Tests pass but coverage dropped, fix applied but can't fully verify |
| **BLOCKED** | Cannot proceed, requires user intervention | 3 failed attempts, missing permissions, external dependency down |
| **NEEDS_CONTEXT** | Missing information to continue | Unclear requirements, need user clarification |

### Escalation Rules

1. **3-strike rule**: After 3 failed attempts at any step, **STOP** and escalate to user.
   Do not continue guessing. Present what was tried and ask for direction.

2. **Scope escalation**: If fix/change touches 5+ files unexpectedly, pause and confirm
   with the user before proceeding.

3. **Security uncertainty**: If you are unsure about a security implication, **STOP** and
   escalate. Never guess on security.

4. **Verification requirement**: Never claim DONE without evidence.
   - "Should work" → RUN IT. Confidence is not evidence.
   - "Already tested earlier" → Code changed since. Test again.
   - "Trivial change" → Trivial changes break production.

### Output Format

```
═══════════════════════════════════════
Status: {DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT}
Summary: {one-line description of outcome}
Evidence: {test output, verification results, or blocking reason}
═══════════════════════════════════════
```
