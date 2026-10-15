---
name: raise
description: "Turns a Plan into dependency-aware beads issues. Use after 'plan' and before 'ship'. Use when the user has a completed Plan and wants to create trackable issues."
---

# Follow these steps in order, one at a time.

## Input

1. Ask for the completed `Plan`.
2. _After_ receiving the `Plan`, read the [cheat sheet](./references/beads-cheat-sheet.md) to understand how beads works.
3. Read the rules below for how we will convert the `Plan` into beads issues.

### Rules

- Convert each slice from 'Section 4: Slice Breakdown' into an epic.
- `br create "<Slice Name>" --type epic --priority <P> --labels "<context labels>"`
- Create child issues under each epic using `--parent <epic-id>`.
- Each child issue must represent one smallest executable observable behavior that can be implemented and proved through the supported entry points.
- Write each child issue description using the [issue template](./references/issue-template.md).
- Order child issues so the simplest happy-path behaviour comes first.
- Child issues must be suitable for TDD red-green-refactor execution.
- Add blocking dependencies with: `br dep add <blocked-id> <blocking-id>`
- Use 'Section 5: Delivery Sequence Summary' to add dependencies between epics in execution order.
- Use labels to encode bounded context and issue category.

## Output

1. Turn the `Plan` into beads issues starting with:

```bash
cd my-project
br init
```

2. _After_ turning the entire plan into beads issues tell the user to proceed to the 'ship' skill.
