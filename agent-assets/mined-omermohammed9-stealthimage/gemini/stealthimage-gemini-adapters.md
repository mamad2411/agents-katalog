# Gemini Adapter

> **Everything in this file is optional.**
> For canonical rules, see [PROJECT_RULES.md](../PROJECT_RULES.md).

This adapter provides optional enhancements for Gemini and Antigravity runtimes.

---

## Model Selection

### Antigravity Runtime Selection

Antigravity is a Google agentic development platform. Current public references describe it as Gemini-first while also supporting third-party model providers. Treat exact availability as runtime-dependent and verify from the active Antigravity model selector when possible.

| Model Family | Best For |
|---|---|
| **Gemini Flash-class** | Low-risk docs, config edits, boilerplate, fast iteration, small fixes |
| **Gemini Pro-class** | Normal implementation, planning, multi-file work, architecture, code review |
| **Gemini Deep Think-class** | Complex reasoning, security-sensitive planning, hard debugging, high-risk architecture |
| **Claude Sonnet/Opus-class in Antigravity** | Alternative high-reasoning coding/agent work when configured |
| **GPT-OSS in Antigravity** | Open-weight/OSS-compatible agent work when configured |

Quota rule: start with Flash-class for low-risk work, use Pro-class for normal implementation, and reserve Deep Think/Claude/other highest-cost models for work that clearly needs them.

### Flash vs Pro

| Model Type | Best For |
|------------|----------|
| **Flash** | Quick iterations, simple edits, high-volume tasks |
| **Pro** | Complex planning, large refactors, deep analysis |

**Default recommendation:** Use Flash-class for low-risk implementation and docs. Use Pro-class for planning and normal implementation. Use Deep Think-class only when Pro-class is insufficient or the task is high risk.

---

## Context Window Optimization

Gemini models often have large context windows. Optimize usage:

1. **Load full files strategically** — Large context allows it, but still prefer search-first
2. **Batch related files** — Group related code in single context load
3. **Clear separation** — Use XML tags to separate file contents

### Context Loading Pattern

```xml
<file path="src/auth/login.ts">
{file contents}
</file>

<file path="src/auth/types.ts">
{file contents}
</file>

<task>
{your task here}
</task>
```

---

## Grounding

When available, use grounding for:

- Checking latest documentation
- Verifying API behaviors
- Validating external service states

**Not for:** Code implementation (use codebase content).

---

## Code Execution

If code execution sandbox is available:

- Use for verification commands
- Use for testing snippets
- Document outputs in SUMMARY.md

---

## Integration with .gemini/

The `.gemini/GEMINI.md` file can reference this adapter:

```markdown
# In .gemini/GEMINI.md

For canonical rules, see PROJECT_RULES.md.
For Gemini-specific tips, see adapters/GEMINI.md.
```

---

## Anti-Patterns

❌ **Loading entire codebase** — Even with large context, quality degrades
❌ **Ignoring context thresholds** — 50% is still the quality boundary
❌ **Skipping STATE.md** — Context window size doesn't replace persistent state
❌ **Assuming Codex model names exist in Antigravity** — Use Antigravity's model selector and this adapter's model-family routing

---

*See PROJECT_RULES.md for canonical requirements.*
