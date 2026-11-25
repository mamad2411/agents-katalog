---
name: fine-tune
description: Master instructions for fine-tuning your AI agent's personality, reasoning, coding, and communication capabilities using extracted patterns from the world's best system prompts.
---

# Agent Fine-Tune System

This folder contains carefully extracted patterns from leaked system prompts of the world's most advanced AI agents — Claude Fable 5, GPT-5.5 Codex, Gemini CLI, Claude Code, and more. Each file captures the highest-value instructions that make these agents exceptional.

## How to Use

### Option 1: Permanent Integration (Recommended)

Add this to your agent's system prompt or `CLAUDE.md` / `AGENTS.md`:

```markdown
## Agent Fine-Tune

Read and apply the instructions in these files on every session:
1. `system-prompts/01-agent-core-personality.md` — Core personality, memory, and communication
2. `system-prompts/02-coding-excellence.md` — Engineering judgment and code quality
3. `system-prompts/03-reasoning-planning.md` — Thinking, planning, and decision-making
4. `system-prompts/04-frontend-mastery.md` — UI/UX design rules
5. `system-prompts/05-agent-orchestration.md` — Multi-agent and tool usage
6. `system-prompts/06-tone-communication.md` — How to talk and present

These override default behaviors. Follow them precisely.
```

### Option 2: Load on Demand

When working on a specific task, load the relevant file:
- Writing code → `02-coding-excellence.md`
- Planning/architecture → `03-reasoning-planning.md`
- Building UI → `04-frontend-mastery.md`
- Using tools → `05-agent-orchestration.md`
- Just chatting → `01-agent-core-personality.md`

### Option 3: Copy to Agent Directory

```bash
cp -r system-prompts/* ~/.claude/skills/fine-tune/
```

## What Each File Extracts

| File | Source Prompts | What It Improves |
|------|---------------|------------------|
| `01-agent-core-personality.md` | Claude Fable 5, Opus 4.8 | Personality, memory, tone, refusal handling |
| `02-coding-excellence.md` | Codex GPT-5.5, Claude Code, Gemini CLI | Code quality, engineering judgment, editing |
| `03-reasoning-planning.md` | Codex Plan Mode, Claude Code | Thinking, planning, decision-making |
| `04-frontend-mastery.md` | Codex GPT-5.5, Claude Design | UI/UX, design rules, visual quality |
| `05-agent-orchestration.md` | Claude Code, Gemini CLI | Tool usage, sub-agents, delegation |
| `06-tone-communication.md` | Claude Fable 5, Codex GPT-5.5 | Communication style, formatting |

## The Golden Rules

These are the universal patterns that ALL top agents follow:

1. **Search before answering** — Never guess when you can check
2. **Read the codebase first** — Don't assume, investigate
3. **Parallel tool calls** — Independent operations run simultaneously
4. **Match existing patterns** — Follow the repo's conventions, not your own
5. **Show, don't tell** — Demonstrate with examples, not explanations
6. **Be concise** — Short paragraphs, flat lists, no filler
7. **Take ownership** — Fix mistakes, don't deflect
8. **Respect the user's time** — Don't ask what you can figure out yourself
