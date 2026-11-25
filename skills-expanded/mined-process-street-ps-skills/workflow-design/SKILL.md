---
name: workflow-design
description: |-
  Turn a business process or SOP into a structured, build-ready Process Street workflow DESIGN — tasks, ordering, typed form fields, conditional logic, role assignment, approval gates, stop tasks, due-date rules, data-set lookups. Design only, no API writes; the artifact hands off to the build step (the ps-build skill via the v1.1 revision API). Use for /workflow-design or when someone says "design a workflow for [process]", "map this SOP into Process Street", "how should we structure this process in PS", "scope a workflow for [client]", or "turn this process doc into a PS design". Not the live build (that's a separate build step).
---

# When to use

Use when someone needs a process mapped into a PS workflow structure *before* building:
- `/workflow-design [process or SOP]`
- "design a workflow for X", "map this SOP into Process Street", "how should we structure this in PS", "scope a workflow for [client]"

**Design only — no API writes.** The artifact hands off to the build step (the `ps-build` skill via the v1.1 revision API). Inputs: a process description, SOP doc, discovery transcript, or compliance requirements.

# What it does

Decomposes the process into a PS structure (tasks → fields → logic → roles → approvals → automations), encodes the design choices the builder can actually execute (correct field types, API operator vocabulary, FormField-vs-content constraints), and emits a build-ready artifact with a handoff-notes block.

# Tools / capabilities

Routed to whatever's connected:
- Read the source process/SOP/transcript
- Read existing workflows for patterns if extending (no writes)
- Post the design artifact

# How to handle it

1. **Decompose into the backbone:** Trigger (manual / webhook / scheduled / CRM-event) → Phases → Handoffs (ownership transfers) → Completion (definition of done + what fires on completion).

2. **Enumerate tasks in execution order**, each with a `taskType`: `Standard` (human work + fields), `Approval` (binary sign-off), `Code` (Enterprise; API/orchestration), `AI` (Enterprise; only when determinism isn't required). Still **plan order fully up front** for a clean build — the toolkit's `edit-workflow` supports inserting later via `afterTask`, but a fresh build is cleanest laid in one ordered pass.

3. **Map form fields per task, typed** from the verified 17-type enum (per this repo's `reference/api-reference.md`, live-verified): `Text, Textarea, Select, MultiSelect, MultiChoice, Date, Email, Url, Number, Members, File, MultiFile, Table, Snippet, Hidden, SendRichEmail, Document`. Rules:
   - **Select/MultiSelect** for anything reportable or that drives logic
   - **Date** picker for deadlines/audit (prefer over computed dates)
   - **File is NOT creatable via the API** (it's rejected on create) — design **MultiFile** instead for any uploaded doc/evidence (max 10)
   - **Number CAN drive logic** via the `IsGreaterThan` / `IsLessThan` operators (added 2026) — design numeric branches directly; use a Select only for categorical branches
   - **`required` is NOT settable via the API** (UI-only) — note required fields in the design as a post-publish UI step
   - `required: true` at every compliance checkpoint
   - **Critical constraint:** any field a **code task** reads/writes, or a **logic rule** shows/hides, must be a **FormField** widget on a **Standard** task — never a content Text widget. Code tasks host zero widgets; Approval tasks host exactly one Text instruction widget. Design an adjacent "confirmation" Standard task to hold fields a code task writes to.

4. **Assign each task to a ROLE, not a person.** Build an assignee matrix (task → role → approver → backup). For dynamic assignment (e.g. county → inspector), design a **data-set lookup**: a code task reads the key field, queries the data set, writes the assignee back.

5. **Define conditional logic as rules** using the **API operator vocabulary**: `Is, IsNot, HasAnyValue, HasNoValue, IsLessThan, IsGreaterThan` (NOT `equals`/`contains`/`Is not equals` — those 400). Format: `IF <field> <op> <value> THEN Show/Hide <tasks or FormFields>`. Targets = tasks or FormField widgets only.

6. **Place approval gates** — binary Approve/Reject (+ reject-with-comments). There is **no "Approve with Changes"**: simulate via Reject → logic routes to a "Make Changes" task → loops back. Each gate needs a date-stamped sign-off field.

7. **Place stop tasks** — block all downstream until complete; sit one above any gate with a required field so it can't be bypassed. Trailing code tasks auto-fire at run creation — if a CT needs human input, place it after a stop task.

8. **Design due dates as relative rules** (anchored to trigger or another task's completion) — never hardcode dates; prefer native due dates over escalation code.

9. **Specify ≥1 completion automation** (Slack/email notify, CRM update) — native trigger, Zapier, or webhook.

10. **Run the quality checklist** and write the **Build Handoff Notes** (final task order, which fields are FormField-typed for code/logic, Enterprise features used, open questions). **The canonical builder is `ps-build`** (this repo's Claude-Code plugin / CLI — build from a structured plan, draft→publish→rollback). This design IS that plan; hand it to `/ps-build`. Upstream, a `gap-analysis` brief (what/why) can feed this design's inputs.

# Output

```
# Workflow Design: <Name>
Org/Folder: <target> · Plan: <Pro/Enterprise> · Trigger: <…> · Completion = <…> · Fires: <automation>
## Roles — <role — responsibility>
## Data Sets — | Set | Key | Returns | Used by |
## Tasks (in order)
### T1. <name> [taskType] — role · Stop: y/n · Due: <relative rule>
  | Label | FieldType | Required | Drives logic | Notes |
  (Code tasks: list inputData read + outputData written + which Standard task hosts them)
## Conditional Logic — | # | IF field | op | value | THEN | Targets |
## Approval Gates — | Gate | Approver | Approve→ | Reject→ | Sign-off |
## Automations — | Event | Action | Tool |
## Build Handoff Notes — order final; code/logic fields are FormFields; Enterprise features; open Qs
```

# Example

**Input:** `/workflow-design vendor approval & onboarding`

**Output (abridged):**
```
# Workflow Design: Vendor Approval & Onboarding
Trigger: manual (Procurement intake) · Completion = vendor active in ERP · Fires: Slack #procurement + ERP create (Zapier)
T1. Vendor Intake [Standard] — Coordinator · Stop: yes
  | Vendor Category | Select(Goods/Services/Software) | yes | YES drives Legal+IT branches |
  | Annual Spend Band | Select | yes | YES |
  | W-9 | File | yes | no |
T2. Risk & Threshold Lookup [Code] — inputData: Category, Spend Band → outputData writes to T3 textareas
T3. Review Routing Confirmation [Standard] — hosts the code-task write targets (Textareas)
T4. Legal Review [Standard] — hiddenByDefault   T5. IT Security Review [Standard] — hiddenByDefault
T6. Finance Approval [Approval] — Stop: yes · Approve→T7 · Reject→T6b
T6b. Revise & Resubmit [Standard] — loops back to T6 (simulates "approve with changes")
T7. ERP Activation [Standard]
Logic: 1) Category Is Software → Show T5 · 2) Category IsNot Goods → Show T4 · 3) Finance Approval Is Rejected → Show T6b
Handoff: order final T1→T7; all code/logic fields are FormFields on Standard tasks; 1 code task (Enterprise); stops T1,T6.
```
Note: code-task I/O lands on FormField textareas (not content widgets), API operators used, approve-with-changes simulated via reject-loop, chain order locked for one-pass build.

# Failure modes

- **Logic/code targets on content widgets** — only FormField widgets (Short/Long/Textarea/Select) accept logic/`outputMapping`; content Text/Embed/Image 400 "not found."
- **Task ordering** — plan the chain up front for a clean build; later insertion is possible (the `edit-workflow` plan's `afterTask: "<name>"` op, or `create-task --after-task-id`) but a one-pass ordered build is cleanest.
- **UI operator strings** — use `Is/IsNot/HasAnyValue/HasNoValue/IsLessThan/IsGreaterThan`; `equals`/`contains` 400.
- **Promising "Approve with Changes"** — doesn't exist; design the reject-loop.
- **File field on create** — the API rejects `File`; design `MultiFile` for any upload.
- **Code/AI tasks on non-Enterprise** — both Enterprise-only; flag plan tier.
- **Human task in a scheduled (all-code) workflow** — it stalls forever.
- **Trailing code task needing human input** — auto-fires at run creation; place after a stop task.
- **Assigning to individuals** — always roles (an unknown email auto-invites a Guest).

# Honesty & guardrails

- **Never fabricate** — design only what PS can actually build; flag plan-gated features; surface open questions rather than guessing.
- This skill never writes to the API — it produces a design; the build is a separate confirmed step (confirm before any state-changing action — draft-first — applies at build, not here).
