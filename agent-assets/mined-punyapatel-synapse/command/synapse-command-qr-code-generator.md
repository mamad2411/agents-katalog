# Qr Code Generator

Generates QR code images from text and decodes QR codes from images.

## Instructions

You have access to the Synapse `qr_code_generator` skill located at `skills/qr_code_generator/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/qr_code_generator/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/qr_code_generator/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `generate`
- `decode`

### Example Invocation
```json
{
  "operation": "generate",
  "data": "https://example.com"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/qr_code_generator/qr_code_generator.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/qr_code_generator/package.json`
- Python: check `skills/qr_code_generator/requirements.txt`
