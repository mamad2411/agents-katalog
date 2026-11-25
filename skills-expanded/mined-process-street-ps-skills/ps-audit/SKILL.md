---
name: ps-audit
description: Audit and optimize an existing Process Street workflow — score it against best practices, surface issues, and optionally apply the fixes. Use when the user wants to review, improve, tighten, or optimize a workflow.
---

# Audit & optimize a Process Street workflow

Analyze a workflow, score it, recommend improvements grounded in `reference/best-practices.md`, and (with consent) apply the fixes via `ps-edit`.

**CLI:** `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" <command>` (plugin) or `scripts/process_street.py` (repo). Needs `PROCESS_STREET_API_KEY`.

## 1. Load the workflow

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" template-export <workflowId>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/process_street.py" template-rules <workflowId> --resolve
```
If you only have a name, `process_street.py workflows` to find the ID.

## 2. Score against the 10-point scorecard

Use the scorecard in `reference/best-practices.md`. For each step and field, check:

- **Structure**: outcome-based name? 6–15 well-ordered, verb-named steps? any step doing two jobs?
- **Data quality**: right field types, or free text where a `Select`/`Date`/`Number` belongs? fields no one needs? missing required fields?
- **Flow**: would conditional logic hide irrelevant steps? are stops/approvals justified or just friction? are approvals configured with subject tasks?
- **Accountability**: does every task have an owner (assignment rule)? dynamic due dates?
- **Automation**: any human re-keying data between systems that a Code/AI task or webhook could remove? hard-coded option lists that should be a Data Set?
- **Polish**: branded first step, help text where ambiguous?

## 3. Present findings

Give a short report:
- **Current score** (X/10) with the 2–3 biggest gaps.
- **Recommendations**, each tagged: `[quick win]` (apply now via API), `[redesign]` (needs restructuring), or `[UI-only]` (required flag, theming, integrations).
- **Projected improvement** if adopted.

## 4. Offer to apply

Ask which to implement. For the API-doable ones, build an edit plan and hand off to the **ps-edit** flow (draft → preview → publish → rollback). Re-export to confirm. List any UI-only items the user must do themselves.

Almost every structural fix is API-applicable: change field types, add logic, add due-date/assignment rules, add/remove steps and fields, add content. Only required-field flagging, theming, org settings, and deep integrations are UI-only.
