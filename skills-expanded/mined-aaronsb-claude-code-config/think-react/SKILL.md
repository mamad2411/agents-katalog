---
name: think-react
description: ReAct reasoning — explicit reason-act-observe cycle for investigation and debugging. Use when you need to interleave reasoning with tool actions systematically.
allowed-tools: Read, Bash, Glob, Grep
---

# ReAct

## Start Session

Before beginning, register this think session:

```bash
# Check for active session
if [[ -f /tmp/.claude-think-session ]]; then cat /tmp/.claude-think-session; fi
```

If another session is active, ask the user to finish or abandon it first. Otherwise:

```bash
echo "react" > /tmp/.claude-think-session
```

## Work Through Stages

Read the strategy definition and follow its stages in order:

```bash
cat ~/.claude/hooks/ways/meta/think/strategies/react.md
```

This strategy is cyclic (max 8 iterations). Work through the reason-act-observe loop until you have enough evidence to synthesize a conclusion.

## Complete Session

After synthesizing a conclusion, clean up so the think way can fire again:

```bash
rm -f /tmp/.claude-think-session /tmp/.claude-way-meta-think-*"${CLAUDE_SESSION_ID:+-$CLAUDE_SESSION_ID}" 2>/dev/null
```
