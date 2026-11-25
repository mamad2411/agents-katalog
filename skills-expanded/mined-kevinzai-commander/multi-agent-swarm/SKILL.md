---
name: multi-agent-swarm
description: "Advanced multi-agent orchestration — swarm patterns, agent specialization, shared state, consensus, and supervision trees"
version: 1.0.0
category: ai-tools
---

# Multi-Agent Swarm Orchestration

Advanced patterns for coordinating multiple Claude Code agents working on the same codebase or problem.

## Swarm Patterns

### 1. Fan-Out / Fan-In (Parallel Decomposition)

Best for: Independent subtasks that can be merged.

```
Orchestrator
├── Agent A → Task 1 → Result A
├── Agent B → Task 2 → Result B
├── Agent C → Task 3 → Result C
└── Merge Results → Final Output
```

**Implementation:**
```markdown
## Orchestrator Instructions

1. Decompose the task into N independent subtasks
2. For each subtask, spawn an agent using the Agent tool:
   - Give each agent a SPECIFIC, ISOLATED task
   - Each agent works on DIFFERENT files (no conflicts)
   - Set clear output format expectations
3. Collect all results
4. Merge, resolve conflicts, verify consistency
5. Run integration tests on the merged result
```

### 2. Pipeline (Sequential Specialization)

Best for: Tasks with natural ordering (design → implement → test → review).

```
Agent A (Architect) → spec.md
  → Agent B (Builder) → implementation
    → Agent C (Tester) → tests
      → Agent D (Reviewer) → review
```

**Key rule:** Each agent reads the previous agent's output, never the raw task.

### 3. Competitive (Best-of-N)

Best for: Important decisions where you want diverse perspectives.

```
Orchestrator → same prompt to 3 agents
├── Agent A (Conservative approach) → Solution A
├── Agent B (Aggressive approach) → Solution B
├── Agent C (Novel approach) → Solution C
└── Referee Agent → evaluates all 3 → picks winner
```

**Implementation with dialectic-review skill:**
- FOR agent argues for approach A
- AGAINST agent argues for approach B
- Referee evaluates evidence, picks the stronger approach

### 4. Supervision Tree

Best for: Long-running autonomous work with error recovery.

```
Supervisor
├── Worker A (file group 1)
│   ├── on_error → retry 3x, then escalate
│   └── on_timeout → kill and redistribute
├── Worker B (file group 2)
│   └── ...
└── Monitor
    ├── Progress tracking
    ├── Conflict detection
    └── Quality gates
```

## Agent Specialization Roles

| Role | Prompt Focus | Tools | Model |
|------|-------------|-------|-------|
| Architect | System design, interface contracts | Read, Grep, Glob | Opus |
| Builder | Implementation, coding | Read, Write, Edit, Bash | Sonnet |
| Tester | Test writing, verification | Read, Write, Bash | Sonnet |
| Reviewer | Code review, quality | Read, Grep | Opus |
| Researcher | Web search, documentation | WebSearch, WebFetch, Read | Haiku |
| Debugger | Bug investigation, root cause | Read, Grep, Bash | Sonnet |

## Shared State Management

### File-Based Coordination

```markdown
## Convention: Use a shared state file

Create `tasks/swarm-state.json`:
{
  "status": "in_progress",
  "agents": {
    "agent-1": { "task": "auth module", "status": "done", "files": ["src/auth/*"] },
    "agent-2": { "task": "API routes", "status": "working", "files": ["src/routes/*"] }
  },
  "conflicts": [],
  "completed": ["auth module"],
  "remaining": ["API routes", "tests", "docs"]
}

Each agent reads this file before starting. The orchestrator updates it after each agent completes.
```

### Git Branch Coordination

```markdown
## Convention: Branch-per-agent

1. Main branch: `feature/main-task`
2. Agent branches: `feature/main-task/agent-1-auth`, `feature/main-task/agent-2-api`
3. Each agent works on its own branch
4. Orchestrator merges branches sequentially, resolving conflicts
5. Final PR from `feature/main-task` to main
```

### Worktree Isolation

```markdown
## Convention: Git worktrees for true isolation

Each agent runs in its own worktree (isolated copy of the repo):
- Agent A: /tmp/worktree-agent-a/
- Agent B: /tmp/worktree-agent-b/

No file conflicts possible. Merge via git after all agents complete.
Use the `isolation: "worktree"` parameter on the Agent tool.
```

## Communication Protocol

### Using claude-peers MCP

If `claude-peers` MCP is available, agents can message each other:

```markdown
## Agent Communication Rules

1. Use `set_summary` at start to describe your current task
2. Use `list_peers` to discover other active agents
3. Use `send_message` to:
   - Request information from another agent
   - Report completion of a dependency
   - Flag a conflict or blocker
4. Use `check_messages` periodically for incoming requests
5. RESPOND IMMEDIATELY to incoming messages (don't queue them)
```

### Without claude-peers (File-Based)

```markdown
## File-Based Communication

Agents communicate via files in `tasks/swarm/`:
- `tasks/swarm/agent-1-status.md` — each agent writes its own status
- `tasks/swarm/messages.jsonl` — append-only message log
- `tasks/swarm/blockers.md` — agents flag blockers here
- Orchestrator reads all files to coordinate
```

## Quality Gates

Before merging any agent's output:

1. **Compilation check** — `npx tsc --noEmit` passes
2. **Test check** — existing tests still pass
3. **Conflict check** — no merge conflicts with other agents' work
4. **Style check** — consistent with codebase conventions
5. **Scope check** — agent didn't modify files outside its assignment

## Anti-Patterns

1. **Shared file editing** — Never assign two agents to the same file
2. **Context bleeding** — Each agent starts fresh; don't assume shared context
3. **Unbounded agents** — Always set max-turns or time limits on autonomous agents
4. **Missing integration** — Always have a merge/integration step after parallel work
5. **No supervision** — Long-running agents need progress monitoring and kill switches
