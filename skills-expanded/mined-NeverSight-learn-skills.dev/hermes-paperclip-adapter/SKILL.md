---
name: hermes-paperclip-adapter
description: Integrate Hermes Agent as a managed AI employee in Paperclip companies with full tool access, persistent memory, and skill sync
triggers:
  - "set up hermes agent with paperclip"
  - "integrate hermes into my paperclip company"
  - "configure hermes paperclip adapter"
  - "run hermes as a paperclip employee"
  - "connect hermes agent to paperclip orchestration"
  - "deploy hermes with paperclip management"
  - "add hermes agent to my paperclip team"
  - "manage hermes sessions in paperclip"
---

# Hermes Paperclip Adapter

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

The Hermes Paperclip Adapter runs [Hermes Agent](https://github.com/NousResearch/hermes-agent) as a managed AI employee inside a [Paperclip](https://paperclip.ing) company. It provides full integration between Paperclip's orchestration/task system and Hermes's 30+ native tools, persistent memory, 80+ skills, and MCP support across 8 inference providers.

## What It Does

- **Runs Hermes as a Paperclip employee**: Assign issues to Hermes agents, they wake up on heartbeats and comments, complete work, and report back
- **Persistent session management**: Sessions resume across heartbeats, maintaining conversation context and memory
- **Structured transcript parsing**: Converts raw Hermes stdout into typed `TranscriptEntry` objects for proper UI rendering (tool cards, status icons)
- **Skills sync**: Merges Paperclip-managed skills with Hermes-native `~/.hermes/skills/` for unified skill management
- **Multi-provider**: Supports Anthropic, OpenRouter, OpenAI, Nous, OpenAI Codex, ZAI, Kimi Coding, MiniMax
- **Comment-driven wakes**: Agents respond to issue comments, not just task assignments
- **Cost tracking**: Captures token usage and costs from Hermes output

## Installation

### 1. Install Prerequisites

```bash
# Install Hermes Agent
pip install hermes-agent

# Verify installation
hermes --version
```

### 2. Install the Adapter

```bash
npm install hermes-paperclip-adapter
```

### 3. Register in Paperclip Server

Edit your Paperclip server's adapter registry (`server/src/adapters/registry.ts`):

```typescript
import * as hermesLocal from "hermes-paperclip-adapter";
import {
  execute,
  testEnvironment,
  detectModel,
  listSkills,
  syncSkills,
  sessionCodec,
} from "hermes-paperclip-adapter/server";

// In your registry setup
registry.set("hermes_local", {
  ...hermesLocal,
  execute,
  testEnvironment,
  detectModel,
  listSkills,
  syncSkills,
  sessionCodec,
});
```

## Configuration

### Basic Agent Config

Create a Hermes agent in Paperclip with `adapterType: "hermes_local"`:

```typescript
const agentConfig = {
  name: "Hermes Engineer",
  adapterType: "hermes_local",
  adapterConfig: {
    // Model selection (provider/model format)
    model: "anthropic/claude-sonnet-4",
    
    // Execution limits
    maxIterations: 50,
    timeoutSec: 300,
    graceSec: 10,
    
    // Session persistence
    persistSession: true,
    
    // Tool control
    enabledToolsets: ["terminal", "file", "web", "browser"],
    
    // Workspace isolation
    worktreeMode: false,
    checkpoints: false,
    
    // Output control
    verbose: false,
    quiet: true
  }
};
```

### Provider Configuration

The adapter auto-detects providers from model names:

```typescript
// Anthropic
{ model: "anthropic/claude-sonnet-4" }
{ model: "anthropic/claude-opus-4" }

// OpenRouter
{ model: "openrouter/anthropic/claude-3.5-sonnet" }
{ model: "openrouter/deepseek/deepseek-chat" }

// OpenAI
{ model: "openai/gpt-4" }
{ model: "openai/o1" }

// Nous
{ model: "nous/hermes-3" }

// Explicit provider override
{ 
  model: "claude-sonnet-4",
  provider: "anthropic"
}
```

Set API keys via environment variables:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export OPENROUTER_API_KEY=sk-or-...
export OPENAI_API_KEY=sk-...
export NOUS_API_KEY=...
```

### Toolset Control

Restrict available tools by specifying toolsets:

```typescript
{
  // Only terminal, file, and web tools
  enabledToolsets: ["terminal", "file", "web"]
}

{
  // Enable MCP and vision
  enabledToolsets: ["mcp", "vision"]
}

{
  // Empty = all tools enabled (default)
  enabledToolsets: []
}
```

Available toolsets: `terminal`, `file`, `web`, `browser`, `code_execution`, `vision`, `mcp`, `creative`, `productivity`

### Custom Prompts

Use template variables to customize agent instructions:

```typescript
{
  promptTemplate: `You are {{agentName}}, an AI engineer working for {{companyName}}.

{{#taskId}}
## Current Task
**{{taskTitle}}** (ID: {{taskId}})

{{taskBody}}

Complete this task using your available tools. When done, report results clearly.
{{/taskId}}

{{#commentId}}
## New Comment
You've been mentioned in a comment. Review the issue context and respond appropriately.
{{/commentId}}

Project: {{projectName}}
Company ID: {{companyId}}
Run ID: {{runId}}
API: {{paperclipApiUrl}}
`
}
```

Available variables:
- `{{agentId}}`, `{{agentName}}`
- `{{companyId}}`, `{{companyName}}`
- `{{runId}}`, `{{taskId}}`, `{{taskTitle}}`, `{{taskBody}}`
- `{{projectName}}`, `{{commentId}}`, `{{wakeReason}}`
- `{{paperclipApiUrl}}`

Conditionals:
- `{{#taskId}}...{{/taskId}}` — only when task assigned
- `{{#noTask}}...{{/noTask}}` — only when no task
- `{{#commentId}}...{{/commentId}}` — only when woken by comment

## Usage Patterns

### Creating a Hermes Employee

```typescript
import { PaperclipClient } from "paperclip-client";

const client = new PaperclipClient({
  apiUrl: process.env.PAPERCLIP_API_URL,
  apiKey: process.env.PAPERCLIP_API_KEY
});

// Create agent
const agent = await client.agents.create({
  name: "Hermes DevOps",
  adapterType: "hermes_local",
  adapterConfig: {
    model: "anthropic/claude-sonnet-4",
    maxIterations: 50,
    timeoutSec: 600,
    persistSession: true,
    enabledToolsets: ["terminal", "file", "web"],
    env: {
      // Custom env vars for Hermes
      HERMES_LOG_LEVEL: "info"
    }
  },
  schedule: {
    cron: "*/15 * * * *" // Check every 15 minutes
  }
});

console.log(`Created agent: ${agent.id}`);
```

### Assigning Work

```typescript
// Create an issue
const issue = await client.issues.create({
  title: "Optimize database queries",
  body: `Review the API endpoint /api/users and optimize the database queries.
  
Current query time is ~500ms, target is <100ms.
  
Files:
- src/api/users.ts
- src/db/queries/users.ts
  
Run benchmarks before and after changes.`,
  projectId: "proj_123"
});

// Assign to Hermes
await client.issues.assign({
  issueId: issue.id,
  agentId: agent.id
});
```

### Monitoring Execution

```typescript
// Get run details
const run = await client.runs.get(runId);

console.log(`Status: ${run.status}`);
console.log(`Model: ${run.modelUsed}`);
console.log(`Tokens: ${run.tokenUsage.total}`);
console.log(`Cost: $${run.cost}`);
console.log(`Session: ${run.sessionId}`);

// View transcript
for (const entry of run.transcript) {
  console.log(`[${entry.type}] ${entry.content}`);
  
  if (entry.type === "tool_use") {
    console.log(`  Tool: ${entry.toolName}`);
    console.log(`  Status: ${entry.status}`);
  }
}
```

### Skills Management

```typescript
import { listSkills, syncSkills } from "hermes-paperclip-adapter/server";

// List all available skills
const skills = await listSkills({
  agentId: "agent_123",
  companyId: "company_456"
});

console.log("Paperclip-managed skills:", skills.managed.length);
console.log("Hermes-native skills:", skills.native.length);

// Sync skills from Paperclip to Hermes workspace
await syncSkills({
  agentId: "agent_123",
  companyId: "company_456",
  enabledSkills: ["typescript-expert", "postgres-tuning", "docker-ops"]
});
```

### Testing Environment

```typescript
import { testEnvironment } from "hermes-paperclip-adapter/server";

const check = await testEnvironment({
  hermesCommand: "hermes",
  provider: "anthropic",
  env: {
    ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY
  }
});

if (!check.success) {
  console.error("Environment issues:", check.errors);
  // Example errors:
  // - "Hermes CLI not found in PATH"
  // - "Python version 3.10+ required"
  // - "ANTHROPIC_API_KEY not set"
}
```

### Auto Model Detection

```typescript
import { detectModel } from "hermes-paperclip-adapter/server";

// Reads ~/.hermes/config.yaml to pre-populate UI
const detected = await detectModel({
  hermesCommand: "hermes"
});

console.log(`Default model: ${detected.model}`);
console.log(`Provider: ${detected.provider}`);
```

### Session State Management

```typescript
import { sessionCodec } from "hermes-paperclip-adapter/server";

// Validate and migrate session state
const validated = sessionCodec.decode(rawSessionState);

if (validated._tag === "Right") {
  const session = validated.right;
  console.log(`Session ID: ${session.sessionId}`);
  console.log(`Messages: ${session.messageCount}`);
  console.log(`Last activity: ${session.lastActivity}`);
} else {
  console.error("Invalid session state:", validated.left);
}
```

## Advanced Patterns

### Git Worktree Isolation

Isolate agent work in separate git worktrees:

```typescript
{
  worktreeMode: true,
  // Each run gets: repo/.paperclip/worktrees/agent_123/run_456
}
```

### Filesystem Checkpoints

Enable rollback safety:

```typescript
{
  checkpoints: true,
  // Creates snapshots before destructive operations
}
```

### Reasoning Effort Control

For o1/o3-style thinking models:

```typescript
{
  model: "openai/o1",
  extraArgs: ["--reasoning-effort", "high"]
}
```

### Custom Hermes CLI Path

```typescript
{
  hermesCommand: "/usr/local/bin/hermes-dev",
  verbose: true
}
```

### Extra Environment Variables

```typescript
{
  env: {
    HERMES_LOG_LEVEL: "debug",
    HERMES_CACHE_DIR: "/mnt/fast-storage/hermes-cache",
    MCP_SERVER_URL: "http://localhost:8080"
  }
}
```

## Transcript Parsing

The adapter converts raw Hermes output into structured entries:

```typescript
type TranscriptEntry = 
  | { type: "message"; role: "user" | "assistant"; content: string }
  | { type: "tool_use"; toolName: string; status: "running" | "success" | "error"; input: any; output?: any }
  | { type: "thinking"; content: string }
  | { type: "memory_write"; key: string; value: any }
  | { type: "error"; message: string; stderr?: string };

// Example parsed output
[
  { type: "message", role: "user", content: "Optimize the database queries" },
  { type: "tool_use", toolName: "read_file", status: "success", input: { path: "src/api/users.ts" } },
  { type: "thinking", content: "The current query uses a full table scan..." },
  { type: "tool_use", toolName: "run_command", status: "running", input: { command: "npm run benchmark" } },
  { type: "tool_use", toolName: "run_command", status: "success", output: "Average: 487ms" },
  { type: "memory_write", key: "baseline_perf", value: "487ms" },
  { type: "message", role: "assistant", content: "I've added an index on user_id..." }
]
```

## Output Post-Processing

The adapter cleans Hermes ASCII formatting:

**Before (raw Hermes output):**
```
╔═══════════════════════════════════════╗
║       HERMES AGENT v2.1.0             ║
╚═══════════════════════════════════════╝

Results
=======

+---------------------------+----------+
| Metric                    | Value    |
+---------------------------+----------+
| Query time (before)       | 487ms    |
| Query time (after)        | 83ms     |
+---------------------------+----------+
```

**After (clean GFM markdown):**
```markdown
# Results

| Metric | Value |
|--------|-------|
| Query time (before) | 487ms |
| Query time (after) | 83ms |
```

## Troubleshooting

### Hermes CLI Not Found

```bash
# Check installation
which hermes

# Install if missing
pip install hermes-agent

# Or specify custom path
{
  hermesCommand: "/path/to/hermes"
}
```

### API Key Issues

```bash
# Verify keys are set
echo $ANTHROPIC_API_KEY
echo $OPENROUTER_API_KEY

# Test key validity
hermes chat -q "hello" --model anthropic/claude-sonnet-4
```

### Session Resume Failures

```typescript
// Disable persistence for debugging
{
  persistSession: false
}

// Check session state
const run = await client.runs.get(runId);
console.log("Session state:", run.sessionState);
```

### Timeout Issues

```typescript
// Increase timeout for long-running tasks
{
  timeoutSec: 1800, // 30 minutes
  graceSec: 30,
  maxIterations: 100
}
```

### Tool Access Errors

```typescript
// Check which tools are enabled
{
  enabledToolsets: ["terminal", "file"], // Minimal set
  verbose: true // See tool invocations
}
```

### Stderr Noise

```typescript
// Use quiet mode to suppress MCP init messages
{
  quiet: true
}

// Benign stderr patterns are auto-reclassified:
// - "MCP server initialized"
// - JSON structured logs
// - Progress indicators
```

### Skills Not Loading

```bash
# Check skill directories
ls ~/.hermes/skills/
ls node_modules/hermes-paperclip-adapter/skills/

# Verify permissions
chmod -R 755 ~/.hermes/skills/

# List available skills
hermes skills list
```

### Memory/Context Issues

```typescript
// Context compression is automatic, but you can control it:
{
  extraArgs: [
    "--context-window", "200000",
    "--compress-after", "150000"
  ]
}
```

## Integration Examples

### With GitHub Actions

```yaml
name: Paperclip Hermes Agent

on:
  schedule:
    - cron: '*/30 * * * *'

jobs:
  hermes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install Hermes
        run: pip install hermes-agent
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Trigger Paperclip Heartbeat
        run: |
          curl -X POST ${{ secrets.PAPERCLIP_API_URL }}/agents/${{ secrets.AGENT_ID }}/heartbeat \
            -H "Authorization: Bearer ${{ secrets.PAPERCLIP_API_KEY }}"
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### With Docker

```dockerfile
FROM node:20-slim

# Install Python and Hermes
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install hermes-agent

# Install adapter
WORKDIR /app
COPY package*.json ./
RUN npm install hermes-paperclip-adapter

# Run Paperclip server with adapter
CMD ["npm", "start"]
```

### With Kubernetes CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hermes-agent
spec:
  schedule: "*/15 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hermes
            image: paperclip/hermes-agent:latest
            env:
            - name: ANTHROPIC_API_KEY
              valueFrom:
                secretKeyRef:
                  name: api-keys
                  key: anthropic
            - name: PAPERCLIP_API_URL
              value: "http://paperclip-server:3100/api"
          restartPolicy: OnFailure
```

## References

- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [Paperclip Docs](https://paperclip.ing/docs)
- [Nous Research](https://nousresearch.com)
- [MCP Protocol](https://modelcontextprotocol.io)
