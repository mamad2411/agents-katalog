---
name: work
description: Analyze GitHub issues, assign to parallel agents, and launch work sessions in isolated worktrees
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Grep, Glob, Task
---

# Work Command

Analyze open GitHub issues, determine parallelization opportunities, and launch 3-5 AI agents in isolated git worktrees.

## Overview

This skill orchestrates parallel development by:
1. Fetching open GitHub issues
2. Grouping them by component to avoid merge conflicts
3. Creating isolated git worktrees for each agent
4. Launching parallel Claude Code sessions with ownership enforcement

## Instructions

### Step 1: Gather Context

Read project context to understand component ownership:

```bash
# Read project configuration
cat CLAUDE.md
cat .claude/rules/03-parallel-workflow.md  # Component ownership table
```

### Step 2: Fetch Open Issues

```bash
# Get all open issues with details
gh issue list --state open --limit 50 --json number,title,labels,body,assignees

# Check existing PRs to avoid duplicate work
gh pr list --state open --json number,title,headRefName

# Check existing worktrees
git worktree list
```

### Step 3: Analyze Issues for Parallelization

For each issue, determine:

| Attribute | How to Determine |
|-----------|------------------|
| **Component** | Labels (e.g., `component:backend`), title keywords, or file paths mentioned |
| **Dependencies** | Parse body for "blocked by #N", "depends on #N", "after #N" |
| **Priority** | Labels (`priority:high`), age, or explicit priority field |
| **Complexity** | Simple (1-2 files), Medium (3-5 files), Complex (6+ files) |

### Step 4: Create Work Packages

Group issues into 3-5 work packages following these rules:

1. **One component per agent** - Prevents merge conflicts
2. **Related issues together** - Reduces context switching
3. **Include quick wins** - Each agent should have at least one small task
4. **Respect dependencies** - Blocked issues go to agent that unblocks them
5. **Balance workload** - Distribute complexity evenly

**Component Ownership** (customize in `03-parallel-workflow.md`):

```
# Example ownership mapping - CUSTOMIZE FOR YOUR PROJECT
backend/         -> Backend Agent
frontend/        -> Frontend Agent
infrastructure/  -> Infrastructure Agent
docs/, knowledge/ -> Staff Engineer Agent
```

### Step 5: Generate Agent Prompts

**CRITICAL**: Each agent's `prompt` field MUST contain the FULL prompt below — not an abbreviated summary. Agents that receive short prompts skip important steps.

For each agent, fill in this template completely and use the entire result as the `prompt` value in the session config JSON:

```
You are the {NAME} agent for this project, working autonomously in a parallel session.

FIRST STEPS (DO NOT SKIP):
1. Read .claude-agent.md in this directory for your agent identity and other running agents
2. Read CLAUDE.md
3. Read relevant knowledge docs for your domain
4. Review existing patterns in your owned directories

YOUR ASSIGNMENT:
- Branch: {BRANCH_NAME}
- Issues: {#N, #M, ...}
- Owned paths (you MUST NOT modify files outside these): {PATHS}

ISSUE DETAILS:
{For each issue: number, title, description summary, acceptance criteria, suggested approach}

VALIDATION — before EACH commit:
- Linting passes (ruff check / eslint / etc.)
- Formatting passes (ruff format --check / prettier --check / etc.)
- Tests pass (pytest / npm test / etc.)
- No secrets committed

GIT WORKFLOW:
- Conventional commits: feat:, fix:, test:, docs:
- Push after each logical unit
- Reference issues: "Fixes #N" or "Part of #N"

COORDINATION:
- Stay in your lane — only modify files in your owned paths
- The AGENT_OWNS env var enforces this at commit time
- If you need something from another agent, document it in docs/INTEGRATION_REQUESTS.md
- Do NOT wait for other agents — continue with other tasks

WHEN COMPLETE:
1. Run /session-wrap to document your work
2. Run /pr-check to validate PR readiness
3. Create PR with gh pr create, referencing all closed issues
4. Review your code against knowledge/staff-engineer-review/SKILL.md

BEGIN NOW. Read CLAUDE.md, then the required knowledge docs, then start on your first issue.
```

### Step 6: Create Session Configuration

Generate config file at `scripts/configs/work-session-{timestamp}.json`:

**IMPORTANT**: The config MUST include `owned_paths` for each pane. This is used by the launcher to set the `AGENT_OWNS` env var, which the pre-commit hook checks to block out-of-scope file modifications.

```json
{
  "session_name": "{project}-work-{timestamp}",
  "startup_delay_seconds": 3,
  "claude_flags": "--dangerously-skip-permissions",
  "panes": [
    {
      "name": "{Agent Display Name}",
      "directory": "{/absolute/path/to/worktree}",
      "branch": "{feat/branch-name}",
      "owned_paths": ["{path/prefix/1/}", "{path/prefix/2/}"],
      "prompt": "{FULL PROMPT FROM STEP 5 — not abbreviated}"
    }
  ]
}
```

### Step 7: Show Dry Run Preview

Before creating worktrees or launching, display a preview table:

```
## Work Session Preview

| Agent | Branch | Issues | Owned Paths | Worktree |
|-------|--------|--------|-------------|----------|
| ... | ... | ... | ... | ... |

Proceed? [Y/n]
```

Wait for user confirmation. If the user says no or wants changes, adjust the plan.

### Step 8: Setup Worktrees

For each agent, create an isolated worktree:

```bash
PROJECT_ROOT=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_ROOT")

# For each agent
AGENT_SUFFIX="{{suffix}}"  # e.g., "backend", "frontend"
BRANCH="feat/{{component}}-{{description}}"
WORKTREE_PATH="../${PROJECT_NAME}-${AGENT_SUFFIX}"

# Create worktree if it doesn't exist
if ! git worktree list | grep -q "$WORKTREE_PATH"; then
    git worktree add "$WORKTREE_PATH" -b "$BRANCH"
    echo "Created worktree: $WORKTREE_PATH on branch $BRANCH"
else
    echo "Worktree exists: $WORKTREE_PATH"
fi
```

### Step 9: Launch Sessions

```bash
./scripts/start-parallel-sessions.sh --config scripts/configs/work-session-{timestamp}.json
```

### Step 10: Output Summary

Display:

```
## Work Session Launched

| Agent | Branch | Issues | Worktree | Ownership Enforced |
|-------|--------|--------|----------|--------------------|
| ... | ... | ... | ... | Yes/No |

Session: {project}-work-{timestamp}

Monitor: /ps or ./scripts/parallel-session-status.sh {session_name}

Config: scripts/configs/work-session-{timestamp}.json
```

---

## Agent Count Heuristics

| Open Issues | Recommended Agents |
|-------------|-------------------|
| 1-5 | 2 |
| 6-12 | 3 |
| 13-20 | 4 |
| 21+ | 5 |

Always include a Staff Engineer agent when there are documentation or knowledge updates needed.

---

## Conflict Avoidance Rules

**NEVER assign two agents to:**
- Same source directory
- Same configuration files
- Overlapping module paths

**Shared files** (`package.json`, `pyproject.toml`, `docker-compose.yml`):
- Assign to Infrastructure or Staff Engineer agent only
- Other agents must not modify these

---

## Error Handling

| Situation | Action |
|-----------|--------|
| No open issues | Report and suggest creating issues first |
| Worktree already exists | Reuse existing, verify correct branch |
| < 3 parallelizable issues | Run with 2 agents or work sequentially |
| All issues blocked | Identify and assign blocker-resolver first |
| Conflicting assignments | Re-analyze, split differently |

---

## Required Setup

For this skill to work, ensure:

1. **GitHub CLI** installed and authenticated (`gh auth login`)
2. **tmux** installed (for parallel session management)
3. **jq** installed (for config parsing)
4. **Component ownership** defined in `.claude/rules/03-parallel-workflow.md`
5. **Git** configured with your credentials

---

## Customization

Edit the component ownership mapping in `.claude/rules/03-parallel-workflow.md` to match your project structure:

```markdown
| Agent | Branch Pattern | Owns |
|-------|----------------|------|
| Backend | `feat/backend-*` | `src/api/`, `src/services/` |
| Frontend | `feat/frontend-*` | `src/components/`, `src/pages/` |
| Infrastructure | `feat/infra-*` | `terraform/`, `.github/`, `docker/` |
| Staff Engineer | `feat/docs-*` | `docs/`, `knowledge/`, `*.md` |
```
