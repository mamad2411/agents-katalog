---
name: hermes-agent-mission-control
description: Mission control Kanban interface for managing autonomous Hermes Agent tasks, routines, and workflows
triggers:
  - "set up minions mission control for hermes agent"
  - "create a kanban board for hermes tasks"
  - "manage multiple hermes agent sessions"
  - "track autonomous agent work with minions"
  - "install hermes mission control interface"
  - "organize hermes agent tasks in a board"
  - "run minions for hermes agent management"
  - "set up task supervision for hermes"
---

# Hermes Agent Mission Control

> Skill by [ara.so](https://ara.so) — Hermes Skills collection

Minions is a mission control interface for Hermes Agent that provides a Kanban board to create, supervise, and review autonomous work. It solves the problem of juggling multiple terminal sessions and losing track of long-running tasks by providing a visual board with task status (in progress, in review, done), live streaming of agent work, and human-in-the-loop verification.

## Installation

**Prerequisites:** Node.js 18+ and [Hermes Agent](https://hermes-agent.nousresearch.com)

Quick start with npx (no installation required):

```bash
npx minionsai
```

Or install globally:

```bash
npm install -g minionsai
```

Then run:

```bash
minions
```

The server starts on `http://localhost:6969` by default.

## Data Storage

Minions creates a local SQLite database on first run:

- Database and state stored in `~/.minions/`
- Chat transcripts live in Hermes's session database
- Task metadata, status, and settings stored in Minions SQLite DB
- Completely local-first by default (no cloud dependency)

## CLI Commands

```bash
# Start the server
minions

# Check version
minions --version

# Compare with latest NPM version
npm view minionsai version
```

## Key Features & Usage

### Task Management

Each task in Minions is a persistent Hermes root session:

1. **Create tasks**: Describe what you want in chat
2. **Autonomous execution**: Agent decides how to get it done
3. **Live streaming**: Watch tool calls, reasoning, and responses in real-time
4. **Completion judge**: Lightweight LLM evaluates whether task is done after each turn
5. **Human verification**: Review agent's proposed completion before moving to "Done"

### Kanban Board States

- **In Progress**: Tasks actively being worked on
- **In Review**: Tasks completed by agent, awaiting human verification
- **Done**: Verified and closed tasks

### Per-Task Configuration

Override model and reasoning settings on individual tasks:

```typescript
// Task metadata structure
interface Task {
  id: string;
  title: string;
  description: string;
  status: 'in_progress' | 'in_review' | 'done';
  sessionId: string; // Hermes session ID
  model?: string; // Override default model
  reasoningEffort?: number; // Override reasoning effort
  createdAt: string;
  updatedAt: string;
}
```

### Routines

Create and manage recurring Hermes jobs:

- Schedule regular agent tasks
- Track execution history
- Review output from each run
- Useful for monitoring, data collection, reporting

### File Browser

View files created by agents in the workspace directory without leaving the interface.

## Configuration

Check settings in the web UI Settings page:

- View running Minions server version
- Configure Hermes Agent connection
- Set default model and reasoning effort
- Manage workspace directory path

## Architecture

Minions is built with TypeScript and uses:

- SQLite for local task metadata storage
- Hermes Agent sessions for chat transcripts
- Real-time WebSocket connections for live streaming
- Kanban board UI for task visualization

```typescript
// Example: Task state transitions
// 1. User creates task → status: 'in_progress'
// 2. Agent completes work → status: 'in_review'
// 3. Human verifies → status: 'done'

// The completion judge runs after each agent turn
interface CompletionCheck {
  isComplete: boolean;
  reasoning: string;
  confidence: number;
}
```

## Common Patterns

### Delegating Long-Running Work

```bash
# Start Minions
npx minionsai

# In the web UI:
# 1. Create new task: "Research top 10 AI tools launched this month"
# 2. Walk away - agent executes autonomously
# 3. Return later to review in "In Review" column
# 4. Verify and move to "Done"
```

### Managing Multiple Projects

```typescript
// Each task is independent:
// - Separate Hermes session
// - Independent model/effort settings
// - Parallel execution supported

// Example workflow:
// Task 1: "Write blog post about TypeScript 5.4 features"
// Task 2: "Analyze competitor pricing pages"
// Task 3: "Generate test data for user onboarding flow"
// All run concurrently, visible on one board
```

### Routine Monitoring

```bash
# Set up daily routine:
# "Check GitHub stars and create summary report"

# Minions will:
# 1. Execute on schedule
# 2. Store execution history
# 3. Make output reviewable
# 4. Alert if intervention needed (roadmap feature)
```

## Integration with Hermes Agent

Minions acts as a control layer over Hermes:

```typescript
// Minions doesn't replace Hermes CLI usage
// It complements it by providing:
// - Visual task organization
// - Persistent session management
// - Completion detection
// - Human review workflow

// You can still use Hermes directly:
hermes chat "quick question"

// Or use Minions for longer work:
// Create task in UI → Minions manages Hermes session
```

## Troubleshooting

### Port Already in Use

```bash
# Default port is 6969
# If occupied, check for existing Minions process:
lsof -i :6969
kill -9 <PID>

# Then restart
npx minionsai
```

### Database Issues

```bash
# Database location
ls -la ~/.minions/

# Reset database (WARNING: deletes all tasks)
rm -rf ~/.minions/
npx minionsai  # Creates fresh database
```

### Connection to Hermes Agent

Ensure Hermes Agent is properly installed and accessible:

```bash
# Verify Hermes installation
which hermes
hermes --version

# Check Hermes can start sessions
hermes chat "test"
```

### Task Stuck in "In Progress"

- Check Hermes session logs for errors
- Review agent's last output in live stream
- Manually intervene in chat
- Adjust model/reasoning effort settings
- Close and recreate task if necessary

## Hosted Option

Self-hosting is recommended for privacy, but a hosted option is available at [Agent37](https://www.agent37.com).

## Limitations

- Currently Hermes-only (OpenClaw adapter planned)
- Notifications not yet implemented (roadmap)
- Skills library not yet available (roadmap)
