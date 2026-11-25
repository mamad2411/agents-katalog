---
name: ux-flow-auditor
description: Traces user task flows with Playwright — click depth, step success, friction — and writes reports to .heyeddi/docs/ux-flows/. Use when measuring ease of use, clicks to complete a task, or onboarding friction. Not for static visual critique (use heyeddi-design critique) or layout screenshots (use visual-auditor).
version: 1.0.0
disable-model-invocation: true
---

# UX Flow Auditor

Task-oriented UX — how many clicks to achieve a goal, where users get stuck.

**All artifacts go under `.heyeddi/docs/` and `.heyeddi/audits/`** — never repo root.

## When to use

- "How many clicks to update settings?"
- Post-ship ease-of-use check
- Compare desktop vs mobile flow (separate flow JSON or viewport)
- Product acceptance: task completes within click budget

## Subagents (default)

See `reference/subagents.md`. Run `trace_flow.py` via **Task `shell`** (needs dev server + Playwright).

## Pipeline

```
init_ux_flows          → ux-flows.md index + example .flow.json
define steps in ux-flows/<task>.flow.json
trace_flow --task-id   → ux-flows/<task>.md + audit screenshot
agent adds friction notes to report
```

## Instructions

1. Ensure `.heyeddi/product.md` defines user tasks (optional context).
2. `python scripts/init_ux_flows.py --project-root <root>` once per project.
3. Add or edit ` .heyeddi/docs/ux-flows/<task-id>.flow.json` with steps (`expect`, `fill`, `click`).
4. Start dev server; set `DEV_SERVER_URL` if not `http://localhost:5173`.
5. `python scripts/trace_flow.py --task-id <id> --project-root <root> --check`
6. Append **Friction notes** to the generated markdown report.

## Flow JSON schema

```json
{
  "task_id": "update-profile",
  "goal": "User saves profile",
  "start_route": "/settings",
  "max_clicks": 4,
  "viewport_width": 1440,
  "steps": [
    { "action": "expect", "selector": ".settings .p-inputtext", "label": "Form visible" },
    { "action": "fill", "selector": ".settings input >> nth=0", "value": "Alex", "label": "Name" },
    { "action": "click", "selector": "button:has-text('Save')", "label": "Save" }
  ]
}
```

## `.heyeddi/` outputs

| Path | Purpose |
|------|---------|
| `.heyeddi/docs/ux-flows.md` | Index of tasks, budgets, last run |
| `.heyeddi/docs/ux-flows/<task>.flow.json` | Machine-readable steps |
| `.heyeddi/docs/ux-flows/<task>.md` | Human report + friction notes |
| `.heyeddi/audits/ux-flow/` | Step screenshots |

## Chain

- After `@design-handoff` / `@heyeddi-design` — verify tasks are completable
- `@visual-auditor` — layout proof; this skill — interaction proof
- `@engineering-excellence` — separate concern (code structure)
