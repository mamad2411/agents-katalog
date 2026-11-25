---
name: prd-task-loop
description: "Autonomous PRD-driven development loop inspired by Ralphy. Reads a PRD/task list, loops through tasks using AI coding agents (OpenCode, Claude Code, Codex) or Hermes subagents, auto-commits, and marks tasks complete. Supports parallel execution, dependency graphs, dry-run, and subagent orchestration."
version: 2.0.0
author: Hermes Agent (inspired by Ralphy by michaelshimeles)
license: MIT
metadata:
  hermes:
    tags: [prd, task-loop, autonomous, opencode, coding-agent, parallel, subagent]
    related_skills: [opencode, claude-code, codex, writing-plans, kiro-spec-tasks, subagent-driven-development]
---

# PRD Task Loop

Autonomous development loop: read a PRD → execute tasks via AI agents/subagents → auto-commit → mark complete → repeat.

## When to Use

- User has a PRD/task list and wants autonomous execution
- User says "run all tasks" or "implement the PRD"
- User wants parallel subagent-based task execution
- User wants to compare AI coding agents on the same task list
- User wants dependency-aware task scheduling

## Task Sources

### Markdown PRD (default)
```markdown
## Features
- [ ] Create user model [priority:high]
- [ ] Add auth endpoints [depends:user-model]
- [x] Setup project (done)
```

### YAML Tasks (recommended for complex projects)
```yaml
tasks:
  - id: setup-db
    title: Setup database schema
    priority: high
    tags: [backend, db]
    engine: opencode
    model: openrouter/anthropic/claude-sonnet-4

  - id: user-model
    title: Create user model
    depends: [setup-db]
    priority: high
    parallel_group: 1

  - id: auth-endpoints
    title: Add auth endpoints
    depends: [user-model]
    parallel_group: 2
```

### Inline Task (single task, no file)
Just describe the task directly in conversation.

## Core Loop (Sequential)

1. Parse PRD → get next incomplete task (respect dependencies)
2. Build prompt with task + project context + rules
3. Run AI agent (opencode/claude/codex/subagent) with the prompt
4. Verify: files changed, tests pass (if applicable)
5. Mark task complete in PRD (`- [ ]` → `- [x]`)
6. Git commit with descriptive message
7. Repeat until all tasks done

## Execution Modes

### Mode 1: Subagent Execution (Recommended for Hermes)

Uses `delegate_task` to spawn subagents. Each subagent gets full tool access.

```python
from hermes_tools import terminal, write_file, read_file

# Sequential: one subagent per task
result = delegate_task(
    goal="Implement the following task in the project at ~/my-project:\n\nCreate a user model with email, password, and created_at fields using Prisma ORM.",
    context="Project: Next.js + Prisma + SQLite. Follow existing code patterns in prisma/schema.prisma.",
    toolsets=["terminal", "file"]
)
```

**Parallel execution with subagents:**

```python
results = delegate_task(
    tasks=[
        {
            "goal": "Create utils.js with add, subtract, multiply functions",
            "context": "Project at ~/my-project. Use ES modules.",
            "toolsets": ["terminal", "file"]
        },
        {
            "goal": "Create types.ts with User, Post, Comment interfaces",
            "context": "Project at ~/my-project. Strict TypeScript.",
            "toolsets": ["terminal", "file"]
        },
        {
            "goal": "Setup jest config and write a sample test",
            "context": "Project at ~/my-project.",
            "toolsets": ["terminal", "file"]
        }
    ]
)
```

### Mode 2: Engine Execution (Direct CLI)

Calls AI coding CLIs directly via terminal. Good for faster, simpler tasks.

```bash
opencode run '<prompt>' --format json
claude --dangerously-skip-permissions -p '<prompt>'
codex exec --full-auto --json '<prompt>'
```

### Mode Comparison

| Aspect | Subagent Mode | Engine Mode |
|--------|--------------|-------------|
| Tool access | Full (file, terminal, web, browser) | Terminal only |
| Context window | Isolated per task | Shared with parent |
| Parallelism | Built-in `delegate_task(tasks=[...])` | Manual background processes |
| Reasoning | LLM-driven, adaptive | Script-driven, predictable |
| Cost | Higher (each subagent = LLM call) | Lower (CLI agent is cheaper) |
| Best for | Complex tasks, multi-file changes | Simple tasks, known patterns |

## Parallel Execution Strategies

### Strategy A: Subagent Parallel (Hermes Native)

Best for complex tasks that need reasoning.

```python
# 1. Parse PRD, group tasks by parallel_group
# 2. Execute groups sequentially, tasks within group in parallel
for group_num in sorted(groups):
    results = delegate_task(tasks=[build_subagent_task(t) for t in groups[group_num]])
    for task, result in zip(groups[group_num], results):
        # 3. Mark complete, commit
        pass
```

### Strategy B: Worktree Parallel (Git Isolation)

Best when tasks modify overlapping files.

```python
# 1. Create isolated worktrees
terminal(command="git worktree add /tmp/prd-agent-1 feature-1")
terminal(command="git worktree add /tmp/prd-agent-2 feature-2")

# 2. Run agents in parallel (background=true)
s1 = terminal(command="opencode run '<task>'", workdir="/tmp/prd-agent-1", background=True)
s2 = terminal(command="opencode run '<task>'", workdir="/tmp/prd-agent-2", background=True)

# 3. Wait for both
process(action="wait", session_id=s1)
process(action="wait", session_id=s2)

# 4. Merge back
terminal(command="cd ~/project && git merge feature-1")
terminal(command="cd ~/project && git merge feature-2")

# 5. Clean up
terminal(command="git worktree remove /tmp/prd-agent-1")
terminal(command="git worktree remove /tmp/prd-agent-2")
```

### Strategy C: Hybrid

Use worktree isolation for parallel tasks, subagent execution within each worktree for complex reasoning.

## Dependency Graph

For YAML tasks with `depends` field:

```python
def resolve_order(tasks):
    """Topological sort with parallel groups."""
    completed = set()
    order = []
    remaining = list(tasks)

    while remaining:
        # Find tasks whose dependencies are all met
        ready = [t for t in remaining if all(d in completed for d in t.get('depends', []))]
        if not ready:
            raise Exception(f"Circular dependency: {[t['id'] for t in remaining]}")

        # Group ready tasks by parallel_group
        groups = {}
        for t in ready:
            g = t.get('parallel_group', t['id'])  # each task is its own group by default
            groups.setdefault(g, []).append(t)

        for g in sorted(groups):
            order.append(groups[g])
            for t in groups[g]:
                completed.add(t['id'])
                remaining.remove(t)

    return order  # list of lists, inner lists are parallel-safe
```

## Dry Run Mode

Preview execution plan without running anything:

```python
def dry_run(prd_content):
    tasks = parse_prd(prd_content)
    order = resolve_order(tasks)
    for i, group in enumerate(order):
        parallel = len(group) > 1
        print(f"Step {i+1} ({'parallel' if parallel else 'sequential'}):")
        for t in group:
            deps = f" [depends: {', '.join(t.get('depends', []))}]" if t.get('depends') else ""
            print(f"  - {t['title']}{deps}")
```

## Prompt Construction

Build a structured prompt for each task:

```
## Project Context
{name: "...", language: "...", framework: "...", root: "..."}

## Rules (you MUST follow these)
{rules from .prd-loop/config.yaml or user preferences}

## Boundaries - Do NOT modify
{files/patterns to never touch}

## Completed Tasks (for context)
{brief summary of already-completed tasks}

## Current Task
{task description from PRD}
Task ID: {id}
Priority: {priority}

## Instructions
1. Implement the task above
2. Write tests if applicable
3. Run tests and ensure they pass
4. DO NOT commit — the orchestrator will handle commits
5. Report what you did in a summary
ONLY WORK ON THIS SINGLE TASK. Do not touch other files.
```

## PRD Parsing

### Markdown Parser (Enhanced)

```python
import re

def parse_markdown_prd(content):
    tasks = []
    for line in content.split('\n'):
        # Match: - [ ] Task description [priority:high] [depends:x,y]
        match = re.match(r'^- \[([ x])\] (.+)', line)
        if match:
            done = match.group(1) == 'x'
            desc = match.group(2)

            # Extract metadata from [key:value] patterns
            priority = re.search(r'\[priority:(\w+)\]', desc)
            depends = re.search(r'\[depends:([\w,\-]+)\]', desc)
            tags = re.search(r'\[tags:([\w,\-,]+)\]', desc)
            engine = re.search(r'\[engine:(\w+)\]', desc)

            clean_desc = re.sub(r'\[\w+:[\w,\-]+\]', '', desc).strip()

            task = {
                'title': clean_desc,
                'completed': done,
                'priority': priority.group(1) if priority else 'normal',
                'depends': depends.group(1).split(',') if depends else [],
                'tags': tags.group(1).split(',') if tags else [],
                'engine': engine.group(1) if engine else None
            }
            tasks.append(task)
    return tasks

def mark_complete(content, task_title):
    return content.replace(f'- [ ] {task_title}', f'- [x] {task_title}', 1)

def count_remaining(tasks):
    return sum(1 for t in tasks if not t['completed'])
```

### YAML Parser

```python
import yaml

def parse_yaml_prd(content):
    data = yaml.safe_load(content)
    return data.get('tasks', [])
```

## Configuration

### `.prd-loop/config.yaml`

```yaml
project:
  name: "my-app"
  root: "."                    # project root (default: current dir)
  language: "TypeScript"
  framework: "Next.js"

prd:
  path: "PRD.md"              # path to PRD file
  format: "markdown"           # markdown | yaml

execution:
  mode: "subagent"             # subagent | engine | hybrid
  default_engine: "opencode"   # opencode | claude | codex
  parallel: false              # enable parallel execution
  max_concurrent: 3            # max parallel tasks (subagent mode)
  worktree_base: "/tmp/prd-worktrees"
  auto_commit: true
  commit_prefix: "feat"        # feat | fix | chore

  # Subagent config
  subagent:
    toolsets: ["terminal", "file"]
    timeout: 300               # seconds per task

  # Engine config
  engine:
    opencode:
      model: "openrouter/anthropic/claude-sonnet-4"
      format: "json"
    claude:
      model: "claude-sonnet-4"
    codex:
      model: "o4-mini"

verification:
  test_command: "npm test"
  lint_command: "npm run lint"
  build_command: "npm run build"
  run_tests: true
  run_lint: false
  run_build: false

rules:
  - "use strict TypeScript"
  - "follow existing code patterns"
  - "add JSDoc comments for public APIs"

boundaries:
  never_touch:
    - "src/legacy/**"
    - "*.lock"
    - "node_modules/**"
```

## Engine Selection

| Engine | Command | Best For |
|--------|---------|----------|
| opencode | `opencode run '<prompt>' --format json` | Default choice, provider-agnostic |
| claude | `claude --dangerously-skip-permissions -p '<prompt>'` | Anthropic models, complex reasoning |
| codex | `codex exec --full-auto --json '<prompt>'` | OpenAI models, fast execution |
| subagent | `delegate_task(goal=...)` | Complex multi-file tasks, needs full tool access |

### Model Override

```bash
opencode run '<prompt>' --model openrouter/anthropic/claude-sonnet-4
opencode run '<prompt>' --model opencode/glm-4.7-free  # free tier
```

## Progress Tracking

### JSON State File (`.prd-loop/progress.json`)

```json
{
  "started_at": "2026-05-02T09:30:00Z",
  "updated_at": "2026-05-02T09:45:00Z",
  "mode": "subagent",
  "tasks_total": 5,
  "tasks_completed": 2,
  "tasks_failed": 0,
  "current_step": 3,
  "entries": [
    {
      "task_id": "user-model",
      "title": "Create user model",
      "status": "completed",
      "started_at": "09:30:15",
      "completed_at": "09:33:42",
      "duration_seconds": 207,
      "commit": "abc1234",
      "files_changed": ["prisma/schema.prisma", "src/models/user.ts"],
      "engine": "subagent"
    },
    {
      "task_id": "auth-endpoints",
      "title": "Add auth endpoints",
      "status": "completed",
      "started_at": "09:34:00",
      "completed_at": "09:42:15",
      "duration_seconds": 495,
      "commit": "def5678",
      "files_changed": ["src/routes/auth.ts", "src/middleware/auth.ts"],
      "engine": "opencode"
    },
    {
      "task_id": "tests",
      "title": "Write auth tests",
      "status": "in_progress",
      "started_at": "09:43:00"
    }
  ]
}
```

### Human-Readable Log (`.prd-loop/progress.md`)

```markdown
# PRD Progress Log

## Task 1: Create user model
- Status: ✅ Completed
- Duration: 3m 27s
- Files: prisma/schema.prisma, src/models/user.ts
- Commit: abc1234

## Task 2: Add auth endpoints
- Status: ✅ Completed
- Duration: 8m 15s
- Files: src/routes/auth.ts, src/middleware/auth.ts
- Commit: def5678

## Task 3: Write auth tests
- Status: 🔄 In Progress
```

## Completion Detection

After each agent run, check (in order):

1. **Files changed?** `git diff --name-only` (must have output)
2. **Exit code?** 0 = success, non-zero = failed
3. **Verification pass?** Run test/lint/build commands if configured
4. **Agent claimed completion?** Look for summary patterns
5. **Remaining tasks?** `count_remaining(prd_content)`

## Error Handling

| Error | Action | Retry? |
|-------|--------|--------|
| Agent timeout | Log error, mark task failed | Yes (2x) |
| Test failure | Report error, don't mark complete | No (fix manually) |
| Merge conflict | Spawn subagent to resolve | Yes (1x) |
| Circular dependency | Abort, report cycle | No |
| Engine not found | Fall back to subagent mode | N/A |
| Git not initialized | Abort, ask user to init | No |
| No PRD found | Ask user for path or generate one | N/A |

## PRD Generation

No PRD? Generate one from project analysis:

```python
# 1. Analyze project structure
analysis = terminal(command="find . -type f -name '*.ts' -o -name '*.js' | head -50")

# 2. Use subagent to generate PRD
prd = delegate_task(
    goal=f"""Analyze this project and generate a PRD.md with implementation tasks.

Project structure:
{analysis}

Generate a markdown PRD with:
- ## Features section with checkbox tasks
- Tasks ordered by dependency
- Each task should be specific and actionable
- Include [priority:high/normal/low] tags
- Include [depends:task-id] for dependent tasks

Output ONLY the PRD content, no explanation.""",
    toolsets=["terminal", "file"]
)
```

## Skill Composition

### Pipeline: kiro-spec-tasks → prd-task-loop

```bash
# 1. Generate tasks from spec
kiro-spec-tasks → produces PRD.md

# 2. Execute tasks
prd-task-loop → runs all tasks
```

### Pipeline: writing-plans → prd-task-loop

```bash
# 1. Create implementation plan
writing-plans → produces PLAN.md

# 2. Convert plan to PRD
# (extract actionable tasks from plan)

# 3. Execute
prd-task-loop → runs all tasks
```

### Pipeline: subagent-driven-development + prd-task-loop

Use subagent-driven-development's patterns for individual task execution within the PRD loop.

## Pitfalls

- OpenCode `run` mode doesn't support `@file` syntax (embed content in prompt instead)
- Don't run parallel agents in the same directory (use worktrees or subagent isolation)
- PRD must be in the git repo root or agents won't find it
- Free models may timeout on complex tasks; set appropriate timeouts
- Git must be initialized before running
- Subagent results are summaries only — intermediate tool outputs don't propagate back
- `delegate_task` max concurrent is configurable but capped at 3 by default
- YAML PRD requires `pyyaml` if parsing in execute_code (usually available)

## Comparison: Execution Modes

| Aspect | Ralphy (bash) | Hermes Engine | Hermes Subagent |
|--------|--------------|---------------|-----------------|
| Setup | `npm i -g ralphy-cli` | No install | No install |
| Parallel | Git worktrees | Manual background | Built-in delegate_task |
| Tool access | Terminal only | Terminal only | Full (file, terminal, web) |
| Reasoning | None (scripted) | CLI agent (limited) | Full LLM reasoning |
| Cost | Lowest | Low | Higher |
| Flexibility | Fixed logic | Medium | Highest |
| Best for | Simple, known tasks | Quick iterations | Complex, unknown tasks |
