# Claude Code Agent Integration

claude-threads provides built-in agents that integrate with Claude Code's multi-agent orchestration system with git worktree isolation support.

## Overview

Agents are specialized Claude instances with focused expertise. They're invoked via Claude Code's Task tool with the `subagent_type` parameter. Agents can work in isolated git worktrees for parallel development.

```
┌─────────────────────────────────────────────────────────────────┐
│                    THREAD ORCHESTRATOR                          │
│              (coordinates all agents)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Developer  │  │   Reviewer   │  │  PR Manager  │          │
│  │    Agent     │  │    Agent     │  │    Agent     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    Fixer     │  │   Security   │  │   Explorer   │          │
│  │    Agent     │  │   Reviewer   │  │    Agent     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Available Agents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| `thread-orchestrator` | Sonnet | All + Task | Coordinate multi-agent workflows with worktree support |
| `story-developer` | Sonnet | Read/Write/Edit | Implement features with TDD |
| `code-reviewer` | Sonnet | Read-only | Quality and best practices review |
| `security-reviewer` | Sonnet | Read-only | Security audit and vulnerability detection |
| `test-writer` | Sonnet | Read/Write/Edit | Write comprehensive tests |
| `issue-fixer` | Sonnet | Read/Write/Edit | Fix CI and review issues with worktree awareness |
| `pr-manager` | Sonnet | Read + Bash | PR lifecycle management with PR Shepherd integration |
| `explorer` | Haiku | Read-only | Fast codebase exploration |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `threads` | Thread orchestration - create, manage, monitor threads |
| `bmad-autopilot` | BMAD autonomous development with worktree isolation |
| `thread-orchestrator` | Multi-agent coordination with worktree and PR Shepherd |

## Agent Configuration

Agents are defined in `.claude/agents/` as Markdown files with YAML frontmatter:

```markdown
---
name: agent-name
description: When to use this agent
tools: Tool1, Tool2, Tool3
model: sonnet
---

# Agent Name

System prompt defining the agent's role and behavior.
```

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase, hyphens) |
| `description` | Yes | Natural language description for auto-matching |
| `tools` | No | Comma-separated tool list (inherits all if omitted) |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` |

## Using Agents

### Automatic Delegation

Claude Code automatically delegates to agents based on task description matching:

```
User: "Review this code for security issues"
→ Claude matches description → Invokes security-reviewer agent
```

### Explicit Invocation

Request specific agent by name:

```
User: "Use the story-developer agent to implement this feature"
→ Claude invokes story-developer directly
```

### Via Task Tool

Programmatically invoke agents:

```typescript
// In agent prompt or code
Use the Task tool with subagent_type="code-reviewer" to review changes
```

## Agent Patterns

### Parallel Execution with Worktrees

Run multiple agents concurrently in isolated worktrees (up to 10):

```
┌─────────────────────────────────────────┐
│          ORCHESTRATOR                    │
│                                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │Developer│ │Developer│ │Developer│   │
│  │ Epic 7A │ │ Epic 8A │ │ Epic 9A │   │
│  │[worktree]│[worktree]│[worktree]│   │
│  └────┬────┘ └────┬────┘ └────┬────┘   │
│       │           │           │         │
│       └───────────┼───────────┘         │
│                   ▼                      │
│           Collect Results                │
└─────────────────────────────────────────┘
```

Each agent works in its own isolated git worktree, enabling true parallel development without conflicts.

### Pipeline Execution

Sequential agent chain:

```
Developer → Code Reviewer → Security Reviewer → PR Manager → Merge
```

### Specialist Routing with PR Shepherd

Route to appropriate agent based on issue type, with worktree isolation:

```
┌─────────────────────────────────────────┐
│           PR SHEPHERD + ORCHESTRATOR     │
│                   │                      │
│          Analyze Issue Type              │
│        (in isolated worktree)            │
│                   │                      │
│     ┌─────────────┼─────────────┐       │
│     ▼             ▼             ▼       │
│ ┌────────┐  ┌──────────┐  ┌────────┐   │
│ │CI Fixer│  │Security  │  │ Style  │   │
│ │[worktree]│Specialist│  │ Fixer  │   │
│ └────────┘  └──────────┘  └────────┘   │
└─────────────────────────────────────────┘
```

The PR Shepherd automatically creates isolated worktrees for fix agents, enabling parallel PR fixes without conflicts.

## BMAD Workflow with Agents and Worktrees

The BMAD autopilot uses agents at each phase with worktree isolation:

```
FIND_EPIC
    │
    ▼
CREATE_WORKTREE ──────────────┐
    │                          │ Isolated git worktree
CREATE_BRANCH                  │ for development
    │                          │
    ▼◄─────────────────────────┘
DEVELOP_STORIES ──────────────┐
    │                         │
    │  ┌─────────────────┐   │
    │  │ story-developer │   │ Parallel for each story
    │  │    (Sonnet)     │   │ (in worktree)
    │  └─────────────────┘   │
    │                         │
    ▼◄────────────────────────┘
CODE_REVIEW
    │
    │  ┌─────────────────┐  ┌──────────────────┐
    │  │  code-reviewer  │  │ security-reviewer │
    │  │    (Sonnet)     │  │     (Sonnet)      │
    │  └─────────────────┘  └──────────────────┘
    │
    ▼
CREATE_PR
    │
    │  ┌─────────────────┐
    │  │   pr-manager    │
    │  │    (Sonnet)     │
    │  └─────────────────┘
    │
    ▼
WAIT_COPILOT (via PR Shepherd)
    │
    │  ┌─────────────────┐
    │  │    explorer     │  Fast status checks
    │  │    (Haiku)      │
    │  └─────────────────┘
    │
    ├── CI FAILED ────────┐
    │                     │
    │  ┌─────────────────┐
    │  │   issue-fixer   │  Works in PR worktree
    │  │    (Sonnet)     │
    │  └─────────────────┘
    │                     │
    │◄────────────────────┘
    ▼
MERGE_PR
    │
    ▼
CLEANUP_WORKTREE ─────────────┐
                              │ Remove isolated worktree
                              │
```

## Creating Custom Agents

### Step 1: Create Agent File

```bash
# Project-level (this project only)
mkdir -p .claude/agents/

# Or user-level (all projects)
mkdir -p ~/.claude/agents/
```

### Step 2: Define Agent

```markdown
---
name: my-specialist
description: Expert in specific domain. Use when working with X technology.
tools: Read, Write, Edit, Bash
model: sonnet
---

# My Specialist Agent

You are an expert in X technology with deep knowledge of...

## Your Role
...

## Workflow
1. First, analyze...
2. Then, implement...
3. Finally, verify...

## Output Events
```json
{"event": "TASK_COMPLETED", "result": "..."}
```
```

### Step 3: Write Effective Descriptions

The description field is crucial for automatic delegation:

```markdown
# Good descriptions
description: Security audit specialist. Use proactively after code changes to check for vulnerabilities.
description: Expert code reviewer. MUST BE USED before creating pull requests.

# Poor descriptions
description: Helps with code  # Too vague
description: Does stuff        # Not specific
```

## Agent Communication

Agents communicate via events on the blackboard:

### Publishing Events

```json
{"event": "STORY_COMPLETED", "story_id": "7A.1", "commit": "abc123"}
```

### Subscribing to Events

Orchestrator watches for events and routes to appropriate agents.

### Inter-Agent Messages

```bash
# Send message to specific agent/thread
ct event publish TASK_REQUEST '{"target": "reviewer", "data": {...}}'
```

## Performance Optimization

### Use Appropriate Models

| Task | Recommended Model |
|------|-------------------|
| Fast searches | Haiku |
| Code generation | Sonnet |
| Complex analysis | Sonnet |
| Critical decisions | Opus |

### Parallel Execution

Launch independent tasks simultaneously:

```
# Instead of sequential:
Developer → Tests → Docs

# Run in parallel:
Developer ─┐
Tests     ─┼─→ Collect Results
Docs      ─┘
```

### Context Isolation

Each agent has its own context window:
- Prevents context pollution
- Focused expertise per agent
- Better results for specialized tasks

## Troubleshooting

### Agent Not Found

```bash
# Check agent files exist
ls -la .claude/agents/
ls -la ~/.claude/agents/

# Verify YAML frontmatter
head -20 .claude/agents/my-agent.md
```

### Agent Not Invoked

- Check description field matches task
- Try explicit invocation by name
- Verify tools are available

### Agent Fails

```bash
# Check logs
ct thread logs <thread-id>

# Check event history
ct event list --source <agent-name>
```

## PR Shepherd Integration

The [PR Shepherd](PR-SHEPHERD.md) uses agents for automatic PR fixing with worktree isolation:

```
PR Shepherd detects CI failure
         │
         ▼
┌─────────────────────┐
│ Create PR Worktree  │  Isolated git worktree for fixes
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     pr-fix.md       │  Template spawned as thread
│  (fix thread)       │  (runs in worktree)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   issue-fixer       │  Agent handles the actual fix
│     (Sonnet)        │  (in isolated worktree)
└──────────┬──────────┘
           │
           ▼
    Push changes from worktree
           │
           ▼
  Shepherd re-checks CI
           │
           ▼ (on merge)
    Cleanup worktree
```

### PR Fix Events

Agents can subscribe to PR events:

| Event | When | Use |
|-------|------|-----|
| `WORKTREE_CREATED` | Worktree created for PR | Track isolation |
| `PR_FIX_STARTED` | Fix thread spawned in worktree | Track fix attempts |
| `CI_FAILED` | CI checks fail | Trigger analysis |
| `CI_PASSED` | CI checks pass | Celebrate |
| `WORKTREE_PUSHED` | Changes pushed from worktree | Track fix progress |
| `PR_APPROVED` | Review approved | Prepare merge |
| `PR_MERGED` | PR merged | Cleanup |
| `WORKTREE_DELETED` | Worktree cleaned up | Confirm cleanup |

### Custom Fix Agents

Create specialized fix agents for your codebase:

```markdown
---
name: my-ci-fixer
description: Expert in fixing CI failures for our Node.js monorepo
tools: Read, Write, Edit, Bash
model: sonnet
---

# My CI Fixer

Specialized knowledge for fixing:
- ESLint errors (our custom rules)
- Jest test failures (our test patterns)
- TypeScript build errors (our tsconfig)
...
```

Then reference in `config.yaml`:

```yaml
pr_shepherd:
  fix_template: prompts/my-ci-fixer.md
```

## Best Practices

1. **Focused Agents**: Each agent should have one clear purpose
2. **Read-Only When Possible**: Limit write access to agents that need it
3. **Descriptive Names**: Use clear, action-oriented names
4. **Event-Driven**: Communicate via events, not shared state
5. **Fail Fast**: Output blocked events when unable to proceed
6. **Minimal Tools**: Only grant necessary permissions
7. **Use Worktrees**: For parallel development, use isolated worktrees
8. **Leverage PR Shepherd**: For automatic CI/review handling

## See Also

- [PR-SHEPHERD.md](PR-SHEPHERD.md) - Automatic PR feedback loop
- [../templates/prompts/pr-fix.md](../templates/prompts/pr-fix.md) - Default fix template
