# Email Sender

Sends emails via SMTP with HTML body support.

## Instructions

You have access to the Synapse `email_sender` skill located at `skills/email_sender/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/email_sender/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/email_sender/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `send`
- `send_template`

### Example Invocation
```json
{
  "operation": "send",
  "to": "user@example.com",
  "subject": "Test",
  "body": "<h1>Hello</h1>"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/email_sender/email_sender.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/email_sender/package.json`
- Python: check `skills/email_sender/requirements.txt`
