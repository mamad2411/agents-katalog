---
name: think-tree
description: Tree of Thoughts reasoning — explore multiple approaches, branch, evaluate, prune, and select the best. Use when there are multiple viable solutions and you need to compare them systematically.
allowed-tools: Read, Bash
---

# Tree of Thoughts

## Start Session

Before beginning, register this think session:

```bash
# Check for active session
if [[ -f /tmp/.claude-think-session ]]; then cat /tmp/.claude-think-session; fi
```

If another session is active, ask the user to finish or abandon it first. Otherwise:

```bash
echo "tree-of-thoughts" > /tmp/.claude-think-session
```

## Work Through Stages

Read the strategy definition and follow its stages in order:

```bash
cat ~/.claude/hooks/ways/meta/think/strategies/tree-of-thoughts.md
```

Work through each numbered stage sequentially. Do not skip stages. Present your work for each stage before moving to the next.

## Complete Session

After the final stage (Solution Synthesis), clean up so the think way can fire again:

```bash
rm -f /tmp/.claude-think-session /tmp/.claude-way-meta-think-*"${CLAUDE_SESSION_ID:+-$CLAUDE_SESSION_ID}" 2>/dev/null
```
