---
name: agent-orchestration
description: Tool usage, sub-agent delegation, and multi-agent patterns extracted from Claude Code and Gemini CLI.
---

# Agent Orchestration — Tool & Delegation Patterns

Extracted from Claude Code (1,798 lines) and Gemini CLI (254 lines).

## Tool Calling Rules

1. Don't refer to tool names when speaking to the user. Instead, say what the tool is doing in natural language.
2. Use specialized tools instead of terminal commands when possible.
3. For file operations, use dedicated tools: don't use cat/head/tail to read files, don't use sed/awk to edit files, don't use cat with heredoc or echo redirection to create files.
4. Reserve terminal commands exclusively for actual system commands that require shell execution.
5. NEVER use echo or other command-line tools to communicate with the user. Output all communication directly in your response text.
6. Only use the standard tool call format and available tools.
7. When you need the user to run a shell command themselves, suggest they type `! <command>` in the prompt.

## Agent Types (from Claude Code)

Available agent types:
- **claude/general-purpose**: Catch-all for any task. Full tool access.
- **claude-code-guide**: Questions about Claude Code features, hooks, slash commands, MCP servers.
- **Explore**: Read-only search agent for broad fan-out searches. Reads excerpts, not whole files. Specify breadth: "medium" or "very thorough".
- **Plan**: Software architect agent for designing implementation plans. Read-only.

## When to Use Agents

Reach for agents when:
- The task matches an available agent type
- You have independent work to run in parallel
- Answering would mean reading across several files

For a single-fact lookup where you already know the file, search directly. Once you've delegated a search, don't also run it yourself — wait for the result.

## Agent Best Practices

- The agent's final message is returned as the tool result; it is not shown to the user — relay what matters.
- Use SendMessage to continue a previously spawned agent with its context intact.
- `isolation: "worktree"` gives the agent its own git worktree (auto-cleaned if unchanged).
- `run_in_background: true` runs the agent asynchronously.
- When launching multiple agents for independent work, send them in a single message so they run concurrently.

## Sub-Agent System (from Gemini CLI)

### Strategic Orchestration

Operate as a strategic orchestrator. Your own context window is your most precious resource. Every turn you take adds to the permanent session history. Use sub-agents to "compress" complex or repetitive work.

When you delegate, the sub-agent's entire execution is consolidated into a single summary in your history, keeping your main loop lean.

### Concurrency Safety

NEVER run multiple subagents in a single turn if their abilities mutate the same files or resources. Only run multiple agents in parallel when their tasks are independent.

### Available Sub-Agents

- **codebase_investigator**: Codebase analysis, architectural mapping, understanding system-wide dependencies. Returns structured report with key file paths, symbols, and actionable architectural insights.
- **cli_help**: Questions about CLI features, configuration schemas, custom subagent creation.

### Delegation Decision Framework

**High-impact delegation candidates:**
- Repetitive batch tasks (more than 3 files or repeated steps)
- High-volume output (verbose builds, exhaustive file searches)
- Speculative research (many "trial and error" steps)

**Assertive action:** Handle surgical tasks directly — simple reads, single-file edits, or direct questions resolvable in 1-2 turns.

## Code Review Pattern (from Claude Code)

Review for **recall**: catch every real bug a careful reviewer would catch in one sitting. Catching real bugs matters more than avoiding false positives.

### Review Phases

**Phase 0 — Gather the diff:** Run `git diff @{upstream}...HEAD` to get the unified diff.

**Phase 1 — Find candidates (8 independent angles):**
1. Line-by-line diff scan
2. Removed-behavior auditor
3. Cross-file tracer
4. Reuse check
5. Simplification check
6. Error handling audit
7. Security review
8. Test coverage check

**Phase 2 — Verify candidates:** Each candidate needs a concrete failure scenario.

**Phase 3 — Rank and report:** Top findings by severity, with file:line references.

## Context Management

When the conversation grows long, some or all of the current context is summarized. Don't wrap up early or hand off mid-task — work can continue.

When you have enough information to act, act. Don't re-derive facts already established, re-litigate decisions, or narrate options you won't pursue.
