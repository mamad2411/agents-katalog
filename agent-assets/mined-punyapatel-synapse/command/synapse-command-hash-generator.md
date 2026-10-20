# Hash Generator

Generates cryptographic hashes (MD5, SHA-1, SHA-256, SHA-512) and UUIDs.

## Instructions

You have access to the Synapse `hash_generator` skill located at `skills/hash_generator/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/hash_generator/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/hash_generator/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `hash`
- `uuid`

### Example Invocation
```json
{
  "operation": "hash",
  "data": "Hello World",
  "algorithm": "sha256"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/hash_generator/hash_generator.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/hash_generator/package.json`
- Python: check `skills/hash_generator/requirements.txt`
