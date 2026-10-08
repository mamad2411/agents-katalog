---
name: mcp-open-bridge
description: Use when a task benefits from a second-opinion reasoning pass, architecture comparison, focused file analysis, or batch synthesis via OpenRouter-backed MCP tools.
---
<!-- vibekit:pack=mcp-open-bridge -->

# Open Bridge MCP

Use this skill when repo-local investigation is not enough and an extra reasoning pass would help compare options, review a tricky implementation idea, synthesize several findings, or inspect a specific file with a focused prompt.

Only use this skill if the Open Bridge MCP tools are available in the current assistant. If they are not available, say that Open Bridge is not configured and continue with local evidence only.

## Workflow

1. Define the exact question or decision you want help with.
2. Send only the minimum relevant context: a focused problem statement, a targeted file, or a small diff.
3. Prefer `consult_openrouter` for one question, `consult_openrouter_with_stdin` for file or diff analysis, and `consult_openrouter_batch` for comparing several files or options.
4. Treat the response as advisory context, not ground truth.
5. Verify useful claims against the repository before planning edits or changing code.
6. Summarize the insight you kept and how it changed your plan, implementation, or review.

## Good Uses

- Stress-testing a plan or architecture choice
- Comparing implementation or rollout options
- Getting a second-pass review of a tricky file, diff, or error pattern
- Synthesizing several research findings into one recommendation

## Avoid

- Sending secrets, tokens, or unrelated proprietary code
- Using it when local code, tests, or official docs already answer the question
- Treating model output as verified fact without code or test confirmation
