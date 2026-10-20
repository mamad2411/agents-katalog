# Agent Task Tracking (SAP-015) - Claude-Specific Awareness

**SAP ID**: SAP-015
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## 📖 Quick Reference

**New to SAP-015?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Initialize beads in repository
- 📚 **Time Savings** - Eliminates 10-15 min context re-establishment per session, persistent task memory across hours/days/weeks
- 🎯 **Feature 1** - `.beads/issues.jsonl` (committed), `.beads/beads.db` (gitignored cache)
- 🔧 **Feature 2** - Automatic ready-work detection (no blockers)
- 📊 **Feature 3** - Share tasks via git push/pull
- 🔗 **Integration** - Works with SAP-001, SAP-010, SAP-012, SAP-013, SAP-015, SAP-027

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-015.
s.

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for beads task tracking.

### First-Time Beads Setup

1. Read [AGENTS.md](AGENTS.md) for generic beads workflows
2. Use this file for Claude Code tool integration (Bash for bd commands, Read for task details)
3. Follow 3-step process: Install beads → Initialize repository → Create first task

### Session Resumption

- Use Bash tool for bd commands (list, create, update, close, dep)
- Parse JSON output for programmatic task queries: `bd list --json`
- Always pull before querying in multi-agent scenarios: `git pull`

---

## Claude Code Beads Workflows

### Workflow 1: Initializing Beads with Claude Code

```markdown
User: "Set up beads task tracking for this project"

Claude (Phase 1: Check Beads - 0-5k tokens):
1. Check if beads installed:
   Bash: which bd
2. If not found, guide user to install:
   "Please install beads CLI:
   npm install -g beads-cli@latest

   Then confirm: which bd"

Claude (Phase 2: Initialize Beads - 5-10k tokens):
3. Check if already initialized:
   Bash: ls .beads/
4. If not exists, initialize:
   Bash: cd /path/to/repo && bd init
5. Verify initialization:
   Bash: ls -la .beads/

Claude (Phase 3: Commit Configuration - 10-15k tokens):
6. Add to git:
   Bash: git add .beads/
7. Commit:
   Bash: git commit -m "feat: Initialize beads task tracking (SAP-015)"
8. Verify commit:
   Bash: git log -1 --oneline

Claude (response to user):
"I've initialized beads task tracking:

✅ Beads initialized (prefix: {project-name})
✅ Configuration committed (.beads/issues.jsonl, config.yaml, metadata.json)
✅ Ready for agent task tracking

Database files:
- .beads/beads.db (SQLite cache, gitignored)
- .beads/issues.jsonl (source of truth, committed)
- .beads/config.yaml (project config, committed)

Next: Create your first task with 'bd create \"Task title\"'"

Result: Repository initialized with beads task tracking
```

---

### Workflow 2: Creating and Tracking Tasks with Claude Code

```markdown
User: "Create beads tasks for implementing OAuth feature"

Claude (Phase 1: Create Main Task - 0-5k tokens):
1. Create main task:
   Bash: bd create "Implement OAuth authentication" --priority 0 --assignee claude-code --json
2. Parse JSON output to get task ID:
   # Output: {"id":"project-a3f8",...}
3. Store task ID: main_task_id = "project-a3f8"

Claude (Phase 2: Create Subtasks - 5-15k tokens):
4. Create subtask 1:
   Bash: bd create "Add OAuth config to settings" --priority 1 --json
   # Store: subtask_1_id = "project-b2c4"
5. Create subtask 2:
   Bash: bd create "Implement OAuth callback handler" --priority 1 --json
   # Store: subtask_2_id = "project-c5d6"
6. Create subtask 3:
   Bash: bd create "Write OAuth integration tests" --priority 1 --json
   # Store: subtask_3_id = "project-d7e8"

Claude (Phase 3: Add Dependencies - 15-25k tokens):
7. Link subtasks to main task:
   Bash: bd dep add project-a3f8 blocks project-b2c4
   Bash: bd dep add project-a3f8 blocks project-c5d6
   Bash: bd dep add project-a3f8 blocks project-d7e8
8. Verify dependencies:
   Bash: bd show project-a3f8

Claude (Phase 4: Query Ready Work - 25-30k tokens):
9. Check what's ready:
   Bash: bd list --ready --json
10. Parse output:
    # Shows: subtask_1, subtask_2, subtask_3 (main task blocked)

Claude (Phase 5: Work on First Subtask - 30-50k tokens):
11. Start first subtask:
    Bash: bd update project-b2c4 --status in_progress
12. Implement OAuth config:
    # Use Edit/Write tools to add config
13. Complete subtask:
    Bash: bd close project-b2c4 "Added OAuth settings (client_id, secret, redirect_uri) to config.py"

Claude (Phase 6: Commit Progress - 50-55k tokens):
14. Commit task updates:
    Bash: git add .beads/issues.jsonl src/config.py
    Bash: git commit -m "feat: Add OAuth config (beads: project-b2c4)"
15. Check next ready task:
    Bash: bd list --ready

Claude (response to user):
"Created beads tasks for OAuth feature:

Main Task:
✅ project-a3f8: Implement OAuth authentication [Priority: 0]

Subtasks (blocking main task):
1. ✅ project-b2c4: Add OAuth config [COMPLETED]
2. ⏳ project-c5d6: Implement callback handler [READY]
3. ⏳ project-d7e8: Write integration tests [READY]

Progress: 1/3 subtasks complete (33%)
Next: Implement OAuth callback handler (project-c5d6)

Dependencies tracked in beads, agent can resume across sessions."

Result: OAuth feature tracked with dependencies, agent knows what's next
```

---

### Workflow 3: Session Resumption with Claude Code

```markdown
User: "What should I work on?" (new session, context reset)

Claude (Phase 1: Sync with Git - 0-5k tokens):
1. Pull latest changes:
   Bash: git pull
   # Beads auto-imports issues.jsonl if newer than beads.db

Claude (Phase 2: Check Ready Work - 5-10k tokens):
2. Query ready tasks:
   Bash: bd list --ready --json
3. Parse JSON output:
   # Shows: Available tasks with no blockers
4. Check in-progress tasks:
   Bash: bd list --status in_progress --json

Claude (Phase 3: Review Task Details - 10-20k tokens):
5. If in-progress tasks exist, show details:
   Bash: bd show <in-progress-task-id>
6. If no in-progress, show highest priority ready task:
   Bash: bd list --ready --json | # Parse first task

Claude (Phase 4: Present Options - 20-25k tokens):
7. Present task options to user with context:
   "Based on beads tasks, here's what's ready to work on:

   In Progress:
   - project-c5d6: Implement OAuth callback handler [Priority: 1]
     Started: 2 hours ago
     Next: Complete /oauth/callback endpoint

   Ready to Start:
   - project-d7e8: Write OAuth integration tests [Priority: 1]
   - project-e9f0: Fix authentication bug [Priority: 0]

   Recommend: Continue project-c5d6 (in-progress) or start project-e9f0 (higher priority)"

Claude (response to user):
"Session resumed from beads task tracking:

Current Work:
⏳ project-c5d6: Implement OAuth callback handler [IN PROGRESS]
   - Started: 2 hours ago
   - Dependencies: None (ready)
   - Next step: Complete /oauth/callback endpoint implementation

Would you like me to:
A) Continue project-c5d6 (OAuth callback)
B) Start project-e9f0 (authentication bug, higher priority)
C) Show all ready tasks"

Result: Agent resumes work in <1 minute with full context
```

---

### Workflow 4: Multi-Agent Coordination with Claude Code

```markdown
Context: Agent 1 (Claude Code) and Agent 2 (Cursor) working on same repository

Agent 1 (Claude Code):
User: "Create tasks for authentication refactor"

Claude (Phase 1: Create Tasks - 0-10k tokens):
1. Create main task:
   Bash: bd create "Refactor authentication module" --priority 0 --assignee agent-1 --json
2. Create subtasks:
   Bash: bd create "Extract AuthProvider interface" --priority 1 --assignee agent-1 --json
   Bash: bd create "Implement OAuth provider" --priority 1 --assignee agent-2 --json
   Bash: bd create "Write provider tests" --priority 1 --assignee agent-1 --json
3. Add dependencies

Claude (Phase 2: Commit and Push - 10-15k tokens):
4. Commit tasks:
   Bash: git add .beads/issues.jsonl
   Bash: git commit -m "Add authentication refactor tasks (agent-1: interface, tests; agent-2: OAuth)"
5. Push to remote:
   Bash: git push

Agent 2 (Cursor):
# Agent 2 pulls, sees assigned task
$ git pull
$ bd list --assignee agent-2
project-c5d6  open  Implement OAuth provider  [Priority: 1]

# Agent 2 works on task, completes, commits, pushes
$ bd update project-c5d6 --status in_progress
$ # Work on OAuth provider...
$ bd close project-c5d6 "OAuth provider implemented (supports GitHub, Google)"
$ git add .beads/issues.jsonl src/auth/oauth_provider.py
$ git commit -m "feat: Implement OAuth provider (beads: project-c5d6)"
$ git push

Agent 1 (Claude Code):
User: "Check task status"

Claude (Phase 3: Sync and Check - 0-5k tokens):
1. Pull updates:
   Bash: git pull
   # Beads auto-imports issues.jsonl
2. Check all tasks:
   Bash: bd list --json
3. Parse to find completed tasks:
   # project-c5d6: closed by agent-2

Claude (response to user):
"Task status updated:

Agent 2 (Cursor) completed:
✅ project-c5d6: Implement OAuth provider
   - Closed: 15 minutes ago
   - Note: OAuth provider implemented (GitHub, Google support)

Your tasks:
⏳ project-b2c4: Extract AuthProvider interface [READY]
⏳ project-d7e8: Write provider tests [BLOCKED by project-b2c4]

Next: Start project-b2c4 (AuthProvider interface)"

Result: Agents coordinate via git, no manual synchronization needed
```

---

### Workflow 5: Discovering Dependencies with Claude Code

```markdown
User: "Work on OAuth implementation"

Claude (Phase 1: Start Task - 0-5k tokens):
1. Update task status:
   Bash: bd update project-a3f8 --status in_progress

Claude (Phase 2: Implementation Work - 5-30k tokens):
2. Read implementation file:
   Read src/auth/oauth.py
3. Discover issue during work:
   # Notice: Authentication module poorly designed, needs refactor first

Claude (Phase 3: Create Blocker Task - 30-40k tokens):
4. Create refactor task:
   Bash: bd create "Refactor authentication module to support OAuth" --priority 0 --json
   # Returns: project-g3h4
5. Link discovered task:
   Bash: bd dep add project-g3h4 discovered-from project-a3f8
6. Add blocking relationship:
   Bash: bd dep add project-a3f8 blocks project-g3h4
7. Pause current task:
   Bash: bd update project-a3f8 --status open

Claude (Phase 4: Work on Blocker - 40-70k tokens):
8. Start blocker task:
   Bash: bd update project-g3h4 --status in_progress
9. Refactor authentication module:
   # Use Edit tool to refactor
10. Complete blocker:
    Bash: bd close project-g3h4 "Refactored to AuthProvider interface (supports OAuth, SAML)"

Claude (Phase 5: Resume Original Task - 70-80k tokens):
11. Check ready work:
    Bash: bd list --ready
    # project-a3f8 now unblocked ✅
12. Resume OAuth implementation:
    Bash: bd update project-a3f8 --status in_progress
13. Continue implementation with refactored module

Claude (response to user):
"Discovered dependency during OAuth implementation:

Blocker Found:
⚠️  Authentication module needs refactor to support OAuth

Actions Taken:
1. ✅ Created blocker task: project-g3h4 (Refactor auth module)
2. ✅ Linked: project-g3h4 discovered-from project-a3f8
3. ✅ Added dependency: project-a3f8 blocks project-g3h4
4. ✅ Completed refactor: AuthProvider interface implemented
5. ✅ Resumed: project-a3f8 now unblocked

OAuth implementation continuing with refactored authentication module."

Result: Dependency discovered dynamically, blocker resolved automatically
```

---

## Claude-Specific Tips

### Tip 1: Use Bash for All bd Commands

**Pattern**:
```bash
# Create task
Bash: bd create "Task title" --priority 0 --json

# List tasks
Bash: bd list --ready --json

# Update task
Bash: bd update <task-id> --status in_progress

# Close task
Bash: bd close <task-id> "Completion note"

# Add dependency
Bash: bd dep add <task-a-id> blocks <task-b-id>

# Show task details
Bash: bd show <task-id>
```

**Why**: Bash tool executes bd CLI commands, no other tool available for beads

---

### Tip 2: Always Use --json Flag for Programmatic Parsing

**Pattern**:
```bash
# List ready tasks with JSON output
Bash: bd list --ready --json

# Parse JSON (pseudo-code):
# output = {"issues": [{"id": "project-a3f8", "title": "...", ...}]}
# Extract first ready task ID: output["issues"][0]["id"]

# Create task with JSON output
Bash: bd create "New task" --json
# Parse: {"id": "project-b2c4", ...}
```

**Why**: JSON output easier to parse than human-readable text format

---

### Tip 3: Pull Before Querying in Multi-Agent Scenarios

**Pattern**:
```bash
# ALWAYS pull before querying tasks (multi-agent)
Bash: git pull
# Beads auto-imports issues.jsonl if newer than beads.db

# Then query tasks
Bash: bd list --ready --json
```

**Why**: Ensures Claude sees latest task state from other agents

---

### Tip 4: Commit issues.jsonl After Task Updates

**Pattern**:
```bash
# After creating/updating/closing tasks:
Bash: git add .beads/issues.jsonl
Bash: git commit -m "Add/update beads tasks"
Bash: git push
```

**Why**: Persists tasks for future sessions and other agents

---

### Tip 5: Use bd show for Task Context

**Pattern**:
```bash
# Before starting work, show task details
Bash: bd show <task-id>

# Output:
# ID: project-a3f8
# Title: Implement OAuth authentication
# Status: open
# Dependencies: blocks project-b2c4, project-c5d6
# Description: Add OAuth2 flow for GitHub authentication
```

**Why**: Provides full context before starting work

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Parsing JSON Output

**Problem**: Executing `bd list --json` but not extracting task IDs from JSON

**Fix**: Parse JSON output to extract task IDs programmatically

```bash
# BAD: Rely on human-readable output
Bash: bd list --ready

# GOOD: Use JSON for parsing
Bash: bd list --ready --json
# Parse: Extract "id" field from first issue in output
```

---

### Pitfall 2: Not Pulling Before Querying (Multi-Agent)

**Problem**: Querying tasks without pulling, missing other agents' updates

**Fix**: Always pull before querying in multi-agent scenarios

```bash
# ALWAYS pull first in multi-agent workflows
Bash: git pull
Bash: bd list --ready --json
```

---

### Pitfall 3: Creating Tasks Without Committing

**Problem**: Creating beads tasks but not committing issues.jsonl, tasks lost on context reset

**Fix**: Commit after creating/updating tasks

```bash
# After task operations:
Bash: git add .beads/issues.jsonl
Bash: git commit -m "Add/update beads tasks"
```

---

### Pitfall 4: Not Linking Dependencies

**Problem**: Creating main task and subtasks but not adding blocking relationships

**Fix**: Always add dependencies after creating related tasks

```bash
# After creating main task (project-a3f8) and subtasks (b2c4, c5d6):
Bash: bd dep add project-a3f8 blocks project-b2c4
Bash: bd dep add project-a3f8 blocks project-c5d6
```

---

### Pitfall 5: Using Beads for Trivial Tasks

**Problem**: Creating beads task for simple 1-step work, overhead not justified

**Fix**: Only use beads for complex (≥3 steps) or multi-session tasks

**Decision tree**:
- Complex (≥3 steps) OR multi-session → Use beads ✅
- Simple (1-2 steps) AND single session → Skip beads ❌

---

## Support & Resources

**SAP-015 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic beads workflows
- [Capability Charter](capability-charter.md) - Problem, solution, trade-offs
- [Protocol Spec](protocol-spec.md) - Beads CLI commands, schema
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide (5 min setup)
- [Ledger](ledger.md) - Adoption tracking, pilot results

**External Resources**:
- [Beads Project](https://github.com/yeggers/beads) - Official beads CLI repo
- [Beads Documentation](https://beads.dev) - Beads CLI reference
- Steve Yegge's Blog - Agent amnesia problem motivation

**Related SAPs**:
- [SAP-001 (inbox-protocol)](../inbox/) - Coordination tasks reference beads
- [SAP-010 (memory-system)](../memory-system/) - A-MEM events correlate with beads
- [SAP-009 (agent-awareness)](../agent-awareness/) - AGENTS.md includes beads patterns

**Templates**:
- `.beads/` directory structure - Created by `bd init`

---

## Version History

- **2.0.0** (2025-11-04): Initial CLAUDE.md for SAP-015
  - Claude Code workflows (initialization, task creation, session resumption, multi-agent coordination, dependency discovery)
  - Tool usage patterns (Bash for bd commands, JSON parsing, git pull sync, commit issues.jsonl)
  - Claude-specific tips (Bash for all commands, --json flag, pull before query, commit after updates, bd show for context)
  - Common pitfalls (no JSON parsing, no pull, no commit, no dependencies, trivial tasks)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic beads workflows
2. Review [protocol-spec.md](protocol-spec.md) for beads CLI specification
3. Check [capability-charter.md](capability-charter.md) for design trade-offs
4. Install beads: `npm install -g beads-cli@latest` → Initialize: `bd init` → Create first task
