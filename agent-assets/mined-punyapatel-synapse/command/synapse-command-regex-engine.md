# Regex Engine

Tests, matches, replaces and extracts text using regular expressions.

## Instructions

You have access to the Synapse `regex_engine` skill located at `skills/regex_engine/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/regex_engine/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/regex_engine/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `test`
- `match`
- `replace`
- `extract`

### Example Invocation
```json
{
  "operation": "match",
  "pattern": "\\d+",
  "text": "abc 123 def 456",
  "flags": "g"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/regex_engine/regex_engine.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/regex_engine/package.json`
- Python: check `skills/regex_engine/requirements.txt`
