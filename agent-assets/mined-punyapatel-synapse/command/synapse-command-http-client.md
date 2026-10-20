# Http Client

Makes HTTP requests (GET, POST, PUT, DELETE, PATCH) with custom headers and payloads.

## Instructions

You have access to the Synapse `http_client` skill located at `skills/http_client/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/http_client/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/http_client/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `request`

### Example Invocation
```json
{
  "method": "GET",
  "url": "https://api.example.com/users"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/http_client/http_client.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/http_client/package.json`
- Python: check `skills/http_client/requirements.txt`
