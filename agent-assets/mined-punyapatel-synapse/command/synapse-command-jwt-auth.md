# Jwt Auth

Signs and verifies JSON Web Tokens using HMAC SHA256.

## Instructions

You have access to the Synapse `jwt_auth` skill located at `skills/jwt_auth/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/jwt_auth/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/jwt_auth/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `sign`
- `verify`

### Example Invocation
```json
{
  "operation": "sign",
  "payload": {
    "sub": "1234567890"
  },
  "secret": "my-secret"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/jwt_auth/jwt_auth.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/jwt_auth/package.json`
- Python: check `skills/jwt_auth/requirements.txt`
