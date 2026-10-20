---
sap_id: SAP-015
version: 2.0.0
status: pilot
last_updated: 2025-11-05
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 12
progressive_loading:
  phase_1: "lines 1-100"    # Quick Reference + Common Workflows
  phase_2: "lines 101-250"  # Integration Patterns + CLI Reference
  phase_3: "full"           # Complete including troubleshooting
phase_1_token_estimate: 2500
phase_2_token_estimate: 5000
phase_3_token_estimate: 8500
tags:
  - task-tracking
  - beads
  - git-backed
  - multi-agent
  - pilot
---

# Agent Task Tracking (SAP-015) - Agent Awareness

**SAP ID**: SAP-015
**Version**: 2.0.0
**Status**: Pilot
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

This AGENTS.md provides: Agent-specific patterns for implementing SAP-015.
n.

---

## Detailed Quick Reference

### What is Agent Task Tracking?

**Agent Task Tracking** = Git-backed persistent task memory for AI agents using beads CLI

SAP-015 provides:
- Persistent task storage across sessions (`.beads/issues.jsonl`)
- Dependency tracking (blocks, related, parent-child)
- Ready-work detection (open issues with no blockers)
- Multi-agent coordination via git sync
- Hash-based IDs prevent collision (beads v0.20.1+)

### When to Use Agent Task Tracking

✅ **Use SAP-015 for**:
- Complex multi-step projects spanning multiple sessions
- Tracking dependencies between tasks (Task B blocks Task A)
- Multi-agent coordination (shared task visibility)
- Persistent memory after context resets
- Reducing session startup time (no need to re-establish context)

❌ **Don't use for**:
- Simple single-step tasks (overhead not justified)
- Projects with <3 tasks (manual tracking sufficient)
- Non-git repositories (beads requires git)
- Projects where external issue trackers are mandatory (GitHub Issues, Jira)

---

## Common Workflows

### Workflow 1: Initializing Beads in Repository

**Context**: New repository needs beads task tracking for agent coordination

**Steps**:
1. Check if beads installed:
   ```bash
   which bd
   # If not found: npm install -g beads-cli@latest
   ```

2. Initialize beads in repository:
   ```bash
   bd init
   # Auto-detects prefix from directory name (e.g., chora-base → chora-base-xxxx)
   ```

3. Verify initialization:
   ```bash
   ls .beads/
   # Expected: beads.db, issues.jsonl, config.yaml, metadata.json, .gitignore
   ```

4. Commit beads configuration:
   ```bash
   git add .beads/
   git commit -m "feat: Initialize beads task tracking (SAP-015)"
   ```

**Result**: Repository initialized with beads, agents can create/track tasks

**Example (chora-utils)**:
```markdown
Context: chora-utils needs agent task tracking for multi-session development

Step 1: Check beads
$ which bd
/usr/local/bin/bd  # Installed ✅

Step 2: Initialize
$ cd chora-utils
$ bd init
✓ Initialized beads repository
  Prefix: chora-utils
  Database: .beads/beads.db
  Issues: .beads/issues.jsonl

Step 3: Verify
$ ls .beads/
beads.db  issues.jsonl  config.yaml  metadata.json  .gitignore

Step 4: Commit
$ git add .beads/
$ git commit -m "feat: Initialize beads task tracking (SAP-015)"
```

**Outcome**: chora-utils ready for agent task tracking

---

### Workflow 2: Creating and Tracking Tasks

**Context**: Agent working on complex feature needs to track subtasks and dependencies

**Steps**:
1. Create main task:
   ```bash
   bd create "Implement OAuth authentication" --priority 0 --assignee agent-name
   # Returns: chora-utils-a3f8
   ```

2. Create dependent subtasks:
   ```bash
   bd create "Add OAuth config to settings" --priority 1
   # Returns: chora-utils-b2c4

   bd create "Implement OAuth callback handler" --priority 1
   # Returns: chora-utils-c5d6
   ```

3. Add dependencies (subtasks block main task):
   ```bash
   bd dep add chora-utils-a3f8 blocks chora-utils-b2c4
   bd dep add chora-utils-a3f8 blocks chora-utils-c5d6
   ```

4. Query ready work (tasks with no blockers):
   ```bash
   bd list --ready
   # Shows: chora-utils-b2c4, chora-utils-c5d6 (main task blocked)
   ```

5. Work on first subtask:
   ```bash
   bd update chora-utils-b2c4 --status in_progress
   # Complete work...
   bd close chora-utils-b2c4 "Config added to settings.py"
   ```

6. Check ready work again:
   ```bash
   bd list --ready
   # Shows: chora-utils-c5d6 (first subtask done)
   # After c5d6 complete: Shows chora-utils-a3f8 (main task unblocked)
   ```

**Result**: Complex feature tracked with dependencies, agent knows what's ready to work on

**Example (OAuth feature)**:
```markdown
Context: Implementing OAuth feature with 3 subtasks

Step 1: Create main task
$ bd create "Implement OAuth authentication" --priority 0 --assignee claude-code
chora-utils-a3f8

Step 2: Create subtasks
$ bd create "Add OAuth config to settings"
chora-utils-b2c4
$ bd create "Implement OAuth callback handler"
chora-utils-c5d6
$ bd create "Write OAuth integration tests"
chora-utils-d7e8

Step 3: Add dependencies
$ bd dep add chora-utils-a3f8 blocks chora-utils-b2c4
$ bd dep add chora-utils-a3f8 blocks chora-utils-c5d6
$ bd dep add chora-utils-a3f8 blocks chora-utils-d7e8

Step 4: Query ready work
$ bd list --ready
chora-utils-b2c4  open  Add OAuth config to settings
chora-utils-c5d6  open  Implement OAuth callback handler
chora-utils-d7e8  open  Write OAuth integration tests
# Main task NOT shown (blocked by subtasks)

Step 5: Complete first subtask
$ bd update chora-utils-b2c4 --status in_progress
$ # Work on config...
$ bd close chora-utils-b2c4 "Added OAuth settings (client_id, secret, redirect_uri)"

Step 6: After all subtasks complete
$ bd list --ready
chora-utils-a3f8  open  Implement OAuth authentication  # Unblocked ✅
```

**Outcome**: Agent systematically completes subtasks, main task automatically unblocked

---

### Workflow 3: Session Resumption with Beads

**Context**: Agent context reset, need to resume work from previous session

**Steps**:
1. Sync with git (in case other agents updated tasks):
   ```bash
   git pull
   # Beads auto-imports .beads/issues.jsonl if newer than beads.db
   ```

2. Check what's ready to work on:
   ```bash
   bd list --ready --json
   # Agent parses JSON output to find next task
   ```

3. Check in-progress tasks:
   ```bash
   bd list --status in_progress
   # Resume incomplete work
   ```

4. Review task details:
   ```bash
   bd show <task-id>
   # See description, dependencies, metadata
   ```

5. Continue work:
   ```bash
   bd update <task-id> --status in_progress
   # Complete task...
   bd close <task-id> "Completed <description>"
   ```

**Result**: Agent resumes work seamlessly, no manual context re-establishment needed

**Example (session resumption)**:
```markdown
Context: Agent session restarted, need to resume OAuth feature work

Step 1: Sync with git
$ git pull
remote: Already up to date.
# Beads auto-imports issues.jsonl (no changes)

Step 2: Check ready work
$ bd list --ready
chora-utils-c5d6  open  Implement OAuth callback handler
chora-utils-d7e8  open  Write OAuth integration tests

Step 3: Check in-progress (from previous session)
$ bd list --status in_progress
# Empty (previous session completed b2c4)

Step 4: Review next task
$ bd show chora-utils-c5d6
ID: chora-utils-c5d6
Title: Implement OAuth callback handler
Status: open
Priority: 1
Assignee: claude-code
Dependencies: None (ready to work)
Description: Add /oauth/callback endpoint to handle OAuth redirect

Step 5: Start work
$ bd update chora-utils-c5d6 --status in_progress
# Implement callback handler...
$ bd close chora-utils-c5d6 "Callback handler implemented in routes/oauth.py"
```

**Outcome**: Agent resumes work in <1 minute, no context loss

---

### Workflow 4: Multi-Agent Coordination

**Context**: Multiple agents working on same repository, need shared task visibility

**Steps**:
1. Agent 1 creates tasks:
   ```bash
   bd create "Fix authentication bug" --assignee agent-1
   bd create "Add rate limiting" --assignee agent-2
   ```

2. Agent 1 commits and pushes:
   ```bash
   git add .beads/issues.jsonl
   git commit -m "Add tasks for authentication and rate limiting"
   git push
   ```

3. Agent 2 pulls changes:
   ```bash
   git pull
   # Beads auto-imports issues.jsonl, updates SQLite DB
   ```

4. Agent 2 queries assigned tasks:
   ```bash
   bd list --assignee agent-2
   # Shows: Add rate limiting
   ```

5. Agent 2 updates task:
   ```bash
   bd update <task-id> --status in_progress
   # Work on task...
   bd close <task-id> "Rate limiting implemented"
   ```

6. Agent 2 commits and pushes:
   ```bash
   git add .beads/issues.jsonl
   git commit -m "Complete rate limiting task"
   git push
   ```

7. Agent 1 pulls to see updates:
   ```bash
   git pull
   # Sees agent-2's completed task
   ```

**Result**: Agents coordinate via git, shared task visibility without central server

**Example (parallel feature development)**:
```markdown
Context: Agent 1 works on auth, Agent 2 works on rate limiting

Agent 1 (Machine 1):
$ bd create "Fix authentication bug" --assignee agent-1 --priority 0
chora-utils-e9f0
$ bd create "Add rate limiting" --assignee agent-2 --priority 1
chora-utils-f1g2
$ git add .beads/issues.jsonl
$ git commit -m "Add tasks for auth and rate limiting"
$ git push

Agent 2 (Machine 2):
$ git pull
remote: 2 new commits
# Beads auto-imports issues.jsonl
$ bd list --assignee agent-2
chora-utils-f1g2  open  Add rate limiting  [Priority: 1]

$ bd update chora-utils-f1g2 --status in_progress
$ # Implement rate limiting...
$ bd close chora-utils-f1g2 "Implemented token bucket rate limiter"

$ git add .beads/issues.jsonl
$ git commit -m "Complete rate limiting (token bucket algorithm)"
$ git push

Agent 1 (Machine 1):
$ git pull
remote: 1 new commit
# Beads auto-imports issues.jsonl
$ bd list --status closed
chora-utils-f1g2  closed  Add rate limiting  [Closed by: agent-2]
```

**Outcome**: Agents coordinate without manual sync, git provides task distribution

---

### Workflow 5: Discovering and Linking Related Tasks

**Context**: Agent working on task, discovers related subtask or dependency

**Steps**:
1. Agent working on task A:
   ```bash
   bd update <task-a-id> --status in_progress
   ```

2. Discover new task B while working:
   ```bash
   bd create "Refactor authentication module" --priority 2
   # Returns: <task-b-id>
   ```

3. Link task B to task A (discovered-from relationship):
   ```bash
   bd dep add <task-b-id> discovered-from <task-a-id>
   ```

4. If task B blocks task A:
   ```bash
   bd dep add <task-a-id> blocks <task-b-id>
   bd update <task-a-id> --status open  # Unblock current task
   ```

5. Work on task B first:
   ```bash
   bd update <task-b-id> --status in_progress
   # Complete task B...
   bd close <task-b-id> "Authentication module refactored"
   ```

6. Resume task A (now unblocked):
   ```bash
   bd update <task-a-id> --status in_progress
   # Continue original work...
   ```

**Result**: Discovered dependencies tracked, agent systematically handles blockers

**Example (discovered dependency)**:
```markdown
Context: Working on "Add OAuth support", discover auth module needs refactor

Step 1: Working on OAuth
$ bd update chora-utils-a3f8 --status in_progress
# Working on OAuth implementation...
# Discover: Authentication module poorly designed, must refactor first

Step 2: Create refactor task
$ bd create "Refactor authentication module to support OAuth" --priority 0
chora-utils-g3h4

Step 3: Link discovered task
$ bd dep add chora-utils-g3h4 discovered-from chora-utils-a3f8

Step 4: Add blocking relationship
$ bd dep add chora-utils-a3f8 blocks chora-utils-g3h4
$ bd update chora-utils-a3f8 --status open  # Pause OAuth work

Step 5: Work on refactor first
$ bd update chora-utils-g3h4 --status in_progress
$ # Refactor authentication module...
$ bd close chora-utils-g3h4 "Refactored to AuthProvider interface (supports OAuth, SAML)"

Step 6: Resume OAuth (unblocked)
$ bd list --ready
chora-utils-a3f8  open  Implement OAuth authentication  # Unblocked ✅
$ bd update chora-utils-a3f8 --status in_progress
# Continue OAuth implementation with refactored auth module...
```

**Outcome**: Dependency discovered dynamically, blocker resolved before continuing

---

## Beads Command Reference

### Initialization

```bash
# Initialize beads (auto-detect prefix from directory name)
bd init

# Initialize with custom prefix
bd init --prefix myproject

# Initialize with separate branch (for protected main)
bd init --branch beads-metadata
```

### Task Creation

```bash
# Create basic issue
bd create "Fix bug in authentication"

# Create with full metadata
bd create "Add OAuth support" \
  --priority 0 \
  --type feature \
  --assignee agent-name \
  --description "Implement OAuth2 flow for GitHub"

# Create with JSON output (agent-friendly)
bd create "Write tests" --json
```

### Querying Tasks

```bash
# List all issues
bd list

# List ready work (no blockers)
bd list --ready

# List by status
bd list --status open
bd list --status in_progress
bd list --status closed

# List by assignee
bd list --assignee agent-name

# List with JSON output
bd list --json
```

### Updating Tasks

```bash
# Update status
bd update <task-id> --status in_progress
bd update <task-id> --status open

# Update priority
bd update <task-id> --priority 0

# Update assignee
bd update <task-id> --assignee new-agent
```

### Closing Tasks

```bash
# Close task
bd close <task-id>

# Close with resolution note
bd close <task-id> "Implemented OAuth callback handler"
```

### Dependency Management

```bash
# Add dependency (task-a blocks task-b)
bd dep add <task-a-id> blocks <task-b-id>

# Add related link
bd dep add <task-a-id> related <task-b-id>

# Add parent-child relationship
bd dep add <parent-id> parent <child-id>

# Add discovered-from link
bd dep add <new-task-id> discovered-from <original-task-id>

# Remove dependency
bd dep rm <task-a-id> blocks <task-b-id>
```

### Task Details

```bash
# Show full task details
bd show <task-id>

# Show with JSON output
bd show <task-id> --json
```

---

## Integration with Other SAPs

### Integration with SAP-001 (Inbox Protocol)

**Pattern**: Coordination tasks can reference beads issue IDs

**Workflow**:
1. Agent creates beads issue for implementation task
2. Coordination event in inbox references beads issue ID
3. Inbox event provides high-level coordination, beads tracks detailed subtasks

**Example**:
```jsonl
# inbox/coordination/events.jsonl
{"type":"request","source":"maintainer","timestamp":"2025-11-04T10:00:00Z","data":{"action":"implement-oauth","beads_issue":"chora-utils-a3f8"}}

# .beads/issues.jsonl
{"id":"chora-utils-a3f8","title":"Implement OAuth authentication","status":"in_progress",...}
```

**Outcome**: High-level coordination (inbox) + detailed task tracking (beads)

---

### Integration with SAP-010 (Memory System / A-MEM)

**Pattern**: A-MEM events correlate with beads task IDs for traceability

**Workflow**:
1. Agent creates beads task
2. Agent work generates A-MEM events (file changes, decisions)
3. A-MEM events include beads task ID in metadata
4. Traceability: A-MEM events → beads tasks → outcomes

**Example**:
```json
// A-MEM event with beads correlation
{
  "timestamp": "2025-11-04T10:15:00Z",
  "type": "implementation",
  "action": "edit_file",
  "file": "src/auth/oauth.py",
  "beads_task_id": "chora-utils-a3f8"
}
```

**Outcome**: A-MEM provides "what was done", beads provides "what to do"

---

### Integration with SAP-009 (Agent Awareness)

**Pattern**: AGENTS.md files include beads workflow patterns

**Workflow**:
1. Agent reads AGENTS.md for capability
2. AGENTS.md includes beads query patterns
3. Agent creates/updates beads tasks during implementation
4. Beads provides persistent context across sessions

**Outcome**: Agent awareness files guide beads usage for task tracking

---

## Common Pitfalls

### Pitfall 1: Not Syncing Before Querying (Multi-Agent)

**Problem**: Agent queries local tasks without pulling latest changes, misses other agents' updates

**Fix**:
```bash
# ALWAYS pull before querying in multi-agent scenarios
git pull  # Beads auto-imports issues.jsonl
bd list --ready
```

**Impact**: Prevents duplicate work, ensures agents see latest task state

---

### Pitfall 2: Creating Tasks Without Dependencies

**Problem**: Creating subtasks but not linking dependencies, agent can't detect ready work

**Fix**:
```bash
# After creating main task and subtasks, ALWAYS link dependencies
bd dep add <main-task-id> blocks <subtask-1-id>
bd dep add <main-task-id> blocks <subtask-2-id>

# Verify dependencies
bd show <main-task-id>
```

**Impact**: Enables automatic ready-work detection

---

### Pitfall 3: Not Committing issues.jsonl

**Problem**: Creating tasks locally but not committing, other agents/sessions don't see tasks

**Fix**:
```bash
# After creating/updating tasks, ALWAYS commit and push
git add .beads/issues.jsonl
git commit -m "Add/update beads tasks"
git push
```

**Impact**: Ensures tasks persist across sessions and agents

---

### Pitfall 4: Using Beads for Simple Single-Step Tasks

**Problem**: Creating beads task for trivial work (1 step, <5 min), overhead not justified

**Fix**: Only use beads for complex tasks with ≥3 steps or cross-session work

**Decision tree**:
- Complex (≥3 steps) OR multi-session → Use beads ✅
- Simple (1-2 steps) AND single session → Skip beads ❌

---

### Pitfall 5: Not Checking Ready Work Before Starting New Task

**Problem**: Starting new task without checking dependencies, work blocked by unfinished dependencies

**Fix**:
```bash
# ALWAYS check ready work before starting
bd list --ready

# If task not in ready list, check dependencies
bd show <task-id>  # See what's blocking
```

**Impact**: Prevents working on blocked tasks, prioritizes unblocked work

---

## Support & Resources

**SAP-015 Documentation**:
- [Capability Charter](capability-charter.md) - Problem, solution, trade-offs, outcomes
- [Protocol Spec](protocol-spec.md) - Beads CLI commands, schema, workflows
- [CLAUDE.md](CLAUDE.md) - Claude Code-specific beads automation
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide (5 min setup)
- [Ledger](ledger.md) - Adoption tracking, pilot results

**External Resources**:
- [Beads Project](https://github.com/yeggers/beads) - Official beads CLI repo
- [Beads Documentation](https://beads.dev) - Beads CLI reference
- Steve Yegge's Blog - Agent amnesia problem motivation

**Related SAPs**:
- [SAP-001 (inbox-protocol)](../inbox/) - Coordination tasks reference beads
- [SAP-010 (memory-system)](../memory-system/) - A-MEM events correlate with beads tasks
- [SAP-009 (agent-awareness)](../agent-awareness/) - AGENTS.md includes beads patterns

**Templates**:
- `.beads/` directory structure - Created by `bd init`
- Integration scripts - `beads-init.py`, `beads-sync.py` (future)

---

## Version History

- **2.0.0** (2025-11-04): Phase 2 format migration - Generic workflows for SAP-015
  - 5 common workflows (initialization, task creation, session resumption, multi-agent coordination, dependency discovery)
  - Beads command reference (init, create, list, update, close, dep, show)
  - Integration with SAP-001 (inbox), SAP-010 (memory), SAP-009 (awareness)
  - 5 common pitfalls (no sync, no dependencies, no commit, simple tasks, ignore ready work)

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific beads automation patterns
2. Review [protocol-spec.md](protocol-spec.md) for detailed beads CLI specification
3. Check [capability-charter.md](capability-charter.md) for design trade-offs and rationale
4. Install beads: `npm install -g beads-cli@latest` → Initialize: `bd init` → Create first task
