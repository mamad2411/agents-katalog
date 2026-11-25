---
name: tinyfish-mcp
description: Use when the user selects TinyFish or the agent has chosen TinyFish MCP tools for web search, page reading, extraction, or browser automation. Respect an explicit choice of another service.
---

# TinyFish MCP

Use the configured TinyFish MCP tools rather than the TinyFish CLI. Match actual tool names and input schemas; client prefixes and available capabilities vary. If the required tool is unavailable, report the connection or capability gap and identify any alternative provider actually used.

## Select a tool

Choose the lightest sufficient tool for the current need; the rows are alternatives, not a sequence to execute on every task.

| Need | Tool | Reading condition |
| --- | --- | --- |
| Discover sources or verify current information | `search` | Inspect relevant results; fetch pages when excerpts do not provide sufficient evidence |
| Read known URLs or extract exposed page content | `fetch_content` | Read directly; group independent URLs when the live tool supports it |
| Click, filter, fill fields, navigate, or reveal content unavailable through reading | `run_web_automation` | Read [automation goals](references/automation.md#automation-goals) before starting |
| Control a browser through raw CDP | `create_browser_session` | Read [raw browser sessions](references/automation.md#raw-browser-sessions) before creating a session |

For long-running automation, read [asynchronous runs](references/automation.md#asynchronous-runs) before starting an async run. For multiple independent automation jobs, read [batch jobs](references/automation.md#batch-jobs) before using batch tools. Escalate from reading to interaction only when the returned content cannot satisfy the task.

## Verify and report

For research, inspect relevant primary sources, official documentation, or original publications; use high-quality secondary sources when primary evidence is unavailable. Verify changing facts against live sources. Retain source URLs and distinguish retrieved evidence from synthesis.

Check the tool's returned status, errors, and actual content against the requested result. A successful call, run ID, or click alone does not prove that extraction, filtering, or the overall task is complete. Report inaccessible pages and missing fields as gaps.

Keep actions within the user's requested workflow and authorization. Match the user's language in the answer, preserve supporting URLs, and identify completed actions, pending work, and failure scope.
