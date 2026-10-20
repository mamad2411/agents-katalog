# Pdf Parser

Extracts text content from PDF files provided as base64 data.

## Instructions

You have access to the Synapse `pdf_parser` skill located at `skills/pdf_parser/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/pdf_parser/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/pdf_parser/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `extract_text`

### Example Invocation
```json
{
  "operation": "extract_text",
  "data": "<base64-pdf>"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/pdf_parser/pdf_parser.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/pdf_parser/package.json`
- Python: check `skills/pdf_parser/requirements.txt`
