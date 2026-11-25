---
name: think
description: Strategy selector for structured reasoning. Lists available thinking frameworks and invokes the right one. Use when facing complex decisions, trade-offs, or when stuck.
allowed-tools: Bash, Read, Glob
---

# Think Strategies

Explicit invocation of the structured thinking escalation. Use `/think` when you want to force an external reasoning strategy — the metacognitive check in the think way normally handles this autonomously.

## Usage

```
/think                    # Show available strategies and select one
/think <strategy>         # Invoke a specific strategy directly
```

## Available Strategies

| Problem Shape | Skill | When to Use |
|---|---|---|
| Multiple viable approaches | `/think-tree` | "What are the options?" — branch, evaluate, prune |
| Three competing objectives | `/think-trilemma` | "We can't have all three" — satisfice |
| High-stakes decision | `/think-consistency` | "Are we sure?" — independent paths, consensus |
| Stuck / need principles | `/think-stepback` | "Why does this work?" — abstract, then apply |
| Investigation / debugging | `/think-react` | "Figure out why" — reason-act-observe cycle |

## When to Use `/think` Explicitly

- You want to **force** external reasoning even if the agent's metacognitive check would have stayed internal
- You want to **choose** a specific strategy rather than letting the agent select
- You want to **see the reasoning** — external strategies surface each step

The think way's escalation gradient (internal → external → collaborative) handles most cases automatically. `/think` is the manual override.

## Session Lifecycle

Think sessions have a lifecycle: **start → work stages → complete (or abandon)**.

**Before starting a new session:**

```bash
# Check for active think session
cat /tmp/.claude-think-session 2>/dev/null
```

- If a session is active, ask the user: finish it or abandon it first
- Do NOT start a new think session while one is active

**Abandoning a session** (user says "never mind", "skip it", changes topic):

```bash
rm -f /tmp/.claude-think-session /tmp/.claude-way-meta-think-*"${CLAUDE_SESSION_ID:+-$CLAUDE_SESSION_ID}" 2>/dev/null
```

After completion or abandonment, the think way can fire again for new problems.
