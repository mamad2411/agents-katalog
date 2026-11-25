---
name: logic-rules
description: Build, edit, debug, and dedupe conditional logic rules inside a Process Street workflow revision — using the exact API shape confirmed to work (operator enum casing, targets-is-an-object with required widgetIds, FormField-only targets, dedupe flow). Use when someone says "add logic rule", "fix logic rule", "logic rule", "why isn't this rule firing", "conditional logic", "hide task when", "show task when", or "dedupe logic rules".
---

# PS Logic Rules Skill

## Purpose

Build, edit, debug, and dedupe conditional logic rules inside a Process Street workflow revision. Logic rules are the highest-error-rate PS surface in field experience — this skill encodes the exact patterns confirmed to work.

---

## When to Use

- Adding new conditional show/hide/require rules to a workflow
- Debugging "why isn't this task showing up"
- Cleaning up duplicate rules from prior builds
- Translating a business rule ("if county is Berkeley, route to inspector A") into the right API shape

---

## Reference

- the API reference (`reference/api-reference.md`) — endpoint list and confirmed revision-API patterns

---

## Rule Anatomy (Confirmed Shape)

> **Verified against the live spec.** Older anatomy (`conditions`/`subjectType`/`subjectId`, UI operator strings like `"Is not equals"`/`"Contains"`) is stale and will 400. The live shape is below, confirmed by the API reference (`reference/api-reference.md`).

```json
{
  "action": "Hide",
  "condition": { "or": [ { "and": [ { "widgetId": "<form-field-id>", "operator": "IsNot", "value": "Berkeley" } ] } ] },
  "targets": { "taskIds": ["<task-id-to-hide>"], "widgetIds": [] }
}
```

Key points:
- **`condition`** (singular) — top level is `{"or": [...]}`, each entry is `{"and": [ ... ]}`, each leaf is `{"widgetId", "operator", "value"}`. (`or` of `and` groups.)
- **`targets` is an object** — `{"taskIds": [...], "widgetIds": [...]}`. **`widgetIds` is REQUIRED even when empty** — omitting it is a 400.
- **`action`** — `Show` or `Hide` only.
- **Logic rules can't target content widgets** — `targets.widgetIds` only resolves FormField widgets; Text/Embed/Image are rejected as "not found". Gate at task level, or add the rule in the UI.

---

## Operators (API enum — exact, verified 2026-06-16)

Only these six are valid. The old UI-string operators (`Is equals`, `Is not equals`, `Contains`, `Does not contain`, `Is empty`, `Is not empty`, `Is before`, `Is after`) all return 400.

| Operator | Notes |
|---|---|
| `Is` | Exact match (for Select, match the option **name**) |
| `IsNot` | Inverse |
| `HasAnyValue` | Presence check — replaces "Is not empty". No `value` needed |
| `HasNoValue` | Absence check — replaces "Is empty". No `value` needed |
| `IsGreaterThan` | Number fields — Number **can** drive logic |
| `IsLessThan` | Number fields |

There is **no** `Contains` / `DoesNotContain` and no dedicated date before/after operator — all rejected. For substring/date-range branching, gate via a Date field constraint or a code task instead.

If unsure, fetch one working rule via `getWorkflowRevisionLogicRule` from a similar workflow and mirror its shape.

---

## Standard Flow

### Add a Rule

1. **Resolve IDs** — get `subjectId` (form field) and `taskIds` (targets) via `ps-audit` (or the CLI `template-export`) or the CLI `template-fields` (lists fields + IDs)
2. **List existing rules** — `listWorkflowRevisionLogicRules` — check for duplicates first
3. **Create** — `createWorkflowRevisionLogicRule` with confirmed shape above
4. **Verify** — re-fetch the rule, confirm the API echoed back what you sent

### Fix a Rule

1. **Get current rule** — `getWorkflowRevisionLogicRule`
2. **Identify the break** — usually one of:
   - Wrong operator (UI string like `"Is equals"` instead of the enum `Is`/`IsNot`/etc.)
   - `targets` flattened instead of object-wrapped, or missing `widgetIds: []`
   - Wrong `subjectId` (field was renamed or moved)
   - Stale rule referencing deleted task/field
3. **Update** — `updateWorkflowRevisionLogicRule` (full body, not patch)
4. **Re-verify**

### Dedupe Rules

1. `listWorkflowRevisionLogicRules`
2. Group by `(condition, targets, action)` — duplicates have identical bodies
3. Delete duplicates via `deleteWorkflowRevisionLogicRule`, keep oldest
4. Republish if workflow was live

---

## Select Widget Options Gotcha

If a rule conditions on a Dropdown/Select field value, the option string in `value` must exactly match the option's display label (not internal id). Verify by reading the widget's options array first.

---

## Trailing CT Race

If you're adding logic rules immediately after writing a code task widget, wait 2–5s before publishing. There is a known race where the rule references a widget the publish step can't yet see.

---

## Output

After any rule write/edit, return:
- Rule ID
- Confirmed echo from API (proves shape was accepted)
- Affected task names (resolved from IDs for readability)
- Warnings (duplicates found, stale references, etc.)

---

## Related Skills

- `ps-audit` (or the CLI `template-export`) — find existing rules + IDs to reference
- the CLI `template-fields` (lists fields + IDs) — resolve form field IDs by label
- `ps-build` — for fresh builds where rules are added in bulk
