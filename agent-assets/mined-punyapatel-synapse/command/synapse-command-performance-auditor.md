# Performance Auditor

Audits HTML for frontend performance issues: blocking scripts, lazy loading, DOM size, inline styles.

## Instructions

You have access to the Synapse `performance_auditor` skill located at `skills/performance_auditor/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/performance_auditor/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/performance_auditor/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `analyze`

### Example Invocation
```json
{
  "operation": "analyze",
  "html": "<html><head><script src=\"app.js\"></script></head></html>"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/performance_auditor/performance_auditor.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/performance_auditor/package.json`
- Python: check `skills/performance_auditor/requirements.txt`
