---
name: agent-sdk-review
description: "Reviews Claude Agent SDK code, or a hand-written Claude API tool loop, and reports design-rule violations ranked by blast radius. Use when onboarding or spot-checking agent code. Flags irreversible actions gated only by a prompt, permissive permission settings, unbounded loops or tool results, authorization that fails open, and unvalidated output. Read-only. Not a gate on one diff (use the agent-sdk-validator agent); not for other agent frameworks."
when_to_use: "review my agent code, audit an agent SDK codebase, check the agent loop, why does my agent never stop, agent permission review, onboard an agent codebase"
argument-hint: "[repository or agent directory, or pasted agent code; defaults to the current directory]"
allowed-tools: Read, Glob, Grep, Agent
disallowed-tools: Write, Edit, NotebookEdit
context: fork
license: MIT
---

# Review Claude Agent Code

Target: $ARGUMENTS

A read-only survey of how an agent is built, ranked by blast radius. The caller applies the fixes and
re-runs. For a pass/fail gate on one diff, use the `agent-sdk-validator` agent instead.

## Step 1 — Find the agent code

Resolve the target: a path, the current directory when empty, or pasted code. This fork can't see the
conversation, so pasted code only arrives through the argument. Then use the Grep tool over `*.py`,
`*.ts`, `*.tsx`, `*.js` and `*.mjs`, skipping `node_modules` and virtualenvs:

- **Agent SDK:** `claude_agent_sdk|@anthropic-ai/claude-agent-sdk`
- **Hand-written Messages API loop:** files matching `from anthropic|import anthropic|@anthropic-ai/sdk`
  that also match `stop_reason|tool_use|tool_result`
- **Tool definitions:** `input_schema|inputSchema|@tool\(|createSdkMcpServer|create_sdk_mcp_server`

If neither of the first two matches, return `No Claude Agent SDK or Claude API agent loop found under
<target>` plus the patterns you searched, and stop. A single model call with no tool loop is out of
scope. If the codebase mixes frameworks, review only the Claude portion and name what you excluded.

## Step 2 — Survey in parallel

Spawn up to three `Agent` calls in one message, one per band. Give each the file lists from Step 1,
its band text, and the finding schema below. If `Agent` is unavailable (the nesting depth limit, or a
surface without subagents), run the bands inline in order.

### Band 1: loop and permissions

**Agent SDK code.** The SDK runs the tool loop itself, so check its options and the result handling:

- **Termination:** does the code check `terminal_reason` before `subtype` (e.g. `api_error` arrives
  as `success`), then the `ResultMessage` `subtype` (`success`, `error_max_turns`,
  `error_max_budget_usd`, `error_during_execution`, …) before reading `result`, and handle each error
  subtype? Does it catch the error a single-shot `query()` raises after an error result?
- **Bounds:** are `maxTurns` / `max_turns` and `maxBudgetUsd` / `max_budget_usd` set for open-ended
  prompts?
- **Permissions:** `allowedTools` auto-approves tools but doesn't restrict them. Unlisted tools stay
  callable, so flag code that treats it as a sandbox; `disallowedTools` or a narrow `tools` list is
  the restriction. Flag `bypassPermissions` outside an isolated environment.
- **`canUseTool` / `can_use_tool`:** does the callback deny on error or on an unknown tool, rather
  than allow?
- **`settingSources` / `setting_sources`:** omitting it loads user, project and local settings,
  `CLAUDE.md` and hooks. Flag multi-tenant or server code that doesn't pass an explicit list.
- **SDK hooks:** are irreversible actions gated by a `PreToolUse` hook or `canUseTool`, rather than by
  prompt text?
- **Subagents** (`agents` option): is context passed explicitly in the prompt? The coordinator should
  own the result, hub-and-spoke rather than peer to peer.

**Hand-written Messages API loops only:**

- Does the loop branch on `stop_reason` rather than on the assistant's prose?
- Is every `tool_use` answered by a `tool_result` in the next user turn, including on the error path?
- Is `max_tokens` truncation distinguished from a finished turn?
- Is the loop bounded by turns and spend?

See `agentic-loop-control` and `agent-orchestration` for the reasoning.

### Band 2: tool interfaces and errors

- Can a stranger use each tool from its description, including when not to call it?
- Are inputs typed and narrow, with enums for closed sets?
- Are outputs bounded (paginated, aggregated, or truncated at a stated ceiling)?
- Do tools return errors the model can act on, with a category and a retryability derived from the
  actual failure? In the Agent SDK, return `isError` / `is_error` with a composed message. An uncaught
  throw reaches Claude only as the raw exception text; the SDK doesn't crash. In a hand-written loop,
  a throw that skips the `tool_result` corrupts the conversation.
- Does authorization fail closed? An empty result on error is indistinguishable from a real empty
  result.

See `tool-interface-design`.

### Band 3: context, output, enforcement, escalation

- Are large tool results summarized, dropped or delegated rather than appended raw?
- Is output consumed downstream schema-validated, with a retry rather than a silent coercion?
- Are writes, deploys, spend and outbound messages gated in code?
- Does data returned from subagents and tools carry provenance?
- Does the agent escalate when blocked, out of retries, or uncertain on a high-stakes step?

See `context-economy`, `output-contracts`, `deterministic-enforcement` and
`provenance-and-escalation`.

Finding schema, for every band:

```json
{"band": 1, "severity": "critical|warning|minor", "file": "path", "line": 0,
 "evidence": "quoted code", "problem": "one sentence", "rule": "short name", "fix": "concrete change"}
```

## Step 3 — Rank by blast radius

- **`critical`:**
  - an irreversible action gated only by a prompt;
  - `bypassPermissions` or `allowedTools`-as-sandbox on a system that matters;
  - authorization or `canUseTool` that fails open;
  - a missing `tool_result`, or a throw that corrupts a hand-written loop.
- **`warning`:**
  - unvalidated or coerced output;
  - an unbounded loop or tool response;
  - unhandled error result subtypes, or `subtype` checked without `terminal_reason` first;
  - implicit `settingSources` on server code.
- **`minor`:** vague descriptions, untyped inputs, missing provenance.

## Step 4 — Verify

Re-open the file and line for every critical finding and confirm the quoted evidence. Drop what you
can't reproduce. Confirm that each finding sits in Claude agent code, not in another framework.

## Report

```markdown
# Agent code review: <target>
Scope: <SDK files n, API-loop files n, excluded: ...>

## Top risks
<one line each for the critical findings, or "none">

## Findings
| # | Severity | File:line | Problem | Fix | Rule |
|---|----------|-----------|---------|-----|------|

## Not checked
<unreadable paths or skipped bands, or "none">
```

A codebase that already follows the rules gets a short report with an empty findings table.
