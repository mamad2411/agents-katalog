# Data Visualizer

Generates chart images (bar, line, pie, scatter) from structured data.

## Instructions

You have access to the Synapse `data_visualizer` skill located at `skills/data_visualizer/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/data_visualizer/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/data_visualizer/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `generate_chart`

### Example Invocation
```json
{
  "operation": "generate_chart",
  "chart_type": "bar",
  "data": {
    "labels": [
      "A",
      "B",
      "C"
    ],
    "values": [
      10,
      20,
      30
    ]
  }
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/data_visualizer/data_visualizer.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/data_visualizer/package.json`
- Python: check `skills/data_visualizer/requirements.txt`
