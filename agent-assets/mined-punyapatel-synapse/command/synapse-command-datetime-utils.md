# Datetime Utils

Parses, formats, converts timezones and calculates differences between dates.

## Instructions

You have access to the Synapse `datetime_utils` skill located at `skills/datetime_utils/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/datetime_utils/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/datetime_utils/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `now`
- `format`
- `diff`
- `convert_tz`

### Example Invocation
```json
{
  "operation": "now",
  "timezone": "Asia/Kolkata"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/datetime_utils/datetime_utils.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/datetime_utils/package.json`
- Python: check `skills/datetime_utils/requirements.txt`
