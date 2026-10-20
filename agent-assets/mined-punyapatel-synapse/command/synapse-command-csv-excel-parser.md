# Csv Excel Parser

Parses and generates CSV/Excel data from structured input.

## Instructions

You have access to the Synapse `csv_excel_parser` skill located at `skills/csv_excel_parser/`.

When the user invokes this command, execute the appropriate handler:

- **TypeScript handler**: `skills/csv_excel_parser/index.js` — import and call `handler(params, context)`
- **Python handler**: `skills/csv_excel_parser/main.py` — import and call `await handler(params, context)`

### Supported Operations
- `parse`
- `generate`

### Example Invocation
```json
{
  "operation": "parse",
  "data": "name,age\\nAlice,30",
  "format": "csv"
}
```

### Execution Pattern

1. Parse the user's request to determine the operation and parameters.
2. Load the skill schema from `skills/csv_excel_parser/csv_excel_parser.skill.json` for parameter validation.
3. Run the handler with the constructed params object.
4. Return the formatted result to the user.

### Dependencies
- TypeScript: check `skills/csv_excel_parser/package.json`
- Python: check `skills/csv_excel_parser/requirements.txt`
