# Code Executor

Executes Python or JavaScript code snippets in a temporary sandbox with timeout protection.

## Instructions

You have access to the Synapse `code_executor` skill located at `skills/code_executor/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/code_executor/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/code_executor/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `run_python`
- `run_js`

### Example Invocation
```json
{
  "operation": "run_python",
  "code": "print(\"Hello!\")"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/code_executor/code_executor.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/code_executor/package.json`
- Python: check `skills/code_executor/requirements.txt`
