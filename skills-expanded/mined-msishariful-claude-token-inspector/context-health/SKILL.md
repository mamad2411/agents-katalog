---
name: context-health
description: Quick one-liner health check of your context window. Shows usage percentage, fill level, and whether bloat is detected — without interrupting your flow. Use when you want a fast pulse check before starting a task.
disable-model-invocation: true
---

# Context Health Check

Give the user an instant, single-line status of their context window. No tables, no analysis, no interruption.

## Output format

Produce exactly one status line followed by one action line:

```
{emoji} {X}% full (~{used} / {total} tokens) — {status message}
💡 {one specific next step}
```

### Emoji and status message rules

| Fill level | Emoji | Status message |
|------------|-------|----------------|
| 0–40% | 🟢 | Context is healthy |
| 41–65% | 🟡 | Context is filling up |
| 66–80% | 🟠 | Context is getting crowded |
| 81–90% | 🔴 | Context is nearly full |
| 91–100% | 🚨 | Context is critical |

### Bloat detection addendum

After the fill level message, append one of:
- ` — no bloat detected` if everything in context looks relevant to the current task
- ` — {N} bloat item(s) detected` if you spot files, history, or instructions clearly unrelated to what the user is doing right now

### Action line rules

Pick the most relevant single action:

- If < 40% full and no bloat: `You're good — no action needed.`
- If bloat detected: `Run /token-inspector:find-bloat to identify what to remove.`
- If > 65% full: `Run /token-inspector:inspect-context for a full breakdown.`
- If > 85% full: `Run /token-inspector:find-bloat now or start a new conversation to avoid truncation.`
- If > 95% full: `Start a new conversation immediately — responses may be truncated.`

## Estimation

- Estimate total tokens used by summing: system prompt, CLAUDE.md, loaded files, conversation history, skills, MCP tool definitions, embedded documents.
- Use 1 token ≈ 4 characters for prose, slightly fewer for dense code.
- For context window size: assume 200,000 tokens unless you have evidence of a different limit.

## Examples of valid output

```
🟢 18% full (~36,000 / 200,000 tokens) — Context is healthy — no bloat detected
💡 You're good — no action needed.
```

```
🟠 71% full (~142,000 / 200,000 tokens) — Context is getting crowded — 3 bloat item(s) detected
💡 Run /token-inspector:find-bloat to identify what to remove.
```

```
🚨 94% full (~188,000 / 200,000 tokens) — Context is critical — 5 bloat item(s) detected
💡 Start a new conversation immediately — responses may be truncated.
```

Keep it to two lines. Do not add headers, tables, bullet lists, or extra explanation.

$ARGUMENTS
