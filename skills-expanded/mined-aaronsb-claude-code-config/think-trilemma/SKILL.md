---
name: think-trilemma
description: Trilemma reasoning — balance three competing objectives through satisficing. Use when you cannot optimize all dimensions simultaneously and need to find an acceptable trade-off.
allowed-tools: Read, Bash
---

# Trilemma

## Start Session

Before beginning, register this think session:

```bash
# Check for active session
if [[ -f /tmp/.claude-think-session ]]; then cat /tmp/.claude-think-session; fi
```

If another session is active, ask the user to finish or abandon it first. Otherwise:

```bash
echo "trilemma" > /tmp/.claude-think-session
```

## Work Through Stages

Read the strategy definition and follow its stages in order:

```bash
cat ~/.claude/hooks/ways/meta/think/strategies/trilemma.md
```

Work through each numbered stage sequentially. Do not skip stages. Present your work for each stage before moving to the next.

## Complete Session

After the final stage, clean up so the think way can fire again:

```bash
rm -f /tmp/.claude-think-session /tmp/.claude-way-meta-think-*"${CLAUDE_SESSION_ID:+-$CLAUDE_SESSION_ID}" 2>/dev/null
```
