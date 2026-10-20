# Calculator

Evaluates mathematical expressions and performs arithmetic operations.

## Instructions

You have access to the Synapse `calculator` skill located at `skills/calculator/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/calculator/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/calculator/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `evaluate`

### Example Invocation
```json
{
  "operation": "evaluate",
  "expression": "(2 + 3) * 4 / 2"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/calculator/calculator.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/calculator/package.json`
- Python: check `skills/calculator/requirements.txt`
