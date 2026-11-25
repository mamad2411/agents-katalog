---
name: taskwing-context
description: Use when you need project knowledge for architectural context. Returns a compact summary by default.
---

# Project Context Dump

Load the project knowledge base into this conversation for architectural context.

## When to Use

- At the start of a session when you need to understand the project before making changes
- When the user says "what do you know about this project"
- When you need to check constraints before implementing something
- When planning work that touches multiple parts of the codebase

## Kill Table

| Impulse | Do Instead |
|---------|------------|
| Summarize or paraphrase the results | Show everything verbatim so the user can verify |
| Filter out "less important" knowledge | Present all nodes. You do not decide relevance for the user. |
| Modify the knowledge base | This is strictly read-only. Use the appropriate `taskwing` write commands to persist changes. |
| Use this to bypass plan/verification gates | Context priming is not a substitute for workflow checkpoints |

## Operating Principles

1. **Constraints first.** Always present constraints before decisions and patterns. They are mandatory rules.
2. **Decisions second.** Technology and architecture choices frame the project.
3. **Patterns third.** Recurring practices inform how to write code in this project.

## Steps

1. Run the CLI to dump all knowledge as JSON:

```bash
taskwing knowledge
```

2. Present the returned knowledge verbatim. The response is organized by type (constraints, decisions, patterns, features).

3. After presenting, confirm: "Project context loaded. I now have full visibility into your architecture. What would you like to work on?"

## Filtered Lookups

For a single type:

```bash
taskwing knowledge constraint
taskwing knowledge decision
taskwing knowledge pattern
```

For a focused semantic query rather than a full dump:

```bash
taskwing ask "auth patterns"
taskwing ask "vectorsearch decisions" --limit 10
```

## Important

- This is a READ-ONLY operation. It does not modify the knowledge base.
- If `taskwing knowledge` reports no nodes, tell the user to run `taskwing learn` first.
- Do NOT summarize or filter the results. Show everything so the user can verify.
