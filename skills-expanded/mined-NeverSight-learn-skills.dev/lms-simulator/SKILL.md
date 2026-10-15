---
name: lms-simulator
description: Multi-role LMS browser simulator. Drives every action through agent-browser as the actor role and observes what every other role sees on screen. Catches UI/DB drift bugs (e.g. table cell shows -1 but modal still shows 0) that pure DB-assertion tests miss. Use when the user asks to "simulate roles", "test as different roles", "check that role X sees what role Y did", "auto simulate the flow", or wants to verify what each role sees after a chained multi-role action.
allowed-tools: Bash(npm run simulate:*), Bash(npx agent-browser:*), Bash(node scripts/simulator/*), Bash(curl:*), Bash(mkdir:*), Read, Write, Edit, Glob, mcp__supabase__execute_sql, mcp__supabase__list_projects, mcp__supabase__list_tables
---

# lms-simulator

Multi-role browser simulator. The user picks pre-defined `actions` (like `add_student`, `mark_present`, `approve_pending_payment`); the simulator runs them through a real Chrome session as the actor role and captures what every observer role sees — both the DOM **and** the DB — for each step. Drift between DOM and DB, or between roles, is the smoking gun.

This skill exists because pure DB-assertion tests miss the most painful bug class: *"the database is correct but what I see on screen is wrong"*. (See memory: `feedback_ui_drift_testing.md`.)

## When to use this skill

- "Simulate as different roles and tell me what each one sees"
- "Test that when role X creates Y, role Z can see it"
- "There's a drift between the table cell and the modal" / "what role A sees doesn't match role B"
- "Run the assistant_admin → instructor → company_admin flow and report"
- "Test the marketplace top-up with both roles"
- "Auto simulate the browser flow"

If the user just wants permission matrix testing, use `test-crud`. If they want single-role chained side-effects, use `test-behavior`. This skill is for **multi-role chained UI flows with cross-role observation**.

## Usage

```
/lms-simulator                                    # list available scenarios
/lms-simulator <scenario-name>                    # run a saved scenario
/lms-simulator new                                # interactive scenario builder
/lms-simulator actions                            # list all available actions
/lms-simulator actions show <action-name>         # show field schema + example for one action
/lms-simulator "<natural-language description>"   # ad-hoc: skill walks user through interactively, runs, saves YAML
```

Direct CLI (same thing, without the skill wrapper):

```
npm run simulate                                  # list scenarios
npm run simulate <scenario-name>                  # run
npm run simulate -- new                           # interactive builder
npm run simulate -- actions [list|show <name>]    # action registry
```

Output goes to `simulator-output/{run-timestamp}/report.md` plus `screenshots/<step>-<role>.png` and per-step `before.json` / `after.json` DB snapshots.

## Prerequisites (verify before running)

1. Dev server up: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/login` → 200
2. agent-browser installed: `npx --yes agent-browser --version` succeeds
3. Supabase MCP reachable: `mcp__supabase__list_projects` returns something
4. The 5 base auth profiles exist in agent-browser vault: `lms-super_admin`, `lms-group_admin`, `lms-company_admin`, `lms-assistant_admin`, `lms-instructor`. Test users created during a run get profiles named `lms-sim-<runId>-<handle>` and are deleted on teardown.

If any prereq fails, stop and report. Don't try to fix prereqs autonomously.

## Workflow when invoked

### When the user runs a known scenario

1. Find the scenario file under `.claude/skills/lms-simulator/scenarios/<name>.yaml`.
2. Run `node scripts/simulator/runner.mjs <name>`.
3. When the runner finishes, read `simulator-output/<latest-ts>/report.md` and surface:
   - the **drift table** (DOM vs DB vs expected per role per checkpoint),
   - any failed steps with the exact UI element that was wrong.
4. Don't paraphrase the report — quote the rows that matter.

### When the user wants to build a new scenario

1. Run `node scripts/simulator/runner.mjs new` — it prompts for scenario name, then loops:
   - "Add a step": user picks an action by name (autocompleted from registry).
   - For that action, the runner reads its declared `fields` schema and prompts for each one (showing required + optional + defaults).
   - User says "auto" for observers (means "every role under same company") or names specific roles.
2. The builder writes the YAML to `.claude/skills/lms-simulator/scenarios/<name>.yaml`.
3. Then ask the user if they want to run it now.

### When the user describes a scenario in natural language

1. Parse intent into actions from the registry. If an action doesn't exist, tell the user and offer to (a) skip that step or (b) approximate with the closest action.
2. Print the proposed YAML and ask for confirmation before saving + running.

## How to interpret the report

The report's killer feature is the **Drift table**:

```
| Step | Role | Field                                        | DOM | DB | Expected | Result      |
|------|------|----------------------------------------------|-----|----|----------|-------------|
| 2    | inst | attendance_table.sessions_remaining          | -1  | -1 | -1       | ✅          |
| 2    | inst | mark_present_modal.sessions_remaining        | 0   | -1 | -1       | ❌ DRIFT    |
| 2    | aa   | student_table.period_active                  | -1  | -1 | -1       | ✅          |
```

- `Field` follows `<role>.<surface>.<field>` — surface is `student_table`, `attendance_table`, `mark_present_modal`, `pending_payments_table`, etc.
- `DOM` = the value extracted from the actual rendered page.
- `DB` = the value from the SQL source of truth.
- `Expected` = what the action's `defaultExpectations` or the scenario's explicit `expect` block predicted.
- A `❌ DRIFT` is a UI/DB mismatch — that's the bug class the user cares most about. Always call these out first.

## Action library (Phase 1 ships with two; more added per Phase 2)

| Action | Surfaces affected | Notes |
|---|---|---|
| `add_student` | `/student` (student-table), `/attendance` (mark-attendance-table), `/pending-payments` | required: name, parent_email, course, package |
| `mark_present` | `/attendance` (table cell + modal), `/student` (period_active) | required: student, lesson, mission, activity |

To see live schema for any action: `npm run simulate -- actions show <id>`.

## Robustness rules (don't shortcut these)

- Always re-snapshot before any interaction (refs go stale on every DOM change).
- Never chain agent-browser commands with `&&` for sequences that mutate the DOM — use the helpers in `scripts/simulator/helpers/ui.mjs` which auto-resnapshot.
- Auth sessions time out — every interaction wraps a retry-once-with-relogin (already in `helpers/ui.mjs`).
- Use semantic locators (`find_input(label="Name")`) not raw refs whenever possible.

## Adding a new action

When the user asks for a new action (e.g. `add_voucher`, `transfer_branch`):

1. Create `scripts/simulator/actions/<id>.mjs` with `id`, `description`, `fields`, `defaultExpectations`, `ui` function.
2. Add to `actions/index.mjs` registry list.
3. Test with a 1-step scenario before adding to a multi-role chain.

The `ui` function receives `(browser, args)` where `browser` is a thin wrapper around agent-browser providing `open`, `click_button`, `fill_label`, `select_option`, `submit`, `screenshot` etc. — all auto-resnapshotting and retry-aware.

## Output structure

```
simulator-output/<ts>/
  report.md                    # the human-readable report (drift table, per-step breakdown)
  fixture.json                 # what fixtures were created + their IDs (for debugging)
  screenshots/
    01-actor-aa.png
    01-observer-inst.png
    01-observer-ca.png
    02-actor-inst.png
    02-observer-inst-modal.png  # the mark-present modal (the killer bug-catcher)
    ...
  snapshots/
    01-before.json              # DB snapshot before step 1
    01-after.json               # ... and after
    ...
```

If a run fails partway, fixtures still get cleaned up (the runner's teardown is in a `finally` block).
