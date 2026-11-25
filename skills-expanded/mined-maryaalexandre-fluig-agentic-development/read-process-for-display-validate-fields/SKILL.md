---
name: read-process-for-display-validate-fields
description: Read a Fluig/TOTVS `.process` diagram to build or revise `displayFields` and `validateForm` with real diagram awareness. Use this when an agent needs to inspect stages, lanes, gateways, assignments, and route-driving fields from an existing process before writing form rules.
---

# Read `.process` for `displayFields` and `validateForm`

Use this skill when the goal is to write or revise form events that depend on the workflow diagram:

- `displayFields.js`
- `validateForm.js`
- sometimes `beforeTaskSave.js` when route validation must be enforced server-side

This skill is for **reading the existing `.process` first**, then deriving form behavior from the real activity graph instead of guessing state ids or field responsibilities.

## What this skill is for

Use it when the agent needs to answer questions like:

- which activity ids should appear in the `switch (WKNumState)`?
- which lanes/roles are responsible for each editable stage?
- which gateway fields control routing and therefore must be validated?
- which tasks are human tasks vs service tasks vs subprocesses?
- which activities should be editable, readonly, or hidden in `displayFields`?
- which fields should be mandatory in `validateForm` because they decide the next path?

Do not use this skill for generic Fluig development without a `.process`. Use the Fluig development skill for Rhino/Fluig API rules.

## Workflow

1. Inspect the `.process`.
2. Build the activity matrix.
3. Identify interactive stages:
   - start
   - user tasks
   - subprocesses with form interaction
4. Identify route-driving fields from gateways.
5. Plan `displayFields` by stage.
6. Plan `validateForm` by stage and by route-driving field.
7. Generate or patch the JS skeleton only after the stage matrix is clear.

## Fast path

Inspect the process and generate the planning artifacts:

```bash
python3 scripts/process_activity_matrix.py \
  --input /abs/path/process.process \
  --format markdown

python3 scripts/process_form_rules_plan.py \
  --input /abs/path/process.process \
  --format markdown
```

If you want starter event files:

```bash
python3 scripts/generate_form_event_skeleton.py \
  --input /abs/path/process.process \
  --output-dir /abs/path/out
```

## Core rules

- Never guess activity ids from labels alone. Read them from the `.process`.
- Prefer the trailing numeric part of BPMN ids as the Fluig activity number:
  - `task12` -> `12`
  - `servicetask41` -> `41`
  - `subprocess105` -> `105`
- Treat only interactive stages as primary `displayFields` / `validateForm` cases:
  - start event
  - user task
  - interactive subprocess
- Service tasks and gateways are usually not direct form-interaction stages, but they still matter for:
  - route validation
  - readonly transitions
  - required field decisions
- Gateway condition fields are the strongest signal for `validateForm`.
- Lane ownership is the strongest signal for `displayFields` visibility and readonly behavior.

## How to derive rules from the diagram

### `displayFields`

Use the diagram to decide:

- who edits
- who only reviews
- which sections are visible in each stage
- which fields become readonly after a handoff

Typical pattern:

- start activity:
  - initialize defaults
  - reveal solicitation fields
- analyst/reviewer lane:
  - unlock review fields
  - keep requester-only fields readonly
- approval lane:
  - reveal only approval block, comments, and route choice fields
- finance/execution lane:
  - unlock execution-specific fields and keep previous decision fields readonly

### `validateForm`

Use the diagram to decide:

- which fields are mandatory in each activity
- which gateway-driving fields must be present before transition
- which branch-specific attachments or table rows must exist

Typical pattern:

- if a gateway uses field `aprovado`, `validateForm` must reject empty or invalid values before leaving the prior task
- if a task leads to multiple outgoing flows, validate the discriminator fields explicitly
- if a subprocess or task changes responsibility, validate the handoff data before movement

## References

- Strategy for reading the diagram:
  - [references/reading-process-for-form-events.md](references/reading-process-for-form-events.md)
- Strategy for `displayFields`:
  - [references/displayfields-from-process.md](references/displayfields-from-process.md)
- Strategy for `validateForm`:
  - [references/validateform-from-process.md](references/validateform-from-process.md)

## Output expectations

When using this skill, report:

- the `.process` file inspected
- the interactive activities found
- the gateway fields that drive routing
- the proposed stage matrix for `displayFields`
- the proposed stage matrix for `validateForm`
- any ambiguity that remains in the diagram
