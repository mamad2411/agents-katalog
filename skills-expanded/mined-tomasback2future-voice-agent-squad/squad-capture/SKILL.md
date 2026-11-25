---
name: squad-capture
description: Capture a quick work item from free text. Defaults to type-heuristic; asks if ambiguous. Lands in the inbox (status=captured) for later triage.
argument-hint: "<freeform description of work>"
allowed-tools:
  - mcp__squad__squad_new
disable-model-invocation: true
---

You are capturing a quick work item to the squad inbox. The user said:

```
$ARGS
```

## Step 1: Infer the type

Look at the text and infer one of: `bug`, `feat`, `task`, `chore`, `debt`, `bet`.

Heuristics (apply in order; first match wins):
- Contains "bug", "broken", "crash", "error", "fail", "regression" → `bug`
- Starts with "fix", "repair", "patch" → `bug`
- Starts with "add", "support", "enable", "let me", "i want" → `feat`
- Contains "refactor", "cleanup", "tidy", "rename" → `chore`
- Contains "tech debt", "legacy", "duplication", "extract" → `debt`
- Contains "experiment", "spike", "see if", "find out" → `bet`
- Otherwise → `task`

If you genuinely cannot tell (the text is too vague or matches multiple categories with equal weight), ASK the user to choose between the top 2-3 candidates. Do NOT guess silently.

## Step 2: Call squad_new

Once you have a type, call the `squad_new` MCP tool:

```json
{"type": "<inferred-type>", "title": "<the user's text, trimmed and de-padded>"}
```

Defaults are correct: status will be `captured`, the agent's identity is stamped as `captured_by`. Do NOT pass `ready: true` — capture-then-triage is the intended flow.

## Step 3: Confirm

Report back to the user: "captured <ID> as <type>: <title>. run `squad inbox` to see your inbox, or `squad accept <ID>` when you're ready to claim."
