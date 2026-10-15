---
name: minions-hermes-mission-control
description: Mission control Kanban board for managing and supervising autonomous Hermes Agent tasks
triggers:
  - "set up minions for hermes agent"
  - "create a kanban board for my ai agent tasks"
  - "how do I manage multiple hermes agent sessions"
  - "install minions mission control"
  - "supervise long-running agent tasks"
  - "track hermes agent work with a dashboard"
  - "run minions to manage ai agents"
  - "configure minions for task management"
---

# Minions Hermes Mission Control

> Skill by [ara.so](https://ara.so) — Hermes Skills collection

Minions is a web-based mission control interface for managing Hermes Agent tasks. It provides a Kanban board to create, supervise, and review autonomous agent work, with features like live streaming, completion judging, and human-in-the-loop verification.

## What It Does

- **Kanban Board**: Visual task management with columns for in-progress, review, and done
- **Autonomous Execution**: Agents work independently on tasks you define
- **Completion Judge**: Lightweight LLM evaluates task completion after each turn
- **Live Streaming**: Real-time view of tool calls, reasoning, and responses
- **Human Verification**: Tasks require your sign-off before moving to done
- **Routines**: Manage recurring Hermes jobs with history and output tracking
- **File Browser**: View agent-created workspace files
- **Local-First**: Self-hosted with SQLite, no cloud dependency

## Installation

**Prerequisites**: Node.js 18+ and [Hermes Agent](https://hermes-agent.nousresearch.com) installed

### Quick Start

```bash
npx minionsai
```

The server starts at `http://localhost:6969`

### Check Version

```bash
minions --version
npm view minionsai version
```

### Data Storage

- Local SQLite database created on first run
- All state stored in `~/.minions/`
- Chat transcripts in Hermes session database
- Task metadata in Minions SQLite

## Key Concepts

### Tasks

Each task is a persistent Hermes root session. Tasks move through Kanban columns:
- **Backlog**: Created but not started
- **In Progress**: Agent actively working
- **In Review**: Agent proposed completion
- **Done**: Human verified and closed

### Routines

Recurring Hermes jobs that can be scheduled and monitored. Minions tracks:
- Execution history
- Output files
- Success/failure status

### Per-Task Configuration

Each task can override:
- Model selection
- Reasoning effort level
- Workspace directory

## Configuration

### Environment Variables

```bash
# API keys for LLM providers (if using completion judge)
export OPENAI_API_KEY=your_openai_key
export ANTHROPIC_API_KEY=your_anthropic_key

# Custom port (default: 6969)
export MINIONS_PORT=8080

# Custom data directory (default: ~/.minions/)
export MINIONS_DATA_DIR=/path/to/data
```

### Settings Page

Access via web UI to configure:
- Default model for new tasks
- Default reasoning effort
- Completion judge settings
- Workspace paths

## Usage Patterns

### Creating a Task

1. Open Minions at `http://localhost:6969`
2. Click "New Task" or use the chat interface
3. Describe what you want the agent to do
4. Agent begins autonomous execution

### Monitoring Tasks

```typescript
// Tasks are displayed in real-time Kanban columns
// Watch live streaming output in the task detail view
// Completion judge runs after each agent turn
```

### Reviewing Completions

1. Agent moves task to "In Review" when it believes work is done
2. Review the chat transcript and outputs
3. Either:
   - Approve and move to "Done"
   - Send back with feedback for more work

### Creating Routines

```typescript
// Example: Daily website monitoring routine
{
  name: "Check competitor pricing",
  schedule: "0 9 * * *", // 9 AM daily
  prompt: "Visit competitor.com and extract current pricing, compare to yesterday",
  workspace: "./data/competitive-intel"
}
```

## Practical Examples

### Research Task

```typescript
// Task prompt:
"Research the top 10 AI coding assistants launched in 2025. 
Create a comparison table with: name, pricing, key features, GitHub stars.
Save as markdown in research/ai-coding-tools.md"

// Agent will:
// 1. Search for AI coding assistants
// 2. Visit documentation sites
// 3. Gather pricing and feature data
// 4. Format as markdown table
// 5. Save file and propose completion
```

### Data Collection Routine

```typescript
// Routine configuration:
{
  name: "Daily HackerNews trending",
  schedule: "0 */6 * * *", // Every 6 hours
  prompt: `
    1. Fetch top 30 HackerNews stories
    2. Extract: title, points, comments, URL
    3. Append to data/hn-trending.jsonl with timestamp
    4. If any story mentions 'AI agents', save separately to data/hn-ai-agents.jsonl
  `,
  workspace: "./scraped-data"
}
```

### Code Generation Task

```typescript
// Task prompt:
"Create a TypeScript function that:
- Takes an array of URLs
- Fetches each in parallel with retry logic
- Returns success/failure status for each
- Includes proper error handling and types
Save to src/utils/fetch-urls.ts with tests"

// Monitor live as agent:
// - Creates the implementation
// - Adds TypeScript types
// - Writes tests
// - Runs them to verify
```

### Content Pipeline

```typescript
// Multi-step task:
"1. Read all markdown files in content/drafts/
2. For each draft:
   - Check grammar with language tool
   - Generate 3 title alternatives
   - Create social media preview text
   - Move to content/ready/ when done
3. Create summary report in content/processing-report.md"
```

## CLI Commands

```bash
# Start Minions server
npx minionsai

# Start on custom port
MINIONS_PORT=3000 npx minionsai

# Check version
minions --version

# Clear all data (reset)
rm -rf ~/.minions/
```

## Integration with Hermes

Minions connects to your local Hermes Agent installation:

```typescript
// Minions creates Hermes sessions via API
// Each task = one persistent Hermes root session
// Sessions persist across Minions restarts
// Chat history stored in Hermes's database
```

### Hermes Session Mapping

```typescript
// Task metadata (Minions SQLite):
{
  id: "task_123",
  title: "Research AI tools",
  status: "in_progress",
  hermesSessionId: "sess_abc", // Reference to Hermes
  model: "claude-3-5-sonnet",
  reasoningEffort: "medium"
}

// Chat transcript: stored in Hermes session database
// File outputs: in workspace directory
```

## File Browser

View agent-created files:

```bash
# Files appear in the Minions UI file browser
# Organized by task workspace directory
# Download or view directly from UI
```

Example workspace structure:

```
~/.minions/
├── db.sqlite                 # Minions task metadata
└── workspaces/
    ├── task_123/             # Per-task workspace
    │   ├── output.json
    │   └── report.md
    └── task_456/
        └── data.csv
```

## Troubleshooting

### Minions won't start

```bash
# Check Node.js version
node --version  # Should be 18+

# Check if port is in use
lsof -i :6969

# Use different port
MINIONS_PORT=8080 npx minionsai
```

### Can't connect to Hermes

```bash
# Verify Hermes is running
# Check Hermes installation at https://hermes-agent.nousresearch.com

# Hermes typically runs on localhost
# Ensure firewall allows local connections
```

### Task stuck in progress

```typescript
// Use the UI to:
// 1. View live streaming output
// 2. Check if agent is waiting for input
// 3. Manually intervene via chat
// 4. Or cancel and restart the task
```

### Completion judge not working

```typescript
// Ensure LLM API key is set:
// export OPENAI_API_KEY=your_key

// Check Settings page for completion judge configuration
// Verify API quota/rate limits
```

### Database corruption

```bash
# Backup current data
cp -r ~/.minions/ ~/.minions.backup/

# Reset database
rm ~/.minions/db.sqlite

# Restart Minions (creates fresh database)
npx minionsai

# Note: Hermes session data is preserved
```

## Best Practices

### Task Prompts

```typescript
// ✅ Good: Specific, measurable outcomes
"Scrape product prices from 5 e-commerce sites, 
save to products.json with timestamp, 
compare to last week's data in products-history.json"

// ❌ Bad: Vague, no clear completion criteria
"Research some products"
```

### Workspace Organization

```bash
# Use task-specific workspaces
task_research/     # Research outputs
task_scraping/     # Scraped data
task_analysis/     # Analysis reports

# Reference files from prompts:
"Save output to ./results/summary-{date}.md"
```

### Routine Scheduling

```typescript
// Use cron syntax for schedules
"0 9 * * 1-5"   // 9 AM weekdays
"*/30 * * * *"  // Every 30 minutes
"0 0 * * 0"     // Weekly on Sunday

// Build in error recovery:
"If website is down, retry 3 times with 5-minute delays.
Log failures to errors.log"
```

## Advanced Usage

### Custom Completion Criteria

```typescript
// In task prompt, specify completion:
"Task is ONLY complete when:
1. All 50 URLs have been processed
2. results.json exists and is valid JSON
3. error_count in summary.md is 0
4. All output files are committed to git"
```

### Multi-Agent Workflows

```typescript
// Create dependent tasks:
// Task 1: "Scrape data, save to data/raw.json"
// Task 2: "Read data/raw.json, analyze, create report.md"
// Task 3: "Read report.md, generate executive summary"

// Monitor all on Kanban board
// Each progresses independently
```
