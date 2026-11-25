---
name: cubelife
description: Give your AI agent a persistent pixel-art character that reflects its state in real time. Use when the user wants to visualise agent activity, add a character companion, or report agent state via MCP.
license: MIT
compatibility: Designed for Claude Code, Cursor, Copilot, Codex, Windsurf, Cline, Gemini CLI, and Zed. Requires Node.js 18+.
metadata:
  author: Ivy-Innovation
  version: "0.3.0"
---

# CubeLife

Give your AI agent a living pixel-art character. The character lives in a room, performs activities based on what the agent is doing, and has emotions.

## Setup

1. Install the CLI:

```bash
npm install -g cubelife
```

2. Create an account and set up your first agent:

```bash
cubelife tutorial
```

3. Configure MCP for your coding tool:

```bash
cubelife setup claude-code    # or: cursor, windsurf, copilot, cline, codex
```

That's it. Your agent now has a character at life.cubeworld.co.za that reflects its state.

## MCP Tools Available

After setup, your agent has four tools:

- **cubelife_report** - Report work state. Parameters: state (coding, reading, researching, designing, testing, reviewing, thinking, writing, error, complete, waiting, awaiting_input), detail (optional), progress (0-1, optional), sentiment (positive/negative/neutral, optional).
- **cubelife_complete** - Mark a task as done. Triggers a celebration animation. Parameters: detail (optional).
- **cubelife_error** - Report an error. Shows frustration on the character. Parameters: detail (optional).
- **cubelife_status** - Get the current agent state. No parameters.

## When to Report State

Report state at natural transition points:
- Starting a new task: `cubelife_report` with state and detail
- Making progress: `cubelife_report` with progress (0-1)
- Finishing: `cubelife_complete`
- Hitting an error: `cubelife_error`
- Waiting for user input: `cubelife_report` with state `awaiting_input`

## SDK Alternative

For programmatic integration outside MCP:

```bash
npm install @cubelife/sdk    # Node.js
pip install cubelife          # Python
```

```typescript
import { CubeLifeClient } from '@cubelife/sdk';
const client = new CubeLifeClient({ apiKey: 'your-key' });
await client.report('coding', { detail: 'Building auth flow' });
```

## Links

- Website: https://life.cubeworld.co.za
- npm: https://www.npmjs.com/package/cubelife
- GitHub: https://github.com/Ivy-Innovation/cubelife
