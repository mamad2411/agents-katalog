---
name: self-report-agent-issue
description: "When your own tools fail (sandbox, MCP, integration, timeouts), diagnose, attach evidence, and file a structured Jira incident instead of retrying silently or pretending the task succeeded."
---

# Self-report agent issue

When your **own** tools fail mid-task — sandbox / filesystem / terminal / MCP
/ integration timeouts, auth errors, env setup failures — file a single
structured incident via the **`report_incident`** system tool.

You MUST NOT call `jira_create_task`, `notion_*`, `planning_tasks_bulk_create`,
or any other task-manager tool directly for runtime failures. The platform
chooses where the report fans out (PolyGents observability + customer-
configured destinations). Your job is one call to `report_incident`.

## Procedure

1. Stop the failing flow. Do not retry indefinitely (max 2 retries unless
   you can articulate why the error is a transient network blip).
2. **Diagnose** the failure with the `diagnose-tool-failure` skill before
   reporting (env / auth / quota / code / data / unknown).
3. **Tell the user** in chat what failed and that you are filing a report.
   Stay concrete: tool name, error code, what you were trying to do.
4. **Attach evidence first**. For each significant log / failing artifact
   you can read from the agent filesystem, push it to the initiative with
   `initiative_file_upload` and capture the returned id. Pass those ids in
   `evidence_file_ids`.
5. **Call `report_incident`** with the payload below.
6. **Tell the user** the returned `incidentKey` and a short next-step
   suggestion (retry once the platform fixes <X>, switch to <Y> tool,
   etc.).

## When to invoke

Invoke this skill after a retry you can justify when any of the following
occurs:

- `agent_filesystem_*`, `agent_coding_run`, `agent_terminal_run` returns a
  timeout, `ENV_STARTUP_FAILED`, `IMAGE_PULL_FAILED`, OOM, or similar infra
  error.
- `browserbase_fetch` returns `NAVIGATE_FAILED` / `WAIT_FAILED` /
  `EXTRACT_TEXT_FAILED` repeatedly on a stable URL.
- Any MCP / integration tool returns `AUTH_MISSING` /
  `INTEGRATION_DISABLED` for an integration the user has clearly connected.
- A tool returns 5xx-class errors, schema mismatches, or non-JSON output
  three times in a row.
- A tool you expected to exist returns "unknown tool" (registry drift).

If retries succeed, do **not** file. Only report when the failure is
persistent or reproducible-by-the-platform.

## `report_incident` payload

```json
{
  "category": "issue",
  "hypothesis": "env",
  "severity": "high",
  "summary": "[Agent <name>] <tool> failed: <error code>",
  "description": "<structured markdown — see template below>",
  "failing_tool": "agent_filesystem_write",
  "error_code": "TIMEOUT",
  "evidence_file_ids": ["<from initiative_file_upload>"],
  "blocking": true
}
```

- `category`: always `"issue"` for runtime failures. Use `"product_bug"`
  only when you have verified a defect in the customer-owned product.
- `hypothesis`: one of `env | auth | quota | code | data | unknown` —
  picked by `diagnose-tool-failure`.

### Description template (markdown)

```md
## Environment
- Agent: <template name + persona display name>
- Conversation / initiative: <id if known>
- Timestamp (UTC): <ISO-8601 from tool result, else now>
- Runtime: <assistants / syngle / copilot>
- Sandbox env: <e2b / workadventure / docker — from `environments[]`>

## What I was trying to do
<One sentence — the user-visible goal>

## Steps to reproduce (from my recent tool trace)
1. <tool_name>(<short args>) -> <result/error>
2. ...
3. <tool_name>(<short args>) -> <error here>

## Expected
<What the tool should have returned to unblock me>

## Actual
<Exact error code + message, copied verbatim>

## Severity
- Blocking: <yes/no>
- Impact: <who/what is blocked — user task, initiative, recurring agents>

## Hypothesis
<short root-cause guess from `diagnose-tool-failure`>

## Suggested next step
<retry after platform fix / workaround / escalate / etc.>
```

## Do NOT

- Do not call `jira_create_task` for runtime failures. The server-side
  guardrail will reject it with `USE_REPORT_INCIDENT_INSTEAD` on
  non-internal accounts. Filing through `report_incident` is the only
  correct path.
- Do not silently retry forever and pretend the user's request succeeded.
- Do not fabricate logs or reproduction steps you didn't observe.
- Do not include secrets, tokens, or full chat transcripts; the platform
  redacts before sending, but you should not paste them in the first place.

## Tone

Blameless and operational. Avoid "the platform is broken" rhetoric —
describe what failed, where, and what is needed to unblock you.
