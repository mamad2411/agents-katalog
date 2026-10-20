# Screenshot Capture

Captures a screenshot of a web page URL via the Microlink API.

## Instructions

You have access to the Synapse `screenshot_capture` skill located at `skills/screenshot_capture/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/screenshot_capture/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/screenshot_capture/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `capture`

### Example Invocation
```json
{
  "operation": "capture",
  "url": "https://example.com"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/screenshot_capture/screenshot_capture.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/screenshot_capture/package.json`
- Python: check `skills/screenshot_capture/requirements.txt`
