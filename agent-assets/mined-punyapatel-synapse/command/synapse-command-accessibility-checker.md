# Accessibility Checker

Scans HTML for accessibility (a11y) issues: missing alt text, ARIA labels, form labels, lang attribute.

## Instructions

You have access to the Synapse `accessibility_checker` skill located at `skills/accessibility_checker/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/accessibility_checker/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/accessibility_checker/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `analyze`

### Example Invocation
```json
{
  "operation": "analyze",
  "html": "<html><body><img src=\"x.png\"></body></html>"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/accessibility_checker/accessibility_checker.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/accessibility_checker/package.json`
- Python: check `skills/accessibility_checker/requirements.txt`
