# Webhook Handler

Parses webhook payloads and validates HMAC signatures for services like Stripe and GitHub.

## Instructions

You have access to the Synapse `webhook_handler` skill located at `skills/webhook_handler/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/webhook_handler/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/webhook_handler/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `parse`
- `validate_signature`

### Example Invocation
```json
{
  "operation": "parse",
  "payload": "{\"event\":\"push\"}"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/webhook_handler/webhook_handler.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/webhook_handler/package.json`
- Python: check `skills/webhook_handler/requirements.txt`
