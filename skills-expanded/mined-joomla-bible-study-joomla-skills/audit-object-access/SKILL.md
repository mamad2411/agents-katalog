---
name: audit-object-access
description: Audit Joomla record access paths for IDOR, BOLA, ownership bypass, and cross-user data leakage — whether every attacker-selectable identifier is constrained to what the current user may see or change. Use when reviewing per-record data isolation in a Joomla extension, or when explicitly invoked for an object-level access audit. For whether an entry point has any check see audit-authz; for whether it checks the right permission see audit-controller-exposure.
---

# Audit Joomla object-level access

Audit whether every attacker-selectable record, collection, export, attachment, and API object is
constrained to what the current user may view or modify.

## Boundaries

This audit owns IDOR/BOLA and data isolation across models, tables, repositories, API serialisers,
downloads, AJAX handlers, plugins, modules, custom fields, web services, scheduled jobs, and
CLI-to-web bridges.

- Whether a controller has **any** access check belongs to `audit-authz`.
- Whether it checks the **correct** permission or asset at that entry point belongs to
  `audit-controller-exposure`.
- SQL syntax safety belongs to `audit-sql-filtering`.

This audit follows the identifier past the entry point, into the data operation and the response, to
find missing **per-object** constraints. A controller can pass every check the other three look for
and still hand back a record the user may not see.

## What to verify

Inventory attacker-selectable identifiers from routes, query and body data, arrays used for bulk
actions (`cid[]`), filters, aliases, filenames, and relationship IDs. Trace them through reads,
writes, deletes, state changes, copies, exports, and serialisation.

Account for the Joomla-specific dimensions of "may see": view access levels
(`$user->getAuthorisedViewLevels()`), category and item assets, ownership via `core.edit.own` and
`created_by`, publication state, language, and parent/child relationships on nested objects.

Check that:

- **List queries and counts apply the same constraints as single-record reads.** The classic Joomla
  split: `getItem()` checks access, `getListQuery()` forgets `whereIn('a.access', ...)`, and the list
  view leaks titles of records the detail view would refuse.
- API fields, relationships, totals, and error differences do not disclose inaccessible objects. A
  404-vs-403 difference is an oracle.
- **Bulk operations validate every ID** and fail safely, rather than authorising the first or the
  parent and looping over the rest.
- Submitted ownership, asset, state, user, group, or tenant fields cannot be mass-assigned beyond the
  actor's privileges — check what the form actually filters and what `Table::bind()` receives.
- Opaque or unguessable IDs are not treated as authorisation.
- Caches and helper methods do not reuse a privileged lookup in a less-privileged context.

Recognise constraints enforced centrally by a parent model, table, query helper, serialiser, plugin,
or database view before reporting.

## Workflow

### Step 1 — Audit

Report findings ordered by severity:

- **CRITICAL** — guest or low-privilege access to secrets, credentials, or broad private datasets; or
  cross-tenant destructive modification.
- **HIGH** — reading or modifying another user's protected records, ownership takeover, or
  publication of inaccessible records.
- **MEDIUM** — limited metadata disclosure, constrained cross-user access, or elevated-role isolation
  failure.
- **LOW** — inconsistent over-restriction, or defence-in-depth gaps with no current bypass.

For each finding identify the entry point, the identifier, the data operation, the missing
constraint, the effective actor, and the exposed action or data, with file and line references.
Include a representative request or call path where it makes the finding concrete.

Report and await user feedback. Do not change code in this step.

### Step 2 — Feedback round

The user is a subject matter expert and may reclassify or overrule a finding after giving more
context — a central constraint you did not read, or a record class that is public by design.

### Step 3 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

---

*Adapted for this suite from the `audit-object-access` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
