---
name: maintaining-user-flows
description: >-
  Use when adding, retiring, renaming, merging, splitting, or checking sync for
  a canonical user flow across the User-Flows-Details Sheet and Linear "User Flow" labels.
  Flow list maintenance only — does not author functional specs or track implementation.
argument-hint: "add|retire|rename|merge|split|drift [canonical-id(s)]"
---

# Maintaining User Flows

## When to Use

Trigger conditions:

- User asks to add a new canonical user flow to the Flow Inventory
- User asks to retire an existing flow (update col H to `retired`)
- User asks to rename a canonical ID in col B (and optionally update col E title)
- User asks to merge two flows into one new flow
- User asks to split one flow into two new flows
- User asks to check sync, show drift, or compare sheet and Linear labels (drift operation)

Not this skill:

- Does not create `docs/functional/` folders or author functional specs
- Does not file or track implementation Linear issues

## Checklist

- [ ] Phase 0 — Preflight (gws auth, load sheet, load Linear labels)
- [ ] Phase 1 — Identify operation and arguments
- [ ] Phase 2 — Validate inputs (see per-operation reference)
- [ ] Phase 3 — Change Preview (see per-operation reference)
- [ ] Phase 4 — Execute changes (see per-operation reference)
- [ ] Phase 5 — Confirm outputs (see per-operation reference)

## Phase 0 — Preflight

1. Verify `gws` is installed and `gws auth status` exits zero. If not, abort: `Run gws auth login first, then retry.` (see `references/sheet-ops.md §2`)
2. Load the full Flow Inventory sheet via `references/sheet-ops.md §3`. Cache the result — do not re-fetch mid-invocation.
3. Load all Linear "User Flow" child labels via `mcp__linear__list_issue_labels`. Cache the result.
4. If the cached CSV does not have exactly 13 columns, abort: "Sheet schema has drifted."
5. Confirm the operation from the invocation context (argument or user message). If ambiguous, ask once: "Which operation? add / retire / rename / merge / split / drift"

## Phase 1 — Identify Operation and Arguments

Route by operation using this table:

| Operation | Reference | Required args |
|---|---|---|
| add | `references/add.md` | canonical-id, repo, category, title, status, persona |
| retire | `references/retire.md` | canonical-id |
| rename | `references/rename.md` | old-id, new-id (and optionally new-title) |
| merge | `references/merge.md` | id-a, id-b, new-id, new-title |
| split | `references/split.md` | source-id, new-id-1, new-title-1, new-id-2, new-title-2 |
| drift | `references/drift.md` | — |

If any required arg is missing, ask the user before proceeding.

## Phases 2–5

Phases 2–5 are operation-specific and delegated to the matching `references/<operation>.md` file. The Phase 3 confirmation gate is universal: present the Change Preview block and wait for the user to respond "yes" or "confirm". If the user responds with anything else, do not write any changes and report: "Operation cancelled. No changes were made."

## Safety Rails

- Never write to the sheet without showing the Change Preview and receiving explicit approval ("yes" or "confirm").
- Never delete a sheet row — retire only via col H update (`retired`).
- Never write to col L (Filename HYPERLINK formula — managed by sheet owners).
- Never assume column layout; abort if CSV does not have exactly 13 columns (see `references/sheet-ops.md §7`).
- Never create a duplicate canonical ID in the sheet or a duplicate Linear label.
- Valid `status` values: `not-started`, `early`, `feature-complete`, `working`, `parked`, `retired`
- Linear label archiving is always a manual step in Linear settings — the MCP has no archive call.

## Error Reporting

If any Linear mutation fails during a batch operation (re-tag, label create):

- Log the failure with issue identifier and error message.
- Continue processing remaining items.
- Surface all failures at the end: `Failed to re-tag: VD-1234 (403 Forbidden)`

Never silently swallow a failure.
