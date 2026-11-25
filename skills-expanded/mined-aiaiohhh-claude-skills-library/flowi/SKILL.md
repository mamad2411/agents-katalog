---
name: flowi
author: tyr0nin - AiAiOHHH
version: 1.0.0
user_invocable: true
description: Visual flowchart and diagram planning tool. Claude writes structured JSON to a .flowi/ directory, which renders as interactive, editable diagrams in the browser. Use for architecture planning, user flows, system design, state machines, and UI mockups.
---

# Flowi - Visual Planning & Diagramming

You are using Flowi, a visual feedback loop for planning. Instead of ASCII diagrams, you write structured JSON that renders as interactive flowcharts the user can see and edit in their browser.

## Workflow

1. **Create** `.flowi/` directory in the project root if it doesn't exist
2. **Write** JSON diagram files to `.flowi/*.json`
3. **Start the viewer** if not already running (tell the user to run the server)
4. **Read back** any changes the user makes visually
5. **Iterate** based on visual feedback

## Starting the Viewer

Tell the user to run this command in a separate terminal:

```bash
node ~/.claude/skills/flowi/server.js
```

This starts a dev server at `http://localhost:3333` that:
- Renders all `.flowi/*.json` files as interactive diagrams
- Live-reloads when you write new JSON
- Saves the user's visual edits back to the JSON files

## JSON Schema

Each `.flowi/*.json` file represents one diagram. Use this schema:

```json
{
  "title": "Diagram Title",
  "type": "flowchart",
  "nodes": [
    {
      "id": "unique-id",
      "type": "start|process|decision|end|io|database|component|note",
      "label": "Node Label",
      "description": "",
      "x": 100,
      "y": 100,
      "color": ""
    }
  ],
  "edges": [
    {
      "from": "source-node-id",
      "to": "target-node-id",
      "label": ""
    }
  ]
}
```

### Node Types

| Type | Shape | Use For |
|------|-------|---------|
| `start` | Rounded pill (green) | Entry points |
| `end` | Rounded pill (red) | Exit/terminal points |
| `process` | Rectangle (blue) | Actions, steps, functions |
| `decision` | Diamond (amber) | Conditionals, branches |
| `io` | Parallelogram (purple) | Input/output, API calls |
| `database` | Cylinder (teal) | Data stores, databases |
| `component` | Rounded rectangle (indigo) | UI components, modules |
| `note` | Dashed rectangle (gray) | Annotations, comments |

### Diagram Types

Use `"type"` to hint at layout:
- `"flowchart"` - Top-to-bottom flow (default)
- `"architecture"` - Free-form system diagram
- `"sequence"` - Left-to-right sequence
- `"statechart"` - State machine
- `"mockup"` - UI wireframe layout

## Layout Guidelines

- Place nodes on a grid: x increments of 200, y increments of 150
- Start nodes at top (y: 50), flow downward
- Decision branches: place "yes" path to the right, "no" path below
- Keep diagrams readable: max ~15 nodes per diagram, split into multiple files if larger
- Use descriptive file names: `auth-flow.json`, `database-schema.json`, `checkout-states.json`

## Reading User Edits

After the user edits a diagram visually:
1. Read the JSON file back from `.flowi/`
2. Note changed positions, added/removed nodes, edited labels
3. Ask the user what they'd like you to do with the changes
4. Update your implementation plan accordingly

## Example: Simple Auth Flow

Write to `.flowi/auth-flow.json`:

```json
{
  "title": "Authentication Flow",
  "type": "flowchart",
  "nodes": [
    { "id": "start", "type": "start", "label": "User visits app", "x": 300, "y": 50 },
    { "id": "check", "type": "decision", "label": "Has session?", "x": 300, "y": 200 },
    { "id": "login", "type": "process", "label": "Show login form", "x": 100, "y": 350 },
    { "id": "auth", "type": "io", "label": "Call auth API", "x": 100, "y": 500 },
    { "id": "dashboard", "type": "process", "label": "Load dashboard", "x": 500, "y": 350 },
    { "id": "end", "type": "end", "label": "App ready", "x": 300, "y": 650 }
  ],
  "edges": [
    { "from": "start", "to": "check" },
    { "from": "check", "to": "login", "label": "No" },
    { "from": "check", "to": "dashboard", "label": "Yes" },
    { "from": "login", "to": "auth" },
    { "from": "auth", "to": "dashboard", "label": "Success" },
    { "from": "dashboard", "to": "end" }
  ]
}
```

## Best Practices

- Always create the `.flowi/` directory first with `mkdir -p .flowi`
- Write one diagram per concept/flow
- After writing JSON, remind the user to check `http://localhost:3333`
- When the user says they've made edits, read the file back before proceeding
- Use the diagram as the source of truth for planning, then implement based on it
