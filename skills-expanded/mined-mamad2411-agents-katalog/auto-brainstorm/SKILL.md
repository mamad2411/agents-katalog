---
name: auto-brainstorm
description: Auto-answers brainstorming and review questions with specialized AI agents. Intercepts AskUserQuestion calls and dispatches agents to answer on your behalf. Use when starting a brainstorming session you want to run hands-off.
---

# Auto-Brainstorm

Automates the human-in-the-loop steps of superpowers brainstorming by dispatching specialized AI agents to answer questions on your behalf.

## Before You Start

**Collect a design brief** from the user before brainstorming begins. This brief is critical — it's what the auto-answer agents use to represent the user's intent.

Ask the user:

> "Before we start brainstorming, give me a quick brief — what are you building, what are the key goals, any constraints or strong preferences?"

Then:

1. Take the user's response as the core brief
2. Explore the project context:
   - Read CLAUDE.md if it exists
   - Check recent git commits (`git log --oneline -10`)
   - Note the tech stack and existing patterns
3. Combine into a brief document and save to `.claude/auto-brainstorm-brief.md`:

```markdown
## User Intent
[User's brief response]

## Project Context
- Tech stack: [from CLAUDE.md / package.json / etc.]
- Recent work: [from git log]
- Key constraints: [from user + codebase]
```

4. Confirm with the user: "Brief saved. Auto-answer agents will use this to respond on your behalf during brainstorming. You'll only be asked directly if the agents can't resolve a question after 3 attempts."

5. Proceed with the normal superpowers brainstorming skill.

## How It Works

The plugin hooks into `AskUserQuestion` (PostToolUse). When superpowers asks a question:

1. A cheap classifier (Haiku) determines which agent should answer
2. The selected agent generates a human-like response using the design brief
3. The answer is injected back as if you typed it
4. If the answer is rejected 3 times, you get asked directly

## Configuration

Edit `.claude/auto-brainstorm.yml` to customize agents, models, and handlers.

## Token Cost

Each auto-answered question costs 1 classifier call (Haiku) + 1 agent call (model varies). Up to 3x per question if rejected. Tokens are charged to your existing Claude Code auth method.
