---
name: edit-existing-process-diagram
description: Edit an existing Fluig/TOTVS `.process` diagram. Use this when the task is to inspect, modify, compare, or validate an existing process diagram instead of creating one from scratch, especially for node labels, lanes, colors, links, gateways, layout, or Graphiti/XMI compatibility.
---

# Edit Existing Process Diagram

This skill is for **editing an existing `.process` diagram safely**.

Use it when the user wants to:

- change labels, nodes, lanes, or colors in an existing `.process`
- fix visual rendering issues in Eclipse
- preserve semantic BPMN while changing Graphiti/XMI
- compare an edited `.process` against the original
- validate that a changed diagram is still structurally safe

Do not use this skill for greenfield process generation. Use it when there is already a `.process` file to inspect and edit.

## Workflow

1. Inspect the current diagram first.
2. Convert the user request into explicit semantic changes.
3. Change the smallest possible set of XML/business-object fields.
4. Re-validate the edited file.
5. Compare before/after so you can explain exactly what changed.

## Fast Path

For an existing `.process`, run:

```bash
python3 scripts/process_diagram_inspector.py --input /abs/path/process.process --format markdown
python3 scripts/process_diagram_validate.py --input /abs/path/process.process
```

If you need to compare before and after:

```bash
python3 scripts/process_diagram_diff.py \
  --before /abs/path/original.process \
  --after /abs/path/edited.process \
  --format markdown
```

## Editing Rules

- Prefer editing the existing diagram instead of regenerating from scratch.
- Preserve `bpmn2:*` business object ids whenever possible.
- Preserve `pi:ContainerShape` / `pi:FreeFormConnection` links to the same business object ids.
- If the change is semantic, update the business object first.
- If the change is visual, update the Graphiti shape tied to that business object.
- For lane and pool colors, keep `bpmn2:BpmnPool/@cores` and `bpmn2:BpmnSwimLane/@cores` aligned with the Graphiti `background` color refs.
- For Link / Link Receipt events, preserve the marker polygon shape, not just the outer ellipse.
- For `AssignmentControllerExecutorMechanism`, use numeric `returns` values in Eclipse-native XML. Do not emit textual `Last`.

## What to Inspect Before Editing

Use `scripts/process_diagram_inspector.py` to answer:

- what is the process id and diagram name?
- which pool and lanes exist?
- which colors are configured for pool and lanes?
- which node ids map to which BPMN types?
- which flows connect which ids?
- whether a node is a task, gateway, start/end event, or link event

If the request affects visuals only, still inspect the business object because many Fluig/Eclipse rendering issues are caused by semantic/visual mismatch.

## Validation Checklist

After editing:

1. XML parses successfully.
2. `pi:Diagram` exists.
3. every shape keeps a `link businessObjects="..."`
4. every `bpmn2:SequenceFlow` still has `sourceRef` and `targetRef`
5. pool/lane Graphiti colors still match business `cores`
6. Link / Link Receipt markers still exist
7. executor-mechanism controllers do not contain textual `returns`

Run:

```bash
python3 scripts/process_diagram_validate.py --input /abs/path/process.process --strict
```

## References

- Editing workflow and decision tree:
  - [references/editing-workflow.md](references/editing-workflow.md)
- Fluig `.process` structure cheat sheet:
  - [references/process-dialect-cheatsheet.md](references/process-dialect-cheatsheet.md)

## Output Expectations

When using this skill, report:

- which file was edited
- which node/lane/flow ids were changed
- whether the change was semantic, visual, or both
- validation result after the edit
- any residual risk, especially around Graphiti rendering
