---
name: design-technical-options
description: Use when a plan makes a costly architecture, module-boundary, or dependency decision. Publish 2–3 structured options with an optional mermaid sketch before you submit the plan.
---

## Gate (all three required)

Publish a technical set only when **all** of these hold:

1. At least two approaches are genuinely viable (no strawmen).
2. They differ materially in effort, risk, reversibility, or maintenance cost.
3. A wrong pick is costly to undo: schema, public API, module boundaries, or a new dependency.

If any check fails, pick one approach in the plan and list the alternatives you rejected, one line each. Do **not** publish a set.

## When this applies

Kinds: `architecture`, `module`, `dependency`. Not `refactor`, and not mid-implementation — planning runs only.

At most **2** technical sets per plan. If you need more, propose a split. UI options (`design:design-ui-options`) are separate.

## How to publish

1. `design__list` first.
2. `design__create` with `kind` set to `architecture`, `module`, or `dependency`.
3. `design__publish` with 2 options by default (3 max). Do **not** call `design__write` and do **not** set `entry`.
4. Each option needs: `id`, `title`, `changes`, `effort`, `risk`, `reversibility`, `rulesOut`, and optional `sketch` (mermaid `flowchart` or `graph` only; no `%%{init}`).
5. Pass `recommendedOptionId` and a one-line `recommendedReason`.
6. Put a `{{design:<setId>}}` marker under the plan section that choice decides.
7. Write the plan around the recommended (or already selected) option.

On a revision, the newest change request alone decides whether to republish that set. Keep each live set's marker under its section. When the gate fails for a previously published decision, drop that marker and list rejected alternatives in the plan instead.
