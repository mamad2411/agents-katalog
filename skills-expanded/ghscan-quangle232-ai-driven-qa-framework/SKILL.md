---
name: publish-testcases
description: Publish approved test cases to the team's test-management tool. Use for "export test cases", "publish to Xray/TestRail", "export to Excel", "push cases to <tool>". Takes the approved canonical JSON and creates/updates cases in Excel · Xray · TestRail, attaches Excel to the parent Jira story, and updates statuses after runs.
---

# publish-testcases — approved JSON → test management

Standalone version of the qa-agent publish step. **Only after `I approve`** (frozen JSON).

## Input
The approved canonical JSON (`json-contract.md` shape) — from the qa-agent design half or a file.

## Target (client-chosen, `meta.testMgmt` / `TEST_MGMT`; default excel) — see
`qa-agent/references/test-management.md`
- **excel** — `node .agents/skills/qa-agent/scripts/export-testcases-excel.mjs --json <file> --out test-output/ai/TestCases_<feature>.xlsx`; attach to the **parent Jira story only** (never a sub-task).
- **xray** — create Xray Test issues in Jira from the JSON (Jira/Xray MCP), linked to the story.
- **testrail** — needs TestRail config + the TestRail MCP; create section/cases + a run.

## Rules
- Do NOT publish before approval. JSON is the source of truth; re-export from it, never hand-edit the xlsx.
- Persist the frozen JSON under `docs/ai/`. After execution, push pass/fail statuses back (Xray Test
  Execution / TestRail results / Excel Result column) — this is the "update status" step read-report/run-tests feed.
- If the target's MCP/config is missing → fall back to Excel and note the gap in `docs/ai/`.
