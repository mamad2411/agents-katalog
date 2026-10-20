# Json Transformer

Transforms, queries, flattens, diffs and validates JSON data using JSONPath, JSON Schema and deep operations.

## Instructions

You have access to the Synapse `json_transformer` skill located at `skills/json_transformer/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/json_transformer/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/json_transformer/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `query`
- `flatten`
- `unflatten`
- `diff`
- `validate`

### Example Invocation
```json
{
  "operation": "query",
  "data": {
    "users": [
      {
        "name": "Alice"
      }
    ]
  },
  "query": "$.users[0].name"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/json_transformer/json_transformer.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/json_transformer/package.json`
- Python: check `skills/json_transformer/requirements.txt`
