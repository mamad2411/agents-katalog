---
name: parallel-agents
description: Dispatch multiple subagents in parallel for independent tasks. Cache-friendly dispatch pattern — identical system prompts let the Anthropic prompt cache (5-min TTL) make 2nd-Nth dispatches nearly free
---

# parallel-agents

## When to use

Use when you have 2+ independent problems that can each be solved without knowing the others' results.

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from the others
- No shared state between investigations (no editing the same files)

**Do not use when:**
- Failures are related (fix one might fix others — investigate together first)
- Need to understand full system state before starting
- Agents would edit the same files (conflicts)

## The pattern

1. **Identify independent domains.** Group failures by what's broken. Each domain is its own agent scope.

2. **Create focused agent tasks.** Each agent gets: specific scope (one file or subsystem), clear goal (make these tests pass), constraints (don't change other code), expected output (summary of root cause and changes).

3. **Dispatch in parallel.** All agents run concurrently.

4. **Review and integrate.** When agents return: read each summary, verify fixes don't conflict, run full test suite.

## Good agent prompt structure

```markdown
Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts:

1. "should abort tool with partial output capture" — expects 'interrupted at' in message
2. "should handle mixed completed and aborted tools" — fast tool aborted instead of completed
3. "should properly track pendingToolCount" — expects 3 results but gets 0

These are likely timing/race condition issues. Your task:
1. Read the test file and understand what each test verifies
2. Identify root cause — timing issues or actual bugs?
3. Fix — replace arbitrary timeouts with event-based waiting if needed

Do NOT just increase timeouts — find the real issue.

Return: summary of root cause and what you fixed.
```

**Common mistakes:**
- Too broad: "Fix all the tests" — agent gets lost → Too specific: "Fix agent-tool-abort.test.ts"
- No context: "Fix the race condition" → Paste the error messages and test names
- No constraints → "Do NOT change production code" / "Fix tests only"
- Vague output: "Fix it" → "Return summary of root cause and changes"

## Cache-friendly dispatch (imlazy pattern)

When dispatching N parallel subagents, construct N requests with **identical** system prompts. The Anthropic prompt cache TTL is ~5 minutes — requests within the same dispatch batch will hit the cache, making dispatches 2 through N roughly 10× cheaper on input tokens.

What varies per dispatch: the user message (task-specific content).
What stays identical: the system prompt (role, constraints, output format).

Do not put task-specific context in the system prompt — it breaks cache hits.

**Real-world impact:** In a debugging session with 6 failures across 3 files, dispatching one agent per file solved all problems concurrently in the time of one sequential investigation, with zero conflicts between the agents' changes.

## Verification after agents return

1. Read each summary — understand what changed and why
2. Check for conflicts — did any agents edit the same code?
3. Run full test suite — verify all fixes work together
4. Spot-check — agents can make systematic errors; sample the actual diffs
