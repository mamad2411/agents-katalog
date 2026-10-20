# Git Operations

Performs Git operations: clone, status, commit, push, and pull.

## Instructions

You have access to the Synapse `git_operations` skill located at `skills/git_operations/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/git_operations/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/git_operations/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `clone`
- `status`
- `commit`
- `push`
- `pull`

### Example Invocation
```json
{
  "operation": "status",
  "repo_dir": "./"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/git_operations/git_operations.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/git_operations/package.json`
- Python: check `skills/git_operations/requirements.txt`
