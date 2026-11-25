---
name: huashu-agent-swarm
description: Multi-agent swarm parallel collaboration using pure git self-organisation, ideal for large-scale project development. Use when the user mentions "swarm mode", "multi-agent", "parallel development", or "agent swarm".
---

# Infinite Agent Loop — Multi-Agent Swarm Mode

> Inspired by Nicholas Carlini's experiment of using 16 Claude instances to autonomously build a C compiler.
> No master agent. Pure git self-organisation. Each agent independently claims tasks, writes code, and pushes.

## Trigger Conditions

Use this skill when the user mentions "swarm mode", "multi-agent parallel", "infinite loop", "agent swarm", or "launch swarm".

## Prerequisites

- tmux (`brew install tmux`)
- Claude CLI (already installed)
- A git repository (existing or new)

## Usage Workflow

### Step 1: Describe the Project

The user tells me:

- Project directory path (must be a git repository)
- Project goal and overall description
- Initial task list (or let the agents break it down themselves)
- Number of agents (default: 8)
- Code standards and test commands

### Step 2: Initialise the Project

```bash
bash SKILL_DIR/scripts/setup_project.sh <project-directory>
```

This creates the following inside the project:

- `AGENT_PROMPT.md` — Generated from a template; I customise it based on user requirements
- `TASKS.md` — Initial task checklist
- `current_tasks/` — Task claim directory
- `agent_logs/` — Logs directory

I then customise `AGENT_PROMPT.md` using `references/agent-prompt-template.md`, filling in project-specific details.

### Step 3: Launch the Swarm

```bash
bash SKILL_DIR/scripts/start_swarm.sh <number-of-agents> <project-directory>
```

This will:

1. Create a git worktree for each agent (shared `.git` object store — no disk waste)
2. Create a tmux session with one pane per agent
3. Each agent enters an infinite loop: pull → claim task → execute → push → next task

### Step 4: Open the Dashboard

```bash
python3 SKILL_DIR/scripts/dashboard.py <project-directory> 8420
```

Open <http://localhost:8420> in your browser to:

- View all agent statuses, git log, and task progress in real time
- View the latest logs for each agent
- Send instructions directly to agents via the input box (written to HUMAN_INPUT.md)
- Stop all agents with one click

You can also monitor via the command line:

```bash
# Terminal status
bash SKILL_DIR/scripts/status.sh <project-directory>

# Send instructions
bash SKILL_DIR/scripts/send_input.sh <project-directory> "your instruction"

# Attach to tmux directly to observe
tmux attach -t swarm-<project-name>
```

### Step 5: Stop the Swarm

```bash
bash SKILL_DIR/scripts/stop_swarm.sh <project-directory>
```

Automatically stops all agents, merges branches, and cleans up worktrees.

## Core Mechanisms

### Git Self-Organisation Coordination

- Each agent claims tasks via `current_tasks/*.lock` files
- Agents track global progress through `TASKS.md`
- Agents understand other agents' work via `git log`
- Conflicts are resolved by agents themselves

### Git Worktree Isolation

- No need for multiple clones — uses `git worktree` for isolation
- All worktrees share the same `.git` object store
- Each agent works independently in its own worktree

### Infinite Loop

- Each agent automatically begins the next session after completing one
- Uses `git pull` to fetch the latest work from other agents
- Sleep intervals between sessions prevent API rate limiting

## Key Configuration

| Parameter | Default | Description |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-agent-swarm
description: Multi-agent swarm parallel collaboration using pure git self-organisation, ideal for large-scale project development. Use when the user mentions "swarm mode", "multi-agent", "parallel development", or "agent swarm".
---

# Infinite Agent Loop — Multi-Agent Swarm Mode

> Inspired by Nicholas Carlini's experiment of using 16 Claude instances to autonomously build a C compiler.
> No master agent. Pure git self-organisation. Each agent independently claims tasks, writes code, and pushes.

## Trigger Conditions

Use this skill when the user mentions "swarm mode", "multi-agent parallel", "infinite loop", "agent swarm", or "launch swarm".

## Prerequisites

- tmux (`brew install tmux`)
- Claude CLI (already installed)
- A git repository (existing or new)

## Usage Workflow

### Step 1: Describe the Project

The user tells me:

- Project directory path (must be a git repository)
- Project goal and overall description
- Initial task list (or let the agents break it down themselves)
- Number of agents (default: 8)
- Code standards and test commands

### Step 2: Initialise the Project

```bash
bash SKILL_DIR/scripts/setup_project.sh <project-directory>
```

This creates the following inside the project:

- `AGENT_PROMPT.md` — Generated from a template; I customise it based on user requirements
- `TASKS.md` — Initial task checklist
- `current_tasks/` — Task claim directory
- `agent_logs/` — Logs directory

I then customise `AGENT_PROMPT.md` using `references/agent-prompt-template.md`, filling in project-specific details.

### Step 3: Launch the Swarm

```bash
bash SKILL_DIR/scripts/start_swarm.sh <number-of-agents> <project-directory>
```

This will:

1. Create a git worktree for each agent (shared `.git` object store — no disk waste)
2. Create a tmux session with one pane per agent
3. Each agent enters an infinite loop: pull → claim task → execute → push → next task

### Step 4: Open the Dashboard

```bash
python3 SKILL_DIR/scripts/dashboard.py <project-directory> 8420
```

Open <http://localhost:8420> in your browser to:

- View all agent statuses, git log, and task progress in real time
- View the latest logs for each agent
- Send instructions directly to agents via the input box (written to HUMAN_INPUT.md)
- Stop all agents with one click

You can also monitor via the command line:

```bash
# Terminal status
bash SKILL_DIR/scripts/status.sh <project-directory>

# Send instructions
bash SKILL_DIR/scripts/send_input.sh <project-directory> "your instruction"

# Attach to tmux directly to observe
tmux attach -t swarm-<project-name>
```

### Step 5: Stop the Swarm

```bash
bash SKILL_DIR/scripts/stop_swarm.sh <project-directory>
```

Automatically stops all agents, merges branches, and cleans up worktrees.

## Core Mechanisms

### Git Self-Organisation Coordination

- Each agent claims tasks via `current_tasks/*.lock` files
- Agents track global progress through `TASKS.md`
- Agents understand other agents' work via `git log`
- Conflicts are resolved by agents themselves

### Git Worktree Isolation

- No need for multiple clones — uses `git worktree` for isolation
- All worktrees share the same `.git` object store
- Each agent works independently in its own worktree

### Infinite Loop

- Each agent automatically begins the next session after completing one
- Uses `git pull` to fetch the latest work from other agents
- Sleep intervals between sessions prevent API rate limiting

## Key Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| Number of agents | 8 | Can be specified at launch |
| Sleep interval | 5 seconds | Adjustable in agent_loop.sh |
| Model | claude-opus-4-6 | Adjustable in agent_loop.sh |

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| API rate limiting | Sleep intervals + adjustable agent count |
| Merge conflicts | AGENT_PROMPT guides small, granular commits |
| Infinite loop doing useless work | Log monitoring + stop conditions |
| Disk space | stop_swarm.sh auto-cleans |
| Cost spiral | Limit session count in AGENT_PROMPT |

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Number of agents | 8 | Can be specified at launch |
| Sleep interval | 5 seconds | Adjustable in agent_loop.sh |
| Model | claude-opus-4-6 | Adjustable in agent_loop.sh |

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| API rate limiting | Sleep intervals + adjustable agent count |
| Merge conflicts | AGENT_PROMPT guides small, granular commits |
| Infinite loop doing useless work | Log monitoring + stop conditions |
| Disk space | stop_swarm.sh auto-cleans |
| Cost spiral | Limit session count in AGENT_PROMPT |

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Number of agents | 8 | Can be specified at launch |
| Sleep interval | 5 seconds | Adjustable in agent_loop.sh |
| Model | claude-opus-4-6 | Adjustable in agent_loop.sh |

## Risks and Mitigations

| Risk | Mitigation |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-agent-swarm
description: Multi-agent swarm parallel collaboration using pure git self-organisation, ideal for large-scale project development. Use when the user mentions "swarm mode", "multi-agent", "parallel development", or "agent swarm".
---

# Infinite Agent Loop — Multi-Agent Swarm Mode

> Inspired by Nicholas Carlini's experiment of using 16 Claude instances to autonomously build a C compiler.
> No master agent. Pure git self-organisation. Each agent independently claims tasks, writes code, and pushes.

## Trigger Conditions

Use this skill when the user mentions "swarm mode", "multi-agent parallel", "infinite loop", "agent swarm", or "launch swarm".

## Prerequisites

- tmux (`brew install tmux`)
- Claude CLI (already installed)
- A git repository (existing or new)

## Usage Workflow

### Step 1: Describe the Project

The user tells me:

- Project directory path (must be a git repository)
- Project goal and overall description
- Initial task list (or let the agents break it down themselves)
- Number of agents (default: 8)
- Code standards and test commands

### Step 2: Initialise the Project

```bash
bash SKILL_DIR/scripts/setup_project.sh <project-directory>
```

This creates the following inside the project:

- `AGENT_PROMPT.md` — Generated from a template; I customise it based on user requirements
- `TASKS.md` — Initial task checklist
- `current_tasks/` — Task claim directory
- `agent_logs/` — Logs directory

I then customise `AGENT_PROMPT.md` using `references/agent-prompt-template.md`, filling in project-specific details.

### Step 3: Launch the Swarm

```bash
bash SKILL_DIR/scripts/start_swarm.sh <number-of-agents> <project-directory>
```

This will:

1. Create a git worktree for each agent (shared `.git` object store — no disk waste)
2. Create a tmux session with one pane per agent
3. Each agent enters an infinite loop: pull → claim task → execute → push → next task

### Step 4: Open the Dashboard

```bash
python3 SKILL_DIR/scripts/dashboard.py <project-directory> 8420
```

Open <http://localhost:8420> in your browser to:

- View all agent statuses, git log, and task progress in real time
- View the latest logs for each agent
- Send instructions directly to agents via the input box (written to HUMAN_INPUT.md)
- Stop all agents with one click

You can also monitor via the command line:

```bash
# Terminal status
bash SKILL_DIR/scripts/status.sh <project-directory>

# Send instructions
bash SKILL_DIR/scripts/send_input.sh <project-directory> "your instruction"

# Attach to tmux directly to observe
tmux attach -t swarm-<project-name>
```

### Step 5: Stop the Swarm

```bash
bash SKILL_DIR/scripts/stop_swarm.sh <project-directory>
```

Automatically stops all agents, merges branches, and cleans up worktrees.

## Core Mechanisms

### Git Self-Organisation Coordination

- Each agent claims tasks via `current_tasks/*.lock` files
- Agents track global progress through `TASKS.md`
- Agents understand other agents' work via `git log`
- Conflicts are resolved by agents themselves

### Git Worktree Isolation

- No need for multiple clones — uses `git worktree` for isolation
- All worktrees share the same `.git` object store
- Each agent works independently in its own worktree

### Infinite Loop

- Each agent automatically begins the next session after completing one
- Uses `git pull` to fetch the latest work from other agents
- Sleep intervals between sessions prevent API rate limiting

## Key Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| Number of agents | 8 | Can be specified at launch |
| Sleep interval | 5 seconds | Adjustable in agent_loop.sh |
| Model | claude-opus-4-6 | Adjustable in agent_loop.sh |

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| API rate limiting | Sleep intervals + adjustable agent count |
| Merge conflicts | AGENT_PROMPT guides small, granular commits |
| Infinite loop doing useless work | Log monitoring + stop conditions |
| Disk space | stop_swarm.sh auto-cleans |
| Cost spiral | Limit session count in AGENT_PROMPT |

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| API rate limiting | Sleep intervals + adjustable agent count |
| Merge conflicts | AGENT_PROMPT guides small, granular commits |
| Infinite loop doing useless work | Log monitoring + stop conditions |
| Disk space | stop_swarm.sh auto-cleans |
| Cost spiral | Limit session count in AGENT_PROMPT |

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| API rate limiting | Sleep intervals + adjustable agent count |
| Merge conflicts | AGENT_PROMPT guides small, granular commits |
| Infinite loop doing useless work | Log monitoring + stop conditions |
| Disk space | stop_swarm.sh auto-cleans |
| Cost spiral | Limit session count in AGENT_PROMPT |

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
