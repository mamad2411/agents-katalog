# File Manager

Performs local file system operations: read, write, delete, list, and move files.

## Instructions

You have access to the Synapse `file_manager` skill located at `skills/file_manager/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/file_manager/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/file_manager/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `read`
- `write`
- `delete`
- `list`
- `move`

### Example Invocation
```json
{
  "operation": "list",
  "path": "./"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/file_manager/file_manager.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/file_manager/package.json`
- Python: check `skills/file_manager/requirements.txt`
